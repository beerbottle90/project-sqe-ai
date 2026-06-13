# Changelog

All notable changes to Project SQE AI are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.0.1]: https://github.com/beerbottle90/project-sqe-ai/releases/tag/v0.0.1
