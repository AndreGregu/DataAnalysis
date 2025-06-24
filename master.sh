#!/bin/bash

#SBATCH --job-name=master_parallel

#SBATCH --account=project_462000827

#SBATCH --output=master-%j.out

#SBATCH --error=master-%j.err

#SBATCH --time=24:00:00

#SBATCH --partition=small



# ask SLURM for 4 nodes, 1 task per node, each with 50 CPUs and 250 GB RAM

#SBATCH --nodes=4

#SBATCH --ntasks=4

#SBATCH --ntasks-per-node=1

#SBATCH --cpus-per-task=50

#SBATCH --mem=250G



### usage check

if [ "$#" -ne 200 ]; then

  echo "Usage: $0 file1.zst file2.zst … file200.zst"

  exit 1

fi

### activate your Python env

source /scratch/project_462000827/agregussen/myenv/bin/activate



### split the 200‐element argument list into 4 chunks of 50

CHUNK_SIZE=50

for i in $(seq 0 3); do

  # Bash array slicing: skip i*50, take 50 elements

  OFFSET=$(( i * CHUNK_SIZE ))

  CHUNK=( "${@:OFFSET+1:CHUNK_SIZE}" )



  echo "[INFO] Launching chunk $((i+1)) on node \$SLURM_JOB_NODELIST"

  # srun --exclusive: carve out one of the 4 nodes, run one task on it

  srun --exclusive \

       --nodes=1 --ntasks=1 \

       --cpus-per-task=50 \

       ./run_execute.sh "${CHUNK[@]}" &

done



wait

echo "[INFO] All 4 chunks are now running. Master script exits."

