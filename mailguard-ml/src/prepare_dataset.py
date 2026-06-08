"""
prepare_dataset.py

Loads each raw email dataset from data/raw/, normalizes them into a unified
schema, applies label mappings, cleans text, removes empty and duplicate rows,
and saves the final combined dataset to data/processed/email_dataset_combined.csv.

Column mapping reference: reports/results/dataset_column_mapping.md

Output columns: source_dataset, subject, body, text, label
Final labels:   safe, spam, phishing
"""

import os
import re
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "email_dataset_combined.csv")

ENCODINGS_TO_TRY = ["utf-8", "latin-1", "cp1252"]


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def read_csv(filename):
    """Read a CSV from data/raw/ trying multiple encodings. Returns DataFrame or None."""
    path = os.path.join(RAW_DIR, filename)
    if not os.path.isfile(path):
        print(f"  [SKIP] File not found: {path}")
        return None
    for encoding in ENCODINGS_TO_TRY:
        try:
            return pd.read_csv(path, encoding=encoding)
        except Exception:
            continue
    print(f"  [SKIP] Could not read {filename} with any known encoding.")
    return None


def require_columns(df, filename, columns):
    """Return True if all required columns exist in df, else print a warning."""
    missing = [c for c in columns if c not in df.columns]
    if missing:
        print(f"  [SKIP] {filename} is missing required columns: {missing}")
        return False
    return True


def clean_text(value):
    """Lightly clean a text value: strip whitespace and collapse internal spaces."""
    text = str(value)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def fill_na(series):
    """Replace NaN with empty string and return a string series."""
    return series.fillna("").astype(str)


# ---------------------------------------------------------------------------
# Per-dataset loaders
# ---------------------------------------------------------------------------

def load_ceas(filename="CEAS_08.csv"):
    """
    CEAS_08: subject + body, label 0→safe / 1→spam
    """
    print(f"Loading {filename} ...")
    df = read_csv(filename)
    if df is None:
        return None
    if not require_columns(df, filename, ["subject", "body", "label"]):
        return None

    result = pd.DataFrame()
    result["source_dataset"] = "CEAS_08"
    result["subject"] = fill_na(df["subject"])
    result["body"] = fill_na(df["body"])
    result["label"] = df["label"].map({0: "safe", 1: "spam"})

    unmapped = result["label"].isna().sum()
    if unmapped:
        print(f"  [WARN] {unmapped} rows had unrecognized label values and will be dropped.")
    result = result.dropna(subset=["label"])

    print(f"  Loaded {len(result)} rows.")
    return result


def load_enron(filename="enron_spam_data.csv"):
    """
    Enron: Subject→subject, Message→body, Spam/Ham ham→safe / spam→spam
    """
    print(f"Loading {filename} ...")
    df = read_csv(filename)
    if df is None:
        return None
    if not require_columns(df, filename, ["Subject", "Message", "Spam/Ham"]):
        return None

    result = pd.DataFrame()
    result["source_dataset"] = "enron_spam_data"
    result["subject"] = fill_na(df["Subject"])
    result["body"] = fill_na(df["Message"])
    result["label"] = df["Spam/Ham"].map({"ham": "safe", "spam": "spam"})

    unmapped = result["label"].isna().sum()
    if unmapped:
        print(f"  [WARN] {unmapped} rows had unrecognized label values and will be dropped.")
    result = result.dropna(subset=["label"])

    print(f"  Loaded {len(result)} rows.")
    return result


def load_messages(filename="messages.csv"):
    """
    messages (Ling-Spam): subject + message→body, label 0→safe / 1→spam
    """
    print(f"Loading {filename} ...")
    df = read_csv(filename)
    if df is None:
        return None
    if not require_columns(df, filename, ["subject", "message", "label"]):
        return None

    result = pd.DataFrame()
    result["source_dataset"] = "messages"
    result["subject"] = fill_na(df["subject"])
    result["body"] = fill_na(df["message"])
    result["label"] = df["label"].map({0: "safe", 1: "spam"})

    unmapped = result["label"].isna().sum()
    if unmapped:
        print(f"  [WARN] {unmapped} rows had unrecognized label values and will be dropped.")
    result = result.dropna(subset=["label"])

    print(f"  Loaded {len(result)} rows.")
    return result


