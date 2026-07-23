from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image


def load_rgb(path: str | Path) -> np.ndarray:
    """Load an image as an RGB float64 array in the range 0 to 255."""
    with Image.open(path) as image:
        return np.asarray(image.convert("RGB"), dtype=np.float64)


def _check_image_pair(reference: np.ndarray, candidate: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    reference = np.asarray(reference, dtype=np.float64)
    candidate = np.asarray(candidate, dtype=np.float64)
    if reference.shape != candidate.shape:
        raise ValueError(f"Image shapes differ: {reference.shape} != {candidate.shape}")
    if reference.ndim not in (2, 3):
        raise ValueError("Images must be two-dimensional or channel-last arrays")
    return reference, candidate


def psnr(reference: np.ndarray, candidate: np.ndarray, data_range: float = 255.0) -> float:
    """Return peak signal-to-noise ratio in decibels."""
    reference, candidate = _check_image_pair(reference, candidate)
    error = np.mean((reference - candidate) ** 2)
    if error == 0:
        return float("inf")
    return float(10.0 * np.log10((data_range**2) / error))


def _gaussian_kernel(size: int = 11, sigma: float = 1.5) -> np.ndarray:
    if size < 1 or size % 2 == 0:
        raise ValueError("Gaussian window size must be a positive odd integer")
    coordinates = np.arange(size, dtype=np.float64) - size // 2
    kernel = np.exp(-(coordinates**2) / (2.0 * sigma**2))
    return kernel / kernel.sum()


def _gaussian_filter(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Apply a separable Gaussian filter without requiring SciPy."""
    radius = len(kernel) // 2
    if image.ndim == 2:
        image = image[..., None]

    height, width, channels = image.shape
    vertical_input = np.pad(image, ((radius, radius), (0, 0), (0, 0)), mode="reflect")
    vertical = np.zeros((height, width, channels), dtype=np.float64)
    for offset, weight in enumerate(kernel):
        vertical += weight * vertical_input[offset : offset + height, :, :]

    horizontal_input = np.pad(vertical, ((0, 0), (radius, radius), (0, 0)), mode="reflect")
    filtered = np.zeros((height, width, channels), dtype=np.float64)
    for offset, weight in enumerate(kernel):
        filtered += weight * horizontal_input[:, offset : offset + width, :]

    return filtered


def ssim(
    reference: np.ndarray,
    candidate: np.ndarray,
    data_range: float = 255.0,
    window_size: int = 11,
    sigma: float = 1.5,
) -> float:
    """Return mean windowed structural similarity for a grayscale or RGB pair."""
    reference, candidate = _check_image_pair(reference, candidate)
    if min(reference.shape[0], reference.shape[1]) < window_size:
        raise ValueError("Images are smaller than the SSIM window")

    if reference.ndim == 2:
        reference = reference[..., None]
        candidate = candidate[..., None]

    kernel = _gaussian_kernel(window_size, sigma)
    mean_reference = _gaussian_filter(reference, kernel)
    mean_candidate = _gaussian_filter(candidate, kernel)

    mean_reference_sq = mean_reference**2
    mean_candidate_sq = mean_candidate**2
    mean_product = mean_reference * mean_candidate

    variance_reference = _gaussian_filter(reference**2, kernel) - mean_reference_sq
    variance_candidate = _gaussian_filter(candidate**2, kernel) - mean_candidate_sq
    covariance = _gaussian_filter(reference * candidate, kernel) - mean_product

    variance_reference = np.maximum(variance_reference, 0.0)
    variance_candidate = np.maximum(variance_candidate, 0.0)

    c1 = (0.01 * data_range) ** 2
    c2 = (0.03 * data_range) ** 2
    numerator = (2.0 * mean_product + c1) * (2.0 * covariance + c2)
    denominator = (mean_reference_sq + mean_candidate_sq + c1) * (
        variance_reference + variance_candidate + c2
    )
    score = numerator / np.maximum(denominator, np.finfo(np.float64).eps)
    return float(np.mean(score))


def bit_error_rate(message: Iterable[int], recovered: Iterable[int]) -> float:
    """Return the fraction of unequal bits."""
    message_array = np.asarray(list(message), dtype=np.uint8)
    recovered_array = np.asarray(list(recovered), dtype=np.uint8)
    if message_array.shape != recovered_array.shape:
        raise ValueError("Transmitted and recovered bit arrays must have the same length")
    if message_array.size == 0:
        raise ValueError("Bit arrays must not be empty")
    if not np.isin(message_array, (0, 1)).all() or not np.isin(recovered_array, (0, 1)).all():
        raise ValueError("Bit arrays may contain only 0 and 1")
    return float(np.mean(message_array != recovered_array))


def read_bits(path: str | Path) -> np.ndarray:
    """Read 0/1 values from a text file, ignoring spaces, commas, and line breaks."""
    text = Path(path).read_text(encoding="utf-8")
    compact = "".join(character for character in text if character not in " \t\r\n,")
    if not compact or any(character not in "01" for character in compact):
        raise ValueError(f"Invalid bit file: {path}")
    return np.fromiter((int(character) for character in compact), dtype=np.uint8)

