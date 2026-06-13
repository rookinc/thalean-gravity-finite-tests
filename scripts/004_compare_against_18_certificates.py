from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SRC18 = ROOT.parent / "18-g900-kernel-admission"

OURS = ROOT / "artifacts/json/003_metric_deformation_summary.json"
CERT_METRIC = SRC18 / "artifacts/json/metric_certificate.json"
CERT_BASELINE = SRC18 / "artifacts/json/baseline_separation_certificate.json"

OUT_JSON = ROOT / "artifacts/json/004_certificate_comparison.json"
OUT_MD = ROOT / "artifacts/md/004_certificate_comparison.md"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm_keys(d):
    if not isinstance(d, dict):
        return d
    out = {}
    for k, v in d.items():
        try:
            kk = int(k)
        except Exception:
            kk = k
        out[kk] = v
    return out

def pick_metric(obj):
    return {
        "diameter": obj.get("diameter"),
        "radius": obj.get("radius"),
        "center_count": obj.get("center_count"),
        "eccentricity_counts": norm_keys(obj.get("eccentricity_counts")),
        "distance_distribution": norm_keys(obj.get("distance_distribution")),
    }

def compare(a, b):
    keys = sorted(set(a.keys()) | set(b.keys()), key=str)
    rows = []
    for k in keys:
        rows.append({
            "field": k,
            "ours": a.get(k),
            "certificate": b.get(k),
            "match": a.get(k) == b.get(k),
        })
    return rows

def main():
    ours = load(OURS)
    metric = load(CERT_METRIC)
    baseline = load(CERT_BASELINE)

    ours_signed = pick_metric(ours["signed_metric"])
    cert_signed = pick_metric(metric)

    ours_base = pick_metric(ours["baseline_metric"])

    # Baseline certificate uses nested fields.
    ub = baseline.get("untwisted_baseline", {})
    cert_base = {
        "diameter": ub.get("diameter"),
        "radius": ub.get("radius"),
        "center_count": ub.get("center_count"),
        "eccentricity_counts": norm_keys(ub.get("eccentricity_counts")),
        "distance_distribution": norm_keys(ub.get("distance_distribution")),
    }

    signed_rows = compare(ours_signed, cert_signed)
    base_rows = compare(ours_base, cert_base)

    report = {
        "ours_file": str(OURS),
        "metric_certificate": str(CERT_METRIC),
        "baseline_certificate": str(CERT_BASELINE),
        "signed_comparison": signed_rows,
        "baseline_comparison": base_rows,
        "signed_all_match": all(r["match"] for r in signed_rows),
        "baseline_all_match": all(r["match"] for r in base_rows),
        "interpretation": {
            "headline_signed_diameter_radius_match": (
                ours_signed["diameter"] == cert_signed["diameter"]
                and ours_signed["radius"] == cert_signed["radius"]
            ),
            "headline_baseline_diameter_radius_match": (
                ours_base["diameter"] == cert_base["diameter"]
                and ours_base["radius"] == cert_base["radius"]
            ),
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Certificate Comparison Audit")
    lines.append("")
    lines.append("This audit compares the fresh 003 metric-deformation computation against the existing Project 18 certificates.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- signed_all_match: {report['signed_all_match']}")
    lines.append(f"- baseline_all_match: {report['baseline_all_match']}")
    lines.append(f"- headline_signed_diameter_radius_match: {report['interpretation']['headline_signed_diameter_radius_match']}")
    lines.append(f"- headline_baseline_diameter_radius_match: {report['interpretation']['headline_baseline_diameter_radius_match']}")
    lines.append("")
    lines.append("## Signed graph comparison")
    lines.append("")
    lines.append("| field | match | ours | certificate |")
    lines.append("|---|---:|---|---|")
    for r in signed_rows:
        lines.append(f"| {r['field']} | {r['match']} | `{r['ours']}` | `{r['certificate']}` |")
    lines.append("")
    lines.append("## Baseline comparison")
    lines.append("")
    lines.append("| field | match | ours | certificate |")
    lines.append("|---|---:|---|---|")
    for r in base_rows:
        lines.append(f"| {r['field']} | {r['match']} | `{r['ours']}` | `{r['certificate']}` |")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("If headline diameter/radius match but detailed distributions differ, do not treat the 003 result as theorem-identical yet.")
    lines.append("The next audit should compare edge hashes, parse mode, source file versions, and certificate source paths.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)
    print("signed_all_match=" + str(report["signed_all_match"]))
    print("baseline_all_match=" + str(report["baseline_all_match"]))
    print("headline_signed_diameter_radius_match=" + str(report["interpretation"]["headline_signed_diameter_radius_match"]))
    print("headline_baseline_diameter_radius_match=" + str(report["interpretation"]["headline_baseline_diameter_radius_match"]))

if __name__ == "__main__":
    main()
