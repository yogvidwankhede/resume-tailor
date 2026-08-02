# Truth Base — narrative context

The machine-readable ledger is `assets/truth-base.yaml`. **That file is
authoritative for facts.** This file carries the judgment that doesn't fit in
YAML: what each experience actually was, which framings are legitimate, and where
the landmines are.

---

## Who this is

Yogvid Wankhede — MS in Data Analytics & Statistics (WashU, May 2026), BTech in
Artificial Intelligence (G.H. Raisoni, 2024). Currently a software engineering
intern building production LLM systems. Under two years of full-time professional
experience, so this is an **early-career profile**: Education leads, projects
carry real weight, and the credibility risk is *over*-claiming scope rather than
under-selling.

Two published papers, two Anthropic certifications, 24 public repos, one shipped
product that placed top 10 in a public competition. The inventory is unusually
broad for the career stage, which means **the tailoring problem here is selection,
not scarcity.** Most runs will spend more effort deciding what to leave out.

---

## The four distinct capability stories

The ledger supports four different resumes. Pick one per application; mixing them
produces a resume that reads as unfocused.

**1. Production LLM / agent engineering.**
EUNO (6-stage LangGraph pipeline, multi-model cost routing, GCP scheduled workers),
VentureOS (8-agent orchestration, SSE streaming, shipped publicly), Vishwakarma
(21 Claude Code skills), HealthMate-AI and law-gpt (two independent RAG systems).
This is the strongest story and the one with the most current evidence.

**2. Applied ML / research.**
The WashU Med inverse-problem work (MFS vs BEM, 0.85→0.92 correlation, 118-episode
validation) plus two publications plus the DTW and captioning work. This is the
story with the most methodological depth and the most defensible numbers.

**3. Data science / analytics.**
ASTERISC (imbalanced-class detection on 494K+ records, time-series forecasting),
SAFETECHNO (three years of Oil & Gas analytics, dashboards, process
standardization), the Tableau sales dashboard, Oasis Infobyte. The longest tenure
in the inventory is here — SAFETECHNO is three years.

**4. Systems / backend.**
PyShell (POSIX shell, on PyPI), the from-scratch HTTP/1.1 server, PyGrep (regex
engine), the DNS-over-HTTPS Chrome extension, plus the NestJS/TypeScript backend
work at EUNO. This story is invisible on every existing resume version and is the
most under-exploited part of the inventory — for a backend or infra posting, these
four repos are better evidence than any of the ML projects.

---

## Where the numbers came from

Read the `mechanism:` fields before rewriting any bullet with a number. The three
that get mis-attributed most often:

- **~40% inference cost reduction (EUNO)** — produced by *cost-aware model routing
  and per-call token budgeting*. Not by evals, not by the pipeline design, not by
  RAG. This exact error has already been caught once in a scoring-tool suggestion.
- **~98% valid structured-output parsing (EUNO)** — produced by *strict JSON
  schemas and input validation*. The interview question is what's in the 2%.
- **95.4% accuracy at 0.6% false-positive rate (ASTERISC)** — on KDDCup 1999, a
  known-easy and heavily criticized benchmark. The defensible framing emphasizes
  the *operating point being tuned for downstream review capacity*, not the raw
  accuracy, because a sophisticated reader will otherwise discount the number.

---

## The dataset landmine

KDDCup 1999 is **network intrusion data**. It is not healthcare data, not
transaction data, not public-health surveillance data. An automated suggestion has
already tried to reframe it as public-health outbreak prediction; the bullet links
to the IJSRD paper, which disproves the reframing on click.

The honest transfer for a fraud or risk role is the *method*: imbalanced-class
anomaly detection, temporal feature engineering, operating-point selection under a
fixed review budget. Say the method, name the domain, and let the reader draw the
line.

---

## What was cut and can come back

Several genuinely strong facts were cut from recent resume versions purely for
space. They carry `cut_from_final: true` and should be the **first** thing checked
when a JD asks for something the current resume doesn't show:

- The EUNO HIPAA-safeguards bullet (AES-GCM field encryption, authorization,
  zero PHI in logs) — re-add for any healthcare, security, or compliance posting.
- The RA scale bullet (28,120 potential maps, 595 electrograms, 8 episodes) —
  re-add for research or large-scale-analysis postings.
- The TA grading/feedback bullet — re-add for teaching or mentoring-heavy roles.
- The entire Oasis Infobyte role — re-add for early-career analyst postings where
  the healthcare/retail framing helps.
- Hadoop, Hive, Excel, Seaborn from the skills block — only if the candidate
  confirms real use.

This is the highest-return move in the whole pipeline and the one most likely to
be overlooked: **the gap is often not a gap, it's a previous space cut.**

---

## Resolved

**Teaching Assistant dates: August 2025 - January 2026.** Confirmed by the candidate on
2 August 2026. Older drafts carrying Sep 2025 - Feb 2026 are wrong. Do not reintroduce.

---

## Unresolved conflicts

These must be settled before submission. Each is a factual claim where two sources
disagree, and shipping the wrong one is a credibility problem independent of
everything else on the page.

| Item | Options | Note |
|---|---|---|
| SAFETECHNO employment type | Full-time (LinkedIn) **vs** Part-Time (recent resume) | Material — three years full-time reads very differently |
| EUNO heartbeat infrastructure | GCP Cloud Tasks **vs** BullMQ/Redis | Possibly both; confirm before naming only one |
| EUNO RAG safeguards | "in-code authorization" **vs** "row-level security" | Pick the one that is literally true |
| PyGrep | CLI + regex engine (GitHub) **vs** VS Code extension (portfolio) | Confirm |
| Anthropic certificate URLs | Which link maps to which certificate | Supplied unlabeled |

---

## Things that are true but rarely worth the space

- Volunteering with Chetana Bahuuddeshiya Sanstha (2 months, health camps). Real,
  and genuinely relevant for public-health or civic-tech roles. Never pluralize it
  into "community organizations."
- UMANG social media management — include only if the role involves communications
  or community.
- The two Forage repos (`forage-walmart-task-4`, `forage-midas`) are **forks of
  provided starter repos**. They are not original work and must never be presented
  as projects.
- The thinner repos (whatsapp-bot, EDA notebooks, Educational-Resource-Management)
  are real but support-level. They belong in a GitHub profile, not on a one-page
  resume.
