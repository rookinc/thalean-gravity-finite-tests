from pathlib import Path
from collections import Counter, deque
from itertools import combinations
import csv
import json
import os
import random
import statistics

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = P18 / "source/kernel_payload"

OUT_JSON = ROOT / "artifacts/json/013_same_size_toggle_control_audit.json"
OUT_MD = ROOT / "artifacts/md/013_same_size_toggle_control_audit.md"
OUT_CSV = ROOT / "artifacts/csv/013_same_size_toggle_controls.csv"

N_SLOT = 15
N_LOCAL = 60
N = N_SLOT * N_LOCAL

SEED = int(os.environ.get("CONTROL_SEED", "90013"))
CONTROL_SAMPLES = int(os.environ.get("CONTROL_SAMPLES", "60"))

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
                        "edges": tri_edges,
                        "signs": ss,
                        "carrier_parity": sum(ss) % 2,
                    })
    return out

def find_triangle_neutralizing_toggles(g15_edges, signs):
    carrier_edges = sorted(g15_edges)
    edge_index = {e: i for i, e in enumerate(carrier_edges)}
    tris = triangle_records(g15_edges, signs)

    targets = [r["carrier_parity"] for r in tris]
    tri_edge_indices = []
    for r in tris:
        tri_edge_indices.append([edge_index[e] for e in r["edges"]])

    for k in range(0, 8):
        for combo in combinations(range(len(carrier_edges)), k):
            combo_set = set(combo)
            ok = True
            for target, idxs in zip(targets, tri_edge_indices):
                toggled_on_triangle = sum(1 for idx in idxs if idx in combo_set) % 2
                if toggled_on_triangle != target:
                    ok = False
                    break
            if ok:
                return tuple(carrier_edges[i] for i in combo)

    raise RuntimeError("no triangle neutralizing toggle set found")

def apply_toggles(signs, toggles):
    out = dict(signs)
    for e in toggles:
        out[e] = 1 - out[e]
    return out

def analyze_variant(name, g15_edges, g60_edges, signs, baseline_adj, toggles):
    adj = adjacency(N, build_edges(g15_edges, g60_edges, signs))

    deltas = []
    for slot in range(N_SLOT):
        for x in range(N_LOCAL):
            src = gid(slot, x)
            dst = gid(slot, (x + 30) % N_LOCAL)
            sd = shortest_distance(adj, src, dst)
            bd = shortest_distance(baseline_adj, src, dst)
            deltas.append(sd - bd)

    tris = triangle_records(g15_edges, signs)
    odd_tris = [r for r in tris if r["carrier_parity"] == 1]

    return {
        "name": name,
        "toggle_edges": [list(e) for e in toggles],
        "toggle_count": len(toggles),
        "odd_triangle_count": len(odd_tris),
        "odd_triangle_slots": sorted({s for r in odd_tris for s in r["triangle"]}),
        "mean_actual_delta": sum(deltas) / len(deltas),
        "compressed_count": sum(1 for d in deltas if d < 0),
        "unchanged_count": sum(1 for d in deltas if d == 0),
        "expanded_count": sum(1 for d in deltas if d > 0),
        "delta_counts": dict(sorted(Counter(deltas).items())),
    }

def median(xs):
    return statistics.median(xs) if xs else None

