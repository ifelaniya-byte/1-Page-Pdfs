from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "market-reach-more-4"
OUTDIR.mkdir(exist_ok=True)

CATALOG = [
    ("AI Email Overload Reset", "AI productivity", 19.99),
    ("Prompt Library Starter", "AI productivity", 17.99),
    ("AI Content Workflow Sheet", "AI productivity", 18.99),
    ("Client Reply Efficiency Planner", "AI productivity", 16.99),
    ("Automation Review Checklist", "AI productivity", 18.99),
    ("Daily Content Sprint Plan", "AI productivity", 17.99),
    ("Marketing Prompt Vault", "AI productivity", 18.99),
    ("Prompt Fatigue Recovery", "AI productivity", 17.99),
    ("AI Tool Cost Tracker", "AI productivity", 16.99),
    ("ChatGPT Workflow Guide", "AI productivity", 18.99),
    ("Business Owner Weekly Reset", "Business ops", 19.99),
    ("Service Business Sales Tracker", "Business ops", 18.99),
    ("Daily Owner Dashboard", "Business ops", 19.99),
    ("Operations Bottleneck Map", "Business ops", 18.99),
    ("Client Delivery Checklist", "Business ops", 17.99),
    ("Workflow Cleanup Worksheet", "Business ops", 18.99),
    ("Pipeline Review Sheet", "Business ops", 17.99),
    ("Task Priority Compass", "Business ops", 16.99),
    ("Team Communication Tracker", "Business ops", 18.99),
    ("Executive Focus Planner", "Business ops", 19.99),
    ("Mortgage Payment Stress Sheet", "Finance", 18.99),
    ("Rent-to-Income Check", "Finance", 17.99),
    ("Savings Goal Tracker", "Finance", 16.99),
    ("Emergency Budget Planner", "Finance", 18.99),
    ("High-Interest Debt Tracker", "Finance", 17.99),
    ("Cash Flow Weekly Reset", "Finance", 18.99),
    ("Subscription Cleanup Sheet", "Finance", 15.99),
    ("Annual Expense Forecast", "Finance", 19.99),
    ("Net Worth Snapshot", "Finance", 18.99),
    ("Budget Zero Reset", "Finance", 17.99),
    ("Medical Visit Prep Sheet", "Healthcare", 16.99),
    ("Dental Appointments Organizer", "Healthcare", 16.99),
    ("Insurance Renewal Tracker", "Healthcare", 17.99),
    ("Healthcare Cost Comparison", "Healthcare", 18.99),
    ("Chronic Condition Planner", "Healthcare", 19.99),
    ("Family Care Weekly Map", "Healthcare", 18.99),
    ("Prescription Schedule Sheet", "Healthcare", 16.99),
    ("Urgent Care Decision Guide", "Healthcare", 17.99),
    ("Home Recovery Checklist", "Healthcare", 18.99),
    ("Medical Record Refresh Sheet", "Healthcare", 17.99),
    ("Legal Intake Summary", "Legal", 20.99),
    ("Contract Renewal Tracker", "Legal", 18.99),
    ("Employment Agreement Review", "Legal", 19.99),
    ("Service Agreement Checklist", "Legal", 18.99),
    ("Client Retainer Tracker", "Legal", 19.99),
    ("Demand Letter Prep Sheet", "Legal", 20.99),
    ("Small Business Legal Audit", "Legal", 21.99),
    ("Business Ownership Risk Sheet", "Legal", 18.99),
    ("Settlement Timeline Planner", "Legal", 19.99),
    ("Legal Deadline Log", "Legal", 17.99),
    ("HVAC Tune-Up Checklist", "Home services", 16.99),
    ("Gutter Cleaning Schedule", "Home services", 17.99),
    ("Water Leak Prevention Plan", "Home services", 17.99),
    ("Garage Door Service Log", "Home services", 16.99),
    ("Pool Water Test Sheet", "Home services", 15.99),
    ("Seasonal Pest Control Plan", "Home services", 17.99),
    ("Lawn Maintenance Planner", "Home services", 16.99),
    ("Pressure Washing Estimate", "Home services", 18.99),
    ("Cleaning Crew Daily Sheet", "Home services", 17.99),
    ("Service Call Escalation Guide", "Home services", 18.99),
    ("Property Turnover Check", "Real estate", 17.99),
    ("Tenant Renewal Offer", "Real estate", 17.99),
    ("Move-In Condition Sheet", "Real estate", 18.99),
    ("Short-Term Rental Planner", "Real estate", 19.99),
    ("Vacancy Recovery Checklist", "Real estate", 17.99),
    ("Rental Compliance Log", "Real estate", 18.99),
    ("Home Inspection Follow-Up", "Real estate", 16.99),
    ("Showing Feedback Tracker", "Real estate", 17.99),
    ("Neighbor Communication Log", "Real estate", 16.99),
    ("Lease Renewal Timeline", "Real estate", 18.99),
    ("Salon Client Retention Sheet", "Lifestyle", 16.99),
    ("Barber Appointment Planner", "Lifestyle", 15.99),
    ("Spa Inventory Snapshot", "Lifestyle", 16.99),
    ("Beauty Service Upsell Planner", "Lifestyle", 17.99),
    ("Massage Client Follow-Up", "Lifestyle", 17.99),
    ("Personal Care Streak Sheet", "Lifestyle", 15.99),
    ("Home Cleaning Rotation", "Lifestyle", 15.99),
    ("Laundry Reset Tracker", "Lifestyle", 14.99),
    ("Wardrobe Capsule Planner", "Lifestyle", 16.99),
    ("Errand Day Organizer", "Lifestyle", 15.99),
    ("Student Budget Recovery", "Education", 16.99),
    ("Scholarship Deadline Sheet", "Education", 17.99),
    ("College Expense Tracker", "Education", 17.99),
    ("Exam Week Survival Plan", "Education", 15.99),
    ("Class Attendance Reset", "Education", 15.99),
    ("Homework Catch-Up Sheet", "Education", 16.99),
    ("Academic Goal Planner", "Education", 16.99),
    ("Study Block Template", "Education", 15.99),
    ("Career School Decision Sheet", "Education", 17.99),
    ("Student Loan Payment Plan", "Education", 18.99),
    ("Instagram Content Engine", "Marketing", 18.99),
    ("Lead Follow-Up Sequence", "Marketing", 17.99),
    ("Offer Review Worksheet", "Marketing", 18.99),
    ("Review Request Script", "Marketing", 16.99),
    ("Landing Page Copy Audit", "Marketing", 17.99),
    ("Local SEO Checklist", "Marketing", 16.99),
    ("Referral Partner Tracker", "Marketing", 17.99),
    ("Advertising Budget Check", "Marketing", 18.99),
    ("Conversion Tracker Sheet", "Marketing", 17.99),
    ("Email Sequence Planner", "Marketing", 18.99),
    ("Senior Tech Setup Plan", "Community", 17.99),
    ("Volunteer Shift Tracker", "Community", 15.99),
    ("Neighborhood Resource Sheet", "Community", 16.99),
    ("Family Event Planner", "Community", 17.99),
    ("Community Cleanup Guide", "Community", 15.99),
    ("Group Meal Organizer", "Community", 16.99),
    ("Neighborhood Safety List", "Community", 15.99),
    ("Local Service Comparison", "Community", 16.99),
    ("Volunteer Coordinator Sheet", "Community", 17.99),
    ("Senior Help Request Sheet", "Community", 16.99)
]

