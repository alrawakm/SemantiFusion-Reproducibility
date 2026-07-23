from pathlib import Path

from semantifusion_repro.release import validate_release


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    errors = validate_release(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Release validation passed.")


if __name__ == "__main__":
    main()

