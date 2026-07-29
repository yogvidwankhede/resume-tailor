# Example 1 — LLM Platform Engineer (early-career, growth-stage startup)

A worked end-to-end run. Shows the highest-value moves: hidden-keyword mirroring,
adjacent-tool bridging, project swap, and a skills-block relabel.

---

## Input JD (excerpt)

> **About the role.** You'll own pieces of our LLM inference platform end to end.
> We care a lot about cost, latency, and reliability — our margins live in the
> inference path. You'll partner with product engineers to ship features, and
> you'll write the documentation that lets the rest of the team operate what you
> build. We move fast and we own our systems in production.
>
> **What you'll do**
> - Build and maintain LLM pipelines with structured outputs
> - Own cost and reliability of the inference path
> - Deploy and operate services on GCP
> - Evaluate model quality and drive model-selection decisions
>
> **Requirements**
> - 1+ years building backend services in Python or TypeScript
> - Experience deploying to a major cloud
> - Familiarity with LLM APIs and prompt design
>
> **Nice to have**
> - Vector databases / retrieval
> - Experience with orchestration frameworks (Airflow, Temporal, or similar)
> - Kubernetes

---

## Stage 2 — JD analysis

```json
{
  "role_title": "LLM Platform Engineer",
  "role_family": "llm-platform",
  "seniority": "junior",
  "company_stage": "growth",
  "required_skills": ["Python", "TypeScript", "backend services", "cloud deployment", "LLM APIs", "prompt design"],
  "preferred_skills": ["vector databases", "retrieval", "orchestration frameworks", "Airflow", "Temporal", "Kubernetes"],
  "hidden_keywords": ["cost", "latency", "reliability", "structured outputs", "documentation", "operate", "own", "production", "partner", "ship"],
  "responsibilities": [
    "build and maintain LLM pipelines with structured outputs",
    "own cost and reliability of the inference path",
    "deploy and operate services on GCP",
    "evaluate model quality and drive model-selection decisions"
  ],
  "vocabulary_fingerprint": ["own", "ship", "operate", "partner", "inference path", "margins"],
  "weights": {"Python": 3.0, "cloud deployment": 3.0, "LLM APIs": 2.0, "cost": 1.5, "reliability": 1.5, "documentation": 1.5}
}
```

**Note where the signal is.** The Requirements block is generic — Python, cloud,
LLM APIs. Every applicant matches it. The differentiating words are all in the
prose: *cost, reliability, structured outputs, documentation, operate, own.*

---

## Stage 3 — Gap table

| Requirement | W | Ledger evidence | Status | Action |
|---|---|---|---|---|
| Python / TypeScript backend | 3.0 | `euno.pipeline` (NestJS/TS), `pyshell`, `http_server` | direct | Lead EUNO bullet; swap a project in for systems evidence |
| Cloud deployment | 3.0 | `euno.heartbeat` (GCP Scheduler/Run/Tasks) | direct | Name the exact GCP services |
| LLM APIs & prompt design | 2.0 | `euno.cost`, `vishwakarma` | direct | — |
| Structured outputs *(hidden)* | 1.5 | `euno.pipeline` — ~98% valid parsing | direct | Use the JD's exact phrase "structured output" |
| Cost *(hidden)* | 1.5 | `euno.cost` — ~40%, sub-$0.002 | direct | Bullet 2; keep the mechanism clause |
| Reliability *(hidden)* | 1.5 | `euno.heartbeat` trigger gates, monitoring | direct | Add "monitoring for drift and failure" |
| Documentation *(hidden)* | 1.5 | `euno.docs` — runbooks, confirmed written | direct | Keep the handoff clause — most candidates have nothing here |
| Vector DB / retrieval | 1.0 | `healthmate`, `law_gpt`, `euno.rag` | direct | Add a Vector & Retrieval skills row |
| Orchestration (Airflow/Temporal) | 1.0 | `euno.heartbeat` | **adjacent** | Phrase as "scheduled orchestration with trigger gates and cooldowns". Do NOT write Airflow. |
| Kubernetes | 1.0 | coursework only | **absent** | Remove from skills. Cover letter. |

---

## Stage 4 — Selection

