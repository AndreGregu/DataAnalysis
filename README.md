

# Compressed Text Processing with Token Counting



This project provides tools for processing `.zst`-compressed text files using Hugging Face tokenizers and GNU Parallel.



## Contents



- `script.py` — Processes a single `.zst` file: decompresses, tokenizes, and collects text statistics.

- `execute.py` — Executes `script.py` in parallel across multiple `.zst` files and manages output directories.

- `run_execute.sh` — SLURM script to allocate resources and run `execute.py` efficiently on HPC systems.



---



## Setup Instructions



### 1. Load Cray Python (on Cray-based systems)



```bash

module load cray-python

```



### 2. Create and activate a virtual environment



```bash

python -m venv myenv

source myenv/bin/activate

```



### 3. Install Python dependencies



```bash

pip install transformers zstandard torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

```



### 4. Install GNU Parallel



#### Option A: Build from source



```bash

wget https://ftp.gnu.org/gnu/parallel/parallel-20250522.tar.bz2

tar -xvjf parallel-20250522.tar.bz2

cd parallel-20250522/

./configure && make

```



#### Option B: Install via package manager (Debian/Ubuntu)



```bash

sudo apt install parallel

```



>**Note:** Ensure the path to GNU Parallel is correct in `execute.py`:



```bash

["../parallel-20250522/src/parallel", ...]

```



---



## Model & Tokenizer



This project uses the Hugging Face model:



```bash

google/gemma-3-4b-it

```



### Authentication



You must authenticate with Hugging Face to download the model:



```bash

huggingface-cli login

```



Then paste your token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

Ensure the token has **access to gated models**.



### Model Cache



By default, models are cached to:



```bash

/scratch/project_462000953/agregussen/hf_cache

```



You can change this using the `--cache_dir` argument when running `execute.py`.



---



## File Structure



```bash

project_root/

├── script.py          # Processes one compressed text file

├── execute.py         # Runs script.py in parallel

├── run_execute.sh     # SLURM job submission script

├── README.md          # This file

```



> Data-sets are not included in the repo due to dataset size.

> Download from: [https://hplt-project.org/datasets/v2.0](https://hplt-project.org/datasets/v2.0)



---



Thanks! Here's the updated `Usage` section of the `README.md`, fully corrected and GitHub-rendered, based on your clarification:



---



## Usage



All processing (single or multiple files) is done using:



```bash

run_execute.sh

```



You must run the script with one or more `.zst` file paths as arguments.



### Process a single file



```bash

bash run_execute.sh data_files/file1.jsonl.zst

```



### Process multiple files



```bash

bash run_execute.sh data_files/file1.jsonl.zst data_files/file2.jsonl.zst data_files/file3.jsonl.zst

```



Or use a wildcard to include many files at once:



```bash

bash run_execute.sh data_files/*.jsonl.zst

```



---



## Output



Each file generates:



```bash

/<parent_folder>/<filename>_results/summary.json

```



Each `summary.json` includes:



* File size (bytes)

* Number of documents

* Number of segments

* Total characters

* Total tokens

* Execution time
