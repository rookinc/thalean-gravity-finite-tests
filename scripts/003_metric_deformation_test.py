from pathlib import Path
from collections import deque, Counter
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT.parent / "18-g900-kernel-admission" / "source" / "kernel_payload"

OUT_JSON = ROOT / "artifacts/json/003_metric_deformation_summary.json"
OUT_MD = ROOT / "artifacts/md/003_metric_deformation_report.md"
OUT_DELTA_CSV = ROOT / "artifacts/csv/003_delta_distribution.csv"
OUT_EXTREME_CSV = ROOT / "artifacts/csv/003_extreme_pairs.csv"

N_SLOT = 15
N_LOCAL = 60
N = N_SLOT * N_LOCAL

def gid(slot, local):
    return int(slot) * N_LOCAL + int(local)

def undirected(a, b):
    a = int(a)
    b = int(b)
    if a == b:
        raise ValueError("loop edge found: " + str(a))
    return (a, b) if a < b else (b, a)

def read_dict_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def read_g15_edges():
    rows = read_dict_csv(SRC / "g15_slot_edges.csv")
    return [undirected(r["slot_u"], r["slot_v"]) for r in rows]

def read_g60_edges():
    rows = read_dict_csv(SRC / "g60_local_edges.csv")
    return [undirected(r["local_u"], r["local_v"]) for r in rows]

def read_signing_table():
    rows = read_dict_csv(SRC / "carrier_signing_table.csv")
    out = []
    for r in rows:
        out.append((int(r["slot_u"]), int(r["slot_v"]), int(r["sign"])))
    return out

def build_baseline_edges(g15_edges, g60_edges):
    edges = set()

    for t in range(N_SLOT):
        for x, y in g60_edges:
            edges.add(undirected(gid(t, x), gid(t, y)))

    for t, u in g15_edges:
        for x in range(N_LOCAL):
            edges.add(undirected(gid(t, x), gid(u, x)))

    return edges

def build_signed_edges(g60_edges, signing):
    edges = set()

    for t in range(N_SLOT):
        for x, y in g60_edges:
            edges.add(undirected(gid(t, x), gid(t, y)))

    for t, u, sign in signing:
        for x in range(N_LOCAL):
            y = (x + 30) % 60 if sign else x
            edges.add(undirected(gid(t, x), gid(u, y)))

    return edges

def read_source_edges_flexible(path):
    rows = read_dict_csv(path)
    if not rows:
        return set(), "empty"

    headers = list(rows[0].keys())
    lower = {h.lower(): h for h in headers}

    direct_pairs = [
        ("u", "v"),
        ("a", "b"),
        ("src", "dst"),
        ("source", "target"),
        ("vertex_u", "vertex_v"),
        ("vertex_a", "vertex_b"),
        ("global_u", "global_v"),
        ("global_a", "global_b"),
    ]

    for a, b in direct_pairs:
        if a in lower and b in lower:
            edges = set()
            for r in rows:
                edges.add(undirected(r[lower[a]], r[lower[b]]))
            if all(0 <= x < N and 0 <= y < N for x, y in edges):
                return edges, "direct:" + a + "," + b

    slot_local_sets = [
        ("slot_u", "local_u", "slot_v", "local_v"),
        ("slot_a", "local_a", "slot_b", "local_b"),
        ("a_slot", "a_local", "b_slot", "b_local"),
        ("t_u", "x_u", "t_v", "x_v"),
        ("t_a", "x_a", "t_b", "x_b"),
    ]

    for su, lu, sv, lv in slot_local_sets:
        if su in lower and lu in lower and sv in lower and lv in lower:
            edges = set()
            for r in rows:
                a = gid(r[lower[su]], r[lower[lu]])
                b = gid(r[lower[sv]], r[lower[lv]])
                edges.add(undirected(a, b))
            return edges, "slot_local:" + ",".join([su, lu, sv, lv])

    numeric_cols = []
    for h in headers:
        ok = True
        vals = []
        for r in rows:
            try:
                vals.append(int(r[h]))
            except Exception:
                ok = False
                break
        if ok:
            numeric_cols.append((h, vals))

    best = None
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            ha, va = numeric_cols[i]
            hb, vb = numeric_cols[j]
            if not all(0 <= x < N for x in va + vb):
                continue
            try:
                edges = set(undirected(a, b) for a, b in zip(va, vb))
            except ValueError:
                continue
            max_seen = max(max(va), max(vb))
            score = (len(edges), max_seen)
            if best is None or score > best[0]:
                best = (score, edges, "numeric_pair:" + ha + "," + hb)

    if best:
        return best[1], best[2]

    raise RuntimeError("could not parse source edge file: " + str(path))

