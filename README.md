# Project SQE AI

**An open-source, source-grounded AI study companion for the SQE1** — Part 1 of
the Solicitors Qualifying Examination (England & Wales).

Project SQE AI turns Claude into an SQE1 coach that:

- runs a **cold-start interview** to learn the candidate and tailor everything;
- drills you with **exam-format single best answer (SBA)** questions, five
  options A–E, one best answer;
- explains every answer with the **governing authority** (statute section or
  leading case);
- **generates new questions grounded in official UK primary law** —
  [legislation.gov.uk](https://www.legislation.gov.uk) and the National Archives'
  [Find Case Law](https://caselaw.nationalarchives.gov.uk);
- operates in **formal UK English**, the language of the assessment.

It runs **two ways**: inside a **claude.ai Project** (no code) or in **Claude
Code** (skills + agents + a local Python pipeline).

> ⚖️ **Jurisdiction:** England & Wales only. This is a study aid, **not legal
> advice**. Always confirm format, dates and fees on the
> [SRA's SQE site](https://sqe.sra.org.uk). See the disclaimer below.

---

## Why this exists

SQE preparation is expensive and the question banks are mostly paywalled.
Project SQE AI is a free, transparent, **source-grounded** alternative — every
generated question can be traced back to an official statute or judgment. It is
built with international, foreign-qualified candidates in mind (for example, a
lawyer qualified abroad who sits SQE1 and applies for an SQE2 exemption).

## Two ways to use it

### A) claude.ai Projects (no code)

1. Create a new Project on [claude.ai](https://claude.ai).
2. Paste [`claude-project/INSTRUCTIONS.md`](claude-project/INSTRUCTIONS.md) into
   the Project's **Custom Instructions**.
3. Upload the three files in
   [`claude-project/knowledge/`](claude-project/knowledge/) to the Project
   knowledge base.
4. Start a chat — the coach runs the cold-start interview, then quizzes you.

Full walkthrough: [`claude-project/SETUP.md`](claude-project/SETUP.md).

### B) Claude Code

Open this repo in Claude Code and use the bundled skills:

- `/sqe-cold-start` — profile the candidate and tailor the plan.
- `/sqe-quiz` — run a quiz session from the verified question bank.
- `/sqe-generate-question` — author a new SBA question grounded in an official
  source and add it to the bank.

There is also a question-generation subagent in
[`.claude/agents/`](.claude/agents/) and repo conventions in
[`CLAUDE.md`](CLAUDE.md).

## Repository map

```
.
├── claude-project/            # claude.ai Projects deliverable
│   ├── INSTRUCTIONS.md        #   → paste into Custom Instructions
│   ├── SETUP.md               #   → step-by-step setup
│   └── knowledge/             #   → upload these to Project knowledge
│       ├── 01-sqe1-overview.md
│       ├── 02-question-bank.md        (generated from the JSON)
│       └── 03-sources-and-question-generation.md
├── .claude/                   # Claude Code layer
│   ├── skills/                #   sqe-cold-start, sqe-quiz, sqe-generate-question
│   └── agents/                #   sqe-question-generator
├── questions/
│   └── original_ew.json       # the verified England & Wales question bank
├── scripts/                   # local Python pipeline (optional)
│   ├── cold_start_interview.py
│   ├── quiz.py
│   ├── build_question_pool.py
│   ├── export_knowledge.py    # JSON → claude-project/knowledge/02-question-bank.md
│   └── fetch_source.py        # pull official text from legislation.gov.uk / Find Case Law
├── sources/                   # fetched official text (generated)
├── data/                      # generated pool / profile (gitignored)
├── CLAUDE.md
├── requirements.txt
└── LICENSE
```

## The question bank

The source of truth is [`questions/original_ew.json`](questions/original_ew.json)
— hand-written, **verified-for-England-&-Wales** SBA questions across the SQE1
syllabus, each carrying a model answer, an explanation, and the governing
authority. Convert it to the Project knowledge document with:

```bash
python scripts/export_knowledge.py   # writes claude-project/knowledge/02-question-bank.md
```

Each question follows this schema:

```json
{
  "id": "ew-tort-0002",
  "subject": "Tort",
  "flk": "FLK1",
  "scenario": "...",
  "question": "...",
  "options": { "A": "...", "B": "...", "C": "...", "D": "...", "E": "..." },
  "answer": "B",
  "explanation": "...",
  "authority": "Occupiers' Liability Act 1957, s 2(2) and s 2(3)(a)",
  "verified_for_ew": true,
  "tags": ["..."]
}
```

## Generating questions from official sources

Pull the exact text of a statute section or judgment, then have Claude author a
grounded, correctly-cited question:

```bash
# Theft Act 1968, section 1
python scripts/fetch_source.py https://www.legislation.gov.uk/ukpga/1968/60/section/1
# or by components
python scripts/fetch_source.py --legislation ukpga/1980/58/section/5 --slug limitation-s5
```

The fetched text lands in `sources/`. Feed it to the `/sqe-generate-question`
skill (or the `sqe-question-generator` agent), which writes a new question into
the bank citing the section verbatim. Question `ew-tort-0002` was produced this
way from the Occupiers' Liability Act 1957, s 2.

## Local Python pipeline (optional)

```bash
pip install -r requirements.txt
python scripts/cold_start_interview.py     # build data/profile.json
python scripts/build_question_pool.py      # assemble data/question_pool.json
python scripts/quiz.py                      # adaptive console quiz (E&W only by default)
```

`build_question_pool.py` can also import two **non-E&W** academic datasets
([LEXam](https://huggingface.co/datasets/LEXam-Benchmark/LEXam),
[reglab/barexam_qa](https://huggingface.co/datasets/reglab/barexam_qa)) purely
for *reasoning* practice. They are clearly tagged `verified_for_ew: false` and
**never** enter the Project knowledge base — their rules are not England & Wales
law. `quiz.py` excludes them unless you pass `--reasoning`.

## Disclaimer

Project SQE AI is an educational study aid for the law of **England & Wales**. It
is **not legal advice** and is not affiliated with the SRA. AI-generated content
can be wrong — verify every rule against the primary source before relying on it.
Exam format, dates and fees change; confirm them on the official SRA site.

## Contributing

Issues and pull requests welcome — especially new verified questions (with an
authority) and corrections. Keep every question England-&-Wales-specific, in UK
English, and cite a real statute section or case.

## Acknowledgements

- SRA SQE sample questions and assessment specification.
- [legislation.gov.uk](https://www.legislation.gov.uk) (Open Government Licence).
- The National Archives [Find Case Law](https://caselaw.nationalarchives.gov.uk).
- [LEXam](https://huggingface.co/datasets/LEXam-Benchmark/LEXam) and
  [reglab/barexam_qa](https://huggingface.co/datasets/reglab/barexam_qa) for
  optional non-E&W reasoning practice.

## License

[MIT](LICENSE). You may switch to Apache-2.0, or license the question content
separately under CC-BY, if that suits your release.
