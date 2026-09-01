from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "market-reach-more"
OUTDIR.mkdir(exist_ok=True)

CATALOG = [
    ("Dental Cost Recovery Planner", "Health & wellness", 19.99),
    ("Pet Care Cost Tracker", "Pet care", 16.99),
    ("Veterinary Visit Prep Sheet", "Pet care", 15.99),
    ("Personal Tax Prep Checklist", "Finance", 18.99),
    ("Quarterly Savings Check-In", "Finance", 17.99),
    ("Emergency Fund Builder", "Finance", 18.49),
    ("Freelancer Invoice Tracker", "Freelance", 19.99),
    ("Client Follow-Up System", "Freelance", 17.99),
    ("Portfolio Pricing Sheet", "Freelance", 18.99),
    ("Independent Contractor Tax Planner", "Freelance", 19.99),
    ("Landlord Rent Collection Tracker", "Real estate", 18.99),
    ("Tenant Move-In Checklist", "Real estate", 17.99),
    ("Property Maintenance Planner", "Real estate", 19.99),
    ("Home Inspection Punch List", "Real estate", 18.99),
    ("Short-Term Rental Setup Sheet", "Real estate", 20.99),
    ("Home Office Ergonomics Audit", "Remote work", 17.99),
    ("Zoom Fatigue Recovery Sheet", "Remote work", 16.99),
    ("Performance Review Prep", "Career", 18.99),
    ("Salary Negotiation Cheat Sheet", "Career", 18.49),
    ("Job Search Recovery Planner", "Career", 17.99),
    ("Resume Booster Checklist", "Career", 16.99),
    ("Portfolio Update Planner", "Career", 17.99),
    ("Business Owner Weekly Review", "Operations", 19.99),
    ("Vendor Risk Scorecard", "Operations", 18.99),
    ("Customer Service Recovery Script", "Operations", 18.49),
    ("Order Fulfillment Tracker", "Operations", 17.99),
    ("Warehouse Receiving Check", "Operations", 16.99),
    ("Delivery Route Optimizer", "Operations", 18.99),
    ("Lawn Care Scheduling Sheet", "Home services", 16.99),
    ("Pool Service Checklist", "Home services", 17.99),
    ("Cleaning Business Daily Planner", "Home services", 19.99),
    ("Pressure Washing Estimate Sheet", "Home services", 18.99),
    ("Garage Door Repair Intake", "Home services", 17.99),
    ("Event Planning Deadlines", "Events", 19.99),
    ("Wedding Budget Tracker", "Events", 17.99),
    ("Birthday Party Setup Checklist", "Events", 16.99),
    ("Corporate Event Ops Guide", "Events", 21.99),
    ("Micro Wedding Vendor Sheet", "Events", 18.99),
    ("Grocery Budget Reset", "Family finance", 16.99),
    ("School Lunch Planning Sheet", "Family finance", 15.99),
    ("Monthly Family Admin Dashboard", "Family finance", 18.99),
    ("Mom Life Recovery Planner", "Family finance", 17.99),
    ("Family Meal Cost Snapshot", "Family finance", 16.99),
    ("College Budget Survival Sheet", "Education", 17.99),
    ("Scholarship Application Tracker", "Education", 18.99),
    ("Student Financial Stress Log", "Education", 15.99),
    ("Academic Recovery Plan", "Education", 17.99),
    ("Study Habit Reset Planner", "Education", 16.99),
    ("Neighborhood Community Resource Map", "Community", 16.99),
    ("Local Service Comparison Sheet", "Community", 15.99),
    ("Senior Tech Help Planner", "Community", 18.99),
    ("Volunteer Shift Organizer", "Community", 16.49),
    ("Community Event Signup Sheet", "Community", 15.99),
    ("Restaurant Profit Health Check", "Food & hospitality", 20.99),
    ("Chef Prep Efficiency Tracker", "Food & hospitality", 19.99),
    ("Menu Item Profit Sheet", "Food & hospitality", 18.99),
    ("Baker Daily Production Planner", "Food & hospitality", 18.99),
    ("Catering Lead Sheet", "Food & hospitality", 19.99),
    ("Beauty Salon Booking Planner", "Personal services", 17.99),
    ("Barber Appointment Tracker", "Personal services", 16.99),
    ("Massage Client Intake Sheet", "Personal services", 18.99),
    ("Spa Inventory Check", "Personal services", 17.99),
    ("Salon Upsell Tracker", "Personal services", 17.99),
    ("Home Cleaning Checklist", "Household", 16.99),
    ("Laundry Routine Reset", "Household", 15.99),
    ("Declutter Sprint Sheet", "Household", 16.99),
    ("Garage Organization Planner", "Household", 17.99),
    ("Smart Home Setup Checklist", "Household", 18.99),
    ("Home Water Leak Prevention", "Home maintenance", 17.99),
    ("HVAC Seasonal Tune-Up Guide", "Home maintenance", 18.99),
    ("Bathroom Upgrade Planner", "Home maintenance", 16.99),
    ("Exterior Maintenance Calendar", "Home maintenance", 17.99),
    ("Storm Prep Survival Sheet", "Home maintenance", 18.99),
    ("Business Forecast Snapshot", "Marketing", 19.99),
    ("Local SEO Content Planner", "Marketing", 18.99),
    ("Customer Review Request Script", "Marketing", 17.99),
    ("Instagram Content Planner", "Marketing", 18.99),
    ("Lead Follow-Up Tracker", "Marketing", 17.49),
    ("Podcast Launch Checklist", "Creator business", 19.99),
    ("YouTube Content Calendar", "Creator business", 18.99),
    ("Brand Voice Starter Sheet", "Creator business", 16.99),
    ("Creator Burnout Recovery", "Creator business", 18.99),
    ("Affiliate Income Tracker", "Creator business", 19.99),
    ("Utility Cost Reduction Plan", "Energy", 18.99),
    ("Water Usage Saver Sheet", "Energy", 16.99),
    ("Solar Savings Explorer", "Energy", 19.99),
    ("Storm Energy Prep Guide", "Energy", 18.99),
    ("Electric Bill Budget Planner", "Energy", 16.99),
    ("Pet Sitting Schedule", "Service business", 16.99),
    ("Dog Walker Route Sheet", "Service business", 16.99),
    ("Cleaning Team Assignment Sheet", "Service business", 18.99),
    ("Lawn Service Customer Tracker", "Service business", 17.99),
    ("Home Watch Check Sheet", "Service business", 18.99),
    ("Credit Score Improvement Plan", "Finance", 18.99),
    ("Debt Snowball Tracker", "Finance", 17.99),
    ("Fintech App Budget Review", "Finance", 15.99),
    ("Savings Goal Builder", "Finance", 16.99),
    ("Cash Flow Emergency Plan", "Finance", 18.99),
]

