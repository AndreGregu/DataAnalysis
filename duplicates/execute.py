import argparse
import os
import subprocess
import sys
import glob
import json
from collections import Counter
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Use GNU Parallel to run script.py on multiple .zst files.")
    parser.add_argument("data_files", nargs="+", help="Paths to .zst data files")
    args = parser.parse_args()
    for path in args.data_files:
        if not os.path.isfile(path):
            print(f"[ERROR] File not found: {path}")
            sys.exit(1)
    commands = []
    for i, path in enumerate(args.data_files, start=1):
        parts = path.split(os.sep)
        try:
            idx = parts.index("catalogue")
            catalogue_type = parts[idx + 1]
        except (ValueError, IndexError):
            raise ValueError(f"Path doesn’t contain a catalogue subfolder: {path!r}")
        if catalogue_type not in ("fineweb", "hplt"):
            raise ValueError(f"Unsupported catalogue type {catalogue_type!r} in path {path!r}")
        abs_path = os.path.abspath(path)
        out_dir  = Path("duplicate_results") / catalogue_type
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / f"result{i}.json"
        cmd = f"python script.py '{abs_path}' '{output_path}'"
        commands.append(cmd)
    print("[INFO] Starting parallel execution...")
    parallel_input = "\n".join(commands)
    subprocess.run(
        ["/project/project_462000953/agregussen/tools/parallel-20250522/src/parallel", "--line-buffer", "-j", str(len(commands))],
        input=parallel_input.encode(),
        check=True
    )
    print("[INFO] All processes completed.")
    domains_hplt = Counter()
    urls_hplt = Counter()
    domains_fw = Counter()
    urls_fw = Counter()
    for file in glob.glob("duplicate_results/*/*.json"):
        parts = file.split(os.sep)
        catalogue_type = parts[1] 
        with open(file, "r", encoding='utf-8') as f:
            data = json.load(f)
            for entry in data.get("urls", []):
                url = entry.get("url")
                count = entry.get("count", 1)
                if not url:
                    continue;
                if catalogue_type == "hplt":                   
                    urls_hplt[url] += count
                else:
                    urls_fw[url] += count
            for entry in data.get("domains", []):
                dom = entry.get("domain")
                count = entry.get("count", 1)
                if not dom:
                    continue
                if catalogue_type == "hplt": 
                    domains_hplt[dom] += count
                else:
                    domains_fw[dom] += count
            try:
                os.remove(file)
                print(f"Deleted {file}")
            except OSError as e:
                print(f"Error deleting {file}: {e}")

    base = Path("duplicate_results")  
    write_aggregate(urls_hplt, domains_hplt, base/"hplt"/"result.json")
    write_aggregate(urls_fw,   domains_fw,   base/"fineweb"/"result.json")
    compare_and_write()

def write_aggregate(counter_urls, counter_domains, out_filename):
        total_dupes = sum(cnt - 1 for cnt in counter_urls.values() if cnt > 1)
        sorted_urls = [{"url": u, "count": c} for u, c in counter_urls.most_common()]
        sorted_dom  = [{"domain": d, "count": c} for d, c in counter_domains.most_common()]
        result = {
            "duplicate_urls": total_dupes,
            "urls": sorted_urls,
            "domains": sorted_dom,
        }
        with open(out_filename, "w", encoding="utf-8") as o:
            json.dump(result, o, indent=2)
            o.write("\n")
        print(f"[INFO] Wrote {out_filename}: {len(sorted_urls)} URLs, "
              f"{len(sorted_dom)} domains, {total_dupes} duplicates")



def compare_and_write(base_dir="duplicate_results", out_filename="comparison.json"):
    base = Path(base_dir)
    hplt_path    = base / "hplt"    / "result.json"
    fineweb_path = base / "fineweb" / "result.json"
    hplt_data    = json.loads(hplt_path.read_text(encoding="utf-8"))
    fineweb_data = json.loads(fineweb_path.read_text(encoding="utf-8"))
    hplt_urls      = { entry["url"]    for entry in hplt_data["urls"] }
    fineweb_urls   = { entry["url"]    for entry in fineweb_data["urls"] }
    hplt_domains    = { entry["domain"] for entry in hplt_data["domains"] }
    fineweb_domains = { entry["domain"] for entry in fineweb_data["domains"] }
    shared_urls = len(hplt_urls & fineweb_urls)
    shared_domains = len(hplt_domains & fineweb_domains)
    unique_hplt_urls = len(hplt_urls - fineweb_urls)
    unique_fineweb_urls = len(fineweb_urls - hplt_urls)
    unique_hplt_domains = len(hplt_domains - fineweb_domains)
    unique_fineweb_domains = len(fineweb_domains - hplt_domains)
    result = {
        "hplt": {
            "urls_count": len(hplt_urls),
            "domains_count": len(hplt_domains),
        },
        "fineweb": {
            "urls_count": len(fineweb_urls),
            "domains_count": len(fineweb_domains),
        },
        "overlap": {
            "shared_urls_count": shared_urls,
            "shared_domains_count": shared_domains,
        },
        "unique_to_hplt": {
            "urls_count":    unique_hplt_urls,
            "domains_count": unique_hplt_domains,
        },
        "unique_to_fineweb": {
            "urls_count":    unique_fineweb_urls,
            "domains_count": unique_fineweb_domains,
        }
    }
    out_path = base / out_filename
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"[INFO] Wrote comparison summary to {out_path}")

if __name__ == "__main__":
    main()
