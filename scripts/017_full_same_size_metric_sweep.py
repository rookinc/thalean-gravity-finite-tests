from pathlib import Path
from collections import Counter, defaultdict, deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations
import csv
import json
import math
import os
import statistics
import time

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = P18 / "source/kernel_payload"

OUT_JSON = ROOT / "artifacts/json/017_full_same_size_metric_sweep.json"
OUT_MD = ROOT / "artifacts/md/017_full_same_size_metric_sweep.md"
OUT_CSV = ROOT / "artifacts/csv/017_full_same_size_metric_sweep.csv"

N_SLOT = 15
N_LOCAL = 60
N = N_SLOT * N_LOCAL
TOGGLE_SIZE = 5

WORKERS = int(os.environ.get("SWEEP_WORKERS", str(max(1, (os.cpu_count() or 2) - 1))))
CHUNK_SIZE = int(os.environ.get("SWEEP_CHUNK_SIZE", "80"))
PROGRESS_EVERY = int(os.environ.get("SWEEP_PROGRESS_EVERY", "2000"))

G15_EDGES = None
G60_EDGES = None
ORIGINAL_SIGN_BITS = None
TRI_INDEX_RECORDS = None
BASELINE_RETURN_D = None
BASE_LOCAL_ADJ = None

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

def read_signs_by_edge():
    out = {}
    for r in read_dict_csv(PAYLOAD / "carrier_signing_table.csv"):
        out[edge(r["slot_u"], r["slot_v"])] = int(r["sign"])
    return out

def triangle_records(g15_edges, signs_by_edge):
    edge_set = set(g15_edges)
    records = []
    for a in range(N_SLOT):
        for b in range(a + 1, N_SLOT):
            for c in range(b + 1, N_SLOT):
                es = [edge(a, b), edge(a, c), edge(b, c)]
                if all(e in edge_set for e in es):
                    ss = [signs_by_edge[e] for e in es]
                    records.append({
                        "triangle": [a, b, c],
                        "edges": es,
                        "carrier_parity": sum(ss) % 2,
                    })
    return records

def build_base_local_adj(g60_edges):
    adj = [[] for _ in range(N)]
    for slot in range(N_SLOT):
        base = slot * N_LOCAL
        for a, b in g60_edges:
            u = base + a
            v = base + b
            adj[u].append(v)
            adj[v].append(u)
    return [tuple(xs) for xs in adj]

def build_variant_adj(sign_bits):
    adj = [list(xs) for xs in BASE_LOCAL_ADJ]

    for idx, (su, sv) in enumerate(G15_EDGES):
        s = sign_bits[idx]
        bu = su * N_LOCAL
        bv = sv * N_LOCAL
        for x in range(N_LOCAL):
            y = (x + 30) % N_LOCAL if s else x
            u = bu + x
            v = bv + y
            adj[u].append(v)
            adj[v].append(u)

    return adj

def shortest_distance(adj, src, dst, seen, depth, stamp):
    if src == dst:
        return 0

    q = deque([src])
    seen[src] = stamp
    depth[src] = 0

    while q:
        v = q.popleft()
        nd = depth[v] + 1
        for w in adj[v]:
            if seen[w] != stamp:
                if w == dst:
                    return nd
                seen[w] = stamp
                depth[w] = nd
                q.append(w)

    return None

def compute_baseline_return_d(g15_edges, g60_edges):
    zero_bits = [0] * len(g15_edges)
    global G15_EDGES, BASE_LOCAL_ADJ
    old_g15 = G15_EDGES
    G15_EDGES = g15_edges
    BASE_LOCAL_ADJ = build_base_local_adj(g60_edges)
    adj = build_variant_adj(zero_bits)

    seen = [0] * N
    depth = [0] * N
    stamp = 0
    out = []

    for slot in range(N_SLOT):
        for x in range(N_LOCAL):
            stamp += 1
            src = gid(slot, x)
            dst = gid(slot, (x + 30) % N_LOCAL)
            out.append(shortest_distance(adj, src, dst, seen, depth, stamp))

    G15_EDGES = old_g15
    return out

