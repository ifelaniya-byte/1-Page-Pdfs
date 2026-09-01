from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "market-reach-more-3"
OUTDIR.mkdir(exist_ok=True)

CATALOG = [
    ("Emergency Room Wait Time Planner", "Healthcare", 19.99),
    ("Insurance Claim Prep Sheet", "Healthcare", 18.99),
    ("Medical Bill Negotiation Guide", "Healthcare", 19.99),
    ("Primary Care Visit Checklist", "Healthcare", 17.99),
    ("Specialist Referral Organizer", "Healthcare", 16.99),
    ("Telehealth Visit Summary", "Healthcare", 17.99),
    ("Pharmacy Management Sheet", "Healthcare", 16.99),
    ("Caregiver Weekly Coverage Plan", "Healthcare", 19.99),
    ("Dementia Care Checklist", "Healthcare", 19.99),
    ("Home Health Care Log", "Healthcare", 17.99),
    ("Medicare Enrollment Guide", "Healthcare", 18.99),
    ("FSA Spending Tracker", "Healthcare", 16.99),
    ("HSA Savings Planner", "Healthcare", 17.99),
    ("Mental Health Check-In Sheet", "Healthcare", 17.99),
    ("Therapy Session Tracker", "Healthcare", 16.99),

    ("Tax Refund Readiness Sheet", "Finance", 17.99),
    ("401k Contribution Planner", "Finance", 18.99),
    ("Debt Consolidation Guide", "Finance", 19.99),
    ("Credit Card Payoff Tracker", "Finance", 17.99),
    ("Mortgage Rate Comparison", "Finance", 18.99),
    ("Car Loan Budget Sheet", "Finance", 16.99),
    ("Bank Account Reconciliation", "Finance", 17.99),
    ("Emergency Cash Buffer Plan", "Finance", 18.99),
    ("Insurance Premium Analyzer", "Finance", 19.99),
    ("Tax Loss Harvesting Primer", "Finance", 19.99),

    ("Solo Attorney Client Intake", "Legal", 21.99),
    ("Consulting Proposal Outline", "Legal", 19.99),
    ("Contract Review Quick Checklist", "Legal", 20.99),
    ("Client Contract Reminder", "Legal", 18.99),
    ("LLC Formation Organizer", "Legal", 19.99),
    ("Mediation Prep Sheet", "Legal", 18.99),
    ("Divorce Financial Checklist", "Legal", 20.99),
    ("Small Business Legal Audit", "Legal", 21.99),
    ("Employment Offer Review", "Legal", 18.99),
    ("Noncompete Review Guide", "Legal", 19.99),

    ("Lead Nurture Tracker", "Marketing", 17.99),
    ("Customer Win-Back Script", "Marketing", 18.99),
    ("Sales Funnel Diagnostic", "Marketing", 19.99),
    ("Landing Page Conversion Check", "Marketing", 17.99),
    ("Brand Messaging Grid", "Marketing", 18.99),
    ("Retargeting Offer Planner", "Marketing", 18.99),
    ("Referral Program Tracker", "Marketing", 17.99),
    ("SEO Content Brief", "Marketing", 18.99),
    ("Local Google Review Request", "Marketing", 16.99),
    ("Ad Spend Review Sheet", "Marketing", 19.99),

    ("Residential Cleaning Job Sheet", "Home services", 16.99),
    ("House Call Service Planner", "Home services", 17.99),
    ("HVAC Service Ticket", "Home services", 18.99),
    ("Plumbing Estimate Template", "Home services", 18.99),
    ("Electric Service Intake", "Home services", 17.99),
    ("Lawn Care Client Tracker", "Home services", 16.99),
    ("Pool Service Maintainer", "Home services", 17.99),
    ("Window Cleaning Checklist", "Home services", 16.99),
    ("Pest Control Service Log", "Home services", 17.99),
    ("Home Watch Daily Log", "Home services", 18.99),

    ("Real Estate Showing Checklist", "Real estate", 17.99),
    ("Rental Screening Checklist", "Real estate", 18.99),
    ("Tenant Renewal Offer Sheet", "Real estate", 17.99),
    ("Property Turnover Planner", "Real estate", 18.99),
    ("Airbnb Host Operations Sheet", "Real estate", 19.99),
    ("HOA Communication Tracker", "Real estate", 17.99),
    ("Vacation Rental Cleaning Log", "Real estate", 16.99),
    ("Vacancy Recovery Sheet", "Real estate", 17.99),
    ("Walkthrough Punch Sheet", "Real estate", 16.99),
    ("Landlord Invoice Tracker", "Real estate", 18.99),

    ("Business Owner Hiring Checklist", "Operations", 19.99),
    ("Team SOP Snapshot", "Operations", 18.99),
    ("Client Onboarding Tracker", "Operations", 17.99),
    ("Customer Escalation Flow", "Operations", 18.99),
    ("Vendor Performance Scorecard", "Operations", 19.99),
    ("Inventory Reorder Planner", "Operations", 17.99),
    ("Warehouse Safety Checklist", "Operations", 18.99),
    ("Shipping Delay Recovery", "Operations", 17.99),
    ("Equipment Maintenance Log", "Operations", 18.99),
    ("Daily Ops Review Sheet", "Operations", 19.99),

    ("Long-Term Care Checklist", "Senior care", 19.99),
    ("Senior Medication Tracker", "Senior care", 17.99),
    ("Elder Tech Setup Guide", "Senior care", 18.99),
    ("Caregiver Support Planner", "Senior care", 18.99),
    ("Memory Care Routine Sheet", "Senior care", 17.99),
    ("Respite Care Calendar", "Senior care", 16.99),
    ("Senior Transportation Planner", "Senior care", 17.99),
    ("Fall Prevention Checklist", "Senior care", 18.99),
    ("Doctor Appointment Organizer", "Senior care", 16.99),
    ("Family Care Meeting Agenda", "Senior care", 17.99),

    ("Routine Health Audit", "Wellness", 17.99),
    ("Daily Hydration Tracker", "Wellness", 15.99),
    ("Stress Relief Ladder", "Wellness", 16.99),
    ("Sleep Hygiene Routine", "Wellness", 15.99),
    ("Vitamin & Supplement Log", "Wellness", 16.99),
    ("Recovery Week Planner", "Wellness", 17.99),
    ("Focus Habit Starter", "Wellness", 16.99),
    ("Workday Reset Sheet", "Wellness", 15.99),
    ("Movement Recovery Tracker", "Wellness", 16.99),
    ("Healthy Meal Planning Sheet", "Wellness", 17.99)
]

