# Resume Writing Rules

Contents:
1. Bullet grammar
2. The verb bank
3. The quantification ladder
4. STAR, compressed
5. Weak-bullet diagnosis and repair
6. Section ordering
7. Skills-block construction
8. Summary construction
9. Tense, person, punctuation
10. Length and density
11. Banned constructions

---

## 1. Bullet grammar

The shape that survives a 20-second scan:

```
[Verb] [object — what you built or changed] [ , with what mechanism ] , [quantified outcome] [ for whom / why it mattered ]
```

Worked:

> **Engineer** cost-aware multi-model orchestration across GPT-4o-mini and Claude Haiku 4.5 **with per-call token budgeting**, cutting inference cost ~40% to sub-$0.002 per cycle

- verb: Engineer
- object: cost-aware multi-model orchestration
- mechanism: per-call token budgeting
- outcome: ~40% cost cut, sub-$0.002/cycle

The mechanism clause is what separates a resume from a wishlist. Anyone can claim
a 40% cost cut; naming *token budgeting* tells the reader you actually did it and
gives the interviewer somewhere to push.

**One bullet, one claim.** If the bullet contains two independent accomplishments
joined by "and", it is two bullets — or, more often, one bullet and one cut.

**Lead with the verb.** No "Responsible for", no "Worked on", no "Helped with",
no participial openers ("Having built…").

**Front-load the JD-relevant noun.** A recruiter scanning for "RAG" should hit it
in the first six words, not at the end of line two.

---

## 2. The verb bank

Choose the verb for the *actual role you played*. Inflating the verb is the
cheapest and most detectable form of fabrication — "Architected" when you
implemented someone else's design reads as a lie the moment the interviewer asks
about the design tradeoffs.

| You did… | Verbs |
|---|---|
| Designed the system's structure | Architected, Designed, Structured, Modeled |
| Wrote the thing that didn't exist | Built, Developed, Engineered, Implemented, Created |
| Put it into production | Shipped, Deployed, Launched, Released, Productionized |
| Made an existing thing better | Optimized, Reduced, Accelerated, Streamlined, Hardened, Refactored |
| Made it bigger / more general | Scaled, Extended, Generalized, Migrated |
| Found something out | Analyzed, Investigated, Diagnosed, Quantified, Characterized, Validated |
| Ran a study | Evaluated, Benchmarked, Measured, Tested, Replicated |
| Owned the outcome | Owned, Led, Drove, Spearheaded, Directed |
| Worked with people | Partnered, Advised, Mentored, Trained, Onboarded, Presented |
| Made a decision stick | Standardized, Established, Instituted, Formalized, Documented |
| Cleaned up a mess | Consolidated, Reconciled, Normalized, Deduplicated, Remediated |

**Verbs to retire on sight:** Utilized, Leveraged, Spearheaded (unless literal),
Assisted, Participated, Helped, Worked on, Was responsible for, Involved in,
Successfully <anything>, Tasked with.

Don't repeat a verb inside a single role, and try not to repeat within a section.
Repetition reads as a limited range even when the work wasn't.

---

## 3. The quantification ladder

When there's no number, climb until you find a rung you can honestly stand on.

1. **Direct outcome metric** — best. "cut inference cost ~40% to sub-$0.002 per cycle"
2. **Quality/accuracy metric** — "95.4% accuracy at a 0.6% false-positive rate"
3. **Scale metric** — "494K+ records", "40K+ text chunks", "40+ undergraduates"
4. **Throughput/latency** — "500+ requests/day at <200ms"
5. **Comparative delta** — "0.85→0.92 correlation", "+11.7% over an LSTM baseline",
   "40% less computation than BEM"
6. **Time/effort saved** — "cut report preparation ~30%"
7. **Breadth/complexity** — "9 attack types", "6-stage pipeline", "15+ projects",
   "100+ candidate signals"
8. **Downstream consequence** — "enabling proactive rather than reactive
   investigation" (no number, but a real consequence)

Rules:

- **Pair the metric with its baseline** when the raw number is meaningless alone.
  "93.3% retrieval accuracy" is fine; "improved accuracy by 18%" needs a *from what*.
- **Ranges and approximations are honest and fine.** `~40%`, `2.9–16.5mm`,
  `40K+`. Precision you don't have is worse than a range you do.
