import argparse
import csv
from pathlib import Path

from semantifusion_repro.manifest import load_pair_manifest, sha256_file, validate_pair_records
from semantifusion_repro.metrics import bit_error_rate, load_rgb, psnr, read_bits, ssim


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute paired fidelity and optional recovery metrics")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = args.manifest.resolve()
    records = load_pair_manifest(manifest)
    errors = validate_pair_records(records, manifest.parent, check_files=True)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    rows: list[dict[str, str]] = []
    for record in records:
        original_path = manifest.parent / record.original_path
        stego_path = manifest.parent / record.stego_path
        original = load_rgb(original_path)
        stego = load_rgb(stego_path)
        ber = ""
        if record.message_bits_path and record.recovered_bits_path:
            message = read_bits(manifest.parent / record.message_bits_path)
            recovered = read_bits(manifest.parent / record.recovered_bits_path)
            ber = f"{bit_error_rate(message, recovered):.10f}"

        rows.append(
            {
                "sample_id": record.sample_id,
                "reference_id": record.reference_id,
                "payload_bits": record.payload_bits,
                "psnr_db": f"{psnr(original, stego):.8f}",
                "ssim": f"{ssim(original, stego):.8f}",
                "ber": ber,
                "original_sha256": sha256_file(original_path),
                "stego_sha256": sha256_file(stego_path),
            }
        )

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "sample_id",
        "reference_id",
        "payload_bits",
        "psnr_db",
        "ssim",
        "ber",
        "original_sha256",
        "stego_sha256",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote metrics for {len(rows)} pairs to {output}")


if __name__ == "__main__":
    main()

