import tempfile
import unittest
from pathlib import Path

from PIL import Image

from semantifusion_repro.manifest import PairRecord
from semantifusion_repro.qualitative import build_pair_grid


class QualitativeFigureTests(unittest.TestCase):
    def test_pair_grid_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            Image.new("RGB", (64, 48), (20, 30, 40)).save(root / "original.png")
            Image.new("RGB", (64, 48), (21, 30, 40)).save(root / "stego.png")
            records = [
                PairRecord(
                    sample_id="sample-1",
                    reference_id="reference-1",
                    original_path="original.png",
                    stego_path="stego.png",
                )
            ]
            output = root / "figure.png"
            build_pair_grid(records, root, output, limit=1, panel_size=(128, 96))
            with Image.open(output) as figure:
                self.assertGreater(figure.width, 256)
                self.assertGreater(figure.height, 96)


if __name__ == "__main__":
    unittest.main()

