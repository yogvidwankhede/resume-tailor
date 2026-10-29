---
name: resume-tailor
description: Tailor a resume and cover letter to a specific job description without fabricating anything — analyze the JD, run a gap analysis against a verified fact ledger, rewrite bullets into quantified impact statements, reorder and regroup skills, retitle projects for the target role, estimate ATS compatibility, run a recruiter critique, and emit a submission-ready one-page resume as .tex and .pdf. Entry-level framing and no Professional Summary by default. Use this skill whenever the user pastes or links a job posting, says "tailor my resume", "optimize my resume for this role", "make my resume ATS-friendly", "will this pass the ATS", "rewrite these bullets", "score my resume against this job", "should I apply", or asks for a resume, CV, cover-letter-adjacent summary, or LaTeX resume build — even if they don't say the word "tailor". Also use it when the user asks to add a new job, project, or metric to their resume, since the fact ledger must be updated first.
license: Complete terms in LICENSE.txt
---

# Resume Tailor

## CORE DIRECTIVE — read and apply this before doing anything else

This block is the skill's default operating behaviour on **every** invocation, for **every**
task, whether or not the user restates it. It is not a guideline and not a preset. It applies
unless the user explicitly overrides a specific rule in the current request; an override of one
rule leaves the others in force.

**1. Entry-level framing is the default.**
Target the posting as an early-career candidate. Use build/ship/implement verbs over
scope-ownership verbs unless the ledger genuinely supports ownership. Education leads. Projects
carry real weight. Never inflate a title, a team size, or a scope. Over-claiming at this career
stage is the fastest way to lose credibility on the whole page.

**2. Never include a Professional Summary.**
No summary, objective, profile, or "About" block, in any form, under any heading. Stage 8 of the
pipeline is **disabled by default**. Those lines go to a third experience bullet instead. Only
generate a summary if the user asks for one by name in the current request.

**3. Deliver `.tex` and `.pdf` only.**
The deliverables are exactly: `resume.tex`, `resume.pdf`, and — whenever a cover letter is
requested or the posting expects one — `cover_letter.tex`, `cover_letter.pdf`. Do not deliver
`.txt`, `.md`, `.json`, tailoring reports, gap tables, change logs, or scratch files. Those
artifacts are still **produced internally** because later stages depend on them; they are simply
not surfaced. Compile every `.tex` to `.pdf` before delivering — a `.tex` without its `.pdf` is
an incomplete deliverable.

**4. Respond with the files, not with prose.**
No walkthrough of what was changed, no section-by-section rationale, no summary of the
optimization. Deliver the files and stop. The **one** exception, which overrides this rule
because accuracy outranks brevity: if `verify_truth.py` fails, or an unresolved ledger
`conflict:` affects something on the page, or a JD requirement is genuinely absent in a way that
changes whether the application is worth submitting — say so in a few lines. Silence about a
factual problem is not concision, it is a defect.

**5. Maximize alignment with the specific posting.**
Every section is optimized against the JD, not merely formatted: skills rows relabelled and
reordered to the posting's own categories, projects selected and retitled for this role, bullets
reordered so the strongest JD-relevant claim leads each entry, the employer's vocabulary mirrored
wherever a true statement already supports the word, and the JD's exact spelling used for every
ATS term. Hidden keywords — the words recurring in the responsibilities prose but absent from the
requirements list — are extracted and worked in. Treat every application as the highest-priority
one.

**6. Cover letters carry no dashes and must not read as machine-written.**
No em dashes, no en dashes, no dash-as-pause. Hyphens inside real compound words stay. Avoid the
banned vocabulary and the banned sentence shapes, use contractions, vary sentence length hard,
include one concrete detail only this candidate could write, and state one limitation plainly.
Full rules in Stage 8b.1 and 8b.2 — read them before drafting any letter.

**7. Truthfulness is absolute and outranks rules 5 and 6.**
Reorder, reframe, compress, requantify from real data, retitle, regroup, and translate into the
employer's vocabulary — freely. Never invent an employer, date, title, degree, certification,
tool, metric, causal link, or scope. Never attribute a real metric to a mechanism that did not
produce it. When maximizing alignment would require a fact the ledger lacks, find a true adjacent
claim, ask the user a specific question, or leave the gap — never split the difference. Voice
rules govern how a true thing is said, never what is said. Run `verify_truth.py` before
delivering; a non-zero exit is a blocker, not a warning.

