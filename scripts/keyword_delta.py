#!/usr/bin/env python3
"""
keyword_delta.py — weighted keyword coverage before vs after tailoring.

    python scripts/keyword_delta.py --prescan out/jd-prescan.json --before master.tex --after tailored.tex

Counts the JD's weighted terms that literally appear in the resume text, the way a keyword scan would.
A guide, not a guarantee. Terms tagged `gap` in the prescan are reported separately and excluded from the
percentage ceiling, because the honest answer for them is to say so, not to add the word.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def plain_text(tex: str) -> str:
    body = tex[tex.index("\\begin{document}"):] if "\\begin{document}" in tex else tex
    body = "\n".join(re.sub(r"(^|[^\\])%.*$", r"\1", l) for l in body.split("\n"))
    body = re.sub(r"\\(?:textbackslash|textasciitilde|textasciicircum)\{\}", " ", body)
    body = re.sub(r"\\([&%$#_{}])", r"\1", body)
    body = re.sub(r"\\[a-zA-Z@]+\*?", " ", body)
    return re.sub(r"[{}\\~^]", " ", body)


def present(text: str, names: list[str]) -> bool:
    for a in names:
        flags = 0 if len(a) <= 3 else re.I
        if re.search(r"(?<![A-Za-z0-9+#])" + re.escape(a) + r"(?![A-Za-z0-9+#])", text, flags):
            return True
    return False


W = {"required": 3.0, "preferred": 1.5, "description": 1.0}


def weight(t: dict) -> float:
    return max(t.get("score", 0.0), 0.0) or 1.0


def coverage(terms: list[dict], text: str) -> dict:
    total = got = 0.0
    found, missing = [], []
    for t in terms:
        w = weight(t)
        total += w
        if present(text, [t["name"], *t.get("aliases", [])]):
            got += w
            found.append(t["name"])
        else:
            missing.append(t["name"])
    return {"pct": round(100 * got / total) if total else 0, "found": found, "missing": missing}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prescan", required=True)
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    pre = json.loads(Path(a.prescan).read_text(encoding="utf-8"))
    scored = [t for t in pre["terms"] if t.get("claim_status") != "gap"]
    gaps = [t["name"] for t in pre["terms"] if t.get("claim_status") == "gap"]
    b = coverage(scored, plain_text(Path(a.before).read_text(encoding="utf-8")))
    c = coverage(scored, plain_text(Path(a.after).read_text(encoding="utf-8")))
    res = {"before_pct": b["pct"], "after_pct": c["pct"], "added": sorted(set(c["found"]) - set(b["found"])),
           "lost": sorted(set(b["found"]) - set(c["found"])), "still_missing": c["missing"], "gaps_not_claimed": gaps}
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"keyword coverage: {res['before_pct']}% -> {res['after_pct']}%")
        print(f"added : {', '.join(res['added']) or '-'}")
        print(f"lost  : {', '.join(res['lost']) or '-'}")
        print(f"still missing (claimable/unverified; only add if a TRUE statement exists): {', '.join(res['still_missing']) or '-'}")
        print(f"gaps (stated plainly, never claimed): {', '.join(gaps) or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
