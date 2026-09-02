import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "derived_checks"
OUT.mkdir(exist_ok=True)

cells = pd.read_csv(ROOT / "results" / "established_explainers" / "cells.csv")
metrics = ["risk", "atom_fraction", "precision", "iou"]
if len(cells) != 330 or cells["cell_id"].nunique() != 66:
    raise SystemExit("Unexpected established-explainer cell table")
task_means = cells.groupby(["family", "task", "method"], as_index=False)[metrics].mean()
family = task_means.groupby(["family", "method"], as_index=False)[metrics].mean()
family.insert(1, "family_label", family["family"].map({"bxaic": "B-XAIC", "google": "Graph Attribution"}))
family.insert(2, "tasks", family["family"].map(task_means.groupby("family")["task"].nunique()))
family.insert(3, "cells", family["family"].map(cells.groupby("family")["cell_id"].nunique()))
expected = pd.read_csv(ROOT / "results" / "established_explainers" / "family_stratified_summary.csv")
columns = ["family", "family_label", "tasks", "cells", "method", *metrics]
family = family[columns].sort_values(["family", "method"]).reset_index(drop=True)
expected = expected[columns].sort_values(["family", "method"]).reset_index(drop=True)
if not family[["family", "family_label", "method"]].equals(expected[["family", "family_label", "method"]]):
    raise SystemExit("Family/method labels do not match")
if not np.allclose(family[["tasks", "cells", *metrics]], expected[["tasks", "cells", *metrics]], rtol=0, atol=1e-12):
    raise SystemExit("Family-stratified values do not reproduce")
family.to_csv(OUT / "family_stratified_recomputed.csv", index=False)

polaris = ROOT / "results" / "polaris_hclint"
seed_scores = {}
for seed in [42, 123, 2026]:
    payload = json.loads((polaris / f"chemeleon_seed{seed}" / "polaris_metrics.json").read_text(encoding="utf-8"))
    seed_scores[seed] = payload["results"][0]["scores"]
ensemble = json.loads((polaris / "chemeleon_ensemble" / "polaris_metrics.json").read_text(encoding="utf-8"))
for metric in seed_scores[42]:
    values = np.array([seed_scores[seed][metric] for seed in [42, 123, 2026]], dtype=float)
    if not np.isclose(values.mean(), ensemble["seed_mean"][metric], rtol=0, atol=1e-12):
        raise SystemExit(f"Seed mean does not reproduce: {metric}")
    if not np.isclose(values.std(ddof=1), ensemble["seed_sample_sd"][metric], rtol=0, atol=1e-12):
        raise SystemExit(f"Seed SD does not reproduce: {metric}")
pd.DataFrame(
    [{"seed": seed, **seed_scores[seed]} for seed in [42, 123, 2026]]
).to_csv(OUT / "polaris_seed_scores_recomputed.csv", index=False)
print("PASS: family-stratified and Polaris seed summaries reproduce")
