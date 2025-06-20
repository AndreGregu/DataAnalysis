#!/bin/bash
#SBATCH --job-name=parallel_execution
#SBATCH --account=agregussen
#SBATCH --output=slurm-%j.out
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1          # Placeholder, will be updated below
#SBATCH --mem=1G                   # Placeholder, will be updated below
#SBATCH --partition=small

set -e

# Directory containing .zst files
INPUT_DIR="/scratch/project_462000953/training/catalogue/hplt/2.0/cleaned"

# Collect all .zst files
FILES=("$INPUT_DIR"/*.zst)
NUM_FILES=${#FILES[@]}

if [ "$NUM_FILES" -eq 0 ]; then
    echo "No .zst files found in $INPUT_DIR"
    exit 1
fi

# Limit CPUs to max 128
CPUS=$((NUM_FILES > 128 ? 128 : NUM_FILES))

# Limit memory to max 256 GB
MEM_GB=$((3 * NUM_FILES * 2))
MEM_GB=$((MEM_GB > 256 ? 256 : MEM_GB))

# Update SLURM directives dynamically (not directly possible inside the script, needs sbatch --cpus-per-task, --mem on command line)
echo "Requesting $CPUS CPUs and ${MEM_GB}G memory for $NUM_FILES files..."

# Activate Python virtual environment if needed
# source /scratch/project_462000953/agregussen/myenv/bin/activate

# Run execute.py with all the .zst files
/usr/bin/time -v python execute.py "${FILES[@]}"