THEME_MAP = {
    "Healthcare": {"bg": "#F2F9FA", "header": "#1E5067", "accent": "#7AC2CC", "text": "#1D2F37", "panel": "#EAF7F9"},
    "Finance": {"bg": "#F8FAF5", "header": "#285140", "accent": "#9DC598", "text": "#1F2B26", "panel": "#EBF5ED"},
    "Legal": {"bg": "#F3F5F2", "header": "#1F382B", "accent": "#BEB287", "text": "#1A241D", "panel": "#EDF0EA"},
    "Marketing": {"bg": "#F7F8FF", "header": "#2B4479", "accent": "#98B5F5", "text": "#1B2540", "panel": "#EAF0FF"},
    "Home services": {"bg": "#F7F8F3", "header": "#44543A", "accent": "#BFCB90", "text": "#1F271C", "panel": "#EFF3E8"},
    "Real estate": {"bg": "#F9F6F2", "header": "#4A3928", "accent": "#D9A96F", "text": "#292116", "panel": "#F3E9DE"},
    "Operations": {"bg": "#F5F9F8", "header": "#294C45", "accent": "#84B8AE", "text": "#1C2B29", "panel": "#E8F3F1"},
    "Senior care": {"bg": "#F8F7F4", "header": "#564A39", "accent": "#D7B788", "text": "#2B221B", "panel": "#F0EAE3"},
    "Wellness": {"bg": "#F9F5FF", "header": "#483B69", "accent": "#B7A0E8", "text": "#2B223C", "panel": "#F1E8FF"},
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
    c.drawString(0.55 * inch, h - 0.42 * inch, "High-conversion niche bundle")

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
    c.drawString(0.95 * inch, 4.8 * inch, "Buyer problem")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    bullet_lines = [
        "Clear pain point",
        "High urgency",
        "Immediate action",
        "Lower friction",
    ]
    y = 4.45 * inch
    for bullet in bullet_lines:
        c.drawString(0.95 * inch, y, "- " + bullet)
        y -= 0.22 * inch

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(3.5 * inch, 3.0 * inch, 2.5 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3.75 * inch, 4.8 * inch, "Buyer value")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(3.75 * inch, 4.45 * inch, "Creates clarity quickly")
    c.drawString(3.75 * inch, 4.20 * inch, "Reduces mistakes and stress")
    c.drawString(3.75 * inch, 3.95 * inch, "Feels premium and practical")
    c.drawString(3.75 * inch, 3.70 * inch, "Easy to use in real life")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(6.35 * inch, 3.0 * inch, 2.1 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(6.58 * inch, 4.8 * inch, "Angle")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(6.58 * inch, 4.45 * inch, "One-page utility")
    c.drawString(6.58 * inch, 4.20 * inch, "Decision aid")
    c.drawString(6.58 * inch, 3.95 * inch, "Premium clarity")
    c.drawString(6.58 * inch, 3.70 * inch, "Fast action")

    c.setFillColor(colors.HexColor(theme["header"]))
    c.roundRect(0.7 * inch, 0.9 * inch, w - 1.4 * inch, 1.1 * inch, 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(0.95 * inch, 1.62 * inch, "Category: " + category)
    c.setFont("Helvetica", 10)
    c.drawString(0.95 * inch, 1.27 * inch, "Designed to reach buyers with urgent, practical, and highly useable single-page tools.")

    c.save()


csv_path = OUTDIR / "market_reach_more_3.csv"
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
    "# Market Reach More 3 Bundle\n\n"
    "This addition targets direct buyer pain in healthcare, legal, finance, operations, senior care, wellness, and home-service categories.\n\n"
    f"Total products: {len(CATALOG)}\n\n"
    "Target categories:\n"
    "- Healthcare\n"
    "- Finance\n"
    "- Legal\n"
    "- Marketing\n"
    "- Home services\n"
    "- Real estate\n"
    "- Operations\n"
    "- Senior care\n"
    "- Wellness\n"
)

print(f"Created {len(CATALOG)} PDFs in {OUTDIR}")
