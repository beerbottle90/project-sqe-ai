#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate the question bank against the project schema and invariants.

Exits non-zero (and prints every problem) if anything is wrong. Used by CI and
worth running locally before committing:

    python scripts/validate_questions.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "questions" / "original_ew.json"

REQUIRED = [
    "id", "source", "jurisdiction", "subject", "flk", "scenario",
    "question", "options", "answer", "explanation", "verified_for_ew", "tags",
]
VALID_FLK = {"FLK1", "FLK2", None}


def main() -> int:
    errors: list[str] = []

    try:
        data = json.loads(BANK.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {BANK} is not valid JSON: {exc}")
        return 1

    if not isinstance(data, list) or not data:
        print("[FAIL] question bank must be a non-empty JSON array")
        return 1

    seen: set[str] = set()
    for i, q in enumerate(data):
        where = q.get("id", f"index {i}")

        for key in REQUIRED:
            if key not in q:
                errors.append(f"{where}: missing required field '{key}'")

        qid = q.get("id")
        if qid in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(qid)

        opts = q.get("options")
        if not isinstance(opts, dict) or len(opts) < 2:
            errors.append(f"{where}: 'options' must be an object with >= 2 entries")
        elif q.get("answer") not in opts:
            errors.append(f"{where}: 'answer' ({q.get('answer')!r}) is not a key in options")

        if q.get("flk") not in VALID_FLK:
            errors.append(f"{where}: 'flk' must be FLK1, FLK2 or null (got {q.get('flk')!r})")

        if not isinstance(q.get("verified_for_ew"), bool):
            errors.append(f"{where}: 'verified_for_ew' must be a boolean")

        if not isinstance(q.get("tags"), list):
            errors.append(f"{where}: 'tags' must be an array")

        # Verified E&W questions must be properly grounded.
        if q.get("verified_for_ew") is True:
            if not (q.get("authority") or "").strip():
                errors.append(f"{where}: verified question must have a non-empty 'authority'")
            if q.get("jurisdiction") != "England & Wales":
                errors.append(f"{where}: verified question must have jurisdiction 'England & Wales'")

    if errors:
        print(f"[FAIL] {len(errors)} problem(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1

    verified = sum(1 for q in data if q.get("verified_for_ew"))
    print(f"[OK] {len(data)} questions valid; {verified} verified for England & Wales.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