- **Never round up into a rounder-sounding lie.** 88.3% does not become "nearly 90%".
- **Attribute the metric to the mechanism that produced it.** This is the single
  most common accidental fabrication — see § 5.
- If no rung applies, the bullet is probably not worth its two lines. Cut it.

---

## 4. STAR, compressed

STAR (Situation, Task, Action, Result) is an interview format, not a resume
format — written out longhand it eats four lines. Compress it to one:

| STAR element | Where it goes in a bullet |
|---|---|
| Situation | An adjective or prepositional phrase: "on 494K+ highly imbalanced records" |
| Task | Usually implicit in the verb + object |
| Action | The verb + object + mechanism clause — the bulk of the bullet |
| Result | The quantified outcome at the end |

> **S+A+R:** "Built an adversarial-attack detection system on 494K+ highly
> imbalanced records (KDDCup 1999), engineering temporal and behavioral features
> across 9 attack types to reach 95.4% accuracy at a 0.6% false-positive rate."

Keep full STAR in the tailoring report's notes so the candidate has interview
answers ready — that's where the Situation and Task belong.

---

## 5. Weak-bullet diagnosis and repair

| Symptom | Diagnosis | Repair |
|---|---|---|
| "Responsible for maintaining data pipelines" | Job-description-shaped, not accomplishment-shaped | Name what changed because you were there, and by how much |
| "Improved model accuracy significantly" | Unquantified intensifier | Climb the ladder; if there's genuinely no number, name the mechanism and the consequence |
| "Used Python and SQL to analyze data" | Tools as the subject | Tools belong in a parenthetical; the *finding* is the subject |
| "Built a dashboard for the team" | Output stated, outcome missing | What decision did it change? What did it save? |
| "Worked with cross-functional stakeholders" | Soft-skill noun soup | Name the function, the artifact, and the decision it drove |
| Bullet runs 3+ lines | Two claims wearing one bullet | Split, then cut the weaker half |
| Third bullet is the best one | Buried lead | Reorder — bullet #1 carries the role |

### The false-causality trap

The most dangerous rewrite is the one where **every individual fact is true but
the causal link is invented.** Example, from a real scoring-tool suggestion:

> ❌ "Implemented evals to cut inference cost ~40%"

Evals existed. The 40% cut existed. But *token budgeting and model routing* cut
the cost — evals did not. This is a fabrication, and it's the kind an interviewer
finds in one question.

> ✅ "Engineered cost-aware model routing with per-call token budgeting, cutting
> inference cost ~40%"

Before shipping any bullet that contains a number, ask: **what actually caused
this number?** If the bullet names something else, rewrite it.

---

## 6. Section ordering

Default: `HEADER → EDUCATION → SKILLS → EXPERIENCE → PROJECTS`

- **Education first** while the candidate is a current student or <2 years from
  graduation, or when the degree is itself a qualification the JD names.
- **Experience first** the moment industry experience outweighs the degree — a
  recruiter for a mid-level role wants the job history in the top third.
- **Skills above Experience** puts the keyword block where both the ATS and the
  human scan first. This is deliberate and worth defending; the alternative
  (skills at the bottom) is a stylistic convention with no scanning benefit.
- **Projects last** unless the candidate has little formal experience in the
  target domain and the projects *are* the case — then Projects moves above
  Experience and the section is renamed to something load-bearing
  ("Selected Engineering Projects", "Applied ML Projects").
- **Publications** get their own section only when there are 3+ or the role is
  research. With 2, inline them in the bullets where they were earned, as links.
- **Summary** — see § 8. Absent by default.

Never reorder roles out of reverse chronology. Recruiters read date columns for
gaps and a shuffled order reads as concealment.

---

## 7. Skills-block construction

Five rows. Each row is `Label` + a comma-separated list.

**The label is a keyword.** `LLM & Agent Frameworks` and `ML & Data Science` are
different bets about what the reader is looking for. Tailor labels first, contents
second.

Label patterns that work by role archetype:

