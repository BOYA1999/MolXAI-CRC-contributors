# Reproducibility surfaces

## A. Self-contained checks

The following checks use only files in this release:

```bash
python -m unittest discover -s src -p "test_*.py"
python scripts/recompute_release_tables.py
python scripts/verify_release.py
```

They validate the core finite-sample correction, recompute the family-stratified established-explainer table, recompute three-seed mean/SD summaries, check fixed Polaris metrics, enforce the release allowlist policy, and verify file hashes.

## B. Public-data reruns

Dataset adapters and reference scripts are provided, but raw molecule tables are intentionally retrieved from upstream sources. Follow `DATA_SOURCES.md`, freeze the exact revisions, and verify the stated hashes before running the benchmark adapters.

## C. Weight-dependent reruns

The 66-cell established-explainer run and three CheMeleon fine-tuning runs require checkpoints that are not distributed in this anonymous package. The release retains aggregate cell-level outputs, fixed configuration files, split indices, checkpoint/prediction hashes, and the scripts necessary to inspect the analysis contract. A byte-for-byte full rerun remains externally gated by obtaining/rebuilding the checkpoints.

For CheMeleon, place the foundation checkpoint obtained from the cited Zenodo record where Chemprop can locate it, materialize `data/train.csv`, and use the fixed configs in `configs/`. The fixed seed rule is 42, 123, and 2026; the ensemble is the unweighted arithmetic mean chosen before hidden-test evaluation.

## D. Evidence boundaries

- Established-explainer comparison: 66 matched cells, 11 task clusters, two benchmark families, two architectures, and three seeds. Family summaries are descriptive strata.
- Polaris predictivity: official 2,229/575 split; metrics are official hidden-test evaluation outputs.
- Polaris explanations: label-free perturbation relevance on 100 deterministically selected hidden-test molecules. This is not external validation of rationale correctness and does not support a rationale risk-control claim.
- Public release and archival deposit are separate. This package has no DOI until an actual immutable archive is created.
