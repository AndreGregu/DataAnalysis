import argparse
import os
import sys
import json

def create_summary(path):
    new_files = []
    walker = os.walk(path)
    next(walker, None)
    for root, dirs, files in walker:
        print(f"{files}")
        file_count = size = documents = segments = characters= tokens = errors = 0
        for fn in files:
            file_count += 1
            full_path = os.path.join(root, fn)
            with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    size += data["file_size"]
                    documents += data["documents"]
                    segments += data["segments"]
                    characters += data["characters"]
                    tokens += data["tokens"]
                    errors += data["error_count"]
        extracted = {
            "number_of_files": file_count,
            "language_size": size,
            "documents": documents,
            "segments": segments,
            "characters": characters,
            "tokens": tokens,
            "errors": errors
        }
        output_path = os.path.join(root, "summary_all.json")
        #with open(output_path, 'w', encoding='utf-8') as f:
        #   json.dump(extracted, f, indent=2)
        new_files.append(output_path)
    return new_files

def main():
    p = argparse.ArgumentParser(
    description="Count total metrics per language and create a total count file..") 
    p.add_argument("dir_path", help="Path to directory")
    args = p.parse_args()

    new_files = create_summary(args.dir_path)
    for i in new_files:
        print(f"{i}")
    print(f"{len(new_files)}")
if __name__ == "__main__":
    main()
