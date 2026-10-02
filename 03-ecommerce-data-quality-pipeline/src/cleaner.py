import pandas as pd
import numpy as np
import os

def clean_data(df: pd.DataFrame, issues: dict) -> tuple[pd.DataFrame, dict]:
    """Clean the dataset based on validation findings. Returns a 
    cleaned DataFrame and a cleaning report dictionary."""
    print("\n Running automated cleaning pipeline...")

    report = {}
    original_count = len(df)
    df = df.copy()

    # ----- Step 1: Remove exact duplicates -----
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    report["duplicates_removed"] = removed
    print(f" Step 1: Removed {removed:,} duplicate rows")

    # ----- Step 2: Remove invalid prices -----
    before = len(df)
    df = df[(df["price"] >= 100) & (df["price"] <= 150_000)]
    removed = before - len(df)
    report["invalid_price_removed"] = removed
    print(f" Step 2: Removed {removed:,} rows with invalid prices")

    # ----- Step 3: Remove invalid registration years -----
    before = len(df)
    df = df[
        (df["yearOfRegistration"] >= 1950) &
        (df["yearOfRegistration"] <= 2016)
    ]
    removed = before - len(df)
    report["invalid_year_removed"] = removed
    print(f" Step 3: Removed {removed:,} rows with invalid registration years")

    # ----- Step 4: Fix invalid power values -----
    # Replace out-of-range power with NaN rather than dropping rows
    before_nulls = df["powerPS"].isnull().sum()
    df.loc[(df["powerPS"] < 10) | (df["powerPS"] > 1_000), "powerPS"] = np.nan
    after_nulls = df["powerPS"].isnull().sum()
    flagged = int(after_nulls - before_nulls)
    report["invalid_power_nulled"] = flagged
    print(f" Step 4: Nulled {flagged:,} invalid powerPS values")


    # ----- Step 5: Fix invalid month values -----
    # Replace month 0 or >12 with NaN
    before_nulls = df["monthOfRegistration"].isnull().sum()
    df.loc[
        (df["monthOfRegistration"] < 1 | (df["monthOfRegistration"] > 12), "monthOfRegistration")
    ] = np.nan
    after_nulls = df["monthOfRegistration"].isnull().sum()
    flagged = int(after_nulls - before_nulls)
    report["invalid_month_nulled"] = flagged
    print(f" Step 5: Nulled {flagged:,} invalid monthOfRegistration values")


    # ----- Step 6: Remove 'wanted ads' (not real listings) -----
    before = len(df)
    df = df[df["offerType"] == "Angebot"]
    removed = before - len(df)
    report["wanted_ads_removed"] = removed
    print(f" Step 6: Removed {removed:,} wanted ad listings")

    # ── STEP 7: Remove commercial sellers ───────────────
    before = len(df)
    df = df[df["seller"] == "privat"]
    removed = before - len(df)
    report["commercial_sellers_removed"] = removed
    print(f" Step 7: Removed {removed:,} commercial seller listings")
 
    # ── STEP 8: Drop useless column ─────────────────────
    df = df.drop(columns=["nrOfPictures"])
    report["columns_dropped"] = ["nrOfPictures"]
    print(f" Step 8: Dropped 'nrOfPictures' column (all zeros)")
 
    # ── STEP 9: Fill missing categorical with 'unknown' ─
    fill_cols = ["vehicleType", "gearbox", "fuelType", "notRepairedDamage", "model"]
    for col in fill_cols:
        nulls = df[col].isnull().sum()
        df[col] = df[col].fillna("unknown")
        report[f"filled_{col}"] = int(nulls)
    print(f" Step 9: Filled missing categorical values with 'unknown'")
 
    # ── STEP 10: Standardize text columns to lowercase ──
    text_cols = ["vehicleType", "gearbox", "fuelType",
                 "notRepairedDamage", "model", "brand"]
    for col in text_cols:
        df[col] = df[col].str.strip().str.lower()
    report["text_columns_standardized"] = text_cols
    print(f" Step 10: Standardized text columns to lowercase")
 
    # ── STEP 11: Reset index ────────────────────────────
    df = df.reset_index(drop=True)
 
    # ── FINAL SUMMARY ───────────────────────────────────
    final_count = len(df)
    report["original_row_count"] = original_count
    report["final_row_count"] = final_count
    report["rows_removed_total"] = original_count - final_count
    report["rows_retained_pct"] = round((final_count / original_count) * 100, 1)
    report["final_column_count"] = len(df.columns)
 
    print(f"\n  Cleaning complete")
    print(f"     Original : {original_count:,} rows")
    print(f"     Cleaned  : {final_count:,} rows")
    print(f"     Removed  : {original_count - final_count:,} rows")
    print(f"     Retained : {report['rows_retained_pct']}%")
 
    return df, report
 
 
def save_clean_data(df: pd.DataFrame, output_path: str):
    """Save the cleaned dataset to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\n  Clean dataset saved to: {output_path}")
 
 
def print_cleaning_summary(report: dict):
    """Print a readable cleaning summary to the terminal."""
    print("\n" + "="*55)
    print("  CLEANING REPORT")
    print("="*55)
    print(f"  Original rows        : {report['original_row_count']:,}")
    print(f"  Final rows           : {report['final_row_count']:,}")
    print(f"  Total rows removed   : {report['rows_removed_total']:,}")
    print(f"  Data retained        : {report['rows_retained_pct']}%")
    print(f"  Final column count   : {report['final_column_count']}")
 
    print("\n  ACTIONS TAKEN:")
    print(f"  {'Action':<45} {'Count':>8}")
    print(f"  {'-'*53}")
 
    actions = [
        ("Duplicate rows removed",           report.get("duplicates_removed", 0)),
        ("Invalid price rows removed",        report.get("invalid_price_removed", 0)),
        ("Invalid year rows removed",         report.get("invalid_year_removed", 0)),
        ("Invalid powerPS values nulled",     report.get("invalid_power_nulled", 0)),
        ("Invalid month values nulled",       report.get("invalid_month_nulled", 0)),
        ("Wanted ad listings removed",        report.get("wanted_ads_removed", 0)),
        ("Commercial seller rows removed",    report.get("commercial_sellers_removed", 0)),
        ("Columns dropped",                   len(report.get("columns_dropped", []))),
        ("vehicleType nulls filled",          report.get("filled_vehicleType", 0)),
        ("gearbox nulls filled",              report.get("filled_gearbox", 0)),
        ("fuelType nulls filled",             report.get("filled_fuelType", 0)),
        ("model nulls filled",                report.get("filled_model", 0)),
        ("notRepairedDamage nulls filled",    report.get("filled_notRepairedDamage", 0)),
    ]
 
    for action, count in actions:
        print(f"  {action:<45} {count:>8,}")
 
    print("="*55)
