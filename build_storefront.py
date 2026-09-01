from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORE = ROOT / "storefront"
STORE.mkdir(exist_ok=True)

CATEGORY_PRIORITY = {
    "AI & productivity": 100,
    "Work-life balance": 96,
    "Small business": 94,
    "Money & budgeting": 98,
    "Health & insurance": 92,
    "Caregiving": 96,
    "Senior care": 92,
    "Family systems": 86,
    "Home ops": 84,
    "Lifestyle & wellness": 80,
    "Digital life": 78,
    "Pet care": 76,
    "Healthcare": 90,
    "Legal": 88,
    "Marketing": 84,
    "Business ops": 90,
    "Digital business": 86,
    "Home services": 82,
    "Real estate": 82,
    "Wellness": 80,
    "Local business": 81,
    "default": 60,
}

KEYWORD_BOOST = {
    "burnout": 14,
    "stress": 12,
    "budget": 12,
    "reset": 10,
    "recovery": 11,
    "care": 12,
    "insurance": 14,
    "risk": 8,
    "cash": 10,
    "ops": 10,
    "planner": 7,
    "tracker": 7,
    "guide": 6,
    "checklist": 6,
    "overwhelm": 12,
    "family": 8,
    "senior": 10,
    "home": 6,
    "safety": 8,
    "energy": 6,
    "digital": 7,
    "marketing": 8,
    "legal": 10,
    "estate": 8,
}

BUNDLE_DEFS = [
    {
        "name": "AI Burnout Recovery Pack",
        "category": "AI & productivity",
        "price": 39.99,
        "products": [
            "AI Overwhelm Reset",
            "Prompt Fatigue Recovery",
            "Work From Home Boundary Planner",
            "Remote Burnout Recovery Sheet",
            "Hybrid Job Energy Tracker",
        ],
    },
    {
        "name": "Money Stress Survival Pack",
        "category": "Money & budgeting",
        "price": 39.99,
        "products": [
            "Emergency Savings Sprint",
            "Rent Pressure Survival Guide",
            "Housing Cost Anxiety Tracker",
            "Inflation Budget Reset",
            "Utility Cost Slashing Sheet",
            "Debt Stress Recovery Plan",
        ],
    },
    {
        "name": "Caregiver Relief Bundle",
        "category": "Caregiving",
        "price": 49.99,
        "products": [
            "Caregiver Capacity Reset",
            "Caregiver Hand-Off Sheet",
            "Caregiver Burnout Reset",
            "Medication Review Timeline",
            "Family Care Timeline",
        ],
    },
    {
        "name": "Small Business Cash Flow Bundle",
        "category": "Small business",
        "price": 49.99,
        "products": [
            "Freelance Cash Flow Stability",
            "Gig Income Buffer Planner",
            "Side Hustle Profit Snapshot",
            "Household Systems Dashboard",
            "Home Energy Cost Tracker",
        ],
    },
    {
        "name": "Home Ops Reset Pack",
        "category": "Home ops",
        "price": 29.99,
        "products": [
            "Home Safety & Routine Guide",
            "Neighborhood Emergency Prep",
            "Pantry Inventory Sheet",
            "Closet Reset Worksheet",
            "Laundry Room Flow Planner",
        ],
    },
    {
        "name": "Healthcare & Insurance Pack",
        "category": "Health & insurance",
        "price": 59.99,
        "products": [
            "Healthcare Benefits Navigator",
            "Prescription Routine Organizer",
            "Medication Review Timeline",
            "Senior Wellness Scorecard",
            "Aging-in-Place Routine",
        ],
    },
    {
        "name": "Senior Care Family Bundle",
        "category": "Senior care",
        "price": 59.99,
        "products": [
            "Senior Move Planning Sheet",
            "Home Safety Audit",
            "Aging-in-Place Routine",
            "Mobility Support Checklist",
            "End-of-Life Planning Organizer",
        ],
    },
    {
        "name": "Digital Wellness Starter Pack",
        "category": "Lifestyle & wellness",
        "price": 29.99,
        "products": [
            "Digital Detox Recovery Plan",
            "Phone Overload Reset",
            "Climate Anxiety Recovery",
            "Hybrid Job Energy Tracker",
            "Work From Home Boundary Planner",
        ],
    },
    {
        "name": "Creator & Local Business Pack",
        "category": "Digital business",
        "price": 49.99,
        "products": [
            "Business Systems Dashboard",
            "Client Intake Sheet",
            "Follow Up Tracker",
            "Marketing Calendar",
            "Website Content Planner",
        ],
    },
    {
        "name": "Pet Care Essentials Bundle",
        "category": "Pet care",
        "price": 34.99,
        "products": [
            "Pet Health Check Reminder",
            "Pet Insurance Cost Tracker",
            "Vet Appointment Organizer",
            "Pet Feeding Tracker",
            "Pet Emergency Plan",
        ],
    },
]