def main():
    random.seed(SEED)

    print("loading repaired Project 18 payload")
    print("control_samples=" + str(CONTROL_SAMPLES))
    print("seed=" + str(SEED))

    g15_edges = read_g15_edges()
    g60_edges = read_g60_edges()
    signs = read_signs()

    baseline_signs = {e: 0 for e in g15_edges}
    baseline_adj = adjacency(N, build_edges(g15_edges, g60_edges, baseline_signs))

    neutralizer = find_triangle_neutralizing_toggles(g15_edges, signs)
    neutralizer_set = set(neutralizer)
    neutralized_signs = apply_toggles(signs, neutralizer)

    carrier_edges = sorted(g15_edges)

    print("analyzing original")
    original = analyze_variant("original", g15_edges, g60_edges, signs, baseline_adj, ())

    print("analyzing triangle_neutralized")
    neutralized = analyze_variant(
        "triangle_neutralized",
        g15_edges,
        g60_edges,
        neutralized_signs,
        baseline_adj,
        neutralizer,
    )

    controls = []
    seen = {tuple(sorted(neutralizer))}
    attempts = 0

    print("analyzing controls")
    while len(controls) < CONTROL_SAMPLES:
        attempts += 1
        combo = tuple(sorted(random.sample(carrier_edges, len(neutralizer))))
        if combo in seen:
            continue
        seen.add(combo)

        control_signs = apply_toggles(signs, combo)
        idx = len(controls) + 1
        print("control " + str(idx) + "/" + str(CONTROL_SAMPLES))
        controls.append(
            analyze_variant(
                "control_" + str(idx).zfill(3),
                g15_edges,
                g60_edges,
                control_signs,
                baseline_adj,
                combo,
            )
        )

    means = [r["mean_actual_delta"] for r in controls]
    compressed = [r["compressed_count"] for r in controls]
    odd_counts = [r["odd_triangle_count"] for r in controls]

    controls_less_or_equal_compressive_than_neutralized = [
        r for r in controls
        if r["mean_actual_delta"] >= neutralized["mean_actual_delta"]
    ]

    controls_with_no_odd_triangles = [
        r for r in controls
        if r["odd_triangle_count"] == 0
    ]

    rows = []
    for r in [original, neutralized] + controls:
        rows.append({
            "name": r["name"],
            "toggle_edges": json.dumps(r["toggle_edges"]),
            "toggle_count": r["toggle_count"],
            "odd_triangle_count": r["odd_triangle_count"],
            "odd_triangle_slots": json.dumps(r["odd_triangle_slots"]),
            "mean_actual_delta": r["mean_actual_delta"],
            "compressed_count": r["compressed_count"],
            "unchanged_count": r["unchanged_count"],
            "expanded_count": r["expanded_count"],
            "delta_counts": json.dumps(r["delta_counts"], sort_keys=True),
        })

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "name",
            "toggle_edges",
            "toggle_count",
            "odd_triangle_count",
            "odd_triangle_slots",
            "mean_actual_delta",
            "compressed_count",
            "unchanged_count",
            "expanded_count",
            "delta_counts",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    control_summary = {
        "control_count": len(controls),
        "attempts": attempts,
        "mean_actual_delta_min": min(means),
        "mean_actual_delta_median": median(means),
        "mean_actual_delta_max": max(means),
        "compressed_count_min": min(compressed),
        "compressed_count_median": median(compressed),
        "compressed_count_max": max(compressed),
        "odd_triangle_count_min": min(odd_counts),
        "odd_triangle_count_median": median(odd_counts),
        "odd_triangle_count_max": max(odd_counts),
        "controls_less_or_equal_compressive_than_neutralized_count": len(controls_less_or_equal_compressive_than_neutralized),
        "controls_with_no_odd_triangles_count": len(controls_with_no_odd_triangles),
    }

    checks = {
        "neutralized_has_no_odd_triangles": neutralized["odd_triangle_count"] == 0,
        "neutralized_removes_minus3_class": neutralized["delta_counts"].get(-3, 0) == 0,
        "neutralized_less_compressive_than_original": neutralized["mean_actual_delta"] > original["mean_actual_delta"],
        "some_controls_preserve_stronger_compression_than_neutralized": any(
            r["mean_actual_delta"] < neutralized["mean_actual_delta"] for r in controls
        ),
    }

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "claim": "same-size controls test whether triangle neutralization is specific rather than generic sign-toggle disturbance",
        "source_payload": str(PAYLOAD),
        "seed": SEED,
        "control_samples": CONTROL_SAMPLES,
        "original": original,
        "triangle_neutralized": neutralized,
        "control_summary": control_summary,
        "checks": checks,
        "controls": controls,
        "boundary": {
            "physical_gravity_claim": False,
            "finite_control_ablation_claim": True,
            "metric_compression_claim": True,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Same-Size Toggle Control Audit")
    lines.append("")
    lines.append("This audit compares the odd-triangle-neutralizing toggle set against random same-size carrier-sign toggle controls.")
    lines.append("")
    lines.append("No physical gravity claim is made. This is a finite graph-theoretic control test.")
    lines.append("")
    lines.append("## Settings")
    lines.append("")
    lines.append(f"- seed: {SEED}")
    lines.append(f"- control_samples: {CONTROL_SAMPLES}")
    lines.append(f"- toggle_size: {len(neutralizer)}")
    lines.append("")
    lines.append("## Original")
    lines.append("")
    lines.append(f"- odd_triangle_count: {original['odd_triangle_count']}")
    lines.append(f"- mean_actual_delta: {original['mean_actual_delta']}")
    lines.append(f"- compressed_count: {original['compressed_count']}")
    lines.append(f"- delta_counts: {original['delta_counts']}")
    lines.append("")
    lines.append("## Triangle neutralized")
    lines.append("")
    lines.append(f"- toggle_edges: {neutralized['toggle_edges']}")
    lines.append(f"- odd_triangle_count: {neutralized['odd_triangle_count']}")
    lines.append(f"- mean_actual_delta: {neutralized['mean_actual_delta']}")
    lines.append(f"- compressed_count: {neutralized['compressed_count']}")
    lines.append(f"- delta_counts: {neutralized['delta_counts']}")
    lines.append("")
    lines.append("## Control summary")
    lines.append("")
    for k, v in control_summary.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in checks.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The triangle-neutralized variant changes five carrier signs, exactly like each random control.")
    lines.append("This test asks whether the weakening seen in audit 012 is specific to removing odd carrier triangles, or whether it is typical of arbitrary five-edge sign toggles.")
    lines.append("")
    lines.append("A strong specificity signal occurs if the triangle-neutralized variant has no odd triangles and is much less compressive than most same-size controls.")
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- artifacts/json/013_same_size_toggle_control_audit.json")
    lines.append("- artifacts/md/013_same_size_toggle_control_audit.md")
    lines.append("- artifacts/csv/013_same_size_toggle_controls.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_CSV)
    print("checks=" + json.dumps(checks, sort_keys=True))
    print("control_summary=" + json.dumps(control_summary, sort_keys=True))

if __name__ == "__main__":
    main()
