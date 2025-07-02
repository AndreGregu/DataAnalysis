import argparse
import io
import json
from urllib.parse import urlparse
import zstandard as zstd
from collections import Counter
import os

def decompress_and_count(compressed_path):
    domains = Counter()
    urls = Counter()
    dctx = zstd.ZstdDecompressor()
    parts = compressed_path.split(os.sep)
    try:
        idx = parts.index("catalogue")
        catalogue_type = parts[idx + 1]
    except (ValueError, IndexError):
        raise ValueError(f"Path doesn’t contain a catalogue subfolder: {compressed_path!r}")
    with open(compressed_path, 'rb') as compressed_file: 
        with dctx.stream_reader(compressed_file) as reader: 
            text_stream = io.TextIOWrapper(reader, encoding='utf-8', errors='replace')
            for line in text_stream:
                try:
                    doc = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if catalogue_type == "fineweb":
                    val = "url"
                elif catalogue_type == "hplt":
                    val = "u"
                else:
                    raise ValueError(f"Unexpected catalogue type {catalogue_type!r} in {compressed_path}")
                url = doc.get(val, "")
                if not url:	
                    continue
                urls[url] += 1
                hostname = urlparse(url).hostname
                if hostname:
                    domains[hostname.lower()] += 1
    return domains, urls

def main(): 
    parser = argparse.ArgumentParser(description="Count domains, unique URLs, and duplicates in a .zst JSONL file..")
    parser.add_argument("compressed", help="Path to .zst file")
    parser.add_argument("output", nargs="?", default="result_test.json", help="Output path for the JSON results")
    args = parser.parse_args()
    domains, urls = decompress_and_count(args.compressed)
    sorted_urls = [
        {"url": url, "count": count}
        for url, count in urls.most_common()
    ]
    sorted_domains = [
    {"domain": dom, "count": count}
    for dom, count in domains.most_common()
    ]
    duplicate_count = sum(count -1 for count in urls.values() if count > 1 )
    result = {
        "duplicate_urls": duplicate_count, 
        "urls": sorted_urls, 
        "domains": sorted_domains,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(
        f"Wrote {len(sorted_urls)} unique URLs and "
        f"{len(sorted_domains)} unique domains, "
        f"with {duplicate_count} total duplicate URLs, to {args.output}"
    )

if __name__ == "__main__":
    main()
