import argparse
from pathlib import Path

from semantifusion_repro.tables import reproduce_tables, validate_aggregate_tables


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild manuscript tables from the retained CSV values")
    parser.add_argument("--output-dir", type=Path, default=Path("output/tables"))
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    primary = root / "data" / "aggregate" / "primary_comparison.csv"
    payload = root / "data" / "aggregate" / "payload_results.csv"
    errors = validate_aggregate_tables(primary, payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    output = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    reproduce_tables(root, output)
    print(f"Wrote table files to {output}")


if __name__ == "__main__":
    main()

