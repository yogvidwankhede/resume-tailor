# Evaluation Checklist

Run before delivering anything. A failure in Part A is a blocker; Parts B–E are
quality gates.

---

## A. Truth (blocking)

```
[ ] scripts/verify_truth.py exits 0
[ ] Every number in the output appears in truth-base.yaml
[ ] Every employer, title, degree, date range matches the ledger exactly
[ ] Every skill listed has an `evidence` entry
[ ] Every metric is attributed to the mechanism that produced it
[ ] No forbidden_claims entry appears, in any paraphrase
[ ] No tool named in the JD but absent from the ledger appears anywhere
[ ] Publications and links resolve to the ledger's URLs
[ ] Unresolved `conflict:` items are flagged in the report, not silently resolved
```

If any line fails, fix the **resume**, not the ledger — unless the user confirms a
real fact was missing.

---

## B. Content

```
[ ] Every bullet is verb-first
[ ] No banned constructions (writing-rules.md § 11)
[ ] Every bullet carries a metric, a mechanism, or a stated consequence
[ ] One claim per bullet
[ ] Bullet #1 of each role is that role's strongest JD-relevant claim
[ ] Tense: present for current role, past for all ended roles, consistent within each
[ ] No verb repeated within a role
[ ] Skills rows are ≤8 items, labels tailored to the JD
[ ] Project titles lead with the capability the JD cares about
[ ] Summary present only if Stage 8's conditions were met
```

---

## C. ATS

```
[ ] Every high-weight required term appears 1–2 times
[ ] At least one appearance of each required term is in a bullet, not only in SKILLS
[ ] No term appears 3+ times (stuffing)
[ ] Spelling variants mirror the posting
[ ] Standard section headings
[ ] Dates parseable and consistently formatted
[ ] Single column; no text boxes, header/footer content, or images
[ ] pdftotext extracts ligature words whole (artificial, certification, classifier,
    efficiency, workflow, fine-tuned)
[ ] pdftotext output is in reading order
[ ] Filename is Firstname_Lastname_Role.pdf
[ ] File format matches what the posting asked for
```

---

## D. Layout (if a PDF was built)

```
[ ] Exactly 1 page (check the LaTeX log's "Output written on … (1 page")
[ ] No Overfull \hbox over ~15pt
[ ] measure_layout.py shows all section headings at the same leftx
[ ] Body font is 9.5pt or larger
[ ] Last ink band lands near the bottom margin — page full but not overflowing
[ ] Links are clickable and unboxed
```

---

## E. Deliverables

```
[ ] out/resume.txt written and sent
[ ] out/resume.md written
[ ] out/resume.tex + resume.pdf written (if requested)
[ ] out/tailoring-report.md contains: gap table, ATS score + missing-term table,
    recruiter review, verdict, before→after change log, absent list, open questions
[ ] The response ends with the verdict and the absent list, not with a summary of
    how good the resume is
```

---

## Self-critique pass

Before sending, reread the output once with these three questions:

1. **Which line would I be least able to defend in an interview?** If there is one,
   it's the wrong line.
2. **If I only read the top third, what job does this person do?** If the answer
   isn't the target job, the ordering is wrong.
3. **What did I cut, and can I justify each cut?** If nothing was cut, the resume
   probably wasn't tailored — it was reformatted.
