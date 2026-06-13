---
name: sqe-quiz
description: Run an SQE1 quiz session — single best answer questions from the verified England & Wales bank, marked with explanations and the governing authority. Use when the candidate says "quiz me", "test me", "practice questions", or "let's do some MCQs".
---

# SQE1 Quiz Session

Run a single-best-answer quiz in **formal UK English**. Canonical behaviour:
`claude-project/INSTRUCTIONS.md`, sections 6–7.

## Source of questions

- Use `questions/original_ew.json` (the verified bank) and/or
  `claude-project/knowledge/02-question-bank.md`.
- If `data/question_pool.json` exists, use **only** items with
  `verified_for_ew: true`. **Never** quiz from non-E&W imported items unless the
  candidate explicitly asks for "reasoning practice", and then label them clearly
  as non-England-&-Wales.
- You may also author fresh questions on the fly — if you do, ground them in an
  official source and cite it (see `/sqe-generate-question`).

## How to run

1. Read `data/profile.json` if present; weight the candidate's **priority
   subjects** and honour their **difficulty** setting.
2. Ask **1–5** questions per round. Each: a realistic scenario (3–6 sentences), a
   precise stem, then five options **A–E**. Exactly one best answer.
3. **Do not reveal the answer** until the candidate responds.
4. After they answer: give the correct **letter**, a concise **explanation**
   grounded in the rule, the **authority** (statute section / case + neutral
   citation), and a brief note on why each strong distractor is wrong.
5. Keep a running tally and note **weak subjects**; revisit them later in the
   session and suggest what to review.

## Format

```
[Subject] — [FLK1 / FLK2]
Scenario: ...
Question: ...
A. …  B. …  C. …  D. …  E. …
```
After the answer:
```
Answer: X
Explanation: …
Authority: …
```
