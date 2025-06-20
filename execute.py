import argparse

import os

import subprocess

import sys



def main():

    parser = argparse.ArgumentParser(description="Use GNU Parallel to run script.py on multiple .zst files.")

    parser.add_argument("data_files", nargs="+", help="Paths to .zst data files")

    parser.add_argument("--cache_dir", default="./scratch/project_462000953/agregussen/hf_cache", help="Cache directory to store transformer model")

    args = parser.parse_args()



    # Validate input files

    for path in args.data_files:

        if not os.path.isfile(path):

            print(f"[ERROR] File not found: {path}")

            sys.exit(1)



    # Prepare commands for GNU Parallel

    commands = []

    parent_dir = "/scratch/project_462000953/agregussen/results"

    for path in args.data_files:

        abs_path = os.path.abspath(path)

        file_name = os.path.basename(abs_path).replace(".jsonl.zst", "")

        output_dir = os.path.join(parent_dir, f"{file_name}_results")

        os.makedirs(output_dir, exist_ok=True)

        output_json_path = os.path.join(output_dir, "summary.json")



        cmd = f"python script.py --compressed '{abs_path}' --output '{output_json_path}' --cache_dir '{args.cache_dir}'"

        commands.append(cmd)



    # Run commands using GNU Parallel

    print("[INFO] Starting parallel execution...")

    parallel_input = "\n".join(commands)

    subprocess.run(

    ["../tools/parallel-20250522/src/parallel", "--line-buffer", "-j", str(len(commands))],

    input=parallel_input.encode(),

    check=True

)

    print("[INFO] All processes completed.")



if __name__ == "__main__":

    main()
