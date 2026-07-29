# Edge Cases

Read this whenever a rewrite feels like it needs a fact you don't have.

---

## 1. The rejected-suggestions catalogue

These are real suggestions produced by commercial resume-scoring tools and by
well-meaning automated advice, all of which were **rejected for being lies.** They
are collected here because the pattern is worth learning: fabrication advice
arrives in a confident, helpful, optimization-flavoured tone, and each item sounds
reasonable in isolation.

| Suggested | Why it was rejected |
|---|---|
| Put "Claude Corps Fellow" as a resume title | Claiming a title not held. The scoring tool's own help text said *"do not lie and say you have."* |
| "Analyzed Oil & Gas datasets **for government agencies**" | The tool literally wrote: *"framing your analytical work as being for government agencies aligns better."* The clients were not government agencies. That is a lie with a rationale attached. |
| "Volunteer work with local community organizations" | One specific NGO, two months. Pluralizing and genericizing inflates it into something that didn't happen. |
| "Professional Development: Onboarding Bootcamp with Anthropic" | A perk you would *receive if hired*, listed as a credential already earned. |
| Reframe the cyber-attack forecasting work as "public health outbreak prediction on anonymized health records" | KDDCup 1999 is a network-intrusion dataset, and the bullet links to the paper that disproves the reframing. |
| "Relevant coursework: Public Health Data Analysis / Civic Technology Applications" | The tool invented course titles. |
| "Developed a comprehensive runbook…" | Only permitted **after** the candidate confirmed he had actually written docs and runbooks. This is the right process: ask, then write. |
| "RAG chatbot using agent frameworks" (for HealthMate-AI) | HealthMate-AI is retrieval, not agents. Two real technologies, one false attribution. |
| "Implemented evals to cut inference cost ~40%" | **False causality.** Token budgeting cut the cost. Both facts true, the link invented. |

**The generalizable rule:** an optimization suggestion that increases your score by
changing *what happened* rather than *how it is described* is a fabrication, no
matter how it is framed. Score movement is not evidence of correctness.

For contrast — these moved a real resume's score from **46 to 93**, and every one
is a true statement:

1. Restored a Teaching Assistant role that had been cut when targeting a different
   job family — teaching was a core responsibility in the new posting.
2. Restored a bullet about an autonomous agent that had been cut for space.
3. Added a skills row named `LLM & Agent Frameworks` listing tools actually used.
4. Fixed the ligature extraction bug, which made "Artificial Intelligence" and
   "Certifications" machine-readable for the first time.
5. Adopted the employer's own vocabulary — "production LLM deployments", "evals",
   "training", "onboarding teammates" — everywhere a true statement supported it.
6. Cut padding, which let the font go **back up** from 8.75pt to 9.5pt.

Note what's in that list: restoring true things that had been cut, fixing a
technical bug, and changing words. Nothing was invented.

---

## 2. Situational edge cases

### Employment gaps
Don't hide them by reordering or by switching to year-only dates — parsers flag
both. Options: leave the gap and address it in the cover letter; or, if real work
happened (freelance, caregiving-adjacent study, open source), give it an honest
entry with an honest title.

### Career change / domain pivot
This is the one case where a Summary earns its lines. Lead the Projects section
with the target-domain projects, retitle them around the target capability, and use
the `transferable` framing from `gap-analysis.md`. Never restate the old domain as
the new one.

### Overqualified for the posting
Don't delete seniority — soften scope verbs ("Led" → "Built"), drop the most
senior-sounding bullet, and let the cover letter explain the motivation. Deleting
a real role to seem junior creates a gap that reads worse.

### Underqualified / stretch application
Say so in the verdict. Then maximize `adjacent` and `transferable` framings, lead
with projects, and list the genuine absences so the candidate can decide. Do not
close the gap with words.

### Short tenures
A two-month internship (`oasis`) is real and includable, but it invites "why so
short?". Include it when the content is JD-relevant and space allows; otherwise
it's the first cut.

### Contract / agency work
Format as `Title, Client (via Agency)`. Don't present the client as the employer.

### Confidential or NDA'd work
`Title, [Financial services company]` with the scale and method described but the
employer generalized. Never invent a plausible employer name.

### Academic → industry
Translate: "published" → "shipped and documented"; "grant" → "funded project";
"cohort" → "dataset". Keep publications — they're evidence of finishing things.
Cut the teaching load detail unless the JD wants mentoring.

### Conflicting source data
The ledger carries `conflict:` markers (e.g. a TA date range that differs between
two documents). **Never pick silently.** Ask the user; if they're unavailable,
choose the more authoritative source, mark it in the report, and flag it as
requiring confirmation before submission. A date that contradicts LinkedIn is a
credibility problem on its own.

### A metric the candidate can't defend
If the ledger's `defend:` question has no good answer, the honest options are: use
a different rung on the quantification ladder, or drop the number. A number that
collapses in the interview is worse than no number.

### The JD asks for years of experience the candidate lacks
Never inflate dates. Lead with density of relevant work and shipped artifacts.
Report the gap in the verdict — many "5+ years" lines are aspirational, but that's
the candidate's call to make with the facts in front of them.

### Multiple postings, one resume
Say clearly that a merged resume is tailored to neither. If the user insists,
target the *intersection* of required skills plus the *union* of hidden keywords,
and note the compromise.

### The user asks you to add something not in the ledger
This is normal and usually legitimate — the ledger is incomplete, not the person.
Ask the specific question ("did you actually write the runbooks, or just the
code?"), get the answer, **add it to the ledger with `verified: true`**, then use
it. The rule isn't "never add facts"; it's "never add facts the candidate hasn't
confirmed."

### The user asks you to add something they didn't do
Decline, explain why in one sentence, and offer the nearest true alternative. Don't
lecture. "I can't put Airflow on there since you haven't used it — but the Cloud
Scheduler → Run → Tasks work is genuinely the same category, and I can phrase it
so a reader recognizes that."

### Non-US conventions
Some markets expect a photo, date of birth, marital status, or a signature
(parts of continental Europe, Japan, parts of the Middle East). US and UK
conventions forbid these. Ask which market before applying US rules globally.

### Academic CV vs resume
A CV is multi-page, exhaustive, and publication-first. If the target is academic,
say that this skill's one-page constraint doesn't apply and switch structure:
`Education → Publications → Research Experience → Teaching → Grants → Service`.
