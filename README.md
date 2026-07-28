# resume-tailor

A truth-constrained resume optimization engine, packaged as a Claude Skill.

Give it a job description. It analyzes the posting, compares it against a verified
inventory of what you have actually done, decides what belongs on the page, rewrites
the bullets into quantified impact statements in the employer's own vocabulary,
scores the result against the posting, critiques it as a recruiter would, and emits
a submission-ready one-page resume — then runs a checker that fails the build if
anything on the page can't be traced back to a real fact.

The design bet is simple: **rewriting is free, inventing is fatal.** One fabricated
line discards the whole document, and every number on a resume is a question you
have volunteered to answer.

---

## Install

Drop the folder into your skills directory:

```
~/.claude/skills/resume-tailor/          # personal
.claude/skills/resume-tailor/            # project-scoped
```

Or install the packaged `resume-tailor.skill` file through your client.

**Dependencies** (only for the scripts; the skill works without them):

```bash
pip install pyyaml pillow --break-system-packages
# for the PDF path:
apt-get install -y poppler-utils texlive-latex-base texlive-fonts-recommended
```

---

## Use

Just describe what you want. The skill triggers on any of:

```
Tailor my resume for this job: <paste>
Will this pass the ATS?
Rewrite these three bullets to be stronger
Score my resume against this posting
Should I even apply to this?
Add my new internship to my resume
```

Typical first run:

```
> Tailor my resume for this: https://…/llm-platform-engineer
```

You get back `resume.txt`, `resume.md`, optionally `resume.tex`/`.pdf`, and a
`tailoring-report.md` containing the gap table, the ATS score with its missing-term
list, the recruiter critique, a before→after change log, and — the part that
matters — the list of things the job wants that you genuinely don't have.

---

## How it works

Eleven stages, run in order. Selection happens before writing, which is the whole
trick: deciding what goes on the page while it's still a list is far cheaper than
deciding after it's prose you're attached to.

| Stage | What it does |
|---|---|
| 0 | Build/verify the truth ledger |
| 1 | Resume Analyzer — weak bullets, buried leads, stale framing, ledger drift |
| 2 | JD Analyzer — required, preferred, **hidden keywords**, seniority, dealbreakers |
| 3 | Gap Analysis — `direct` / `adjacent` / `transferable` / `absent` per requirement |
| 4 | Tailoring Engine — ranking, space budget, ordering, vocabulary map |
| 5 | Bullet Rewriter — verb + object + mechanism → quantified outcome |
| 6 | Project Optimizer — selection and capability-first retitling |
| 7 | Skills Optimizer — regroup, relabel, reorder |
| 8 | Summary Generator — conditional; absent by default |
| 9 | ATS Score Estimator — score, and more usefully the missing-term list |
| 10 | Recruiter Review — the 20-second scan, the "prove it" test, an honest verdict |
| 11 | Final Generator — TXT / MD / LaTeX / PDF + report, then the truth check |

---

## The two files that matter

**`assets/truth-base.yaml`** — the fact ledger. Every role, date, metric, tool,
project, and link. Nothing may appear on a generated resume that isn't traceable
here. Fields worth knowing:

- `mechanism:` — what actually produced a metric. Guards against the most common
  accidental fabrication: attributing a real number to the wrong real cause.
- `defend:` — the interview question the claim invites. Doubles as prep.
- `conflict:` — two sources disagree; never resolved silently.
- `cut_from_final: true` — real facts cut for space in a previous pass. Check
  these first when a JD asks for something the resume doesn't show; the gap is
  often not a gap.
- `forbidden_claims:` — specific rewrites that were proposed and rejected as lies.

**`assets/resume-master.txt`** — the canonical template. Section ordering, bullet
grammar, density, and the plaintext form an ATS actually parses. Its companion
`resume-master.tex` carries the layout.

---

## What it will and won't do

