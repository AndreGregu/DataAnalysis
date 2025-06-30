import argparse
import io
import json
from urllib.parse import urlparse
import zstandard as zstd

def decompress_and_count(compressed_path):
    domains = []
    urls = []
    duplicates = 0
    dctx = zstd.ZstdDecompressor()
    with open(compressed_path, 'rb') as compressed_file: 
        with dctx.stream_reader(compressed_file) as reader: 
            text_stream = io.TextIOWrapper(reader, encoding='utf-8', errors='replace')
            for i , line in enumerate(text_stream, 1):
                try:
                    doc = json.loads(line)
                except json.JSONDecodeError:
                    continue
                url = doc.get("u", "")
                if not url:
                    continue
                if url in urls:  
                    duplicates += 1
                else: 
                    urls.append(url)
                    domain = get_domain(url)
                    if not domain in domains:   
                        domains.append(domain)
    return domains, urls, duplicates

def get_domain(url):
    p = urlparse(url)
    domain = p.netloc.lower()
    if domain.endswith(':80'):
        domain = domain[:-3]
    if domain.endswith('443'):
        domain = domain[:-4]
    return domain

def main(): 
    parser = argparse.ArgumentParser(description="Count domains, unique URLs, and duplicates in a .zst JSONL file..")
    parser.add_argument("compressed", help="Path to .zst file")
    parser.add_argument("output", nargs="?", default="result_test.json", help="Output path for the JSON results")
    args = parser.parse_args()
    domains, urls, duplicates = decompress_and_count(args.compressed)
    domains.sort()
    urls.sort()
    result = {
        "domains": domains, 
        "urls": urls, 
        "duplicates": duplicates,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(f"Wrote {len(domains)} domains and {len(urls)} URLs with {duplicates} duplicates to {args.output}")

if __name__ == "__main__":
    main()
