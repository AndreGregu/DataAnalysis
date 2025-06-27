import argparse
import os
import sys
import json

def create_summary(path):
    new_files = []
    walker = os.walk(path)
    next(walker, None)
    total_languages= total_file_count = total_size = total_documents = total_segments = total_characters = total_tokens = total_errors = 0 
    for root, dirs, files in walker:
        file_count = size = documents = segments = characters = tokens = errors = 0
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
        individual_summary = {
            "number_of_files": file_count,
            "language_size": size,
            "documents": documents,
            "segments": segments,
            "characters": characters,
            "tokens": tokens,
            "errors": errors
        }
        total_languages += 1
        total_file_count += file_count
        total_size += size
        total_documents += documents
        total_segments += segments
        total_characters += characters
        total_tokens += tokens
        total_errors += errors
        output_path = os.path.join(root, "summary.json")
        with open(output_path, 'w', encoding='utf-8') as f:
           json.dump(individual_summary, f, indent=2)
        new_files.append(output_path)
    total_summary = {
        "number_of_languages": total_languages,
        "number_of_files": total_file_count,
        "language_size": total_size,
        "documents": total_documents,
        "segments": total_segments,
        "characters": total_characters,
        "tokens": total_tokens,
        "errors": total_errors
    }
    output_path = os.path.join(path, "total_summary.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(total_summary, f, indent=2)
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

if __name__ == "__main__":
    main()
