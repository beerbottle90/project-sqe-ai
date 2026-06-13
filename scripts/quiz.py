#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQE quiz runner (local console)
===============================

Reads the question pool and (optionally) the candidate profile, then runs an
adaptive single-best-answer quiz in the terminal.

By default it uses ONLY questions verified for England and Wales
(verified_for_ew == true). Use --reasoning to also include imported non-E&W
questions for pure reasoning practice (their answers are NOT verified against
English law - treat with care).

Usage:
  python scripts/quiz.py                 # E&W only, 10 questions
  python scripts/quiz.py -n 20           # 20 questions
  python scripts/quiz.py --subject Tort  # one subject
  python scripts/quiz.py --reasoning     # include imported non-E&W questions
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POOL = ROOT / "data" / "question_pool.json"
PROFILE = ROOT / "data" / "profile.json"


def load_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def main() -> int:
    ap = argparse.ArgumentParser(description="SQE quiz runner")
    ap.add_argument("-n", "--num", type=int, default=10, help="Number of questions")
    ap.add_argument("--subject", help="Restrict to one subject")
    ap.add_argument("--reasoning", action="store_true",
                    help="Include imported non-E&W questions (unverified)")
    args = ap.parse_args()

    pool = load_json(POOL, [])
    if not pool:
        print(f"No questions found. Run: python scripts/build_question_pool.py")
        return 1
    profile = load_json(PROFILE, {})

    # Safety: England & Wales only unless --reasoning
    if not args.reasoning:
        pool = [q for q in pool if q.get("verified_for_ew")]
    if args.subject:
        pool = [q for q in pool if q.get("subject") == args.subject]

    # Adapt: prioritise the profile's focus subjects
    focus = set(profile.get("focus_subjects", []))
    if focus:
        pool.sort(key=lambda q: 0 if q.get("subject") in focus else 1)
        head = [q for q in pool if q.get("subject") in focus]
        tail = [q for q in pool if q.get("subject") not in focus]
        random.shuffle(head)
        random.shuffle(tail)
        pool = head + tail
    else:
        random.shuffle(pool)

    questions = pool[: args.num]
    if not questions:
        print("No questions match those filters.")
        return 1

    score = 0
    wrong_subjects: dict[str, int] = {}
    print(f"\nSQE quiz - {len(questions)} questions "
          f"({'E&W only' if not args.reasoning else 'incl. non-E&W'}).\n")

    for i, q in enumerate(questions, 1):
        print("=" * 70)
        print(f"Q{i}/{len(questions)}  [{q.get('subject')}"
              f"{' / ' + q['flk'] if q.get('flk') else ''}]"
              f"{'' if q.get('verified_for_ew') else '  (NON-E&W - unverified)'}")
        if q.get("scenario"):
            print("\n" + q["scenario"])
        print("\n" + q["question"] + "\n")
        for letter, text in q["options"].items():
            print(f"  {letter}. {text}")
        ans = input("\nYour answer: ").strip().upper()
        correct = (q.get("answer") or "").strip().upper()
        if ans == correct:
            score += 1
            print("  -> Correct.")
        else:
            print(f"  -> Incorrect. Best answer: {correct}")
            subj = q.get("subject", "Other")
            wrong_subjects[subj] = wrong_subjects.get(subj, 0) + 1
        if q.get("explanation"):
            print(f"  Explanation: {q['explanation']}")
        if q.get("authority"):
            print(f"  Authority: {q['authority']}")
        print()

    pct = round(100 * score / len(questions))
    print("=" * 70)
    print(f"Score: {score}/{len(questions)}  ({pct}%)")
    if wrong_subjects:
        worst = ", ".join(f"{s} ({n})" for s, n in
                          sorted(wrong_subjects.items(), key=lambda kv: -kv[1]))
        print(f"Review these subjects: {worst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
