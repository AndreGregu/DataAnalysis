#!/bin/bash
#SBATCH --job-name=parallel_execution
#SBATCH --account=project_462000827
#SBATCH --output=slurm-%j.out
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
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

# Inform the user
echo "Running on node: $(hostname)"
echo "Number of files submitted : $CPUS"

# Run execute.py with provided .zst files
/usr/bin/time -v python execute.py "$@"
