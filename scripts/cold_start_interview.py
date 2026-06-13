#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQE Cold-Start Interview (standalone)
=====================================

Asks the candidate single-best-answer questions to build a profile
(data/profile.json). The quiz runner and the claude.ai Project coach use this
profile to adapt: priority subjects, difficulty, explanation depth, study plan
and exemption strategy.

NOTE: Inside the claude.ai Project the cold-start interview is run by the coach
itself (see claude-project/INSTRUCTIONS.md, section 4). This script is the local
equivalent for use with the Python pipeline.

Usage:
  python scripts/cold_start_interview.py
  python scripts/cold_start_interview.py --show     # print current profile
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "data" / "profile.json"

# Single-choice questions: (key, prompt, [(letter, label, value)])
SINGLE = [
    ("background", "What is your legal background?", [
        ("a", "Lawyer qualified in Turkey", "turkish-qualified-lawyer"),
        ("b", "Law graduate / recent graduate", "law-graduate"),
        ("c", "Non-law / starting from scratch", "non-law"),
        ("d", "Other", "other"),
    ]),
    ("years_experience", "Years of post-qualification experience? (relevant to the SQE2 exemption)", [
        ("a", "0-2 years", "0-2"),
        ("b", "2-5 years", "2-5"),
        ("c", "5+ years", "5+"),
    ]),
    ("target_sitting", "Which SQE1 sitting are you targeting?", [
        ("a", "July - already booked", "july-registered"),
        ("b", "July - not yet booked", "july-unregistered"),
        ("c", "January", "january"),
        ("d", "Undecided", "undecided"),
    ]),
    ("weekly_hours", "How much time can you study per week?", [
        ("a", "Under 5 hours", "<5"),
        ("b", "5-15 hours", "5-15"),
        ("c", "15-30 hours", "15-30"),
        ("d", "30+ hours (intensive)", "30+"),
    ]),
    ("difficulty", "Preferred question difficulty?", [
        ("a", "Easy-medium (build the basics first)", "easy-medium"),
        ("b", "Medium-hard", "medium-hard"),
        ("c", "Exam-level (true SQE1 difficulty)", "exam-level"),
    ]),
    ("exemption_strategy", "What is your strategy? (typical route for a foreign lawyer)", [
        ("a", "Sit SQE1 + apply for an SQE2 exemption", "sit-sqe1-exempt-sqe2"),
        ("b", "Sit both SQE1 and SQE2", "sit-both"),
        ("c", "Undecided", "undecided"),
    ]),
]

SUBJECTS = [
    ("a", "Contract", "Contract"),
    ("b", "Tort", "Tort"),
    ("c", "Business Law and Practice", "Business Law and Practice"),
    ("d", "Dispute Resolution", "Dispute Resolution"),
    ("e", "Property Practice", "Property Practice"),
    ("f", "Land Law", "Land Law"),
    ("g", "Trusts", "Trusts"),
    ("h", "Wills and Administration of Estates", "Wills and Administration of Estates"),
    ("i", "Criminal Law", "Criminal Law"),
    ("j", "Solicitors Accounts", "Solicitors Accounts"),
    ("k", "Constitutional and Administrative Law", "Constitutional and Administrative Law"),
    ("l", "Ethics and Professional Conduct", "Ethics and Professional Conduct"),
]


def ask_single(prompt, options):
    valid = {h for h, _, _ in options}
    while True:
        print("\n" + prompt)
        for h, label, _ in options:
            print(f"  {h}) {label}")
        ans = input("Your choice (letter): ").strip().lower()
        if ans in valid:
            return next(v for h, _, v in options if h == ans)
        print("  ! Invalid choice, try again.")


def ask_multi(prompt, options):
    valid = {h for h, _, _ in options}
    while True:
        print("\n" + prompt + "  (comma-separated, e.g. a,b,d)")
        for h, label, _ in options:
            print(f"  {h}) {label}")
        raw = input("Your choices: ").strip().lower()
        picks = [p.strip() for p in raw.split(",") if p.strip()]
        if picks and all(p in valid for p in picks):
            return [v for h, _, v in options if h in picks]
        print("  ! Invalid choice, try again.")


def run_interview() -> dict:
    print("=" * 60)
    print(" SQE Cold-Start Interview")
    print(" Let's get to know you; the tool will adapt accordingly.")
    print("=" * 60)

    profile: dict = {}
    name = input("\nName (optional, press Enter to skip): ").strip()
    if name:
        profile["name"] = name

    for key, prompt, options in SINGLE:
        profile[key] = ask_single(prompt, options)

    profile["focus_subjects"] = ask_multi(
        "Which subjects do you want to prioritise?", SUBJECTS)

    return profile


def save(profile: dict) -> None:
    PROFILE.parent.mkdir(parents=True, exist_ok=True)
    with PROFILE.open("w", encoding="utf-8") as fh:
        json.dump(profile, fh, ensure_ascii=False, indent=2)
    print(f"\n[written] {PROFILE}")
    print("\nProfile summary:")
    for k, v in profile.items():
        print(f"  - {k}: {v}")
    print("\nNow start a quiz:  python scripts/quiz.py")


def main() -> int:
    ap = argparse.ArgumentParser(description="SQE cold-start interview")
    ap.add_argument("--show", action="store_true", help="Print the current profile")
    args = ap.parse_args()

    if args.show:
        if PROFILE.exists():
            print(PROFILE.read_text(encoding="utf-8"))
        else:
            print("No profile yet. Run: python scripts/cold_start_interview.py")
        return 0

    save(run_interview())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
