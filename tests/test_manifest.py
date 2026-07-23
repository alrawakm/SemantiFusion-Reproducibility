import unittest

from semantifusion_repro.manifest import PairRecord, validate_pair_records


class ManifestTests(unittest.TestCase):
    def test_duplicate_sample_id(self) -> None:
        records = [
            PairRecord("sample", "ref-1", "a.png", "b.png", split="train"),
            PairRecord("sample", "ref-2", "c.png", "d.png", split="test"),
        ]
        errors = validate_pair_records(records, check_files=False)
        self.assertTrue(any("duplicate sample_id" in error for error in errors))

    def test_reference_split_leakage(self) -> None:
        records = [
            PairRecord("sample-1", "ref-1", "a.png", "b.png", split="train"),
            PairRecord("sample-2", "ref-1", "c.png", "d.png", split="test"),
        ]
        errors = validate_pair_records(records, check_files=False)
        self.assertTrue(any("appears in both" in error for error in errors))

    def test_valid_records(self) -> None:
        records = [
            PairRecord("sample-1", "ref-1", "a.png", "b.png", payload_bits="256", split="test")
        ]
        self.assertEqual(validate_pair_records(records, check_files=False), [])


if __name__ == "__main__":
    unittest.main()

