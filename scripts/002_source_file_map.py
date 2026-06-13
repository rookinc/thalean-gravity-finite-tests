from pathlib import Path
import json
import csv

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT.parent / "18-g900-kernel-admission"
OUT_MD = ROOT / "artifacts/md/002_source_file_map.md"
OUT_JSON = ROOT / "artifacts/json/002_source_file_map.json"

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}

INTEREST_TERMS = [
    "kernel", "payload", "edge", "graph", "canonical", "baseline",
    "untwisted", "sibling", "sign", "sigma", "carrier", "certificate",
    "diameter", "radius", "distance", "metric", "qed"
]

def should_skip(path):
    return any(part in SKIP_DIRS for part in path.parts)

def is_interesting(path):
    low = str(path).lower()
    return any(t in low for t in INTEREST_TERMS)

def json_summary(path):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"ok": False, "error": repr(e)}

    if isinstance(obj, dict):
        keys = sorted([str(k) for k in obj.keys()])
        return {
            "ok": True,
            "type": "dict",
            "size": len(obj),
            "keys": keys[:100],
        }

    if isinstance(obj, list):
        sample = obj[:5]
        return {
            "ok": True,
            "type": "list",
            "size": len(obj),
            "sample_types": [type(x).__name__ for x in sample],
            "sample": sample,
        }

    return {
        "ok": True,
        "type": type(obj).__name__,
        "value": repr(obj)[:300],
    }

def csv_summary(path):
    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            rows = []
            for i, row in enumerate(reader):
                rows.append(row)
                if i >= 5:
                    break
        row_count = sum(1 for _ in path.open("r", encoding="utf-8", newline=""))
        return {
            "ok": True,
            "rows": row_count,
            "header": rows[0] if rows else [],
            "sample": rows[1:],
        }
    except Exception as e:
        return {"ok": False, "error": repr(e)}

def text_head(path, max_chars=500):
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except Exception as e:
        return "ERROR: " + repr(e)

def main():
    report = {
        "source": str(SRC),
        "source_exists": SRC.exists(),
        "files": [],
        "interesting_files": [],
        "json_files": [],
        "csv_files": [],
        "md_files": [],
        "py_files": [],
    }

    if SRC.exists():
        for p in sorted(SRC.rglob("*")):
            if not p.is_file():
                continue
            if should_skip(p.relative_to(SRC)):
                continue

            rel = str(p.relative_to(SRC))
            item = {
                "path": rel,
                "bytes": p.stat().st_size,
                "suffix": p.suffix.lower(),
                "interesting": is_interesting(p),
            }
            report["files"].append(item)

            if item["interesting"]:
                report["interesting_files"].append(item)

            if p.suffix.lower() == ".json":
                item["summary"] = json_summary(p)
                report["json_files"].append(item)
            elif p.suffix.lower() == ".csv":
                item["summary"] = csv_summary(p)
                report["csv_files"].append(item)
            elif p.suffix.lower() == ".md":
                item["head"] = text_head(p)
                report["md_files"].append(item)
            elif p.suffix.lower() == ".py":
                item["head"] = text_head(p)
                report["py_files"].append(item)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Source File Map")
    lines.append("")
    lines.append(f"source: `{report['source']}`")
    lines.append(f"source_exists: `{report['source_exists']}`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- files_excluding_git: {len(report['files'])}")
    lines.append(f"- interesting_files: {len(report['interesting_files'])}")
    lines.append(f"- json_files: {len(report['json_files'])}")
    lines.append(f"- csv_files: {len(report['csv_files'])}")
    lines.append(f"- md_files: {len(report['md_files'])}")
    lines.append(f"- py_files: {len(report['py_files'])}")
    lines.append("")
    lines.append("## Interesting files")
    lines.append("")
    for item in report["interesting_files"][:120]:
        lines.append(f"- `{item['path']}` ({item['bytes']} bytes)")
    if not report["interesting_files"]:
        lines.append("- none")
    lines.append("")
    lines.append("## JSON summaries")
    lines.append("")
    for item in report["json_files"]:
        s = item.get("summary", {})
        lines.append(f"### {item['path']}")
        lines.append("")
        lines.append(f"- bytes: {item['bytes']}")
        lines.append(f"- ok: {s.get('ok')}")
        lines.append(f"- type: {s.get('type')}")
        if "size" in s:
            lines.append(f"- size: {s.get('size')}")
        if "keys" in s:
            lines.append(f"- keys: {s.get('keys')}")
        if "sample_types" in s:
            lines.append(f"- sample_types: {s.get('sample_types')}")
        if "sample" in s:
            lines.append(f"- sample: {repr(s.get('sample'))[:600]}")
        if "error" in s:
            lines.append(f"- error: {s.get('error')}")
        lines.append("")
    lines.append("## CSV summaries")
    lines.append("")
    for item in report["csv_files"]:
        s = item.get("summary", {})
        lines.append(f"### {item['path']}")
        lines.append("")
        lines.append(f"- bytes: {item['bytes']}")
        lines.append(f"- ok: {s.get('ok')}")
        lines.append(f"- rows: {s.get('rows')}")
        lines.append(f"- header: {s.get('header')}")
        lines.append(f"- sample: {repr(s.get('sample'))[:600]}")
        if "error" in s:
            lines.append(f"- error: {s.get('error')}")
        lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append("Use the JSON and CSV summaries to locate kernel payloads, canonical graph certificates, baseline certificates, and sibling certificates.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("source_exists=" + str(report["source_exists"]))
    print("files_excluding_git=" + str(len(report["files"])))
    print("interesting_files=" + str(len(report["interesting_files"])))
    print("json_files=" + str(len(report["json_files"])))
    print("csv_files=" + str(len(report["csv_files"])))
    print("md_files=" + str(len(report["md_files"])))
    print("py_files=" + str(len(report["py_files"])))

if __name__ == "__main__":
    main()
