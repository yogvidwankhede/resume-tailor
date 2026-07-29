# Job Description Analyzer

Goal: turn a posting into a structured, weighted target so every later stage has
something concrete to optimize against. Output conforms to
`assets/schemas/jd-analysis.schema.json`.

---

## 1. Segment the posting first

Most postings decompose into these blocks. Label them before extracting, because
*which block a term appears in determines its weight*.

| Block | Typical headings | What it tells you |
|---|---|---|
| Company framing | "About us", "Our mission" | Vocabulary fingerprint, values language, company stage |
| Role framing | "About the role", "The opportunity" | Seniority, scope, who you report to |
| Responsibilities | "What you'll do", "Responsibilities" | **Hidden keywords live here** — the day-to-day the manager actually pictures |
| Requirements | "Requirements", "You have", "Basic qualifications" | Hard filters. Weight highest. |
| Preferred | "Nice to have", "Bonus", "Preferred qualifications" | Differentiators. Weight medium. |
| Logistics | Location, comp, visa, clearance | Dealbreakers |

If the posting is a single unstructured blob, segment it yourself by sentence
function before extracting.

---

## 2. What to extract

### required_skills
Anything in the Requirements block, plus anything in Responsibilities phrased as a
necessity ("you will own the Kafka pipeline" makes Kafka required even if it's not
in the list). Normalize to a canonical name but **record the posting's own spelling**.

### preferred_skills
The Preferred/Bonus block. Also anything hedged: "familiarity with", "exposure to",
"a plus", "ideally".

### hidden_keywords
The highest-leverage extraction in the whole pipeline.

**Definition:** terms that recur ≥2 times in the *Responsibilities* or *About the
role* prose but never appear in the Requirements list.

**Why they matter:** the requirements list is written by whoever owns the req
template. The responsibilities prose is written by the person who will read your
resume. Nearly every applicant mirrors the requirements list; almost none mirror
the prose. Matching the prose is what makes a resume feel like it was written for
the job.

**How to find them:** strip stopwords and the requirements terms, then rank the
remaining nouns and noun phrases by frequency. Look especially for:
- Recurring *nouns of concern*: "latency", "reliability", "drift", "cost",
  "onboarding", "documentation", "handoff", "ambiguity", "iteration speed"
- Recurring *verbs of ownership*: "own", "drive", "unblock", "partner", "scale"
- Domain nouns the requirements list never names: "clinicians", "sellers",
  "regulators", "field technicians"

### responsibilities
Verbatim-ish list. These become the mapping targets in the gap analysis — each
responsibility should ideally have one resume bullet pointing at it.

### seniority
Infer from the whole posting, not the title. Signals:

| Signal | Reads as |
|---|---|
| "under guidance", "learn from", "support the team" | Intern / new grad |
| "own a component", "with some autonomy", 1–3 yrs | Junior / L3 |
| "own a system", "mentor", "drive projects", 3–6 yrs | Mid / L4 |
| "set technical direction", "across teams", "ambiguity" | Senior / L5+ |
| "define strategy", "hire", "org" | Staff / lead |

Seniority drives verb selection (Stage 5) and how much scope language is
appropriate. Claiming "drove technical direction" against a junior posting is as
bad a fit signal as under-claiming against a senior one.

### industry / company_stage
Regulated (health, finance, gov) → emphasize compliance, validation, safeguards,
documentation. Early-stage startup → emphasize shipping, breadth, ownership,
cost-consciousness. Big tech → emphasize scale, systems, cross-team.

### ats_terms
The exact strings a parser will match on. Capture **every spelling variant the
posting uses**, because the parser is usually doing substring or exact matching,
not semantics:

- `CI/CD` vs `CICD` vs `continuous integration`
- `Postgres` vs `PostgreSQL`
- `ML` vs `machine learning`
- `LLM` vs `large language model`
- `K8s` vs `Kubernetes`
- `A/B testing` vs `AB testing` vs `experimentation`

Rule: if the posting uses a form, prefer that form. If it uses both, use the
long form once and the acronym elsewhere.

### soft_skills
Extract the *phrase*, not the abstraction. "Communicating complex results to
non-technical partners" is actionable; "communication skills" is not. Then find
the ledger evidence — teaching, presenting to clinical stakeholders, writing
runbooks, onboarding teammates.

### dealbreakers
Work authorization / sponsorship, clearance, location & onsite days, degree
requirement, hard years-of-experience floor, licensure. Surface these at the top
of the tailoring report. A resume can't fix a dealbreaker, and the honest thing is
to say so before spending an hour on wording.

### vocabulary_fingerprint
The 8–15 house words the company uses for ordinary things. Examples: "partners"
vs "stakeholders"; "customers" vs "users" vs "members"; "experiments" vs "tests";
"surface" vs "show"; "craft" vs "quality".

Mirroring these is free — it costs nothing and it is not fabrication — **provided
a true statement already supports the word.** You may swap "presented results to
doctors" → "communicated findings to clinical partners". You may not swap
"analyzed Oil & Gas data" → "analyzed data for government agencies", because that
changes a fact rather than a word.

---

## 3. Weighting

Assign each extracted term a weight for Stage 9 scoring:

| Source | Weight |
|---|---|
| Required, repeated ≥2× | 3.0 |
| Required, once | 2.0 |
| Hidden keyword (prose, ≥2×) | 1.5 |
| Preferred | 1.0 |
| Company-framing vocabulary | 0.5 |

---

## 4. Handling degenerate inputs

**A URL instead of text.** Fetch it. If the fetch fails or returns a JS shell, ask
for a paste rather than guessing — a hallucinated JD poisons every downstream stage.

**A screenshot.** Read it, then echo back the extracted requirements list for
confirmation before proceeding.

**A title only** ("tailor this for a data scientist role"). Say clearly that
you're working from a generic role profile, generate one, label it
`GENERIC_PROFILE` in the report, and offer to redo it against a real posting.

**A posting that is mostly company marketing.** Extract heavily from the
vocabulary fingerprint and be explicit that required-skill extraction is thin.

**Multiple postings at once.** Analyze separately and produce separate resumes.
Averaging two JDs produces a resume tailored to neither. If the user wants one
resume for a family of roles, say so explicitly and target the intersection of
required skills plus the union of hidden keywords.

---

## 5. Worked micro-example

Posting excerpt:

> **What you'll do:** Partner with clinical teams to ship ML services into
> production. Own reliability and cost of the inference path. Write the
> documentation that lets others operate what you build.
> **Requirements:** Python; experience with cloud deployment; ML fundamentals.

Extraction:

```yaml
required_skills: [Python, cloud deployment, ML fundamentals]
preferred_skills: []
hidden_keywords: [production, reliability, cost, documentation, ownership, clinical]
responsibilities:
  - partner with clinical teams to ship ML services into production
  - own reliability and cost of the inference path
  - write operational documentation for others
seniority: mid           # "own", "lets others operate" without "set direction"
industry: healthcare
vocabulary_fingerprint: [partner, ship, own, operate]
```

Note what happened: the Requirements block was almost content-free (Python, cloud,
ML — every applicant has these). **All the signal was in the prose.** `cost`,
`reliability`, `documentation`, and `clinical` are the words that will make this
resume land, and none of them are in the requirements list.
