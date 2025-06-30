import argparse
import os
import subprocess
import sys
from pathlib import Path
import glob
import json

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
    result_files = glob.glob("result*")
    combined_domains = []
    combined_urls = []
    combined_duplicates = 0
    for file in result_files: 
        with open(file, "r", encoding='utf-8') as f:
            data = json.load(f)
            domains = data.get("domains", [])
            urls = data.get("urls", [])
            combined_duplicates = data.get("duplicates")
            for u in urls: 
                if not u in combined_urls: 
                    combined_urls.append(u)
                else: 
                    combined_duplicates += 1
            for d in domains:
                if not d in combined_domains: 
                    combined_domains.append(d)
            try:
                os.remove(file)
                print(f"Deleted {file}")
            except OSError as e:
                print(f"Error deleting {file}: {e}")
    result = {
        "domains": combined_domains, 
        "urls": combined_urls, 
        "duplicates": combined_duplicates,
    }
    with open("result.json", "w", encoding="utf-8") as out: 
        json.dump(result, out, indent=2)
        out.write("\n")
   
if __name__ == "__main__":
    main()
