# Target-aware steganalysis protocol

## Purpose

The transfer AUC in the manuscript measures a detector trained outside the SemantiFusion output distribution. It does not test a detector trained on SemantiFusion images. This protocol covers the missing test.

## Frozen generator

Freeze the generator, decoder, preprocessing code, sampler, and checkpoint hashes before creating detector data. Record every model identifier and file digest. Do not tune the generator after viewing detector test results.

## Reference-level split

Assign references to train, validation, and test partitions before generation. Every output derived from one reference stays in the same partition. This includes different payloads, messages, and generation seeds.

A suitable first allocation is 70% train, 10% validation, and 20% test. Publish the split manifest and the script that created it.

## Negative classes

Report two detector tasks.

1. Reference images versus message-conditioned outputs.
2. Benign diffusion reconstructions versus message-conditioned outputs.

The first task measures operational detectability against the available carrier. The second separates message conditioning from artifacts caused by diffusion reconstruction.

## Sampling

Use the same number of positive and negative examples in each partition. Generate at least one output for every reference. Add a repeated-reference condition with several messages and seeds per reference. Keep those repeated outputs in the reference's assigned partition.

Record:

- reference identifier;
- split;
- payload length;
- message and generation seeds;
- sampler and step count;
- model and checkpoint hashes;
- original, benign-reconstruction, and stego file hashes.

## Detectors

Train an image-domain detector such as SRNet on the frozen outputs. Add a detector that uses recovered diffusion-noise or inversion features when the generator permits inversion. Select hyperparameters with the validation partition only.

Report ROC AUC, balanced accuracy, sensitivity, specificity, calibration, and the false-positive rate at a fixed sensitivity. Preserve per-image scores.

## Statistical record

Repeat detector training with several seeds. Give the result for every seed and a bootstrap interval formed by resampling reference groups, not individual derived images. The held-out test partition must be evaluated once after model selection.

## Release

Deposit detector source code, environment files, trained checkpoints, manifests, per-image predictions, and a command that rebuilds every result table. A release check should fail when a required digest, prediction file, or split field is missing.

