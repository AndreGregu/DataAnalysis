

# Compressed Text Processing with Token Counting



This project provides tools for processing `.zst`-compressed text files using Hugging Face tokenizers and GNU Parallel.

The project is divided in two parts: 

* Counting the metrics of compressed files

* COunting unique metrics of groups of compressed files 




---



## Contents



* `extra/model.py` — Downloads the gemma3 model to a `hf_cache`-folder two parent-directories up.

* `extra/tree.py` — Prints the tree-structure of a desired directory.

* `extra/find_missing.py` — Finds the missing files between a list of files and the `results`-folder, and create>

* `extra/count_metrics.py` — Calculates the total metrics per language.

* `metrics/script.py` — Processes a single `.zst` file: decompresses, tokenizes, and collects text statistics.

* `metrics/execute.py` — Executes pertaining `script.py` in parallel across multiple `.zst` files and manages output directories.

* `metrics/run_execute.sh` — SLURM script to allocate resources and run pertaining `execute.py` efficiently on HPC systems.

* `metrics/master.sh` — Runs multiple jobs of pertaining `run_execute.py` on several nodes.

* `duplicates/script.py` — Processes a single `.zst` file: decompresses, gathers unique URLs and domains..

* `duplicates/execute.py` — Executes pertaining `script.py` in parallel across multiple `.zst` files and manages output directories.

* `duplicates/run_execute.sh` — SLURM script to allocate resources and run pertaining `execute.py` efficiently on HPC systems.

* `duplicates/compare.py` — Compares the different result files in a language, and creates a summary file called `result.json`, which are compared to each other to create a `comparison.json` file.



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

["/project/project_462000953/agregussen/parallel-20250522/src/parallel", ...]

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



You can change this using the `--cache_dir` argument when running `metrics/execute.py`.



---



## File Structure



```bash

project_root/

├── extra/                     # Sub-folder with additional scripts

│   └── count_metrics.py       # Summarizes the metrics of the results

│   └── find_missing.py        # Compares a file list and a folder and finds missing files

│   └── model.py               # Downloads the hf-model

│   └── tree.py                # Prints the tree-structure of a folder

├── README.md                  # This file

├── metrics/ 

│   └── script.py                  # Processes one compressed text file

│   └── execute.py                 # Runs script.py in parallel on several cores

│   └── run_execute.sh             # SLURM job submission script

│   └── master.sh                  # Master script to distribute run_execute.sh on several nodes

├── duplicates/ 

│   └── script.py                  # Processes one compressed text file

│   └── execute.py                 # Runs script.py in parallel on several cores

│   └── run_execute.sh             # SLURM job submission scripts

│   └── compare.py	 	   # Creates summaries of the different jobs

```



>**Note:** Data-sets are not included in the repo due to dataset size. Download from: [https://hplt-project.org/datasets/v2.0](https://hplt-project.org/datasets/v2.0)



---



## Usage



Make the SLURM-script executable:



```bash

chmod +x <path>/<file_name>

```



### Code for counting metrics



Counting the metrics of multiple files on several cores accross multiple nodes is done using:



```bash

sbatch metrics/master.sh /project/project_462000953/oe/hplt.files

```



If you provide less than 20 files, only one job will be started as the code submitts jobs in batches of 20.



As shown above, the code takes a list of files as one argument, and will not work on several arguments. 



>**Note:** It is important that the following values are cutomized in metrics/master.sh based on where the actual files are stored.:



```bash

BASEDIR=/project/project_462000953/scratch/training/catalogue/fineweb/2.1.0/data

```



### Code for counting duplicates



Provide all files for a language in both HPLT and Fineweb to `duplicates/run_execute.sh` (the code will sort the two) as such: 



```bash  

sbatch run_execute.sh $(find /project/project_462000953/scratch/training/catalogue/fineweb/2.1.0/data/nob_Latn/train/ -name "*zst") $(find /project/project_462000953/scratch/training/catalogue/hplt/2.0/cleaned/nob_Latn/ -name "*.zst")

```



It is also possible to only count for one dataset type (i.e HPLT) by only providing files in the HPLT folder. 



### Extra codes



`count_metrics.py` will count the metrics of all .json files and generate a `summary.json` of the groups of files (i.e. a summary for a fineweb `nob_LATN` train set, or a hplt `nob_Latn` set), and also generate a full summary for the hplt or fineweb groups called `total_summary.json`:



```bash

python count_metrics ../../results/fineweb/

```



>**Note:** In order for the code to correctly place the summaries, it is important that the path in `count_metrics.py` lead to a subgroup of the result folder (i.e. `hplt` or `fineweb`) 



`tree.py` will print the whole tree structure of a folder:



```bash

python tree.py ../../results

```



`find_missing.py` will take a list of files (i.e. .txt or .files) and a create a file list with the missing elements. Usefull if some jobs got cancelled and files were missing in the results folder: 



```bash

python find_missing expected_files.txt ../../results

```
 


`model.py` will load the HuggingFace Model into a local folder. It is required that the model is pre-downloaded before starting parallelization on several nodes, as it requires authentication to operate.



```bash 

python model.py

```



---



## Output



### Code for counting metrics



Each file generates:



```bash

/<parent_folder>/<file_name>.json

```



Where `parent_folder` is the language (i.e. the subfolder in which the file is stored)



Each `<file_name>.json` includes:



* `{file_size}` — File size (bytes)

* `{documents}` — Number of documents

* `{segments}` — Number of segments

* `{characters}` — Total characters

* `{tokens}` — Total tokens

* `{execution_time}` — Execution time

* `{error_count}` — Error count

* `{error_indexes}` — Error list



### Summarize the metrics



Using the file `count_metrics.py` with the folder containing the results as argument will generate: 



* A summary of the metrics for each language stored as `summary.json` in the pertaining folder

* A total summary of all `summary.json` files stored as `total_summary.json` in the results-folder



### Code for counting duplicates



The code wil create a folder in the current directory called `duplication_results/` which will include: 



* A folder for HPLT files called `HPLT`

* A folder for Fineweb files called `Fineweb`



In each folder, a `results.json` file will be generated which includes: 



* `{duplicate_urls}` — Number of duplicate URLs

* `{urls}` — All URLs in a list with the number of times the appear. 

* `{domains}` — All domains in a list with the number of times they appear.

* `{duplicate_signatures}` — Number of duplicate Signatures

* `{signatures}` —  All signatures in a list with the number of times they appear. 



In addition, a file called `summary.json` will be generated in the `suplicateion_results/` folder which includes: 



```bash

{

  "hplt": {

    "duplicate_urls": …,

    "duplicate_signatures": …,

    "urlss_count": …,

    "domainss_count": …,

    "signaturess_count": …

  },

  "fineweb": {

    "duplicate_urls": …,

    "duplicate_signatures": …,

    "urlss_count": …,

    "domainss_count": …,

    "signaturess_count": …

  },

  "overlap": { … },

  "unique_to_hplt": { … },

  "unique_to_fineweb": { … }

}

```