---

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
experience outweighs the degree, Experience moves above Education. **No Summary** — Core
Directive rule 2 removes it unconditionally.

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
| 8 | Summary Generator | **disabled by default** (Core Directive 2) |
| 8b | Cover Letter | `cover_letter.tex` (when requested) |
| 9 | ATS Score Estimator | score + missing-term list |
| 10 | Recruiter Review | 20-second-scan critique |
| 11 | Final Generator | `resume.tex` + `resume.pdf` (+ cover letter pair) |

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

**Start with the deterministic pre-scan** (no judgment, so it never drifts):
`python scripts/jd_prescan.py --jd jd.txt --ledger <truth-base.yaml> --out out/jd-prescan.json`.
It weights terms by where they appear (title, Required, Preferred, description), skips EEO/benefits
boilerplate, and tags each term `claimable` / `gap` / `unverified` against the ledger. Treat it as a
draft: review it, then fill the full schema below. Every `gap` term is stated plainly in the cover
note and is never added to the resume. Detection never grants a skill.

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

### Stage 8 — Summary Generator — DISABLED BY DEFAULT

Core Directive rule 2 disables this stage. Produce no summary, objective, profile, or "About"
block. The lines it would have cost go to a third experience bullet, which carries evidence
instead of assertion.

Run this stage **only** when the user asks for a summary by name in the current request. If they
do: 2–3 lines, no first person, no "results-driven professional" — structure it as
`[what you are] + [the two most JD-relevant proof points, with numbers] + [what you're aiming at].`

### Stage 8b — Cover Letter

Run whenever a cover letter is requested or the posting expects one. Build it from
`assets/cover-letter-master.tex`, which shares the resume's font, margins, and ATS preamble so
the pair reads as one application.

Four paragraphs, under one page, no filler:

1. **The hook.** The role by name, and the single strongest piece of evidence that you can do it —
   a specific number from the ledger, not an adjective. No "I am writing to apply for."
2. **The proof.** Two or three sentences on the work that maps hardest onto the posting's
   responsibilities. Same facts as the resume, different register: the resume states the result,
   the letter explains the decision behind it. Do not restate bullets verbatim.
3. **The gap, addressed.** This is what makes a cover letter worth reading. Take the strongest
   `adjacent` or `absent` item from the gap analysis and address it in one honest sentence — what
   you have done that is closest, and that you know the difference. This paragraph is where an
   entry-level application earns trust that a resume alone cannot.
4. **The company, specifically.** One thing about this employer that is real and checkable — from
   the posting, their docs, their product. Generic praise is worse than omitting the paragraph.

Rules: no "I believe I would be a great fit", no restating the resume, no adjective inflation,
and every claim traceable to the ledger exactly as in the resume. `verify_truth.py` runs against
the cover letter too.

#### 8b.1 — No dashes

The cover letter contains **no em dashes (—) and no en dashes (–)**, and no dash used as a
parenthetical or a dramatic pause. This is the single most recognizable machine-writing tell, and
a letter free of it reads noticeably more like a person typed it.

Recast instead of substituting. A dash almost always marks a place where two thoughts were welded
together; splitting them usually improves the sentence anyway.

- dash as pause → full stop, and start a new sentence
- dash as aside → commas, or move the aside into its own sentence
- dash as "namely" → colon, or just say it directly
- dash pair as brackets → commas, or cut the aside entirely

Hyphens **inside real compound words stay** — `cost-aware`, `6-stage`, `fine-tuned`, `sub-$0.002`.
Removing those would be a misspelling, not a style choice. The rule is about dashes as
punctuation, not hyphens as spelling. Also avoid the slash-as-conjunction (`design/build`) for the
same reason.

#### 8b.2 — Write like a person, not a model

Machine-written prose fails in consistent, recognizable ways. Avoid each of these deliberately:

**Banned words and phrases.** delve, leverage, robust, landscape, realm, testament, underscore,
pivotal, meticulous, seamless, spearheaded, showcase, tapestry, resonate, navigate (figurative),
foster, myriad, plethora, "in today's fast-paced", "it's not just X, it's Y", "I am writing to
apply for", "I was excited to see", "I believe my background makes me", "passionate about",
"proven track record", "align perfectly with", "I would love the opportunity to", "eager to
contribute", "at the intersection of", "deep dive", "unlock", "empower", "journey".

