from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent

NAVY = colors.HexColor("#102B3D")
BLUE = colors.HexColor("#1A4D7A")
GOLD = colors.HexColor("#D9B15D")
TEAL = colors.HexColor("#188E8B")
LIGHT = colors.HexColor("#F4F7FB")
TEXT = colors.HexColor("#1E2A38")
MUTED = colors.HexColor("#5D6B7B")
WHITE = colors.white


def title_from_stem(stem: str) -> str:
    cleaned = stem.replace("_", " ").replace("-", " ")
    cleaned = re.sub(r"^\d+[\s._-]*", "", cleaned)
    cleaned = " ".join(cleaned.split())
    if not cleaned:
        return "Premium One-Page Tool"
    return cleaned.title()


def premium_lines(title: str) -> list[str]:
    base = [
        "Capture the essential task in one page.",
        "Highlight the priority actions first.",
        "Turn a simple process into a repeatable system.",
        "Make it easy to execute in under 10 minutes.",
        "Reduce mistakes, delay, and wasted effort.",
    ]
    title_tokens = title.split()
    if len(title_tokens) >= 3:
        refined = title_tokens[:3]
        return [
            "Install a clearer workflow for " + " ".join(refined).lower() + ".",
            "Use the page as a daily decision and execution tool.",
            "Track progress without extra admin or complex setup.",
            "Turn routine work into a premium operating system.",
            "Create a repeatable standard that supports better decisions.",
        ]
    return base


def build_pdf(path: Path, title: str, category: str) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter

    # Background and header.
    c.setFillColor(LIGHT)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    c.setFillColor(NAVY)
    c.rect(0, h - 0.7 * inch, w, 0.7 * inch, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.55 * inch, h - 0.38 * inch, "Premium 1-Page System")

    c.setFillColor(GOLD)
    c.roundRect(0.55 * inch, h - 1.05 * inch, 2.0 * inch, 0.25 * inch, 0.1 * inch, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.7 * inch, h - 0.92 * inch, category.upper())

    # Big title block.
    c.setFillColor(WHITE)
    c.roundRect(0.5 * inch, h - 2.7 * inch, w - 1.0 * inch, 1.05 * inch, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 24)
    lines = []
    current = ""
    for word in title.split():
        candidate = f"{current} {word}".strip()
        if len(candidate) <= 22:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    y = h - 2.34 * inch
    for line in lines[:2]:
        c.drawString(0.75 * inch, y, line)
        y -= 0.28 * inch

    # Right-side value strip.
    c.setFillColor(TEAL)
    c.roundRect(w - 2.25 * inch, h - 2.6 * inch, 1.55 * inch, 0.8 * inch, 0.16 * inch, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(w - 2.0 * inch, h - 2.22 * inch, "Higher")
    c.drawString(w - 2.0 * inch, h - 2.5 * inch, "Value")
    c.setFont("Helvetica", 9)
    c.drawString(w - 2.0 * inch, h - 2.7 * inch, "1-page system")

    # Content columns.
    left_x = 0.7 * inch
    right_x = 4.2 * inch
    box_w = 2.45 * inch
    box_h = 1.9 * inch
    gap = 0.12 * inch

    # Left column: Quick checklist.
    c.setFillColor(WHITE)
    c.setStrokeColor(colors.HexColor("#D9E2EC"))
    c.roundRect(left_x, 3.05 * inch, box_w, 2.65 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_x + 0.15 * inch, 5.38 * inch, "Quick Wins")
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 9.5)
    checklist = [
        "1. Clarify the goal before you start.",
        "2. Capture the highest-value action first.",
        "3. Standardize routine decisions and steps.",
        "4. Review progress before the next cycle.",
        "5. Repeat the process to improve speed.",
    ]
    y = 5.05 * inch
    for item in checklist:
        c.drawString(left_x + 0.2 * inch, y, item)
        y -= 0.27 * inch

    # Center column: Business value and operating flow.
    c.setFillColor(WHITE)
    c.setStrokeColor(colors.HexColor("#D9E2EC"))
    c.roundRect(right_x, 3.05 * inch, box_w, 2.65 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(right_x + 0.15 * inch, 5.38 * inch, "Why This Works")
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 9.5)
    value_lines = premium_lines(title)
    y = 5.05 * inch
    for item in value_lines[:4]:
        c.drawString(right_x + 0.2 * inch, y, item)
        y -= 0.27 * inch

    # Right column: execution cards.
    c.setFillColor(WHITE)
    c.setStrokeColor(colors.HexColor("#D9E2EC"))
    c.roundRect(w - 2.85 * inch, 3.05 * inch, 2.0 * inch, 2.65 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(w - 2.75 * inch, 5.38 * inch, "Action Plan")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(w - 2.75 * inch, 5.05 * inch, "Step 1")
    c.setFont("Helvetica", 9)
    c.drawString(w - 2.75 * inch, 4.85 * inch, "Define the priority task.")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(w - 2.75 * inch, 4.45 * inch, "Step 2")
    c.setFont("Helvetica", 9)
    c.drawString(w - 2.75 * inch, 4.25 * inch, "Track the essentials.")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(w - 2.75 * inch, 3.85 * inch, "Step 3")
    c.setFont("Helvetica", 9)
    c.drawString(w - 2.75 * inch, 3.65 * inch, "Improve the process.")

    # Bottom callout and metrics.
    c.setFillColor(NAVY)
    c.roundRect(0.6 * inch, 1.0 * inch, w - 1.2 * inch, 1.35 * inch, 0.16 * inch, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.9 * inch, 1.92 * inch, "Premium Outcome")
    c.setFont("Helvetica", 10)
    c.drawString(0.9 * inch, 1.55 * inch, "This one-page system creates clarity, speed, and a more valuable result without adding complexity.")

    c.setFillColor(GOLD)
    c.roundRect(5.9 * inch, 1.25 * inch, 0.95 * inch, 0.72 * inch, 0.12 * inch, fill=1, stroke=0)
    c.roundRect(7.0 * inch, 1.25 * inch, 0.95 * inch, 0.72 * inch, 0.12 * inch, fill=1, stroke=0)
    c.roundRect(8.1 * inch, 1.25 * inch, 0.95 * inch, 0.72 * inch, 0.12 * inch, fill=1, stroke=0)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(6.17 * inch, 1.65 * inch, "Fast")
    c.drawString(7.25 * inch, 1.65 * inch, "Clear")
    c.drawString(8.35 * inch, 1.65 * inch, "Useful")

    c.save()


def main() -> None:
    pdf_paths = sorted(ROOT.rglob("*.pdf"))
    if not pdf_paths:
        raise FileNotFoundError(f"No PDF files found under {ROOT}")

    for pdf_path in pdf_paths:
        title = title_from_stem(pdf_path.stem)
        parent = pdf_path.relative_to(ROOT).parts[:-1]
        category = parent[0] if parent else "Premium PDF"
        build_pdf(pdf_path, title, category)

    print(f"Premiumized {len(pdf_paths)} one-page PDFs under {ROOT}")


if __name__ == "__main__":
    main()
