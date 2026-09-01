from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent

THEME_BY_CATEGORY = {
    "AI & productivity": {"bg": "#F5F8FF", "header": "#1F4475", "accent": "#8FB4F1", "text": "#1E2E45", "panel": "#EAF2FF"},
    "Work-life balance": {"bg": "#FFF9F2", "header": "#7A3F36", "accent": "#E6B473", "text": "#2B1F1B", "panel": "#FDEFE7"},
    "Small business": {"bg": "#F7F9F4", "header": "#2E5045", "accent": "#A3C6A4", "text": "#1D2E28", "panel": "#ECF5ED"},
    "Money & budgeting": {"bg": "#F7FBF7", "header": "#1E5B4D", "accent": "#78C7A9", "text": "#1E2E2B", "panel": "#EAF8F2"},
    "Health & insurance": {"bg": "#F6FAFC", "header": "#234B5D", "accent": "#7FC5CF", "text": "#1A2D35", "panel": "#EAF8FB"},
    "Caregiving": {"bg": "#FFF9F6", "header": "#7A4342", "accent": "#F0B39D", "text": "#2D1D1C", "panel": "#FDEEE9"},
    "Family systems": {"bg": "#F9F7FF", "header": "#4A3A73", "accent": "#BAA5E7", "text": "#29223D", "panel": "#F1EAFF"},
    "Home ops": {"bg": "#F8F9F5", "header": "#385135", "accent": "#A4C39A", "text": "#1C2B1E", "panel": "#EBF4EA"},
    "Lifestyle & wellness": {"bg": "#FAF5FF", "header": "#4A3767", "accent": "#C39DE6", "text": "#2B213A", "panel": "#F1E7FF"},
    "Health & wellness": {"bg": "#F3FBFA", "header": "#1F4F5A", "accent": "#78C4BE", "text": "#1D3036", "panel": "#E9F9F7"},
    "Education & career": {"bg": "#F8F8F3", "header": "#2E485C", "accent": "#D7B66F", "text": "#1F2B34", "panel": "#F4F0E8"},
    "Local business": {"bg": "#F9F6F0", "header": "#41382D", "accent": "#D6A467", "text": "#201B17", "panel": "#F3EDE2"},
    "Digital life": {"bg": "#F3F8FB", "header": "#2D5266", "accent": "#83C0CE", "text": "#1D2E36", "panel": "#EAF6F9"},
    "AI productivity": {"bg": "#F5F8FF", "header": "#1F4475", "accent": "#8FB4F1", "text": "#1E2E45", "panel": "#EAF2FF"},
    "Business ops": {"bg": "#F6F9F6", "header": "#2F5349", "accent": "#87C0AC", "text": "#1B2E29", "panel": "#ECF7F3"},
    "Finance": {"bg": "#F8FAF4", "header": "#285748", "accent": "#A5C89E", "text": "#1E2D2A", "panel": "#ECF5ED"},
    "Healthcare": {"bg": "#F3FAFB", "header": "#1E5365", "accent": "#7FBCCB", "text": "#1A2F37", "panel": "#EAF7FA"},
    "Legal": {"bg": "#F4F5F2", "header": "#20372B", "accent": "#BDB28C", "text": "#1A241D", "panel": "#EEF1EA"},
    "Home services": {"bg": "#F8F8F3", "header": "#44543B", "accent": "#C2C982", "text": "#212B1D", "panel": "#EFF3E8"},
    "Real estate": {"bg": "#F9F7F2", "header": "#4B3C29", "accent": "#D5A76D", "text": "#292117", "panel": "#F4EBDC"},
    "Marketing": {"bg": "#F7F9FF", "header": "#2D457A", "accent": "#9ABAF1", "text": "#1B2541", "panel": "#EAF1FF"},
    "Community": {"bg": "#F8F8F0", "header": "#4D4E39", "accent": "#C4C989", "text": "#252B1E", "panel": "#F2F1E6"},
    "Technology": {"bg": "#F5F9FB", "header": "#35596B", "accent": "#7CBFC2", "text": "#1B2E36", "panel": "#E9F6F9"},
    "Lifestyle": {"bg": "#FFF9F8", "header": "#6B4158", "accent": "#E7A4B4", "text": "#2C1E21", "panel": "#FDEEF1"},
    "Digital business": {"bg": "#F5F8FF", "header": "#2C4477", "accent": "#9ABCF5", "text": "#1B2540", "panel": "#EBF2FF"},
    "Freelance": {"bg": "#F8F7FF", "header": "#3A4274", "accent": "#A8AEEB", "text": "#232845", "panel": "#EDEEFF"},
    "Senior care": {"bg": "#F8F6F2", "header": "#594A3C", "accent": "#D9B888", "text": "#2A221B", "panel": "#F0EAE0"},
    "Wellness": {"bg": "#FAF5FF", "header": "#4E3868", "accent": "#BFA4E4", "text": "#2A213B", "panel": "#F1E9FF"},
    "Pet care": {"bg": "#FFF8F5", "header": "#7D413E", "accent": "#F2BAA7", "text": "#2D1D1D", "panel": "#FDEFEA"},
    "Events": {"bg": "#FFF9F3", "header": "#734B32", "accent": "#E4B77D", "text": "#2D1F1A", "panel": "#FDEFE2"},
    "Hospitality": {"bg": "#FFF8F5", "header": "#7A1F1F", "accent": "#E5AF77", "text": "#2E1919", "panel": "#FDEAE2"},
    "default": {"bg": "#F7F9FB", "header": "#102B3D", "accent": "#D9B15D", "text": "#1E2A38", "panel": "#EBF1F7"},
}


