#!/usr/bin/env python3
"""output_name.py — Firstname_Lastname_Resume_Company file base, e.g. Yogvid_Wankhede_Resume_Study.com"""
import argparse
import re
import sys
import unicodedata


def part(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9.]+", "-", s).strip("-.")
    return re.sub(r"\.{2,}", ".", s)


def file_base(name: str, company: str = "", kind: str = "Resume") -> str:
    words = name.split()
    who = [words[0], words[-1]] if len(words) > 1 else words
    return "_".join(p for p in [*(part(w) for w in who), kind, part(company) if company else ""] if p)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--company", default="")
    ap.add_argument("--kind", default="Resume", help="Resume or CoverLetter")
    a = ap.parse_args()
    print(file_base(a.name, a.company, a.kind))
    sys.exit(0)
