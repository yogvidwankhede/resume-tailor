# Example 2 — Fraud / Risk Data Scientist (fintech)

The interesting case: a domain the candidate has never worked in, where the
*method* transfers completely and the *data* does not. This is where fabrication
pressure is highest, and where a scoring tool once explicitly suggested lying.

---

## Input JD (excerpt)

> Build models that catch fraudulent transactions before they settle. You'll work
> with extremely imbalanced data and you'll have to reason carefully about the
> precision/recall tradeoff, because every false positive costs a real customer a
> real decline. You'll partner with the investigations team, whose review capacity
> is finite. Own model monitoring in production.
>
> **Requirements:** Python; SQL; supervised learning on imbalanced datasets;
> feature engineering; comfort with precision/recall and ROC-AUC.
> **Preferred:** anomaly detection, time-series, model monitoring, production
> deployment experience.

---

## Stage 3 — Gap table (the important rows)

| Requirement | Ledger evidence | Status | Action |
|---|---|---|---|
| Imbalanced supervised learning | `ast.forecast` — KDDCup 1999, 494K+ records, 9 classes | **transferable** | Reframe on the method; name the real domain |
| Precision/recall reasoning | `ast.forecast` — 95.4% acc @ 0.6% FPR | direct | Lead with the operating point, not the accuracy |
| Feature engineering | `ast.forecast` mechanism | direct | Name "temporal and behavioral features" |
| Anomaly detection | `ast.forecast`, `ast.dtw` | direct | — |
| Time-series | `ast.dtw`, `oasis.forecast`, `ra.*` | direct | — |
| Model monitoring in production | `euno.heartbeat` — usage logging, drift/failure monitoring | **adjacent** | Bridge honestly |
| Fraudulent transactions | none | **absent** | Never claim. Cover letter. |
| SQL | `safetechno`, `asterisc` | direct | — |

---

## The core rewrite

**What a scoring tool suggested:**

> ❌ "Built a fraud detection system on 494K+ transaction records, achieving 95.4%
> accuracy at a 0.6% false positive rate"

Every word except "fraud" and "transaction" is true. Those two words are a
fabrication: the dataset is KDDCup 1999, network intrusion data, and the resume
links to the IJSRD paper that says so. A reviewer who clicks the link finds it in
thirty seconds.

**What the skill produces instead:**

> ✅ Built an **imbalanced-class anomaly detection** system on 494K+ highly skewed
> network-intrusion records (KDDCup 1999), **engineering temporal and behavioral
> features** across 9 attack classes to reach 95.4% detection at a **0.6% false-positive
> rate** — tuning the operating point explicitly for finite downstream review capacity

Why this is stronger than the lie, not just safer:

- **"tuning the operating point explicitly for finite downstream review capacity"**
  is the exact concern the JD raises about the investigations team. It demonstrates
  the *judgment* the role needs. The fabricated version demonstrates only a number.
- Naming the real domain and dataset signals confidence. A reader who knows KDDCup
  is a soft benchmark sees a candidate who isn't hiding it.
- Every keyword the ATS needs — imbalanced, anomaly detection, feature engineering,
  false-positive rate — is present, in the JD's own vocabulary.

**Second ASTERISC bullet:**

> ✅ Deployed a Dynamic Time Warping classifier (88.3% accuracy, 4–8 day lead time)
> that surfaced emerging attack patterns before they materialized, enabling
> **proactive rather than reactive investigation**

The closing clause has no number, but it names a real consequence in the language
of an investigations team.

**Model monitoring bridge (EUNO):**

> ✅ Own usage logging and **monitoring for drift and failure modes** across a
> production inference pipeline running 2 scheduled cycles daily

Honest, and it reaches "model monitoring in production" without claiming an
MLOps platform he hasn't used.

---

## Selection changes vs the master template

- **Skills relabelled:** `Programming` / `ML & Statistics` / `Data & Pipelines` /
  `Cloud & Tools` / `LLM & Reporting`. The `ML & Statistics` row is expanded to
  carry `Imbalanced-Class Modeling`, `Anomaly & Fraud Detection`,
  `ROC-AUC / Precision-Recall`, `Hypothesis Testing` — all with ledger evidence.
  *(Note: "Fraud Detection" is claimable as a **skill category** the candidate has
  studied and applied the methods of; "built a fraud system" is not claimable as an
  **accomplishment**. That distinction is the whole game here.)*
- **ASTERISC moves to the top of Experience** — it is the most relevant role and
  reverse chronology still permits it only if it is genuinely most recent. It is
  not, so it stays third but gets **3 bullets** while EUNO drops to 2. Space, not
  order, carries the emphasis.
- **Education gains the Coursework line** (`Statistical Inference, Predictive
  Modeling, Time Series, Experimental Design`) in place of the certifications line —
  a quant JD rewards coursework more than an AI-fluency certificate.
- **Projects:** HealthMate-AI (retrieval + rigorous evals), Sales Dashboard
  (business impact framing), Sign Language Interpreter (published DTW method,
  connects to the time-series requirement).

---

## Verdict

**worth applying** — every required method is direct or transferable, and the
precision/recall reasoning is genuinely strong. The absence is domain: no
financial-services or transaction data. That belongs in the cover letter as a
sentence, not on the resume as a claim.

**Absent list:** fraud/payments domain experience; production ML monitoring
tooling (Evidently, WhyLabs, or similar); financial regulatory context.
