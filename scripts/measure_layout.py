#!/usr/bin/env python3
"""
measure_layout.py — verify resume layout by measuring pixels, not by looking.

Renders a PDF page to an image, finds horizontal bands of ink, and reports the
leftmost dark pixel in each band. Section headings must all share the same left
edge; the classic LaTeX bug where the FIRST heading sits ~1.5em right of the
others is invisible at 100% zoom and obvious here.

    python scripts/measure_layout.py out/resume.pdf
    python scripts/measure_layout.py out/resume.pdf --top-fraction 0.35 --check-indent

Requires: pdftoppm (poppler-utils) and Pillow.

Decision rule: the first section heading's leftx must equal the leftx of the later
headings. Name and address are centered and show a large leftx — ignore those.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("Pillow required:  pip install pillow --break-system-packages\n")
    raise SystemExit(2)


def render(pdf: Path, dpi: int, outdir: Path) -> Path:
    if not shutil.which("pdftoppm"):
        sys.stderr.write("pdftoppm not found — install poppler-utils.\n")
        raise SystemExit(2)
    stem = outdir / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), "-f", "1", "-l", "1", str(pdf), str(stem)],
        check=True, capture_output=True,
    )
    pages = sorted(outdir.glob("page*.png"))
    if not pages:
        sys.stderr.write("pdftoppm produced no output.\n")
        raise SystemExit(2)
    return pages[0]


def bands(img: Image.Image, threshold: int, min_dark: int, min_height: int):
    """Yield (y0, y1, leftx, rightx) for each horizontal band containing ink."""
    g = img.convert("L")
    w, h = g.size
    px = g.load()

    rows = []
    for y in range(h):
        dark_x = [x for x in range(w) if px[x, y] < threshold]
        rows.append(dark_x if len(dark_x) > min_dark else [])

    out, y = [], 0
    while y < h:
        if not rows[y]:
            y += 1
            continue
        y0 = y
        xs: list[int] = []
        while y < h and rows[y]:
            xs.extend(rows[y])
            y += 1
        if y - y0 >= min_height and xs:
            out.append((y0, y, min(xs), max(xs)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--top-fraction", type=float, default=1.0,
                    help="only measure the top N fraction of the page (default: whole page)")
    ap.add_argument("--threshold", type=int, default=110)
    ap.add_argument("--min-dark", type=int, default=3,
                    help="minimum dark pixels in a row to count as ink")
    ap.add_argument("--min-height", type=int, default=5)
    ap.add_argument("--check-indent", action="store_true",
                    help="fail if the first left-aligned band differs from the modal left edge")
    args = ap.parse_args()

    pdf = Path(args.pdf)
    if not pdf.exists():
        sys.stderr.write(f"no such file: {pdf}\n")
        return 2

    with tempfile.TemporaryDirectory() as td:
        png = render(pdf, args.dpi, Path(td))
        img = Image.open(png)
        w, h = img.size
        if args.top_fraction < 1.0:
            img = img.crop((0, 0, w, int(h * args.top_fraction)))
        rows = bands(img, args.threshold, args.min_dark, args.min_height)

    print(f"page: {w}x{h} px @ {args.dpi} dpi   bands: {len(rows)}\n")
    print(f"{'band':>4}  {'y0':>5} {'y1':>5}  {'leftx':>6} {'rightx':>6}  note")
    lefts: list[int] = []
    for i, (y0, y1, lx, rx) in enumerate(rows):
        centered = lx > w * 0.18 and (w - rx) > w * 0.18
        note = "centered (name/address?)" if centered else ""
        if not centered:
            lefts.append(lx)
        print(f"{i:>4}  {y0:>5} {y1:>5}  {lx:>6} {rx:>6}  {note}")

    if lefts:
        modal = max(set(lefts), key=lefts.count)
        outliers = sorted({x for x in lefts if abs(x - modal) > 3})
        print(f"\nmodal left edge: {modal}px")
        if outliers:
            print(f"left-edge outliers: {outliers}")
            print("  -> Bullet items legitimately sit a few px right of the modal edge;")
            print("     that is expected. What matters is the FIRST left-aligned band:")
            print("     if it is an outlier, that is the indented-first-heading bug.")
            print("     Fix with \\setlength{\\parindent}{0pt} in the preamble, not \\noindent.")
        else:
            print("all left-aligned bands share the same left edge — no indent bug")

        if args.check_indent and lefts and abs(lefts[0] - modal) > 3:
            print("\nFAIL: first left-aligned band is indented relative to the rest.")
            return 1

    if rows:
        last_y = rows[-1][1]
        fill = last_y / (h * args.top_fraction)
        print(f"\nvertical fill: {fill:.1%} of the measured region")
        if args.top_fraction >= 1.0:
            if fill < 0.90:
                print("  -> page is under-filled; you have room for another bullet")
            elif fill > 0.99:
                print("  -> page is at the edge; check the log for a 2-page overflow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
