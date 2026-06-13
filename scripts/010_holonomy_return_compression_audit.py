from pathlib import Path
from collections import Counter, deque, defaultdict
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = P18 / "source/kernel_payload"

OUT_JSON = ROOT / "artifacts/json/010_holonomy_return_compression_audit.json"
OUT_MD = ROOT / "artifacts/md/010_holonomy_return_compression_audit.md"
OUT_CSV = ROOT / "artifacts/csv/010_holonomy_return_pairs.csv"

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
    rows = read_dict_csv(PAYLOAD / "g15_slot_edges.csv")
    return [edge(r["slot_u"], r["slot_v"]) for r in rows]

def read_g60_edges():
    rows = read_dict_csv(PAYLOAD / "g60_local_edges.csv")
    return [edge(r["local_u"], r["local_v"]) for r in rows]

def read_signing():
    rows = read_dict_csv(PAYLOAD / "carrier_signing_table.csv")
    signs = {}
    for r in rows:
        e = edge(r["slot_u"], r["slot_v"])
        signs[e] = int(r["sign"])
    return signs

def build_signed_edges(g60_edges, signs):
    edges = set()

    for slot in range(N_SLOT):
        for a, b in g60_edges:
            edges.add(edge(gid(slot, a), gid(slot, b)))

    for (su, sv), sign in signs.items():
        for x in range(N_LOCAL):
            y = (x + 30) % N_LOCAL if sign else x
            edges.add(edge(gid(su, x), gid(sv, y)))

    return edges

def build_baseline_edges(g15_edges, g60_edges):
    edges = set()

    for slot in range(N_SLOT):
        for a, b in g60_edges:
            edges.add(edge(gid(slot, a), gid(slot, b)))

    for su, sv in g15_edges:
        for x in range(N_LOCAL):
            edges.add(edge(gid(su, x), gid(sv, x)))

    return edges

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

def all_pairs_bfs_small(adj):
    out = []
    for src in range(len(adj)):
        dist = [-1] * len(adj)
        dist[src] = 0
        q = deque([src])
        while q:
            v = q.popleft()
            nd = dist[v] + 1
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = nd
                    q.append(w)
        out.append(dist)
    return out

def canonical_cycle(path):
    n = len(path)
    rots = []
    for seq in (path, list(reversed(path))):
        for i in range(n):
            rots.append(tuple(seq[i:] + seq[:i]))
    return min(rots)

def enumerate_simple_cycles(g15_edges):
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
    total = 0
    n = len(cycle)
    for i in range(n):
        e = edge(cycle[i], cycle[(i + 1) % n])
        total += signs.get(e, 0)
    return total % 2

