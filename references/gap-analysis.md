# Gap Analysis & Selection

Compare the JD analysis against the truth ledger, classify every requirement, and
decide what goes on the page.

---

## 1. The status taxonomy

For each JD requirement, assign exactly one:

### `direct` — the ledger names it
Action: surface it, and use the **posting's spelling**. If the JD says "Postgres"
and the ledger says "PostgreSQL", write the JD's form.

### `adjacent` — a near neighbour, different name
The candidate did the same category of work with a different tool or in a
different shape.

*Example:* JD wants Airflow. Ledger has "Cloud Scheduler → Cloud Run → Cloud Tasks,
2 scheduled cycles daily with trigger gates and cooldowns."

Action: describe the **real** thing in language that makes the adjacency legible —
"scheduled batch orchestration", "job queue", "DAG-style pipeline stages". Never
write the JD's tool name. Then list the tool in the report as a learn-before-interview
item.

Legible-adjacency phrasing, tested:

| JD wants | Ledger has | Honest bridge |
|---|---|---|
| Airflow / Dagster | Cloud Scheduler → Run → Tasks | "scheduled orchestration with trigger gates and retries" |
| Fraud detection | KDDCup intrusion detection | "imbalanced-class anomaly detection tuned for a fixed review capacity" |
| Feature store | ad-hoc feature engineering pipelines | "reusable feature-engineering pipelines across 9 event classes" |
| Snowflake / BigQuery | PostgreSQL + Spark | "analytical SQL over large datasets; distributed processing with Spark" |
| Terraform | Docker + GCP console/CLI deploys | "owned deployment lifecycle across scheduler, container runtime, and queue" |
| Experimentation platform | head-to-head model evals | "structured head-to-head evaluation to justify production model choice" |
| Observability / Datadog | usage logging + drift monitoring | "usage logging and monitoring for drift and failure modes" |

### `transferable` — different domain, same underlying skill
Action: reframe around the **method**, which is the honest invariant, and name the
original domain so nothing is concealed.

> ✅ "Built an imbalanced-class anomaly detection system on 494K+ network-intrusion
> records, tuning the operating point for downstream review capacity"

for a fraud-detection JD. The method transfers; the domain is stated; nothing is
hidden.

> ❌ "Built a fraud detection system on 494K+ transaction records"

This is fabrication. The records were not transactions.

### `absent` — no evidence at all
Action: **say so.** Absent items go in the report's absent list and drive two
recommendations: what to address in the cover letter, and what to learn. If more
than ~40% of *required* items are absent, the honest verdict is "stretch" or
"misaligned" — say that before optimizing wording.

---

## 2. The gap table

Emit this in the report, always:

| JD requirement | Weight | Ledger evidence | Status | Action |
|---|---|---|---|---|
| Production LLM deployment | 3.0 | `euno.pipeline`, `euno.cost` | direct | Lead EUNO bullet 1 |
| Airflow | 2.0 | `euno.heartbeat` | adjacent | Phrase as scheduled orchestration; learn Airflow |
| Kubernetes in production | 2.0 | coursework only | absent | Cover letter; do not list under Cloud |
| Clinical partnership | 1.5 (hidden) | `ra.stakeholders`, `euno.rag` | direct | Add "presented findings to clinical stakeholders" to RA |

---

## 3. Weak-signal detection

Beyond missing skills, flag these:

- **Missing measurable impact** — a JD-critical bullet with no number, when the
  ledger has one available. Frequently the number exists and was cut for space in
  a previous tailoring pass. Check `cut_from_final: true` entries first.
- **Weak projects** — projects on the current resume with no mapping to any JD
  requirement. These are pure space cost; swap them.
- **Weak bullets** — see `writing-rules.md` § 5.
- **Overweighted irrelevance** — a role with 3 bullets that maps to nothing in the
  JD, while a role with 2 bullets maps to four requirements. Rebalance.
- **Keyword dilution** — skills listed with no ledger evidence. Remove.

---

## 4. Project selection

Projects are the most malleable section and the fastest way to pivot a resume.
Select 2–3 by scoring each against the JD:

```
project_score = 2*(direct required hits)
              + 1*(preferred hits)
              + 1.5*(hidden keyword hits)
              + 1*(has a hard number)
              + 1*(shipped / public / published)
              - 1*(duplicate of another selected project's category)
```

That last term matters: two RAG projects tell the reader one thing twice. Prefer
breadth across the JD's concerns.

Archetype → default selection from this ledger:

| Target role | Projects |
|---|---|
| LLM / agent platform | VentureOS, HealthMate-AI, Vishwakarma |
| ML engineer | HealthMate-AI, Sign Language Interpreter, Image Captioning |
| Backend / infra / systems | PyShell, HTTP server from scratch, VentureOS |
| Data scientist / analyst | Sales Dashboard, Sign Language Interpreter, HealthMate-AI |
| Applied research | Sign Language Interpreter (Springer), HealthMate-AI, Image Captioning |
| Developer tooling / DX | Vishwakarma, PyShell, PyGrep |
| Health / civic tech | HealthMate-AI, Sign Language Interpreter, Image Captioning |

### Retitling
A project title is prime keyword real estate. Retitle to lead with the capability
the JD cares about, keeping the project's real name as the prefix:

- `HealthMate-AI: RAG System with Domain-Adapted Embeddings for Medical Decision Support`
  → medical / RAG roles
- `HealthMate-AI: Retrieval System with Domain-Adapted Embeddings for High-Stakes Decision Support`
  → fintech / risk roles (same project, honest retitle — nothing about the system changed)
- `HealthMate-AI: Domain-Adapted Embedding Fine-Tuning with LoRA and 3-Fold Cross-Validation`
  → ML-research roles

The rule: retitling may re-emphasize what the system **is**. It may not claim a
domain the system was never applied to.

---

## 5. Space budget

One page. Rough allocation at 9.5pt:

| Section | Lines |
|---|---|
| Header | 2 |
| Education | 5–7 |
| Skills | 5–6 |
| Experience | 26–32 |
| Projects | 10–14 |

When over budget, cut in this order:
1. The oldest role's weakest bullet
2. The third project's second bullet
3. The Certifications/Coursework line
4. A whole low-relevance role (only if it doesn't create a visible date gap)
5. The portfolio link from the header

Never cut: dates, employers, the degree, or the metric from a JD-critical bullet.
