from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "market-reach-more-5"
OUTDIR.mkdir(exist_ok=True)

CATALOG = [
    ("Pet Health Check Reminder", "Pet care", 15.99),
    ("Dog Walking Route Planner", "Pet care", 16.99),
    ("Cat Care Routine Sheet", "Pet care", 15.99),
    ("Pet Insurance Cost Tracker", "Pet care", 16.99),
    ("Vet Appointment Organizer", "Pet care", 15.99),
    ("Pet Grooming Schedule", "Pet care", 15.99),
    ("Pet Feeding Tracker", "Pet care", 14.99),
    ("Dog Training Habit Sheet", "Pet care", 15.99),
    ("Pet Emergency Plan", "Pet care", 17.99),
    ("Pet Sitter Checklist", "Pet care", 15.99),
    ("Senior Move Planning Sheet", "Senior care", 18.99),
    ("Home Safety Audit", "Senior care", 17.99),
    ("Aging-in-Place Routine", "Senior care", 18.99),
    ("Medication Review Timeline", "Senior care", 17.99),
    ("Caregiver Hand-Off Sheet", "Senior care", 16.99),
    ("Family Care Timeline", "Senior care", 17.99),
    ("Mobility Support Checklist", "Senior care", 16.99),
    ("Senior Wellness Scorecard", "Senior care", 17.99),
    ("Caregiver Burnout Reset", "Senior care", 18.99),
    ("End-of-Life Planning Organizer", "Senior care", 19.99),
    ("Small Apartment Storage Plan", "Home organization", 15.99),
    ("Closet Reset Worksheet", "Home organization", 14.99),
    ("Pantry Inventory Sheet", "Home organization", 15.99),
    ("Laundry Room Flow Planner", "Home organization", 15.99),
    ("Entryway Drop Zone Guide", "Home organization", 14.99),
    ("Garage Sorting Checklist", "Home organization", 15.99),
    ("Seasonal Decor Storage", "Home organization", 14.99),
    ("Toy Rotation Organizer", "Home organization", 15.99),
    ("Under-Bed Storage Plan", "Home organization", 14.99),
    ("Home Reset Daily Sheet", "Home organization", 15.99),
    ("Wedding Venue Checklist", "Events", 18.99),
    ("Guest Seating Planner", "Events", 16.99),
    ("Catering Budget Sheet", "Events", 17.99),
    ("Wedding Vendor Tracker", "Events", 17.99),
    ("Event Backup Plan", "Events", 18.99),
    ("Birthday Party Budget", "Events", 15.99),
    ("Baby Shower Setup Sheet", "Events", 16.99),
    ("Holiday Party Planner", "Events", 17.99),
    ("Corporate Event Checklist", "Events", 18.99),
    ("Bridal Timeline Planner", "Events", 18.99),
    ("Neighborhood Food Drive Sheet", "Community", 15.99),
    ("Volunteer Intake Tracker", "Community", 16.99),
    ("Community Yard Sale Planner", "Community", 15.99),
    ("Block Watch Checklist", "Community", 16.99),
    ("Local Fundraiser Calendar", "Community", 17.99),
    ("School Supply Drive Sheet", "Community", 16.99),
    ("Senior Meal Delivery Log", "Community", 17.99),
    ("Community Clean-Up Schedule", "Community", 15.99),
    ("Neighborhood Event Signup", "Community", 16.99),
    ("Local Donation Organizer", "Community", 15.99),
    ("Chronic Pain Recovery Plan", "Wellness", 18.99),
    ("Inflammation Food Tracker", "Wellness", 16.99),
    ("Movement Pain Log", "Wellness", 15.99),
    ("Stress Recovery Ladder", "Wellness", 16.99),
    ("Daily Mood Reset Sheet", "Wellness", 15.99),
    ("Energy Management Planner", "Wellness", 16.99),
    ("Magnesium & Recovery Log", "Wellness", 15.99),
    ("Mindfulness Minute Guide", "Wellness", 14.99),
    ("Recovery Meal Planner", "Wellness", 16.99),
    ("Breathwork Practice Sheet", "Wellness", 14.99),
    ("Freelance Client Retention Sheet", "Freelance", 17.99),
    ("Client Proposal Checklist", "Freelance", 16.99),
    ("Scope Creep Control Sheet", "Freelance", 17.99),
    ("Portfolio Client Tracker", "Freelance", 16.99),
    ("Invoice Follow-Up Schedule", "Freelance", 16.99),
    ("Retainer Renewal Planner", "Freelance", 17.99),
    ("Discovery Call Checklist", "Freelance", 15.99),
    ("Service Package Comparison", "Freelance", 16.99),
    ("Independent Consultant Planner", "Freelance", 17.99),
    ("Client Feedback Snapshot", "Freelance", 15.99),
    ("Cold Email Response Tracker", "Marketing", 16.99),
    ("Instagram DM Follow-Up", "Marketing", 15.99),
    ("Lead Magnet Review Sheet", "Marketing", 16.99),
    ("Content Topic Matrix", "Marketing", 15.99),
    ("Customer Journey Map", "Marketing", 17.99),
    ("Offer Testing Tracker", "Marketing", 16.99),
    ("Campaign Feedback Sheet", "Marketing", 16.99),
    ("Search Intent Planner", "Marketing", 15.99),
    ("Landing Page CTA Review", "Marketing", 16.99),
    ("Sales Call Debrief Sheet", "Marketing", 17.99),
    ("Mobile Notary Checklist", "Legal", 17.99),
    ("Power of Attorney Organizer", "Legal", 18.99),
    ("Document Signing Tracker", "Legal", 16.99),
    ("Client Consent Checklist", "Legal", 16.99),
    ("Notary Journal Log", "Legal", 15.99),
    ("Witness Signature Sheet", "Legal", 15.99),
    ("Fee Schedule Tracker", "Legal", 16.99),
    ("Client Follow-Up Reminder", "Legal", 15.99),
    ("Document Return Log", "Legal", 16.99),
    ("Notary Appointment Planner", "Legal", 17.99),
    ("Cleaning Business Lead Sheet", "Local services", 18.99),
    ("Pressure Washing Client Log", "Local services", 17.99),
    ("Animal Grooming Booking Sheet", "Local services", 16.99),
    ("Home Repair Intake", "Local services", 17.99),
    ("Pet Sitting Turn Sheet", "Local services", 16.99),
    ("Landscaping Service Planner", "Local services", 17.99),
    ("Pool Cleaning Schedule", "Local services", 16.99),
    ("Repair Technician Sheet", "Local services", 17.99),
    ("Service Route Optimizer", "Local services", 18.99),
    ("Client Follow-Up Tracker", "Local services", 16.99),
    ("Digital Declutter Tracker", "Digital life", 15.99),
    ("Inbox Zero System", "Digital life", 15.99),
    ("Password Reset Checklist", "Digital life", 16.99),
    ("Phone Storage Cleanup", "Digital life", 14.99),
    ("Cloud Folder Organizer", "Digital life", 15.99),
    ("Device Maintenance Log", "Digital life", 15.99),
    ("Screen Time Boundaries", "Digital life", 15.99),
    ("App Subscription Audit", "Digital life", 14.99),
    ("Digital Files Recovery", "Digital life", 15.99),
    ("Data Backup Checklist", "Digital life", 16.99),
    ("Restaurant Cost Check", "Hospitality", 18.99),
    ("Inventory Waste Review", "Hospitality", 17.99),
    ("Kitchen Cleaning Schedule", "Hospitality", 16.99),
    ("Staff Training Log", "Hospitality", 17.99),
    ("Shift Coverage Planner", "Hospitality", 16.99),
    ("Vendor Performance Sheet", "Hospitality", 17.99),
    ("Menu Item Review", "Hospitality", 16.99),
    ("Food Safety Log", "Hospitality", 17.99),
    ("Prep List Audit", "Hospitality", 16.99),
    ("Customer Complaint Recovery", "Hospitality", 18.99)
]

