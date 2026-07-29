#!/usr/bin/env python3
"""
ats_score.py — estimate ATS compatibility and, more usefully, produce the
missing-term list.

    python scripts/ats_score.py --resume out/resume.txt --jd out/jd-analysis.json
    python scripts/ats_score.py --resume out/resume.txt --jd out/jd-analysis.json \
                                --pdf out/resume.pdf --json

The number is a diagnostic, not a grade. Its real output is the table of terms the
JD wants and the resume doesn't contain — for each one, ask whether a TRUE
statement exists that would naturally contain that word.

Components (see references/scoring-and-review.md):
    required coverage   40
    preferred coverage  15
    hidden keywords     15
    evidence placement  10   (required terms appearing in a bullet, not just SKILLS)
    parseability        10
    impact density      10
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

LIGATURE_WORDS = [
    "artificial", "certification", "classifier", "classification",
    "efficiency", "workflow", "profile", "fine-tuned", "identify", "specific",
]


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"[‐-―]", "-", t)
    t = re.sub(r"\s+", " ", t)
    return t


def variants(term: str) -> list[str]:
    """Reasonable spelling variants a parser might match."""
    t = norm(term)
    out = {t}
    out.add(t.replace("/", ""))
    out.add(t.replace("/", " "))
    out.add(t.replace("-", " "))
    out.add(t.replace("-", ""))
    out.add(t.replace(".", ""))
    if t.endswith("s"):
        out.add(t[:-1])
    else:
        out.add(t + "s")
    return sorted(out)


def blob_forms(blob: str) -> list[str]:
    """The resume side needs the same folding as the term side — otherwise
    'structured output' misses 'structured-output' and vice versa."""
    return [blob, blob.replace("-", " "), blob.replace("-", ""), blob.replace("/", " ")]


def present(term: str, blob: str) -> bool:
    forms = blob_forms(blob)
    return any(v and any(v in b for b in forms) for v in variants(term))


def count(term: str, blob: str) -> int:
    forms = blob_forms(blob)
    return max(
        (len(re.findall(re.escape(v), b)) for v in variants(term) if v for b in forms),
        default=0,
    )


def weighted(terms, blob, weights: dict | None = None):
    """Return (score_fraction, hits, misses)."""
    hits, misses, got, tot = [], [], 0.0, 0.0
    for t in terms:
        w = float((weights or {}).get(t, 1.0))
        tot += w
        if present(t, blob):
            hits.append(t)
            got += w
        else:
            misses.append(t)
    return (got / tot if tot else 1.0), hits, misses


def split_sections(resume: str) -> dict[str, str]:
    """Crude section split so we can tell SKILLS-only mentions from bullet mentions."""
    sections, current, buf = {}, "HEADER", []
    for line in resume.splitlines():
        stripped = line.strip().rstrip(":").upper()
        if stripped in {"EDUCATION", "SKILLS", "EXPERIENCE", "PROJECTS",
                        "SUMMARY", "PUBLICATIONS", "CERTIFICATIONS"}:
            sections[current] = "\n".join(buf)
            current, buf = stripped, []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf)
    return sections


def parseability(resume: str) -> tuple[float, list[str]]:
    notes, score = [], 1.0
    up = resume.upper()
    for h in ("EDUCATION", "EXPERIENCE", "SKILLS"):
        if h not in up:
            score -= 0.2
            notes.append(f"missing standard heading: {h}")
    if not re.search(r"[A-Za-z]+\s+\d{4}\s*[-–]\s*(?:[A-Za-z]+\s+\d{4}|Present)", resume):
        score -= 0.25
        notes.append("no parseable 'Month YYYY - Month YYYY' date range found")
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", resume):
        score -= 0.15
        notes.append("no email address found in the body")
    if "\t" in resume:
        score -= 0.05
        notes.append("tab characters present (column-layout risk)")
    return max(0.0, score), notes


def impact_density(resume: str) -> tuple[float, int, int]:
    bullets = [l for l in resume.splitlines()
               if re.match(r"\s*[-*•]\s+\S", l) or "\\item" in l]
    if not bullets:
        return 0.0, 0, 0
    with_num = sum(1 for b in bullets if re.search(r"\d", b))
    return with_num / len(bullets), with_num, len(bullets)


def pdf_extraction_check(pdf: Path) -> tuple[bool, list[str]]:
    if not shutil.which("pdftotext"):
        return True, ["pdftotext not installed — extraction check skipped"]
    try:
        txt = subprocess.run(["pdftotext", str(pdf), "-"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception as e:                                    # noqa: BLE001
        return True, [f"pdftotext failed: {e}"]
    low = norm(txt)
    # Look for the classic mangled forms, as whole words — 'ne-tuned' is a
    # substring of the CORRECT 'fine-tuned', so substring matching false-positives.
    mangled = [m for m in ("articial", "certications", "certication", "classier",
                           "classication", "eciency", "ecient", "workow", "prole",
                           "ne-tuned", "identiy", "signicant", "conguration")
               if re.search(rf"(?<![a-z]){re.escape(m)}(?![a-z])", low)]
    notes = []
    ok = True
    if mangled:
        ok = False
        notes.append(f"LIGATURE BUG — extracted text contains {mangled}. "
                     "Add \\usepackage{cmap}, [T1]{fontenc}, {lmodern}.")
    if len(low.strip()) < 400:
        ok = False
        notes.append("extracted text is suspiciously short — possible image-only PDF")
    if ok and not notes:
        notes.append("PDF text extraction looks clean")
    return ok, notes


def band(score: float) -> str:
    if score >= 85:
        return "Strong keyword alignment; remaining risk is human judgment."
    if score >= 70:
        return "Will clear most filters. Check whether misses are real gaps or vocabulary mismatches."
    if score >= 55:
        return "Borderline — usually a vocabulary problem, not a capability one. Highest-return zone for rewriting."
    return "Either a genuine mismatch or a different role family. Say so plainly."


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resume", required=True)
    ap.add_argument("--jd", required=True, help="jd-analysis.json")
    ap.add_argument("--pdf", help="optional: also run the PDF extraction check")
    ap.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = ap.parse_args()

    resume_raw = Path(args.resume).read_text(encoding="utf-8")
    jd = json.loads(Path(args.jd).read_text(encoding="utf-8"))
    blob = norm(resume_raw)

    req = jd.get("required_skills", []) or []
    pref = jd.get("preferred_skills", []) or []
    hidden = jd.get("hidden_keywords", []) or []
    weights = jd.get("weights", {}) or {}

    f_req, hit_req, miss_req = weighted(req, blob, weights)
    f_pref, hit_pref, miss_pref = weighted(pref, blob)
    f_hid, hit_hid, miss_hid = weighted(hidden, blob)

    sections = split_sections(resume_raw)
    non_skills = norm("\n".join(v for k, v in sections.items() if k != "SKILLS"))
    placed = [t for t in hit_req if present(t, non_skills)]
    f_place = len(placed) / len(hit_req) if hit_req else 1.0

    f_parse, parse_notes = parseability(resume_raw)
    f_impact, n_num, n_bul = impact_density(resume_raw)

    score = round(
        40 * f_req + 15 * f_pref + 15 * f_hid
        + 10 * f_place + 10 * f_parse + 10 * f_impact, 1
    )

    stuffed = [t for t in hit_req if count(t, blob) >= 3]

    pdf_ok, pdf_notes = (True, [])
    if args.pdf:
        pdf_ok, pdf_notes = pdf_extraction_check(Path(args.pdf))
        if not pdf_ok:
            score = round(score * 0.6, 1)

    result = {
        "score": score,
        "band": band(score),
        "components": {
            "required_coverage": round(f_req, 3),
            "preferred_coverage": round(f_pref, 3),
            "hidden_keyword_coverage": round(f_hid, 3),
            "evidence_placement": round(f_place, 3),
            "parseability": round(f_parse, 3),
            "impact_density": round(f_impact, 3),
        },
        "missing_required": miss_req,
        "missing_preferred": miss_pref,
        "missing_hidden": miss_hid,
        "possible_stuffing": stuffed,
        "parseability_notes": parse_notes,
        "pdf_notes": pdf_notes,
        "bullets": {"total": n_bul, "with_number": n_num},
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"\nATS SCORE: {score}/100")
    print(f"  {band(score)}\n")
    print("Components")
    for k, v in result["components"].items():
        print(f"  {k:<26} {v:>6.0%}")
    print(f"\nBullets with a number: {n_num}/{n_bul}")

    def table(title, items):
        if items:
            print(f"\n{title}")
            for t in items:
                w = weights.get(t, "")
                print(f"  - {t}{f'  (weight {w})' if w else ''}")

    table("MISSING — required  [for each: is there a TRUE statement containing this word?]", miss_req)
    table("MISSING — preferred", miss_pref)
    table("MISSING — hidden keywords (highest-leverage; these are the manager's own words)", miss_hid)
    if stuffed:
        table("POSSIBLE STUFFING (3+ occurrences)", stuffed)
    if parse_notes:
        table("PARSEABILITY", parse_notes)
    if pdf_notes:
        table("PDF EXTRACTION", pdf_notes)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
