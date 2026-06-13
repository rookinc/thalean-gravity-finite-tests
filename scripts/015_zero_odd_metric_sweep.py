from pathlib import Path
from collections import Counter, deque
import ast
import csv
import json
import statistics
import time

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = P18 / "source/kernel_payload"

IN_ZERO = ROOT / "artifacts/csv/014_zero_odd_toggle_sets.csv"

OUT_JSON = ROOT / "artifacts/json/015_zero_odd_metric_sweep.json"
OUT_MD = ROOT / "artifacts/md/015_zero_odd_metric_sweep.md"
OUT_CSV = ROOT / "artifacts/csv/015_zero_odd_metric_sweep.csv"

N_SLOT = 15
N_LOCAL = 60
N = N_SLOT * N_LOCAL
PROGRESS_EVERY = 10

def gid(slot, local):
    return int(slot) * N_LOCAL + int(local)

def edge(a, b):
    a = int(a)
    b = int(b)
    if a == b:
        raise ValueError("loop edge")
    return (a, b) if a < b else (b, a)

def read_dict_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def read_g15_edges():
    return [edge(r["slot_u"], r["slot_v"]) for r in read_dict_csv(PAYLOAD / "g15_slot_edges.csv")]

def read_g60_edges():
    return [edge(r["local_u"], r["local_v"]) for r in read_dict_csv(PAYLOAD / "g60_local_edges.csv")]

def read_signs():
    out = {}
    for r in read_dict_csv(PAYLOAD / "carrier_signing_table.csv"):
        out[edge(r["slot_u"], r["slot_v"])] = int(r["sign"])
    return out

def parse_toggle_edges(s):
    try:
        raw = json.loads(s)
    except Exception:
        raw = ast.literal_eval(s)
    return tuple(edge(a, b) for a, b in raw)

def read_zero_toggles():
    rows = read_dict_csv(IN_ZERO)
    out = []
    for idx, r in enumerate(rows):
        toggles = parse_toggle_edges(r["toggle_edges"])
        out.append({
            "index": idx,
            "is_neutralizer": str(r.get("is_neutralizer", "")).lower() == "true",
            "toggles": toggles,
        })
    return out

def apply_toggles(signs, toggles):
    out = dict(signs)
    for e in toggles:
        out[e] = 1 - out[e]
    return out

def build_edges(g15_edges, g60_edges, signs):
    out = set()

    for slot in range(N_SLOT):
        for a, b in g60_edges:
            out.add(edge(gid(slot, a), gid(slot, b)))

    for su, sv in g15_edges:
        s = signs[edge(su, sv)]
        for x in range(N_LOCAL):
            y = (x + 30) % N_LOCAL if s else x
            out.add(edge(gid(su, x), gid(sv, y)))

    return out

