import os
import subprocess
from transformers import AutoTokenizer
import zstandard as zstd
import argparse

def decompress_file(compressed_path, output_path):
    with open(compressed_path, 'rb') as compressed_file, open(output_path, 'wb') as decompressed_file:
        decompress = zstd.ZstdDecompressor()
        decompress.copy_stream(compressed_file, decompressed_file)



def count_bytes(file_path):
    return os.path.getsize(file_path)

def count(file_path, tokenizer, buffer_size=50000):
    total_lines = 0
    total_segments = 0
    total_characters = 0
    total_tokens = 0
    buffer = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, 1):
            buffer.append(line)
            total_lines += 1
            total_segments += line.count('\n')
            total_characters += len(line)

            if len(buffer) >= buffer_size:
                encoded = tokenizer(buffer, add_special_tokens=False)
                total_tokens += sum(len(ids) for ids in encoded['input_ids'])
                buffer = []

                if i % 10000 == 0:
                    print(f"Processed {i} lines...")

        
        if buffer:
            encoded = tokenizer(buffer, add_special_tokens=False)
            total_tokens += sum(len(ids) for ids in encoded['input_ids'])

    return total_lines, total_segments, total_characters, total_tokens

"""
def count(file_path, tokenizer):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        total_lines = sum(1 for _ in file)
        total_segments = content.count('\n')
        total_characters = len(content)
        total_tokens = len(tokenizer.encode(line, add_special_tokens=False))
        return (total_lines, total_segments, total_characters, total_tokens)
"""

def main():

    parser = argparse.ArgumentParser(description="Process and tokenize a decompressed .zst file.")
    parser.add_argument("--compressed", default="nob_data.zst", help="Path to the .zst file")
    parser.add_argument("--decompressed", default="nob_data", help="Path to output decompressed file")
    parser.add_argument("--model", default="google/gemma-3-4b-it", help="Hugging Face model name")

    args = parser.parse_args()

    decompressed_file = args.decompressed          
    compressed_file = args.compressed 

    model_name = "google/gemma-3-4b-it" 
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    compressed_file = args.compressed
    if not os.path.exists(decompressed_file):
        decompress_file(compressed_file, decompressed_file)

    byte_count = count_bytes(compressed_file)

    line_count, segment_count, character_count, token_count = count(decompressed_file, tokenizer)

    print(f"Compressed file size: {byte_count} bytes")
    print(f"Number of lines in decompressed file: {line_count}")
    print(f"Number of segments in decompressed file: {segment_count}")
    print(f"Number of characters in decompressed file: {character_count}")
    print(f"Number of tokens in decompressed file: {token_count} ")

if __name__ == "__main__":
    main()
