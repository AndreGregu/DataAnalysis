import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Use GNU Parallel to run script.py on multiple .zst files.")
    parser.add_argument("data_files", nargs="+", help="Paths to .zst data files")
    args = parser.parse_args()

    # Validate input files
    for path in args.data_files:
        if not os.path.isfile(path):
            print(f"[ERROR] File not found: {path}")
            sys.exit(1)

    # Prepare commands for GNU Parallel
    commands = []
    for path in args.data_files:
        abs_path = os.path.abspath(path)
        file_name = os.path.splitext(os.path.basename(abs_path))[0]
        parent_dir = "./nob_data"
        #parent_dir = os.path.dirname(abs_path)
        output_dir = os.path.join(parent_dir, f"{file_name}_results")
        os.makedirs(output_dir, exist_ok=True)
        output_json_path = os.path.join(output_dir, "summary.json")

        cmd = f"python script.py --compressed '{abs_path}' --output '{output_json_path}'"
        commands.append(cmd)

    # Run commands using GNU Parallel
    print("[INFO] Starting parallel execution...")
    parallel_input = "\n".join(commands)
    subprocess.run(
    ["../parallel-20250522/src/parallel", "--eta", "--progress", "--color", "--line-buffer", "-j", str(len(commands))],
    input=parallel_input.encode(),
    check=True
)
    print("[INFO] All processes completed.")

if __name__ == "__main__":
    main()