def normalize_category(value: str) -> str:
    return (value or "default").strip().replace("_", " ")


def score_row(row: dict) -> int:
    title = (row.get("title") or "").strip()
    category = normalize_category(row.get("category") or "default")
    price = float(row.get("price_usd") or row.get("price") or 0)
    score = CATEGORY_PRIORITY.get(category, CATEGORY_PRIORITY["default"])
    text = f"{title} {category}".lower()
    for keyword, boost in KEYWORD_BOOST.items():
        if keyword in text:
            score += boost
    if price >= 8:
        score += 8
    elif price >= 5:
        score += 4
    return score


def load_market_rows() -> list[dict]:
    rows: list[dict] = []
    csv_paths = list(ROOT.glob("market-reach-*.csv")) + list(ROOT.glob("**/market_reach_*.csv"))
    seen: set[str] = set()
    for path in sorted(csv_paths):
        if not path.name.endswith(".csv"):
            continue
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        try:
            with path.open("r", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    title = (row.get("title") or row.get("product") or row.get("Product") or "").strip()
                    filename = (row.get("filename") or row.get("file") or "").strip()
                    category = normalize_category(row.get("category") or row.get("Category") or "")
                    price = row.get("price_usd") or row.get("price") or "0"
                    if not title and not filename:
                        continue
                    rows.append({
                        "title": title,
                        "category": category,
                        "price_usd": price,
                        "filename": filename,
                    })
        except Exception:
            continue
    return rows


def build_hero_products() -> list[dict]:
    rows = load_market_rows()
    scored = []
    for row in rows:
        if not row.get("title"):
            continue
        row = dict(row)
        row["score"] = score_row(row)
        row["buyer"] = row["category"]
        row["intent"] = "high-intent" if float(row.get("price_usd") or 0) >= 5 else "value"
        scored.append(row)
    scored.sort(key=lambda x: (-int(x["score"]), -float(x["price_usd"] or 0), x["title"]))
    seen_files: set[str] = set()
    hero = []
    for row in scored:
        filename = (row.get("filename") or "").strip()
        if not filename or filename in seen_files:
            continue
        seen_files.add(filename)
        hero.append(row)
        if len(hero) >= 200:
            break
    return hero


def write_hero_csv(rows: list[dict]) -> None:
    target = STORE / "hero-products.csv"
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "title", "category", "buyer", "price_usd", "filename", "intent", "score"])
        for i, row in enumerate(rows, start=1):
            writer.writerow([
                i,
                row.get("title", ""),
                row.get("category", ""),
                row.get("buyer", row.get("category", "")),
                row.get("price_usd", ""),
                row.get("filename", ""),
                row.get("intent", "high-intent"),
                row.get("score", 0),
            ])


def write_bundle_csv() -> None:
    target = STORE / "premium-bundles.csv"
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["bundle_name", "category", "price_usd", "incl_1", "incl_2", "incl_3", "incl_4", "incl_5", "incl_6"])
        for bundle in BUNDLE_DEFS:
            values = [bundle["name"], bundle["category"], bundle["price"]]
            for idx in range(6):
                values.append(bundle["products"][idx] if idx < len(bundle["products"]) else "")
            writer.writerow(values)


def write_readme() -> None:
    readme = STORE / "README.md"
    readme.write_text(
        """# Sales storefront

This storefront is the conversion-focused front-end for the repo. The full archive remains intact, but the sales layer now highlights the products most likely to convert quickly.

## Structure

- `hero-products.csv` — the highest-priority 200 items selected from the demand-heavy market bundles.
- `premium-bundles.csv` — curated premium packs designed for higher AOV and clearer buyer intent.
- `bundle-briefs/` — reserved for the next layer of expanded bundle narratives and campaign naming.

## Recommended sales flow

1. Front with the hero products.
2. Upsell premium bundles.
3. Use niche bundles for ad targeting.
4. Keep the full catalog as the long-tail archive.

## Best conversion themes

- AI/work overload
- money stress and budgeting
- caregiver and senior support
- healthcare and benefits navigation
- small business cash flow
- home ops and household systems
- digital wellness and work-life boundaries

## Sales guidance

Keep the storefront simple, clean, and pain-driven. Buyers are responding to clear problems, not broad catalog breadth.
""",
        encoding="utf-8",
    )

    bundle_dir = STORE / "bundle-briefs"
    bundle_dir.mkdir(exist_ok=True)
    (bundle_dir / ".gitkeep").write_text("", encoding="utf-8")


def main() -> None:
    rows = build_hero_products()
    write_hero_csv(rows)
    write_bundle_csv()
    write_readme()
    print(f"Wrote {len(rows)} hero products and bundle briefs to {STORE}")


if __name__ == "__main__":
    main()
