#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
from statistics import median
import csv
import hashlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "artifacts/csv/017_full_same_size_metric_sweep.csv"
JSON_PATH = ROOT / "artifacts/json/017_full_same_size_metric_sweep.json"
MD_PATH = ROOT / "artifacts/md/017_full_same_size_metric_sweep.md"
SCRIPT_PATH = ROOT / "scripts/017_full_same_size_metric_sweep.py"

OUT_JSON = ROOT / "artifacts/json/018_full_census_theorem_verification.json"
OUT_MD = ROOT / "artifacts/md/018_full_census_theorem_verification.md"

EXPECTED_TOTAL = 142506
EXPECTED_CLASS_COUNTS = {
    0: 243,
    2: 12015,
    4: 58995,
    6: 58995,
    8: 12015,
    10: 243,
}
EXPECTED_MEDIAN_COMPRESSED = {
    0: 30,
    2: 174,
    4: 270,
    6: 342,
    8: 390,
    10: 390,
}
EXPECTED_MEDIAN_MEAN_DELTA = {
    0: -0.057777777777777775,
    2: -0.23333333333333334,
    4: -0.3511111111111111,
    6: -0.44,
    8: -0.5,
    10: -0.5,
}

def fail(msg):
    print("ERROR:", msg)
    sys.exit(1)

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def pick_field(fieldnames, candidates):
    norm = {name.strip().lower(): name for name in fieldnames}
    for cand in candidates:
        key = cand.strip().lower()
        if key in norm:
            return norm[key]
    return None

def close(a, b, tol=1e-12):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)

def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def find_checks(obj):
    if isinstance(obj, dict):
        if "checks" in obj and isinstance(obj["checks"], dict):
            return obj["checks"]
        for v in obj.values():
            found = find_checks(v)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = find_checks(v)
            if found is not None:
                return found
    return None

for path in [CSV_PATH, JSON_PATH, MD_PATH, SCRIPT_PATH]:
    if not path.exists():
        fail("missing required file: " + str(path.relative_to(ROOT)))

rows = []
with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    if not reader.fieldnames:
        fail("CSV has no header")

    odd_field = pick_field(reader.fieldnames, ["odd_triangle_count", "odd_count"])
    mean_field = pick_field(reader.fieldnames, ["mean_actual_delta", "mean_delta"])
    comp_field = pick_field(reader.fieldnames, ["compressed_count"])
    exp_field = pick_field(reader.fieldnames, ["expanded_count"])

    missing = []
    if odd_field is None:
        missing.append("odd_triangle_count")
    if mean_field is None:
        missing.append("mean_actual_delta")
    if comp_field is None:
        missing.append("compressed_count")
    if exp_field is None:
        missing.append("expanded_count")
    if missing:
        fail("CSV missing expected fields: " + ", ".join(missing))

    for row in reader:
        odd = int(row[odd_field])
        mean_delta = float(row[mean_field])
        compressed = int(row[comp_field])
        expanded = int(row[exp_field])
        rows.append({
            "odd_triangle_count": odd,
            "mean_actual_delta": mean_delta,
            "compressed_count": compressed,
            "expanded_count": expanded,
        })

classes = defaultdict(list)
for row in rows:
    classes[row["odd_triangle_count"]].append(row)

class_stats = {}
for odd in sorted(classes):
    group = classes[odd]
    class_stats[str(odd)] = {
        "count": len(group),
        "median_mean_actual_delta": median([r["mean_actual_delta"] for r in group]),
        "median_compressed_count": median([r["compressed_count"] for r in group]),
        "max_expanded_count": max([r["expanded_count"] for r in group]),
        "min_expanded_count": min([r["expanded_count"] for r in group]),
    }

checks = {}

checks["csv_total_matches_expected"] = len(rows) == EXPECTED_TOTAL

observed_counts = {odd: len(classes.get(odd, [])) for odd in EXPECTED_CLASS_COUNTS}
checks["class_counts_match_expected"] = observed_counts == EXPECTED_CLASS_COUNTS

checks["no_unexpected_odd_triangle_classes"] = (
    sorted(classes.keys()) == sorted(EXPECTED_CLASS_COUNTS.keys())
)

checks["no_expansion_in_any_same_size_variant"] = all(
    r["expanded_count"] == 0 for r in rows
)

median_compressed_ok = True
median_mean_ok = True
for odd in EXPECTED_CLASS_COUNTS:
    stat = class_stats.get(str(odd))
    if stat is None:
        median_compressed_ok = False
        median_mean_ok = False
        continue
    if stat["median_compressed_count"] != EXPECTED_MEDIAN_COMPRESSED[odd]:
        median_compressed_ok = False
    if not close(stat["median_mean_actual_delta"], EXPECTED_MEDIAN_MEAN_DELTA[odd]):
        median_mean_ok = False

