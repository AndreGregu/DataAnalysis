import argparse
import os
import sys

def find_files(path):
    file_list = []
    for root , dir, files in os.walk(path):
        for fn in files:
            name, _  = os.path.splitext(fn)
            full_path = os.path.join(root, name)
            file_list.append(os.path.relpath(full_path, path))
    return file_list

def process_files(path):
    file_list = []
    with open(path, 'r') as files:
        for fn in files:
            temp_name, _ = os.path.splitext(fn)
            name, _ = os.path.splitext(temp_name)
            file_list.append(name)
    return file_list

def find_missing(expected, result):
    missing = []
    for file in expected:
        if file in result:
            continue
        else:
            missing.append(file)
    return missing

def main():
    p = argparse.ArgumentParser(
    description="Compare a file list against a results directory and report missing files.")	
    p.add_argument("file_list", help="Path to text file listing expected filenames")
    p.add_argument("results_dir", nargs="?", default="../../results", help="Directory where files should be present")
    args = p.parse_args()
    expected = process_files(args.file_list)
    result = find_files(args.results_dir)
    missing = find_missing(expected, result)
    print(f"{len(expected)} expected, {len(result)} found, {len(missing)} missing")
#    output_path = os.path.join(os.getcwd(), "missing.files") 
#    with open(output_path , "w") as out: 
#        for fn in missing: 
#            out.write(f"{fn}.jsonl.zst" + "\n")
	
if __name__ == "__main__":
    main()
