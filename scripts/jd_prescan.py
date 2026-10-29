#!/usr/bin/env python3
"""
jd_prescan.py — deterministic first pass over a job description (Stage 2 helper).

    python scripts/jd_prescan.py --jd jd.txt --ledger truth-base.yaml --out out/jd-prescan.json

Ported in spirit from the Resume Maxer analyzer: a fixed term dictionary (assets/jd_terms.json) is matched
against the posting, weighted by WHERE it appears (title 3, required section 3, preferred 1.5, description 1).
It is DETECTION ONLY. It never grants a skill. Every detected term is tagged against the truth ledger:

    claimable   the ledger lists evidence for the term (or one of its aliases)
    gap         the term is on the Do-NOT-claim list, or the ledger marks it weak; say so plainly, never add it
    unverified  no evidence either way; ask whether a TRUE statement exists before using it

The output is a DRAFT for the JD Analyzer stage: its required/preferred/hidden lists feed ats_score.py once reviewed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# Fallback gap list (the candidate's standing Do-NOT-claim set). A ledger's weak_evidence list is added to it.
DEFAULT_GAPS = {
    "kubernetes", "k8s", "azure", "spark", "apache spark", "pyspark", "kafka", "hadoop", "hive", "mongodb",
    "xgboost", "databricks", "snowflake", "dbt", "airflow", "fastapi", "llamaindex", "r programming", "java",
    "c", "c++", "ci/cd", "terraform", "ansible", "jenkins", "github actions",
}

SKIP = re.compile(r"^(benefits?|compensation|salary|pay range|base pay|total compensation|equal opportunity|eeo|"
                  r"about (amazon|us|the company|google|microsoft)|our (benefits|culture|values|mission)|privacy|"
                  r"accommodations?|work authorization|how we hire|why join|apply now|share this job|similar jobs|"
                  r"related jobs|more jobs|other (jobs|openings|roles|positions)|you may also like|recommended jobs|"
                  r"back to search|view jobs?|locations?)\b", re.I)
SKIP_INLINE = re.compile(r"equal opportunity employer|reasonable accommodation|affirmative action|pay range|"
                         r"total compensation|privacy notice|cookie", re.I)
REQUIRED = re.compile(r"(basic|minimum|required)\s+(qualifications|skills|requirements)|^(required|requirements?)$|"
                      r"^requirements?\b|what you(?:'|’)ll need|what you will need|must have|^you have\b|^qualifications?\b", re.I)
PREFERRED = re.compile(r"preferred\s+(qualifications|skills|requirements)|nice to have|^bonus|^desired|^preferred|^plus\b", re.I)
DESCRIPTION = re.compile(r"responsibilities|job description|^description|what you(?:'|’)ll do|about the (role|team|job)|"
                         r"^the role|^overview|^key job", re.I)
INLINE_PREF = re.compile(r"\b(preferred|nice to have|a plus|bonus|desired)\b", re.I)
TITLE = re.compile(r"(engineer|developer|scientist|analyst|manager|intern|architect|sde|researcher)", re.I)
WEIGHT = {"required": 3.0, "preferred": 1.5, "description": 1.0}


def norm_key(s: str) -> str:
    return re.sub(r"[^a-z0-9+#]", "", s.lower())


def load_terms() -> list[dict]:
    return json.loads((ASSETS / "jd_terms.json").read_text(encoding="utf-8"))


def build_patterns(terms: list[dict]):
    by_name = {t["name"]: t for t in terms}
    pats = []
    for t in terms:
        for alias in [t["name"], *t.get("aliases", [])]:
            cs = bool(t.get("cs")) or len(alias) <= 3
            rx = re.compile(r"(?<![A-Za-z0-9+#])" + re.escape(alias) + r"(?![A-Za-z0-9+#])", 0 if cs else re.I)
            also = [by_name[n] for n in t.get("also", []) if n in by_name]
            pats.append((len(alias), t, also, rx))
    pats.sort(key=lambda p: -p[0])  # longest alias first so phrases win over their parts
    return pats


def find_matches(line: str, pats) -> list[dict]:
    claimed = [False] * len(line)
    hits: list[dict] = []
    for _, term, also, rx in pats:
        for m in rx.finditer(line):
            a, b = m.span()
            if any(claimed[a:b]):
                continue
            for i in range(a, b):
                claimed[i] = True
            hits.append(term)
            hits.extend(also)
    return hits


def guess_title(text: str) -> str:
    for line in [l.strip() for l in text.splitlines() if l.strip()][:5]:
        if len(line) < 140 and TITLE.search(line):
            return line
    return ""


def analyze(text: str, terms: list[dict]) -> dict:
    pats = build_patterns(terms)
    title = guess_title(text)
    stats: dict[str, dict] = {}

    def get(t: dict) -> dict:
        return stats.setdefault(t["name"], {"name": t["name"], "type": t.get("type", ""), "aliases": t.get("aliases", []),
                                            "count": 0, "required": 0, "preferred": 0, "description": 0,
                                            "in_title": False, "score": 0.0})

    for t in find_matches(title, pats):
        s = get(t)
        s["in_title"] = True
        s["score"] += 3
    mode = "description"
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line == title:
            continue
        heading = (not re.match(r"^[-•*·●▪\d]", line) and len(line) < 70
                   and (line.endswith(":") or len(line.split()) <= 6) and not re.search(r"[.;]$", line))
        if heading:
            if SKIP.search(line):
                mode = "skip"; continue
            if PREFERRED.search(line):
                mode = "preferred"; continue
            if REQUIRED.search(line):
                mode = "required"; continue
            if DESCRIPTION.search(line):
                mode = "description"; continue
        if mode == "skip" or SKIP_INLINE.search(line):
            continue
        seen: dict[tuple[str, str], list] = {}
        for clause in re.split(r";|\s[—–-]\s", line):
            line_mode = "preferred" if mode == "required" and INLINE_PREF.search(clause) else mode
            for t in find_matches(clause, pats):
                k = (t["name"], line_mode)
                seen[k] = [t, line_mode, (seen[k][2] if k in seen else 0) + 1]
        for t, line_mode, n in seen.values():
            s = get(t)
            occ = min(n, 2)
            s["count"] += n
            s[line_mode] += occ
            s["score"] += WEIGHT[line_mode] * occ
    out = list(stats.values())
    for s in out:
        s["priority"] = "high" if s["score"] >= 5 or (s["required"] > 0 and s["score"] >= 3) else "medium" if s["score"] >= 2 else "low"
    out.sort(key=lambda s: (-s["score"], s["name"]))
    return {"title": title, "terms": out}


def load_ledger(path: Path | None) -> tuple[set[str], set[str]]:
    """Return (claimable keys, gap keys). Missing ledger => nothing claimable, default gaps."""
    claimable: set[str] = set()
    gaps = {norm_key(g) for g in DEFAULT_GAPS}
    if not path or not path.exists():
        return claimable, gaps
    import yaml
    led = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    skills = led.get("skills") or {}
    for group, items in skills.items():
        if group == "weak_evidence":
            gaps |= {norm_key(str(x)) for x in items or []}
        elif isinstance(items, dict):
            for name, evidence in items.items():
                # evidence that is only 'education' (coursework) is not hands-on; treat as gap, not claimable
                if evidence and set(map(str, evidence)) <= {"education"}:
                    gaps.add(norm_key(name))
                elif evidence:
                    claimable.add(norm_key(name))
    return claimable, gaps


def classify(term: dict, claimable: set[str], gaps: set[str]) -> str:
    keys = {norm_key(term["name"]), *(norm_key(a) for a in term.get("aliases", []))}
    if keys & gaps:
        return "gap"
    for k in keys:
        if k in claimable or any(k and (k in c or c in k) and min(len(k), len(c)) >= 4 for c in claimable):
            return "claimable"
    return "unverified"


def build_draft(analysis: dict, claimable: set[str], gaps: set[str]) -> dict:
    required, preferred, hidden, tagged = [], [], [], []
    for t in analysis["terms"]:
        t["claim_status"] = classify(t, claimable, gaps)
        tagged.append(t)
        if t["required"] or t["in_title"]:
            required.append(t["name"])
        elif t["preferred"]:
            preferred.append(t["name"])
        elif t["description"]:
            hidden.append(t["name"])
    return {
        "source": "jd_prescan.py (deterministic draft; review before relying on it)",
        "role_title": analysis["title"],
        "required_skills": required, "preferred_skills": preferred, "hidden_keywords": hidden,
        "terms": tagged,
        "gaps_to_state_plainly": [t["name"] for t in tagged if t["claim_status"] == "gap"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jd", required=True, help="job description text file")
    ap.add_argument("--ledger", help="truth-base.yaml (adds claimable/gap tags)")
    ap.add_argument("--out", help="write draft jd-analysis JSON here")
    args = ap.parse_args()
    text = Path(args.jd).read_text(encoding="utf-8")
    claimable, gaps = load_ledger(Path(args.ledger) if args.ledger else None)
    draft = build_draft(analyze(text, load_terms()), claimable, gaps)
    blob = json.dumps(draft, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(blob, encoding="utf-8")
    print(f"role: {draft['role_title'] or '(unknown)'}")
    for label, key in (("required", "required_skills"), ("preferred", "preferred_skills"), ("hidden", "hidden_keywords")):
        print(f"{label:9}: {', '.join(draft[key]) or '-'}")
    print(f"GAPS (say so plainly, never claim): {', '.join(draft['gaps_to_state_plainly']) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
