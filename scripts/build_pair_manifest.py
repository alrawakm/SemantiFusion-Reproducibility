import argparse
import os
from pathlib import Path

from semantifusion_repro.manifest import PairRecord, write_pair_manifest


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def image_map(directory: Path) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for path in sorted(directory.iterdir()):
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            if path.stem in mapping:
                raise ValueError(f"Duplicate image stem in {directory}: {path.stem}")
            mapping[path.stem] = path
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a manifest for original/stego image pairs")
    parser.add_argument("--original-dir", type=Path, required=True)
    parser.add_argument("--stego-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--payload-bits", type=int)
    parser.add_argument("--split", choices=("train", "validation", "test"), default="")
    args = parser.parse_args()

    originals = image_map(args.original_dir.resolve())
    stegos = image_map(args.stego_dir.resolve())
    shared = sorted(originals.keys() & stegos.keys())
    missing_originals = sorted(stegos.keys() - originals.keys())
    missing_stegos = sorted(originals.keys() - stegos.keys())
    if missing_originals or missing_stegos:
        raise SystemExit(
            f"Unpaired files: missing originals={missing_originals}, missing stegos={missing_stegos}"
        )
    if not shared:
        raise SystemExit("No matching image stems were found")

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    records = [
        PairRecord(
            sample_id=f"{stem}-stego",
            reference_id=stem,
            original_path=Path(os.path.relpath(originals[stem], output.parent)).as_posix(),
            stego_path=Path(os.path.relpath(stegos[stem], output.parent)).as_posix(),
            payload_bits=str(args.payload_bits or ""),
            split=args.split,
        )
        for stem in shared
    ]
    write_pair_manifest(output, records)
    print(f"Wrote {len(records)} paired records to {output}")


if __name__ == "__main__":
    main()

