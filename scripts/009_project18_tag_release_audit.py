from pathlib import Path
from collections import Counter, deque
import csv
import io
import json
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"

OUT_JSON = ROOT / "artifacts/json/009_project18_tag_release_audit.json"
OUT_MD = ROOT / "artifacts/md/009_project18_tag_release_audit.md"

N = 900
REFS = [
    "HEAD",
    "g900-kernel-admission-manuscript-v1.0.0",
    "g900-kernel-admission-bounded-qed-v1.0.0",
    "138dc5c",
]

EDGE_PATH = "source/kernel_payload/x_sigma_edges.csv"
CERT_PATH = "artifacts/json/metric_certificate.json"

def run_git(args):
    p = subprocess.run(
        ["git"] + args,
        cwd=str(P18),
        text=True,
        capture_output=True,
    )
    return {
        "ok": p.returncode == 0,
        "stdout": p.stdout,
        "stderr": p.stderr,
        "returncode": p.returncode,
    }

def git_show(ref, path):
    return run_git(["show", ref + ":" + path])

def edge(a, b):
    a = int(a)
    b = int(b)
    if a == b:
        raise ValueError("loop")
    return (a, b) if a < b else (b, a)

def hash_edges(edges):
    text = "\n".join(str(a) + "," + str(b) for a, b in sorted(edges))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def parse_edges(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    edges = set()

    for r in rows:
        if "u_vertex" in r and "v_vertex" in r:
            edges.add(edge(r["u_vertex"], r["v_vertex"]))
        elif "u_slot" in r and "u_local" in r and "v_slot" in r and "v_local" in r:
            a = int(r["u_slot"]) * 60 + int(r["u_local"])
            b = int(r["v_slot"]) * 60 + int(r["v_local"])
            edges.add(edge(a, b))
        elif "slot_a" in r and "local_a" in r and "slot_b" in r and "local_b" in r:
            a = int(r["slot_a"]) * 60 + int(r["local_a"])
            b = int(r["slot_b"]) * 60 + int(r["local_b"])
            edges.add(edge(a, b))
        else:
            raise RuntimeError("unknown edge headers: " + repr(list(r.keys())))

    return edges, rows[0].keys() if rows else []

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

def norm_int_keys(d):
    if not isinstance(d, dict):
        return d
    out = {}
    for k, v in d.items():
        try:
            out[int(k)] = v
        except Exception:
            out[k] = v
    return out

def compact_cert(obj):
    if not isinstance(obj, dict):
        return None
    return {
        "diameter": obj.get("diameter"),
        "radius": obj.get("radius"),
        "center_count": obj.get("center_count"),
        "eccentricity_counts": norm_int_keys(obj.get("eccentricity_counts")),
        "distance_distribution": norm_int_keys(obj.get("distance_distribution")),
        "hashes": obj.get("hashes"),
        "source_edge_file": obj.get("source_edge_file"),
    }

def compact_metric(m):
    return {
        "diameter": m.get("diameter"),
        "radius": m.get("radius"),
        "center_count": m.get("center_count"),
        "eccentricity_counts": m.get("eccentricity_counts"),
        "distance_distribution": m.get("distance_distribution"),
    }

def main():
    report = {
        "project18_root": str(P18),
        "git_current": {
            "head": run_git(["rev-parse", "--short", "HEAD"]),
            "branch": run_git(["branch", "--show-current"]),
            "tags_at_head": run_git(["tag", "--points-at", "HEAD"]),
            "status_short": run_git(["status", "--short"]),
        },
        "refs": [],
    }

    for ref in REFS:
        item = {"ref": ref}

        rev = run_git(["rev-parse", "--short", ref])
        item["rev_parse"] = {
            "ok": rev["ok"],
            "stdout": rev["stdout"].strip(),
            "stderr": rev["stderr"].strip(),
        }

        e = git_show(ref, EDGE_PATH)
        item["edge_file_ok"] = e["ok"]
        item["edge_file_error"] = e["stderr"].strip()

        if e["ok"]:
            edges, headers = parse_edges(e["stdout"])
            m = metric(edges)
            item["edge_headers"] = list(headers)
            item["edge_count"] = len(edges)
            item["edge_sha256"] = hash_edges(edges)
            item["metric_from_edge_file"] = m
        else:
            item["edge_headers"] = []
            item["edge_count"] = None
            item["edge_sha256"] = None
            item["metric_from_edge_file"] = None

        c = git_show(ref, CERT_PATH)
        item["cert_file_ok"] = c["ok"]
        item["cert_file_error"] = c["stderr"].strip()

        if c["ok"]:
            obj = json.loads(c["stdout"])
            cert = compact_cert(obj)
            item["metric_certificate"] = cert
            item["edge_metric_matches_certificate"] = (
                compact_metric(item["metric_from_edge_file"]) == {
                    "diameter": cert.get("diameter"),
                    "radius": cert.get("radius"),
                    "center_count": cert.get("center_count"),
                    "eccentricity_counts": cert.get("eccentricity_counts"),
                    "distance_distribution": cert.get("distance_distribution"),
                }
                if item["metric_from_edge_file"] else False
            )
        else:
            item["metric_certificate"] = None
            item["edge_metric_matches_certificate"] = None

        report["refs"].append(item)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Project 18 Tag/Release Audit")
    lines.append("")
    lines.append("This audit compares Project 18 HEAD and release refs without checking out or modifying Project 18.")
    lines.append("")
    lines.append("## Current Project 18 git state")
    lines.append("")
    for k, v in report["git_current"].items():
        lines.append(f"- {k}: ok={v.get('ok')} stdout=`{v.get('stdout').strip()}` stderr=`{v.get('stderr').strip()}`")
    lines.append("")
    lines.append("## Ref comparisons")
    lines.append("")
    for item in report["refs"]:
        lines.append(f"### {item['ref']}")
        lines.append("")
        lines.append(f"- rev_parse_ok: {item['rev_parse']['ok']}")
        lines.append(f"- rev: `{item['rev_parse']['stdout']}`")
        lines.append(f"- edge_file_ok: {item['edge_file_ok']}")
        lines.append(f"- cert_file_ok: {item['cert_file_ok']}")
        lines.append(f"- edge_headers: {item['edge_headers']}")
        lines.append(f"- edge_count: {item['edge_count']}")
        lines.append(f"- edge_sha256: `{item['edge_sha256']}`")
        lines.append(f"- edge_metric_matches_certificate: {item['edge_metric_matches_certificate']}")
        m = item.get("metric_from_edge_file") or {}
        lines.append("")
        lines.append("Edge-file metric:")
        lines.append(f"- connected: {m.get('connected')}")
        lines.append(f"- diameter: {m.get('diameter')}")
        lines.append(f"- radius: {m.get('radius')}")
        lines.append(f"- center_count: {m.get('center_count')}")
        lines.append(f"- eccentricity_counts: {m.get('eccentricity_counts')}")
        lines.append(f"- distance_distribution: {m.get('distance_distribution')}")
        c = item.get("metric_certificate") or {}
        lines.append("")
        lines.append("Certificate metric:")
        lines.append(f"- diameter: {c.get('diameter')}")
        lines.append(f"- radius: {c.get('radius')}")
        lines.append(f"- center_count: {c.get('center_count')}")
        lines.append(f"- eccentricity_counts: {c.get('eccentricity_counts')}")
        lines.append(f"- distance_distribution: {c.get('distance_distribution')}")
        lines.append(f"- hashes: {c.get('hashes')}")
        lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("If the bounded-QED tag exists and its edge-file metric matches its certificate, then the paper release is internally consistent and Project 19 should cite that release separately from local HEAD.")
    lines.append("If the bounded-QED tag does not exist locally, fetch tags or inspect the remote before making a stronger claim.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    for item in report["refs"]:
        print(item["ref"] + ": rev=" + str(item["rev_parse"]["stdout"]) + " match=" + str(item["edge_metric_matches_certificate"]))

if __name__ == "__main__":
    main()
