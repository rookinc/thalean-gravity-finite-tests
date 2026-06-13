from pathlib import Path
import json
import hashlib
import csv
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SRC18 = ROOT.parent / "18-g900-kernel-admission"
PAYLOAD = SRC18 / "source" / "kernel_payload"

OUT_JSON = ROOT / "artifacts/json/005_project18_provenance_audit.json"
OUT_MD = ROOT / "artifacts/md/005_project18_provenance_audit.md"

FILES = [
    "source/kernel_payload/x_sigma_edges.csv",
    "source/kernel_payload/carrier_signing_table.csv",
    "source/kernel_payload/g15_slot_edges.csv",
    "source/kernel_payload/g60_local_edges.csv",
    "artifacts/json/metric_certificate.json",
    "artifacts/json/exact_edge_set_identity_certificate.json",
    "artifacts/json/baseline_separation_certificate.json",
]

CERTS = [
    "artifacts/json/metric_certificate.json",
    "artifacts/json/exact_edge_set_identity_certificate.json",
    "artifacts/json/baseline_separation_certificate.json",
    "artifacts/json/sibling_full_graph_separation_certificate.json",
]

SCRIPTS = [
    "scripts/build_metric_certificate.py",
    "scripts/build_exact_edge_set_identity_certificate.py",
    "scripts/build_baseline_separation_certificate.py",
]

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"__load_error__": repr(e)}

def csv_head(path, n=8):
    out = {
        "exists": path.exists(),
        "header": [],
        "rows": [],
    }
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        for i, row in enumerate(r):
            if i == 0:
                out["header"] = row
            elif i <= n:
                out["rows"].append(row)
            else:
                break
    return out

def git_cmd(args):
    try:
        p = subprocess.run(
            ["git"] + args,
            cwd=str(SRC18),
            text=True,
            capture_output=True,
            timeout=10,
        )
        return {
            "ok": p.returncode == 0,
            "stdout": p.stdout.strip(),
            "stderr": p.stderr.strip(),
            "returncode": p.returncode,
        }
    except Exception as e:
        return {"ok": False, "error": repr(e)}

def extract_hash_like(obj, prefix="$", out=None):
    if out is None:
        out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = prefix + "." + str(k)
            if "hash" in str(k).lower() or "source" in str(k).lower() or "file" in str(k).lower():
                out.append({"path": p, "value": v})
            extract_hash_like(v, p, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:20]):
            extract_hash_like(v, prefix + "[" + str(i) + "]", out)
    return out

def grep_script_terms(path):
    if not path.exists():
        return []
    terms = [
        "x_sigma_edges",
        "metric_certificate",
        "DictReader",
        "csv",
        "u_vertex",
        "v_vertex",
        "slot",
        "local",
        "source_edge_file",
        "hash",
        "distance_distribution",
    ]
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = []
    for i, line in enumerate(lines, start=1):
        low = line.lower()
        if any(t.lower() in low for t in terms):
            hits.append({"line": i, "text": line[:220]})
    return hits[:80]

def main():
    report = {
        "source_project": str(SRC18),
        "git": {
            "status_short": git_cmd(["status", "--short"]),
            "head": git_cmd(["rev-parse", "--short", "HEAD"]),
            "branch": git_cmd(["branch", "--show-current"]),
            "tags_at_head": git_cmd(["tag", "--points-at", "HEAD"]),
        },
        "files": [],
        "csv_heads": {},
        "certificates": {},
        "script_hits": {},
    }

    for rel in FILES:
        p = SRC18 / rel
        item = {
            "path": rel,
            "exists": p.exists(),
            "bytes": p.stat().st_size if p.exists() else None,
            "sha256": sha256_file(p) if p.exists() else None,
        }
        report["files"].append(item)

    for rel in [
        "source/kernel_payload/x_sigma_edges.csv",
        "source/kernel_payload/carrier_signing_table.csv",
        "source/kernel_payload/g15_slot_edges.csv",
        "source/kernel_payload/g60_local_edges.csv",
    ]:
        report["csv_heads"][rel] = csv_head(SRC18 / rel)

    for rel in CERTS:
        p = SRC18 / rel
        obj = load_json(p)
        report["certificates"][rel] = {
            "top_keys": sorted(obj.keys()) if isinstance(obj, dict) else [],
            "hash_source_file_entries": extract_hash_like(obj),
        }

    for rel in SCRIPTS:
        report["script_hits"][rel] = grep_script_terms(SRC18 / rel)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Project 18 Provenance Audit")
    lines.append("")
    lines.append("This audit checks whether the current Project 18 payload matches the certificates used by the bounded theorem package.")
    lines.append("")
    lines.append("## Git state")
    lines.append("")
    for k, v in report["git"].items():
        lines.append(f"- {k}: ok={v.get('ok')} stdout=`{v.get('stdout')}` stderr=`{v.get('stderr')}`")
    lines.append("")
    lines.append("## File hashes")
    lines.append("")
    for item in report["files"]:
        lines.append(f"- `{item['path']}`")
        lines.append(f"  - exists: {item['exists']}")
        lines.append(f"  - bytes: {item['bytes']}")
        lines.append(f"  - sha256: `{item['sha256']}`")
    lines.append("")
    lines.append("## CSV heads")
    lines.append("")
    for rel, info in report["csv_heads"].items():
        lines.append(f"### {rel}")
        lines.append("")
        lines.append(f"- exists: {info['exists']}")
        lines.append(f"- header: {info['header']}")
        lines.append("- rows:")
        for row in info["rows"]:
            lines.append(f"  - {row}")
        lines.append("")
    lines.append("## Certificate hash/source entries")
    lines.append("")
    for rel, info in report["certificates"].items():
        lines.append(f"### {rel}")
        lines.append("")
        lines.append(f"- top_keys: {info['top_keys']}")
        for entry in info["hash_source_file_entries"][:80]:
            lines.append(f"- `{entry['path']}` = `{entry['value']}`")
        lines.append("")
    lines.append("## Script parse/source hits")
    lines.append("")
    for rel, hits in report["script_hits"].items():
        lines.append(f"### {rel}")
        lines.append("")
        for h in hits:
            lines.append(f"- L{h['line']}: `{h['text']}`")
        lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append("If the current edge-file hash differs from the certificate hash, Project 19 should record that it is auditing the current local payload, not claiming identity with the published Project 18 detailed metric certificate.")
    lines.append("If hashes match but metrics differ, inspect the Project 18 metric script parsing path.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("project18_head=" + str(report["git"]["head"].get("stdout")))
    print("project18_status=" + repr(report["git"]["status_short"].get("stdout")))
    print("x_sigma_hash=" + str(next(x for x in report["files"] if x["path"].endswith("x_sigma_edges.csv"))["sha256"]))

if __name__ == "__main__":
    main()
