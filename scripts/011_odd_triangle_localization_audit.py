from pathlib import Path
from collections import Counter, defaultdict
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = P18 / "source/kernel_payload"

IN_RETURN_CSV = ROOT / "artifacts/csv/010_holonomy_return_pairs.csv"

OUT_JSON = ROOT / "artifacts/json/011_odd_triangle_localization_audit.json"
OUT_MD = ROOT / "artifacts/md/011_odd_triangle_localization_audit.md"
OUT_CSV = ROOT / "artifacts/csv/011_slot_triangle_compression.csv"

N_SLOT = 15

def edge(a, b):
    a = int(a)
    b = int(b)
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
                es = [edge(a, b), edge(b, c), edge(a, c)]
                if all(e in edge_set for e in es):
                    ss = [signs[e] for e in es]
                    parity = sum(ss) % 2
                    records.append({
                        "triangle": [a, b, c],
                        "edges": [list(e) for e in es],
                        "signs": ss,
                        "carrier_parity": parity,
                    })
    return records

def read_return_pairs():
    rows = read_dict_csv(IN_RETURN_CSV)
    out = []
    for r in rows:
        out.append({
            "slot": int(r["slot"]),
            "local": int(r["local"]),
            "best_odd_cycle_len": int(r["best_odd_cycle_len_at_slot"]) if r["best_odd_cycle_len_at_slot"] else None,
            "signed_distance": int(r["signed_distance"]),
            "baseline_distance": int(r["baseline_distance"]),
            "actual_delta": int(r["actual_delta_signed_minus_baseline"]),
        })
    return out

def mean(xs):
    return sum(xs) / len(xs) if xs else None

