---
name: sqe-generate-question
description: Generate a new SQE1 single best answer question grounded in official UK primary law (legislation.gov.uk / Find Case Law) and add it to the verified bank. Use when the candidate says "make a new question on X", "generate questions about [topic]", or "I need more practice on [subject]".
---

# Generate an SQE1 Question from Official Sources

Author exam-format questions that are accurate, current and **traceable to a real
England-&-Wales source**. Canonical rules: `claude-project/INSTRUCTIONS.md`
(section 8) and `claude-project/knowledge/03-sources-and-question-generation.md`.

## Golden rules

1. **England & Wales only.**
2. **Never invent** a citation, section number or case name. If you cannot verify
   it, state the rule without a citation — do not fabricate one.
3. Single best answer, five options A–E, one best answer, realistic scenario,
   distractors that each encode a genuine misconception.
4. Match the candidate's subject and difficulty.

## Steps

1. Pick the syllabus point (subject list in `01-sqe1-overview.md`).
2. Pull the governing rule from an official source:
   - `python scripts/fetch_source.py <url>` (legislation.gov.uk or Find Case
     Law) → clean text in `sources/`; **or** use WebFetch on the section /
     judgment page.
   - Preference order: legislation.gov.uk → caselaw.nationalarchives.gov.uk →
     bailii.org.
3. Draft the scenario around **one** decisive issue, then five options.
4. Write the explanation: state the rule, name the **authority**, and say briefly
   why each strong distractor fails.
5. Append the question to `questions/original_ew.json` using the schema, with
   `verified_for_ew: true` and an `authority` field.
6. Run `python scripts/export_knowledge.py` to refresh
   `claude-project/knowledge/02-question-bank.md`.

## Worked precedent

`ew-tort-0002` was generated from the **Occupiers' Liability Act 1957, s 2**
(fetched from legislation.gov.uk) and cites s 2(2) and s 2(3)(a). Follow the same
pattern.
