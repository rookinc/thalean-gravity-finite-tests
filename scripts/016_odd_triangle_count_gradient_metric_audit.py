from pathlib import Path
from collections import Counter, defaultdict, deque
from itertools import combinations
import csv
import json
import random
import statistics
import time

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = P18 / "source/kernel_payload"

OUT_JSON = ROOT / "artifacts/json/016_odd_triangle_count_gradient_metric_audit.json"
OUT_MD = ROOT / "artifacts/md/016_odd_triangle_count_gradient_metric_audit.md"
OUT_CSV = ROOT / "artifacts/csv/016_odd_triangle_count_gradient_metric_audit.csv"

N_SLOT = 15
N_LOCAL = 60
N = N_SLOT * N_LOCAL

SEED = 90016
SAMPLE_PER_CLASS = 243
PROGRESS_EVERY = 25

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

def triangle_records(g15_edges, signs):
    edge_set = set(g15_edges)
    records = []
    for a in range(N_SLOT):
        for b in range(a + 1, N_SLOT):
            for c in range(b + 1, N_SLOT):
                es = [edge(a, b), edge(a, c), edge(b, c)]
                if all(e in edge_set for e in es):
                    ss = [signs[e] for e in es]
                    records.append({
                        "triangle": [a, b, c],
                        "edges": es,
                        "carrier_parity": sum(ss) % 2,
                    })
    return records

def classify_combo(combo_indices, tri_index_records):
    combo_set = set(combo_indices)
    odd_triangles = []
    odd_slots = set()

    for tri in tri_index_records:
        toggled = sum(1 for idx in tri["edge_indices"] if idx in combo_set) % 2
        new_parity = tri["original_parity"] ^ toggled
        if new_parity == 1:
            odd_triangles.append(tri["triangle"])
            odd_slots.update(tri["triangle"])

    return len(odd_triangles), len(odd_slots), odd_triangles, sorted(odd_slots)

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
    out = {}
    for slot in range(N_SLOT):
        for x in range(N_LOCAL):
            src = gid(slot, x)
            dst = gid(slot, (x + 30) % N_LOCAL)
            out[(slot, x)] = shortest_distance(baseline_adj, src, dst)
    return out

def analyze_metric(g15_edges, g60_edges, signs, baseline_return_d):
    adj = adjacency(build_edges(g15_edges, g60_edges, signs))
    deltas = []

    for slot in range(N_SLOT):
        for x in range(N_LOCAL):
            src = gid(slot, x)
            dst = gid(slot, (x + 30) % N_LOCAL)
            sd = shortest_distance(adj, src, dst)
            bd = baseline_return_d[(slot, x)]
            deltas.append(sd - bd)

    return {
        "mean_actual_delta": sum(deltas) / len(deltas),
        "compressed_count": sum(1 for d in deltas if d < 0),
        "unchanged_count": sum(1 for d in deltas if d == 0),
        "expanded_count": sum(1 for d in deltas if d > 0),
        "delta_counts": dict(sorted(Counter(deltas).items())),
    }

def summarize(xs):
    return {
        "count": len(xs),
        "min": min(xs),
        "median": statistics.median(xs),
        "max": max(xs),
        "mean": sum(xs) / len(xs),
    }

