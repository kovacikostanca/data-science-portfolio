import pandas as pd
import numpy as np


def run_validation(df: pd.DataFrame) -> dict:
    """
    Run all validation rules against the dataset.
    Returns a dictionary of issues found per rule.
    """
    print("\n  Running validation rules engine...")
    issues = {}

    # ── RULE 1: Duplicate rows ───────────────────────────
    dupes = df.duplicated()
    issues["duplicate_rows"] = {
        "count": int(dupes.sum()),
        "description": "Exact duplicate rows",
        "severity": "HIGH",
        "indices": df[dupes].index.tolist()
    }

    # ── RULE 2: Price out of valid range ─────────────────
    # Valid car price: EUR100 to EUR150,000
    invalid_price = (df["price"] < 100) | (df["price"] > 150_000)
    issues["invalid_price"] = {
        "count": int(invalid_price.sum()),
        "description": "Price outside valid range (EUR100 - EUR150,000)",
        "severity": "HIGH",
        "indices": df[invalid_price].index.tolist()
    }

    # ── RULE 3: Year of registration out of valid range ──
    # Valid years: 1950 to 2016 (dataset was scraped in 2016)
    invalid_year = (df["yearOfRegistration"] < 1950) | (df["yearOfRegistration"] > 2016)
    issues["invalid_year"] = {
        "count": int(invalid_year.sum()),
        "description": "Year of registration outside valid range (1950-2016)",
        "severity": "HIGH",
        "indices": df[invalid_year].index.tolist()
    }

    # ── RULE 4: Power (PS) out of valid range ────────────
    # Valid engine power: 10 PS to 1,000 PS
    invalid_power = (df["powerPS"] < 10) | (df["powerPS"] > 1_000)
    issues["invalid_power"] = {
        "count": int(invalid_power.sum()),
        "description": "Engine power outside valid range (10-1,000 PS)",
        "severity": "MEDIUM",
        "indices": df[invalid_power].index.tolist()
    }

    # ── RULE 5: Month of registration invalid ────────────
    # Valid months: 1 to 12 (0 is unknown/missing)
    invalid_month = (df["monthOfRegistration"] < 1) | (df["monthOfRegistration"] > 12)
    issues["invalid_month"] = {
        "count": int(invalid_month.sum()),
        "description": "Month of registration outside valid range (1-12)",
        "severity": "LOW",
        "indices": df[invalid_month].index.tolist()
    }

    # ── RULE 6: Missing vehicleType ──────────────────────
    missing_vehicle_type = df["vehicleType"].isnull()
    issues["missing_vehicle_type"] = {
        "count": int(missing_vehicle_type.sum()),
        "description": "Missing vehicle type",
        "severity": "MEDIUM",
        "indices": df[missing_vehicle_type].index.tolist()
    }

    # ── RULE 7: Missing fuelType ─────────────────────────
    missing_fuel = df["fuelType"].isnull()
    issues["missing_fuel_type"] = {
        "count": int(missing_fuel.sum()),
        "description": "Missing fuel type",
        "severity": "MEDIUM",
        "indices": df[missing_fuel].index.tolist()
    }

    # ── RULE 8: Missing gearbox ──────────────────────────
    missing_gearbox = df["gearbox"].isnull()
    issues["missing_gearbox"] = {
        "count": int(missing_gearbox.sum()),
        "description": "Missing gearbox type",
        "severity": "LOW",
        "indices": df[missing_gearbox].index.tolist()
    }

    # ── RULE 9: Missing model ────────────────────────────
    missing_model = df["model"].isnull()
    issues["missing_model"] = {
        "count": int(missing_model.sum()),
        "description": "Missing car model",
        "severity": "MEDIUM",
        "indices": df[missing_model].index.tolist()
    }

    # ── RULE 10: Missing notRepairedDamage ───────────────
    missing_damage = df["notRepairedDamage"].isnull()
    issues["missing_damage_info"] = {
        "count": int(missing_damage.sum()),
        "description": "Missing damage status (notRepairedDamage)",
        "severity": "MEDIUM",
        "indices": df[missing_damage].index.tolist()
    }

    # ── RULE 11: Useless column — nrOfPictures ───────────
    all_zero_pictures = (df["nrOfPictures"] == 0).all()
    issues["useless_column_pictures"] = {
        "count": int(all_zero_pictures),
        "description": "nrOfPictures column is 0 for all rows - no information",
        "severity": "LOW",
        "indices": []
    }

    # ── RULE 12: Seller type suspicious ──────────────────
    # 'gewerblich' = commercial, 'privat' = private
    # Flag commercial sellers as they may be outliers in a private marketplace
    commercial = df["seller"] == "gewerblich"
    issues["commercial_sellers"] = {
        "count": int(commercial.sum()),
        "description": "Listings from commercial sellers (may skew price analysis)",
        "severity": "LOW",
        "indices": df[commercial].index.tolist()
    }

    # ── RULE 13: offerType not 'Angebot' ─────────────────
    # 'Angebot' = offer (normal listing), 'Gesuch' = wanted ad
    not_offer = df["offerType"] != "Angebot"
    issues["non_standard_offer_type"] = {
        "count": int(not_offer.sum()),
        "description": "Listings that are 'wanted ads' not actual offers",
        "severity": "MEDIUM",
        "indices": df[not_offer].index.tolist()
    }

    # ── RULE 14: Kilometer value suspicious ──────────────
    # Dataset already has min 5,000 km but flag unrealistically low
    low_km = df["kilometer"] < 5_000
    issues["suspiciously_low_km"] = {
        "count": int(low_km.sum()),
        "description": "Kilometer reading below 5,000 (suspiciously low for used car)",
        "severity": "LOW",
        "indices": df[low_km].index.tolist()
    }

    print(f"  Validation complete — {len(issues)} rules checked")
    return issues


def print_validation_summary(issues: dict):
    """Print a readable validation summary to the terminal."""

    total_issues = sum(v["count"] for v in issues.values())
    high   = [(k, v) for k, v in issues.items() if v["severity"] == "HIGH"]
    medium = [(k, v) for k, v in issues.items() if v["severity"] == "MEDIUM"]
    low    = [(k, v) for k, v in issues.items() if v["severity"] == "LOW"]

    print("\n" + "="*55)
    print("  VALIDATION REPORT")
    print("="*55)
    print(f"  Rules checked     : {len(issues)}")
    print(f"  Total issues found: {total_issues:,}")
    print(f"  HIGH severity     : {len(high)}")
    print(f"  MEDIUM severity   : {len(medium)}")
    print(f"  LOW severity      : {len(low)}")

    for label, group in [("🔴 HIGH", high), ("🟡 MEDIUM", medium), ("🟢 LOW", low)]:
        print(f"\n  {label} SEVERITY ISSUES:")
        print(f"  {'Rule':<35} {'Count':>10}")
        print(f"  {'-'*45}")
        for key, val in group:
            print(f"  {val['description']:<35} {val['count']:>10,}")

    print("="*55)