from pathlib import Path
import json
import csv
import hashlib

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
SOURCE = PROJECT_ROOT / "18-g900-kernel-admission"

OUT_JSON = ROOT / "artifacts/json/001_intake_scan.json"
OUT_MD = ROOT / "artifacts/md/001_intake_scan.md"

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json_preview(path):
    try:
        with path.open("r", encoding="utf-8") as f:
            obj = json.load(f)
        kind = type(obj).__name__
        size = None
        keys = []
        if isinstance(obj, list):
            size = len(obj)
            if obj and isinstance(obj[0], dict):
                keys = sorted(list(obj[0].keys()))[:20]
            elif obj and isinstance(obj[0], list):
                keys = ["list_item_len_" + str(len(obj[0]))]
        elif isinstance(obj, dict):
            size = len(obj)
            keys = sorted(list(obj.keys()))[:30]
        return {"ok": True, "kind": kind, "size": size, "keys": keys}
    except Exception as e:
        return {"ok": False, "error": repr(e)}

def looks_like_edge_list_json(preview):
    if not preview.get("ok"):
        return False
    if preview.get("kind") != "list":
        return False
    keys = preview.get("keys") or []
    size = preview.get("size")
    if size in (1800, 3600, 7200):
        return True
    joined = " ".join(keys).lower()
    if "source" in joined or "target" in joined or "u" in joined or "v" in joined or "edge" in joined:
        return True
    return False

def main():
    report = {
        "project": "19-thalean-gravity-finite-tests",
        "source_dir": str(SOURCE),
        "source_exists": SOURCE.exists(),
        "json_files": [],
        "csv_files": [],
        "npy_files": [],
        "edge_list_candidates": [],
    }

    if SOURCE.exists():
        for path in sorted(SOURCE.rglob("*")):
            if not path.is_file():
                continue
            rel = str(path.relative_to(PROJECT_ROOT))
            suffix = path.suffix.lower()

            if suffix == ".json":
                preview = load_json_preview(path)
                item = {
                    "path": rel,
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                    "preview": preview,
                }
                report["json_files"].append(item)
                if looks_like_edge_list_json(preview):
                    report["edge_list_candidates"].append(item)

            elif suffix == ".csv":
                item = {
                    "path": rel,
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
                report["csv_files"].append(item)

            elif suffix == ".npy":
                item = {
                    "path": rel,
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
                report["npy_files"].append(item)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Intake Scan")
    lines.append("")
    lines.append(f"source_dir: `{report['source_dir']}`")
    lines.append(f"source_exists: `{report['source_exists']}`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- json_files: {len(report['json_files'])}")
    lines.append(f"- csv_files: {len(report['csv_files'])}")
    lines.append(f"- npy_files: {len(report['npy_files'])}")
    lines.append(f"- edge_list_candidates: {len(report['edge_list_candidates'])}")
    lines.append("")
    lines.append("## Edge-list candidates")
    lines.append("")
    if report["edge_list_candidates"]:
        for item in report["edge_list_candidates"][:40]:
            p = item["preview"]
            lines.append(f"- `{item['path']}`")
            lines.append(f"  - bytes: {item['bytes']}")
            lines.append(f"  - kind: {p.get('kind')}")
            lines.append(f"  - size: {p.get('size')}")
            lines.append(f"  - keys: {p.get('keys')}")
    else:
        lines.append("- none found")
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append("Use this report to identify canonical, baseline, and sibling edge-list files for the first metric-deformation test.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("source_exists=" + str(report["source_exists"]))
    print("json_files=" + str(len(report["json_files"])))
    print("csv_files=" + str(len(report["csv_files"])))
    print("npy_files=" + str(len(report["npy_files"])))
    print("edge_list_candidates=" + str(len(report["edge_list_candidates"])))

if __name__ == "__main__":
    main()
