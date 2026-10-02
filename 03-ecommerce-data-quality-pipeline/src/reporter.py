from fpdf import FPDF
from datetime import datetime
import os

def safe(text):
    return str(text).encode("latin-1", errors="replace").decode("latin-1")
 
 
class DataQualityReport(FPDF):
    """Custom PDF class with GrowInData branding."""
 
    def header(self):
        self.set_fill_color(99, 102, 241)
        self.rect(0, 0, 210, 2, "F")
 
        self.set_y(8)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(99, 102, 241)
        self.cell(0, 8, "GrowInData", ln=False, align="L")
 
        self.set_font("Helvetica", "", 9)
        self.set_text_color(140, 140, 160)
        self.cell(0, 8, "Data Quality Pipeline Report", ln=True, align="R")
 
        self.set_draw_color(220, 220, 235)
        self.set_line_width(0.3)
        self.line(10, 18, 200, 18)
        self.ln(6)
 
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(160, 160, 180)
        self.cell(0, 10, "GrowInData  |  growindata.com  |  Page " + str(self.page_no()), align="C")
        self.set_fill_color(99, 102, 241)
        self.rect(0, 295, 210, 2, "F")
 
    def section_title(self, title):
        self.ln(4)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(99, 102, 241)
        self.cell(0, 8, title, ln=True)
        self.set_draw_color(99, 102, 241)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)
 
    def stat_box(self, label, value, color=(99, 102, 241)):
        x = self.get_x()
        y = self.get_y()
        w, h = 56, 22
 
        self.set_fill_color(245, 245, 252)
        self.set_draw_color(*color)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "DF")
 
        self.set_xy(x, y + 3)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*color)
        self.cell(w, 8, value, align="C")
 
        self.set_xy(x, y + 12)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(100, 100, 120)
        self.cell(w, 6, label, align="C")
 
        self.set_xy(x + w + 3, y)
 
    def body_text(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(60, 60, 80)
        self.multi_cell(0, 5.5, text)
        self.ln(2)
 
    def table_header(self, cols, widths):
        self.set_fill_color(99, 102, 241)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8.5)
        for col, w in zip(cols, widths):
            self.cell(w, 7, col, border=0, fill=True, align="L")
        self.ln()
 
    def table_row(self, values, widths, shade=False):
        if shade:
            self.set_fill_color(247, 247, 252)
        else:
            self.set_fill_color(255, 255, 255)
        self.set_text_color(50, 50, 70)
        self.set_font("Helvetica", "", 8.5)
        for val, w in zip(values, widths):
            self.cell(w, 6.5, safe(val), border=0, fill=True, align="L")
        self.ln()
 
 
