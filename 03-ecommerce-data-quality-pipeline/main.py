from src.loader import load_data, profile_data, print_profile_summary
from src.validator import run_validation, print_validation_summary
from src.cleaner import clean_data, save_clean_data, print_cleaning_summary
from src.reporter import generate_report

# ── CONFIG ──────────────────────────────────────────────
RAW_FILE        = "data/raw/autos.csv"
CLEAN_FILE      = "output/clean/autos_clean.csv"
REPORT_FILE     = "output/reports/data_quality_report.pdf"
# ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  GROWINDATA — DATA QUALITY PIPELINE")
    print("="*55 + "\n")

    # ── PHASE 1: Load & Profile ──────────────────────────
    print("► PHASE 1: Load & Profile")
    df = load_data(RAW_FILE)
    profile = profile_data(df)
    print_profile_summary(profile)

    # ── PHASE 2: Validate ────────────────────────────────
    print("\n► PHASE 2: Validation Rules Engine")
    issues = run_validation(df)
    print_validation_summary(issues)

    # ── PHASE 3: Clean ───────────────────────────────────
    print("\n► PHASE 3: Automated Cleaning")
    df_clean, cleaning_report = clean_data(df, issues)
    print_cleaning_summary(cleaning_report)
    save_clean_data(df_clean, CLEAN_FILE)

    # ── PHASE 4: Report ──────────────────────────────────
    print("\n► PHASE 4: Generating PDF Report")
    generate_report(profile, issues, cleaning_report, REPORT_FILE)

    print("\n" + "="*55)
    print("  PIPELINE COMPLETE")
    print(f"  Clean data : {CLEAN_FILE}")
    print(f"  PDF report : {REPORT_FILE}")
    print("="*55 + "\n")