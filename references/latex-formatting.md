# LaTeX Formatting & One-Page Fitting

The layout in `assets/resume-master.tex` is the output of a measured sweep, not
taste. This file records what was tested, what won, and why — so the settings
survive future edits.

---

## 1. The formatting philosophy

> **Cut content, never shrink the font below 9.5pt.**

Every instinct under space pressure is to tighten leading, shrink type, and crush
bullet spacing. That direction was tested to its end and reversed. A page at 8.75pt
with `\linespread{0.86}` fits more words and reads as desperate; a page at 9.5pt
with real gaps between entries reads as edited. Editing is the signal.

The corollary: **the fitting mechanism is deletion.** When a tailored resume
overflows, the answer is in `gap-analysis.md` § Space budget, not in this file.

---

## 2. Settings, and why each one

| Setting | Value | Why |
|---|---|---|
| Base class size | `\input{size10.clo}` inside `\makeatletter…\makeatother` | `resume.cls` hardcodes 11pt and doesn't accept a class option. This forces 10pt without forking the class. |
| geometry load order | **after** the size change | Otherwise the class's own margins win and the geometry call is silently ignored. |
| Margins | `left=0.3in, top=0.14in, right=0.3in, bottom=0.13in` | Tested floor. Below ~0.25in some printers and some PDF viewers clip. |
| Body font | `\fontsize{9.5}{10.0}\selectfont` | 9.5pt is the readability floor. 10.0pt leading is the tightest that doesn't look mashed at that size. |
| `\linespread` | `1.0` | Swept at 0.86 / 0.88 / 0.90 / 0.92 and abandoned. Tightening leading buys ~2 lines and costs more legibility than deleting one bullet. |
| `\parindent` | `0pt` in the preamble | The **only** correct fix for the indented first heading (see § 3). |
| `\namesize` | `\LARGE` | `\huge` wastes a line and the name is not the point. |
| `nameskip` / `addressskip` / `sectionskip` / `sectionlineskip` | `\smallskip` | Class defaults are `\bigskip`/`\medskip` — roughly 4 wasted lines across the page. |
| `\setlist[itemize]` | `nosep, left=0pt` | Kills enumitem's default vertical padding and the left gutter. |
| Per-list | `[itemsep=1.5pt, topsep=2pt]` | **Positive**, deliberately. Earlier versions used `-2pt`; the negative value is what a crushed page looks like. |
| Between experience entries | `\vspace{0.15em}` | Also positive. Entry separation is what makes the page scannable. |
| Section pull-ups | `-0.7` to `-0.95em`; PROJECTS `-1.8em` | `rSection` emits a rule plus a `\smallskip`; these cancel it. PROJECTS needs more because its `\item` sits outside a list environment. |
| Tabular row spacing | `\\[0.2em]` | A bare `\vspace` between tabular rows is absorbed into the next row's first cell and does nothing. This trips people up every time. |
| Education entry spacing | `\\[0.35em]` | Same mechanism. |
| hyperref | `[hidelinks]` | Coloured link boxes print badly and add visual noise. |

---

## 3. The indented-first-heading bug

**Symptom:** `EDUCATION` sits ~1.5em to the right of `SKILLS`/`EXPERIENCE`/`PROJECTS`.

**Cause:** the `\vspace{-0.7em}` immediately after `\begin{document}` starts a
paragraph, so `\parindent` fires on the first `rSection`.

Six fixes were built and pixel-measured:

| Variant | Intervention | Result |
|---|---|---|
| A | drop the `\vspace` entirely | fixes indent, loses the pull-up |
| B | `\vspace*{-0.7em}` | no |
| C | `\par\vspace{-0.7em}` | no |
| D | `\null\vspace{-0.7em}` | no |
| E | `\vspace{-0.7em}\noindent` | fixes this instance only; fragile |
| **F** | **`\setlength{\parindent}{0pt}` in the preamble** | **fixes it globally and keeps the pull-up** |

