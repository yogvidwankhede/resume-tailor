---
name: resume-tailor
description: Tailor a resume to a specific job description without fabricating anything — analyze the JD, run a gap analysis against a verified fact ledger, rewrite bullets into quantified impact statements, reorder and regroup skills, generate a targeted summary, estimate ATS compatibility, run a recruiter critique, and emit a submission-ready one-page resume in TXT/Markdown/LaTeX/PDF. Use this skill whenever the user pastes or links a job posting, says "tailor my resume", "optimize my resume for this role", "make my resume ATS-friendly", "will this pass the ATS", "rewrite these bullets", "score my resume against this job", "should I apply", or asks for a resume, CV, cover-letter-adjacent summary, or LaTeX resume build — even if they don't say the word "tailor". Also use it when the user asks to add a new job, project, or metric to their resume, since the fact ledger must be updated first.
license: Complete terms in LICENSE.txt
---

# Resume Tailor

A truth-constrained resume optimization engine. It takes (1) a verified inventory of what
the candidate has actually done and (2) a job description, and produces a resume that reads
as if it were written for that job — while every single claim on the page remains defensible
in an interview.

The whole skill rests on one asymmetry: **rewriting is free, inventing is fatal.** A recruiter
who catches one fabricated line discards the entire document, and every number on the page is
a question the candidate has volunteered to answer. So the engine is built to be aggressive
about emphasis, ordering, vocabulary, and compression — and absolutely rigid about facts.

---

## The two inputs

**1. The Truth Ledger.** The candidate's complete factual inventory: roles, dates, employers,
metrics, tools, projects, publications, links. Nothing may appear in an output resume that
is not traceable to a ledger entry.

- Default ledger: `assets/truth-base.yaml` (+ human-readable `references/truth-base.md`)
- If the user supplies their own resume/LinkedIn/GitHub instead, build a ledger from it
  first (see *Stage 0*) — never skip straight to tailoring.

**2. The Job Description.** Pasted text, a URL, or a screenshot. If only a job title is given,
say so and either ask for the posting or work from an explicitly-labelled generic role profile.

---

## The canonical template

`assets/resume-master.txt` is the canonical structure. It defines section ordering, bullet
grammar, density, and the plaintext form an ATS actually sees. `assets/resume-master.tex` is
the same document in the tuned LaTeX build. **The TXT is the source of truth for content; the
TEX is the source of truth for layout.** Anything generated should follow the TXT template
unless a specific tailoring decision requires deviating — and when it does, say which rule was
broken and why.

Canonical section order (do not reorder without a stated reason):

```
HEADER  →  EDUCATION  →  SKILLS  →  EXPERIENCE  →  PROJECTS
```

Reordering rules live in `references/writing-rules.md` § Section ordering. Short version:
Education leads while the candidate is a student or <2 years out; the moment industry
experience outweighs the degree, Experience moves above Education. A Summary is added only
when the JD demands a pivot the bullets can't carry alone.

---

## The pipeline

Eleven stages. Run them in order — later stages depend on earlier artifacts. For a quick
"just fix these three bullets" request, run stages 2, 3, 5 only and say that you did.

| # | Stage | Output artifact |
|---|---|---|
| 0 | Ledger build / verification | `truth-base.yaml` |
| 1 | Resume Analyzer | baseline diagnosis |
| 2 | JD Analyzer | `jd-analysis.json` |
| 3 | Gap Analysis | gap table |
| 4 | Tailoring Engine | selection + ordering plan |
| 5 | Bullet Rewriter | rewritten bullets |
| 6 | Project Optimizer | project selection + rewrites |
| 7 | Skills Optimizer | regrouped skills block |
| 8 | Summary Generator | 2–3 line summary (conditional) |
| 9 | ATS Score Estimator | score + missing-term list |
| 10 | Recruiter Review | 20-second-scan critique |
| 11 | Final Generator | resume.txt / .md / .tex / .pdf |

### Stage 0 — Ledger build / verification

Read `assets/truth-base.yaml`. If the user is not the default candidate, or supplies new
material, extract every role, date range, employer, metric, tool, link, and project into the
same schema. Flag conflicts rather than picking silently — the default ledger already carries
`conflict:` markers where two source documents disagree (e.g. TA start date). Ask the user to
resolve conflicts that affect the output; carry unresolved ones forward as flags.

Also load `references/truth-base.md` for the narrative context behind the numbers — which
metric came from which mechanism, which claims were tested and rejected, what each number
commits the candidate to defending.

### Stage 1 — Resume Analyzer

Diagnose the current resume before touching it. Report, concretely:

- **Weak bullets** — responsibility-shaped ("Responsible for…", "Worked on…"), unquantified,
  or ending at the output without stating the outcome.
- **Buried leads** — the strongest bullet in a role sitting third.
- **Density problems** — a bullet over ~2.2 lines at 9.5pt, or a role with 5+ bullets when a
  more recent role has 2.
- **Stale framing** — vocabulary from a previous target role still sitting in the document.
- **Ledger drift** — anything on the resume that is *not* in the ledger. This is a bug: either
  the ledger is incomplete or the resume contains an unverified claim. Resolve before proceeding.

