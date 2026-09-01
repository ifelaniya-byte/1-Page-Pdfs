from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "market-reach-more-6"
OUTDIR.mkdir(exist_ok=True)

CATALOG = [
    ("Owner Salary Calculator", "Small business", 19.99),
    ("Business Tax Prep Checklist", "Small business", 18.99),
    ("Vendor Margin Review", "Small business", 17.99),
    ("Operating Cash Snapshot", "Small business", 18.99),
    ("Business Expense Audit", "Small business", 17.99),
    ("Monthly P&L Sheet", "Small business", 19.99),
    ("Payroll Planning Sheet", "Small business", 18.99),
    ("Owner Burnout Reset", "Small business", 18.99),
    ("Sales Forecast Planner", "Small business", 19.99),
    ("Client Retention Scorecard", "Small business", 18.99),
    ("Homeowner Repair Planner", "Home services", 17.99),
    ("Bathroom Renovation Checklist", "Home services", 18.99),
    ("Kitchen Upgrade Planner", "Home services", 18.99),
    ("Exterior Paint Planner", "Home services", 17.99),
    ("Drywall Repair Checklist", "Home services", 17.99),
    ("Tile Installation Guide", "Home services", 16.99),
    ("Appliance Repair Tracker", "Home services", 17.99),
    ("Furniture Assembly Sheet", "Home services", 15.99),
    ("HVAC Filter Reminder", "Home services", 15.99),
    ("Home Maintenance Calendar", "Home services", 16.99),
    ("Estate Planning Basics", "Legal", 20.99),
    ("Trust Funding Checklist", "Legal", 19.99),
    ("Power of Attorney Guide", "Legal", 19.99),
    ("Will Review Prep Sheet", "Legal", 18.99),
    ("Beneficiary Update Sheet", "Legal", 18.99),
    ("Debt Settlement Guide", "Legal", 19.99),
    ("Family Business Succession", "Legal", 20.99),
    ("Real Estate Closing Checklist", "Legal", 19.99),
    ("Business Partnership Review", "Legal", 20.99),
    ("Asset Protection Planner", "Legal", 21.99),
    ("Family Budget Recovery", "Finance", 17.99),
    ("Emergency Savings Tracker", "Finance", 16.99),
    ("Mortgage Prep Checklist", "Finance", 17.99),
    ("Budget Freeze Sheet", "Finance", 16.99),
    ("Debt Payoff Sprint", "Finance", 17.99),
    ("Cash Reserve Planner", "Finance", 18.99),
    ("Income Stabilizer Sheet", "Finance", 17.99),
    ("Annual Expense Reset", "Finance", 18.99),
    ("Sinking Fund Tracker", "Finance", 17.99),
    ("Bill Due Timeline", "Finance", 16.99),
    ("Postpartum Recovery Sheet", "Healthcare", 18.99),
    ("Baby Feeding Tracker", "Healthcare", 16.99),
    ("New Parent Daily Planner", "Healthcare", 17.99),
    ("Birth Recovery Checklist", "Healthcare", 18.99),
    ("School Readiness Checklist", "Healthcare", 16.99),
    ("Family Health Snapshot", "Healthcare", 17.99),
    ("Vaccination Tracker", "Healthcare", 16.99),
    ("Baby Sleep Schedule", "Healthcare", 17.99),
    ("Child Health Log", "Healthcare", 15.99),
    ("Family Wellness Calendar", "Healthcare", 17.99),
    ("Client Follow-Up Sequence", "Marketing", 17.99),
    ("Offer Positioning Sheet", "Marketing", 18.99),
    ("Brand Promise Checklist", "Marketing", 16.99),
    ("Sales Page Audit", "Marketing", 17.99),
    ("Customer Persona Snapshot", "Marketing", 16.99),
    ("Ad Creative Review Sheet", "Marketing", 17.99),
    ("Landing Page Headline Test", "Marketing", 16.99),
    ("List Building Tracker", "Marketing", 17.99),
    ("Lead Magnet Conversion Check", "Marketing", 16.99),
    ("Email Campaign Planner", "Marketing", 18.99),
    ("Caregiver Support Network", "Community", 16.99),
    ("Local Support Directory", "Community", 15.99),
    ("Neighborhood Help Board", "Community", 15.99),
    ("Volunteer Matching Sheet", "Community", 16.99),
    ("Family Resource Board", "Community", 15.99),
    ("Senior Support Circle", "Community", 16.99),
    ("Community Meal Schedule", "Community", 15.99),
    ("School Parent Network", "Community", 16.99),
    ("Local Resource Guide", "Community", 15.99),
    ("Family Help Tracker", "Community", 16.99),
    ("Senior Tech Setup Tracker", "Technology", 17.99),
    ("Password Recovery Guide", "Technology", 15.99),
    ("Device Battery Health Check", "Technology", 15.99),
    ("Smart Home Setup Sheet", "Technology", 16.99),
    ("Wifi Troubleshooting Guide", "Technology", 15.99),
    ("Phone Backup Checklist", "Technology", 15.99),
    ("Tablet Learning Path", "Technology", 16.99),
    ("Online Safety Checklist", "Technology", 15.99),
    ("Laptop Setup Planner", "Technology", 16.99),
    ("Digital Literacy Starter", "Technology", 17.99),
    ("Salon Service Planner", "Lifestyle", 16.99),
    ("Beauty Product Inventory", "Lifestyle", 15.99),
    ("Self-Care Routine Sheet", "Lifestyle", 15.99),
    ("Routine Beauty Schedule", "Lifestyle", 16.99),
    ("Client Booking Checklist", "Lifestyle", 16.99),
    ("Spa Treatment Tracker", "Lifestyle", 17.99),
    ("At-Home Glow Routine", "Lifestyle", 15.99),
    ("Wellness Gift Planning", "Lifestyle", 16.99),
    ("Personal Care Budget", "Lifestyle", 15.99),
    ("Luxury Self-Care Planner", "Lifestyle", 18.99),
    ("Business Website Audit", "Digital business", 18.99),
    ("Landing Page Checklist", "Digital business", 17.99),
    ("Client Portal Setup", "Digital business", 18.99),
    ("Membership Funnel Planner", "Digital business", 19.99),
    ("Website Lead Capture Sheet", "Digital business", 18.99),
    ("Page Speed Fix Plan", "Digital business", 17.99),
    ("Online Service Menu", "Digital business", 16.99),
    ("Booking Flow Review", "Digital business", 17.99),
    ("Website Refresh Planner", "Digital business", 18.99),
    ("Digital Sales Funnel Sheet", "Digital business", 19.99),
    ("Freelance Onboarding Tracker", "Freelance", 17.99),
    ("Project Scope Tracker", "Freelance", 17.99),
    ("Client Communication Log", "Freelance", 16.99),
    ("Proposal Follow-Up Sheet", "Freelance", 16.99),
    ("Contract Renewal Planner", "Freelance", 17.99),
    ("Referral Ask Script", "Freelance", 15.99),
    ("Service Delivery Checklist", "Freelance", 16.99),
    ("Weekly Client Review", "Freelance", 16.99),
    ("Rate Increase Planner", "Freelance", 18.99),
    ("Client Win Tracker", "Freelance", 17.99)
]