THEME_MAP = {
    "Pet care": {"bg": "#FFF8F5", "header": "#7E413C", "accent": "#F1B8A5", "text": "#2D1E1D", "panel": "#FDEFEA"},
    "Senior care": {"bg": "#F8F6F2", "header": "#584A3B", "accent": "#D7B788", "text": "#2A221C", "panel": "#F0E9E0"},
    "Home organization": {"bg": "#F5FAF4", "header": "#35563A", "accent": "#A8C998", "text": "#1E2D1F", "panel": "#EAF5EA"},
    "Events": {"bg": "#FFF9F2", "header": "#734C31", "accent": "#E4B880", "text": "#2D211B", "panel": "#FDEFE2"},
    "Community": {"bg": "#F8F7F1", "header": "#4C5037", "accent": "#C4C786", "text": "#242C1A", "panel": "#F1F0E4"},
    "Wellness": {"bg": "#F9F4FF", "header": "#4F386A", "accent": "#BD9AE5", "text": "#2B213C", "panel": "#F1E8FF"},
    "Freelance": {"bg": "#F7F7FF", "header": "#3A4071", "accent": "#A5ABEB", "text": "#232744", "panel": "#EDEEFF"},
    "Marketing": {"bg": "#F7F8FF", "header": "#2E467D", "accent": "#9BB9F0", "text": "#1B2640", "panel": "#EBF0FF"},
    "Legal": {"bg": "#F3F5F2", "header": "#20352B", "accent": "#C0B08B", "text": "#1A241E", "panel": "#EEF0EA"},
    "Local services": {"bg": "#F9F7F2", "header": "#4B3E2D", "accent": "#D5A76B", "text": "#292115", "panel": "#F4ECDD"},
    "Digital life": {"bg": "#F4F8FA", "header": "#2D5365", "accent": "#7FBCC9", "text": "#1D2E35", "panel": "#E9F4F8"},
    "Hospitality": {"bg": "#FFF8F5", "header": "#7B1F1F", "accent": "#E7AF76", "text": "#2D1919", "panel": "#FDEAE3"},
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
    c.drawString(0.55 * inch, h - 0.42 * inch, "Crowded buyer niche bundle")

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
    c.drawString(0.95 * inch, 4.8 * inch, "High buyer fit")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(0.95 * inch, 4.45 * inch, "- Addresses a recurring pain")
    c.drawString(0.95 * inch, 4.20 * inch, "- Easy to use immediately")
    c.drawString(0.95 * inch, 3.95 * inch, "- Feels tailored and useful")
    c.drawString(0.95 * inch, 3.70 * inch, "- Fine for quick digital sales")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(3.5 * inch, 3.0 * inch, 2.5 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3.75 * inch, 4.8 * inch, "Why this sells")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(3.75 * inch, 4.45 * inch, "Creates order and control")
    c.drawString(3.75 * inch, 4.20 * inch, "Supports faster decisions")
    c.drawString(3.75 * inch, 3.95 * inch, "Feels premium in a niche")
    c.drawString(3.75 * inch, 3.70 * inch, "Transforms a task into a system")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor(theme["accent"]))
    c.roundRect(6.35 * inch, 3.0 * inch, 2.1 * inch, 2.1 * inch, 0.12 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor(theme["header"]))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(6.58 * inch, 4.8 * inch, "Angle")
    c.setFillColor(colors.HexColor(theme["text"]))
    c.setFont("Helvetica", 9.2)
    c.drawString(6.58 * inch, 4.45 * inch, "Quick fix")
    c.drawString(6.58 * inch, 4.20 * inch, "Better routine")
    c.drawString(6.58 * inch, 3.95 * inch, "Premium clarity")
    c.drawString(6.58 * inch, 3.70 * inch, "Higher utility")

    c.setFillColor(colors.HexColor(theme["header"]))
    c.roundRect(0.7 * inch, 0.9 * inch, w - 1.4 * inch, 1.1 * inch, 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(0.95 * inch, 1.62 * inch, "Category: " + category)
    c.setFont("Helvetica", 10)
    c.drawString(0.95 * inch, 1.27 * inch, "Built for strong niche demand, broader reach, and fast customer trust.")

    c.save()


csv_path = OUTDIR / "market_reach_more_5.csv"
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
    "# Market Reach More 5 Bundle\n\n"
    "This batch targets ultra-relevant, everyday pain points with strong personal-use and small-business utility: pet care, senior care, home organization, local services, wellness, and digital life systems.\n\n"
    f"Total products: {len(CATALOG)}\n\n"
    "Primary niches:\n"
    "- Pet care\n"
    "- Senior care\n"
    "- Home organization\n"
    "- Events\n"
    "- Community\n"
    "- Wellness\n"
    "- Freelance\n"
    "- Marketing\n"
    "- Legal\n"
    "- Local services\n"
    "- Digital life\n"
    "- Hospitality\n"
)

print(f"Created {len(CATALOG)} PDFs in {OUTDIR}")
