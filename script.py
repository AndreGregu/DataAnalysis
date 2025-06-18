import os
import argparse
import io
from transformers import AutoTokenizer
import zstandard as zstd
import json
import time

# function that does the work
def decompress_and_count(compressed_path, tokenizer, char_buffer_size=80_000_000):
    file_size = os.path.getsize(compressed_path)
    total_docs = total_segments = total_characters = total_tokens = 0
    buffer = []
    buffer_append = buffer.append
    char_buffer_len = 0

    dctx = zstd.ZstdDecompressor()
    with open(compressed_path, 'rb') as compressed_file:
        with dctx.stream_reader(compressed_file) as reader:
            text_stream = io.TextIOWrapper(reader, encoding='utf-8', errors='replace')

            for i, line in enumerate(text_stream, 1):
                try:
                    doc = json.loads(line)
                    text = doc.get("text", "")
                except json.JSONDecodeError:
                    continue  # Skip malformed lines

                buffer_append(text)
                total_docs += 1
                total_segments += text.count('\n')
                char_len = len(text)
                total_characters += char_len
                char_buffer_len += char_len

                if char_buffer_len >= char_buffer_size:
                    total_tokens += tokenize_batch(buffer, tokenizer)
                    buffer.clear()
                    char_buffer_len = 0

                    if total_docs % 10_000 == 0:
                        print(f"[INFO] Processed {total_docs:,} documents...")

            if buffer:
                total_tokens += tokenize_batch(buffer, tokenizer)

    return file_size, total_docs, total_segments, total_characters, total_tokens


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

def format_seconds(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def main():
    parser = argparse.ArgumentParser(description="Efficiently process and tokenize a compressed .zst file.")
    parser.add_argument("--compressed", required=True, help="Path to .zst file")
    parser.add_argument("--model", default="google/gemma-3-4b-it", help="Hugging Face tokenizer model")
    parser.add_argument("--output", required=True, help="Output JSON file with stats")

    # handle args
    args = parser.parse_args()

    start_time = time.time()
    
    # define tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        trust_remote_code=True,
        cache_dir="/fp/projects01/ec403/hf_models",
        use_fast=True
    )

    # gather results
    file_size, docs, segments, characters, tokens = decompress_and_count(args.compressed, tokenizer)

    elapsed_time = time.time() - start_time
    formatted_time = format_seconds(elapsed_time)

    result = {
        "file_size": file_size,
        "documents": docs,
        "segments": segments,
        "characters": characters,
        "tokens": tokens,
        "execution_time": formatted_time
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("\n=== Summary saved to:", args.output)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
