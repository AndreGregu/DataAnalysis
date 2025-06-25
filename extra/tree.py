import os
import argparse

def print_tree(startpath):
    print(startpath)
    for root, dirs, files in os.walk(startpath):
        # Calculate depth based on the folder hierarchy
        depth = root[len(startpath):].count(os.sep)
        indent = '│   ' * depth
        print(f"{indent}├── {os.path.basename(root)}/")
        subindent = '│   ' * (depth + 1)
        for f in files:
            print(f"{subindent}├── {f}")

def main():
    parser = argparse.ArgumentParser(description="Recursively print tree structure of a directory.")
    parser.add_argument("folder", help="Path to the folder")
    args = parser.parse_args()
    
    if not os.path.isdir(args.folder):
        print(f"Error: '{args.folder}' is not a directory.")
        return

    print_tree(os.path.abspath(args.folder))

if __name__ == "__main__":
    main()

