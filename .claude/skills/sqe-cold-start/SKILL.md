---
name: sqe-cold-start
description: Run the SQE1 cold-start interview to profile the candidate and tailor study (priority subjects, difficulty, study plan, exemption strategy). Use at the start with a new candidate, or when they say "set me up", "get started", "cold start", "profile me".
---

# SQE1 Cold-Start Interview

Profile the candidate, then adapt everything to them. Operate in **formal UK
English**. The full behaviour spec is `claude-project/INSTRUCTIONS.md` — follow
section 4 (cold-start) and section 5 (adapt).

## Steps

1. Ask these as single-best-answer multiple choice questions. Present them a few
   at a time and **wait** for answers:
   1. Legal background — (a) lawyer qualified abroad, (b) law graduate,
      (c) non-law, (d) other.
   2. Years of post-qualification experience — (a) 0–2, (b) 2–5, (c) 5+.
   3. Target sitting — (a) July booked, (b) July not booked, (c) January,
      (d) undecided.
   4. Weekly study time — (a) <5h, (b) 5–15h, (c) 15–30h, (d) 30+h.
   5. Preferred difficulty — (a) easy–medium, (b) medium–hard, (c) exam-level.
   6. Priority subjects (multi-select) — Contract; Tort; Business Law and
      Practice; Dispute Resolution; Property Practice; Land Law; Trusts; Wills;
      Criminal Law; Solicitors Accounts; Constitutional & Administrative Law;
      Ethics.
   7. Exemption strategy — (a) sit SQE1 + apply for SQE2 exemption,
      (b) sit both, (c) undecided.

2. Summarise the profile back in a short block.

3. Persist it so future sessions can reuse it:
   - In Claude Code, write it to `data/profile.json` (or run
     `python scripts/cold_start_interview.py`).
   - In a claude.ai Project, tell the candidate to **save the summary and paste
     it at the start of future chats** (Project chats do not share memory).

4. Hand off: offer to start `/sqe-quiz`, weighting the candidate's priority
   subjects and chosen difficulty.

## Adaptation cues

- A lawyer qualified abroad → strong general reasoning, **no** E&W-specific
  knowledge; explain English rules from first principles; keep the SQE2 exemption
  route in view.
- Map weekly time to a realistic plan and a daily question target.