def build_adj(edges):
    adj = [[] for _ in range(N)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for xs in adj:
        xs.sort()
    return adj

def degree_counts(adj):
    return dict(sorted(Counter(len(xs) for xs in adj).items()))

def all_pairs_bfs(adj, label):
    all_dist = []
    for src in range(N):
        if src % 100 == 0:
            print(label + ": bfs root " + str(src) + "/" + str(N))
        dist = [-1] * N
        dist[src] = 0
        q = deque([src])
        while q:
            v = q.popleft()
            nd = dist[v] + 1
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = nd
                    q.append(w)
        if any(d < 0 for d in dist):
            raise RuntimeError(label + " is disconnected from root " + str(src))
        all_dist.append(dist)
    print(label + ": bfs done")
    return all_dist

def metric_summary(dist):
    ecc = [max(row) for row in dist]
    radius = min(ecc)
    diameter = max(ecc)
    centers = [i for i, e in enumerate(ecc) if e == radius]
    ecc_counts = dict(sorted(Counter(ecc).items()))

    dd = Counter()
    for i in range(N):
        row = dist[i]
        for j in range(i + 1, N):
            dd[row[j]] += 1

    return {
        "radius": radius,
        "diameter": diameter,
        "center_count": len(centers),
        "eccentricity_counts": ecc_counts,
        "distance_distribution": dict(sorted(dd.items())),
        "sample_centers": centers[:30],
    }

def deformation_summary(d_signed, d_base):
    delta_counts = Counter()
    by_base_distance = {}
    compressed = []
    expanded = []
    total = 0
    pair_count = 0

    for i in range(N):
        for j in range(i + 1, N):
            ds = d_signed[i][j]
            db = d_base[i][j]
            delta = ds - db
            total += delta
            pair_count += 1
            delta_counts[delta] += 1

            bucket = by_base_distance.setdefault(db, Counter())
            bucket[delta] += 1

            rec = (delta, i, j, db, ds)
            if delta < 0:
                compressed.append(rec)
            elif delta > 0:
                expanded.append(rec)

    compressed.sort()
    expanded.sort(reverse=True)

    return {
        "pair_count": pair_count,
        "delta_counts": dict(sorted(delta_counts.items())),
        "mean_delta": total / pair_count,
        "compressed_pair_count": sum(c for d, c in delta_counts.items() if d < 0),
        "unchanged_pair_count": delta_counts.get(0, 0),
        "expanded_pair_count": sum(c for d, c in delta_counts.items() if d > 0),
        "min_delta": min(delta_counts),
        "max_delta": max(delta_counts),
        "by_baseline_distance": {
            str(k): dict(sorted(v.items())) for k, v in sorted(by_base_distance.items())
        },
        "top_compressed_pairs": [
            {"delta": d, "u": i, "v": j, "baseline_d": db, "signed_d": ds}
            for d, i, j, db, ds in compressed[:30]
        ],
        "top_expanded_pairs": [
            {"delta": d, "u": i, "v": j, "baseline_d": db, "signed_d": ds}
            for d, i, j, db, ds in expanded[:30]
        ],
    }

def write_csvs(defm):
    with OUT_DELTA_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["delta", "pair_count"])
        for k, v in defm["delta_counts"].items():
            w.writerow([k, v])

    with OUT_EXTREME_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["class", "delta", "u", "v", "baseline_d", "signed_d"])
        for r in defm["top_compressed_pairs"]:
            w.writerow(["compressed", r["delta"], r["u"], r["v"], r["baseline_d"], r["signed_d"]])
        for r in defm["top_expanded_pairs"]:
            w.writerow(["expanded", r["delta"], r["u"], r["v"], r["baseline_d"], r["signed_d"]])

