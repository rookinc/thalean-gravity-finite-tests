from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations
import csv
import json
import math

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = P18 / "source/kernel_payload"

OUT_JSON = ROOT / "artifacts/json/014_exhaustive_same_size_triangle_parity_control.json"
OUT_MD = ROOT / "artifacts/md/014_exhaustive_same_size_triangle_parity_control.md"
OUT_ZERO_CSV = ROOT / "artifacts/csv/014_zero_odd_toggle_sets.csv"
OUT_DIST_CSV = ROOT / "artifacts/csv/014_triangle_parity_distribution.csv"

N_SLOT = 15
PROGRESS_EVERY = 10000

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

def read_signs():
    rows = read_dict_csv(PAYLOAD / "carrier_signing_table.csv")
    out = {}
    for r in rows:
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
                        "signs": ss,
                        "carrier_parity": sum(ss) % 2,
                    })

    return records

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

def combo_key(combo):
    return ";".join(str(list(e)) for e in combo)

def main():
    print("loading repaired Project 18 payload from " + str(PAYLOAD))

    g15_edges = sorted(read_g15_edges())
    signs = read_signs()
    triangles = triangle_records(g15_edges, signs)
    neutralizer = find_triangle_neutralizing_toggles(g15_edges, signs)
    toggle_size = len(neutralizer)

    edge_index = {e: i for i, e in enumerate(g15_edges)}
    tri_index_records = []
    original_odd_slots = set()

    for tri in triangles:
        idxs = [edge_index[e] for e in tri["edges"]]
        tri_index_records.append({
            "triangle": tri["triangle"],
            "edge_indices": idxs,
            "original_parity": tri["carrier_parity"],
        })
        if tri["carrier_parity"] == 1:
            original_odd_slots.update(tri["triangle"])

    total_combos = math.comb(len(g15_edges), toggle_size)
    print("carrier_edges=" + str(len(g15_edges)))
    print("triangles=" + str(len(triangles)))
    print("toggle_size=" + str(toggle_size))
    print("total_same_size_combos=" + str(total_combos))
    print("neutralizer=" + combo_key(neutralizer))

    odd_triangle_count_dist = Counter()
    odd_slot_count_dist = Counter()
    joint_dist = Counter()
    zero_rows = []
    min_odd_triangle_count = None
    max_odd_triangle_count = None
    neutralizer_rank_key = combo_key(tuple(sorted(neutralizer)))
    neutralizer_record = None

    for idx, combo_indices in enumerate(combinations(range(len(g15_edges)), toggle_size), start=1):
        if idx % PROGRESS_EVERY == 0:
            print("progress " + str(idx) + "/" + str(total_combos))

        combo_set = set(combo_indices)
        odd_triangles = []
        odd_slots = set()

        for tri in tri_index_records:
            toggled_on_triangle = sum(1 for eidx in tri["edge_indices"] if eidx in combo_set) % 2
            new_parity = tri["original_parity"] ^ toggled_on_triangle
            if new_parity == 1:
                odd_triangles.append(tri["triangle"])
                odd_slots.update(tri["triangle"])

        odd_count = len(odd_triangles)
        odd_slot_count = len(odd_slots)

        odd_triangle_count_dist[odd_count] += 1
        odd_slot_count_dist[odd_slot_count] += 1
        joint_dist[(odd_count, odd_slot_count)] += 1

        if min_odd_triangle_count is None or odd_count < min_odd_triangle_count:
            min_odd_triangle_count = odd_count
        if max_odd_triangle_count is None or odd_count > max_odd_triangle_count:
            max_odd_triangle_count = odd_count

        combo_edges = tuple(g15_edges[i] for i in combo_indices)
        key = combo_key(combo_edges)

        rec = {
            "toggle_edges": [list(e) for e in combo_edges],
            "odd_triangle_count": odd_count,
            "odd_slot_count": odd_slot_count,
            "odd_triangles": odd_triangles,
            "odd_triangle_slots": sorted(odd_slots),
            "is_neutralizer": key == neutralizer_rank_key,
        }

        if odd_count == 0:
            zero_rows.append(rec)

        if key == neutralizer_rank_key:
            neutralizer_record = rec

    distribution_rows = []
    for (odd_count, odd_slot_count), count in sorted(joint_dist.items()):
        distribution_rows.append({
            "odd_triangle_count": odd_count,
            "odd_slot_count": odd_slot_count,
            "same_size_toggle_count": count,
        })

    with OUT_DIST_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "odd_triangle_count",
            "odd_slot_count",
            "same_size_toggle_count",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in distribution_rows:
            w.writerow(r)

    with OUT_ZERO_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "is_neutralizer",
            "toggle_edges",
            "odd_triangle_count",
            "odd_slot_count",
            "odd_triangles",
            "odd_triangle_slots",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in zero_rows:
            w.writerow({
                "is_neutralizer": r["is_neutralizer"],
                "toggle_edges": json.dumps(r["toggle_edges"]),
                "odd_triangle_count": r["odd_triangle_count"],
                "odd_slot_count": r["odd_slot_count"],
                "odd_triangles": json.dumps(r["odd_triangles"]),
                "odd_triangle_slots": json.dumps(r["odd_triangle_slots"]),
            })

    zero_count = len(zero_rows)
    controls_with_zero_excluding_neutralizer = sum(
        1 for r in zero_rows if not r["is_neutralizer"]
    )

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "claim": "exhaustive same-size sign parity control for odd triangle neutralization",
        "source_payload": str(PAYLOAD),
        "carrier_edge_count": len(g15_edges),
        "triangle_count": len(triangles),
        "original_odd_triangle_count": sum(1 for t in triangles if t["carrier_parity"] == 1),
        "original_odd_triangle_slots": sorted(original_odd_slots),
        "toggle_size": toggle_size,
        "total_same_size_combos": total_combos,
        "neutralizer": {
            "toggle_edges": [list(e) for e in neutralizer],
            "record": neutralizer_record,
        },
        "min_odd_triangle_count": min_odd_triangle_count,
        "max_odd_triangle_count": max_odd_triangle_count,
        "odd_triangle_count_distribution": {
            str(k): v for k, v in sorted(odd_triangle_count_dist.items())
        },
        "odd_slot_count_distribution": {
            str(k): v for k, v in sorted(odd_slot_count_dist.items())
        },
        "zero_odd_toggle_count": zero_count,
        "zero_odd_fraction": zero_count / total_combos,
        "zero_odd_controls_excluding_neutralizer": controls_with_zero_excluding_neutralizer,
        "zero_odd_toggle_sets": zero_rows,
        "checks": {
            "neutralizer_found": neutralizer_record is not None,
            "neutralizer_has_zero_odd_triangles": (
                neutralizer_record is not None
                and neutralizer_record["odd_triangle_count"] == 0
            ),
            "zero_odd_is_minimal_odd_triangle_count": min_odd_triangle_count == 0,
            "neutralizer_in_zero_odd_class": any(r["is_neutralizer"] for r in zero_rows),
            "zero_odd_class_is_rare_under_same_size_toggles": (
                zero_count / total_combos < 0.05
            ),
        },
        "boundary": {
            "physical_gravity_claim": False,
            "finite_parity_control_claim": True,
            "metric_compression_claim": False,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Exhaustive Same-Size Triangle Parity Control")
    lines.append("")
    lines.append("This audit enumerates every same-size carrier-sign toggle set and counts the resulting odd carrier triangles.")
    lines.append("")
    lines.append("No physical gravity claim is made. This is a finite sign-parity control, not a metric BFS audit.")
    lines.append("")
    lines.append("## Settings")
    lines.append("")
    lines.append(f"- carrier_edge_count: {len(g15_edges)}")
    lines.append(f"- triangle_count: {len(triangles)}")
    lines.append(f"- original_odd_triangle_count: {report['original_odd_triangle_count']}")
    lines.append(f"- original_odd_triangle_slots: {report['original_odd_triangle_slots']}")
    lines.append(f"- toggle_size: {toggle_size}")
    lines.append(f"- total_same_size_combos: {total_combos}")
    lines.append("")
    lines.append("## Neutralizer")
    lines.append("")
    lines.append(f"- toggle_edges: {[list(e) for e in neutralizer]}")
    lines.append(f"- odd_triangle_count: {neutralizer_record['odd_triangle_count']}")
    lines.append(f"- odd_slot_count: {neutralizer_record['odd_slot_count']}")
    lines.append("")
    lines.append("## Exhaustive distribution")
    lines.append("")
    lines.append(f"- min_odd_triangle_count: {min_odd_triangle_count}")
    lines.append(f"- max_odd_triangle_count: {max_odd_triangle_count}")
    lines.append(f"- zero_odd_toggle_count: {zero_count}")
    lines.append(f"- zero_odd_fraction: {zero_count / total_combos}")
    lines.append(f"- zero_odd_controls_excluding_neutralizer: {controls_with_zero_excluding_neutralizer}")
    lines.append("")
    lines.append("### Odd triangle count distribution")
    lines.append("")
    for k, v in sorted(odd_triangle_count_dist.items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("### Odd slot count distribution")
    lines.append("")
    for k, v in sorted(odd_slot_count_dist.items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in report["checks"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This audit asks whether the odd-triangle-neutralizing toggle set belongs to a rare same-size sign-parity class.")
    lines.append("")
    lines.append("If the zero-odd class is small, then audit 013's weak-compression result is not merely a generic five-edge sign disturbance. It belongs to a special parity regime where the odd carrier triangles have been erased.")
    lines.append("")
    lines.append("The next metric step is to run BFS compression metrics on every zero-odd toggle set, then compare that class against the sampled and original profiles.")
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- artifacts/json/014_exhaustive_same_size_triangle_parity_control.json")
    lines.append("- artifacts/md/014_exhaustive_same_size_triangle_parity_control.md")
    lines.append("- artifacts/csv/014_zero_odd_toggle_sets.csv")
    lines.append("- artifacts/csv/014_triangle_parity_distribution.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_ZERO_CSV)
    print("wrote", OUT_DIST_CSV)
    print("zero_odd_toggle_count=" + str(zero_count))
    print("zero_odd_fraction=" + str(zero_count / total_combos))
    print("checks=" + json.dumps(report["checks"], sort_keys=True))

if __name__ == "__main__":
    main()