def generate_report(profile, issues, cleaning_report, output_path):
    """Generate the full PDF data quality report."""
    print("\n  Generating PDF report...")
 
    pdf = DataQualityReport(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(10, 10, 10)
    pdf.add_page()
 
    now = datetime.now().strftime("%B %d, %Y  %H:%M")
 
    total_issues = sum(v["count"] for v in issues.values())
    rows_removed = cleaning_report.get("rows_removed_total", 0)
    retained_pct = cleaning_report.get("rows_retained_pct", 0)
    original     = cleaning_report.get("original_row_count", 0)
    clean_rows   = cleaning_report.get("final_row_count", 0)
 
    # ── COVER ────────────────────────────────────────────
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 50)
    pdf.cell(0, 12, "Data Quality Report", ln=True)
 
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(140, 140, 160)
    pdf.cell(0, 6, "Dataset: eBay Kleinanzeigen Used Cars  |  Generated: " + now, ln=True)
    pdf.ln(6)
 
    # ── EXECUTIVE SUMMARY ────────────────────────────────
    pdf.section_title("Executive Summary")
 
    pdf.stat_box("Total Records",    str(f"{original:,}"),    (99, 102, 241))
    pdf.stat_box("Issues Detected",  str(f"{total_issues:,}"),(220, 38, 38))
    pdf.stat_box("Records Removed",  str(f"{rows_removed:,}"),(217, 119, 6))
    pdf.ln(28)
 
    pdf.stat_box("Clean Records",    str(f"{clean_rows:,}"),  (22, 163, 74))
    pdf.stat_box("Data Retained",    str(f"{retained_pct}%"), (22, 163, 74))
    pdf.stat_box("Rules Checked",    str(len(issues)),         (99, 102, 241))
    pdf.ln(30)
 
    pdf.body_text(
        "This report documents the findings of an automated data quality audit run on the "
        "eBay Kleinanzeigen Used Cars dataset. The pipeline profiled, validated, and cleaned "
        + str(f"{original:,}") + " raw records across 20 columns, identifying "
        + str(f"{total_issues:,}") + " data quality issues across 14 validation rules. "
        "After cleaning, " + str(f"{clean_rows:,}") + " records ("
        + str(retained_pct) + "% of the original dataset) were retained as analysis-ready data."
    )
 
    # ── PHASE 1: PROFILE ─────────────────────────────────
    pdf.section_title("Phase 1 - Data Profile")
 
    pdf.body_text(
        "The raw dataset contained " + str(f"{profile['total_rows']:,}") + " rows across "
        + str(profile['total_columns']) + " columns. "
        + str(profile['duplicate_rows']) + " exact duplicate rows were identified during profiling."
    )
 
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(60, 60, 80)
    pdf.cell(0, 6, "Missing Values by Column", ln=True)
    pdf.ln(1)
 
    pdf.table_header(["Column", "Missing Count", "Missing %"], [80, 50, 50])
    shade = False
    for col, stats in profile["missing_values"].items():
        if stats["count"] > 0:
            pdf.table_row(
                [col, f"{stats['count']:,}", f"{stats['percentage']}%"],
                [80, 50, 50], shade
            )
            shade = not shade
    pdf.ln(4)
 
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(60, 60, 80)
    pdf.cell(0, 6, "Numeric Column Ranges", ln=True)
    pdf.ln(1)
 
    pdf.table_header(["Column", "Min", "Max", "Mean"], [60, 40, 55, 35])
    shade = False
    for col, stats in profile["numeric_stats"].items():
        if stats["min"] is not None:
            pdf.table_row(
                [col, f"{stats['min']:,.1f}", f"{stats['max']:,.1f}", f"{stats['mean']:,.1f}"],
                [60, 40, 55, 35], shade
            )
            shade = not shade
    pdf.ln(4)
 
    # ── PHASE 2: VALIDATION ──────────────────────────────
    pdf.add_page()
    pdf.section_title("Phase 2 - Validation Rules Engine")
 
    high   = [(k, v) for k, v in issues.items() if v["severity"] == "HIGH"]
    medium = [(k, v) for k, v in issues.items() if v["severity"] == "MEDIUM"]
    low    = [(k, v) for k, v in issues.items() if v["severity"] == "LOW"]
 
    pdf.body_text(
        str(len(issues)) + " validation rules were run against the dataset. "
        "A total of " + str(f"{total_issues:,}") + " issues were detected: "
        + str(len(high)) + " HIGH severity, "
        + str(len(medium)) + " MEDIUM severity, and "
        + str(len(low)) + " LOW severity."
    )
 
    cols   = ["Severity", "Rule Description", "Issues Found"]
    widths = [28, 120, 32]
 
    for label, group, color in [
        ("HIGH SEVERITY",   high,   (220, 38, 38)),
        ("MEDIUM SEVERITY", medium, (217, 119, 6)),
        ("LOW SEVERITY",    low,    (22, 163, 74)),
    ]:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*color)
        pdf.cell(0, 7, "* " + label, ln=True)
        pdf.ln(1)
        pdf.table_header(cols, widths)
        shade = False
        for key, val in group:
            desc = val["description"].replace("EUR", "EUR").replace("€", "EUR")
            pdf.table_row(
                [val["severity"], desc, f"{val['count']:,}"],
                widths, shade
            )
            shade = not shade
        pdf.ln(5)
 
    # ── PHASE 3: CLEANING ────────────────────────────────
    pdf.add_page()
    pdf.section_title("Phase 3 - Automated Cleaning")
 
    pdf.body_text(
        "The cleaning pipeline applied 10 automated steps to resolve identified issues. "
        + str(f"{rows_removed:,}") + " rows were removed from the dataset, retaining "
        + str(f"{clean_rows:,}") + " clean records (" + str(retained_pct) + "% of original data). "
        "The cleaned dataset was saved to output/clean/autos_clean.csv."
    )
 
    cols   = ["Cleaning Action", "Records Affected"]
    widths = [140, 40]
    pdf.table_header(cols, widths)
 
    actions = [
        ("Duplicate rows removed",                  cleaning_report.get("duplicates_removed", 0)),
        ("Invalid price rows removed",               cleaning_report.get("invalid_price_removed", 0)),
        ("Invalid registration year rows removed",   cleaning_report.get("invalid_year_removed", 0)),
        ("Invalid powerPS values nulled",            cleaning_report.get("invalid_power_nulled", 0)),
        ("Invalid month values nulled",              cleaning_report.get("invalid_month_nulled", 0)),
        ("Wanted ad listings removed",               cleaning_report.get("wanted_ads_removed", 0)),
        ("Commercial seller rows removed",           cleaning_report.get("commercial_sellers_removed", 0)),
        ("Columns dropped (nrOfPictures)",           len(cleaning_report.get("columns_dropped", []))),
        ("vehicleType nulls filled with unknown",    cleaning_report.get("filled_vehicleType", 0)),
        ("gearbox nulls filled with unknown",        cleaning_report.get("filled_gearbox", 0)),
        ("fuelType nulls filled with unknown",       cleaning_report.get("filled_fuelType", 0)),
        ("model nulls filled with unknown",          cleaning_report.get("filled_model", 0)),
        ("notRepairedDamage filled with unknown",    cleaning_report.get("filled_notRepairedDamage", 0)),
        ("Text columns standardized to lowercase",   len(cleaning_report.get("text_columns_standardized", []))),
    ]
 
    shade = False
    for action, count in actions:
        pdf.table_row([action, f"{count:,}"], widths, shade)
        shade = not shade
 
    pdf.ln(8)
 
    # Result box
    box_y = pdf.get_y()
    pdf.set_fill_color(240, 242, 255)
    pdf.set_draw_color(99, 102, 241)
    pdf.set_line_width(0.5)
    pdf.rect(10, box_y, 190, 28, "DF")
    pdf.set_xy(14, box_y + 4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 6, "Pipeline Result", ln=True)
    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 50, 70)
    pdf.multi_cell(
        182, 5.5,
        "The automated pipeline successfully processed " + str(f"{original:,}") + " raw records, "
        "detected " + str(f"{total_issues:,}") + " data quality issues, and delivered "
        + str(f"{clean_rows:,}") + " clean, analysis-ready records - retaining "
        + str(retained_pct) + "% of the original dataset with all critical quality issues resolved."
    )
    pdf.ln(10)
 
    # ── RECOMMENDATIONS ──────────────────────────────────
    pdf.section_title("Recommendations")
 
    recommendations = [
        ("Implement upstream validation",
         "Add price and year range constraints at the point of data entry to prevent "
         "corrupted records from entering the system in future."),
        ("Make damage status mandatory",
         "The notRepairedDamage field was missing for 19.4% of listings. "
         "This field directly impacts pricing and buyer decisions - it should be required."),
        ("Standardize registration date capture",
         "37,675 records had invalid month values (0 or >12). "
         "A dropdown selector at entry would eliminate this class of error entirely."),
        ("Schedule monthly pipeline runs",
         "This pipeline is fully reusable. Running it monthly on new data "
         "ensures quality issues are caught early rather than accumulating over time."),
    ]
 
    for i, (title, text) in enumerate(recommendations, 1):
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(99, 102, 241)
        pdf.cell(0, 6, str(i) + ". " + title, ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 100)
        pdf.multi_cell(0, 5.5, text)
        pdf.ln(3)
 
    # ── SAVE ─────────────────────────────────────────────
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print("  PDF report saved to: " + output_path)
 