# Setting up Project SQE AI in claude.ai Projects

A five-minute, no-code setup. You will create a Project, give it the coach's
instructions, and upload the knowledge files.

## 1. Create the Project

1. Go to [claude.ai](https://claude.ai) and open **Projects**.
2. Click **Create Project**. Name it **Project SQE AI** (or "SQE1 Coach").
3. Add a short description, e.g. *"SQE1 study coach — England & Wales,
   single best answer practice."*

## 2. Add the custom instructions

1. Open the Project's **Custom Instructions** (sometimes "Set instructions").
2. Copy the **entire** contents of [`INSTRUCTIONS.md`](INSTRUCTIONS.md) and paste
   them in. Save.

## 3. Upload the knowledge files

Add these three files from [`knowledge/`](knowledge/) to the Project knowledge:

- `01-sqe1-overview.md` — exam format, syllabus, dates, fees, exemptions.
- `02-question-bank.md` — the verified England & Wales question bank.
- `03-sources-and-question-generation.md` — official sources + how new questions
  are generated.

> If you have run the Python pipeline, `02-question-bank.md` is regenerated from
> `questions/original_ew.json` by `python scripts/export_knowledge.py`. Re-upload
> it whenever you add questions.

## 4. Start studying

Open a new chat in the Project and say, for example, **"Let's begin."** The coach
will:

1. Run a short **cold-start interview** (multiple choice) to learn your
   background, target sitting, weekly time, difficulty and priority subjects.
2. Summarise your **profile** — **save this** and paste it at the start of future
   chats (separate Project chats do not share memory).
3. Start **quizzing** you with single best answer questions, marking each answer
   with an explanation and the governing authority.

Useful prompts:
- *"Quiz me on Tort, exam level, five questions."*
- *"Generate a new question from the Limitation Act 1980."*
- *"Explain the intermediate track again."*
- *"Build me a 4-week plan at 15 hours a week."*

## 5. Keep it current

Exam dates and fees change. Ask the coach to confirm against the SRA site, or
update `01-sqe1-overview.md` and re-upload.

---

### Hızlı not (TR)

claude.ai → Projects → **Create Project** → adını *Project SQE AI* koy →
**Custom Instructions** kısmına `INSTRUCTIONS.md` içeriğini yapıştır →
`knowledge/` klasöründeki 3 dosyayı projeye yükle → yeni sohbet aç ve
"Let's begin" yaz. Asistan UK English çalışır: önce cold-start interview yapar,
sonra çoktan seçmeli sorularla sınar. Profil özetini kaydet, sonraki sohbetlerin
başında yapıştır.
