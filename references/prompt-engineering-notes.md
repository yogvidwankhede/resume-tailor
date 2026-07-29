# Prompt Engineering Notes

Design notes for whoever extends, debugs, or ports this skill. These record *why*
the skill is shaped the way it is, so the structure survives editing.

---

## 1. Why a ledger instead of "here's my resume"

The obvious design is: give the model the old resume and the JD, ask for a new
resume. It fails in a specific, predictable way — the model treats the old resume
as a *style sample* rather than a *fact boundary*, and interpolates. Given a JD
mentioning Airflow and a resume mentioning Cloud Scheduler, an unconstrained
rewrite will eventually produce "orchestrated data pipelines with Airflow." Not
from malice; from pattern completion.

Separating **facts** (`truth-base.yaml`) from **form** (`resume-master.txt`) makes
the boundary explicit and, critically, **machine-checkable** — which is what
`verify_truth.py` exploits. The verifier is only possible because the facts live
in a structured file.

Design principle: *if you want a model to not invent things, give it a place where
the true things live and a checker that compares against it.* Instructions alone
degrade over long generations; a diff doesn't.

---

## 2. Why the pipeline is staged rather than one prompt

A single "tailor this resume" prompt produces a plausible resume and no reasoning
you can inspect. Staging buys three things:

- **Inspectable intermediate artifacts.** The gap table is often more useful to the
  user than the resume — it tells them what to learn and what to say in the
  interview.
- **Ordering discipline.** Selection (Stage 4) happens *before* writing (Stage 5).
  Without that separation the model writes beautiful bullets for the wrong roles
  and then can't bear to cut them. Deciding what goes on the page while it's still
  a list is much cheaper than deciding after it's prose.
- **Failure localization.** A bad output is traceable to a stage.

The cost is verbosity. Mitigation: the SKILL.md explicitly authorizes running
stages 2/3/5 only for narrow requests.

---

## 3. Why `defend:` and `mechanism:` fields exist

`mechanism:` exists because the most common accidental fabrication is
false causality — attributing a real number to the wrong real cause. A model
generating "implemented evals to cut cost 40%" is doing associative composition of
two true facts. Storing the cause *with* the metric makes the error checkable and
gives the writing rules something concrete to point at.

`defend:` exists because a resume is a set of interview commitments. Writing the
question next to the claim makes the cost of each number visible at authoring
time, and doubles as interview prep in the report.

---

## 4. Why `forbidden_claims` is in the ledger

Negative examples are more instructive than positive ones for this task, because
the failure mode is *plausible* output, not obviously wrong output. A list of nine
specific rejected rewrites, each with a one-line reason, teaches the shape of the
error far better than "don't fabricate."

It also creates a feedback loop: every time a real rewrite is caught and rejected,
it should be appended. The catalogue is the skill's memory.

---

## 5. Why hidden keywords are weighted so heavily

Requirements lists are template-generated and near-universal within a role family
("Python, SQL, communication skills"). Every applicant matches them, so they carry
almost no differentiating information. The responsibilities prose is written by the
hiring manager and contains the words they actually think in. Matching those is
what produces the "this person read the posting" reaction.

This is also the safest optimization available, because it changes vocabulary
rather than facts — provided the true-statement precondition holds.

---

## 6. Instruction-design choices

- **Imperative voice throughout.** "Extract", "Rank", "Cut" — not "you should
  consider extracting."
- **Reasons attached to rules.** `writing-rules.md` explains *why* mechanism
  clauses matter rather than just mandating them, because a rule with a reason
  generalizes to cases the rule didn't anticipate.
- **Tables for lookup, prose for judgment.** Verb banks and status taxonomies are
  tables. Anything requiring a decision is prose with a worked example.
- **Worked examples over abstract schemas** at every decision point. The
  adjacent-phrasing table in `gap-analysis.md` does more work than a paragraph
  describing what adjacency means.
- **Progressive disclosure.** SKILL.md stays under ~300 lines and routes to
  references. Loading all ~2500 lines of reference material for a "fix this bullet"
  request would crowd out the actual work.
- **A hard failure at the end.** `verify_truth.py` exiting non-zero is a blocker.
  Soft warnings get rationalized away over a long generation; an exit code doesn't.

---

## 7. Known limitations

- **`verify_truth.py` is lexical.** It catches invented numbers, employers, dates,
  and links. It cannot catch a semantically false rearrangement of true tokens
  (a false-causality bullet built entirely from ledger vocabulary will pass).
  Stage 10's credibility scan is the human-judgment backstop; treat the verifier as
  a floor, not a ceiling.
- **ATS score is a model, not a measurement.** Real systems vary widely and are
  opaque. The score's value is the missing-term list.
- **The ledger goes stale.** Every new job, project, or metric must be added or the
  skill quietly optimizes against an outdated candidate. Any "add X to my resume"
  request is a ledger-update request first.
- **Hidden-keyword extraction is frequency-based** and will miss a
  once-mentioned but load-bearing term. Read the responsibilities block yourself.
- **One-page assumption** is baked into space budgeting. Senior and academic
  targets need the edge-case guidance instead.

---

## 8. Porting to another candidate

1. Replace `assets/truth-base.yaml` — keep the schema, including `mechanism:`,
   `defend:`, `conflict:`, and `forbidden_claims`.
2. Regenerate `assets/resume-master.txt` from their actual best resume; keep the
   slot-inventory section at the bottom.
3. Keep `references/writing-rules.md`, `jd-analysis.md`, `ats-guidelines.md`,
   `scoring-and-review.md` unchanged — they're candidate-independent.
4. Rewrite `references/truth-base.md`'s narrative and the `forbidden_claims` list;
   these are the parts that carry candidate-specific judgment.
5. Update `examples/` with two or three runs against that candidate's real target
   roles. Generic examples teach much less than real ones.
