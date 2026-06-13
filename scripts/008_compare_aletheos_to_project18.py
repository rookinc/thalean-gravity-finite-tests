from pathlib import Path
from collections import Counter, deque
import csv
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
CORI = ROOT.parents[2]
ALET = CORI / "aletheos.ai"
P18 = ROOT.parent / "18-g900-kernel-admission"

ALET_P900 = ALET / "public_html/json/p900"
P18_PAYLOAD = P18 / "source/kernel_payload"

OUT_JSON = ROOT / "artifacts/json/008_aletheos_project18_edge_comparison.json"
OUT_MD = ROOT / "artifacts/md/008_aletheos_project18_edge_comparison.md"

N_SLOT = 15
N_LOCAL = 60
N = N_SLOT * N_LOCAL

def gid(pair):
    return int(pair[0]) * N_LOCAL + int(pair[1])

def edge(a, b):
    a = int(a)
    b = int(b)
    if a == b:
        raise ValueError("loop edge")
    return (a, b) if a < b else (b, a)

def hash_edges(edges):
    text = "\n".join(str(a) + "," + str(b) for a, b in sorted(edges))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def read_csv_dict(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def read_p18_edges():
    rows = read_csv_dict(P18_PAYLOAD / "x_sigma_edges.csv")
    all_edges = set()
    internal_edges = set()
    external_edges = set()
    kind_counts = Counter()
    for r in rows:
        e = edge(r["u_vertex"], r["v_vertex"])
        all_edges.add(e)
        k = r.get("kind", "")
        kind_counts[k] += 1
        if "external" in k:
            external_edges.add(e)
        elif "internal" in k:
            internal_edges.add(e)
    return {
        "all": all_edges,
        "internal": internal_edges,
        "external": external_edges,
        "kind_counts": dict(sorted(kind_counts.items())),
    }

def read_aletheos_phase17_external():
    obj = load_json(ALET_P900 / "p900_phase17_external_edge_list.json")
    edges = set()
    for r in obj["external_edges"]:
        edges.add(edge(gid(r["a"]), gid(r["b"])))
    return obj, edges

def read_aletheos_phase30_edges():
    path = ALET_P900 / "p900_phase30_combined_graph_export.json"
    obj = load_json(path)
    candidates = []
    parsed_sets = []

    def walk(value, jpath="$"):
        parsed = parse_edge_list_guess(value)
        if parsed is not None:
            candidates.append({
                "path": jpath,
                "size": len(value) if isinstance(value, list) else None,
                "sample": value[:3] if isinstance(value, list) else None,
            })
            parsed_sets.append({
                "path": jpath,
                "size": len(value) if isinstance(value, list) else None,
                "parsed_edges": len(parsed),
                "sha256": hash_edges(parsed),
                "edges": parsed,
            })

        if isinstance(value, dict):
            for k, v in value.items():
                walk(v, jpath + "." + str(k))
        elif isinstance(value, list):
            for i, v in enumerate(value[:20]):
                walk(v, jpath + "[" + str(i) + "]")

    walk(obj)
    return obj, candidates, parsed_sets

def parse_edge_list_guess(value):
    if not isinstance(value, list):
        return None
    edges = set()
    ok = False
    for r in value:
        try:
            if isinstance(r, dict):
                if "u_vertex" in r and "v_vertex" in r:
                    edges.add(edge(r["u_vertex"], r["v_vertex"]))
                    ok = True
                elif "source" in r and "target" in r:
                    edges.add(edge(r["source"], r["target"]))
                    ok = True
                elif "u" in r and "v" in r:
                    edges.add(edge(r["u"], r["v"]))
                    ok = True
                elif "a" in r and "b" in r and isinstance(r["a"], list) and isinstance(r["b"], list):
                    edges.add(edge(gid(r["a"]), gid(r["b"])))
                    ok = True
            elif isinstance(r, list) and len(r) >= 2:
                if isinstance(r[0], list) and isinstance(r[1], list):
                    edges.add(edge(gid(r[0]), gid(r[1])))
                    ok = True
                else:
                    edges.add(edge(r[0], r[1]))
                    ok = True
        except Exception:
            return None
    return edges if ok else None

def metric(edges):
    adj = [[] for _ in range(N)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    ecc = []
    dd = Counter()
    for s in range(N):
        d = [-1] * N
        d[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            nd = d[v] + 1
            for w in adj[v]:
                if d[w] < 0:
                    d[w] = nd
                    q.append(w)
        if any(x < 0 for x in d):
            return {
                "connected": False,
                "edge_count": len(edges),
                "degree_counts": dict(sorted(Counter(len(x) for x in adj).items())),
            }
        ecc.append(max(d))
        for t in range(s + 1, N):
            dd[d[t]] += 1

    return {
        "connected": True,
        "edge_count": len(edges),
        "degree_counts": dict(sorted(Counter(len(x) for x in adj).items())),
        "diameter": max(ecc),
        "radius": min(ecc),
        "center_count": sum(1 for x in ecc if x == min(ecc)),
        "eccentricity_counts": dict(sorted(Counter(ecc).items())),
        "distance_distribution": dict(sorted(dd.items())),
    }

def main():
    p18 = read_p18_edges()
    phase17_obj, phase17_edges = read_aletheos_phase17_external()
    phase30_obj, phase30_candidates, phase30_sets = read_aletheos_phase30_edges()

    phase30_compact = []
    for item in phase30_sets:
        edges = item["edges"]
        phase30_compact.append({
            "path": item["path"],
            "size": item["size"],
            "parsed_edges": item["parsed_edges"],
            "sha256": item["sha256"],
            "equals_p18_all": edges == p18["all"],
            "equals_p18_external": edges == p18["external"],
            "metric_if_900_graph": metric(edges) if len(edges) == 3600 else None,
        })

    report = {
        "aletheos_root": str(ALET),
        "project18_root": str(P18),
        "phase17": {
            "external_edge_count_claim": phase17_obj.get("external_edge_count"),
            "parsed_external_edges": len(phase17_edges),
            "sha256": hash_edges(phase17_edges),
            "equals_project18_external": phase17_edges == p18["external"],
            "missing_from_project18_external": len(phase17_edges - p18["external"]),
            "extra_in_project18_external": len(p18["external"] - phase17_edges),
            "component_count": phase17_obj.get("component_count"),
            "degree_histogram": phase17_obj.get("degree_histogram"),
            "preferred_half_turn_set": phase17_obj.get("preferred_half_turn_set"),
        },
        "project18": {
            "all_edges": len(p18["all"]),
            "internal_edges": len(p18["internal"]),
            "external_edges": len(p18["external"]),
            "kind_counts": p18["kind_counts"],
            "all_sha256": hash_edges(p18["all"]),
            "external_sha256": hash_edges(p18["external"]),
        },
        "phase30": {
            "top_keys": sorted([str(k) for k in phase30_obj.keys()]) if isinstance(phase30_obj, dict) else [],
            "candidate_array_count": len(phase30_candidates),
            "candidate_arrays": phase30_candidates[:20],
            "parsed_edge_sets": phase30_compact,
        },
        "interpretation": {
            "phase17_is_upstream_external_source": phase17_edges == p18["external"],
            "full_graph_source_found_in_phase30": any(x["equals_p18_all"] for x in phase30_compact),
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Aletheos to Project 18 Edge Comparison")
    lines.append("")
    lines.append("This audit compares Aletheos P900 source artifacts against Project 18 kernel payload edges.")
    lines.append("")
    lines.append("## Phase 17 external comparison")
    lines.append("")
    p = report["phase17"]
    lines.append(f"- phase17 external_edge_count_claim: {p['external_edge_count_claim']}")
    lines.append(f"- phase17 parsed_external_edges: {p['parsed_external_edges']}")
    lines.append(f"- project18 external_edges: {report['project18']['external_edges']}")
    lines.append(f"- equals_project18_external: {p['equals_project18_external']}")
    lines.append(f"- missing_from_project18_external: {p['missing_from_project18_external']}")
    lines.append(f"- extra_in_project18_external: {p['extra_in_project18_external']}")
    lines.append(f"- phase17 sha256: `{p['sha256']}`")
    lines.append(f"- project18 external sha256: `{report['project18']['external_sha256']}`")
    lines.append(f"- component_count: {p['component_count']}")
    lines.append(f"- degree_histogram: {p['degree_histogram']}")
    lines.append(f"- preferred_half_turn_set: {p['preferred_half_turn_set']}")
    lines.append("")
    lines.append("## Project 18 edge split")
    lines.append("")
    q = report["project18"]
    lines.append(f"- all_edges: {q['all_edges']}")
    lines.append(f"- internal_edges: {q['internal_edges']}")
    lines.append(f"- external_edges: {q['external_edges']}")
    lines.append(f"- kind_counts: {q['kind_counts']}")
    lines.append(f"- all_sha256: `{q['all_sha256']}`")
    lines.append("")
    lines.append("## Phase 30 candidates")
    lines.append("")
    lines.append(f"- phase30 top_keys: {report['phase30']['top_keys']}")
    lines.append(f"- candidate_array_count: {report['phase30']['candidate_array_count']}")
    lines.append("")
    for item in report["phase30"]["parsed_edge_sets"]:
        lines.append(f"### {item['path']}")
        lines.append("")
        lines.append(f"- size: {item['size']}")
        lines.append(f"- parsed_edges: {item['parsed_edges']}")
        lines.append(f"- sha256: `{item['sha256']}`")
        lines.append(f"- equals_p18_all: {item['equals_p18_all']}")
        lines.append(f"- equals_p18_external: {item['equals_p18_external']}")
        if item["metric_if_900_graph"]:
            lines.append(f"- metric_if_900_graph: {item['metric_if_900_graph']}")
        lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(f"- phase17_is_upstream_external_source: {report['interpretation']['phase17_is_upstream_external_source']}")
    lines.append(f"- full_graph_source_found_in_phase30: {report['interpretation']['full_graph_source_found_in_phase30']}")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("phase17_equals_project18_external=" + str(report["phase17"]["equals_project18_external"]))
    print("phase30_full_graph_source_found=" + str(report["interpretation"]["full_graph_source_found_in_phase30"]))
    print("phase30_candidate_array_count=" + str(report["phase30"]["candidate_array_count"]))

if __name__ == "__main__":
    main()
