# Contributing to Project SQE AI

Thanks for helping build a free, source-grounded SQE1 study tool. Contributions
of **verified questions**, corrections, and tooling improvements are all welcome.

## Ground rules

1. **England & Wales law only.** Never add a US/EU/other-jurisdiction rule as an
   answer. Imported non-E&W datasets are reasoning practice only and stay out of
   the knowledge base.
2. **Cite a real authority.** Every question must carry an `authority` — an Act +
   section or a case + neutral citation. Do not invent citations.
3. **Formal UK English.** British spelling and UK legal terminology
   (*claimant*, *solicitor*, *judgment*).
4. **Single best answer format.** A realistic scenario, a precise stem, five
   options A–E, exactly one best answer, plausible distractors.

## Adding a question

1. Add an object to [`questions/original_ew.json`](questions/original_ew.json)
   using the schema (see [`CLAUDE.md`](CLAUDE.md)). Use the id pattern
   `ew-<subject>-NNNN` and set `verified_for_ew: true`.
2. If you generated it from an official source, pull the text first:
   `python scripts/fetch_source.py <legislation.gov.uk or Find Case Law URL>`.
3. Regenerate the knowledge document:
   `python scripts/export_knowledge.py`.
4. Open a pull request.

## Pull request checklist

- [ ] England & Wales law only.
- [ ] Every new question has a verified `authority`.
- [ ] Formal UK English.
- [ ] Single best answer format, five options.
- [ ] Ran `python scripts/export_knowledge.py` and committed the updated
      `claude-project/knowledge/02-question-bank.md`.
- [ ] `questions/original_ew.json` is valid JSON.

## Development

```bash
pip install -r requirements.txt
python -c "import json; json.load(open('questions/original_ew.json', encoding='utf-8'))"  # validate
python scripts/export_knowledge.py
```

## Reporting issues

Use the issue templates: bug report, feature request, or **question correction**
(for a wrong answer or citation — please include the authority that supports the
fix).

By contributing you agree your contributions are licensed under the repository's
[MIT License](LICENSE).
