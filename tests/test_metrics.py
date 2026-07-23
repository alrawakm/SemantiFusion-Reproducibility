import math
import unittest

import numpy as np

from semantifusion_repro.metrics import bit_error_rate, psnr, ssim


class MetricTests(unittest.TestCase):
    def test_identical_images(self) -> None:
        image = np.full((32, 32, 3), 127, dtype=np.uint8)
        self.assertTrue(math.isinf(psnr(image, image)))
        self.assertAlmostEqual(ssim(image, image), 1.0, places=12)

    def test_constant_offset_psnr(self) -> None:
        reference = np.zeros((32, 32, 3), dtype=np.uint8)
        candidate = np.full((32, 32, 3), 10, dtype=np.uint8)
        self.assertAlmostEqual(psnr(reference, candidate), 28.1308036087, places=8)

    def test_bit_error_rate(self) -> None:
        self.assertAlmostEqual(bit_error_rate([0, 1, 1, 0], [0, 0, 1, 1]), 0.5)

    def test_bit_length_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            bit_error_rate([0, 1], [0])


if __name__ == "__main__":
    unittest.main()

