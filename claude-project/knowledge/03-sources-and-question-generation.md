# Official Sources & Question Generation Guide

How the coach should create **new** SQE1 questions that are accurate, current,
and grounded in **England-and-Wales** primary law.

## Golden rules

1. **England and Wales only.** Never state a US/EU/Swiss rule as the answer.
2. **Never invent citations.** Cite an Act + section or a case + neutral citation
   only when you are confident it is correct. If unsure, state the rule without a
   citation rather than fabricate one.
3. **Single best answer format**, five options A–E, one best answer, realistic
   scenario, plausible distractors that test a genuine misconception.
4. Calibrate difficulty and subject mix to the candidate's profile.

## Official primary sources (preferred order)

- **Legislation:** https://www.legislation.gov.uk — the official UK statute book.
  Cite as *Act name Year, s X* (e.g. *Limitation Act 1980, s 5*).
  Direct section URLs look like:
  `https://www.legislation.gov.uk/ukpga/1968/60/section/1` (Theft Act 1968, s 1).
  Machine-readable text: append `/data.xml` or `/data.akn` to a section URL.
- **Case law (official):** **Find Case Law**, The National Archives —
  https://caselaw.nationalarchives.gov.uk . Cite case name + neutral citation
  (e.g. *R v Jogee [2016] UKSC 8*). Judgment XML: append `/data.xml` to a
  judgment URL.
- **Case law (secondary, acceptable):** **BAILII** — https://www.bailii.org .

## Workflow

1. Pick a syllabus point (use the subject list in `01-sqe1-overview.md`).
2. Pull the governing rule from the source above (statute section or leading case).
3. Write a scenario that turns on **one** decisive issue.
4. Draft five options: one best answer + four distractors, each reflecting a
   realistic error (wrong test, right test/wrong application, plausible-but-dated
   rule, etc.).
5. Write the explanation: state the rule, name the **authority**, and say briefly
   why each strong distractor fails.
6. Save to the question bank using the schema below; mark `verified_for_ew: true`
   only once the authority is confirmed.

## Question schema (matches `questions/original_ew.json`)

```json
{
  "id": "ew-<subject>-NNNN",
  "source": "original",
  "jurisdiction": "England & Wales",
  "subject": "Contract | Tort | Criminal Law | ...",
  "flk": "FLK1 | FLK2 | null",
  "scenario": "facts ...",
  "question": "the stem ...",
  "options": { "A": "...", "B": "...", "C": "...", "D": "...", "E": "..." },
  "answer": "A",
  "explanation": "rule + why others fail",
  "verified_for_ew": true,
  "tags": ["...", "..."],
  "authority": "Act s X / Case [year] court no"
}
```

## Starter index — key authorities by subject

A non-exhaustive anchor list to generate from. Verify each before citing.

- **Contract:** *Carlill v Carbolic Smoke Ball Co* [1893]; *Williams v Roffey Bros*
  [1991] (practical benefit); *Hadley v Baxendale* (1854) (remoteness);
  Consumer Rights Act 2015; Misrepresentation Act 1967.
- **Tort:** *Donoghue v Stevenson* [1932]; *Caparo Industries plc v Dickman*
  [1990] UKHL 2 (duty / economic loss); Occupiers' Liability Acts 1957 & 1984;
  *Wagon Mound (No 1)* [1961] (remoteness).
- **Criminal:** Theft Act 1968; Criminal Justice Act 1967, s 8 (intention);
  *R v Jogee* [2016] UKSC 8 (accessories); Offences Against the Person Act 1861.
- **Business Law:** Companies Act 2006 (e.g. s 168 removal of director;
  ss 21, 168, 282–283 resolutions); Insolvency Act 1986.
- **Dispute Resolution:** Civil Procedure Rules (tracks; Part 36 offers);
  Limitation Act 1980 (s 5 contract 6 yrs; s 2 tort 6 yrs; s 11 PI 3 yrs).
- **Land Law:** Law of Property Act 1925 (e.g. s 36(2) severance);
  Land Registration Act 2002; *Re Ellenborough Park* [1956] (easements).
- **Trusts:** *Knight v Knight* (1840) (three certainties);
  *Re Adams and Kensington Vestry* (1884) (precatory words);
  Trustee Act 2000.
- **Wills:** Wills Act 1837 (s 9 execution; s 15 beneficiary-witness);
  Administration of Estates Act 1925; Inheritance (Provision for Family and
  Dependants) Act 1975.
- **Property Practice:** Standard Conditions of Sale (risk on exchange);
  Law of Property (Miscellaneous Provisions) Act 1989, s 2.
- **Solicitors Accounts / Ethics:** SRA Accounts Rules; SRA Standards and
  Regulations (SRA Principles; Code of Conduct for Solicitors).

## Worked example (generated from an official source)

Source pulled from legislation.gov.uk: **Occupiers' Liability Act 1957, s 2** —
s 2(2) common duty of care; **s 2(3)(a)** "an occupier must be prepared for
children to be less careful than adults". The question
`ew-tort-0002` in the question bank is generated from this section and cites it.
