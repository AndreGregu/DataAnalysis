#!/bin/bash
#SBATCH --job-name=master_parallel
#SBATCH --account=project_462000827
#SBATCH --output=master-%j.out
#SBATCH --error=master-%j.err
#SBATCH --time=24:00:00
#SBATCH --partition=small
# coordination job: 1 task, minimal resources
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <hplt.files>"
  exit 1
fi

LISTFILE=$1
BASEDIR=/scratch/project_462000953/training/catalogue/hplt/2.0/cleaned

# load relative paths
mapfile -t RELFILES < "$LISTFILE"
TOTAL=${#RELFILES[@]}
if [ "$TOTAL" -eq 0 ]; then
  echo "Error: no entries found in $LISTFILE"
  exit 1
fi

echo "[MASTER] Found $TOTAL files, splitting into chunks of 30."

# build absolute paths
ABSFILES=()
for idx in "${!RELFILES[@]}"; do
  ABSFILES+=("$BASEDIR/${RELFILES[idx]}")
done

# chunk size and number of chunks
CHUNK_SIZE=30
NUM_CHUNKS=$(( (TOTAL + CHUNK_SIZE - 1) / CHUNK_SIZE ))

# submit one batch job per chunk
for ((i=0;i<NUM_CHUNKS;i++)); do
  START=$(( i * CHUNK_SIZE ))
  CHUNK=( "${ABSFILES[@]:START:CHUNK_SIZE}" )
  echo "[MASTER] Submitting chunk #$i with ${#CHUNK[@]} files"
  sbatch ./run_execute.sh "${CHUNK[@]}"
done

echo "[MASTER] All $NUM_CHUNKS chunks submitted."