THEME_MAP = {
    "Small business": {"bg": "#F7F9F5", "header": "#2F4B44", "accent": "#A0C2A0", "text": "#1E2C29", "panel": "#ECF5EE"},
    "Home services": {"bg": "#F8F8F3", "header": "#44543A", "accent": "#B9C986", "text": "#212C1B", "panel": "#EEF3E5"},
    "Legal": {"bg": "#F5F5F3", "header": "#20362B", "accent": "#C1B494", "text": "#1A241E", "panel": "#EFF0EB"},
    "Finance": {"bg": "#F8FAF4", "header": "#274F3E", "accent": "#9DC7A4", "text": "#1F2B26", "panel": "#ECF5EE"},
    "Healthcare": {"bg": "#F3FAFB", "header": "#1E5365", "accent": "#82C0CD", "text": "#1C2E35", "panel": "#EAF8FA"},
    "Marketing": {"bg": "#F7F9FF", "header": "#2D467C", "accent": "#9CB9F2", "text": "#1B2641", "panel": "#EBF1FF"},
    "Community": {"bg": "#F8F8F0", "header": "#4A4D36", "accent": "#C5C98A", "text": "#242B1B", "panel": "#F2F1E4"},
    "Technology": {"bg": "#F5F9FB", "header": "#355A6A", "accent": "#7CBFC0", "text": "#1B2E36", "panel": "#EAF6F8"},
    "Lifestyle": {"bg": "#FFF9F8", "header": "#6A4054", "accent": "#EAA4B2", "text": "#2B1D20", "panel": "#FDEEF2"},
    "Digital business": {"bg": "#F5F8FF", "header": "#2C4476", "accent": "#9ABCF4", "text": "#1C2640", "panel": "#EBF1FF"},
    "Freelance": {"bg": "#F8F7FF", "header": "#3B4275", "accent": "#A8AEEB", "text": "#232946", "panel": "#EDEEFF"},
    "default": {"bg": "#F7F9FB", "header": "#102B3D", "accent": "#D9B15D", "text": "#1E2A38", "panel": "#EBF1F7"},
}