- **Experience:** EUNO ×3 bullets · ASTERISC ×2 · WashU Med ×2 · SAFETECHNO ×2.
  Teaching Assistant **cut** — nothing in this JD rewards teaching, and the space
  buys the systems project.
- **Projects:** VentureOS (agent orchestration + shipped + streaming),
  HealthMate-AI (retrieval + evals), **PyShell** (backend/systems credibility).
  Sign Language and Image Captioning cut — both are CV/ML, and this JD is a
  platform role.
- **Skills rows relabelled:** `Backend & Languages` / `LLM & Agents` /
  `Vector & Retrieval` / `Cloud & Infra` / `Data & Storage`. Kubernetes removed.
- **No summary** — the first EUNO bullet already says what this person does.

---

## Stage 5 — Bullet rewrites (before → after)

**EUNO bullet 1**

> *Before:* Build a 6-stage LLM reasoning pipeline on the LangGraph.js agent
> framework (NestJS, TypeScript), turning raw conversation into structured
> per-user knowledge via strict JSON schemas, reaching ~98% valid structured-output
> parsing

> *After:* Own a 6-stage LLM inference pipeline in production (LangGraph.js, NestJS,
> TypeScript), enforcing strict JSON schemas and input validation to reach ~98%
> valid **structured-output** parsing

*Why:* "Own" and "production" are the JD's words and are true — this is his
system. "inference pipeline" mirrors "inference path". "structured-output" was
already there and is left exactly as the JD spells it. Nothing factual changed.

**EUNO bullet 2**

> *Before:* Engineer cost-aware multi-model orchestration across GPT-4o-mini and
> Claude Haiku 4.5, cutting inference cost ~40% to sub-$0.002 per cycle

> *After:* Cut **inference cost** ~40% to sub-$0.002 per cycle through cost-aware
> model routing and per-call token budgeting across GPT-4o-mini and Claude Haiku
> 4.5, with usage logging for **reliability** and drift monitoring

*Why:* leads with the outcome because cost is the JD's stated margin concern. The
mechanism clause is preserved verbatim — this is the bullet a scoring tool once
tried to attribute to evals. Monitoring is added from `euno.heartbeat`, which is
true and reaches "reliability".

**EUNO bullet 3**

> *After:* Deploy and operate scheduled batch orchestration on **GCP** (Cloud
> Scheduler → Cloud Run → Cloud Tasks) with trigger gates, cooldowns, and
> tension-scoring over 100+ signals; authored the runbooks and **documentation**
> that let teammates take ownership after handoff

*Why:* "scheduled batch orchestration" is the honest bridge to Airflow/Temporal —
it describes what the system is without claiming a tool. "Deploy and operate" is
lifted from the posting. The documentation clause is the differentiator: almost no
early-career resume has one, and this JD asks for it explicitly.

**Project retitle**

> `PyShell: POSIX-Compatible Shell in Python — 50+ Built-in Commands, Published on PyPI`

*Why:* for a platform role, "wrote a shell from scratch and shipped it to PyPI" is
stronger backend evidence than any of the ML projects.

---

## Stage 9 — ATS

```
ATS SCORE: 86.4/100
  Strong keyword alignment; remaining risk is human judgment.

MISSING — preferred
  - Airflow      (adjacent — bridged, cannot claim)
  - Temporal     (adjacent — bridged, cannot claim)
  - Kubernetes   (genuine gap)
```

---

## Stage 10 — Recruiter review

- **Scan lands on:** name → "Software Engineering Intern, EUNO" → "Own a 6-stage
  LLM inference pipeline in production". Correct three.
- **Title inferable from top third:** yes.
- **Most likely "prove it":** *"~98% valid structured-output parsing"* → defensible;
  the ledger's `defend:` note prepares the "what's in the 2%" answer.
- **Credibility flag:** "Own" against an internship is fine here because the
  posting is junior and the ledger supports single ownership of the heartbeat
  system. Against a senior posting it would read as inflation.
- **Would cut:** the SAFETECHNO second bullet if one more line is needed.
- **Likely rejection reason:** internship-only LLM experience against candidates
  with a full-time year. Nothing on the page fixes that; the cover letter should
  lead with the cost and reliability ownership.

**Verdict: strong fit** — direct coverage on every required item; the two adjacent
misses are preferred-only.
