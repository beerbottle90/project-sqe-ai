#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQE soru havuzu derleyici
=========================

Hugging Face'ten iki açık hukuk-sınavı datasetini indirir, SQE ile örtüşen
konuları (Contract / Tort / Criminal) filtreler, kendi İngiliz-hukuku soru
bankamızla birleştirir ve tek bir JSON dosyasına yazar.

  - reglab/barexam_qa        -> ABD Multistate Bar Exam (jurisdiction: US)
  - LEXam-Benchmark/LEXam    -> İsviçre/AB/uluslararası hukuk sınavları
  - questions/original_ew.json -> bizim doğruladığımız İngiliz-hukuku soruları

!!! UYARI -- JURISDICTION !!!
barexam_qa ve LEXam İngiliz hukuku DEĞİLDİR. Doğru cevapları İngiliz hukukuna
göre teyit edilmemiştir; her biri "verified_for_ew": false olarak işaretlenir.
Bunları yalnızca muhakeme pratiği için kullan, kural ezberlemek için DEĞİL.

Kullanım:
  pip install -r requirements.txt
  python scripts/build_question_pool.py                 # her şey, varsayılan filtre
  python scripts/build_question_pool.py --limit 200     # kaynak başına 200 ile sınırla
  python scripts/build_question_pool.py --sources lexam # sadece LEXam
  python scripts/build_question_pool.py --all-subjects  # konu filtresi yok
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGINAL = ROOT / "questions" / "original_ew.json"
OUT_DEFAULT = ROOT / "data" / "question_pool.json"

# SQE ile örtüşen çekirdek konular (varsayılan filtre)
DEFAULT_SUBJECTS = {"Contract", "Tort", "Criminal Law"}

# Konu sınıflandırıcı: metinde aranan anahtar kelimeler (küçük harfle).
# Sıra önemli -- ilk eşleşen konu kazanır.
SUBJECT_KEYWORDS = [
    ("Criminal Law", [
        " r v ", "mens rea", "actus reus", "theft", "burglary", "robbery",
        "murder", "manslaughter", "assault", "battery", "guilty", "prosecut",
        "criminal", "indict", "homicide", "self-defence", "self-defense",
    ]),
    ("Tort", [
        "negligen", "duty of care", "tort", "nuisance", "occupier",
        "trespass", "defamation", "vicarious", "remoteness", "breach of duty",
    ]),
    ("Contract", [
        "contract", "breach of contract", "consideration", "offer and",
        "acceptance", "promisor", "promisee", "warranty", "repudiat",
        "misrepresentation", "agreement to", "frustrat",
    ]),
]


def classify_subject(text: str) -> str | None:
    """Serbest metinden SQE konusunu tahmin et; eşleşme yoksa None."""
    low = " " + text.lower() + " "
    for subject, keywords in SUBJECT_KEYWORDS:
        if any(kw in low for kw in keywords):
            return subject
    return None


def letter(idx: int) -> str:
    return chr(ord("A") + idx)


# --------------------------------------------------------------------------- #
# Kaynak: reglab/barexam_qa
# --------------------------------------------------------------------------- #
def load_barexam(limit: int | None, keep_all_subjects: bool) -> list[dict]:
    from datasets import load_dataset, concatenate_datasets, DatasetDict

    ds = load_dataset("reglab/barexam_qa", "qa")
    if isinstance(ds, DatasetDict):
        ds = concatenate_datasets([ds[s] for s in ds.keys()])

    out: list[dict] = []
    for row in ds:
        scenario = (row.get("prompt") or "").strip()
        question = (row.get("question") or "").strip()
        subject = classify_subject(scenario + " " + question)
        if not keep_all_subjects:
            if subject is None or subject not in DEFAULT_SUBJECTS:
                continue
        options = {
            "A": row.get("choice_a", ""),
            "B": row.get("choice_b", ""),
            "C": row.get("choice_c", ""),
            "D": row.get("choice_d", ""),
        }
        out.append({
            "id": f"barexam-{row.get('idx')}",
            "source": "barexam_qa",
            "jurisdiction": "US (Multistate Bar Exam)",
            "subject": subject or "Other",
            "flk": None,
            "scenario": scenario,
            "question": question,
            "options": options,
            "answer": (row.get("answer") or "").strip().upper(),
            "explanation": "",
            "verified_for_ew": False,
            "tags": ["imported", "us-law", "reasoning-practice"],
        })
        if limit and len(out) >= limit:
            break
    return out