def make_price_pdf(path: Path, title: str, category: str, price: float) -> None:
    theme = THEME_BY_CATEGORY.get(category, THEME_BY_CATEGORY["default"])
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter

    c.setFillColor(colors.HexColor(theme["bg"]))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    c.setFillColor(colors.HexColor(theme["header"]))
    c.rect(0, h - 0.75 * inch, w, 0.75 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.58 * inch, h - 0.42 * inch, "Competitive price")

    c.setFillColor(colors.HexColor(theme["panel"]))
    c.roundRect(0.52 * inch, h - 2.45 * inch, w - 1.04 * inch, 1.0 * inch, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica-Bold", 24)
    lines = []
    current = ""
    for word in title.split():
        cand = f"{current} {word}".strip()
        if len(cand) <= 18:
            current = cand
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    y = h - 1.82 * inch
    for line in lines[:2]:
        c.drawString(0.78 * inch, y, line)
        y -= 0.28 * inch

    c.setFillColor(colors.HexColor(theme["accent"]))
    c.roundRect(w - 2.15 * inch, h - 2.28 * inch, 1.3 * inch, 0.72 * inch, 0.14 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(w - 1.92 * inch, h - 1.94 * inch, f"${price:.2f}")

    c.setFillColor(colors.HexColor(theme["header"]))
    c.roundRect(0.75 * inch, 0.92 * inch, w - 1.5 * inch, 1.1 * inch, 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(0.98 * inch, 1.62 * inch, "Category: " + category)
    c.setFont("Helvetica", 10)
    c.drawString(0.98 * inch, 1.28 * inch, "Competitive, market-aligned pricing for fast buyer conversion.")

    c.save()


def main() -> None:
    for bundle_dir in sorted(ROOT.glob("market-reach-*")):
        csv_path = next(bundle_dir.glob("*.csv"), None)
        if not csv_path:
            continue
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for row in rows:
            title = (row.get("title") or row.get("product") or row.get("Product") or "Premium One-Page PDF").strip()
            category = (row.get("category") or row.get("Category") or "default").strip()
            price = float(row.get("price_usd") or row.get("price") or 14.99)
            filename = row.get("filename") or row.get("file") or ""
            if not filename:
                continue
            pdf_path = bundle_dir / filename
            if pdf_path.exists():
                make_price_pdf(pdf_path, title, category, price)
    print("Updated competitive price badge on all market-reach PDFs")


if __name__ == "__main__":
    main()
