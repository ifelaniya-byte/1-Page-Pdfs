from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PRICE_RULES = {
    "AI productivity": 17.99,
    "Business ops": 19.99,
    "Finance": 19.99,
    "Healthcare": 24.99,
    "Legal": 24.99,
    "Home services": 16.99,
    "Real estate": 18.99,
    "Marketing": 17.99,
    "Community": 15.99,
    "Technology": 16.99,
    "Lifestyle": 15.99,
    "Digital business": 18.99,
    "Freelance": 17.99,
    "Senior care": 19.99,
    "Wellness": 15.99,
    "Pet care": 15.99,
    "Events": 17.99,
    "Digital life": 14.99,
    "Hospitality": 18.99,
    "Small business": 19.99,
    "Education": 16.99,
    "Work-life balance": 17.99,
    "Money & budgeting": 17.99,
    "Health & insurance": 21.99,
    "Caregiving": 18.99,
    "Family systems": 16.99,
    "Home ops": 16.99,
    "Lifestyle & wellness": 15.99,
    "Health & wellness": 17.99,
    "Education & career": 17.99,
    "Local business": 18.99,
    "AI & productivity": 17.99,
    "Operations": 18.99,
    "Real Estate": 18.99,
    "Restaurant & Food Service": 16.99,
    "Retail & Store Ops": 17.99,
    "Construction & Trades": 18.99,
    "Legal & Professional Services": 24.99,
    "default": 14.99,
}

KEYWORD_ADJUSTMENTS = {
    "insurance": 2.0,
    "legal": 3.0,
    "estate": 4.0,
    "medical": 2.0,
    "benefits": 2.0,
    "debt": 1.5,
    "budget": 1.0,
    "mortgage": 1.5,
    "rent": 1.0,
    "tax": 1.5,
    "contract": 2.0,
    "care": 1.0,
    "elder": 1.5,
    "senior": 1.5,
    "service": 1.0,
    "repair": 1.0,
    "business": 1.0,
    "marketing": 1.0,
    "ai": 1.0,
    "automation": 1.0,
}


def normalize_category(value: str) -> str:
    value = (value or "").strip()
    return value.replace("_", " ")


def competitive_price(title: str, category: str) -> float:
    category_key = normalize_category(category)
    base = PRICE_RULES.get(category_key, PRICE_RULES["default"])
    text = f"{title} {category}".lower()
    adjustment = 0.0
    for keyword, delta in KEYWORD_ADJUSTMENTS.items():
        if keyword in text:
            adjustment += delta
    price = base + adjustment
    # Keep pricing within realistic, competitive ranges.
    if price < 9.99:
        return 9.99
    if price > 29.99:
        return 29.99
    return round(price, 2)


def update_csv(path: Path) -> int:
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return 0
    header = rows[0]
    if "price" not in header and "price_usd" not in header:
        return 0
    changed = 0
    price_idx = None
    title_idx = None
    category_idx = None
    for idx, col in enumerate(header):
        lowered = col.lower()
        if lowered in {"price", "price_usd"}:
            price_idx = idx
        if lowered in {"product", "title", "name"}:
            title_idx = idx
        if lowered == "category":
            category_idx = idx
    if price_idx is None:
        return 0
    for row in rows[1:]:
        if len(row) <= price_idx:
            continue
        title_value = row[title_idx] if title_idx is not None and len(row) > title_idx else ""
        category_value = row[category_idx] if category_idx is not None and len(row) > category_idx else ""
        new_price = competitive_price(title_value, category_value)
        row[price_idx] = f"{new_price:.2f}"
        changed += 1
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    return changed


def main() -> None:
    targets = [
        *sorted(ROOT.glob("market-reach-*.csv")),
        *sorted(ROOT.glob("**/market_reach_*.csv")),
        *sorted(ROOT.glob("**/launch_batch_*.csv")),
        *sorted(ROOT.glob("**/*.csv"))
    ]
    seen = set()
    updated = []
    for p in targets:
        key = str(p.resolve())
        if key in seen:
            continue
        seen.add(key)
        if p.name.endswith(".csv") and "market-reach" in p.as_posix() or "launch_batch" in p.name or p.name.lower() == "catalog_1000.csv":
            try:
                count = update_csv(p)
                if count:
                    updated.append((p.as_posix(), count))
            except Exception:
                pass
    print(f"Updated {len(updated)} CSV files with competitive pricing")
    for path, count in updated[:10]:
        print(f"- {path}: {count} rows")


if __name__ == "__main__":
    main()