def main():
    t0 = time.time()
    random.seed(SEED)

    print("loading repaired Project 18 payload")
    g15_edges = sorted(read_g15_edges())
    g60_edges = read_g60_edges()
    original_signs = read_signs()

    edge_index = {e: i for i, e in enumerate(g15_edges)}
    triangles = triangle_records(g15_edges, original_signs)

    tri_index_records = []
    for tri in triangles:
        tri_index_records.append({
            "triangle": tri["triangle"],
            "edge_indices": [edge_index[e] for e in tri["edges"]],
            "original_parity": tri["carrier_parity"],
        })

    print("building balanced stratified sample")
    buckets = defaultdict(list)
    total = 0

    for combo_indices in combinations(range(len(g15_edges)), 5):
        total += 1
        odd_count, odd_slot_count, odd_tris, odd_slots = classify_combo(combo_indices, tri_index_records)
        if len(buckets[odd_count]) < SAMPLE_PER_CLASS:
            combo_edges = tuple(g15_edges[i] for i in combo_indices)
            buckets[odd_count].append({
                "toggle_edges": combo_edges,
                "odd_triangle_count": odd_count,
                "odd_slot_count": odd_slot_count,
                "odd_triangles": odd_tris,
                "odd_triangle_slots": odd_slots,
            })

    print("total_combos=" + str(total))
    print("bucket_sizes=" + str({k: len(v) for k, v in sorted(buckets.items())}))

    baseline_signs = {e: 0 for e in g15_edges}
    baseline_adj = adjacency(build_edges(g15_edges, g60_edges, baseline_signs))

    print("computing baseline half-flip distances")
    baseline_return_d = baseline_half_distances(baseline_adj)

    print("analyzing original")
    original_metric = analyze_metric(g15_edges, g60_edges, original_signs, baseline_return_d)
    original_odd_count = sum(1 for t in triangles if t["carrier_parity"] == 1)
    original_odd_slots = sorted({s for t in triangles if t["carrier_parity"] == 1 for s in t["triangle"]})

    records = []
    all_items = []
    for odd_count in sorted(buckets):
        all_items.extend(buckets[odd_count])

    print("sample_count=" + str(len(all_items)))
    for i, item in enumerate(all_items, start=1):
        if i == 1 or i % PROGRESS_EVERY == 0 or i == len(all_items):
            print("progress " + str(i) + "/" + str(len(all_items)))

        signs = apply_toggles(original_signs, item["toggle_edges"])
        metric = analyze_metric(g15_edges, g60_edges, signs, baseline_return_d)

        rec = {
            "name": "sample_" + str(i).zfill(4),
            "toggle_edges": [list(e) for e in item["toggle_edges"]],
            "odd_triangle_count": item["odd_triangle_count"],
            "odd_slot_count": item["odd_slot_count"],
            "odd_triangles": item["odd_triangles"],
            "odd_triangle_slots": item["odd_triangle_slots"],
            **metric,
        }
        records.append(rec)

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "name",
            "odd_triangle_count",
            "odd_slot_count",
            "toggle_edges",
            "mean_actual_delta",
            "compressed_count",
            "unchanged_count",
            "expanded_count",
            "delta_counts",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in records:
            w.writerow({
                "name": r["name"],
                "odd_triangle_count": r["odd_triangle_count"],
                "odd_slot_count": r["odd_slot_count"],
                "toggle_edges": json.dumps(r["toggle_edges"]),
                "mean_actual_delta": r["mean_actual_delta"],
                "compressed_count": r["compressed_count"],
                "unchanged_count": r["unchanged_count"],
                "expanded_count": r["expanded_count"],
                "delta_counts": json.dumps(r["delta_counts"], sort_keys=True),
            })

    by_odd_count = {}
    for odd_count in sorted(set(r["odd_triangle_count"] for r in records)):
        group = [r for r in records if r["odd_triangle_count"] == odd_count]
        by_odd_count[str(odd_count)] = {
            "count": len(group),
            "mean_actual_delta": summarize([r["mean_actual_delta"] for r in group]),
            "compressed_count": summarize([r["compressed_count"] for r in group]),
            "expanded_count": summarize([r["expanded_count"] for r in group]),
            "odd_slot_count": summarize([r["odd_slot_count"] for r in group]),
        }

    class_medians = [
        (int(k), v["mean_actual_delta"]["median"], v["compressed_count"]["median"])
        for k, v in by_odd_count.items()
    ]

    checks = {
        "zero_odd_class_weaker_than_all_positive_odd_medians": all(
            by_odd_count["0"]["mean_actual_delta"]["median"] > by_odd_count[str(k)]["mean_actual_delta"]["median"]
            for k in sorted(int(x) for x in by_odd_count.keys())
            if k > 0
        ),
        "compressed_median_increases_after_zero_odd": all(
            by_odd_count["0"]["compressed_count"]["median"] < by_odd_count[str(k)]["compressed_count"]["median"]
            for k in sorted(int(x) for x in by_odd_count.keys())
            if k > 0
        ),
        "original_is_stronger_than_zero_odd_median": (
            original_metric["mean_actual_delta"] < by_odd_count["0"]["mean_actual_delta"]["median"]
        ),
    }

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "claim": "balanced metric sample across odd carrier triangle count classes",
        "source_payload": str(PAYLOAD),
        "seed": SEED,
        "sample_per_class": SAMPLE_PER_CLASS,
        "runtime_seconds": time.time() - t0,
        "original": {
            "odd_triangle_count": original_odd_count,
            "odd_triangle_slots": original_odd_slots,
            **original_metric,
        },
        "by_odd_triangle_count": by_odd_count,
        "class_medians": class_medians,
        "checks": checks,
        "records": records,
        "boundary": {
            "physical_gravity_claim": False,
            "finite_metric_gradient_claim": True,
            "metric_compression_claim": True,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Odd Triangle Count Gradient Metric Audit")
    lines.append("")
    lines.append("This audit runs a balanced metric sample across same-size toggle classes grouped by odd carrier triangle count.")
    lines.append("")
    lines.append("No physical gravity claim is made. This is a finite graph-theoretic metric gradient test.")
    lines.append("")
    lines.append("## Settings")
    lines.append("")
    lines.append(f"- seed: {SEED}")
    lines.append(f"- sample_per_class: {SAMPLE_PER_CLASS}")
    lines.append(f"- runtime_seconds: {report['runtime_seconds']}")
    lines.append("")
    lines.append("## Original")
    lines.append("")
    lines.append(f"- odd_triangle_count: {original_odd_count}")
    lines.append(f"- odd_triangle_slots: {original_odd_slots}")
    lines.append(f"- mean_actual_delta: {original_metric['mean_actual_delta']}")
    lines.append(f"- compressed_count: {original_metric['compressed_count']}")
    lines.append(f"- delta_counts: {original_metric['delta_counts']}")
    lines.append("")
    lines.append("## Class summaries")
    lines.append("")
    for k, v in by_odd_count.items():
        lines.append(f"### odd_triangle_count {k}")
        lines.append("")
        lines.append(f"- count: {v['count']}")
        lines.append(f"- mean_actual_delta: {v['mean_actual_delta']}")
        lines.append(f"- compressed_count: {v['compressed_count']}")
        lines.append(f"- expanded_count: {v['expanded_count']}")
        lines.append(f"- odd_slot_count: {v['odd_slot_count']}")
        lines.append("")
    lines.append("## Class medians")
    lines.append("")
    for odd_count, mean_med, comp_med in class_medians:
        lines.append(f"- odd_count={odd_count}: median_mean_delta={mean_med}, median_compressed_count={comp_med}")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in checks.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This audit asks whether the weak zero-odd class is part of a broader metric gradient as odd carrier triangles return.")
    lines.append("")
    lines.append("The key comparison is not whether every additional odd triangle monotonically increases compression. The cautious question is whether the zero-odd class is separated from the positive-odd classes.")
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- artifacts/json/016_odd_triangle_count_gradient_metric_audit.json")
    lines.append("- artifacts/md/016_odd_triangle_count_gradient_metric_audit.md")
    lines.append("- artifacts/csv/016_odd_triangle_count_gradient_metric_audit.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_CSV)
    print("checks=" + json.dumps(checks, sort_keys=True))

if __name__ == "__main__":
    main()
