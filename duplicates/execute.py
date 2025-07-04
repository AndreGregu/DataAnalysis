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
    print("[INFO] Running comparison step..."))
    subprocess.run(
        ["python", "compare.py"],
        check=True
    )
    print("[INFO] Comparison done.")

if __name__ == "__main__":
    main()
