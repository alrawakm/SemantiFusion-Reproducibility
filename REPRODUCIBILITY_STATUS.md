# Reproducibility status

## Present in the release

- Revised manuscript source and bibliography.
- Machine-readable primary and payload-sweep tables.
- The archive-supplied qualitative COCO composite.
- SHA-256 provenance for the qualitative artifact.
- Paired-image PSNR, SSIM, and BER code.
- Pair-manifest generation and validation.
- Reference-level split and target-aware steganalysis protocol.
- Unit tests and a GitHub Actions check.

## Missing from the supplied archive

- Original training source code.
- Exact diffusion, VAE, vision-language, message-encoder, and decoder checkpoint identifiers.
- Trained model weights.
- Loss weights and complete optimization configuration.
- Random seeds and generation scheduler settings.
- Raw original/stego image pairs.
- Payload and recovered-bit files for each image.
- Image-level train, validation, and test manifests.
- Run-level steganalysis predictions and detector checkpoints.

## Consequence

The aggregate tables and artifact checks can be reproduced. The reported model cannot yet be retrained, and the displayed stego outputs cannot be regenerated from weights. This repository must not be described as a full computational reproduction until the missing source, configurations, weights, and run-level records are deposited and checked.