def main():
    print("loading Project 18 repaired payload from " + str(PAYLOAD))

    g15_edges = read_g15_edges()
    g60_edges = read_g60_edges()
    signs = read_signing()

    print("g15_edges=" + str(len(g15_edges)))
    print("g60_edges=" + str(len(g60_edges)))
    print("signed_carrier_edges=" + str(len(signs)))

    signed_edges = build_signed_edges(g60_edges, signs)
    baseline_edges = build_baseline_edges(g15_edges, g60_edges)

    signed_adj = adjacency(N, signed_edges)
    baseline_adj = adjacency(N, baseline_edges)
    g60_adj = adjacency(N_LOCAL, g60_edges)

    print("signed_edges=" + str(len(signed_edges)))
    print("baseline_edges=" + str(len(baseline_edges)))
    print("enumerating G15 simple cycles")

    cycles = enumerate_simple_cycles(g15_edges)

    cycle_records = []
    length_parity = Counter()
    best_odd_len_by_slot = {slot: None for slot in range(N_SLOT)}
    odd_cycles_by_slot = Counter()

    for c in cycles:
        p = cycle_parity(c, signs)
        length_parity[(len(c), p)] += 1
        rec = {
            "cycle": list(c),
            "length": len(c),
            "carrier_parity": p,
        }
        cycle_records.append(rec)

        if p == 1:
            for slot in c:
                odd_cycles_by_slot[slot] += 1
                cur = best_odd_len_by_slot[slot]
                if cur is None or len(c) < cur:
                    best_odd_len_by_slot[slot] = len(c)

    print("cycle_count=" + str(len(cycles)))
    print("odd_cycle_count=" + str(sum(1 for r in cycle_records if r["carrier_parity"] == 1)))

    print("computing G60 distances")
    g60_dist = all_pairs_bfs_small(g60_adj)

    rows = []
    actual_delta_counts = Counter()
    shortcut_delta_counts = Counter()
    slot_actual = defaultdict(list)

    print("computing half-flip return pair distances")
    for slot in range(N_SLOT):
        print("slot " + str(slot) + "/" + str(N_SLOT))
        best_odd = best_odd_len_by_slot[slot]
        for x in range(N_LOCAL):
            y = (x + 30) % N_LOCAL
            src = gid(slot, x)
            dst = gid(slot, y)

            signed_d = shortest_distance(signed_adj, src, dst)
            baseline_d = shortest_distance(baseline_adj, src, dst)
            internal_d = g60_dist[x][y]

            actual_delta = signed_d - baseline_d
            actual_delta_counts[actual_delta] += 1
            slot_actual[slot].append(actual_delta)

            if best_odd is None:
                shortcut_delta = None
            else:
                shortcut_delta = best_odd - internal_d
                shortcut_delta_counts[shortcut_delta] += 1

            rows.append({
                "slot": slot,
                "local": x,
                "half_local": y,
                "best_odd_cycle_len_at_slot": best_odd,
                "internal_g60_half_flip_distance": internal_d,
                "signed_distance": signed_d,
                "baseline_distance": baseline_d,
                "actual_delta_signed_minus_baseline": actual_delta,
                "shortcut_delta_best_odd_minus_internal": shortcut_delta,
            })

    by_slot = {}
    for slot, vals in sorted(slot_actual.items()):
        by_slot[str(slot)] = {
            "count": len(vals),
            "mean_actual_delta": sum(vals) / len(vals),
            "actual_delta_counts": dict(sorted(Counter(vals).items())),
            "best_odd_cycle_len": best_odd_len_by_slot[slot],
            "odd_cycle_count_containing_slot": odd_cycles_by_slot[slot],
        }

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "slot",
            "local",
            "half_local",
            "best_odd_cycle_len_at_slot",
            "internal_g60_half_flip_distance",
            "signed_distance",
            "baseline_distance",
            "actual_delta_signed_minus_baseline",
            "shortcut_delta_best_odd_minus_internal",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "source_payload": str(PAYLOAD),
        "claim": "carrier holonomy induces half-flip return paths and measurable return-pair metric deformation",
        "counts": {
            "g15_edges": len(g15_edges),
            "g60_edges": len(g60_edges),
            "signed_edges": len(signed_edges),
            "baseline_edges": len(baseline_edges),
            "simple_cycle_count": len(cycles),
            "odd_holonomy_cycle_count": sum(1 for r in cycle_records if r["carrier_parity"] == 1),
            "even_holonomy_cycle_count": sum(1 for r in cycle_records if r["carrier_parity"] == 0),
            "return_pair_count": len(rows),
        },
        "cycle_length_parity_counts": {
            str(k): v for k, v in sorted(length_parity.items())
        },
        "best_odd_cycle_len_by_slot": {
            str(k): v for k, v in sorted(best_odd_len_by_slot.items())
        },
        "actual_delta_counts": dict(sorted(actual_delta_counts.items())),
        "shortcut_delta_counts": dict(sorted(shortcut_delta_counts.items())),
        "by_slot": by_slot,
        "sample_odd_cycles": [
            r for r in cycle_records if r["carrier_parity"] == 1
        ][:20],
        "boundary": {
            "physical_gravity_claim": False,
            "finite_graph_holonomy_claim": True,
            "metric_deformation_claim": True,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Holonomy Return Compression Audit")
    lines.append("")
    lines.append("This audit tests whether nontrivial signed carrier cycles create half-flip return paths and measurable metric deformation.")
    lines.append("")
    lines.append("No physical gravity claim is made. This is a finite graph-theoretic holonomy and metric test.")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    for k, v in report["counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Cycle parity")
    lines.append("")
    for k, v in report["cycle_length_parity_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Best odd holonomy cycle length by slot")
    lines.append("")
    for k, v in report["best_odd_cycle_len_by_slot"].items():
        lines.append(f"- slot {k}: {v}")
    lines.append("")
    lines.append("## Return-pair metric deformation")
    lines.append("")
    lines.append("Return pairs are pairs of the form `(slot,x)` to `(slot,x+30)`.")
    lines.append("")
    lines.append(f"- actual_delta_counts: {report['actual_delta_counts']}")
    lines.append(f"- shortcut_delta_counts: {report['shortcut_delta_counts']}")
    lines.append("")
    lines.append("Here `actual_delta = signed_distance - baseline_distance`.")
    lines.append("")
    lines.append("- negative actual delta means signed carrier holonomy shortens the half-flip return pair.")
    lines.append("- zero means no change for that pair.")
    lines.append("- positive means the signed carrier graph lengthens that pair.")
    lines.append("")
    lines.append("## By slot")
    lines.append("")
    for slot, data in report["by_slot"].items():
        lines.append(f"### Slot {slot}")
        lines.append("")
        lines.append(f"- best_odd_cycle_len: {data['best_odd_cycle_len']}")
        lines.append(f"- odd_cycle_count_containing_slot: {data['odd_cycle_count_containing_slot']}")
        lines.append(f"- mean_actual_delta: {data['mean_actual_delta']}")
        lines.append(f"- actual_delta_counts: {data['actual_delta_counts']}")
        lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("An odd carrier cycle is a finite holonomy witness: transport around the closed slot cycle returns to the same slot with local coordinate shifted by 30.")
    lines.append("")
    lines.append("The audit asks whether those half-flip return paths are metric-active relative to the untwisted baseline.")
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- artifacts/json/010_holonomy_return_compression_audit.json")
    lines.append("- artifacts/md/010_holonomy_return_compression_audit.md")
    lines.append("- artifacts/csv/010_holonomy_return_pairs.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_CSV)
    print("odd_holonomy_cycle_count=" + str(report["counts"]["odd_holonomy_cycle_count"]))
    print("actual_delta_counts=" + str(report["actual_delta_counts"]))
    print("shortcut_delta_counts=" + str(report["shortcut_delta_counts"]))

if __name__ == "__main__":
    main()