def load_spamassassin(filename="SpamAssasin.csv"):
    """
    SpamAssassin: subject + body, label 0→safe / 1→spam
    """
    print(f"Loading {filename} ...")
    df = read_csv(filename)
    if df is None:
        return None
    if not require_columns(df, filename, ["subject", "body", "label"]):
        return None

    result = pd.DataFrame()
    result["source_dataset"] = "SpamAssasin"
    result["subject"] = fill_na(df["subject"])
    result["body"] = fill_na(df["body"])
    result["label"] = df["label"].map({0: "safe", 1: "spam"})

    unmapped = result["label"].isna().sum()
    if unmapped:
        print(f"  [WARN] {unmapped} rows had unrecognized label values and will be dropped.")
    result = result.dropna(subset=["label"])

    print(f"  Loaded {len(result)} rows.")
    return result


def load_nazario(filename="Nazario.csv"):
    """
    Nazario: subject + body, all rows → phishing (label column ignored).
    """
    print(f"Loading {filename} ...")
    df = read_csv(filename)
    if df is None:
        return None
    if not require_columns(df, filename, ["subject", "body"]):
        return None

    result = pd.DataFrame()
    result["source_dataset"] = "Nazario"
    result["subject"] = fill_na(df["subject"])
    result["body"] = fill_na(df["body"])
    result["label"] = "phishing"

    print(f"  Loaded {len(result)} rows.")
    return result


def load_nigerian_fraud(filename="Nigerian_Fraud.csv"):
    """
    Nigerian_Fraud: subject + body, all rows → phishing (label column ignored).
    """
    print(f"Loading {filename} ...")
    df = read_csv(filename)
    if df is None:
        return None
    if not require_columns(df, filename, ["subject", "body"]):
        return None

    result = pd.DataFrame()
    result["source_dataset"] = "Nigerian_Fraud"
    result["subject"] = fill_na(df["subject"])
    result["body"] = fill_na(df["body"])
    result["label"] = "phishing"

    print(f"  Loaded {len(result)} rows.")
    return result


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Dataset preparation starting")
    print("=" * 60)

    # --- Step 1: Load all datasets ---
    print("\n[Step 1] Loading raw datasets\n")

    frames = [
        load_ceas(),
        load_enron(),
        load_messages(),
        load_spamassassin(),
        load_nazario(),
        load_nigerian_fraud(),
    ]

    frames = [f for f in frames if f is not None]
    if not frames:
        print("\nNo datasets loaded. Make sure CSV files are in data/raw/.")
        return

    # --- Step 2: Combine ---
    print("\n[Step 2] Combining datasets")
    combined = pd.concat(frames, ignore_index=True)
    print(f"  Combined shape: {combined.shape}")

    # --- Step 3: Build text column ---
    print("\n[Step 3] Building text column (subject + body)")
    combined["subject"] = combined["subject"].apply(clean_text)
    combined["body"] = combined["body"].apply(clean_text)
    combined["text"] = combined["subject"] + " " + combined["body"]
    combined["text"] = combined["text"].apply(clean_text)

    # --- Step 4: Remove empty text rows ---
    print("\n[Step 4] Removing rows with empty text")
    before = len(combined)
    combined = combined[combined["text"].str.strip() != ""]
    removed = before - len(combined)
    print(f"  Removed {removed} empty-text rows. Remaining: {len(combined)}")

    # --- Step 5: Remove duplicate texts ---
    print("\n[Step 5] Removing duplicate email texts")
    before = len(combined)
    combined = combined.drop_duplicates(subset=["text"])
    removed = before - len(combined)
    print(f"  Removed {removed} duplicate rows. Remaining: {len(combined)}")

    # --- Step 6: Keep only valid labels ---
    print("\n[Step 6] Keeping only valid labels: safe, spam, phishing")
    valid_labels = {"safe", "spam", "phishing"}
    before = len(combined)
    combined = combined[combined["label"].isin(valid_labels)]
    removed = before - len(combined)
    if removed:
        print(f"  Removed {removed} rows with unrecognized labels.")
    print(f"  Remaining: {len(combined)}")

    # --- Step 7: Reorder columns and save ---
    print("\n[Step 7] Saving to", OUTPUT_FILE)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    combined = combined[["source_dataset", "subject", "body", "text", "label"]]
    combined.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print("  Saved.")

    # --- Step 8: Summary ---
    print("\n" + "=" * 60)
    print("Final dataset summary")
    print("=" * 60)
    print(f"\nShape: {combined.shape[0]} rows, {combined.shape[1]} columns")

    print("\nLabel distribution:")
    label_counts = combined["label"].value_counts()
    label_pct = combined["label"].value_counts(normalize=True) * 100
    for label in label_counts.index:
        print(f"  {label:<10} {label_counts[label]:>6}  ({label_pct[label]:.1f}%)")

    print("\nSource distribution:")
    for source, count in combined["source_dataset"].value_counts().items():
        print(f"  {source:<20} {count:>6}")

    print("\nDone. Output saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
