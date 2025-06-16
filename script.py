import os
import subprocess
from transformers import AutoTokenizer
import zstandard as zstd
import argparse

def decompress_and_count(compressed_path, tokenizer, buffer_size=50000):
    bytes = os.path.getsize(compressed_path)
    total_lines = 0
    total_segments = 0
    total_characters = 0
    total_tokens = 0
    buffer = []

    dctx = zstd.ZstdDecompressor()
    with open(compressed_path, 'rb') as compressed:
        with dctx.stream_reader(compressed) as reader:
            # Wrap the byte stream in a text reader
            text_stream = open(reader.fileno(), mode='r', encoding='utf-8', errors='replace', closefd=False)

            for i, line in enumerate(text_stream, 1):
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

            # Remaining lines
            if buffer:
                encoded = tokenizer(buffer, add_special_tokens=False)
                total_tokens += sum(len(ids) for ids in encoded['input_ids'])

    return bytes, total_lines, total_segments, total_characters, total_tokens


def main():

    parser = argparse.ArgumentParser(description="Process and tokenize a decompressed .zst file.")
    parser.add_argument("--compressed", default="nob_data.zst", help="Path to the .zst file")
    parser.add_argument("--model", default="google/gemma-3-4b-it", help="Hugging Face model name")

    args = parser.parse_args()
        
    compressed_file = args.compressed 

    model_name = "google/gemma-3-4b-it" 
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    byte_count, line_count, segment_count, character_count, token_count = decompress_and_count(compressed_file, tokenizer)


    print(f"Compressed file size: {byte_count} bytes")
    print(f"Number of lines in decompressed file: {line_count}")
    print(f"Number of segments in decompressed file: {segment_count}")
    print(f"Number of characters in decompressed file: {character_count}")
    print(f"Number of tokens in decompressed file: {token_count} ")

if __name__ == "__main__":
    main()
