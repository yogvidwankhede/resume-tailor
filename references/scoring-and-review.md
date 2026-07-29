# ATS Score Estimator & Recruiter Review

---

## Part A — ATS Score Estimator

### What the number is for

The score is a **diagnostic that produces a list**, not a grade. Its only real
output is: *these JD terms are missing from the resume.* For each one you then ask
the only question that matters — **is there a true statement that would naturally
contain this word?** If yes, rewrite a bullet. If no, leave it missing and report it.

A resume that scores 95 by listing tools the candidate hasn't used is worth less
than one that scores 72 honestly, because the first one fails at the interview and
costs the referral.

### Components

| Component | Weight | Measures |
|---|---|---|
| Required-term coverage | 40% | fraction of `required_skills` present, weighted by JD weight |
| Preferred-term coverage | 15% | fraction of `preferred_skills` present |
| Hidden-keyword coverage | 15% | fraction of `hidden_keywords` present |
| Evidence placement | 10% | fraction of required terms appearing in a *bullet*, not only the skills list |
| Parseability | 10% | headings, dates, single column, clean text extraction |
| Impact density | 10% | fraction of bullets containing a real number |

Run: `python scripts/ats_score.py --resume out/resume.txt --jd out/jd-analysis.json`
Add `--pdf out/resume.pdf` to include the extraction check.

### Bands

| Score | Reading |
|---|---|
| 85–100 | Strong keyword alignment. Remaining risk is human judgment, not filtering. |
| 70–84 | Will clear most filters. Check that the misses are genuine gaps, not vocabulary mismatches. |
| 55–69 | Borderline. Usually means required terms exist in the ledger but are phrased in the candidate's vocabulary rather than the employer's. Highest-return zone for rewriting. |
| <55 | Either a genuine mismatch, or the JD is for a different role family. Say so plainly. |

### Reporting rule

Always report the score **with** the missing-term table:

| Missing term | Weight | Ledger evidence? | Verdict |
|---|---|---|---|
| Airflow | 2.0 | adjacent (`euno.heartbeat`) | Bridge phrasing added; can't claim the tool |
| Kubernetes | 2.0 | none | Genuine gap — cover letter |
| "reliability" | 1.5 | `euno.heartbeat` monitoring | Added to bullet 3 |

Never report a bare number.

---

## Part B — Recruiter Review

Re-read the finished resume cold, as someone with ~20 seconds and 300 other
applications. The point of this stage is that keyword optimization and human
readability pull in opposite directions, and something has to check the second one.

### The rubric

**1. The 20-second scan.**
What are the first three things the eye lands on? (Usually: name, first job title,
the first bold thing in the top third.) Are those the three you'd have chosen for
this JD? If the first thing a reader sees is a degree when the JD wants shipping
experience, the section order is wrong.

**2. The title test.**
Cover everything below the halfway line. Can the target job title be inferred from
what's left? If not, the top third isn't working — usually the skills block labels
or the first role's first bullet.

**3. The "prove it" test.**
Which single line most invites *"walk me through that"*? Then check the ledger's
`defend:` field. If the candidate can't answer it, that line is a liability,
regardless of how good it looks.

**4. The credibility scan.**
Any claim that reads as inflated relative to the role's seniority and duration?
An intern who "architected the platform" in two months triggers doubt about
everything else on the page. Downgrade the verb, not the accomplishment.

**5. The cut test.**
What would you delete? There is always something. If the answer is "nothing", you
haven't read it critically enough — go back to the weakest bullet in the oldest role.

**6. The rejection reason.**
State bluntly, in one sentence, the most likely reason this resume gets passed
over. Not to be discouraging — this is the item the cover letter or the outreach
note has to address.

### The verdict

End with one of:

- **strong fit** — required coverage is direct, nothing material absent
- **worth applying** — a few adjacent/absent items, none of them dealbreakers
- **stretch** — several required items absent, or a seniority mismatch of one level
- **misaligned** — dealbreaker present (sponsorship, clearance, location, licence)
  or a different role family

An honest "stretch" is more useful than a flattering score. If the verdict is
`misaligned`, say it in the first line of the report and explain why, rather than
burying it after 400 words of optimization.

### Output shape

```markdown
## Recruiter Review

**20-second scan lands on:** …
**Title inferable from top third:** yes / no — because …
**Most likely "prove it":** "…" → defensible / risky because …
**Credibility flags:** …
**I would cut:** …
**Most likely rejection reason:** …

**Verdict: worth applying** — direct coverage on 7/9 required items; Kubernetes and
Airflow are genuine gaps but neither is listed as a hard requirement.
```