| Target role | Row labels |
|---|---|
| LLM / agent platform | Backend & Languages · LLM & Agents · Vector & Retrieval · Cloud & Infra · Data & Storage |
| ML engineer | Programming · ML & Modeling · Data & Pipelines · Cloud & MLOps · Tools |
| Data scientist | Programming · Statistics & Modeling · Data & Pipelines · Visualization & Reporting · Cloud & Tools |
| Data analyst | Analytics & SQL · Visualization & Reporting · Statistics · Data Engineering · Tools |
| Backend / platform | Languages & Frameworks · Distributed Systems · Data & Storage · Cloud & Infra · Practices |

Ordering rules:

- Row 1 = the JD's core stack. Item 1 in each row = the JD's most-required item
  in that category.
- Use the JD's spelling. If the posting says "Postgres", write "PostgreSQL
  (Postgres)" only if both forms matter; otherwise mirror the posting.
- **Every item must have evidence.** Cross-check against `truth-base.yaml`'s
  `skills:` map — an item with no backing experience or project is both a keyword
  dilutant and an interview landmine.
- Cap at ~8 items per row. Beyond that the row wraps and the density gain reverses.
- Six rows forces the body font below the 9.5pt floor. Merge two weak rows instead
  (this is exactly how `Big Data & Databases` + `Visualization` became
  `Data & Visualization`, which bought the font back).

---

## 8. Summary construction

Include a summary only when: the JD requires a pivot the bullets can't make on
their own, there's a domain jump to explain, or the user asks.

Structure, 2–3 lines, no first person:

```
[What you are, in the JD's words] with [N] years across [the two domains that matter here].
[Strongest JD-relevant proof point, with its number]. [Second proof point, with its number].
[What you're aiming at — one clause, only if it adds information.]
```

Worked (for an LLM-infrastructure role):

> Software engineer building production LLM systems — a 6-stage reasoning pipeline
> at ~98% valid structured-output parsing, and cost-aware model routing that cut
> inference spend ~40% to sub-$0.002 per cycle. MS in Data Analytics & Statistics
> with published research in time-series and retrieval.

Banned openers: "Results-driven professional", "Passionate about", "Seeking a
challenging role", "Detail-oriented", "Proven track record".

---

## 9. Tense, person, punctuation

- **Present tense** for the current role. **Past tense** for everything ended.
  Be consistent within a role; a mixed-tense role reads as careless.
- **No first person.** No "I", no "my". Implied subject throughout.
- **No terminal periods on bullets** — or terminal periods on all of them. Pick
  one and hold it. (This template uses none.)
- **Serial comma**, consistently.
- **Numerals for all numbers**, including under ten: "9 attack types", "6-stage
  pipeline", "2 daily cycles".
- **Spell out an acronym once** if the JD spells it out; otherwise use the form
  the JD uses. When in doubt, `Retrieval-Augmented Generation (RAG)` on first use
  covers both parser and human.
- **Arrows and math symbols**: fine in LaTeX (`0.85→0.92`), but the plaintext
  export must degrade to `0.85 -> 0.92`. Never rely on a glyph the ATS may drop.

---

## 10. Length and density

- **One page**, until ~8–10 years of experience.
- Most relevant role: 3 bullets. Others: 2. Least relevant / oldest: 1–2.
- 2–3 projects, 1–2 bullets each.
- A bullet should occupy 1–2 rendered lines at 9.5pt. A bullet that renders as
  2 lines + 3 words is the worst case — it costs a full line for nothing. Trim it
  to 2 lines or expand it to earn the third.
- **Cut content, don't shrink the font.** 9.5pt is the floor. Below that the page
  reads as desperate and prints badly. See `latex-formatting.md`.

---

## 11. Banned constructions

- "Responsible for", "Duties included", "Tasked with"
- "Utilized", "Leveraged" as a substitute for "used"
- "Successfully" (the alternative is not on the resume)
- "Various", "multiple", "several" where a count exists
- "Cutting-edge", "state-of-the-art", "robust", "comprehensive", "innovative",
  "seamless", "synergy" — adjectives standing in for evidence
- "Team player", "hard worker", "fast learner", "self-starter"
- "Familiar with" / "exposure to" in a skills block — if it needs a hedge, it
  doesn't belong there
- References available upon request
- Photos, birthdate, marital status, full mailing address
- Skill-level bars, star ratings, percentage-proficiency graphics (unparseable
  and unfalsifiable)
