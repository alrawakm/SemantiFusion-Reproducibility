from __future__ import annotations

import argparse
from pathlib import Path

from .release import validate_release
from .tables import reproduce_tables


def validate_main() -> None:
    parser = argparse.ArgumentParser(description="Validate the SemantiFusion release")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_release(args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Release validation passed.")


def tables_main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild tables from aggregate CSV files")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path("output/tables"))
    args = parser.parse_args()
    reproduce_tables(args.repo_root, args.output_dir)
    print(f"Wrote tables to {args.output_dir}")

