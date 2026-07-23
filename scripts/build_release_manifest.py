import argparse
import hashlib
from pathlib import Path


EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "output"}
EXCLUDED_NAMES = {"RELEASE_MANIFEST.sha256"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Write SHA-256 digests for release files")
    parser.add_argument("--output", type=Path, default=Path("RELEASE_MANIFEST.sha256"))
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = args.output if args.output.is_absolute() else root / args.output
    files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in EXCLUDED_NAMES
        and not any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts)
    ]
    lines = [f"{sha256(path)}  {path.relative_to(root).as_posix()}" for path in sorted(files)]
    output.write_text("\n".join(lines) + "\n", encoding="ascii")
    print(f"Wrote {len(lines)} digests to {output}")


if __name__ == "__main__":
    main()