**F wins.** Use `\parindent=0pt`. Do not patch with `\noindent`.

---

## 4. Verify layout by measurement, not by looking

Eyeballing a PDF at 100% zoom will not reliably tell you whether two headings are
flush. `scripts/measure_layout.py` renders the PDF to PNG, thresholds it, finds
horizontal ink bands, and reports the leftmost dark pixel per band.

```bash
python scripts/measure_layout.py out/resume.pdf --top-fraction 0.35
```

Decision rule: **the first section heading's `leftx` must equal the `leftx` of the
later headings.** Name and address are centered, so they show a large `leftx` and
are ignored. Anything else is the indent bug.

Also use it to check the page is genuinely full but not overflowing — the last ink
band's `y` should be within ~40px of the bottom margin.

---

## 5. The build loop

```bash
pdflatex -interaction=nonstopmode resume.tex
pdflatex -interaction=nonstopmode resume.tex     # twice, for \hfill and refs

grep -E "Overfull|Underfull|Warning" resume.log
pdftotext resume.pdf - | head -60                 # extraction sanity
python scripts/measure_layout.py resume.pdf       # layout sanity
```

**Log lines that matter:**

- `Output written on resume.pdf (1 page, …)` — the one-page target. **2 pages is a
  failed build**, not a stylistic choice.
- `Overfull \hbox (Xpt too wide)` — a line runs into the margin. Under ~5pt is
  usually invisible; over ~15pt is visible and must be fixed by shortening the text
  (not by `\sloppy`). The header address line is the usual offender when a link is
  added.
- `Package cmap Warning: fontenc already loaded` — `cmap` must be loaded **before**
  `fontenc`, or some fonts go unprocessed and the ligature fix is partial.

Note on the ligature fix: on a current TeX Live with a recent poppler, extraction
often succeeds even without `cmap`/`fontenc`/`lmodern`. That is not a reason to drop
them. The extractors inside ATS products are frequently years-old PDFBox or iText
builds, you can't see which one the employer runs, and the failure is silent. Keep
the three lines and keep running the `pdftotext` check.

---

## 6. Building without `resume.cls`

If `resume.cls` isn't available, this preamble reproduces the same output on stock
`article`:

```latex
\documentclass[10pt,letterpaper]{article}
\usepackage[left=0.3in,top=0.14in,right=0.3in,bottom=0.13in]{geometry}
\usepackage{cmap}\usepackage[T1]{fontenc}\usepackage{lmodern}
\usepackage[hidelinks]{hyperref}\usepackage{enumitem}\usepackage{titlesec}
\setlist[itemize]{nosep, left=0pt}
\setlength{\parindent}{0pt}\pagestyle{empty}\linespread{1.0}

\titleformat{\section}{\large\bfseries}{}{0pt}{}[\vspace{-0.6em}\hrule\vspace{-0.2em}]
\titlespacing{\section}{0pt}{0.6em}{0.2em}

\newcommand{\resumename}[1]{\begin{center}{\LARGE\bfseries #1}\end{center}\vspace{-0.6em}}
\newcommand{\resumecontact}[1]{\begin{center}#1\end{center}\vspace{-0.4em}}
```

Then `\section{EDUCATION}` in place of `\begin{rSection}{\large EDUCATION}`. The
negative `\vspace` values in the master template are tuned for `rSection` and
should be re-measured after switching.

---

## 7. Changing the template safely

1. Change one thing.
2. Rebuild twice, read the log.
3. Run `measure_layout.py`.
4. Run `pdftotext` and check the ligature words.
5. Confirm still one page.

Do not batch layout changes. The negative `\vspace` values interact, and a stack of
simultaneous edits makes the regression un-bisectable.

**Never remove**, under any circumstance: `cmap`, `fontenc`, `lmodern`,
`\parindent=0pt`, or the `\fontsize{9.5}{10.0}` floor.
