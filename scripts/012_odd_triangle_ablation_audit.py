from pathlib import Path
from collections import Counter, defaultdict, deque
from itertools import combinations
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = P18 / "source/kernel_payload"

OUT_JSON = ROOT / "artifacts/json/012_odd_triangle_ablation_audit.json"
OUT_MD = ROOT / "artifacts/md/012_odd_triangle_ablation_audit.md"
OUT_CSV = ROOT / "artifacts/csv/012_odd_triangle_ablation_returns.csv"

N_SLOT = 15
N_LOCAL = 60
N = N_SLOT * N_LOCAL

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

def build_baseline_edges(g15_edges, g60_edges):
    zeros = {e: 0 for e in g15_edges}
    return build_edges(g15_edges, g60_edges, zeros)

def adjacency(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for xs in adj:
        xs.sort()
    return adj

def shortest_distance(adj, src, dst):
    if src == dst:
        return 0
    dist = [-1] * len(adj)
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

def triangle_records(g15_edges, signs):
    es = set(g15_edges)
    out = []
    for a in range(N_SLOT):
        for b in range(a + 1, N_SLOT):
            for c in range(b + 1, N_SLOT):
                tri_edges = [edge(a, b), edge(a, c), edge(b, c)]
                if all(e in es for e in tri_edges):
                    ss = [signs[e] for e in tri_edges]
                    out.append({
                        "triangle": [a, b, c],
                        "edges": [list(e) for e in tri_edges],
                        "signs": ss,
                        "carrier_parity": sum(ss) % 2,
                    })
    return out

def canonical_cycle(path):
    rots = []
    for seq in (path, list(reversed(path))):
        for i in range(len(path)):
            rots.append(tuple(seq[i:] + seq[:i]))
    return min(rots)

def simple_cycles(g15_edges):
    adj = [[] for _ in range(N_SLOT)]
    for a, b in g15_edges:
        adj[a].append(b)
        adj[b].append(a)
    for xs in adj:
        xs.sort()

    cycles = set()

    def dfs(start, cur, path):
        for nb in adj[cur]:
            if nb == start and len(path) >= 3:
                cycles.add(canonical_cycle(path))
            elif nb > start and nb not in path:
                dfs(start, nb, path + [nb])

    for start in range(N_SLOT):
        dfs(start, start, [start])

    return sorted(cycles, key=lambda c: (len(c), c))

def cycle_parity(cycle, signs):
    s = 0
    for i in range(len(cycle)):
        s += signs[edge(cycle[i], cycle[(i + 1) % len(cycle)])]
    return s % 2

def best_odd_cycle_lengths(cycles, signs):
    best = {slot: None for slot in range(N_SLOT)}
    counts = Counter()

    for c in cycles:
        if cycle_parity(c, signs) == 1:
            for slot in c:
                counts[slot] += 1
                if best[slot] is None or len(c) < best[slot]:
                    best[slot] = len(c)

    return best, counts

def find_triangle_neutralizing_toggles(g15_edges, signs):
    carrier_edges = sorted(g15_edges)
    edge_index = {e: i for i, e in enumerate(carrier_edges)}
    tris = triangle_records(g15_edges, signs)

    odd_targets = [r["carrier_parity"] for r in tris]
    tri_edge_indices = []

    for r in tris:
        tri_edge_indices.append([edge_index[edge(*e)] for e in r["edges"]])

    for k in range(0, 8):
        for combo in combinations(range(len(carrier_edges)), k):
            combo_set = set(combo)
            ok = True
            for target, idxs in zip(odd_targets, tri_edge_indices):
                toggled_on_triangle = sum(1 for idx in idxs if idx in combo_set) % 2
                if toggled_on_triangle != target:
                    ok = False
                    break
            if ok:
                return [carrier_edges[i] for i in combo]

    raise RuntimeError("no triangle neutralizing toggle set found up to size 7")

def apply_toggles(signs, toggles):
    out = dict(signs)
    for e in toggles:
        out[e] = 1 - out[e]
    return out

def mean(vals):
    return sum(vals) / len(vals) if vals else None

def analyze_variant(name, g15_edges, g60_edges, signs, baseline_adj, cycles):
    signed_adj = adjacency(N, build_edges(g15_edges, g60_edges, signs))
    tris = triangle_records(g15_edges, signs)
    odd_tris = [r for r in tris if r["carrier_parity"] == 1]
    odd_slots = sorted({slot for r in odd_tris for slot in r["triangle"]})

    best_odd, odd_cycle_counts = best_odd_cycle_lengths(cycles, signs)

    rows = []
    deltas = []
    by_slot = defaultdict(list)

    for slot in range(N_SLOT):
        for x in range(N_LOCAL):
            y = (x + 30) % N_LOCAL
            src = gid(slot, x)
            dst = gid(slot, y)
            sd = shortest_distance(signed_adj, src, dst)
            bd = shortest_distance(baseline_adj, src, dst)
            delta = None if sd is None or bd is None else sd - bd
            if delta is not None:
                deltas.append(delta)
                by_slot[slot].append(delta)

            rows.append({
                "variant": name,
                "slot": slot,
                "local": x,
                "half_local": y,
                "signed_distance": sd,
                "baseline_distance": bd,
                "actual_delta": delta,
                "best_odd_cycle_len_at_slot": best_odd[slot],
                "odd_cycle_count_containing_slot": odd_cycle_counts[slot],
                "has_odd_triangle": slot in odd_slots,
            })

    slot_summary = {}
    for slot in range(N_SLOT):
        vals = by_slot[slot]
        slot_summary[str(slot)] = {
            "best_odd_cycle_len": best_odd[slot],
            "odd_cycle_count_containing_slot": odd_cycle_counts[slot],
            "has_odd_triangle": slot in odd_slots,
            "mean_actual_delta": mean(vals),
            "delta_counts": dict(sorted(Counter(vals).items())),
        }

    return {
        "name": name,
        "odd_triangle_count": len(odd_tris),
        "odd_triangles": odd_tris,
        "odd_triangle_slots": odd_slots,
        "delta_counts": dict(sorted(Counter(deltas).items())),
        "mean_actual_delta": mean(deltas),
        "compressed_count": sum(1 for d in deltas if d < 0),
        "unchanged_count": sum(1 for d in deltas if d == 0),
        "expanded_count": sum(1 for d in deltas if d > 0),
        "slot_summary": slot_summary,
        "rows": rows,
    }

def main():
    print("loading repaired Project 18 payload")
    g15_edges = read_g15_edges()
    g60_edges = read_g60_edges()
    signs = read_signs()
    cycles = simple_cycles(g15_edges)

    toggles = find_triangle_neutralizing_toggles(g15_edges, signs)
    neutralized_signs = apply_toggles(signs, toggles)

    baseline_adj = adjacency(N, build_baseline_edges(g15_edges, g60_edges))

    print("toggle_edges=" + str([list(e) for e in toggles]))
    print("analyzing original")
    original = analyze_variant("original", g15_edges, g60_edges, signs, baseline_adj, cycles)
    print("analyzing triangle_neutralized")
    neutralized = analyze_variant("triangle_neutralized", g15_edges, g60_edges, neutralized_signs, baseline_adj, cycles)

    csv_rows = original["rows"] + neutralized["rows"]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "variant",
            "slot",
            "local",
            "half_local",
            "signed_distance",
            "baseline_distance",
            "actual_delta",
            "best_odd_cycle_len_at_slot",
            "odd_cycle_count_containing_slot",
            "has_odd_triangle",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in csv_rows:
            w.writerow(r)

    checks = {
        "original_has_odd_triangles": original["odd_triangle_count"] > 0,
        "neutralized_has_no_odd_triangles": neutralized["odd_triangle_count"] == 0,
        "return_distribution_changes_after_neutralization": original["delta_counts"] != neutralized["delta_counts"],
        "minus3_compression_removed_by_neutralization": (
            original["delta_counts"].get(-3, 0) > 0 and neutralized["delta_counts"].get(-3, 0) == 0
        ),
        "neutralized_mean_less_compressive_than_original": (
            neutralized["mean_actual_delta"] > original["mean_actual_delta"]
        ),
    }

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "claim": "odd carrier triangles are causal contributors to the strongest half-flip return compression",
        "source_payload": str(PAYLOAD),
        "toggle_edges_to_neutralize_triangles": [list(e) for e in toggles],
        "original": {k: v for k, v in original.items() if k != "rows"},
        "triangle_neutralized": {k: v for k, v in neutralized.items() if k != "rows"},
        "checks": checks,
        "boundary": {
            "physical_gravity_claim": False,
            "finite_ablation_claim": True,
            "metric_compression_claim": True,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Odd Triangle Ablation Audit")
    lines.append("")
    lines.append("This audit tests whether the odd carrier triangles are causal contributors to the strongest half-flip return compression.")
    lines.append("")
    lines.append("No physical gravity claim is made. This is a finite graph-theoretic ablation test.")
    lines.append("")
    lines.append("## Toggle set")
    lines.append("")
    lines.append("Carrier edges toggled to neutralize all odd carrier triangles:")
    lines.append("")
    for e in toggles:
        lines.append(f"- {list(e)}")
    lines.append("")
    lines.append("## Original")
    lines.append("")
    lines.append(f"- odd_triangle_count: {original['odd_triangle_count']}")
    lines.append(f"- odd_triangle_slots: {original['odd_triangle_slots']}")
    lines.append(f"- mean_actual_delta: {original['mean_actual_delta']}")
    lines.append(f"- delta_counts: {original['delta_counts']}")
    lines.append(f"- compressed_count: {original['compressed_count']}")
    lines.append(f"- unchanged_count: {original['unchanged_count']}")
    lines.append(f"- expanded_count: {original['expanded_count']}")
    lines.append("")
    lines.append("## Triangle neutralized")
    lines.append("")
    lines.append(f"- odd_triangle_count: {neutralized['odd_triangle_count']}")
    lines.append(f"- odd_triangle_slots: {neutralized['odd_triangle_slots']}")
    lines.append(f"- mean_actual_delta: {neutralized['mean_actual_delta']}")
    lines.append(f"- delta_counts: {neutralized['delta_counts']}")
    lines.append(f"- compressed_count: {neutralized['compressed_count']}")
    lines.append(f"- unchanged_count: {neutralized['unchanged_count']}")
    lines.append(f"- expanded_count: {neutralized['expanded_count']}")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in checks.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The neutralized variant keeps the same slot graph, same local graph, and same number of carrier edges.")
    lines.append("Only selected carrier signs are toggled so that every carrier triangle has even parity.")
    lines.append("")
    lines.append("If the strongest return-compression class weakens or disappears after this toggle, then odd carrier triangles are not merely descriptive markers. They are causal contributors to the compression profile.")
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- artifacts/json/012_odd_triangle_ablation_audit.json")
    lines.append("- artifacts/md/012_odd_triangle_ablation_audit.md")
    lines.append("- artifacts/csv/012_odd_triangle_ablation_returns.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_CSV)
    print("checks=" + json.dumps(checks, sort_keys=True))
    print("original_delta_counts=" + str(original["delta_counts"]))
    print("neutralized_delta_counts=" + str(neutralized["delta_counts"]))

if __name__ == "__main__":
    main()
