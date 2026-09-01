from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "market-reach-last-month"
OUTDIR.mkdir(exist_ok=True)

CATALOG = [
    ("AI Overwhelm Reset", "AI & productivity", 19.99),
    ("Prompt Fatigue Recovery", "AI & productivity", 18.49),
    ("Work From Home Boundary Planner", "Work-life balance", 17.99),
    ("Remote Burnout Recovery Sheet", "Work-life balance", 16.99),
    ("Hybrid Job Energy Tracker", "Work-life balance", 18.99),
    ("Freelance Cash Flow Stability", "Small business", 21.99),
    ("Gig Income Buffer Planner", "Small business", 19.99),
    ("Side Hustle Profit Snapshot", "Small business", 18.99),
    ("Emergency Savings Sprint", "Money & budgeting", 17.99),
    ("Rent Pressure Survival Guide", "Money & budgeting", 19.99),
    ("Housing Cost Anxiety Tracker", "Money & budgeting", 18.99),
    ("Inflation Budget Reset", "Money & budgeting", 19.49),
    ("Utility Cost Slashing Sheet", "Money & budgeting", 16.99),
    ("Debt Stress Recovery Plan", "Money & budgeting", 17.99),
    ("Healthcare Benefits Navigator", "Health & insurance", 22.99),
    ("Prescription Routine Organizer", "Health & insurance", 16.99),
    ("Caregiver Capacity Reset", "Caregiving", 19.99),
    ("New Parent Overwhelm Sheet", "Caregiving", 18.99),
    ("Family Admin Chaos Reset", "Caregiving", 17.99),
    ("Childcare Budget Survival", "Caregiving", 18.99),
    ("School Drop-Off Flow Planner", "Family systems", 16.99),
    ("Household Systems Dashboard", "Family systems", 18.99),
    ("Meal Planning Under Stress", "Family systems", 16.99),
    ("Home Energy Cost Tracker", "Home ops", 17.99),
    ("Home Safety & Routine Guide", "Home ops", 16.99),
    ("Neighborhood Emergency Prep", "Home ops", 17.99),
    ("Climate Anxiety Recovery", "Lifestyle & wellness", 16.99),
    ("Digital Detox Recovery Plan", "Lifestyle & wellness", 17.99),
    ("Phone Overload Reset", "Lifestyle & wellness", 16.49),
    ("Social Media Burnout Breaker", "Lifestyle & wellness", 18.99),
    ("Sleep Debt Recovery Guide", "Lifestyle & wellness", 17.99),
    ("Brain Fog Recovery Checker", "Health & wellness", 17.99),
    ("Neurodivergent Focus Reset", "Health & wellness", 18.99),
    ("Anxiety Relief Grounding Sheet", "Health & wellness", 16.99),
    ("Burnout Recovery 7-Day Plan", "Health & wellness", 18.49),
    ("Chronic Illness Energy Map", "Health & wellness", 19.99),
    ("Student Debt Reality Planner", "Education & career", 18.99),
    ("Career Pivot Survival Plan", "Education & career", 19.99),
    ("Professional Reentry Planner", "Education & career", 18.49),
    ("Interview Confidence Sprint", "Education & career", 17.99),
    ("Small Business Cost Survival", "Local business", 21.99),
    ("Retail Margin Recovery Sheet", "Local business", 20.99),
    ("Service Business Ops Checklist", "Local business", 19.99),
    ("Auto Repair Intake Plus Quote", "Local business", 20.99),
    ("Salon Client Flow Planner", "Local business", 18.99),
    ("Property Manager Itinerary", "Local business", 19.99),
    ("Database Cleanup Sprint", "Digital life", 15.99),
    ("Inbox Recovery Control Page", "Digital life", 15.99),
    ("Digital Files Reset Sheet", "Digital life", 16.49),
    ("Calendar Overload Fix", "Digital life", 16.99),
]

THEME_BY_GROUP = {
    "AI & productivity": {"bg": "#F2F7FF", "header": "#1B3A64", "accent": "#8AB7FF", "text": "#1B2640", "panel": "#EAF2FF"},
    "Work-life balance": {"bg": "#FFF9F2", "header": "#733D2A", "accent": "#E7B668", "text": "#2A1E1A", "panel": "#FDF0E5"},
    "Small business": {"bg": "#F8F7F3", "header": "#2E3B2F", "accent": "#C7B278", "text": "#1F2A20", "panel": "#EEF2EA"},
    "Money & budgeting": {"bg": "#F6FBF6", "header": "#1E5A4E", "accent": "#7BC6A4", "text": "#1E2D2B", "panel": "#EAF8F1"},
    "Health & insurance": {"bg": "#F6FAFC", "header": "#234B5C", "accent": "#77C7D7", "text": "#1B2D34", "panel": "#EAF7FB"},
    "Caregiving": {"bg": "#FFF9F5", "header": "#7A3B3B", "accent": "#F1B49A", "text": "#2E2020", "panel": "#FDEFEA"},
    "Family systems": {"bg": "#F9F6FF", "header": "#45386F", "accent": "#B29AE8", "text": "#2B2340", "panel": "#F1ECFF"},
    "Home ops": {"bg": "#F6F9F4", "header": "#344A2D", "accent": "#A8BE7B", "text": "#1D2B1C", "panel": "#EDF4E6"},
    "Lifestyle & wellness": {"bg": "#F9F4FF", "header": "#4D366B", "accent": "#CF9DF2", "text": "#2B1F3D", "panel": "#F3E9FF"},
    "Health & wellness": {"bg": "#F4FBFA", "header": "#1D4D57", "accent": "#6FC1B7", "text": "#1B2F34", "panel": "#E8F8F7"},
    "Education & career": {"bg": "#F9F9F3", "header": "#2A3E52", "accent": "#D9B76E", "text": "#1F2C38", "panel": "#F4F0E7"},
    "Local business": {"bg": "#F8F4EF", "header": "#3B382D", "accent": "#D4A05E", "text": "#1F1A15", "panel": "#F3EDE4"},
    "Digital life": {"bg": "#F3F7F9", "header": "#274F62", "accent": "#8CC5D9", "text": "#1D2F39", "panel": "#E8F4FA"},
}


