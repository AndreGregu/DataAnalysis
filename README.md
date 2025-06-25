

# Compressed Text Processing with Token Counting



This project provides tools for processing `.zst`-compressed text files using Hugging Face tokenizers and GNU Parallel.



## Contents



- `script.py` — Processes a single `.zst` file: decompresses, tokenizes, and collects text statistics.

- `execute.py` — Executes `script.py` in parallel across multiple `.zst` files and manages output directories.

- `run_execute.sh` — SLURM script to allocate resources and run `execute.py` efficiently on HPC systems.

- `master.sh` — Runs multiple jobs of `run_execute.py` on several nodes. 

- `extra/model.py` — Downloads the gemma3 model to a `hf_cache`-folder two parent-directories up.

- `extra/tree.py` — Prints the tree-structure of a desired directory.

- `extra/find_missing.py` — Finds the missing files between two argument inputs, one beeing a list of files and the other a folder, and creates a new list. 

- `extra/count_metrics.py` — Calculates the total metrics per language and stores the results in the correct folder as `summary_all.json`.

---



## Setup Instructions



### 1. Load Cray Python (on Cray-based systems)



```bash

module load cray-python

```



>**Note:** Sometimes the python module is not loaded in the virtual environment. Reload the module to fix. 



### 2. Create and activate a virtual environment



```bash

python -m venv myenv

source myenv/bin/activate

```



### 3. Install Python dependencies



```bash

pip install transformers zstandard  
 
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

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

>**Note:** You need to download the model before you run the program accross several nodes. If you dont, the authentication of the model fails on the remote nodes, and the process will be terminated.



### Model Cache



By default, models are cached to:



```bash

/project/project_462000953/agregussen/hf_cache

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



>**Note:** Data-sets are not included in the repo due to dataset size. Download from: [https://hplt-project.org/datasets/v2.0](https://hplt-project.org/datasets/v2.0)



---



## Usage



Make the SLURM-script executable:



```bash

chmod +x <path>/master.sh <path>/run_execute.sh

```



Processing of multiple files on several cores accross multiple nodes is done using:



```bash

sbatch ./master.sh /project/project_462000953/oe/hplt.files

```



Processing multiple files on several cores on one node is done using:



```bash

sbatch ./run_execute.sh /project/project_462000953/oe/hplt.files

```



>**Note:** It is important that the following values are cutomized in run_execute.py:



```bash

#SBATCH --account=<your_project>

#SBATCH --time=<expected_time>

#SBATCH --cpus-per-task=<number_of_files_per_node>

#SBATCH --mem=<total_memory_per_node>

#SBATCH --partition=<type_of_node>

```



---



## Output



Each file generates:



```bash

/<parent_folder>/<file_name>.json

```



Each `<file_name>.json` includes:



* File size (bytes)

* Number of documents

* Number of segments

* Total characters

* Total tokens

* Execution time

* Error counte

* Error list
