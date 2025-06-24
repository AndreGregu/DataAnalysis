#!/bin/bash

#SBATCH --job-name=master_parallel

#SBATCH --account=project_462000827

#SBATCH --output=master-%j.out

#SBATCH --error=master-%j.err

#SBATCH --time=24:00:00

#SBATCH --partition=small



# request 4 nodes for coordination only

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



mapfile -t RELFILES <"$LISTFILE"

if [ "${#RELFILES[@]}" -lt 200 ]; then

  echo "Error: only ${#RELFILES[@]} entries (<200)"

  exit 1

fi



# build absolute file list of first 200

for i in {0..199}; do

  ABSFILES[i]="$BASEDIR/${RELFILES[i]}"

done



# now loop 4 chunks and sbatch each
for i in $(seq 0 3); do

  CHUNK=( "${ABSFILES[@]:$((i*50)):50}" )

  echo "[MASTER] Submitting chunk #$i with ${#CHUNK[@]} files"

  sbatch ./run_execute.sh "${CHUNK[@]}"

done


echo "[MASTER] All 4 chunks submitted."

