import pandas as pd
import numpy as np
import os

def load_data(filepath: str) -> pd.DataFrame:
    """Load the autos.csv file with correct encoding."""
    print(f" Loading data from: {filepath}")

    # Check if the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Load the CSV file with the correct encoding
    df = pd.read_csv(filepath, encoding="latin-1")
    print(f" Loaded {len(df):,} rows and {len(df.columns)} columns")
    return df

def profile_data(df: pd.DataFrame) -> dict:
    """Profile the dataset and return a summary dictionary.
    Covers: shape, dtypes, nulls, duplicates, and per-column stats."""
    print("\n Profiling dataset...")
    
    profile = {}

    # Basic shape
    profile["total_rows"] = len(df)
    profile["total_columns"] = len(df.columns)

    # Duplicate rows
    duplicate_count = df.duplicated().sum()
    profile["duplicate_rows"] = int(duplicate_count)

    # Missing values per column
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df) * 100).round(2)

    profile["missing_values"] = {
        col: {
            "count": int(null_counts[col]),
            "percentage": float(null_pct[col])
        }
        for col in df.columns
    }

    # Column data types
    profile["dtypes"] = {col: str(dtype) for col, dtype in df.dtypes.items()}

    # Per-column stats for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    profile["numeric_stats"] = {}
    for col in numeric_cols:
        profile["numeric_stats"][col] = {
            "min": float(df[col].min()) if not df[col].isnull().all() else None,
            "max": float(df[col].max()) if not df[col].isnull().all() else None,
            "mean": float(df[col].mean()) if not df[col].isnull().all() else None,
            "nulls": int(df[col].isnull().sum())
        }

    # Per-column stats for categorical columns
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    profile["categorical_stats"] = {}
    for col in cat_cols:
        profile["categorical_stats"][col] = {
            "unique_values": int(df[col].nunique()),
            "top_value": str(df[col].mode()[0]) if not df[col].isnull().all() else None,
            "nulls": int(df[col].isnull().sum())
        }
    print(f" Profile complete")
    return profile

def print_profile_summary(profile: dict):
    """Print a readable summary of the profile to the terminal."""
    print("\n" + "="*55)
    print(" DATA PROFILE SUMMARY ")
    print("="*55)
    print(f" Total rows       : {profile['total_rows']:,}")
    print(f" Total columns    : {profile['total_columns']}")
    print(f" Duplicate rows   : {profile['duplicate_rows']:,}")

    print("\n MISSING VALUES PER COLUMN ")
    print(f"  {'Column':<30} {'Missing':>8} {'%':>8}")
    print(f"  {'-'*46}")
    for col, stats in profile["missing_values"].items():
        if stats["count"] > 0:
            print(f"  {col:<30} {stats['count']:>8,} {stats['percentage']:>7.1f}%")

    print("\n NUMERIC COLUMN RANGES ")
    print(f"  {'Column':<25} {'Min':>12} {'Max':>12} {'Mean':>12}")
    print(f"  {'-'*61}")
    for col, stats in profile["numeric_stats"].items():
        if stats["min"] is not None:
            print(f"  {col:<25} {stats['min']:>12,.1f} {stats['max']:>12,.1f} {stats['mean']:>12,.1f}")
 
    print("\n  CATEGORICAL COLUMNS — UNIQUE VALUE COUNTS:")
    print(f"  {'Column':<30} {'Unique':>8}")
    print(f"  {'-'*38}")
    for col, stats in profile["categorical_stats"].items():
        print(f"  {col:<30} {stats['unique_values']:>8,}")
 
    print("="*55)