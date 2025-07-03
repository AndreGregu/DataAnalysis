import argparse
import os
import subprocess
import sys

def get_catalogue_type(abs_path: str) -> str:
    parts = abs_path.split(os.sep)
    if "catalogue" not in parts:
        print(f"[ERROR] Path doesn’t contain a 'catalogue' folder: {abs_path}")
        sys.exit(1)
    idx = parts.index("catalogue")
    if idx + 1 >= len(parts):
        print(f"[ERROR] No subfolder under 'catalogue' in path: {abs_path}")
        sys.exit(1)
    cat = parts[idx + 1]
    if cat not in ("fineweb", "hplt"):
        print(f"[ERROR] Unsupported catalogue type '{cat}' in path: {abs_path}")
        sys.exit(1)
    return cat

def main():
    parser = argparse.ArgumentParser(description="Use GNU Parallel to run script.py on multiple .zst files.")
    parser.add_argument("data_files", nargs="+", help="Paths to .zst data files")
    parser.add_argument("--cache_dir", default="/project/project_462000953/agregussen/hf_cache", help="Cache directory to store transformer model")
    args = parser.parse_args()
    for path in args.data_files:
        if not os.path.isfile(path):
            print(f"[ERROR] File not found: {path}")
            sys.exit(1)
    commands = []
    result_root = "/project/project_462000953/agregussen/results"
    for path in args.data_files:
        abs_path = os.path.abspath(path)
        catalogue_type = get_catalogue_type(abs_path)
        file_name = os.path.basename(abs_path).replace(".jsonl.zst", "")
        parent = os.path.basename(os.path.dirname(abs_path))
        if parent in ("train", "test"):
            lang = os.path.basename(os.path.dirname(os.path.dirname(abs_path)))
            output_dir = os.path.join(result_root, catalogue_type, lang, parent)
        else:
            output_dir = os.path.join(result_root, catalogue_type, parent)
        os.makedirs(output_dir, exist_ok=True)
        output_json_path = os.path.join(output_dir, f"{file_name}.json")
        cmd = f"python script.py --compressed '{abs_path}' --output '{output_json_path}' --cache_dir '{args.cache_dir}'"
        commands.append(cmd)
    print("[INFO] Starting parallel execution...")
    parallel_input = "\n".join(commands)
    subprocess.run(
        ["/project/project_462000953/agregussen/tools/parallel-20250522/src/parallel", "--line-buffer", "-j", str(len(commands))],
        input=parallel_input.encode(),
        check=True
    )
    print("[INFO] All processes completed.")

if __name__ == "__main__":
    main()