THEME_MAP = {
    "AI productivity": {"bg": "#F4F8FF", "header": "#1E3F78", "accent": "#8AB3F5", "text": "#1F2E45", "panel": "#EAF2FF"},
    "Business ops": {"bg": "#F5F9F6", "header": "#2C5048", "accent": "#87C1AA", "text": "#1D2E2A", "panel": "#EAF7F3"},
    "Finance": {"bg": "#F6F9F3", "header": "#285748", "accent": "#A3C89D", "text": "#1E2D29", "panel": "#EAF4EB"},
    "Healthcare": {"bg": "#F3FAFB", "header": "#1D5364", "accent": "#7DB8C8", "text": "#1C2E35", "panel": "#EAF7FA"},
    "Legal": {"bg": "#F4F5F2", "header": "#1F352B", "accent": "#C2B390", "text": "#1A231C", "panel": "#EEF1EC"},
    "Home services": {"bg": "#F8F8F3", "header": "#42533B", "accent": "#C3C782", "text": "#212B1D", "panel": "#F0F2E7"},
    "Real estate": {"bg": "#F9F7F2", "header": "#4A3827", "accent": "#D6A56B", "text": "#2A2116", "panel": "#F4EADA"},
    "Lifestyle": {"bg": "#FFF9F8", "header": "#6D4057", "accent": "#E7A6B3", "text": "#2C1E21", "panel": "#FDEFF1"},
    "Education": {"bg": "#F5FAFB", "header": "#2A5865", "accent": "#7EBED1", "text": "#1E2F35", "panel": "#EAF7FB"},
    "Marketing": {"bg": "#F7F8FF", "header": "#2B3F79", "accent": "#9ABAF5", "text": "#1B2340", "panel": "#EBF0FF"},
    "Community": {"bg": "#F8F7F2", "header": "#4E5138", "accent": "#C4C486", "text": "#242C1C", "panel": "#F2F1E5"},
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
    c.drawString(0.55 * inch, h - 0.42 * inch, "Commercial-grade niche bundle")

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
    c.roundRect(w - 2.2 * inch, h - 2.28 * inch, 1.24 * inch, 0.72 * inch, 0.14 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 15)
    c.drawString(w - 2.0 * inch, h - 1.95 * inch, f"${price:.2f}")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(0.72 * inch, 3.0 * inch, 2.45 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.96 * inch, 4.8 * inch, "High-demand need")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    for i, text in enumerate(["Clear problem", "Affects money or time", "Urgent action", "Repeatable use"], start=1):
        c.drawString(0.96 * inch, 4.45 * inch - (i - 1) * 0.24 * inch, "- " + text)

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(3.52 * inch, 3.0 * inch, 2.52 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3.78 * inch, 4.8 * inch, "Value proposition")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(3.78 * inch, 4.45 * inch, "Cuts friction immediately")
    c.drawString(3.78 * inch, 4.20 * inch, "Creates a clearer process")
    c.drawString(3.78 * inch, 3.95 * inch, "Looks more premium than a basic checklist")
    c.drawString(3.78 * inch, 3.70 * inch, "Works for fast digital sales")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(6.38 * inch, 3.0 * inch, 2.12 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(6.62 * inch, 4.8 * inch, "Offer angle")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(6.62 * inch, 4.45 * inch, "1-page utility")
    c.drawString(6.62 * inch, 4.20 * inch, "Quick win")
    c.drawString(6.62 * inch, 3.95 * inch, "Premium clarity")
    c.drawString(6.62 * inch, 3.70 * inch, "Instant use")

    c.setFillColor(colors.HexColor(theme["header"]))
    c.roundRect(0.7 * inch, 0.9 * inch, w - 1.4 * inch, 1.1 * inch, 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(0.95 * inch, 1.62 * inch, "Category: " + category)
    c.setFont("Helvetica", 10)
    c.drawString(0.95 * inch, 1.27 * inch, "This bundle is optimized for high buyer intent, urgency, and immediate one-page value.")

    c.save()


csv_path = OUTDIR / "market_reach_more_4.csv"
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
    "# Market Reach More 4 Bundle\n\n"
    "This batch aggressively expands the catalog into fast-moving buyers: AI workflow, business ops, finance stress, local home services, healthcare management, legal clarity, and education support.\n\n"
    f"Total products: {len(CATALOG)}\n\n"
    "Core categories:\n"
    "- AI productivity\n"
    "- Business ops\n"
    "- Finance\n"
    "- Healthcare\n"
    "- Legal\n"
    "- Home services\n"
    "- Real estate\n"
    "- Lifestyle\n"
    "- Education\n"
    "- Marketing\n"
    "- Community\n"
)

print(f"Created {len(CATALOG)} PDFs in {OUTDIR}")
