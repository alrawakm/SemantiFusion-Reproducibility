import tempfile
import unittest
from pathlib import Path

from semantifusion_repro.tables import reproduce_tables, validate_aggregate_tables


class TableTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]

    def test_aggregate_values_are_consistent(self) -> None:
        errors = validate_aggregate_tables(
            self.root / "data" / "aggregate" / "primary_comparison.csv",
            self.root / "data" / "aggregate" / "payload_results.csv",
        )
        self.assertEqual(errors, [])

    def test_table_export(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            reproduce_tables(self.root, output)
            self.assertIn("SemantiFusion", (output / "primary_comparison.tex").read_text())
            self.assertIn("1024", (output / "payload_results.md").read_text())


if __name__ == "__main__":
    unittest.main()

