"""
inspect_datasets.py

A simple inspection script for the raw email datasets.

It looks inside the data/raw/ folder, finds all CSV files, and prints a short
summary for each one (shape, columns, a few sample rows, and label counts).

This script ONLY reads and prints information. It does not modify, clean, or
save any dataset files.
"""

import os
import pandas as pd

# Folder where the raw datasets should be placed.
RAW_DATA_DIR = os.path.join("data", "raw")

# Encodings to try when reading a CSV file (in order).
ENCODINGS_TO_TRY = ["utf-8", "latin-1", "cp1252"]

# Column names that might contain the label (safe / spam / phishing, etc.).
LIKELY_LABEL_COLUMNS = [
    "label",
    "Label",
    "class",
    "Class",
    "category",
    "Category",
    "target",
    "Target",
    "Spam/Ham",
    "spam",
    "phishing",
]

# How many characters to show before truncating long text values.
MAX_TEXT_LENGTH = 80


def find_csv_files(folder):
    """Return a sorted list of .csv file names inside the given folder."""
    if not os.path.isdir(folder):
        return []
    files = [name for name in os.listdir(folder) if name.lower().endswith(".csv")]
    return sorted(files)


def read_csv_with_fallback(file_path):
    """
    Try to read a CSV file using several encodings.

    Returns the DataFrame on success, or None if all encodings fail.
    """
    for encoding in ENCODINGS_TO_TRY:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except Exception:
            # Try the next encoding.
            continue
    return None


def shorten(value):
    """Shorten long text values so the sample rows stay readable."""
    text = str(value)
    if len(text) > MAX_TEXT_LENGTH:
        return text[:MAX_TEXT_LENGTH] + "..."
    return text


def print_sample_rows(df, row_count=3):
    """Print the first few rows with long text values truncated."""
    sample = df.head(row_count).copy()
    for column in sample.columns:
        sample[column] = sample[column].apply(shorten)
    print(sample.to_string(index=False))


def print_label_counts(df):
    """Print value counts for any likely label columns that exist."""
    found_any = False
    for column in LIKELY_LABEL_COLUMNS:
        if column in df.columns:
            found_any = True
            print(f"\nValue counts for likely label column '{column}':")
            print(df[column].value_counts())
    if not found_any:
        print("\nNo likely label columns found in this file.")


def inspect_file(file_name):
    """Print an inspection summary for a single CSV file."""
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    print("\n" + "=" * 70)
    print(f"File: {file_name}")
    print("=" * 70)

    df = read_csv_with_fallback(file_path)
    if df is None:
        print("Could not read this file with any of the tried encodings.")
        print("Skipping to the next file.")
        return

    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")

    print("\nFirst 3 rows:")
    print_sample_rows(df, row_count=3)

    print_label_counts(df)


def main():
    """Find and inspect all CSV files in the raw data folder."""
    csv_files = find_csv_files(RAW_DATA_DIR)

    if not csv_files:
        print(f"No CSV files found in '{RAW_DATA_DIR}'.")
        print("Please place the raw dataset CSV files there and run again.")
        return

    print(f"Found {len(csv_files)} CSV file(s) in '{RAW_DATA_DIR}'.")
    for file_name in csv_files:
        inspect_file(file_name)


if __name__ == "__main__":
    main()