def slugify(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = ''.join(ch if ch.isalnum() or ch in [' ', '-', '_'] else ' ' for ch in value)
    value = value.replace(' ', '-')
    return value.strip('-')


def make_pdf(path: Path, title: str, category: str, price: float) -> None:
    theme = THEME_BY_GROUP.get(category, {"bg": "#F7F9FB", "header": "#102B3D", "accent": "#D9B15D", "text": "#1E2A38", "panel": "#EBF1F7"})
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter

    c.setFillColor(colors.HexColor(theme["bg"]))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    c.setFillColor(colors.HexColor(theme["header"]))
    c.rect(0, h - 0.7 * inch, w, 0.7 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.58 * inch, h - 0.42 * inch, "Last-month demand trend bundle")

    c.setFillColor(colors.HexColor(theme["panel"]))
    c.roundRect(0.52 * inch, h - 2.5 * inch, w - 1.04 * inch, 1.0 * inch, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica-Bold", 25)
    title_lines = []
    current = ""
    for token in title.split():
        cand = f"{current} {token}".strip()
        if len(cand) <= 20:
            current = cand
        else:
            title_lines.append(current)
            current = token
    if current:
        title_lines.append(current)
    y = h - 1.8 * inch
    for line in title_lines[:2]:
        c.drawString(0.8 * inch, y, line)
        y -= 0.28 * inch

    c.setFillColor(colors.HexColor(theme["accent"]))
    c.roundRect(w - 2.25 * inch, h - 2.3 * inch, 1.25 * inch, 0.7 * inch, 0.12 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 15)
    c.drawString(w - 2.05 * inch, h - 1.95 * inch, f"${price:.2f}")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(0.6 * inch, 3.0 * inch, 2.4 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.88 * inch, 4.8 * inch, "Why people buy")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    bullets = [
        "Addresses a live pressure point.",
        "Offers a clear actionable fix.",
        "Can be used immediately in one sitting.",
        "Feels useful, premium, and practical.",
    ]
    y2 = 4.45 * inch
    for line in bullets:
        c.drawString(0.88 * inch, y2, line)
        y2 -= 0.22 * inch

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(3.35 * inch, 3.0 * inch, 2.5 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3.64 * inch, 4.8 * inch, "Buyer pull")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(3.64 * inch, 4.43 * inch, "- Relief from stress and overload")
    c.drawString(3.64 * inch, 4.18 * inch, "- Better control of time, money, or home")
    c.drawString(3.64 * inch, 3.93 * inch, "- More clarity with less chaos")
    c.drawString(3.64 * inch, 3.68 * inch, "- Fast action without learning curve")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(6.25 * inch, 3.0 * inch, 2.15 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(6.5 * inch, 4.8 * inch, "Best angle")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(6.5 * inch, 4.43 * inch, "One-page fix")
    c.drawString(6.5 * inch, 4.18 * inch, "Quick win")
    c.drawString(6.5 * inch, 3.93 * inch, "Premium clarity")
    c.drawString(6.5 * inch, 3.68 * inch, "Low-friction use")

    c.setFillColor(colors.HexColor(theme["header"]))
    c.roundRect(0.7 * inch, 0.9 * inch, w - 1.4 * inch, 1.05 * inch, 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.95 * inch, 1.58 * inch, "High-demand category: " + category)
    c.setFont("Helvetica", 10)
    c.drawString(0.95 * inch, 1.23 * inch, "Designed for immediate usability, premium framing, and broader reach across stress-heavy buyer groups.")

    c.save()


csv_path = OUTDIR / "market_reach_last_month.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "category", "price_usd", "filename"])
    for title, category, price in CATALOG:
        filename = f"{slugify(title)}.pdf"
        path = OUTDIR / filename
        make_pdf(path, title, category, price)
        writer.writerow([title, category, price, filename])

README = OUTDIR / "README.md"
README.write_text(
    "# Market Reach Last-Month Demand Bundle\n\n"
    "This set represents the most likely one-page digital products that are currently resonating across the last-month buying patterns: cost-of-living stress, AI/work overload, caregiving, healthcare navigation, digital burnout, and small-business ops.\n\n"
    "Note: this bundle is based on recent market demand signals and product patterns, not on direct access to a live storefront or sales ledger. Actual purchased PDFs can only be verified from your marketplace, Shopify, Gumroad, Etsy, or payment dashboard.\n\n"
    f"Total products: {len(CATALOG)}\n\n"
    "Categories covered:\n"
    "- AI & productivity\n"
    "- Work-life balance\n"
    "- Small business\n"
    "- Money & budgeting\n"
    "- Health & insurance\n"
    "- Caregiving\n"
    "- Family systems\n"
    "- Home ops\n"
    "- Lifestyle & wellness\n"
    "- Health & wellness\n"
    "- Education & career\n"
    "- Local business\n"
    "- Digital life\n"
)

print(f"Created {len(CATALOG)} PDFs in {OUTDIR}")
