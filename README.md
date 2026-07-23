# SemantiFusion reproducibility artifact

This repository accompanies the manuscript:

> SemantiFusion: Message-Conditioned Semantic--Diffusion Steganography for Natural Images

It preserves the evidence that was present in the supplied research archive and provides executable analysis and validation code. It does not claim to reconstruct files that were absent from that archive.

This is a code-only repository. The manuscript, journal template, and compiled PDF are maintained separately and are not included here.

## Reproducibility boundary

The release has three evidence levels.

1. **Exactly reproducible from this repository:** aggregate tables, payload calculations, file digests, manifest validation, and the release checks.
2. **Inspectable but not regenerable:** the retained COCO original/stego composite. The repository records its SHA-256 digest, dimensions, source archive, and displayed COCO identifiers.
3. **Not currently reproducible:** model training and stego-image generation. The original training program, model configuration, checkpoint identifiers, trained generator/decoder weights, seeds, raw paired images, and run-level detector scores were not present in the supplied archive.

The distinction matters. The qualitative figure shows three recorded outputs, but it is not a replacement for raw pairs, independent regeneration, or target-aware steganalysis.

## Quick start

Python 3.10 or later is required.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
python scripts/validate_release.py
python scripts/reproduce_reported_tables.py --output-dir output/tables
python -m unittest discover -s tests -v
```

On Linux or macOS, activate the environment with `source .venv/bin/activate`.

## Working with raw image pairs

Raw reference/stego pairs are not included because they were not retained. When they become available, create a paired manifest and compute the metrics as follows:

```bash
python scripts/build_pair_manifest.py \
  --original-dir /path/to/original \
  --stego-dir /path/to/stego \
  --output data/pairs.csv

python scripts/compute_pair_metrics.py \
  --manifest data/pairs.csv \
  --output output/pair_metrics.csv

python scripts/build_qualitative_figure.py \
  --manifest data/pairs.csv \
  --output output/qualitative_pairs.png \
  --limit 3
```

The manifest keeps reference-level identifiers together so that all outputs derived from one reference can be assigned to the same train, validation, or test partition.

## Repository contents

- `artifacts/qualitative/`: the retained composite figure and its provenance record.
- `data/aggregate/`: machine-readable values used by the manuscript tables.
- `data/schema/`: field definitions for raw-pair and experiment manifests.
- `src/semantifusion_repro/`: metric, manifest, table, and figure utilities.
- `scripts/`: command-line entry points.
- `tests/`: deterministic unit tests.
- `docs/`: the target-aware evaluation protocol and release limitations.

## Metric implementation

The package computes RGB PSNR, windowed SSIM, and bit error rate. The SSIM implementation uses an 11-pixel Gaussian window with sigma 1.5 and the usual constants for 8-bit images. The original archive did not retain its metric-library version. Results recomputed by this package must therefore record the package version and should not be presented as bit-for-bit reconstructions of the archived aggregate table unless the original metric implementation is recovered.

## Dataset access

Dataset images are not redistributed. Obtain MS-COCO, DIV2K, and BOSSBase from their maintainers and record release identifiers and checksums in the experiment manifest. The displayed qualitative artifact names COCO val2017 images `000000000139.jpg`, `000000000632.jpg`, and `000000000724.jpg`.

## Citation and reuse

Citation metadata are provided in `CITATION.cff`. No software license has been selected by the author; see `LICENSE_STATUS.md` before reusing the code.
