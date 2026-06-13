from pathlib import Path
from collections import Counter, deque
import csv
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SRC18 = ROOT.parent / "18-g900-kernel-admission"
EDGE_FILE = SRC18 / "source/kernel_payload/x_sigma_edges.csv"
CERT_FILE = SRC18 / "artifacts/json/metric_certificate.json"

OUT_JSON = ROOT / "artifacts/json/006_metric_parser_path_audit.json"
OUT_MD = ROOT / "artifacts/md/006_metric_parser_path_audit.md"

N = 900

def edge(a, b):
    a = int(a)
    b = int(b)
    if a == b:
        raise ValueError("loop")
    return (a, b) if a < b else (b, a)

def read_rows(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def hash_edges(edges):
    text = "\n".join(str(a) + "," + str(b) for a, b in sorted(edges))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def parse_correct_direct(rows):
    return set(edge(r["u_vertex"], r["v_vertex"]) for r in rows)

def parse_slot_local_named(rows):
    return set(
        edge(
            int(r["u_slot"]) * 60 + int(r["u_local"]),
            int(r["v_slot"]) * 60 + int(r["v_local"]),
        )
        for r in rows
    )

def parse_project18_metric_style(rows):
    parsed = set()
    skipped = 0
    examples = []
    for r in rows:
        xs = []
        for k, v in r.items():
            try:
                xs.append(int(v))
            except Exception:
                pass

        if len(xs) < 4:
            skipped += 1
            if len(examples) < 8:
                examples.append({"reason": "fewer_than_4_ints", "row": r})
            continue

        a_slot, a_local, b_slot, b_local = xs[:4]
        if 0 <= a_slot < 15 and 0 <= b_slot < 15 and 0 <= a_local < 60 and 0 <= b_local < 60:
            a = a_slot * 60 + a_local
            b = b_slot * 60 + b_local
            try:
                parsed.add(edge(a, b))
            except Exception:
                skipped += 1
                if len(examples) < 8:
                    examples.append({"reason": "loop_after_project18_parse", "row": r, "xs4": xs[:4]})
        else:
            skipped += 1
            if len(examples) < 8:
                examples.append({"reason": "bounds_fail", "row": r, "xs4": xs[:4]})
    return parsed, skipped, examples

def adj(edges):
    out = [[] for _ in range(N)]
    for a, b in edges:
        out[a].append(b)
        out[b].append(a)
    return out

def metric(edges):
    a = adj(edges)
    dd = Counter()
    ecc = []
    connected = True
    for s in range(N):
        d = [-1] * N
        d[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            for w in a[v]:
                if d[w] < 0:
                    d[w] = d[v] + 1
                    q.append(w)
        if any(x < 0 for x in d):
            connected = False
            ecc.append(None)
            continue
        ecc.append(max(d))
        for t in range(s + 1, N):
            dd[d[t]] += 1

    if not connected:
        return {
            "connected": False,
            "degree_counts": dict(sorted(Counter(len(x) for x in a).items())),
        }

    return {
        "connected": True,
        "edge_count": len(edges),
        "degree_counts": dict(sorted(Counter(len(x) for x in a).items())),
        "diameter": max(ecc),
        "radius": min(ecc),
        "center_count": sum(1 for x in ecc if x == min(ecc)),
        "eccentricity_counts": dict(sorted(Counter(ecc).items())),
        "distance_distribution": dict(sorted(dd.items())),
    }

def norm_dict(d):
    return {int(k): v for k, v in d.items()}

def main():
    rows = read_rows(EDGE_FILE)
    cert = json.loads(CERT_FILE.read_text(encoding="utf-8"))

    correct = parse_correct_direct(rows)
    named = parse_slot_local_named(rows)
    p18, skipped, examples = parse_project18_metric_style(rows)

    correct_metric = metric(correct)
    p18_metric = metric(p18)

    cert_metric = {
        "diameter": cert.get("diameter"),
        "radius": cert.get("radius"),
        "center_count": cert.get("center_count"),
        "eccentricity_counts": norm_dict(cert.get("eccentricity_counts", {})),
        "distance_distribution": norm_dict(cert.get("distance_distribution", {})),
    }

    p18_compact = {
        "diameter": p18_metric.get("diameter"),
        "radius": p18_metric.get("radius"),
        "center_count": p18_metric.get("center_count"),
        "eccentricity_counts": p18_metric.get("eccentricity_counts"),
        "distance_distribution": p18_metric.get("distance_distribution"),
    }

    correct_compact = {
        "diameter": correct_metric.get("diameter"),
        "radius": correct_metric.get("radius"),
        "center_count": correct_metric.get("center_count"),
        "eccentricity_counts": correct_metric.get("eccentricity_counts"),
        "distance_distribution": correct_metric.get("distance_distribution"),
    }

    report = {
        "edge_file": str(EDGE_FILE),
        "row_count": len(rows),
        "edge_counts": {
            "correct_direct": len(correct),
            "slot_local_named": len(named),
            "project18_metric_style": len(p18),
            "project18_metric_style_skipped_rows": skipped,
        },
        "hashes": {
            "correct_direct": hash_edges(correct),
            "slot_local_named": hash_edges(named),
            "project18_metric_style": hash_edges(p18),
            "certificate_source_edge_id_set_sha256": cert.get("hashes", {}).get("source_edge_id_set_sha256"),
        },
        "edge_set_equalities": {
            "correct_direct_equals_slot_local_named": correct == named,
            "correct_direct_equals_project18_metric_style": correct == p18,
        },
        "metrics": {
            "correct_direct": correct_metric,
            "project18_metric_style": p18_metric,
            "certificate": cert_metric,
        },
        "matches_certificate": {
            "correct_direct": correct_compact == cert_metric,
            "project18_metric_style": p18_compact == cert_metric,
        },
        "project18_parse_skip_examples": examples,
        "interpretation": {
            "likely_issue": "Project 18 metric certificate parser may read u_vertex,v_vertex,u_slot,u_local as slot/local fields.",
            "safe_claim": "Use correct direct u_vertex/v_vertex parse for Project 19 metric-deformation tests.",
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Metric Parser Path Audit")
    lines.append("")
    lines.append("This audit compares three ways of reading Project 18 `x_sigma_edges.csv`.")
    lines.append("")
    lines.append("## Edge counts")
    lines.append("")
    for k, v in report["edge_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Hashes")
    lines.append("")
    for k, v in report["hashes"].items():
        lines.append(f"- {k}: `{v}`")
    lines.append("")
    lines.append("## Edge-set equalities")
    lines.append("")
    for k, v in report["edge_set_equalities"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Certificate match")
    lines.append("")
    for k, v in report["matches_certificate"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Correct direct metric")
    lines.append("")
    m = report["metrics"]["correct_direct"]
    lines.append(f"- diameter: {m.get('diameter')}")
    lines.append(f"- radius: {m.get('radius')}")
    lines.append(f"- center_count: {m.get('center_count')}")
    lines.append(f"- eccentricity_counts: {m.get('eccentricity_counts')}")
    lines.append(f"- distance_distribution: {m.get('distance_distribution')}")
    lines.append("")
    lines.append("## Project 18 metric-style parse")
    lines.append("")
    m = report["metrics"]["project18_metric_style"]
    lines.append(f"- connected: {m.get('connected')}")
    lines.append(f"- edge_count: {m.get('edge_count')}")
    lines.append(f"- degree_counts: {m.get('degree_counts')}")
    lines.append(f"- diameter: {m.get('diameter')}")
    lines.append(f"- radius: {m.get('radius')}")
    lines.append(f"- center_count: {m.get('center_count')}")
    lines.append(f"- eccentricity_counts: {m.get('eccentricity_counts')}")
    lines.append(f"- distance_distribution: {m.get('distance_distribution')}")
    lines.append("")
    lines.append("## Skip examples")
    lines.append("")
    for ex in examples:
        lines.append(f"- {ex}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("If `correct_direct` fails to match the old certificate while the source edge file is correct, Project 19 should proceed with corrected direct parsing and record the Project 18 detailed metric certificate as needing regeneration.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("correct_edges=" + str(len(correct)))
    print("named_edges=" + str(len(named)))
    print("p18_style_edges=" + str(len(p18)))
    print("p18_style_skipped=" + str(skipped))
    print("correct_equals_named=" + str(correct == named))
    print("correct_matches_certificate=" + str(report["matches_certificate"]["correct_direct"]))
    print("p18_style_matches_certificate=" + str(report["matches_certificate"]["project18_metric_style"]))

if __name__ == "__main__":
    main()
