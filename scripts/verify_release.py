import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".py", ".json", ".csv", ".toml", ".cff", ".yaml", ".yml", ".gitignore"}
FORBIDDEN_SUFFIXES = {".pt", ".pth", ".ckpt", ".npz", ".npy", ".rar", ".7z", ".doc", ".docx", ".xlsx", ".pptx", ".tex", ".pdf", ".png", ".svg"}
FORBIDDEN_DIRS = {"__pycache__", ".git", ".pytest_cache", "cache", "logs", "sources", "model_0", "lightning_logs", "figures", "manuscript", "paper"}
FORBIDDEN_TEXT = [
    re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]"),
    re.compile(r"(?:^|[^A-Za-z0-9_.-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:$|[^A-Za-z0-9_.-])"),
    re.compile("C:" + r"[\\/]" + "Users", re.IGNORECASE),
    re.compile("0804" + "JCC|XAI" + "_Boundary|revision_next" + "_journal|" + r"\\bAD" + "MIN" + r"\\b", re.IGNORECASE),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


failures = []
files = [path for path in ROOT.rglob("*") if path.is_file()]
for path in files:
    relative = path.relative_to(ROOT)
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        failures.append(f"forbidden suffix: {relative}")
    if any(part in FORBIDDEN_DIRS for part in relative.parts):
        failures.append(f"forbidden directory: {relative}")
    if path.suffix.lower() in TEXT_SUFFIXES or path.name == ".gitignore":
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN_TEXT:
            if pattern.search(text):
                failures.append(f"privacy/path pattern {pattern.pattern!r}: {relative}")

established = ROOT / "results" / "established_explainers"
with (established / "cells.csv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
if len(rows) != 330 or len({row["cell_id"] for row in rows}) != 66 or len({(row["family"], row["task"]) for row in rows}) != 11:
    failures.append("established-explainer table does not have 330 rows/66 cells/11 tasks")
with (established / "family_stratified_summary.csv").open(encoding="utf-8", newline="") as handle:
    family_rows = list(csv.DictReader(handle))
if len(family_rows) != 10 or {row["family"] for row in family_rows} != {"bxaic", "google"}:
    failures.append("family-stratified table does not have two families x five methods")

polaris = ROOT / "results" / "polaris_hclint"
for group in ["ecfp_rf", "chemeleon_seed42", "chemeleon_seed123", "chemeleon_seed2026", "chemeleon_ensemble"]:
    with (polaris / group / "predictions_no_structures.csv").open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        prediction_rows = list(reader)
    if reader.fieldnames != ["test_index", "prediction"] or len(prediction_rows) != 575:
        failures.append(f"invalid structure-free prediction table: {group}")
    if [int(row["test_index"]) for row in prediction_rows] != list(range(575)):
        failures.append(f"test index order changed: {group}")

metadata = json.loads((ROOT / "data" / "polaris_hclint_metadata.json").read_text(encoding="utf-8"))
if metadata["n_train"] != 2229 or metadata["n_test"] != 575 or metadata["test_targets_accessed"] is not False:
    failures.append("Polaris metadata boundary failed")
ensemble = json.loads((polaris / "chemeleon_ensemble" / "polaris_metrics.json").read_text(encoding="utf-8"))
scores = ensemble["results"]["results"][0]["scores"]
if abs(scores["mean_absolute_error"] - 0.3252032841802898) > 1e-12 or abs(scores["pearsonr"] - 0.7325225421906688) > 1e-12:
    failures.append("fixed Polaris ensemble metrics changed")
attribution = json.loads((polaris / "attribution_compatibility" / "summary.json").read_text(encoding="utf-8"))
if attribution["n_molecules"] != 100 or attribution["test_targets_accessed"] is not False or "no atom rationale" not in attribution["interpretation"]:
    failures.append("Polaris attribution boundary failed")

manifest = ROOT / "MANIFEST_SHA256.txt"
if not manifest.exists():
    failures.append("missing MANIFEST_SHA256.txt")
else:
    manifest_paths = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        manifest_paths.add(relative)
        target = ROOT / Path(relative)
        if not target.exists() or sha256(target) != expected:
            failures.append(f"manifest mismatch: {relative}")
    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in files
        if path.name != "MANIFEST_SHA256.txt"
    }
    if manifest_paths != actual_paths:
        failures.append("manifest file list is incomplete or contains stale entries")

if failures:
    raise SystemExit("FAIL\n" + "\n".join(failures))
print(f"PASS: {len(files)} files; privacy, policy, evidence, and manifest checks passed")
