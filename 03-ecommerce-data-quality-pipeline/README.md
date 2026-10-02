# Data Quality Pipeline

An automated 4-phase data quality pipeline built in Python that profiles, validates, cleans, and reports on raw datasets, delivering analysis-ready data and a branded PDF audit report in a single command.

Two versions are included: a **production-style modular pipeline** and an **exploratory Jupyter Notebook** with full visualizations.

Built by [GrowInData](https://growindata.com) as part of a freelance data consultancy portfolio.

---

## The Problem This Solves

Businesses accumulate messy data over time - duplicate records, impossible values, missing fields, inconsistent formatting. Before any analysis or dashboard can be trusted, that data needs to be validated and cleaned.

This pipeline automates the entire process:
- Detects what is wrong and how severe it is
- Fixes what can be fixed automatically
- Flags what needs human review
- Delivers a professional PDF report documenting every finding and action taken

---

## Demo Results (eBay Kleinanzeigen Used Cars Dataset)

| Metric | Value |
|---|---|
| Raw records processed | 371,528 |
| Validation rules run | 14 |
| Total issues detected | 291,570 |
| Rows removed | 27,577 |
| Clean records delivered | 343,951 |
| Data retained | 92.6% |
| Data health score (before) | 22/100 |
| Data health score (after) | 91/100 |

Issues found included prices up to EUR 2.1 billion, registration years between 1,000 and 9,999, engine power values of 20,000 PS, and 72,060 listings missing damage status information.

---

## Two Versions - Two Audiences

| | Pipeline (`main.py`) | Notebook (`data_quality_analysis.ipynb`) |
|---|---|---|
| Style | Modular, production-ready | Exploratory, narrative |
| Output | PDF report + clean CSV | Inline visualizations |
| Best for | Automation, client delivery | Analysis, communication |
| Audience | Engineers, technical clients | Data science recruiters |

---

## Pipeline Architecture

```
data-quality-pipeline/
├── data/
│   └── raw/                        <- Place raw CSV files here
├── output/
│   ├── clean/                      <- Cleaned dataset saved here
│   └── reports/                    <- PDF report saved here
├── src/
│   ├── loader.py                   <- Phase 1: Load and profile
│   ├── validator.py                <- Phase 2: Validation rules engine
│   ├── cleaner.py                  <- Phase 3: Automated cleaning
│   └── reporter.py                 <- Phase 4: PDF report generator
├── data_quality_analysis.ipynb     <- Jupyter Notebook version
├── main.py                         <- Single entry point for pipeline
├── requirements.txt
└── README.md
```

### Phase 1 | Load and Profile
Loads the raw CSV with correct encoding, counts rows and columns, identifies duplicates, computes missing value rates per column, and calculates numeric ranges and categorical cardinality across the full dataset.

### Phase 2 | Validation Rules Engine
Runs 14 business-specific validation rules across the dataset, classifying each issue as HIGH, MEDIUM, or LOW severity. Rules cover price integrity, date validity, engine power ranges, missing critical fields, structural anomalies, and listing type classification.

### Phase 3 | Automated Cleaning
Applies 10 sequential cleaning steps: removing duplicates, dropping structurally invalid rows, nulling out-of-range numeric values, filling missing categoricals, standardizing text formatting, and dropping uninformative columns. Outputs a clean CSV ready for analysis or dashboard ingestion.

### Phase 4 | PDF Report Generator
Auto-generates a branded 4-page PDF report including an executive summary with key metrics, a data health score (before and after), full profiling tables, validation findings by severity, cleaning action log, pipeline result summary, and 4 business recommendations.

---

## Jupyter Notebook | What's Inside

The notebook walks through the same 4 phases with full visualizations and markdown explanations:

- **Missing value analysis** : bar chart by column with severity colour coding + missingno matrix
- **Outlier detection** : histograms of price, year, power, and kilometer with valid range markers
- **Categorical distributions** : bar charts for all categorical columns
- **Cleaning impact** : step-by-step tracking table and before/after comparison charts
- **Summary and recommendations** : plain-language business findings

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/kovacikostanca/data-quality-pipeline.git
cd data-quality-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Requirements

```
pandas
numpy
fpdf2
colorama
matplotlib
seaborn
missingno
jupyterlab
```

Install with:

```bash
pip install pandas numpy fpdf2 colorama matplotlib seaborn missingno jupyterlab
```

Python 3.9 or higher recommended.

---

## Dataset Used

**eBay Kleinanzeigen Used Cars**
- Source: Kaggle - [used-cars-database](https://www.kaggle.com/datasets/orgesleka/used-cars-database)
- Size: ~370,000 rows, 20 columns
- Real scraped data from German eBay classifieds
- Naturally messy: price overflows, impossible dates, missing fields, inconsistent formatting

---

## Key Validation Rules

| Rule | Severity | Description |
|---|---|---|
| Duplicate rows | HIGH | Exact duplicate records |
| Invalid price | HIGH | Price outside EUR 100 to EUR 150,000 |
| Invalid year | HIGH | Registration year outside 1950 to 2016 |
| Invalid power | MEDIUM | Engine power outside 10 to 1,000 PS |
| Missing vehicle type | MEDIUM | Null vehicleType field |
| Missing fuel type | MEDIUM | Null fuelType field |
| Missing damage status | MEDIUM | Null notRepairedDamage field |
| Wanted ads | MEDIUM | Listings seeking cars, not selling them |
| Invalid month | LOW | Month value outside 1 to 12 |
| Useless column | LOW | nrOfPictures is 0 for all rows |

---