def classify_combo(combo_indices):
    combo_set = set(combo_indices)
    odd_triangles = 0
    odd_slots = set()

    for tri in TRI_INDEX_RECORDS:
        toggled = sum(1 for idx in tri["edge_indices"] if idx in combo_set) % 2
        new_parity = tri["original_parity"] ^ toggled
        if new_parity == 1:
            odd_triangles += 1
            odd_slots.update(tri["triangle"])

    return odd_triangles, len(odd_slots)

def analyze_combo(combo_indices):
    sign_bits = list(ORIGINAL_SIGN_BITS)
    for idx in combo_indices:
        sign_bits[idx] = 1 - sign_bits[idx]

    odd_count, odd_slot_count = classify_combo(combo_indices)
    adj = build_variant_adj(sign_bits)

    seen = [0] * N
    depth = [0] * N
    stamp = 0
    deltas = []

    i = 0
    for slot in range(N_SLOT):
        for x in range(N_LOCAL):
            stamp += 1
            src = gid(slot, x)
            dst = gid(slot, (x + 30) % N_LOCAL)
            sd = shortest_distance(adj, src, dst, seen, depth, stamp)
            bd = BASELINE_RETURN_D[i]
            deltas.append(sd - bd)
            i += 1

    delta_counts = dict(sorted(Counter(deltas).items()))

    return {
        "toggle_edges": [list(G15_EDGES[i]) for i in combo_indices],
        "odd_triangle_count": odd_count,
        "odd_slot_count": odd_slot_count,
        "mean_actual_delta": sum(deltas) / len(deltas),
        "compressed_count": sum(1 for d in deltas if d < 0),
        "unchanged_count": sum(1 for d in deltas if d == 0),
        "expanded_count": sum(1 for d in deltas if d > 0),
        "delta_counts": delta_counts,
    }

def analyze_chunk(chunk):
    return [analyze_combo(combo) for combo in chunk]

def init_worker(g15_edges, g60_edges, original_sign_bits, tri_index_records, baseline_return_d, base_local_adj):
    global G15_EDGES, G60_EDGES, ORIGINAL_SIGN_BITS, TRI_INDEX_RECORDS, BASELINE_RETURN_D, BASE_LOCAL_ADJ
    G15_EDGES = g15_edges
    G60_EDGES = g60_edges
    ORIGINAL_SIGN_BITS = original_sign_bits
    TRI_INDEX_RECORDS = tri_index_records
    BASELINE_RETURN_D = baseline_return_d
    BASE_LOCAL_ADJ = base_local_adj