**Will:** reorder, reframe, compress, expand, requantify from real data, retitle,
regroup, and translate into the employer's vocabulary.

**Won't:** invent an employer, a date, a title, a degree, a certification, a tool
you haven't used, a metric that wasn't measured, a causal link that didn't hold, or
a scope that didn't exist.

When a rewrite needs a fact the ledger lacks, it finds a true adjacent claim, asks
you a specific question, or reports the gap. It never splits the difference.

`references/edge-cases.md` catalogues real suggestions from commercial resume
scorers that were rejected for being fabrications — including one that said, in as
many words, that framing the work as being for government agencies "aligns better
with the role."

---

## Layout notes worth stealing

Even if you never use the tailoring engine, three things in
`references/latex-formatting.md` are worth having:

1. **The ligature bug.** A LaTeX PDF can render "Artificial" perfectly and
   *extract* as "Articial", because `fi` is a single glyph. Current TeX Live +
   poppler usually handles it; the years-old PDFBox builds inside many ATS
   products do not, and you can't see which one the employer runs. Fix:
   `\usepackage{cmap}`, `[T1]{fontenc}`, `{lmodern}`. Verify with
   `pdftotext resume.pdf - | grep -i artificial`.
2. **Cut content, don't shrink the font.** 9.5pt is the floor. Tightening leading
   was swept from 0.86 to 0.92 and abandoned — it buys two lines and costs more
   legibility than deleting one bullet.
3. **Measure, don't look.** `scripts/measure_layout.py` renders the page and
   compares the left edge of every section heading. The classic indented-first-
   heading bug is invisible at 100% zoom.

---

## Scripts

```bash
python scripts/verify_truth.py   --resume out/resume.txt --ledger assets/truth-base.yaml
python scripts/ats_score.py      --resume out/resume.txt --jd out/jd-analysis.json --pdf out/resume.pdf
python scripts/measure_layout.py out/resume.pdf --check-indent
```

`verify_truth.py` exiting non-zero is a blocker, not a warning. It's a lexical
check — it catches invented numbers, employers, dates and links, but it cannot
catch a false-causality bullet assembled entirely from true tokens. Stage 10 is the
backstop for that.

---

## Porting to another candidate

Replace `assets/truth-base.yaml` and `assets/resume-master.txt`, rewrite
`references/truth-base.md` and the `forbidden_claims` list, and swap in your own
`examples/`. Everything in `references/writing-rules.md`, `jd-analysis.md`,
`ats-guidelines.md`, and `scoring-and-review.md` is candidate-independent. See
`references/prompt-engineering-notes.md` § 8.

---

## Layout

```
resume-tailor/
├── SKILL.md
├── README.md
├── references/
│   ├── truth-base.md              narrative context for the ledger
│   ├── jd-analysis.md             extraction taxonomy, hidden-keyword heuristics
│   ├── gap-analysis.md            status rules, adjacency bridges, project selection
│   ├── writing-rules.md           bullet grammar, verb bank, quantification ladder
│   ├── ats-guidelines.md          parser behaviour, ligature bug, keyword density
│   ├── latex-formatting.md        layout knobs, one-page fitting, build loop
│   ├── scoring-and-review.md      scoring components, recruiter rubric
│   ├── edge-cases.md              rejected-suggestion catalogue, situational cases
│   ├── prompt-engineering-notes.md  design rationale, limitations, porting
│   └── evaluation-checklist.md    pre-flight gates
├── assets/
│   ├── truth-base.yaml            THE FACT LEDGER
│   ├── resume-master.txt          canonical content template
│   ├── resume-master.tex          canonical layout template
│   └── schemas/                   jd-analysis · tailoring-plan · run-report
├── scripts/
│   ├── verify_truth.py            anti-fabrication gate (blocking)
│   ├── ats_score.py               score + missing-term list
│   └── measure_layout.py          pixel-level layout verification
├── examples/                      three worked end-to-end runs
└── evals/evals.json               test prompts
```
