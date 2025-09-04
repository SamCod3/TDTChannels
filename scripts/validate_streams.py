#!/usr/bin/env python3
"""Validate stream URLs in TELEVISION.md and RADIO.md.

Reads the second column of the tables (streams) and performs HTTP HEAD
requests to ensure the URLs are reachable. If a HEAD request fails, a
GET request is attempted. Failing URLs are reported and the script exits
with a non-zero status code.
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple

import requests

ROOT = Path(__file__).resolve().parent.parent
FILES = [ROOT / "TELEVISION.md", ROOT / "RADIO.md"]
URL_PATTERN = re.compile(r"https?://[^\s)]+")


def extract_stream_urls(text: str) -> List[str]:
    """Extract stream URLs from the second column of markdown tables."""
    urls: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        stream_col = parts[2]
        urls.extend(URL_PATTERN.findall(stream_col))
    return urls


def check_url(url: str, timeout: int = 10) -> Tuple[str, int]:
    """Return tuple of URL and status code (0 if unreachable)."""
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout)
        if r.status_code >= 400:
            r = requests.get(url, allow_redirects=True, timeout=timeout, stream=True)
        return url, r.status_code
    except requests.RequestException:
        return url, 0


def main(limit: int | None = None) -> int:
    urls: List[str] = []
    for path in FILES:
        if path.exists():
            urls.extend(extract_stream_urls(path.read_text(encoding="utf-8")))
    if limit is not None:
        urls = urls[:limit]

    failures: List[Tuple[str, int]] = []
    for url in urls:
        _, status = check_url(url)
        if status < 200 or status >= 400:
            failures.append((url, status))
            print(f"FAIL {url} -> {status}")
        else:
            print(f"OK   {url} -> {status}")
    if failures:
        print(f"\n{len(failures)} URL(s) failed")
        return 1
    print("\nAll URLs are reachable")
    return 0


if __name__ == "__main__":
    # Optional limit via command line for quick checks
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    sys.exit(main(limit))
