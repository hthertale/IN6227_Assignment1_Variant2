#!/usr/bin/env python3
"""Deterministic QA for the generated IN6227 report PDF.

Usage:
  python scripts/check_report.py IN6227_variant2_report.pdf

Checks page count, required headings, numbered Methods steps, common
unsupported claims, and basic PDF text-geometry overlap/clipping when
PyMuPDF is available. It does not judge writing quality.
"""
import shutil
import subprocess
import sys
from pathlib import Path

HEADINGS = [
    "INTRODUCTION",
    "METHODS OR PROCEDURES",
    "RESULTS",
    "DISCUSSION",
    "CONCLUSION",
    "REFERENCES",
]


def page_count(pdf: Path):
    try:
        import pypdf  # type: ignore
        reader = pypdf.PdfReader(str(pdf))
        return len(reader.pages)
    except Exception:
        pass
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        out = subprocess.check_output([pdfinfo, str(pdf)], text=True, stderr=subprocess.STDOUT)
        for line in out.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":", 1)[1].strip())
    return None


def extract_text(pdf: Path):
    try:
        import pypdf  # type: ignore
        reader = pypdf.PdfReader(str(pdf))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        pass
    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        return subprocess.check_output([pdftotext, str(pdf), "-"], text=True, stderr=subprocess.STDOUT)
    return None


def geometry_warnings(pdf: Path):
    """Return basic warnings for overlapping text blocks or page spill.

    These are heuristics. Tables and same-line spans can legitimately touch,
    so only flag substantial overlap between different text blocks.
    """
    try:
        import fitz  # type: ignore
    except Exception:
        return ["PyMuPDF unavailable; visual overlap/clipping inspection required"]

    warnings = []
    doc = fitz.open(str(pdf))
    for pno, page in enumerate(doc, start=1):
        rect = page.rect
        blocks = page.get_text("blocks")
        text_blocks = []
        for b in blocks:
            x0, y0, x1, y1, text = b[:5]
            if not text.strip():
                continue
            r = fitz.Rect(x0, y0, x1, y1)
            text_blocks.append((r, text.strip()))
            if r.x0 < -0.5 or r.y0 < -0.5 or r.x1 > rect.x1 + 0.5 or r.y1 > rect.y1 + 0.5:
                warnings.append(f"page {pno}: text block extends beyond page bounds")

        for i, (a, ta) in enumerate(text_blocks):
            for b, tb in text_blocks[i + 1 :]:
                inter = a & b
                if inter.is_empty:
                    continue
                # Ignore tiny contact at boundaries; flag substantive overlap.
                inter_area = max(0.0, inter.get_area())
                smaller = max(1.0, min(a.get_area(), b.get_area()))
                if inter_area / smaller > 0.08:
                    warnings.append(
                        f"page {pno}: possible text overlap between blocks "
                        f"{ta[:35]!r} and {tb[:35]!r}"
                    )
    return warnings


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/check_report.py REPORT.pdf")
    pdf = Path(sys.argv[1])
    if not pdf.exists():
        raise SystemExit(f"ERROR: file not found: {pdf}")

    pages = page_count(pdf)
    text = extract_text(pdf)
    print(f"PDF: {pdf}")
    print(f"Pages: {pages if pages is not None else 'UNKNOWN (no PDF parser available)'}")
    if pages is not None and pages > 2:
        print("FAIL: report exceeds the two-page limit")
    else:
        print("PASS: page-count check")

    if text is not None:
        missing = [h for h in HEADINGS if h not in text.upper()]
        if missing:
            print("FAIL: missing main headings:", ", ".join(missing))
        else:
            print("PASS: required main headings detected")

        upper = text.upper()
        if "METHODS OR PROCEDURES" in upper:
            methods_pos = upper.find("METHODS OR PROCEDURES")
            results_pos = upper.find("RESULTS", methods_pos + 1)
            if results_pos != -1:
                methods_block = text[methods_pos:results_pos]
                expected_steps = ["1.", "2.", "3.", "4.", "5.", "6.", "7."]
                missing_steps = [x for x in expected_steps if x not in methods_block]
                if missing_steps:
                    print("WARN: numbered Methods workflow may be incomplete:", ", ".join(missing_steps))
                else:
                    print("PASS: numbered Methods workflow detected")

        if "CALIBR" in upper:
            print("WARN: calibration language detected; verify that a calibration metric/curve was actually computed")
        if "LOWEST" in upper and "COST" in upper:
            print("WARN: cost-superlative language detected; verify that runtime/cost was actually measured")
    else:
        print("WARN: could not extract PDF text; inspect headings manually")

    warnings = geometry_warnings(pdf)
    if warnings:
        print("RENDERING QA WARNINGS:")
        for w in warnings[:20]:
            print(" -", w)
        if len(warnings) > 20:
            print(f" - ... {len(warnings) - 20} more")
    else:
        print("PASS: no obvious text-overlap/page-spill issues detected by geometry heuristic")


if __name__ == "__main__":
    main()
