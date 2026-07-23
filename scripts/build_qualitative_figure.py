import argparse
from pathlib import Path

from semantifusion_repro.manifest import load_pair_manifest, validate_pair_records
from semantifusion_repro.qualitative import build_pair_grid


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an original/stego comparison figure")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    manifest = args.manifest.resolve()
    records = load_pair_manifest(manifest)
    errors = validate_pair_records(records, manifest.parent, check_files=True)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    build_pair_grid(records, manifest.parent, args.output.resolve(), limit=args.limit)
    print(f"Wrote qualitative figure to {args.output.resolve()}")


if __name__ == "__main__":
    main()

