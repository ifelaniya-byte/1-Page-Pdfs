from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent

THEMES = {
    "food_service": {
        "label": "Food Service",
        "bg": colors.HexColor("#FFF7F1"),
        "panel": colors.HexColor("#FFF3E8"),
        "header": colors.HexColor("#7A1F1F"),
        "accent": colors.HexColor("#D9A441"),
        "text": colors.HexColor("#2E1C1A"),
        "muted": colors.HexColor("#7B5A52"),
        "chip": colors.HexColor("#F6E6D9"),
    },
    "retail": {
        "label": "Retail Ops",
        "bg": colors.HexColor("#F5F9FF"),
        "panel": colors.HexColor("#EAF1FF"),
        "header": colors.HexColor("#1D3C78"),
        "accent": colors.HexColor("#B6C7E3"),
        "text": colors.HexColor("#1A2542"),
        "muted": colors.HexColor("#5E6D8A"),
        "chip": colors.HexColor("#E3ECFF"),
    },
    "construction": {
        "label": "Construction",
        "bg": colors.HexColor("#F7F6F2"),
        "panel": colors.HexColor("#F1EDE5"),
        "header": colors.HexColor("#2D2D2D"),
        "accent": colors.HexColor("#D47D2A"),
        "text": colors.HexColor("#1E1E1E"),
        "muted": colors.HexColor("#5B544D"),
        "chip": colors.HexColor("#F0E7DA"),
    },
    "legal": {
        "label": "Legal",
        "bg": colors.HexColor("#F5F7F5"),
        "panel": colors.HexColor("#EDF2EE"),
        "header": colors.HexColor("#1D352A"),
        "accent": colors.HexColor("#C3A25A"),
        "text": colors.HexColor("#192924"),
        "muted": colors.HexColor("#5A6B64"),
        "chip": colors.HexColor("#E7EEE7"),
    },
    "health": {
        "label": "Caregiver & Health",
        "bg": colors.HexColor("#F7F9FE"),
        "panel": colors.HexColor("#ECF4F8"),
        "header": colors.HexColor("#1C4D5B"),
        "accent": colors.HexColor("#60A6A6"),
        "text": colors.HexColor("#1E2F38"),
        "muted": colors.HexColor("#587286"),
        "chip": colors.HexColor("#E3F1F6"),
    },
    "local_business": {
        "label": "Local Business",
        "bg": colors.HexColor("#FBFAF7"),
        "panel": colors.HexColor("#F2F0E7"),
        "header": colors.HexColor("#1B2C45"),
        "accent": colors.HexColor("#D7B76E"),
        "text": colors.HexColor("#1B2432"),
        "muted": colors.HexColor("#646F7F"),
        "chip": colors.HexColor("#F4EEDB"),
    },
    "wellness": {
        "label": "Wellness",
        "bg": colors.HexColor("#F9F7FB"),
        "panel": colors.HexColor("#F2ECFB"),
        "header": colors.HexColor("#44325F"),
        "accent": colors.HexColor("#9C84D1"),
        "text": colors.HexColor("#2A203B"),
        "muted": colors.HexColor("#625A6F"),
        "chip": colors.HexColor("#F0E8FF"),
    },
    "default": {
        "label": "Premium System",
        "bg": colors.HexColor("#F7F9FB"),
        "panel": colors.HexColor("#EBF1F7"),
        "header": colors.HexColor("#102B3D"),
        "accent": colors.HexColor("#D9B15D"),
        "text": colors.HexColor("#1E2A38"),
        "muted": colors.HexColor("#607183"),
        "chip": colors.HexColor("#E7F0F8"),
    },
}

KEYWORDS = {
    "food_service": [
        "food", "kitchen", "restaurant", "menu", "breakfast", "lunch", "dinner", "beverage",
        "opening", "closing", "inventory", "safety", "staffing", "vendor", "prep", "franchise",
        "catering", "bar", "shift", "service", "line", "drive", "cashflow", "cash-flow"
    ],
    "retail": [
        "retail", "sales", "store", "checkout", "merch", "planogram", "restock", "return",
        "pricing", "stockroom", "customer", "front", "queue", "display", "upsell", "holiday",
        "cash", "inventory", "daily", "dashboard", "audit"
    ],
    "construction": [
        "construction", "jobsite", "safety", "estimate", "punch", "inspection", "crew", "equipment",
        "site", "material", "change", "permit", "subcontractor", "progress", "cleanup", "weather",
        "roof", "demolition", "paint", "electrical", "plumbing", "hvac", "flooring", "drywall",
        "concrete", "tool", "field", "road", "maintenance"
    ],
    "legal": [
        "legal", "law", "client", "case", "billing", "deadline", "follow", "conflict", "evidence",
        "discovery", "retention", "consultation", "matter", "document", "compliance", "appeal", "court",
        "settlement", "research", "file", "handoff", "paralegal", "notary", "trust", "escrow", "intake"
    ],
    "health": [
        "caregiver", "health", "wellness", "burnout", "recovery", "stress", "anxiety", "sleep", "energy",
        "mood", "symptom", "chronic", "illness", "immune", "support", "benefits", "prescription",
        "pet", "parent", "family", "care", "medical", "clinic", "habit", "brain", "fatigue"
    ],
    "local_business": [
        "business", "ops", "workflow", "system", "dashboard", "checklist", "planner", "tracker",
        "audit", "review", "management", "team", "training", "owner", "launch", "lead", "process",
        "performance", "operations", "admin", "service"
    ],
    "wellness": [
        "budget", "money", "screen", "focus", "habit", "student", "sleep", "routine", "reset",
        "overwhelm", "anxiety", "self", "life", "planner", "debt", "digital", "brain", "time", "hormone",
        "focus", "mindset", "personal", "care"
    ],
}


