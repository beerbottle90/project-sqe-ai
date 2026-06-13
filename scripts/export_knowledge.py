#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export the verified England-and-Wales question bank (JSON) to a Markdown
knowledge file for upload to a claude.ai Project.

Reads : questions/original_ew.json
Writes: claude-project/knowledge/02-question-bank.md

Run after adding or editing questions:
    python scripts/export_knowledge.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "questions" / "original_ew.json"
OUT = ROOT / "claude-project" / "knowledge" / "02-question-bank.md"

# Subject display order (FLK1 then FLK2, ethics last)
ORDER = [
    "Contract", "Tort", "Business Law and Practice", "Dispute Resolution",
    "Constitutional and Administrative Law",
    "Property Practice", "Land Law", "Trusts",
    "Wills and Administration of Estates", "Criminal Law", "Solicitors Accounts",
    "Ethics and Professional Conduct",
]


def sort_key(subject: str) -> int:
    return ORDER.index(subject) if subject in ORDER else len(ORDER)


def main() -> int:
    questions = json.loads(SRC.read_text(encoding="utf-8"))
    questions.sort(key=lambda q: (sort_key(q.get("subject", "")), q.get("id", "")))

    lines: list[str] = []
    lines.append("# SQE1 Question Bank (England & Wales, verified)\n")
    lines.append(
        "Single best answer questions for SQE1 practice. Every question is "
        "verified for the law of England and Wales and carries the governing "
        "authority. Do not present any other jurisdiction's rule as the answer.\n"
    )
    lines.append(f"**Total questions:** {len(questions)}\n")
    lines.append("---\n")

    current = None
    for q in questions:
        subj = q.get("subject", "Other")
        if subj != current:
            current = subj
            lines.append(f"\n## {subj}\n")

        flk = q.get("flk") or "pervasive"
        lines.append(f"### {q['id']}  ({flk})\n")
        if q.get("scenario"):
            lines.append(f"**Scenario.** {q['scenario']}\n")
        lines.append(f"**Question.** {q['question']}\n")
        for letter, text in q["options"].items():
            lines.append(f"- **{letter}.** {text}")
        lines.append("")
        lines.append(f"**Answer:** {q['answer']}")
        lines.append(f"**Explanation:** {q['explanation']}")
        if q.get("authority"):
            lines.append(f"**Authority:** {q['authority']}")
        if q.get("tags"):
            lines.append(f"**Tags:** {', '.join(q['tags'])}")
        lines.append("\n---\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[written] {OUT}  ({len(questions)} questions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