def chunks(iterable, size):
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) >= size:
            yield buf
            buf = []
    if buf:
        yield buf

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

    print("loading repaired Project 18 payload")
    g15_edges = sorted(read_g15_edges())
    g60_edges = read_g60_edges()
    signs_by_edge = read_signs_by_edge()
    original_sign_bits = [signs_by_edge[e] for e in g15_edges]

    edge_index = {e: i for i, e in enumerate(g15_edges)}
    triangles = triangle_records(g15_edges, signs_by_edge)

    tri_index_records = []
    for tri in triangles:
        tri_index_records.append({
            "triangle": tri["triangle"],
            "edge_indices": [edge_index[e] for e in tri["edges"]],
            "original_parity": tri["carrier_parity"],
        })

    print("building local adjacency")
    base_local_adj = build_base_local_adj(g60_edges)

    print("computing baseline half-flip distances")
    init_worker(g15_edges, g60_edges, original_sign_bits, tri_index_records, [], base_local_adj)
    baseline_return_d = compute_baseline_return_d(g15_edges, g60_edges)

    print("analyzing original")
    init_worker(g15_edges, g60_edges, original_sign_bits, tri_index_records, baseline_return_d, base_local_adj)
    original = analyze_combo(tuple())

    original_odd_count = sum(1 for t in triangles if t["carrier_parity"] == 1)
    original_odd_slots = sorted({s for t in triangles if t["carrier_parity"] == 1 for s in t["triangle"]})

    total_expected = math.comb(len(g15_edges), TOGGLE_SIZE)
    print("running full exhaustive same-size metric sweep")
    print("workers=" + str(WORKERS))
    print("chunk_size=" + str(CHUNK_SIZE))
    print("total_expected=" + str(total_expected))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    records_for_summary = []
    completed = 0

    combo_iter = combinations(range(len(g15_edges)), TOGGLE_SIZE)
    chunk_list = list(chunks(combo_iter, CHUNK_SIZE))

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "index",
            "odd_triangle_count",
            "odd_slot_count",
            "toggle_edges",
            "mean_actual_delta",
            "compressed_count",
            "unchanged_count",
            "expanded_count",
            "delta_counts",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        with ProcessPoolExecutor(
            max_workers=WORKERS,
            initializer=init_worker,
            initargs=(g15_edges, g60_edges, original_sign_bits, tri_index_records, baseline_return_d, base_local_adj),
        ) as ex:
            futures = [ex.submit(analyze_chunk, chunk) for chunk in chunk_list]

            for fut in as_completed(futures):
                batch = fut.result()
                for r in batch:
                    r["index"] = completed
                    completed += 1
                    records_for_summary.append(r)
                    writer.writerow({
                        "index": r["index"],
                        "odd_triangle_count": r["odd_triangle_count"],
                        "odd_slot_count": r["odd_slot_count"],
                        "toggle_edges": json.dumps(r["toggle_edges"]),
                        "mean_actual_delta": r["mean_actual_delta"],
                        "compressed_count": r["compressed_count"],
                        "unchanged_count": r["unchanged_count"],
                        "expanded_count": r["expanded_count"],
                        "delta_counts": json.dumps(r["delta_counts"], sort_keys=True),
                    })

                if completed == len(batch) or completed % PROGRESS_EVERY < len(batch) or completed == total_expected:
                    elapsed = time.time() - t0
                    print("progress " + str(completed) + "/" + str(total_expected) + " elapsed_seconds=" + str(round(elapsed, 2)))
                    f.flush()

    class_records = defaultdict(list)
    for r in records_for_summary:
        class_records[r["odd_triangle_count"]].append(r)

    by_odd_count = {}
    for odd_count in sorted(class_records):
        group = class_records[odd_count]
        by_odd_count[str(odd_count)] = {
            "count": len(group),
            "mean_actual_delta": summarize([r["mean_actual_delta"] for r in group]),
            "compressed_count": summarize([r["compressed_count"] for r in group]),
            "expanded_count": summarize([r["expanded_count"] for r in group]),
            "odd_slot_count": summarize([r["odd_slot_count"] for r in group]),
            "distinct_delta_patterns": len(Counter(json.dumps(r["delta_counts"], sort_keys=True) for r in group)),
        }

    class_medians = [
        (
            int(k),
            v["mean_actual_delta"]["median"],
            v["compressed_count"]["median"],
        )
        for k, v in by_odd_count.items()
    ]

    checks = {
        "total_matches_expected": completed == total_expected,
        "zero_odd_class_weaker_than_all_positive_odd_medians": all(
            by_odd_count["0"]["mean_actual_delta"]["median"] > by_odd_count[str(k)]["mean_actual_delta"]["median"]
            for k in sorted(int(x) for x in by_odd_count.keys())
            if k > 0
        ),
        "compressed_median_strictly_increases_until_saturation": (
            by_odd_count["0"]["compressed_count"]["median"]
            < by_odd_count["2"]["compressed_count"]["median"]
            < by_odd_count["4"]["compressed_count"]["median"]
            < by_odd_count["6"]["compressed_count"]["median"]
            < by_odd_count["8"]["compressed_count"]["median"]
            == by_odd_count["10"]["compressed_count"]["median"]
        ),
        "mean_delta_median_strictly_decreases_until_saturation": (
            by_odd_count["0"]["mean_actual_delta"]["median"]
            > by_odd_count["2"]["mean_actual_delta"]["median"]
            > by_odd_count["4"]["mean_actual_delta"]["median"]
            > by_odd_count["6"]["mean_actual_delta"]["median"]
            > by_odd_count["8"]["mean_actual_delta"]["median"]
            == by_odd_count["10"]["mean_actual_delta"]["median"]
        ),
        "no_expansion_in_any_same_size_variant": all(
            r["expanded_count"] == 0 for r in records_for_summary
        ),
    }

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "claim": "full exhaustive same-size metric sweep grouped by odd carrier triangle count",
        "source_payload": str(PAYLOAD),
        "toggle_size": TOGGLE_SIZE,
        "runtime_seconds": time.time() - t0,
        "workers": WORKERS,
        "chunk_size": CHUNK_SIZE,
        "total_variants": completed,
        "original": {
            "odd_triangle_count": original_odd_count,
            "odd_triangle_slots": original_odd_slots,
            "mean_actual_delta": original["mean_actual_delta"],
            "compressed_count": original["compressed_count"],
            "unchanged_count": original["unchanged_count"],
            "expanded_count": original["expanded_count"],
            "delta_counts": original["delta_counts"],
        },
        "by_odd_triangle_count": by_odd_count,
        "class_medians": class_medians,
        "checks": checks,
        "boundary": {
            "physical_gravity_claim": False,
            "finite_metric_census_claim": True,
            "metric_compression_claim": True,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Full Same-Size Metric Sweep")
    lines.append("")
    lines.append("This audit runs half-flip return metrics for every five-edge carrier-sign toggle set.")
    lines.append("")
    lines.append("No physical gravity claim is made. This is a finite graph-theoretic metric census.")
    lines.append("")
    lines.append("## Settings")
    lines.append("")
    lines.append(f"- toggle_size: {TOGGLE_SIZE}")
    lines.append(f"- total_variants: {completed}")
    lines.append(f"- workers: {WORKERS}")
    lines.append(f"- chunk_size: {CHUNK_SIZE}")
    lines.append(f"- runtime_seconds: {report['runtime_seconds']}")
    lines.append("")
    lines.append("## Original")
    lines.append("")
    lines.append(f"- odd_triangle_count: {original_odd_count}")
    lines.append(f"- odd_triangle_slots: {original_odd_slots}")
    lines.append(f"- mean_actual_delta: {original['mean_actual_delta']}")
    lines.append(f"- compressed_count: {original['compressed_count']}")
    lines.append(f"- delta_counts: {original['delta_counts']}")
    lines.append("")
    lines.append("## Full class summaries")
    lines.append("")
    for k, v in by_odd_count.items():
        lines.append(f"### odd_triangle_count {k}")
        lines.append("")
        lines.append(f"- count: {v['count']}")
        lines.append(f"- mean_actual_delta: {v['mean_actual_delta']}")
        lines.append(f"- compressed_count: {v['compressed_count']}")
        lines.append(f"- expanded_count: {v['expanded_count']}")
        lines.append(f"- odd_slot_count: {v['odd_slot_count']}")
        lines.append(f"- distinct_delta_patterns: {v['distinct_delta_patterns']}")
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
    lines.append("This full census upgrades audit 016 from a balanced sample to an exhaustive same-size metric result.")
    lines.append("")
    lines.append("The central question is whether odd carrier triangle count organizes a monotone finite metric gradient for half-flip return compression.")
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- artifacts/json/017_full_same_size_metric_sweep.json")
    lines.append("- artifacts/md/017_full_same_size_metric_sweep.md")
    lines.append("- artifacts/csv/017_full_same_size_metric_sweep.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_CSV)
    print("checks=" + json.dumps(checks, sort_keys=True))

if __name__ == "__main__":
    main()