def classify_theme(title: str, path: Path) -> str:
    haystack = f"{title} {path.as_posix()}".lower()
    for key, words in KEYWORDS.items():
        if any(word in haystack for word in words):
            return key
    return "default"


def title_formatted(stem: str) -> str:
    cleaned = stem.replace("_", " ").replace("-", " ")
    cleaned = re.sub(r"^\d+[\s._-]*", "", cleaned)
    cleaned = " ".join(cleaned.split())
    return cleaned.title() if cleaned else "Premium One-Page System"


def human_summary(title: str) -> list[str]:
    if any(word in title.lower() for word in ["client", "case", "billing", "legal", "court", "intake"]):
        return [
            "Collect the essential facts first.",
            "Map the decision point clearly.",
            "Close the loop before work piles up.",
            "Turn admin into a clean client experience.",
        ]
    if any(word in title.lower() for word in ["job", "site", "crew", "inspection", "safety", "permit", "concrete", "roof", "drywall", "hvac"]):
        return [
            "Reduce jobsite drift and lost time.",
            "Keep safety, schedule, and scope aligned.",
            "Catch issues before they become expensive.",
            "Turn each field day into a clean operating rhythm.",
        ]
    if any(word in title.lower() for word in ["restaurant", "food", "kitchen", "menu", "staffing", "opening", "closing", "inventory", "service"]):
        return [
            "Protect margin and consistency in every shift.",
            "Speed up service decisions without chaos.",
            "Tighten prep, inventory, and staff visibility.",
            "Create a premium operating standard for the team.",
        ]
    if any(word in title.lower() for word in ["retail", "store", "sales", "checkout", "inventory", "returns", "pricing", "display", "customer"]):
        return [
            "Use every customer interaction to move conversion.",
            "Keep stock, pricing, and team flow sharper.",
            "Protect margin while improving the in-store experience.",
            "Turn a simple checklist into a retail advantage.",
        ]
    if any(word in title.lower() for word in ["caregiver", "health", "stress", "burnout", "recovery", "sleep", "brain", "family", "energy", "symptom"]):
        return [
            "Reduce overwhelm with a clearer decision path.",
            "Spot what matters most without more complexity.",
            "Use a calmer system to preserve energy and consistency.",
            "Convert daily pressure into a repeatable routine.",
        ]
    return [
        "Create a more useful system out of the basic task.",
        "Reduce friction and improve daily execution.",
        "Keep the process simple, valuable, and repeatable.",
        "Turn a one-page tool into a premium operating asset.",
    ]


