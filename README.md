# Compressed Text Processing with Token Counting

This project includes two Python scripts for processing `.zst`-compressed text files:  
- `script.py`: Processes a single `.zst` file by decompressing, tokenizing, and collecting text statistics.  
- `execute.py`: Uses GNU Parallel to run `script.py` on multiple `.zst` files concurrently.  

---

## Requirements  

### Python Packages  
Install required Python libraries:  

```bash  
pip install transformers zstandard  

```
### GNU Parallel
```bash
# Download GNU Parallel (example version)  
wget https://ftp.gnu.org/gnu/parallel/parallel-20250522.tar.bz2  

# Extract the archive  
tar -xvjf parallel-20250522.tar.bz2  

# On Ubuntu/Debian  
sudo apt install parallel  

# OR build from source (used here)  
cd ../parallel-20250522/  
./configure && make  
```  

**Make sure the path to parallel is correct in the script `execute.py`**  
```bash  
["../parallel-20250522/src/parallel", ...]  
```  

### Pretrained Tokenizer
The script uses the Hugging Face tokenizer:  
```bash  
google/gemma-3-4b-it
```  

By default the models will be cached in:  
```bash  
/fp/projects01/ec403/hf_models  
```  
**Make sure this directory exists or pass another directory as `--cache_dir` argument when running `execute.py`**  

## File Structure  
```bash  
project_root/  
│  
├── script.py          # Handles decompression and token counting for one file  
├── execute.py         # Batch execution with GNU Parallel  
├── data_files/        # Your input .zst files  
├── nob_data/          # Output folder (created automatically)  
├── README.md          # This file  
```
The `data_files` folder is non existent as the datasets are to large to upload to git. Download them from `https://hplt-project.org/datasets/v2.0`.  

## Running The Scripts  
Process a single file:  
```bash  
python script.py --compressed data_files/file1.jsonl.zst --output nob_data/file1_results/summary.json  
```  

Process multiple files in parallel:  
```bash
python execute.py data_files/*.jsonl.zst 
```

## Output  
Each processed file will generate: 

nob_data/<file_results>/summary.json  

A `summary.json` file will contain following metrics regarding the dataset:  
- File size  
- Documents  
- Segments  
- Characters  
- Tokens  
- Execution time  


