from pathlib import Path
import json
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
CORI = ROOT.parents[2]
ALET = CORI / "aletheos.ai"

OUT_JSON = ROOT / "artifacts/json/007_aletheos_source_probe.json"
OUT_MD = ROOT / "artifacts/md/007_aletheos_source_probe.md"

TARGETS = [
    "public_html/json/p900",
    "public_html/labs/constructor/kernel",
    "public_html/labs/p900_observatory/kernel",
    "public_html/labs/g900_admission/kernel",
    "notes",
    "theorem",
    "reports",
]

INTEREST = [
    "p900", "g900", "900", "external", "edge", "carrier",
    "sigma", "sign", "phase17", "phase20", "phase30",
    "combined", "checkpoint", "candidate", "orbit", "graph",
]

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def summarize_json(path):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"ok": False, "error": repr(e)}

    out = {"ok": True, "type": type(obj).__name__}

    if isinstance(obj, dict):
        out["size"] = len(obj)
        out["keys"] = sorted([str(k) for k in obj.keys()])[:80]
        out["candidate_arrays"] = []
        out["candidate_dicts"] = []
        for k, v in obj.items():
            if isinstance(v, list):
                out["candidate_arrays"].append({
                    "key": k,
                    "size": len(v),
                    "sample_types": [type(x).__name__ for x in v[:3]],
                    "sample": v[:2],
                })
            elif isinstance(v, dict):
                out["candidate_dicts"].append({
                    "key": k,
                    "size": len(v),
                    "keys": sorted([str(x) for x in v.keys()])[:40],
                })

    elif isinstance(obj, list):
        out["size"] = len(obj)
        out["sample_types"] = [type(x).__name__ for x in obj[:5]]
        out["sample"] = obj[:3]

    return out

def interesting_file(path):
    low = str(path).lower()
    if path.suffix.lower() not in [".json", ".js", ".md", ".py"]:
        return False
    return any(x in low for x in INTEREST)

def grep_hits(path):
    if path.suffix.lower() not in [".js", ".md", ".py", ".json"]:
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []
    hits = []
    rx = re.compile(r"(p900|g900|phase17|phase20|phase30|external|edge|carrier|sigma|sign|half|900)", re.I)
    for i, line in enumerate(lines, start=1):
        if rx.search(line):
            hits.append({"line": i, "text": line[:220]})
        if len(hits) >= 30:
            break
    return hits

def main():
    report = {
        "project": "19-thalean-gravity-finite-tests",
        "aletheos_root": str(ALET),
        "exists": ALET.exists(),
        "files": [],
        "json_files": [],
        "text_hits": [],
    }

    if ALET.exists():
        for target in TARGETS:
            base = ALET / target
            if not base.exists():
                continue
            for p in sorted(base.rglob("*")):
                if not p.is_file():
                    continue
                rel = str(p.relative_to(ALET))
                if not interesting_file(p):
                    continue

                item = {
                    "path": rel,
                    "bytes": p.stat().st_size,
                    "sha256": sha256_file(p),
                    "suffix": p.suffix.lower(),
                }
                report["files"].append(item)

                if p.suffix.lower() == ".json":
                    item["summary"] = summarize_json(p)
                    report["json_files"].append(item)

                hits = grep_hits(p)
                if hits:
                    report["text_hits"].append({
                        "path": rel,
                        "hits": hits,
                    })

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Aletheos Source Probe")
    lines.append("")
    lines.append(f"aletheos_root: `{report['aletheos_root']}`")
    lines.append(f"exists: `{report['exists']}`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- interesting_files: {len(report['files'])}")
    lines.append(f"- json_files: {len(report['json_files'])}")
    lines.append(f"- text_hit_files: {len(report['text_hits'])}")
    lines.append("")
    lines.append("## Interesting files")
    lines.append("")
    for item in report["files"][:100]:
        lines.append(f"- `{item['path']}` ({item['bytes']} bytes)")
    lines.append("")
    lines.append("## JSON summaries")
    lines.append("")
    for item in report["json_files"]:
        s = item.get("summary", {})
        lines.append(f"### {item['path']}")
        lines.append("")
        lines.append(f"- bytes: {item['bytes']}")
        lines.append(f"- sha256: `{item['sha256']}`")
        lines.append(f"- ok: {s.get('ok')}")
        lines.append(f"- type: {s.get('type')}")
        if "size" in s:
            lines.append(f"- size: {s.get('size')}")
        if "keys" in s:
            lines.append(f"- keys: {s.get('keys')}")
        if "candidate_arrays" in s:
            lines.append("- candidate_arrays:")
            for arr in s["candidate_arrays"][:18]:
                lines.append(f"  - key: {arr.get('key')}")
                lines.append(f"    size: {arr.get('size')}")
                lines.append(f"    sample_types: {arr.get('sample_types')}")
                lines.append(f"    sample: {repr(arr.get('sample'))[:450]}")
        if "sample" in s:
            lines.append(f"- sample: {repr(s.get('sample'))[:650]}")
        if "error" in s:
            lines.append(f"- error: {s.get('error')}")
        lines.append("")
    lines.append("## Text hits")
    lines.append("")
    for item in report["text_hits"][:40]:
        lines.append(f"### {item['path']}")
        lines.append("")
        for h in item["hits"][:12]:
            lines.append(f"- L{h['line']}: `{h['text']}`")
        lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append("Use this to identify whether Aletheos contains an earlier or alternate P900/G900 edge source.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("aletheos_exists=" + str(report["exists"]))
    print("interesting_files=" + str(len(report["files"])))
    print("json_files=" + str(len(report["json_files"])))
    print("text_hit_files=" + str(len(report["text_hits"])))

if __name__ == "__main__":
    main()
