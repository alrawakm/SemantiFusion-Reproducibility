from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path


REQUIRED_FIELDS = ("sample_id", "reference_id", "original_path", "stego_path")


@dataclass(frozen=True)
class PairRecord:
    sample_id: str
    reference_id: str
    original_path: str
    stego_path: str
    payload_bits: str = ""
    message_bits_path: str = ""
    recovered_bits_path: str = ""
    split: str = ""
    model_id: str = ""
    checkpoint_sha256: str = ""
    message_seed: str = ""
    generation_seed: str = ""


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def load_pair_manifest(path: str | Path) -> list[PairRecord]:
    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in REQUIRED_FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Manifest is missing required fields: {', '.join(missing)}")
        records = []
        for row in reader:
            values = {field: (row.get(field) or "").strip() for field in PairRecord.__dataclass_fields__}
            records.append(PairRecord(**values))
    return records


def validate_pair_records(
    records: list[PairRecord],
    manifest_dir: str | Path = ".",
    check_files: bool = True,
) -> list[str]:
    errors: list[str] = []
    sample_ids: set[str] = set()
    reference_splits: dict[str, str] = {}
    base = Path(manifest_dir)

    for index, record in enumerate(records, start=2):
        if not all((record.sample_id, record.reference_id, record.original_path, record.stego_path)):
            errors.append(f"row {index}: required value is empty")
        if record.sample_id in sample_ids:
            errors.append(f"row {index}: duplicate sample_id {record.sample_id}")
        sample_ids.add(record.sample_id)

        if record.split:
            previous = reference_splits.get(record.reference_id)
            if previous and previous != record.split:
                errors.append(
                    f"row {index}: reference {record.reference_id} appears in both {previous} and {record.split}"
                )
            reference_splits[record.reference_id] = record.split

        if record.payload_bits:
            try:
                if int(record.payload_bits) <= 0:
                    raise ValueError
            except ValueError:
                errors.append(f"row {index}: payload_bits must be a positive integer")

        if record.checkpoint_sha256 and (
            len(record.checkpoint_sha256) != 64
            or any(character not in "0123456789abcdefABCDEF" for character in record.checkpoint_sha256)
        ):
            errors.append(f"row {index}: checkpoint_sha256 is not a SHA-256 digest")

        if check_files:
            for field_name in ("original_path", "stego_path", "message_bits_path", "recovered_bits_path"):
                relative = getattr(record, field_name)
                if relative and not (base / relative).is_file():
                    errors.append(f"row {index}: {field_name} does not exist: {relative}")
    return errors


def write_pair_manifest(path: str | Path, records: list[PairRecord]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(PairRecord.__dataclass_fields__)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: getattr(record, field) for field in fields})

