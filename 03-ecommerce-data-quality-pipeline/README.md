# Data Quality Pipeline (E-commerce)

An automated, 4-phase data quality pipeline in Python. It profiles, validates and cleans a raw dataset, then writes a branded PDF audit report, all from a single command. Tested on 371,528 real used-car listings from eBay Kleinanzeigen.

**Sample report:** [`output/reports/data_quality_report.pdf`](output/reports/data_quality_report.pdf)

<!-- Tip: add a screenshot of page 1 of the PDF report here, e.g. ![Report preview](images/report_preview.png) -->

| Data health score | Raw records | Validation rules | Data retained |
|:---:|:---:|:---:|:---:|
| **22 → 91** (out of 100) | **371,528** | **14** | **92.6%** |

---

## Overview

Businesses collect messy data over time: duplicate records, impossible values, missing fields, inconsistent formatting. Before any analysis or dashboard can be trusted, that data has to be validated and cleaned.

This pipeline automates the whole process. It:

- **detects** what is wrong, and how severe it is
- **fixes** what can be fixed automatically
- **flags** what needs human review
- **delivers** a PDF report that documents every finding and every action taken

Built by [GrowInData](https://growindata.com) as part of my data portfolio.

## Results

Demo run on the eBay Kleinanzeigen Used Cars dataset:

| Metric | Value |
|---|---|
| Raw records processed | 371,528 |
| Validation rules run | 14 |
| Total issues detected | 291,570 |
| Rows removed | 27,577 (7.4%) |
| Clean records delivered | 343,951 |
| Data retained | 92.6% |
| Data health score (before) | 22 / 100 |
| Data health score (after) | 91 / 100 |

Issues found included prices up to EUR 2.1 billion, registration years between 1,000 and 9,999, engine power values of 20,000 PS, and 72,060 listings (about 19%) with no damage status.

> A single EUR 2.1 billion listing would, on its own, add roughly EUR 5,650 to the average price of all 371,528 listings. That is why the cleaning step matters before any analysis.

*Note: one row can break more than one rule, so "issues detected" is not the same as "rows affected".*

## Two versions, two audiences

| | Pipeline (`main.py`) | Notebook (`data_quality_analysis.ipynb`) |
|---|---|---|
| **Style** | Modular, production-style | Exploratory, narrative |
| **Output** | PDF report and clean CSV | Inline visualizations |
| **Best for** | Automation, client delivery | Analysis, communication |
| **Audience** | Engineers, technical clients | Data science recruiters |

## How it works

### Phase 1 | Load and profile
Loads the raw CSV with the correct encoding, counts rows and columns, identifies duplicates, computes missing-value rates per column, and calculates numeric ranges and categorical cardinality across the full dataset.

### Phase 2 | Validation rules engine
Runs 14 business-specific rules and classifies each issue as HIGH, MEDIUM or LOW severity. The rules cover price integrity, date validity, engine power ranges, missing critical fields, structural anomalies and listing type.

### Phase 3 | Automated cleaning
Applies 10 sequential cleaning steps: removing duplicates, dropping structurally invalid rows, setting out-of-range numeric values to missing, filling missing categoricals, standardizing text formatting, and dropping uninformative columns. Outputs a clean CSV ready for analysis or dashboard ingestion.

### Phase 4 | PDF report generator
Generates a branded 4-page PDF with an executive summary, the data health score before and after, full profiling tables, validation findings by severity, a cleaning action log, a result summary, and 4 business recommendations.

## Key validation rules

| Rule | Severity | Description |
|---|---|---|
| Duplicate rows | HIGH | Exact duplicate records |
| Invalid price | HIGH | Price outside EUR 100 to EUR 150,000 |
| Invalid year | HIGH | Registration year outside 1950 to 2016 |
| Invalid power | MEDIUM | Engine power outside 10 to 1,000 PS |
| Missing vehicle type | MEDIUM | Empty `vehicleType` field |
| Missing fuel type | MEDIUM | Empty `fuelType` field |
| Missing damage status | MEDIUM | Empty `notRepairedDamage` field |
| Wanted ads | MEDIUM | Listings seeking cars, not selling them |
| Invalid month | LOW | Month value outside 1 to 12 |
| Useless column | LOW | `nrOfPictures` is 0 for every row |

These are the main rules; the pipeline runs 14 in total. The valid ranges are business judgments for this dataset, not universal facts, so adjust them for your own data.

## What the notebook adds

The Jupyter notebook walks through the same four phases with charts and written explanations:

- **Missing value analysis:** bar chart by column with severity colors, plus a missingno matrix
- **Outlier detection:** histograms of price, year, power and kilometers with valid-range markers
- **Categorical distributions:** bar charts for every categorical column
- **Cleaning impact:** a step-by-step tracking table and before/after comparison charts
- **Summary and recommendations:** plain-language business findings

## Project structure

```
03-ecommerce-data-quality-pipeline/
├── data/
│   └── raw/                        <- Place raw CSV files here
├── output/
│   ├── clean/                      <- Cleaned dataset saved here
│   └── reports/                    <- PDF report saved here
├── src/
│   ├── loader.py                   <- Phase 1: load and profile
│   ├── validator.py                <- Phase 2: validation rules engine
│   ├── cleaner.py                  <- Phase 3: automated cleaning
│   └── reporter.py                 <- Phase 4: PDF report generator
├── data_quality_analysis.ipynb     <- Jupyter Notebook version
├── main.py                         <- Single entry point for the pipeline
├── requirements.txt
└── README.md
```

## Run it locally

Python 3.9 or higher is recommended.

```bash
# 1. Clone the repository and open this project's folder
git clone https://github.com/kovacikostanca/data-science-portfolio.git
cd data-science-portfolio/03-ecommerce-data-quality-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add the raw CSV to data/raw/, then run the pipeline
python main.py
```

The clean CSV is saved to `output/clean/` and the PDF report to `output/reports/`.

To explore the notebook version instead:

```bash
jupyter lab data_quality_analysis.ipynb
```

## Dataset

**eBay Kleinanzeigen Used Cars**, from Kaggle ([used-cars-database](https://www.kaggle.com/datasets/orgesleka/used-cars-database)).

- About 370,000 rows and 20 columns
- Real scraped data from German eBay classifieds
- Naturally messy: price overflows, impossible dates, missing fields, inconsistent formatting

## Tech stack

Python · Pandas · NumPy · fpdf2 · colorama · Matplotlib · Seaborn · missingno · JupyterLab

## Limitations and next steps

- The validation ranges are tuned to this dataset. Another dataset needs its own rules, and a rare but real listing (a classic car, for example) could be removed by mistake.
- The data health score is a custom measure for before/after comparison, not an industry standard.
- Next: move thresholds into a config file, add automated tests for each rule, and support scheduled runs.

## Author

**Kostanca Kovaci**: Data Analyst and Data Scientist · MSc Data Science (Distinction)
[LinkedIn](https://www.linkedin.com/in/kostanca-kovaci) · [GitHub](https://github.com/kovacikostanca) · [Portfolio case study](https://kostancakovaci.com)
