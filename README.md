# MolXAI-CRC anonymous reproducibility package

This repository contains anonymous code, aggregate evidence, and release checks for a study of finite-sample risk control around atom-level molecular explanations. It was rebuilt from an explicit allowlist for peer review. Manuscript text, supplementary text, tables, captions, and publication figures are not included. It also contains no author identity, email address, affiliation, local machine path, model checkpoint, execution log, cache, or bundled third-party source tree.

## What this package supports

- The original B-XAIC and Graph Attribution audits, calibration analyses, negative controls, and hierarchy-aware resampling results.
- A matched comparison of Gradient x Input, Integrated Gradients, Saliency, atom occlusion, and GNNExplainer across 66 model-task-seed cells and 11 task clusters. Family-stratified results are included.
- A predictivity and compatibility audit on the official Polaris `polaris/adme-fang-hclint-1` split. The fixed three-seed CheMeleon ensemble obtained MAE 0.325203 and Pearson r 0.732523; the ECFP4 random-forest baseline obtained MAE 0.444031 and Pearson r 0.504066.
- A label-free attribution perturbation check on 100 hidden-test molecules. Because Polaris HCLint has no atom-level rationale labels, this is computational compatibility evidence only, not a missed-rationale risk-control validation.

The statistical claims are bounded to the benchmark families, task clusters, architectures, seeds, and split definitions represented here. Family-stratified summaries are descriptive and do not establish population-wide or cross-dataset generalization.

## Quick verification

```bash
python -m unittest discover -s src -p "test_*.py"
python scripts/recompute_release_tables.py
python scripts/verify_release.py
```

The first command checks the core risk-control implementation. The second recomputes family-stratified tables and seed summaries from the released aggregate evidence. The third checks row counts, fixed metrics, file policy, privacy patterns, and `MANIFEST_SHA256.txt`.

## Repository map

- `src/`: core method, benchmark adapters, aggregation, and audit code.
- `scripts/reference/`: full-run reference scripts for the established-explainer experiment; original public datasets and fine-tuned checkpoints are required.
- `scripts/polaris/`: Polaris data retrieval, baseline, ensemble, and attribution scripts.
- `contracts/`: data, experiment, and analysis contracts.
- `data/`: provenance metadata only; raw molecular structures are intentionally not redistributed.
- `results/original_audits/`: aggregate evidence from the original benchmark and control analyses.
- `results/established_explainers/`: the 330-row comparison table, family-stratified summary, and paired analyses.
- `results/polaris_hclint/`: model metrics, structure-free predictions, split indices, and label-free attribution summaries.
- `DATA_SOURCES.md`: exact sources, revisions, licenses, checksums, and retrieval boundaries.
- `REPRODUCIBILITY.md`: executable surfaces and known external gates.
- `THIRD_PARTY_NOTICES.md`: separation between this repository's MIT license and upstream assets.

## Deliberate exclusions

Manuscript text, supplementary information, publication tables, captions, figures, and figure-generation scripts are maintained only in the separate submission workspace. Raw B-XAIC, Graph Attribution, and Polaris molecule tables are obtained from their upstream sources. Fine-tuned checkpoints and the CheMeleon foundation checkpoint are not redistributed. Predictions are released without SMILES; row identity is retained by the frozen zero-based test index. Per-cell execution JSON files were excluded because they recorded local checkpoint paths; the complete 330-row method comparison and the timing/statistical summaries needed for paper-level verification are retained.


