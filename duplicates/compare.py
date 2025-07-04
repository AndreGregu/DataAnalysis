import os
import json
import glob
from collections import Counter
from pathlib import Path

CATALOGS = ("hplt", "fineweb")
SECTIONS = {
    "urls": ("url", Counter),
    "domains": ("domain", Counter),
    "signatures": ("signature", Counter),
}

def main(base_dir="duplicate_results", comparison_file="comparison.json"):
    base = Path(base_dir)
    counters = {
        cat: { sec: cls() for sec, (_, cls) in SECTIONS.items() }
        for cat in CATALOGS
    }
    for file in base.glob("*/*.json"):
        cat = file.parent.name
        if cat not in counters:
            continue
        data = json.loads(file.read_text(encoding="utf-8"))
        for sec, (field, counter_cls) in SECTIONS.items():
            cnt = counters[cat][sec]
            for entry in data.get(sec, []):
                key = entry.get(field)
                if key:
                    cnt[key] += entry.get("count", 1)
        try:
            file.unlink()
            print(f"Deleted {file}")
        except OSError as e:
            print(f"Error deleting {file}: {e}")
    summary = {}
    for cat in CATALOGS:
        url_cnt = counters[cat]["urls"]
        if not url_cnt:
            continue
        dom_cnt = counters[cat]["domains"]
        sig_cnt = counters[cat]["signatures"]
        out_path = base / cat / "result.json"
        write_aggregate(url_cnt, dom_cnt, sig_cnt, out_path)
        summary[cat] = {
            sec: set(counters[cat][sec].keys())
            for sec in SECTIONS
        }
    if len(summary) == 2:
        compare_and_write(summary, base / comparison_file)

def write_aggregate(urls: Counter, domains: Counter, sigs: Counter, out_path: Path):
    total_url_dupes = sum(c - 1 for c in urls.values() if c > 1)
    total_sig_dupes = sum(c -1 for c in sigs.values() if c > 1)
    result = {
        "duplicate_urls": total_url_dupes,
        "urls": [{"url": u, "count": c} for u, c in urls.most_common()],
        "domains": [{"domain": d, "count": c} for d, c in domains.most_common()],
        "duplicate_signatures": total_sig_dupes,
        "signatures": [{"signature": s, "count": c} for s, c in sigs.most_common()],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"[INFO] Wrote {out_path}: {total_url_dupes} url duplicates, "
          f"{len(result['urls'])} URLs, {len(result['domains'])} domains, " 
          f"{total_url_dupes} signature duplicates, "
          f"{len(result['signatures'])} signatures")

def compare_and_write(summary: dict, out_path: Path):
    base = out_path.parent
    hplt_raw = json.loads((base/"hplt"/"result.json").read_text(encoding="utf-8"))
    fw_raw = json.loads((base/"fineweb"/"result.json").read_text(encoding="utf-8"))
    dupe_urls_hplt = hplt_raw.get("duplicate_urls", 0)
    dupe_sigs_hplt = hplt_raw.get("duplicate_signatures", 0)
    dupe_urls_fw = fw_raw.get("duplicate_urls", 0)
    dupe_sigs_fw = fw_raw.get("duplicate_signatures", 0)
    hplt, fw = summary["hplt"], summary["fineweb"]
    dims = SECTIONS.keys()
    result = {
        "hplt": {
            "duplicate_urls": dupe_urls_hplt,
            "duplicate_signatures": dupe_sigs_hplt,
            **{ f"{dim}s_count": len(hplt[dim]) for dim in dims }
        },
        "fineweb": {
            "duplicate_urls": dupe_urls_fw,
            "duplicate_signatures": dupe_sigs_fw,
            **{ f"{dim}s_count": len(fw[dim]) for dim in dims }
        }
    }
    overlap = {}
    uniques = {"hplt": {}, "fineweb": {}}
    for dim in dims:
        set_hplt, set_fw = hplt[dim], fw[dim]
        overlap[f"shared_{dim}s_count"] = len(set_hplt & set_fw)
        uniques["hplt"][f"{dim}s_count"] = len(set_hplt - set_fw)
        uniques["fineweb"][f"{dim}s_count"] = len(set_fw - set_hplt)
    result["overlap"] = overlap
    result["unique_to_hplt"] = uniques["hplt"]
    result["unique_to_fineweb"] = uniques["fineweb"]
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"[INFO] Wrote comparison summary to {out_path}")

if __name__ == "__main__":
    main()
