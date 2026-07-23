from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

from .manifest import PairRecord, sha256_file


def validate_archive_artifact(artifact_path: str | Path, provenance_path: str | Path) -> list[str]:
    artifact = Path(artifact_path)
    provenance = json.loads(Path(provenance_path).read_text(encoding="utf-8"))
    errors: list[str] = []

    if not artifact.is_file():
        return [f"artifact is missing: {artifact}"]
    if sha256_file(artifact) != provenance["sha256"]:
        errors.append("qualitative artifact SHA-256 does not match provenance.json")
    with Image.open(artifact) as image:
        if image.width != int(provenance["width"]) or image.height != int(provenance["height"]):
            errors.append("qualitative artifact dimensions do not match provenance.json")
    return errors


def _font(size: int) -> ImageFont.ImageFont:
    for name in ("DejaVuSans.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_pair_grid(
    records: list[PairRecord],
    manifest_dir: str | Path,
    output_path: str | Path,
    limit: int = 3,
    panel_size: tuple[int, int] = (640, 420),
) -> None:
    if limit < 1:
        raise ValueError("limit must be positive")
    selected = records[:limit]
    if not selected:
        raise ValueError("manifest has no records")

    base = Path(manifest_dir)
    panel_width, panel_height = panel_size
    margin = 24
    title_height = 54
    label_height = 36
    row_height = label_height + panel_height + margin
    canvas = Image.new(
        "RGB",
        (2 * panel_width + 3 * margin, title_height + len(selected) * row_height),
        "white",
    )
    draw = ImageDraw.Draw(canvas)
    heading = _font(28)
    label = _font(18)
    draw.text((margin + panel_width // 2, 8), "Original", fill="black", font=heading, anchor="ma")
    draw.text(
        (2 * margin + panel_width + panel_width // 2, 8),
        "Stego",
        fill="black",
        font=heading,
        anchor="ma",
    )

    for row_index, record in enumerate(selected):
        top = title_height + row_index * row_height
        draw.text(
            (canvas.width // 2, top),
            record.reference_id,
            fill="black",
            font=label,
            anchor="ma",
        )
        with Image.open(base / record.original_path) as original_file:
            original = ImageOps.contain(original_file.convert("RGB"), panel_size)
        with Image.open(base / record.stego_path) as stego_file:
            stego = ImageOps.contain(stego_file.convert("RGB"), panel_size)

        image_top = top + label_height
        left_x = margin + (panel_width - original.width) // 2
        right_x = 2 * margin + panel_width + (panel_width - stego.width) // 2
        canvas.paste(original, (left_x, image_top + (panel_height - original.height) // 2))
        canvas.paste(stego, (right_x, image_top + (panel_height - stego.height) // 2))

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, format="PNG", optimize=True)