def slugify(value: str) -> str:
    value = value.lower()
    value = ''.join(ch if ch.isalnum() or ch in [' ', '-', '_'] else ' ' for ch in value)
    value = value.replace(' ', '-')
    return value.strip('-')


def build_pdf(path: Path, title: str, category: str, price: float) -> None:
    theme = THEME_MAP.get(category, THEME_MAP["default"])
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter

    c.setFillColor(colors.HexColor(theme["bg"]))
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.rect(0, h - 0.7 * inch, w, 0.7 * inch, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.55 * inch, h - 0.42 * inch, "High-intent growth bundle")

    c.setFillColor(colors.HexColor(theme["panel"]))
    c.roundRect(0.52 * inch, h - 2.45 * inch, w - 1.04 * inch, 1.0 * inch, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica-Bold", 24)
    lines = []
    current = ""
    for word in title.split():
        candidate = f"{current} {word}".strip()
        if len(candidate) <= 18:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    y = h - 1.82 * inch
    for line in lines[:2]:
        c.drawString(0.8 * inch, y, line)
        y -= 0.28 * inch

    c.setFillColor(colors.HexColor(theme["accent"]))
    c.roundRect(w - 2.2 * inch, h - 2.28 * inch, 1.25 * inch, 0.72 * inch, 0.14 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 15)
    c.drawString(w - 2.0 * inch, h - 1.95 * inch, f"${price:.2f}")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(0.7 * inch, 3.0 * inch, 2.4 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.95 * inch, 4.8 * inch, "Problem fit")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    items = ["Daily friction", "Money or time loss", "Clear fix", "Repeat demand"]
    y = 4.45 * inch
    for i, item in enumerate(items):
        c.drawString(0.95 * inch, y - i * 0.23 * inch, "- " + item)

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(3.5 * inch, 3.0 * inch, 2.5 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3.75 * inch, 4.8 * inch, "Why it converts")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(3.75 * inch, 4.45 * inch, "Creates quick clarity")
    c.drawString(3.75 * inch, 4.20 * inch, "Feels premium and specific")
    c.drawString(3.75 * inch, 3.95 * inch, "Reduces decision fatigue")
    c.drawString(3.75 * inch, 3.70 * inch, "Pains are urgent and recurring")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(6.35 * inch, 3.0 * inch, 2.1 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(6.58 * inch, 4.8 * inch, "Offer")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(6.58 * inch, 4.45 * inch, "One-page utility")
    c.drawString(6.58 * inch, 4.20 * inch, "Actionable")
    c.drawString(6.58 * inch, 3.95 * inch, "Smartly niche")
    c.drawString(6.58 * inch, 3.70 * inch, "Fast value")

    c.setFillColor(colors.HexColor(theme["header"]))
    c.roundRect(0.7 * inch, 0.9 * inch, w - 1.4 * inch, 1.1 * inch, 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(0.95 * inch, 1.62 * inch, "Category: " + category)
    c.setFont("Helvetica", 10)
    c.drawString(0.95 * inch, 1.27 * inch, "This bundle is optimized for targeted, high-trust, one-page buyer intent.")

    c.save()


csv_path = OUTDIR / "market_reach_more_6.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "category", "price_usd", "filename"])
    for title, category, price in CATALOG:
        filename = f"{slugify(title)}.pdf"
        path = OUTDIR / filename
        build_pdf(path, title, category, price)
        writer.writerow([title, category, price, filename])

README = OUTDIR / "README.md"
README.write_text(
    "# Market Reach More 6 Bundle\n\n"
    "This batch leans hard into owner operations, finance stress, life-admin gaps, legal clarity, family support, and digital business utility.\n\n"
    f"Total products: {len(CATALOG)}\n\n"
    "Target categories:\n"
    "- Small business\n"
    "- Home services\n"
    "- Legal\n"
    "- Finance\n"
    "- Healthcare\n"
    "- Marketing\n"
    "- Community\n"
    "- Technology\n"
    "- Lifestyle\n"
    "- Digital business\n"
    "- Freelance\n"
)

print(f"Created {len(CATALOG)} PDFs in {OUTDIR}")
