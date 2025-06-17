import os
import argparse
import io
from transformers import AutoTokenizer
import zstandard as zstd
from concurrent.futures import ThreadPoolExecutor, as_completed

# function that does the work
def decompress_and_count(compressed_path, tokenizer, buffer_size=20000):
    file_size = os.path.getsize(compressed_path) # path to compressed file
    total_lines = total_segments = total_characters = total_tokens = 0
    buffer = [] # buffer array

    # decompress file
    dctx = zstd.ZstdDecompressor()
    with open(compressed_path, 'rb') as compressed_file:
        with dctx.stream_reader(compressed_file) as reader: # stream reader to not have to store the file
            text_stream = io.TextIOWrapper(reader, encoding='utf-8', errors='replace')

            #iterate through stream
            for i, line in enumerate(text_stream, 1):
                buffer.append(line) # add line to buffer
                total_lines += 1 # count lines
                total_segments += line.count('\n') # count segments
                total_characters += len(line) # counts chars

                # clean buffer when full
                if len(buffer) >= buffer_size:
                    total_tokens += tokenize_batch(buffer, tokenizer)
                    buffer.clear()

                    # print progress
                    if i % 20000 == 0:
                        print(f"[INFO] Processed {i:,} lines...")
            # handle rest-buffer
            if buffer:
                total_tokens += tokenize_batch(buffer, tokenizer)

    return file_size, total_lines, total_segments, total_characters, total_tokens

# efficiently tokenize buffer
def tokenize_batch(lines, tokenizer):
    encoded = tokenizer(
        lines,
        add_special_tokens=False,
        return_attention_mask=False,
        return_token_type_ids=False,
        padding=False,
        truncation=False
    )
    return sum(len(ids) for ids in encoded['input_ids'])



def main():
    parser = argparse.ArgumentParser(description="Efficiently process and tokenize a compressed .zst file.")
    parser.add_argument("--compressed", default="nob_data.zst", help="Path to .zst file")
    parser.add_argument("--model", default="google/gemma-3-4b-it", help="Hugging Face tokenizer model")

    # handle args
    args = parser.parse_args()

    # define tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        trust_remote_code=True,
        # Cache dir on fox
        # cache_dir="/fp/projects01/ec403/hf_models",
        use_fast=True
    )

    # gather results
    results = decompress_and_count(args.compressed, tokenizer)

    # print results
    print("\n=== File Summary ===")
    print(f"Compressed file size:       {results[0]:,} bytes")
    print(f"Number of lines:            {results[1]:,}")
    print(f"Number of segments:         {results[2]:,}")
    print(f"Number of characters:       {results[3]:,}")
    print(f"Number of tokens:           {results[4]:,}")

if __name__ == "__main__":
    main()
