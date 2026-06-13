# Changelog

All notable changes to Project SQE AI are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-06-13

### Added
- **31 new verified England & Wales questions** (bank now totals **44**),
  expanding coverage across Contract, Tort, Business Law, Dispute Resolution,
  Criminal Law, Land Law, Trusts, Wills, Property Practice, Solicitors Accounts,
  Ethics, and a new **Constitutional and Administrative Law** subject. Each is
  grounded in an official source and cites its authority (e.g. Misrepresentation
  Act 1967 s 2(1); Wagon Mound (No 1); Companies Act 2006 s 175; Theft Act 1968
  ss 8–9; Offences against the Person Act 1861 ss 18/20/47; Trustee Act 1925
  s 34(2); Wills Act 1837 s 18; Human Rights Act 1998 ss 3–4).
- **`scripts/validate_questions.py`** — schema and invariants validator
  (unique ids, answer ∈ options, verified questions must cite an authority and be
  England & Wales).
- **Continuous integration** (`.github/workflows/ci.yml`) — runs the validator
  and checks that `claude-project/knowledge/02-question-bank.md` is in sync with
  the JSON bank on every push and pull request.
- **`.gitattributes`** — normalises line endings so the export-freshness check is
  deterministic across platforms.

### Changed
- Regenerated `claude-project/knowledge/02-question-bank.md` (44 questions).
- Set the `LICENSE` copyright holder to **beerbottle90**.
- Updated `README.md` (CI/licence badges, question count, repo map).

## [0.0.1] - 2026-06-13

Initial public release.

### Added
- **claude.ai Projects package** (`claude-project/`): custom instructions
  (`INSTRUCTIONS.md`), three knowledge files (SQE1 overview, question bank,
  sources & generation guide), and a step-by-step `SETUP.md`.
- **Claude Code layer** (`.claude/`): skills `sqe-cold-start`, `sqe-quiz`,
  `sqe-generate-question`, and the `sqe-question-generator` agent; plus
  `CLAUDE.md` repo conventions.
- **Verified question bank** (`questions/original_ew.json`): 13 England & Wales
  single-best-answer questions across the SQE1 syllabus, each with a model
  answer, explanation and a cited authority.
- **Local Python pipeline** (`scripts/`): `cold_start_interview.py`, `quiz.py`,
  `build_question_pool.py`, `export_knowledge.py`, and `fetch_source.py`
  (pulls official text from legislation.gov.uk / Find Case Law; standard library
  only).
- **Source-grounded generation**: demo question `ew-tort-0002` generated from the
  Occupiers' Liability Act 1957, s 2.
- Formal **UK English** throughout; **England & Wales only** jurisdiction policy;
  non-E&W datasets isolated as optional reasoning practice.
- Project docs: `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, MIT
  `LICENSE`, GitHub issue/PR templates.

[0.0.2]: https://github.com/beerbottle90/project-sqe-ai/releases/tag/v0.0.2
[0.0.1]: https://github.com/beerbottle90/project-sqe-ai/releases/tag/v0.0.1
