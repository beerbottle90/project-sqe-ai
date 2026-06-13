#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch official England-and-Wales primary law text to ground question generation.

Sources:
  - legislation.gov.uk  (the official UK statute book)
  - caselaw.nationalarchives.gov.uk  (Find Case Law - official judgments)

It downloads the machine-readable text, strips the markup, and saves a clean
.txt plus a .json stub you can hand to the coach (or to Claude in the Project)
to author a grounded, correctly-cited SQE1 question.

Uses only the Python standard library (no extra dependencies).

Examples:
  # Theft Act 1968, section 1
  python scripts/fetch_source.py https://www.legislation.gov.uk/ukpga/1968/60/section/1

  # By components
  python scripts/fetch_source.py --legislation ukpga/1980/58/section/5 --slug limitation-s5

  # A judgment from Find Case Law
  python scripts/fetch_source.py https://caselaw.nationalarchives.gov.uk/uksc/2016/8
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
UA = {"User-Agent": "sqe-study-tool/1.0 (educational use)"}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_markup(raw: str) -> str:
    # remove XML/HTML tags, decode a few entities, collapse whitespace
    text = re.sub(r"<[^>]+>", " ", raw)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#163;", "GBP "), ("&nbsp;", " ")):
        text = text.replace(a, b)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def normalise_url(args) -> tuple[str, str]:
    """Return (fetch_url, slug)."""
    if args.legislation:
        path = args.legislation.strip("/")
        url = f"https://www.legislation.gov.uk/{path}"
        slug = args.slug or path.replace("/", "-")
    elif args.url:
        url = args.url
        slug = args.slug or re.sub(r"[^a-z0-9]+", "-",
                                   url.split("//")[-1].lower()).strip("-")
    else:
        raise SystemExit("Provide a URL or --legislation <path>.")

    # legislation.gov.uk: prefer the machine-readable data endpoint
    if "legislation.gov.uk" in url and not url.endswith(("/data.xml", "/data.akn")):
        url = url.rstrip("/") + "/data.xml"
    # Find Case Law: data.xml gives the LegalDocML judgment
    if "caselaw.nationalarchives.gov.uk" in url and not url.endswith("/data.xml"):
        url = url.rstrip("/") + "/data.xml"
    return url, slug


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch official E&W primary law text")
    ap.add_argument("url", nargs="?", help="Full source URL")
    ap.add_argument("--legislation", help="legislation.gov.uk path, e.g. ukpga/1968/60/section/1")
    ap.add_argument("--slug", help="Output file name (without extension)")
    args = ap.parse_args()

    fetch_url, slug = normalise_url(args)
    print(f"[fetch] {fetch_url}")
    try:
        raw = fetch(fetch_url)
    except Exception as exc:
        print(f"[error] download failed: {exc}", file=sys.stderr)
        return 1

    text = strip_markup(raw)
    SOURCES.mkdir(parents=True, exist_ok=True)
    txt_path = SOURCES / f"{slug}.txt"
    json_path = SOURCES / f"{slug}.json"
    txt_path.write_text(text, encoding="utf-8")
    json_path.write_text(json.dumps({
        "slug": slug,
        "source_url": fetch_url,
        "char_count": len(text),
        "generation_prompt": (
            "Using ONLY the England-and-Wales law in this source text, write one "
            "SQE1 single-best-answer question (realistic scenario + stem + five "
            "options A-E, one best answer). Then give the answer, a concise "
            "explanation, and cite the exact section/case. Match the schema in "
            "questions/original_ew.json and set verified_for_ew to true."
        ),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[written] {txt_path}  ({len(text)} chars)")
    print(f"[written] {json_path}")
    print("\nNext: paste the .txt into the Project chat and ask the coach to "
          "generate a grounded question, or add it to questions/original_ew.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