checks["median_compressed_counts_match_theorem"] = median_compressed_ok
checks["median_mean_deltas_match_theorem"] = median_mean_ok

mc = {odd: class_stats[str(odd)]["median_compressed_count"] for odd in EXPECTED_CLASS_COUNTS}
mm = {odd: class_stats[str(odd)]["median_mean_actual_delta"] for odd in EXPECTED_CLASS_COUNTS}

checks["compressed_median_strictly_increases_until_saturation"] = (
    mc[0] < mc[2] < mc[4] < mc[6] < mc[8] and mc[8] == mc[10]
)

checks["mean_delta_median_strictly_decreases_until_saturation"] = (
    mm[0] > mm[2] > mm[4] > mm[6] > mm[8] and close(mm[8], mm[10])
)

checks["zero_odd_class_weaker_than_all_positive_odd_medians"] = all(
    mm[0] > mm[odd] for odd in [2, 4, 6, 8, 10]
)

source_json = read_json(JSON_PATH)
source_checks = find_checks(source_json)
if source_checks is None:
    checks["source_017_json_checks_found"] = False
    checks["source_017_json_checks_all_true"] = False
else:
    checks["source_017_json_checks_found"] = True
    checks["source_017_json_checks_all_true"] = all(v is True for v in source_checks.values())

hash_paths = [
    SCRIPT_PATH,
    CSV_PATH,
    JSON_PATH,
    MD_PATH,
]

payload_root = ROOT.parent / "18-g900-kernel-admission" / "source" / "kernel_payload"
for name in [
    "g15_slot_edges.csv",
    "g60_local_edges.csv",
    "carrier_signing_table.csv",
    "x_sigma_edges.csv",
]:
    p = payload_root / name
    if p.exists():
        hash_paths.append(p)

hashes = {}
for path in hash_paths:
    hashes[str(path.relative_to(ROOT.parent))] = sha256_file(path)

verdict_ok = all(checks.values())

report = {
    "artifact": "018_full_census_theorem_verification",
    "verdict_ok": verdict_ok,
    "input_artifacts": {
        "csv": str(CSV_PATH.relative_to(ROOT)),
        "json": str(JSON_PATH.relative_to(ROOT)),
        "md": str(MD_PATH.relative_to(ROOT)),
        "script": str(SCRIPT_PATH.relative_to(ROOT)),
    },
    "expected_total": EXPECTED_TOTAL,
    "observed_total": len(rows),
    "expected_class_counts": EXPECTED_CLASS_COUNTS,
    "observed_class_counts": observed_counts,
    "class_stats": class_stats,
    "checks": checks,
    "sha256": hashes,
}

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_MD.parent.mkdir(parents=True, exist_ok=True)

with OUT_JSON.open("w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, sort_keys=True)
    f.write("\n")

lines = []
lines.append("# Full Census Theorem Verification")
lines.append("")
lines.append("## Verdict")
lines.append("")
lines.append("- verdict_ok: " + str(verdict_ok))
lines.append("- observed_total: " + str(len(rows)))
lines.append("- expected_total: " + str(EXPECTED_TOTAL))
lines.append("")
lines.append("## Class table")
lines.append("")
lines.append("| odd_triangle_count | count | median_mean_actual_delta | median_compressed_count | max_expanded_count |")
lines.append("|---:|---:|---:|---:|---:|")
for odd in sorted(EXPECTED_CLASS_COUNTS):
    stat = class_stats[str(odd)]
    lines.append(
        "| {odd} | {count} | {mean} | {compressed} | {expanded} |".format(
            odd=odd,
            count=stat["count"],
            mean=stat["median_mean_actual_delta"],
            compressed=stat["median_compressed_count"],
            expanded=stat["max_expanded_count"],
        )
    )

lines.append("")
lines.append("## Checks")
lines.append("")
for key in sorted(checks):
    lines.append("- " + key + ": " + str(checks[key]))

lines.append("")
lines.append("## Source artifacts")
lines.append("")
for key, value in report["input_artifacts"].items():
    lines.append("- " + key + ": " + value)

lines.append("")
lines.append("## SHA-256")
lines.append("")
for key in sorted(hashes):
    lines.append("- " + key + ": " + hashes[key])

lines.append("")
with OUT_MD.open("w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("wrote", OUT_JSON.relative_to(ROOT))
print("wrote", OUT_MD.relative_to(ROOT))
print("verdict_ok=" + str(verdict_ok))
for key in sorted(checks):
    print(key + "=" + str(checks[key]))

if not verdict_ok:
    sys.exit(2)