def main():
    g15_edges = read_g15_edges()
    signs = read_signs()
    triangles = triangle_records(g15_edges, signs)
    returns = read_return_pairs()

    odd_triangles = [r for r in triangles if r["carrier_parity"] == 1]
    even_triangles = [r for r in triangles if r["carrier_parity"] == 0]

    odd_triangle_slots = set()
    even_triangle_slots = set()

    for r in odd_triangles:
        odd_triangle_slots.update(r["triangle"])
    for r in even_triangles:
        even_triangle_slots.update(r["triangle"])

    by_slot_returns = defaultdict(list)
    for r in returns:
        by_slot_returns[r["slot"]].append(r)

    slot_rows = []
    slot_summary = {}

    for slot in range(N_SLOT):
        rs = by_slot_returns[slot]
        deltas = [r["actual_delta"] for r in rs]
        best_lens = sorted(set(r["best_odd_cycle_len"] for r in rs))
        has_odd_triangle = slot in odd_triangle_slots
        has_even_triangle = slot in even_triangle_slots

        odd_tri_count = sum(1 for t in odd_triangles if slot in t["triangle"])
        even_tri_count = sum(1 for t in even_triangles if slot in t["triangle"])

        delta_counts = dict(sorted(Counter(deltas).items()))
        compressed_count = sum(1 for d in deltas if d < 0)
        unchanged_count = sum(1 for d in deltas if d == 0)
        expanded_count = sum(1 for d in deltas if d > 0)

        rec = {
            "slot": slot,
            "has_odd_triangle": has_odd_triangle,
            "has_even_triangle": has_even_triangle,
            "odd_triangle_count": odd_tri_count,
            "even_triangle_count": even_tri_count,
            "best_odd_cycle_lens": best_lens,
            "return_pair_count": len(rs),
            "compressed_count": compressed_count,
            "unchanged_count": unchanged_count,
            "expanded_count": expanded_count,
            "mean_actual_delta": mean(deltas),
            "delta_counts": delta_counts,
        }

        slot_summary[str(slot)] = rec

        slot_rows.append({
            "slot": slot,
            "has_odd_triangle": str(has_odd_triangle),
            "odd_triangle_count": odd_tri_count,
            "even_triangle_count": even_tri_count,
            "best_odd_cycle_lens": ";".join(str(x) for x in best_lens),
            "return_pair_count": len(rs),
            "compressed_count": compressed_count,
            "unchanged_count": unchanged_count,
            "expanded_count": expanded_count,
            "mean_actual_delta": mean(deltas),
            "delta_counts": json.dumps(delta_counts, sort_keys=True),
        })

    odd_triangle_slot_deltas = []
    no_odd_triangle_slot_deltas = []

    for slot in range(N_SLOT):
        vals = [r["actual_delta"] for r in by_slot_returns[slot]]
        if slot in odd_triangle_slots:
            odd_triangle_slot_deltas.extend(vals)
        else:
            no_odd_triangle_slot_deltas.extend(vals)

    checks = {
        "all_odd_triangle_slots_have_best_odd_len_3": all(
            3 in slot_summary[str(slot)]["best_odd_cycle_lens"]
            for slot in odd_triangle_slots
        ),
        "no_non_odd_triangle_slot_has_best_odd_len_3": all(
            3 not in slot_summary[str(slot)]["best_odd_cycle_lens"]
            for slot in range(N_SLOT)
            if slot not in odd_triangle_slots
        ),
        "no_return_pair_expansion": all(
            slot_summary[str(slot)]["expanded_count"] == 0
            for slot in range(N_SLOT)
        ),
        "odd_triangle_slots_more_compressive_than_non_odd_triangle_slots": (
            mean(odd_triangle_slot_deltas) < mean(no_odd_triangle_slot_deltas)
        ),
    }

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "source_payload": str(PAYLOAD),
        "claim": "odd carrier triangles localize the strongest half-flip return compression",
        "counts": {
            "g15_edges": len(g15_edges),
            "triangle_count": len(triangles),
            "odd_triangle_count": len(odd_triangles),
            "even_triangle_count": len(even_triangles),
            "odd_triangle_slot_count": len(odd_triangle_slots),
            "non_odd_triangle_slot_count": N_SLOT - len(odd_triangle_slots),
        },
        "odd_triangles": odd_triangles,
        "even_triangles": even_triangles,
        "odd_triangle_slots": sorted(odd_triangle_slots),
        "non_odd_triangle_slots": [
            slot for slot in range(N_SLOT) if slot not in odd_triangle_slots
        ],
        "slot_summary": slot_summary,
        "aggregate_delta_by_slot_class": {
            "odd_triangle_slots": {
                "count": len(odd_triangle_slot_deltas),
                "mean_actual_delta": mean(odd_triangle_slot_deltas),
                "delta_counts": dict(sorted(Counter(odd_triangle_slot_deltas).items())),
            },
            "non_odd_triangle_slots": {
                "count": len(no_odd_triangle_slot_deltas),
                "mean_actual_delta": mean(no_odd_triangle_slot_deltas),
                "delta_counts": dict(sorted(Counter(no_odd_triangle_slot_deltas).items())),
            },
        },
        "checks": checks,
        "boundary": {
            "physical_gravity_claim": False,
            "finite_holonomy_localization_claim": True,
            "metric_compression_claim": True,
        },
    }

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "slot",
            "has_odd_triangle",
            "odd_triangle_count",
            "even_triangle_count",
            "best_odd_cycle_lens",
            "return_pair_count",
            "compressed_count",
            "unchanged_count",
            "expanded_count",
            "mean_actual_delta",
            "delta_counts",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in slot_rows:
            w.writerow(r)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Odd Triangle Localization Audit")
    lines.append("")
    lines.append("This audit tests whether odd carrier triangles localize the strongest half-flip return compression.")
    lines.append("")
    lines.append("No physical gravity claim is made. This is a finite graph-theoretic holonomy-localization test.")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    for k, v in report["counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Odd carrier triangles")
    lines.append("")
    for r in odd_triangles:
        lines.append(f"- triangle {r['triangle']} signs={r['signs']} parity={r['carrier_parity']}")
    lines.append("")
    lines.append("## Slot classes")
    lines.append("")
    lines.append(f"- odd_triangle_slots: {report['odd_triangle_slots']}")
    lines.append(f"- non_odd_triangle_slots: {report['non_odd_triangle_slots']}")
    lines.append("")
    lines.append("## Aggregate compression by slot class")
    lines.append("")
    for cls, data in report["aggregate_delta_by_slot_class"].items():
        lines.append(f"### {cls}")
        lines.append("")
        lines.append(f"- count: {data['count']}")
        lines.append(f"- mean_actual_delta: {data['mean_actual_delta']}")
        lines.append(f"- delta_counts: {data['delta_counts']}")
        lines.append("")
    lines.append("## Per-slot summary")
    lines.append("")
    for slot in range(N_SLOT):
        r = slot_summary[str(slot)]
        lines.append(f"### Slot {slot}")
        lines.append("")
        lines.append(f"- has_odd_triangle: {r['has_odd_triangle']}")
        lines.append(f"- odd_triangle_count: {r['odd_triangle_count']}")
        lines.append(f"- even_triangle_count: {r['even_triangle_count']}")
        lines.append(f"- best_odd_cycle_lens: {r['best_odd_cycle_lens']}")
        lines.append(f"- mean_actual_delta: {r['mean_actual_delta']}")
        lines.append(f"- delta_counts: {r['delta_counts']}")
        lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in checks.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("Odd carrier triangles are length-3 closed slot cycles whose carrier parity is one.")
    lines.append("Transport around such a cycle returns to the same slot with the local coordinate half-flipped.")
    lines.append("")
    lines.append("The audit shows whether the strongest half-flip return compression is localized exactly on slots touching such odd triangles.")
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- artifacts/json/011_odd_triangle_localization_audit.json")
    lines.append("- artifacts/md/011_odd_triangle_localization_audit.md")
    lines.append("- artifacts/csv/011_slot_triangle_compression.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_CSV)
    print("odd_triangles=" + str(len(odd_triangles)))
    print("odd_triangle_slots=" + str(sorted(odd_triangle_slots)))
    print("non_odd_triangle_slots=" + str(report["non_odd_triangle_slots"]))
    print("checks=" + json.dumps(checks, sort_keys=True))

if __name__ == "__main__":
    main()
