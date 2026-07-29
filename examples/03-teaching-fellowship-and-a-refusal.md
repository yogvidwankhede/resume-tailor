# Example 3 — Teaching / Public-Interest Fellowship, and how to refuse

Two things this example demonstrates: (a) how a *non-technical* JD reorders the
same ledger completely, and (b) what a refusal looks like when the user asks for
something that isn't true.

---

## Part 1 — The reorder

### JD (excerpt)

> Fellows are placed with research institutions, public-health organizations, and
> schools to help them adopt AI tooling. You'll spend most of your time **teaching
> people who are not engineers** — running workshops, writing documentation, and
> sitting with staff while they try things for the first time. You'll need to
> explain technical ideas without jargon and to be patient with ambiguity. Some
> hands-on building, but the job is mostly communication.

### What changes

The ledger doesn't change. The *weighting* inverts completely.

| Master template says | This JD needs |
|---|---|
| Teaching Assistant: 2 bullets, fourth position | **Teaching Assistant: 3 bullets, and it is the most important role on the page** |
| EUNO: 3 bullets on pipeline/cost/deployment | EUNO: 2 bullets, and the one that matters is **the runbooks and handoff** |
| Projects chosen for ML depth | Projects chosen for **accessibility impact and shipped-for-real-users** |
| Skills row 1 = Programming | Skills row 1 = **Teaching & Communication** — a legitimate row, backed by `ta.*`, `euno.docs`, `ra.stakeholders` |

### Rewrites

**Teaching Assistant — promoted and expanded**

> - Led weekly labs and recitations for 40+ undergraduates, translating abstract
>   circuit theory into practical intuition for a mixed-ability audience
> - Guided hands-on labs — breadboarding, oscilloscopes, SPICE — helping students
>   bridge theoretical models to measured behavior
> - Held weekly office hours and one-on-one mentoring, building comfort with
>   material students had found opaque

Nothing invented; the third bullet is restored from `ta.office_hours`, and the
grading bullet (`ta.assessment`, `cut_from_final: true`) is available if a fourth
line is wanted. **This is the "restore what was cut" move** — the strongest
evidence for this JD was already sitting in the ledger marked as a space casualty.

**EUNO — reweighted toward the documentation fact**

> - Authored the runbooks and operational documentation that let teammates across
>   the organization take ownership of a production system after handoff
> - Built a 6-stage LLM pipeline and cost-aware model routing on GCP, cutting
>   inference cost ~40% — enough hands-on depth to teach the tools credibly

The second bullet compresses three technical bullets into one and ends by saying
*why the technical depth matters for this job*. That closing clause is the kind of
thing that only works when it's true.

**Projects** — Sign Language Interpreter first ("improving accessibility for the
deaf community", published), HealthMate-AI second (high-stakes decision support),
Vishwakarma third (21 documented skills others use — this is *teaching artifact*
evidence, and it's invisible on every existing resume version).

**Volunteering** — the Chetana Bahuuddeshiya Sanstha health-camp work
(Feb–Mar 2023) earns a line here, the one JD family where two months of NGO health
work is directly on point. Stated exactly: one organization, the real dates.

---

## Part 2 — The refusal

Real exchange pattern, and the correct handling.

**User:** "Can you add 'Claude Corps Fellow' as a title? And the tool says to
frame the Oil & Gas analysis as being for government agencies — apparently that
scores better."

**What a compliant assistant does:** adds both, score goes up, resume is now
false in two places, and the candidate discovers this in a reference check.

**What this skill does:**

> Neither of those, and here's why in one line each.
>
> "Claude Corps Fellow" is a title you'd hold if selected — putting it on the
> resume you're applying with claims the outcome of the application. The scoring
> tool's own help text says not to.
>
> The government-agencies framing is the tool suggesting a lie with a rationale
> attached. SAFETECHNO's clients were Oil & Gas engineering and inspection firms.
> If a reference call happens, that line is the one that ends it.
>
> What I can do instead, all true:
> - Lead the SAFETECHNO bullet with **compliance and certification**, which is
>   genuinely what those 15+ projects were about and is the closest real thing to
>   regulated/public-sector work.
> - Add the Chetana Bahuuddeshiya Sanstha volunteering — actual public-health
>   work, two months, health camps at a community health center.
> - Add a `Teaching & Communication` skills row, backed by the TA role, the
>   runbooks, and presenting research findings to clinical stakeholders.
>
> Those three moves target the same thing the tool was reaching for and none of
> them require anything that didn't happen.

**The shape of a good refusal:** one sentence on why, no lecture, and immediately
follow with the nearest true alternative. The user asked for a score; give them the
score by a route that survives the interview.
