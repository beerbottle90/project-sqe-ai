# CLAUDE.md — Project SQE AI

Guidance for any Claude instance working in this repository.

## What this project is

Project SQE AI is an open-source study companion for **SQE1** (Solicitors
Qualifying Examination, Part 1, **England & Wales**). It ships as:

1. A **claude.ai Projects** package — `claude-project/INSTRUCTIONS.md` (custom
   instructions) plus `claude-project/knowledge/` (upload to the Project).
2. A **Claude Code** layer — skills in `.claude/skills/`, an agent in
   `.claude/agents/`, and a Python pipeline in `scripts/`.

The substantive coaching behaviour is specified in
`claude-project/INSTRUCTIONS.md` — read it first; it is the canonical behaviour
spec and the skills defer to it.

## Golden rules (non-negotiable)

1. **England & Wales law only.** Never present a US / EU / Swiss / other rule as
   the answer. The imported datasets in `data/question_pool.json` tagged
   `verified_for_ew: false` are non-E&W *reasoning practice* and must never be
   treated as authoritative or copied into the knowledge base.
2. **Never invent a citation.** Cite an Act + section or a case + neutral
   citation only when confident. If unsure, state the rule without a citation.
3. **Formal UK English** everywhere (British spelling, UK legal terms:
   *claimant*, *solicitor*, *judgment*).
4. **Single best answer format**: realistic scenario, precise stem, five options
   A–E, exactly one best answer; reveal the answer only after the candidate
   responds.

## The question bank

- Source of truth: `questions/original_ew.json` (schema below).
- After editing it, regenerate the Project knowledge doc:
  `python scripts/export_knowledge.py`.

```json
{
  "id": "ew-<subject>-NNNN",
  "source": "original",
  "jurisdiction": "England & Wales",
  "subject": "Contract | Tort | Criminal Law | ...",
  "flk": "FLK1 | FLK2 | null",
  "scenario": "...",
  "question": "...",
  "options": { "A": "...", "B": "...", "C": "...", "D": "...", "E": "..." },
  "answer": "A",
  "explanation": "rule + why the strong distractors fail",
  "verified_for_ew": true,
  "tags": ["..."],
  "authority": "Act s X / Case [year] court no"
}
```

## Adding a question grounded in an official source

1. `python scripts/fetch_source.py <legislation.gov.uk or Find Case Law URL>` →
   clean text in `sources/`.
2. Author one SBA question from that text; cite the section/case verbatim.
3. Append it to `questions/original_ew.json` with `verified_for_ew: true`.
4. `python scripts/validate_questions.py` to check schema + invariants.
5. `python scripts/export_knowledge.py` to refresh the knowledge doc.

CI (`.github/workflows/ci.yml`) runs steps 4–5 on every push/PR and fails if the
exported `02-question-bank.md` is out of sync with the JSON bank.

Official sources, in order of preference: `legislation.gov.uk` (statute),
`caselaw.nationalarchives.gov.uk` (Find Case Law), then `bailii.org`.

## Skills and agent

- `.claude/skills/sqe-cold-start/` — run the cold-start interview.
- `.claude/skills/sqe-quiz/` — run a quiz session from the verified bank.
- `.claude/skills/sqe-generate-question/` — generate a grounded question.
- `.claude/agents/sqe-question-generator.md` — subagent for batch question
  generation from official sources.

## Conventions

- Python: standard library only where possible; `fetch_source.py` has **no**
  third-party deps; `build_question_pool.py` needs `datasets` (optional).
- Keep `data/` and `sources/` out of version control (see `.gitignore`); the
  committed deliverables are the JSON bank and `claude-project/`.