### Stage 2 — JD Analyzer

Extract into `assets/schemas/jd-analysis.schema.json` shape. Full taxonomy and extraction
heuristics: **read `references/jd-analysis.md`.** Extract at minimum:

- `required_skills` / `preferred_skills` (separate them — the "Requirements" vs "Nice to have"
  split drives ranking weight)
- `hidden_keywords` — terms that recur in the *responsibilities* prose but never appear in the
  requirements list. These are the highest-leverage words in the posting because they are what
  the hiring manager actually thinks about, and most applicants only mirror the bullet list.
- `responsibilities`, `seniority`, `industry`, `company_stage`
- `ats_terms` — exact-string forms the parser will look for, including the spelling variants
  the JD itself uses ("CI/CD" vs "CICD", "Postgres" vs "PostgreSQL")
- `soft_skills` and the phrases that signal them
- `dealbreakers` — clearance, location, degree, years-of-experience floors
- `vocabulary_fingerprint` — the employer's own house words. Mirroring these is the single
  highest-return move in the whole pipeline, and it is free of fabrication risk *as long as a
  true statement already supports the word.*

### Stage 3 — Gap Analysis

Produce a table with one row per JD requirement:

| JD requirement | Ledger evidence | Status | Action |
|---|---|---|---|

Status ∈ `{direct, adjacent, transferable, absent}`.

- **direct** — the ledger names it. Surface it, use the JD's spelling.
- **adjacent** — a near neighbour (JD wants Airflow; ledger has Cloud Scheduler → Cloud Run →
  Cloud Tasks orchestration). Describe the real thing in language that makes the adjacency
  legible. Never write the JD's tool name as if it were used.
- **transferable** — different domain, same underlying skill (imbalanced-class fraud detection
  ← imbalanced-class intrusion detection). Reframe honestly; the underlying method is the claim.
- **absent** — say so, out loud, in the report. Do not paper over it. Absent items become the
  "what to learn / what to address in the cover letter" list, and if enough required items are
  absent, the honest recommendation is that this is a stretch application.

Full decision rules and worked examples: `references/gap-analysis.md`.

### Stage 4 — Tailoring Engine

Decide what goes on the page and in what order, before writing a word.

1. **Rank every ledger item** by relevance to the JD (direct hits > adjacent > transferable).
2. **Allocate space.** One page. Roughly: the most relevant role gets 3 bullets, others 2,
   the least relevant 1–2. Projects get 2–3 entries totalling 4–6 bullets.
3. **Order within each role** so bullet #1 is the strongest JD-relevant claim. Recruiters read
   the first bullet of each role and skim the rest.
4. **Choose what to cut.** Cutting is the mechanism that buys readability — see the formatting
   philosophy in `references/latex-formatting.md`: *cut content, never shrink the font below
   9.5pt.*
5. **Set the vocabulary map** — for each ledger concept, the JD's word for it (only where true).

### Stage 5 — Bullet Rewriter

The bullet grammar, the verb bank, the quantification ladder, and the STAR-compression pattern
live in `references/writing-rules.md`. **Read it before rewriting.** The core shape:

```
[Strong verb] [what you built/changed] [with what mechanism] → [quantified outcome] [for whom / why it mattered]
```

Non-negotiables enforced here:

- The metric must be attributed to the mechanism that actually produced it. Writing
  "implemented evals to cut inference cost 40%" when token budgeting cut the cost is a
  **false-causality fabrication** even though both facts are true. This is the most common way
  a truthful writer accidentally lies.
- Present tense for current roles, past for ended roles. Consistently.
- No adjective inflation ("comprehensive", "cutting-edge", "robust") in place of a number.
- One bullet, one claim. If it has two "and"s, it is two bullets or one cut.

### Stage 6 — Project Optimizer