THEME_MAP = {
    "Health & wellness": {"bg": "#F2FBF9", "header": "#1D4D57", "accent": "#75C6B8", "text": "#1D2F35", "panel": "#EAF8F7"},
    "Pet care": {"bg": "#FFF8F4", "header": "#7A3E4C", "accent": "#F2B9A9", "text": "#2C1B1D", "panel": "#FEEFE9"},
    "Finance": {"bg": "#F7F9F5", "header": "#234E3B", "accent": "#9CC39B", "text": "#1F2F29", "panel": "#EAF4ED"},
    "Freelance": {"bg": "#F7F7FF", "header": "#3A3D72", "accent": "#A7A9E8", "text": "#232543", "panel": "#EDEEFF"},
    "Real estate": {"bg": "#F9F7F3", "header": "#4B3C28", "accent": "#D1A266", "text": "#2A2118", "panel": "#F4EBD9"},
    "Remote work": {"bg": "#F3F8FF", "header": "#2E4C7A", "accent": "#7FA6E8", "text": "#1F2E44", "panel": "#EAF1FF"},
    "Career": {"bg": "#F9F7F2", "header": "#3E4C5B", "accent": "#D9B57C", "text": "#1F2B35", "panel": "#F2EDE5"},
    "Operations": {"bg": "#F4F9F6", "header": "#294B44", "accent": "#86B8A8", "text": "#1D2B28", "panel": "#E7F5F0"},
    "Home services": {"bg": "#F8F8F5", "header": "#48543B", "accent": "#C8C383", "text": "#1F2B1D", "panel": "#F0F3E7"},
    "Events": {"bg": "#FFF9F2", "header": "#694733", "accent": "#E5B67F", "text": "#2D1D14", "panel": "#FDEEE2"},
    "Family finance": {"bg": "#F9F7FF", "header": "#4A3C6B", "accent": "#B49AE4", "text": "#2A2143", "panel": "#F0E9FF"},
    "Education": {"bg": "#F5FAFB", "header": "#2B5D66", "accent": "#7FC9D6", "text": "#1D2F35", "panel": "#E9F7FB"},
    "Community": {"bg": "#F8F7F1", "header": "#4B5038", "accent": "#C4C58A", "text": "#242B1A", "panel": "#F1F0E7"},
    "Food & hospitality": {"bg": "#FFF8F4", "header": "#7A1F1F", "accent": "#E7B177", "text": "#2E1A1A", "panel": "#FDE9E2"},
    "Personal services": {"bg": "#FFF9F8", "header": "#6A3B55", "accent": "#E2A8B9", "text": "#2A1C1F", "panel": "#FDEDF0"},
    "Household": {"bg": "#F5FAF7", "header": "#264E3A", "accent": "#A1D0A4", "text": "#1C2E26", "panel": "#EAF6EE"},
    "Home maintenance": {"bg": "#F7F8F4", "header": "#3E4336", "accent": "#B5C08C", "text": "#22291E", "panel": "#EEF1E3"},
    "Marketing": {"bg": "#F6F9FF", "header": "#264A73", "accent": "#88ACE2", "text": "#1D2E43", "panel": "#EAF2FF"},
    "Creator business": {"bg": "#F9F4FF", "header": "#4A366B", "accent": "#B196D9", "text": "#28213A", "panel": "#F1E6FF"},
    "Energy": {"bg": "#F4FBFB", "header": "#1C5C5C", "accent": "#77BFAE", "text": "#1D2F2F", "panel": "#EAF8F7"},
    "Service business": {"bg": "#F9F7F2", "header": "#514128", "accent": "#D3AB6D", "text": "#241F1A", "panel": "#F4EDE4"},
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
    c.drawString(0.55 * inch, h - 0.42 * inch, "Demand expansion bundle")

    c.setFillColor(colors.HexColor(theme["panel"]))
    c.roundRect(0.52 * inch, h - 2.5 * inch, w - 1.04 * inch, 1.0 * inch, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica-Bold", 24)
    current = ""
    lines = []
    for word in title.split():
        cand = f"{current} {word}".strip()
        if len(cand) <= 18:
            current = cand
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    y = h - 1.88 * inch
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
    c.roundRect(0.65 * inch, 3.05 * inch, 2.45 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.9 * inch, 4.8 * inch, "Why it sells")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    items = [
        "Solves a real friction point.",
        "Acts quickly and feels practical.",
        "Easy to use without more learning.",
        "Fits a premium one-page offer.",
    ]
    y = 4.48 * inch
    for item in items:
        c.drawString(0.9 * inch, y, item)
        y -= 0.22 * inch

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(3.48 * inch, 3.05 * inch, 2.5 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3.75 * inch, 4.8 * inch, "Buyer urgency")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(3.75 * inch, 4.48 * inch, "- Immediate problem relief")
    c.drawString(3.75 * inch, 4.22 * inch, "- Clear action in under 10 min")
    c.drawString(3.75 * inch, 3.96 * inch, "- Less stress, more control")
    c.drawString(3.75 * inch, 3.70 * inch, "- Premium productivity feel")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(6.35 * inch, 3.05 * inch, 2.1 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(6.58 * inch, 4.8 * inch, "Angle")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(6.58 * inch, 4.48 * inch, "One-page fix")
    c.drawString(6.58 * inch, 4.22 * inch, "Actionable")
    c.drawString(6.58 * inch, 3.96 * inch, "Premium utility")
    c.drawString(6.58 * inch, 3.70 * inch, "Fast value")

    c.setFillColor(colors.HexColor(theme["header"]))
    c.roundRect(0.7 * inch, 0.92 * inch, w - 1.4 * inch, 1.1 * inch, 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(0.95 * inch, 1.63 * inch, "Category: " + category)
    c.setFont("Helvetica", 10)
    c.drawString(0.95 * inch, 1.28 * inch, "High-demand niche utility designed for broader reach and instant buyer trust.")

    c.save()


csv_path = OUTDIR / "market_reach_more.csv"
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
    "# Market Reach More Bundle\n\n"
    "This is a broader, more niche expansion set for one-page PDF products targeting active buyer pain points in financial stress, home services, education, local operations, creator businesses, and family systems.\n\n"
    f"Total products: {len(CATALOG)}\n\n"
    "Categories included:\n"
    "- Health & wellness\n"
    "- Pet care\n"
    "- Finance\n"
    "- Freelance\n"
    "- Real estate\n"
    "- Remote work\n"
    "- Career\n"
    "- Operations\n"
    "- Home services\n"
    "- Events\n"
    "- Family finance\n"
    "- Education\n"
    "- Community\n"
    "- Food & hospitality\n"
    "- Personal services\n"
    "- Household\n"
    "- Home maintenance\n"
    "- Marketing\n"
    "- Creator business\n"
    "- Energy\n"
    "- Service business\n"
)

print(f"Created {len(CATALOG)} PDFs in {OUTDIR}")
