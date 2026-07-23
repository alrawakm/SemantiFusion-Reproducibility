# SemantiFusion Overleaf project

This directory is the clean manuscript project. It keeps the Springer Nature `sn-jnl` template used in the supplied archive.

## Upload and compile

1. Upload the ZIP containing this directory to Overleaf.
2. Open **Menu** and set **Main document** to `main.tex` if Overleaf does not select it automatically.
3. Use the pdfLaTeX compiler. The template selects the Springer Nature numbered mathematics/physics bibliography style through `sn-mathphys-num`.
4. Recompile twice after BibTeX has run so citations, references, and cross-references settle.

## Project files

- `main.tex`: authoritative manuscript.
- `references.bib`: deduplicated bibliography containing only traceable publications.
- `sn-jnl.cls`: supplied Springer Nature class.
- `sn-mathphys-num.bst`: supplied numbered reference style.
- `CITATION_AUDIT.md`: citation verification record and list of removed unresolved keys.
- `figures/qualitative_coco_pairs.png`: archive-supplied COCO original/stego comparisons.

The method figure is drawn in LaTeX with TikZ. The qualitative COCO figure is retained because it records original/stego examples and image identifiers. Other bitmap figures from the archive were not copied because they describe a different perturbative pipeline or contain results that cannot be tied to the revised method.

## Checks completed

- Every citation key in `main.tex` exists exactly once in `references.bib`.
- Every bibliography entry is cited.
- All 15 DOI-bearing records resolved through Crossref with matching publication titles.
- URL-only records point to official proceedings, publisher, PMLR, OpenReview, CVF, or arXiv pages.
- Duplicate entries and unresolved 2025--2026 placeholders from the supplied bibliography were removed.
- Numerical statements in the abstract now agree with the payload table.
- The security claim is limited to the reported transfer-detector setting.
- The local build includes the qualitative COCO examples and states their provenance limits.

## Evidence still needed before submission

The supplied archive contains the manuscript's aggregate tables but not run-level detector scores, trained checkpoints, code, loss weights, exact model identifiers, or split manifests. These items are not reconstructed in this project. They should be archived before the paper is presented as independently reproducible. The most important missing experiment is target-aware steganalysis trained directly on SemantiFusion outputs.

The verified local build is 25 pages. No manuscript section was removed to meet a shorter page target.

The funding and data/code-availability declarations in `main.tex` should be checked by the author before submission and changed if the underlying facts differ.