Projects are the most malleable section — pick the 2–3 that map hardest onto the JD, retitle
them to lead with the *capability* rather than the toy name, and rewrite bullets against the
target role's concerns. A project title is prime keyword real estate: `HealthMate-AI: Retrieval
System with Domain-Adapted Embeddings for High-Stakes Decision Support` and `HealthMate-AI: RAG
System for Medical Decision Support` are the same project aimed at two different jobs.

Selection rules and the full project inventory: `references/gap-analysis.md` § Project selection.

### Stage 7 — Skills Optimizer

Reorder and regroup, never invent. Rules:

- Group *labels* are tailored, not just contents. A JD for an LLM platform role wants to see
  a row literally called `LLM & Agent Frameworks`; a data-analytics JD wants `Statistics &
  Modeling`. The label is itself a keyword.
- The first row and the first item in each row are the highest-value slots — put the JD's
  required stack there.
- 5 rows is the density sweet spot at 9.5pt. 6 rows forces the body font down and costs more
  than it gains. If a 6th row is needed, merge two weak ones instead.
- Drop tools that neither the JD nor the candidate's own bullets support. Every unsupported
  skill dilutes keyword density and invites an interview question with no good answer.

### Stage 8 — Summary Generator

Default: **no summary.** For a one-page early-career resume, a summary usually costs 3 lines
that a third experience bullet would spend better. Add one only when:

- the JD requires a pivot the bullets can't make obvious on their own,
- there's a career-change / non-obvious domain jump to explain, or
- the user asks.

When included: 2–3 lines, no first person, no "results-driven professional". Structure —
`[what you are] + [the two most JD-relevant proof points, with numbers] + [what you're aiming at].`

### Stage 9 — ATS Score Estimator

Run `scripts/ats_score.py` on the generated plaintext + `jd-analysis.json`. It reports coverage
of required terms, preferred terms, and hidden keywords, plus a parseability check. The number
is a *diagnostic*, not a grade — its job is to produce the list of missing terms so you can ask:
*is there a true statement that would naturally contain this word?* If yes, rewrite. If no,
leave it missing and note it.

Scoring bands, weighting, and the parseability rules: `references/scoring-and-review.md`.

### Stage 10 — Recruiter Review

Re-read the output cold, as a recruiter with ~20 seconds and 300 other resumes. Answer:

- What are the first three things the eye lands on? Are they the three you'd choose?
- Can the target job title be inferred from the top third of the page alone?
- Which single line is most likely to trigger "prove it" — and can the candidate?
- What's the most likely rejection reason, stated bluntly?
- What would you cut?

Then state the verdict: `strong fit` / `worth applying` / `stretch` / `misaligned`, with the
reason. An honest "stretch" is more useful than a flattering score.

### Stage 11 — Final Generator

Emit in this order, always:

1. **`resume.txt`** — the canonical plaintext. This is what the ATS reads; it is the deliverable
   that must be right.
2. **`resume.md`** — readable review copy.
3. **`resume.tex`** — only when the user wants the typeset version. Build rules, the exact
   spacing knobs, and the one-page fitting procedure are in `references/latex-formatting.md`.
   The ATS-safety preamble lines (`cmap`, `fontenc`, `lmodern`) are load-bearing and must never
   be dropped — without them PDF text extraction can turn "Artificial Intelligence" into
   "Articial" on the older extractors many ATS products still ship, and the failure is silent.
4. **`tailoring-report.md`** — gap table, ATS score, recruiter review, the change log
   (every rewritten line, before → after), and the **unresolved / absent list**.

Then run the verifier before showing anything:

```bash
python scripts/verify_truth.py --resume out/resume.txt --ledger assets/truth-base.yaml
```

It fails on any number, employer, date, tool, or link in the output that has no ledger
counterpart. **A failing verify is a blocker, not a warning.** Fix the resume, not the ledger —
unless the user confirms the ledger was genuinely missing a real fact.

---

## The fabrication line

The engine may **reorder, reframe, compress, expand, requantify from real data, retitle,
regroup, and translate into the employer's vocabulary.**

It may never invent an employer, a date, a title, a degree, a certification, a tool the
candidate hasn't used, a metric that wasn't measured, a causal link that didn't hold, or a
scope that didn't exist.

Borderline cases and how they were adjudicated in practice — including a catalogue of real
suggestions from commercial resume-scoring tools that were **rejected for being lies** — are in
`references/edge-cases.md`. Read it when tempted. The catalogue exists because automated resume
advice reliably suggests fabrication in a confident, helpful tone, and the pattern is worth
recognizing: *"framing your work as being for government agencies aligns better with the role"*
is a scoring tool telling you to lie.

When a rewrite would require a fact the ledger doesn't have, do one of these — in this order:

1. Find a true adjacent claim that serves the same purpose.
2. Ask the user a specific question ("did you actually write the runbooks, or just the code?")
   and use the answer. Many gaps are real experience that never made it into the ledger.
3. Leave the gap, and put it in the report's absent list.

Never quietly split the difference.

---

## Reference map

Read on demand — don't load everything up front.

| File | Read when |
|---|---|
| `references/truth-base.md` | Always, at Stage 0 — the fact ledger in narrative form |
| `references/jd-analysis.md` | Stage 2 — extraction taxonomy, hidden-keyword heuristics |
| `references/gap-analysis.md` | Stage 3–4, 6 — status rules, project selection |
| `references/writing-rules.md` | Stage 5, 7, 8 — bullet grammar, verb bank, quantification |
| `references/ats-guidelines.md` | Stage 9, 11 — parser behaviour, keyword density, file format |
| `references/latex-formatting.md` | Stage 11 — layout knobs, one-page fitting, ATS preamble |
| `references/scoring-and-review.md` | Stage 9–10 — scoring bands, recruiter rubric |
| `references/edge-cases.md` | Any time a rewrite feels like it needs a fact you don't have |
| `references/prompt-engineering-notes.md` | Extending or debugging the skill itself |
| `references/evaluation-checklist.md` | Before delivering — the pre-flight checklist |
| `examples/` | Three end-to-end worked runs against real JD archetypes |

## Output contract

Always deliver files, not chat-only text. Always deliver `resume.txt` and
`tailoring-report.md` at minimum. Always end the response with the honest verdict and the
absent list — the parts the user needs to act on are the gaps, not the compliments.
