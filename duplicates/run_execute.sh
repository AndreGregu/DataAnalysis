#!/bin/bash
#SBATCH --job-name=parallel_execution
#SBATCH --account=project_462000827
#SBATCH --output=slurm-%j.out
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --mem=250G
#SBATCH --partition=small

# Check if at least one .zst file is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 file1.zst [file2.zst ...]"
    exit 1
fi

if [ "$#" -gt 40 ]; then
    echo "Error: Maximum of 40 files allowed. You provided $#."
    exit 1
fi

# Calculate CPU and memory requirements (limited by hardware)
CPUS="$#"
MEM_PER_FILE=25
TOTAL_MEM=$(echo "$CPUS * $MEM_PER_FILE" | bc) 

# Run execute.py with provided .zst files
/usr/bin/time -v python execute.py "$@"
