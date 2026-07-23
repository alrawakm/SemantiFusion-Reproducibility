from __future__ import annotations

import json
from pathlib import Path

from .qualitative import validate_archive_artifact
from .tables import validate_aggregate_tables


def validate_release(repo_root: str | Path) -> list[str]:
    root = Path(repo_root)
    errors: list[str] = []
    required = (
        "README.md",
        "REPRODUCIBILITY_STATUS.md",
        "config.json",
        "data/aggregate/primary_comparison.csv",
        "data/aggregate/payload_results.csv",
        "artifacts/qualitative/provenance.json",
        "artifacts/qualitative/visual_coco_original_stego.png",
    )
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"required file is missing: {relative}")

    config_path = root / "config.json"
    if config_path.is_file():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if config.get("artifact_version") != "0.1.0":
            errors.append("unexpected artifact version")

    primary = root / "data" / "aggregate" / "primary_comparison.csv"
    payload = root / "data" / "aggregate" / "payload_results.csv"
    if primary.is_file() and payload.is_file():
        errors.extend(validate_aggregate_tables(primary, payload))

    artifact = root / "artifacts" / "qualitative" / "visual_coco_original_stego.png"
    provenance = root / "artifacts" / "qualitative" / "provenance.json"
    if artifact.is_file() and provenance.is_file():
        errors.extend(validate_archive_artifact(artifact, provenance))
    return errors