def adjacency(edges):
    adj = [[] for _ in range(N)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for xs in adj:
        xs.sort()
    return adj

def shortest_distance(adj, src, dst):
    if src == dst:
        return 0
    dist = [-1] * N
    dist[src] = 0
    q = deque([src])
    while q:
        v = q.popleft()
        nd = dist[v] + 1
        for w in adj[v]:
            if dist[w] < 0:
                if w == dst:
                    return nd
                dist[w] = nd
                q.append(w)
    return None

def baseline_half_distances(baseline_adj):
    d = {}
    for slot in range(N_SLOT):
        for x in range(N_LOCAL):
            src = gid(slot, x)
            dst = gid(slot, (x + 30) % N_LOCAL)
            d[(slot, x)] = shortest_distance(baseline_adj, src, dst)
    return d

def analyze_variant(name, g15_edges, g60_edges, signs, baseline_return_d, toggles=(), is_neutralizer=False):
    adj = adjacency(build_edges(g15_edges, g60_edges, signs))

    deltas = []
    signed_dist_counts = Counter()
    baseline_dist_counts = Counter()

    for slot in range(N_SLOT):
        for x in range(N_LOCAL):
            src = gid(slot, x)
            dst = gid(slot, (x + 30) % N_LOCAL)
            sd = shortest_distance(adj, src, dst)
            bd = baseline_return_d[(slot, x)]
            delta = sd - bd
            deltas.append(delta)
            signed_dist_counts[sd] += 1
            baseline_dist_counts[bd] += 1

    return {
        "name": name,
        "is_neutralizer": bool(is_neutralizer),
        "toggle_edges": [list(e) for e in toggles],
        "mean_actual_delta": sum(deltas) / len(deltas),
        "compressed_count": sum(1 for d in deltas if d < 0),
        "unchanged_count": sum(1 for d in deltas if d == 0),
        "expanded_count": sum(1 for d in deltas if d > 0),
        "delta_counts": dict(sorted(Counter(deltas).items())),
        "signed_distance_counts": dict(sorted(signed_dist_counts.items())),
        "baseline_distance_counts": dict(sorted(baseline_dist_counts.items())),
    }

def summarize_numeric(xs):
    return {
        "min": min(xs),
        "median": statistics.median(xs),
        "max": max(xs),
        "mean": sum(xs) / len(xs),
    }

def main():
    t0 = time.time()

    print("loading repaired Project 18 payload")
    g15_edges = read_g15_edges()
    g60_edges = read_g60_edges()
    original_signs = read_signs()
    zero_toggles = read_zero_toggles()

    print("zero_odd_toggle_sets=" + str(len(zero_toggles)))

    baseline_signs = {e: 0 for e in g15_edges}
    baseline_adj = adjacency(build_edges(g15_edges, g60_edges, baseline_signs))

    print("computing baseline half-flip return distances")
    baseline_return_d = baseline_half_distances(baseline_adj)

    print("analyzing original")
    original = analyze_variant(
        "original",
        g15_edges,
        g60_edges,
        original_signs,
        baseline_return_d,
    )

    records = []
    neutralizer_record = None

    print("sweeping zero-odd toggle sets")
    for i, item in enumerate(zero_toggles, start=1):
        if i == 1 or i % PROGRESS_EVERY == 0 or i == len(zero_toggles):
            print("progress " + str(i) + "/" + str(len(zero_toggles)))

        signs = apply_toggles(original_signs, item["toggles"])
        rec = analyze_variant(
            "zero_odd_" + str(item["index"]).zfill(3),
            g15_edges,
            g60_edges,
            signs,
            baseline_return_d,
            toggles=item["toggles"],
            is_neutralizer=item["is_neutralizer"],
        )
        records.append(rec)
        if item["is_neutralizer"]:
            neutralizer_record = rec

    rows = []
    for r in records:
        rows.append({
            "name": r["name"],
            "is_neutralizer": r["is_neutralizer"],
            "toggle_edges": json.dumps(r["toggle_edges"]),
            "mean_actual_delta": r["mean_actual_delta"],
            "compressed_count": r["compressed_count"],
            "unchanged_count": r["unchanged_count"],
            "expanded_count": r["expanded_count"],
            "delta_counts": json.dumps(r["delta_counts"], sort_keys=True),
            "signed_distance_counts": json.dumps(r["signed_distance_counts"], sort_keys=True),
        })

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "name",
            "is_neutralizer",
            "toggle_edges",
            "mean_actual_delta",
            "compressed_count",
            "unchanged_count",
            "expanded_count",
            "delta_counts",
            "signed_distance_counts",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    means = [r["mean_actual_delta"] for r in records]
    compressed = [r["compressed_count"] for r in records]
    expanded = [r["expanded_count"] for r in records]
    delta_pattern_counts = Counter(json.dumps(r["delta_counts"], sort_keys=True) for r in records)

    best = min(records, key=lambda r: r["mean_actual_delta"])
    weakest = max(records, key=lambda r: r["mean_actual_delta"])

    same_as_neutralizer = []
    if neutralizer_record is not None:
        target_pattern = json.dumps(neutralizer_record["delta_counts"], sort_keys=True)
        same_as_neutralizer = [
            r["name"] for r in records
            if json.dumps(r["delta_counts"], sort_keys=True) == target_pattern
        ]

    summary = {
        "zero_odd_count": len(records),
        "runtime_seconds": time.time() - t0,
        "mean_actual_delta": summarize_numeric(means),
        "compressed_count": summarize_numeric(compressed),
        "expanded_count": summarize_numeric(expanded),
        "distinct_delta_patterns": len(delta_pattern_counts),
        "delta_pattern_counts": dict(delta_pattern_counts),
        "best_most_compressive_zero_odd": {
            "name": best["name"],
            "mean_actual_delta": best["mean_actual_delta"],
            "compressed_count": best["compressed_count"],
            "delta_counts": best["delta_counts"],
            "toggle_edges": best["toggle_edges"],
        },
        "weakest_least_compressive_zero_odd": {
            "name": weakest["name"],
            "mean_actual_delta": weakest["mean_actual_delta"],
            "compressed_count": weakest["compressed_count"],
            "delta_counts": weakest["delta_counts"],
            "toggle_edges": weakest["toggle_edges"],
        },
        "neutralizer": neutralizer_record,
        "same_delta_pattern_as_neutralizer_count": len(same_as_neutralizer),
        "same_delta_pattern_as_neutralizer_names": same_as_neutralizer[:50],
    }

    checks = {
        "all_zero_odd_have_no_expansion": all(r["expanded_count"] == 0 for r in records),
        "neutralizer_found": neutralizer_record is not None,
        "neutralizer_is_weakest_or_tied": (
            neutralizer_record is not None
            and neutralizer_record["mean_actual_delta"] == weakest["mean_actual_delta"]
        ),
        "zero_odd_class_is_weak_vs_original_median": (
            statistics.median(means) > original["mean_actual_delta"]
        ),
        "all_zero_odd_weaker_than_original": all(
            r["mean_actual_delta"] > original["mean_actual_delta"]
            for r in records
        ),
    }

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "claim": "metric sweep over all zero-odd same-size toggle sets",
        "source_payload": str(PAYLOAD),
        "original": original,
        "summary": summary,
        "checks": checks,
        "records": records,
        "boundary": {
            "physical_gravity_claim": False,
            "finite_metric_control_claim": True,
            "metric_compression_claim": True,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Zero-Odd Metric Sweep")
    lines.append("")
    lines.append("This audit runs half-flip return metric tests on every same-size toggle set that erases all odd carrier triangles.")
    lines.append("")
    lines.append("No physical gravity claim is made. This is a finite graph-theoretic metric control.")
    lines.append("")
    lines.append("## Original")
    lines.append("")
    lines.append(f"- mean_actual_delta: {original['mean_actual_delta']}")
    lines.append(f"- compressed_count: {original['compressed_count']}")
    lines.append(f"- expanded_count: {original['expanded_count']}")
    lines.append(f"- delta_counts: {original['delta_counts']}")
    lines.append("")
    lines.append("## Zero-odd class summary")
    lines.append("")
    lines.append(f"- zero_odd_count: {summary['zero_odd_count']}")
    lines.append(f"- runtime_seconds: {summary['runtime_seconds']}")
    lines.append(f"- distinct_delta_patterns: {summary['distinct_delta_patterns']}")
    lines.append(f"- mean_actual_delta: {summary['mean_actual_delta']}")
    lines.append(f"- compressed_count: {summary['compressed_count']}")
    lines.append(f"- expanded_count: {summary['expanded_count']}")
    lines.append("")
    lines.append("## Neutralizer")
    lines.append("")
    if neutralizer_record is None:
        lines.append("- neutralizer: not found")
    else:
        lines.append(f"- name: {neutralizer_record['name']}")
        lines.append(f"- mean_actual_delta: {neutralizer_record['mean_actual_delta']}")
        lines.append(f"- compressed_count: {neutralizer_record['compressed_count']}")
        lines.append(f"- expanded_count: {neutralizer_record['expanded_count']}")
        lines.append(f"- delta_counts: {neutralizer_record['delta_counts']}")
        lines.append(f"- same_delta_pattern_as_neutralizer_count: {summary['same_delta_pattern_as_neutralizer_count']}")
    lines.append("")
    lines.append("## Most compressive zero-odd member")
    lines.append("")
    b = summary["best_most_compressive_zero_odd"]
    lines.append(f"- name: {b['name']}")
    lines.append(f"- mean_actual_delta: {b['mean_actual_delta']}")
    lines.append(f"- compressed_count: {b['compressed_count']}")
    lines.append(f"- delta_counts: {b['delta_counts']}")
    lines.append(f"- toggle_edges: {b['toggle_edges']}")
    lines.append("")
    lines.append("## Least compressive zero-odd member")
    lines.append("")
    w = summary["weakest_least_compressive_zero_odd"]
    lines.append(f"- name: {w['name']}")
    lines.append(f"- mean_actual_delta: {w['mean_actual_delta']}")
    lines.append(f"- compressed_count: {w['compressed_count']}")
    lines.append(f"- delta_counts: {w['delta_counts']}")
    lines.append(f"- toggle_edges: {w['toggle_edges']}")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in checks.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This audit asks whether erasing all odd carrier triangles generally weakens half-flip return compression.")
    lines.append("")
    lines.append("If the zero-odd class is uniformly weaker than the original, the causal mechanism becomes stronger: odd triangle holonomy is not merely correlated with the strong profile; removing it moves the system into a weak-compression metric class.")
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- artifacts/json/015_zero_odd_metric_sweep.json")
    lines.append("- artifacts/md/015_zero_odd_metric_sweep.md")
    lines.append("- artifacts/csv/015_zero_odd_metric_sweep.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_CSV)
    print("checks=" + json.dumps(checks, sort_keys=True))
    print("summary=" + json.dumps({
        "zero_odd_count": summary["zero_odd_count"],
        "runtime_seconds": summary["runtime_seconds"],
        "mean_actual_delta": summary["mean_actual_delta"],
        "compressed_count": summary["compressed_count"],
        "distinct_delta_patterns": summary["distinct_delta_patterns"],
    }, sort_keys=True))

if __name__ == "__main__":
    main()
