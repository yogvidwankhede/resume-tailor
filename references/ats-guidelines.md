# ATS Guidelines

What applicant tracking systems actually do, and what that means for the document.

---

## 1. The mental model

An ATS is not an AI screener. In the common case it is:

1. A **text extractor** run over the uploaded file.
2. A **parser** that segments the extracted text into fields (name, contact, jobs,
   dates, schools, skills) using headings and layout heuristics.
3. A **matcher** that scores extracted text against a requisition's keyword list —
   usually substring / exact match, sometimes stemmed, occasionally embedding-based.
4. A **queue** a human recruiter reads, sorted by that score.

Three failure modes follow, in descending order of frequency:

- **Extraction failure** — the text never comes out of the file correctly.
- **Parse failure** — the text comes out but lands in the wrong field, or a whole
  role is dropped.
- **Match failure** — everything parsed, but the vocabulary didn't line up.

Most ATS advice online is about match failure. **Extraction failure is more
common, more silent, and more fatal.**

---

## 2. Extraction: the ligature bug

This is the single highest-value item in this file.

A PDF produced by LaTeX with default fonts renders "Artificial" correctly on
screen, but the `fi` is a **single ligature glyph**. If the font's ToUnicode map
doesn't cover it, an extractor gets `Articial`. The same bug eats:

- `Artificial` → `Articial`
- `Certifications` → `Certications`
- `classifier`, `classification` → `classier`, `classication`
- `efficiency`, `workflow`, `profile`, `fine-tuned`, `identify`
- Accented characters (`Thévenin`) become mojibake or vanish

Every one of those is a keyword. The resume looks perfect and scores near zero on
terms the candidate genuinely has.

**How likely is it?** It depends entirely on the toolchain. A current TeX Live with
`pdftotext` from a recent poppler usually extracts these correctly even without the
fix. Older TeX distributions, Overleaf's non-default font packages, and — more to
the point — the extraction libraries embedded in ATS products (many of which are
years-old PDFBox or iText builds) frequently do not. You cannot see which extractor
the employer runs. The three packages cost nothing, the check is one command, and
the failure mode is silent, so treat this as non-negotiable rather than optional.

**Fix (LaTeX):**

```latex
\usepackage{cmap}          % ToUnicode map — must come first
\usepackage[T1]{fontenc}   % single-glyph accented characters
\usepackage{lmodern}       % Latin Modern: ligatures map back to real letters
```

**Verify, every build:**

```bash
pdftotext resume.pdf - | grep -i "artificial\|certification\|classifi"
```

If those words don't come out whole, the resume is broken regardless of how it
looks. `scripts/ats_score.py --pdf` runs this check automatically.

**Non-LaTeX equivalents:** exporting from Word/Docs is generally safe. Exporting
from design tools (Figma, InDesign, Canva) frequently produces outlined text or
per-character positioning that extracts as garbage — always run `pdftotext` on
the result before trusting it.

---

## 3. Parse: layout rules

| Do | Don't |
|---|---|
| Single column, top-to-bottom | Two columns, sidebars |
| Standard section headings: `EDUCATION`, `EXPERIENCE`, `SKILLS`, `PROJECTS` | Creative headings: "Where I've Been", "My Toolkit" |
| Dates as `Month YYYY - Month YYYY` on the same line as the role | Dates in a separate column, or as `'21–'23` |
| Text bullets (`-` / `•`) | Nested bullets, custom dingbats, emoji |
| Contact info as plain text in the body | Contact info in a header/footer region (many parsers skip these) |
| Real text | Text inside images, logos, or charts |
| One page, one file | Multi-file portfolios, ZIPs |

Additional parse traps:

- **Tables** used for layout scramble reading order. The skills block in this
  template uses a two-column tabular; it extracts fine because it's a simple
  label→values map with no merged cells, but verify after any change.
- **Text boxes** are frequently skipped entirely.
- **Headers/footers** — put nothing you need parsed there.
- **Filename** — `Firstname_Lastname_Role.pdf`. Some systems display it to the
  recruiter. Never `resume_final_v7_ACTUAL.pdf`.
- **File format** — PDF unless the posting explicitly asks for .docx. If the
  posting asks for .docx, give it .docx; a wrong format is a real rejection cause.
- **Never submit a scanned or image-only PDF.**

---

## 4. Match: keyword strategy

### Density
Aim for each **required** term to appear **1–2 times**, in at least one substantive
context (a bullet), not only in the skills list. A term that appears only in the
skills block reads to a human as a claim without evidence, and to some parsers as
lower weight.

Three or more repetitions of the same term is stuffing: it's visible to the human
reader, it costs space, and modern systems penalize it.

### Placement
Weighted roughly: skills block ≈ job titles > first bullet of each role > later
bullets > project titles > project bullets. The top third of the page carries the
most weight both to parsers and to the human 20-second scan — which is why the
skills block sits above experience in this template.

### Spelling variants
Mirror the posting. When the posting uses both forms, use the long form once and
the short form elsewhere:

> "Retrieval-Augmented Generation (RAG) pipeline over 40K+ chunks… second RAG
> system deployed on Pinecone"

Common pairs to check: CI/CD ↔ CICD; ML ↔ machine learning; LLM ↔ large language
model; K8s ↔ Kubernetes; Postgres ↔ PostgreSQL; NLP ↔ natural language processing;
A/B ↔ AB ↔ experimentation.

### What never works
- **White text keyword stuffing.** Extraction sees it, the recruiter sees it in
  the parsed view, and it is a disqualification, not a trick.
- **A "Keywords" block at the bottom.** Reads as gaming; wastes space.
- **Listing the JD's tools you haven't used.** Passes the filter, fails the
  interview, and burns the referral.

---

## 5. Job titles

Use your real title. If the real title is internally idiosyncratic, you may add a
clarifying standard title in parentheses:

> ✅ `Member of Technical Staff (Software Engineer)`
> ✅ `Data Science Intern` → for an ML role, `Data Science Intern` stays; the
>    ledger's `title_variants` may be used only where the variant was also real
>    (e.g. LinkedIn lists this role as "Machine Learning Intern")
> ❌ Inventing `Machine Learning Engineer` for an internship titled `Data Science Intern`

Title inflation is the fabrication ATS advice most often encourages and the one
most easily caught by a reference check.

---

## 6. Dates and gaps

- Every role needs a start and end. `Present` for current.
- Consistent format across all entries. Mixed formats confuse date parsers and
  produce phantom gaps.
- Month-level precision. Year-only ranges read as concealment.
- Real gaps: don't hide them by shuffling order. A parser that sees non-chronological
  dates often flags the resume.

---

## 7. Pre-submission checklist

```
[ ] pdftotext extracts every keyword whole (esp. ligature words)
[ ] pdftotext output is in reading order, not scrambled
[ ] Every role has title, employer, and a parseable date range
[ ] Section headings are standard
[ ] Single column, no text boxes, no header/footer content
[ ] Contact info is plain text in the body
[ ] Filename is Firstname_Lastname_Role.pdf
[ ] Format matches what the posting asked for
[ ] Every required JD term appears 1–2 times, at least one in a bullet
[ ] No skill listed without ledger evidence
[ ] One page
```
