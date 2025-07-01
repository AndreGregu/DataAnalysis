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
    i = 0
    for path in args.data_files:
        i += 1
        abs_path = os.path.abspath(path)
        output_path = f"result{i}"
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
    result_files = sorted(glob.glob("result*"))
    combined_domains = Counter()
    combined_urls = Counter()
    for file in result_files: 
        with open(file, "r", encoding='utf-8') as f:
            data = json.load(f)
            for entry in data.get("urls", []):
                url = entry.get("url")
                count = entry.get("count", 1)
                if url: 
                    combined_urls[url] += count
            for entry in data.get("domians", []):
                dom = entry.get("domain")
                count = entry.get("count", 1)
                if dom: 
                    combined_domains[dom] += count
            try:
                os.remove(file)
                print(f"Deleted {file}")
            except OSError as e:
                print(f"Error deleting {file}: {e}")
    total_duplicates = sum(count -1 for count in combined_urls.values() if count > 1)
    sorted_urls = [
        {"url": url, "count": count}
        for url, count in combined_urls.most_common()
    ]
    sorted_domains = [
        {"domain": dom, "count": count}
        for dom, count in combined_domains.most_common()
    ]
    result = {
        "duplicate_urls": total_duplicates,
        "urls": sorted_urls, 
        "domains": sorted_domains, 
    }
    with open("result.json", "w", encoding="utf-8") as out: 
        json.dump(result, out, indent=2)
        out.write("\n")
    print(
        f"[INFO] Wrote result.json: "
        f"{len(sorted_urls)} unique URLs, "
        f"{len(sorted_domains)} unique domains, "
        f"{total_duplicates} total duplicates"
    )

if __name__ == "__main__":
    main()
