#!/bin/bash

INPUT_DIR="/scratch/project_462000953/training/catalogue/hplt/2.0/cleaned"
NUM_FILES_AVAILABLE=$(find "$INPUT_DIR" -type f -name "*.zst" | wc -l)

if [ "$NUM_FILES_AVAILABLE" -eq 0 ]; then
    echo "No .zst files found in $INPUT_DIR"
    exit 1
fi

# Constraints
MAX_CPUS=128
NODE_RAM_GB=258
PER_FILE_RAM_GB=6

# Max files based on RAM
MAX_FILES=$(( NODE_RAM_GB / PER_FILE_RAM_GB ))

# Final number of files (min of available, RAM-limited, CPU-limited)
FILES_TO_USE=$NUM_FILES_AVAILABLE
[ "$FILES_TO_USE" -gt "$MAX_FILES" ] && FILES_TO_USE=$MAX_FILES
[ "$FILES_TO_USE" -gt "$MAX_CPUS" ] && FILES_TO_USE=$MAX_CPUS

# Total memory required
MEM_GB=$(( FILES_TO_USE * PER_FILE_RAM_GB ))

echo "Submitting job for $FILES_TO_USE files"
echo "  CPUs     : $FILES_TO_USE"
echo "  Memory   : ${MEM_GB}G"

/usr/bin/sbatch --cpus-per-task=$FILES_TO_USE --mem=${MEM_GB}G run_execute.sh