**Banned shapes.**
- The rule of three used repeatedly. One list of three is fine; three of them in four paragraphs
  is a fingerprint.
- Perfect parallelism across consecutive sentences. Vary the construction on purpose.
- The self-summarizing closer ("In closing, my combination of X and Y…"). Just stop.
- Every paragraph the same length. Vary them.
- Every sentence 18 to 25 words. Vary them hard: a 34-word sentence next to a 6-word one is what
  human writing actually looks like.
- Restating the company's own marketing language back at them.

**What to do instead.**
- Use contractions. `I've`, `didn't`, `it's`. Their absence reads as stiff.
- Start a sentence with `And`, `But`, or `So` at least once. It is not a grammar error and it
  breaks the metronome.
- Include one concrete detail only this candidate could write: the thing that broke, the number
  that surprised them, the choice they nearly got wrong. Specificity is the strongest human signal
  available and it costs nothing in truthfulness because it comes from the ledger.
- State one limitation plainly, without hedging around it (this is paragraph 3's job). A model
  writing a cover letter never volunteers a weakness. A candidate worth hiring does.
- Let one sentence be blunt and short.
- Prefer the plain verb: `used` over `utilized`, `built` over `architected` unless the ledger
  supports the stronger word, `cut` over `optimized`.

**The read-aloud test.** Before delivering, read the letter as if speaking it. Any sentence you
would not say out loud to a person gets rewritten. Sentences that sound like a press release, a
LinkedIn post, or a performance review are all failures of the same kind.

Truthfulness still outranks all of this. Voice is *how* the true thing is said, never *what* is
said.

### Stage 9 — ATS Score Estimator

Run `scripts/ats_score.py` on the generated plaintext + `jd-analysis.json`. It reports coverage
of required terms, preferred terms, and hidden keywords, plus a parseability check. The number
is a *diagnostic*, not a grade — its job is to produce the list of missing terms so you can ask:
*is there a true statement that would naturally contain this word?* If yes, rewrite. If no,
leave it missing and note it.

Also report the before/after delta so the tailoring is measurable:
`python scripts/keyword_delta.py --prescan out/jd-prescan.json --before <master>.tex --after <tailored>.tex`
(`gap` terms are excluded from the percentage and listed separately). Name the output files with
`python scripts/output_name.py --name "<Full Name>" --company "<Company>"` (add `--kind CoverLetter`).

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

**Deliver `resume.tex` + `resume.pdf`, and `cover_letter.tex` + `cover_letter.pdf` when a letter
was requested. Nothing else** (Core Directive rule 3).

Build rules, the exact spacing knobs, and the one-page fitting procedure are in
`references/latex-formatting.md`. The ATS-safety preamble lines (`cmap`, `fontenc`, `lmodern`)
are load-bearing and must never be dropped — without them PDF text extraction can turn
"Artificial Intelligence" into "Articial" on the older extractors many ATS products still ship,
and the failure is silent.

Generate a plaintext rendering and a tailoring report **internally** — the verifier and the ATS
scorer both consume them, and Stage 10 needs the change log. Write them to a scratch path and do
not deliver them.

Before delivering, every time:

```bash
pdflatex -interaction=nonstopmode resume.tex && pdflatex -interaction=nonstopmode resume.tex
grep -E "Output written|Overfull" resume.log     # must say "(1 page"
pdftotext resume.pdf - | head -60                 # extraction sanity
python scripts/measure_layout.py resume.pdf --check-indent
```

A build that produces 2 pages is a failed build, not a stylistic choice — go cut content.

Then run the verifier:

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
| `assets/cover-letter-master.tex` | Stage 8b — the cover letter template |
| `examples/` | Three end-to-end worked runs against real JD archetypes |

## Output contract

Deliver `resume.tex` + `resume.pdf`, plus `cover_letter.tex` + `cover_letter.pdf` when a letter
was requested. No other files. No walkthrough, no rationale, no summary of changes.

Break that silence only for a factual problem: a failing truth check, an unresolved ledger
`conflict:` that affects the page, or an absent requirement material enough to change whether the
application is worth submitting. A few lines, then stop.
