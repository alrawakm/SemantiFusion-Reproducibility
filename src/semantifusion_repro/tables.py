from __future__ import annotations

import csv
from pathlib import Path


def read_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_aggregate_tables(primary_path: str | Path, payload_path: str | Path) -> list[str]:
    errors: list[str] = []
    primary = read_rows(primary_path)
    payload = read_rows(payload_path)

    if len(primary) != 3:
        errors.append(f"primary table has {len(primary)} rows; expected 3")
    if len(payload) != 4:
        errors.append(f"payload table has {len(payload)} rows; expected 4")

    methods = [row.get("method", "") for row in primary]
    if methods != ["HiDDeN", "SteganoGAN", "SemantiFusion"]:
        errors.append("primary method order or names do not match the manuscript")

    payload_by_bits = {row.get("payload_bits", ""): row for row in payload}
    if set(payload_by_bits) != {"64", "256", "512", "1024"}:
        errors.append("payload table does not contain the four reported payload sizes")

    for row in payload:
        try:
            bits = int(row["payload_bits"])
            width = int(row["image_width"])
            height = int(row["image_height"])
            stored_bpp = float(row["bpp"])
            expected_bpp = bits / (width * height)
            if abs(stored_bpp - expected_bpp) > 0.00005:
                errors.append(f"payload {bits}: stored bpp does not match bits/(width*height)")
        except (KeyError, ValueError, ZeroDivisionError):
            errors.append("payload table contains an invalid numeric value")

    semantifusion = next((row for row in primary if row.get("method") == "SemantiFusion"), None)
    payload_256 = payload_by_bits.get("256")
    if semantifusion and payload_256:
        pairs = (
            ("psnr_db", 1e-9),
            ("ssim", 1e-9),
            ("ber_percent", 1e-9),
            ("transfer_auc", 1e-9),
        )
        for field, tolerance in pairs:
            if abs(float(semantifusion[field]) - float(payload_256[field])) > tolerance:
                errors.append(f"256-bit value differs between tables for {field}")
    return errors


def render_primary_latex(rows: list[dict[str, str]]) -> str:
    body = "\n".join(
        f"{row['method']} & {row['psnr_db']} & {row['ssim']} & {row['ber_percent']} & {row['transfer_auc']} \\\\"
        for row in rows
    )
    return (
        "\\begin{tabular}{lcccc}\n"
        "\\toprule\n"
        "Method & PSNR (dB) & SSIM & BER (\\%) & AUC \\\\\n"
        "\\midrule\n"
        f"{body}\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
    )


def render_payload_latex(rows: list[dict[str, str]]) -> str:
    body = "\n".join(
        f"{row['payload_bits']} & {row['bpp']} & {row['psnr_db']} & {row['ssim']} & "
        f"{row['ber_percent']} & {row['transfer_auc']} \\\\"
        for row in rows
    )
    return (
        "\\begin{tabular}{rrrrrr}\n"
        "\\toprule\n"
        "Bits & bpp & PSNR (dB) & SSIM & BER (\\%) & AUC \\\\\n"
        "\\midrule\n"
        f"{body}\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
    )


def render_markdown(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(row[field] for field in fields) + " |" for row in rows]
    return "\n".join([header, divider, *body]) + "\n"


def reproduce_tables(repo_root: str | Path, output_dir: str | Path) -> None:
    root = Path(repo_root)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    primary = read_rows(root / "data" / "aggregate" / "primary_comparison.csv")
    payload = read_rows(root / "data" / "aggregate" / "payload_results.csv")

    (output / "primary_comparison.tex").write_text(render_primary_latex(primary), encoding="utf-8")
    (output / "payload_results.tex").write_text(render_payload_latex(payload), encoding="utf-8")
    (output / "primary_comparison.md").write_text(
        render_markdown(primary, ["method", "psnr_db", "ssim", "ber_percent", "transfer_auc"]),
        encoding="utf-8",
    )
    (output / "payload_results.md").write_text(
        render_markdown(
            payload,
            ["payload_bits", "bpp", "psnr_db", "ssim", "ber_percent", "transfer_auc"],
        ),
        encoding="utf-8",
    )