def write_report(report):
    lines = []
    lines.append("# Metric Deformation Test")
    lines.append("")
    lines.append("This is the first finite Thalean gravity test.")
    lines.append("")
    lines.append("It compares the canonical signed carrier graph X_sigma against the untwisted product baseline X_0.")
    lines.append("")
    lines.append("No physical gravity claim is made here. The tested claim is finite and graph-theoretic: signed carrier transport induces a measurable metric deformation.")
    lines.append("")
    lines.append("## Edge checks")
    lines.append("")
    lines.append(f"- generated_signed_edges: {report['edge_checks']['generated_signed_edges']}")
    lines.append(f"- source_signed_edges: {report['edge_checks']['source_signed_edges']}")
    lines.append(f"- source_parse_mode: {report['edge_checks']['source_parse_mode']}")
    lines.append(f"- generated_matches_source: {report['edge_checks']['generated_matches_source']}")
    lines.append(f"- baseline_edges: {report['edge_checks']['baseline_edges']}")
    lines.append(f"- signed_degree_counts: {report['edge_checks']['signed_degree_counts']}")
    lines.append(f"- baseline_degree_counts: {report['edge_checks']['baseline_degree_counts']}")
    lines.append("")
    lines.append("## Metric summaries")
    lines.append("")
    for name in ["signed_metric", "baseline_metric"]:
        m = report[name]
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"- diameter: {m['diameter']}")
        lines.append(f"- radius: {m['radius']}")
        lines.append(f"- center_count: {m['center_count']}")
        lines.append(f"- eccentricity_counts: {m['eccentricity_counts']}")
        lines.append(f"- distance_distribution: {m['distance_distribution']}")
        lines.append("")
    d = report["deformation"]
    lines.append("## Deformation summary")
    lines.append("")
    lines.append(f"- pair_count: {d['pair_count']}")
    lines.append(f"- delta_counts: {d['delta_counts']}")
    lines.append(f"- mean_delta: {d['mean_delta']}")
    lines.append(f"- compressed_pair_count: {d['compressed_pair_count']}")
    lines.append(f"- unchanged_pair_count: {d['unchanged_pair_count']}")
    lines.append(f"- expanded_pair_count: {d['expanded_pair_count']}")
    lines.append(f"- min_delta: {d['min_delta']}")
    lines.append(f"- max_delta: {d['max_delta']}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if report["edge_checks"]["generated_matches_source"]:
        lines.append("- The generated signed graph matches the source X_sigma edge file.")
    else:
        lines.append("- WARNING: The generated signed graph does not match the source X_sigma edge file.")
    lines.append("- A negative delta means the signed carrier graph shortens a pairwise distance relative to the untwisted baseline.")
    lines.append("- A positive delta means the signed carrier graph lengthens a pairwise distance relative to the untwisted baseline.")
    lines.append("- The finite gravity signal is the organized deformation field d_signed - d_baseline.")
    lines.append("")
    lines.append("## Output files")
    lines.append("")
    lines.append("- artifacts/json/003_metric_deformation_summary.json")
    lines.append("- artifacts/csv/003_delta_distribution.csv")
    lines.append("- artifacts/csv/003_extreme_pairs.csv")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

def main():
    print("loading kernel payload from " + str(SRC))

    g15_edges = read_g15_edges()
    g60_edges = read_g60_edges()
    signing = read_signing_table()

    print("g15_edges=" + str(len(g15_edges)))
    print("g60_edges=" + str(len(g60_edges)))
    print("signing_rows=" + str(len(signing)))

    signed_edges = build_signed_edges(g60_edges, signing)
    baseline_edges = build_baseline_edges(g15_edges, g60_edges)
    source_edges, parse_mode = read_source_edges_flexible(SRC / "x_sigma_edges.csv")

    signed_adj = build_adj(signed_edges)
    baseline_adj = build_adj(baseline_edges)

    print("signed_edges=" + str(len(signed_edges)))
    print("baseline_edges=" + str(len(baseline_edges)))
    print("source_edges=" + str(len(source_edges)))
    print("source_parse_mode=" + parse_mode)
    print("generated_matches_source=" + str(signed_edges == source_edges))

    d_signed = all_pairs_bfs(signed_adj, "signed")
    d_base = all_pairs_bfs(baseline_adj, "baseline")

    signed_metric = metric_summary(d_signed)
    baseline_metric = metric_summary(d_base)
    defm = deformation_summary(d_signed, d_base)

    report = {
        "project": "19-thalean-gravity-finite-tests",
        "source": str(SRC),
        "claim": "finite carrier-induced metric deformation",
        "edge_checks": {
            "generated_signed_edges": len(signed_edges),
            "source_signed_edges": len(source_edges),
            "source_parse_mode": parse_mode,
            "generated_matches_source": signed_edges == source_edges,
            "baseline_edges": len(baseline_edges),
            "signed_degree_counts": degree_counts(signed_adj),
            "baseline_degree_counts": degree_counts(baseline_adj),
            "signed_only_edge_count": len(signed_edges - source_edges),
            "source_only_edge_count": len(source_edges - signed_edges),
        },
        "signed_metric": signed_metric,
        "baseline_metric": baseline_metric,
        "deformation": defm,
        "boundary": {
            "physical_gravity_claim": False,
            "gr_claim": False,
            "newtonian_claim": False,
            "finite_graph_metric_claim": True,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_csvs(defm)
    write_report(report)

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("wrote", OUT_DELTA_CSV)
    print("wrote", OUT_EXTREME_CSV)
    print("signed_diameter=" + str(signed_metric["diameter"]))
    print("signed_radius=" + str(signed_metric["radius"]))
    print("baseline_diameter=" + str(baseline_metric["diameter"]))
    print("baseline_radius=" + str(baseline_metric["radius"]))
    print("delta_counts=" + str(defm["delta_counts"]))
    print("mean_delta=" + str(defm["mean_delta"]))

if __name__ == "__main__":
    main()