# --------------------------------------------------------------------------- #
# Kaynak: LEXam-Benchmark/LEXam  (mcq_4_choices, sadece İngilizce)
# --------------------------------------------------------------------------- #
def load_lexam(limit: int | None, keep_all_subjects: bool) -> list[dict]:
    from datasets import load_dataset

    ds = load_dataset("LEXam-Benchmark/LEXam", "mcq_4_choices", split="test")

    # area -> etiket eşlemesi. LEXam E&W DEĞİLDİR; konuyu açıkça non-E&W işaretle
    # ki yerel havuzda E&W sorularıyla karışmasın.
    area_map = {"private": "Private Law (non-E&W)", "criminal": "Criminal Law (non-E&W)"}

    out: list[dict] = []
    for row in ds:
        if (row.get("language") or "").lower() != "en":
            continue
        area = (row.get("area") or "").lower()
        if not keep_all_subjects and area not in area_map:
            continue
        subject = area_map.get(area, area.capitalize() or "Other")
        choices = row.get("choices") or []
        options = {letter(i): c for i, c in enumerate(choices)}
        gold = row.get("gold")
        answer = letter(gold) if isinstance(gold, int) and 0 <= gold < len(choices) else ""
        juris = (row.get("jurisdiction") or "").strip() or "unknown"
        course = (row.get("course") or "").strip()
        out.append({
            "id": f"lexam-{row.get('id')}",
            "source": "lexam",
            "jurisdiction": f"{juris} (LEXam{': ' + course if course else ''})",
            "subject": subject,
            "flk": None,
            "scenario": "",
            "question": (row.get("question") or "").strip(),
            "options": options,
            "answer": answer,
            "explanation": "",
            "verified_for_ew": False,
            "tags": ["imported", "non-ew-law", "reasoning-practice"],
        })
        if limit and len(out) >= limit:
            break
    return out


def load_original() -> list[dict]:
    if not ORIGINAL.exists():
        print(f"[uyari] {ORIGINAL} bulunamadi; ozgun soru eklenmiyor.", file=sys.stderr)
        return []
    with ORIGINAL.open(encoding="utf-8") as fh:
        data = json.load(fh)
    for q in data:
        q.setdefault("source", "original")
        q.setdefault("jurisdiction", "England & Wales")
        q.setdefault("verified_for_ew", True)
    return data


def summarise(pool: list[dict]) -> None:
    by_source: dict[str, int] = {}
    by_subject: dict[str, int] = {}
    verified = 0
    for q in pool:
        by_source[q["source"]] = by_source.get(q["source"], 0) + 1
        by_subject[q["subject"]] = by_subject.get(q["subject"], 0) + 1
        verified += 1 if q.get("verified_for_ew") else 0
    print("\n=== Soru havuzu ozeti ===")
    print(f"Toplam soru        : {len(pool)}")
    print(f"E&W dogrulanmis     : {verified}")
    print(f"Dogrulanmamis (diger): {len(pool) - verified}")
    print("Kaynak dagilimi    :", dict(sorted(by_source.items())))
    print("Konu dagilimi      :", dict(sorted(by_subject.items())))


def main() -> int:
    ap = argparse.ArgumentParser(description="SQE soru havuzu derleyici")
    ap.add_argument("--sources", default="barexam,lexam",
                    help="Virgulle ayrilmis: barexam,lexam (varsayilan ikisi de)")
    ap.add_argument("--limit", type=int, default=None,
                    help="Kaynak basina maksimum soru sayisi")
    ap.add_argument("--all-subjects", action="store_true",
                    help="Konu filtresini kapat (her seyi al)")
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT,
                    help="Cikti JSON yolu")
    args = ap.parse_args()

    sources = {s.strip().lower() for s in args.sources.split(",") if s.strip()}
    pool: list[dict] = []

    # Cekirdek: her zaman bizim İngiliz-hukuku sorularimiz
    original = load_original()
    print(f"[ok] ozgun E&W soru: {len(original)}")
    pool.extend(original)

    # Her kaynak kendi try/except'inde: biri patlarsa digeri yine yuklenir.
    def try_source(name: str, fn) -> None:
        try:
            items = fn(args.limit, args.all_subjects)
            print(f"[ok] {name}: {len(items)} soru alindi")
            pool.extend(items)
        except ImportError:
            print(f"[HATA] {name}: 'datasets' kurulu degil "
                  "(pip install -r requirements.txt).", file=sys.stderr)
        except Exception as exc:
            print(f"[HATA] {name} basarisiz: {exc}", file=sys.stderr)

    if "barexam" in sources:
        # Not: reglab/barexam_qa script-tabanli yuklenir; datasets 3.x bunu
        # desteklemez. Gerekirse: pip install 'datasets<3' veya parquet'i elle indir.
        try_source("barexam_qa", load_barexam)
    if "lexam" in sources:
        try_source("lexam", load_lexam)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fh:
        json.dump(pool, fh, ensure_ascii=False, indent=2)

    summarise(pool)
    print(f"\n[yazildi] {args.out}  ({len(pool)} soru)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