def build_pdf(path: Path, title: str) -> None:
    theme_key = classify_theme(title, path)
    theme = THEMES.get(theme_key, THEMES["default"])

    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter

    c.setFillColor(theme["bg"])
    c.rect(0, 0, width, height, fill=1, stroke=0)

    c.setFillColor(theme["header"])
    c.rect(0, height - 0.7 * inch, width, 0.7 * inch, fill=1, stroke=0)

    c.setFillColor(theme["accent"])
    c.roundRect(0.52 * inch, height - 1.05 * inch, 2.0 * inch, 0.22 * inch, 0.08 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.72 * inch, height - 0.88 * inch, theme["label"].upper())

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.52 * inch, height - 0.42 * inch, "Luxury one-page operating system")

    c.setFillColor(theme["panel"])
    c.roundRect(0.52 * inch, height - 2.45 * inch, width - 1.04 * inch, 1.0 * inch, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(theme["text"])
    c.setFont("Helvetica-Bold", 26)
    wrapped = []
    current = ""
    for token in title.split():
        candidate = f"{current} {token}".strip()
        if len(candidate) <= 19:
            current = candidate
        else:
            wrapped.append(current)
            current = token
    if current:
        wrapped.append(current)
    if len(wrapped) > 2:
        wrapped = wrapped[:2]
    y = height - 1.82 * inch
    for line in wrapped:
        c.drawString(0.8 * inch, y, line)
        y -= 0.28 * inch

    c.setFillColor(theme["chip"])
    c.roundRect(width - 2.15 * inch, height - 2.28 * inch, 1.3 * inch, 0.7 * inch, 0.14 * inch, fill=1, stroke=0)
    c.setFillColor(theme["header"])
    c.setFont("Helvetica-Bold", 16)
    c.drawString(width - 1.9 * inch, height - 1.95 * inch, "Value")
    c.setFont("Helvetica", 9)
    c.drawString(width - 1.88 * inch, height - 2.12 * inch, "premium")

    left_x = 0.7 * inch
    gap = 0.16 * inch
    col_w = 2.42 * inch
    right_x = 3.75 * inch
    last_x = width - 2.9 * inch

    panel_h = 2.2 * inch
    y_start = 3.0 * inch

    c.setFillColor(colors.white)
    c.setStrokeColor(theme["accent"])
    c.roundRect(left_x, y_start, col_w, panel_h, 0.14 * inch, fill=1, stroke=1)
    c.setFillColor(theme["header"])
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_x + 0.18 * inch, y_start + 1.78 * inch, "Priority Actions")
    c.setFillColor(theme["text"])
    c.setFont("Helvetica", 9.2)
    action_lines = [
        "1. Define the goal clearly.",
        "2. Capture the key decision.",
        "3. Prioritize the most valuable move.",
        "4. Finish with a check and reset.",
    ]
    y = y_start + 1.45 * inch
    for line in action_lines:
        c.drawString(left_x + 0.18 * inch, y, line)
        y -= 0.24 * inch

    c.setFillColor(colors.white)
    c.setStrokeColor(theme["accent"])
    c.roundRect(right_x, y_start, col_w, panel_h, 0.14 * inch, fill=1, stroke=1)
    c.setFillColor(theme["header"])
    c.setFont("Helvetica-Bold", 12)
    c.drawString(right_x + 0.18 * inch, y_start + 1.78 * inch, "Why It Converts")
    c.setFillColor(theme["text"])
    c.setFont("Helvetica", 9.2)
    value_lines = human_summary(title)
    y = y_start + 1.45 * inch
    for line in value_lines:
        c.drawString(right_x + 0.18 * inch, y, line)
        y -= 0.24 * inch

    c.setFillColor(colors.white)
    c.setStrokeColor(theme["accent"])
    c.roundRect(last_x, y_start, 2.1 * inch, panel_h, 0.14 * inch, fill=1, stroke=1)
    c.setFillColor(theme["header"])
    c.setFont("Helvetica-Bold", 12)
    c.drawString(last_x + 0.18 * inch, y_start + 1.78 * inch, "Premium Workflow")
    c.setFillColor(theme["text"])
    c.setFont("Helvetica-Bold", 10)
    c.drawString(last_x + 0.18 * inch, y_start + 1.45 * inch, "Step 1")
    c.setFont("Helvetica", 9)
    c.drawString(last_x + 0.18 * inch, y_start + 1.18 * inch, "Set the target outcome.")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(last_x + 0.18 * inch, y_start + 0.88 * inch, "Step 2")
    c.setFont("Helvetica", 9)
    c.drawString(last_x + 0.18 * inch, y_start + 0.61 * inch, "Track the essentials only.")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(last_x + 0.18 * inch, y_start + 0.31 * inch, "Step 3")
    c.setFont("Helvetica", 9)
    c.drawString(last_x + 0.18 * inch, y_start + 0.04 * inch, "Repeat with better speed.")

    c.setFillColor(theme["header"])
    c.roundRect(0.62 * inch, 0.86 * inch, width - 1.24 * inch, 1.2 * inch, 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.9 * inch, 1.66 * inch, "Luxury result")
    c.setFont("Helvetica", 10.2)
    c.drawString(0.9 * inch, 1.32 * inch, "A cleaner one-page system that feels more premium, more useful, and more worth paying for.")

    c.setFillColor(theme["accent"])
    c.roundRect(6.2 * inch, 1.08 * inch, 0.88 * inch, 0.52 * inch, 0.12 * inch, fill=1, stroke=0)
    c.roundRect(7.3 * inch, 1.08 * inch, 0.88 * inch, 0.52 * inch, 0.12 * inch, fill=1, stroke=0)
    c.roundRect(8.4 * inch, 1.08 * inch, 0.88 * inch, 0.52 * inch, 0.12 * inch, fill=1, stroke=0)
    c.setFillColor(theme["header"])
    c.setFont("Helvetica-Bold", 9)
    c.drawString(6.44 * inch, 1.25 * inch, "FAST")
    c.drawString(7.52 * inch, 1.25 * inch, "CLEAR")
    c.drawString(8.64 * inch, 1.25 * inch, "USEFUL")

    c.save()


def main() -> None:
    pdf_files = sorted(ROOT.rglob("*.pdf"))
    for pdf_path in pdf_files:
        title = title_formatted(pdf_path.stem)
        build_pdf(pdf_path, title)
    print(f"Luxury premiumized {len(pdf_files)} PDFs in {ROOT}")


if __name__ == "__main__":
    main()
