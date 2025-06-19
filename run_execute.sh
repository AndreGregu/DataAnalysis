#!/bin/bash
#SBATCH --job-name=parallel_execution
#SBATCH --account=ec403
#SBATCH --output=slurm-%j.out
#SBATCH --time=01:30:00             # Still safe based on past runs
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2           # Because you're running -j 2
#SBATCH --mem=6G                    # 2 transformer tasks × ~2.5–3 GB = 6 GB total

# Exit on any error
set -e

# Check if at least one .zst file is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 file1.zst [file2.zst ...]"
    exit 1
fi

# Activate Python virtual environment
# source /scratch/project_462000953/agregussen/myenv/bin/activate

# Run execute.py with provided .zst files
/usr/bin/time -v python execute.py "$@"
