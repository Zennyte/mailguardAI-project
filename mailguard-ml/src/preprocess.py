"""
preprocess.py

Loads the combined email dataset, splits it into train/test sets,
fits a TF-IDF vectorizer on the training text, and transforms both sets.

Run this before training any models.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_FILE = os.path.join("data", "processed", "email_dataset_combined.csv")
RESULTS_DIR = os.path.join("reports", "results")

TEST_SIZE = 0.2
RANDOM_STATE = 42

TFIDF_SETTINGS = {
    "max_features": 30000,
    "ngram_range": (1, 2),
    "min_df": 2,
    "max_df": 0.95,
}


def load_data():
    if not os.path.isfile(DATA_FILE):
        print(f"File not found: {DATA_FILE}")
        print("Run src/prepare_dataset.py first.")
        return None
    df = pd.read_csv(DATA_FILE)
    print(f"Loaded {len(df)} rows from {DATA_FILE}")
    return df


def split_data(df):
    X = df["text"].fillna("").astype(str)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    return X_train, X_test, y_train, y_test


def print_split_summary(X_train, X_test, y_train, y_test):
    print(f"\nTrain size: {len(X_train)}  Test size: {len(X_test)}")

    print("\nTrain label distribution:")
    train_counts = y_train.value_counts()
    train_pcts = y_train.value_counts(normalize=True) * 100
    for label in train_counts.index:
        print(f"  {label:<12} {train_counts[label]:>6}  ({train_pcts[label]:.1f}%)")

    print("\nTest label distribution:")
    test_counts = y_test.value_counts()
    test_pcts = y_test.value_counts(normalize=True) * 100
    for label in test_counts.index:
        print(f"  {label:<12} {test_counts[label]:>6}  ({test_pcts[label]:.1f}%)")


def fit_tfidf(X_train, X_test):
    print("\nFitting TF-IDF vectorizer on training data ...")
    vectorizer = TfidfVectorizer(**TFIDF_SETTINGS)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"TF-IDF train matrix shape: {X_train_tfidf.shape}")
    print(f"TF-IDF test  matrix shape: {X_test_tfidf.shape}")
    return vectorizer, X_train_tfidf, X_test_tfidf


def save_summary(X_train, X_test, y_train, y_test, X_train_tfidf, X_test_tfidf):
    train_counts = y_train.value_counts()
    train_pcts = y_train.value_counts(normalize=True) * 100
    test_counts = y_test.value_counts()
    test_pcts = y_test.value_counts(normalize=True) * 100

    lines = [
        "# Preprocessing Summary\n\n",
        "## Input Dataset\n\n",
        f"- Path: `{DATA_FILE}`\n",
        f"- Total rows: {len(X_train) + len(X_test)}\n\n",
        "## Train/Test Split\n\n",
        f"- Test size: {TEST_SIZE} (80% train / 20% test)\n",
        f"- Random state: {RANDOM_STATE}\n",
        f"- Stratified: yes\n\n",
        "## Split Shapes\n\n",
        f"- X_train: {X_train.shape[0]} rows\n",
        f"- X_test:  {X_test.shape[0]} rows\n\n",
        "## Train Label Distribution\n\n",
        "| Label | Count | % |\n",
        "|---|---|---|\n",
    ]
    for label in train_counts.index:
        lines.append(f"| {label} | {train_counts[label]} | {train_pcts[label]:.1f}% |\n")

    lines += [
        "\n## Test Label Distribution\n\n",
        "| Label | Count | % |\n",
        "|---|---|---|\n",
    ]
    for label in test_counts.index:
        lines.append(f"| {label} | {test_counts[label]} | {test_pcts[label]:.1f}% |\n")

    lines += [
        "\n## TF-IDF Settings\n\n",
        f"- max_features: {TFIDF_SETTINGS['max_features']}\n",
        f"- ngram_range: {TFIDF_SETTINGS['ngram_range']}\n",
        f"- min_df: {TFIDF_SETTINGS['min_df']}\n",
        f"- max_df: {TFIDF_SETTINGS['max_df']}\n\n",
        "## TF-IDF Matrix Shapes\n\n",
        f"- Train: {X_train_tfidf.shape[0]} rows x {X_train_tfidf.shape[1]} features\n",
        f"- Test:  {X_test_tfidf.shape[0]} rows x {X_test_tfidf.shape[1]} features\n",
    ]

    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, "preprocessing_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"\nSaved: {path}")


def main():
    print("=" * 60)
    print("Preprocessing")
    print("=" * 60)

    df = load_data()
    if df is None:
        return

    print("\n[Step 1] Train/test split")
    X_train, X_test, y_train, y_test = split_data(df)
    print_split_summary(X_train, X_test, y_train, y_test)

    print("\n[Step 2] TF-IDF vectorization")
    vectorizer, X_train_tfidf, X_test_tfidf = fit_tfidf(X_train, X_test)

    print("\n[Step 3] Saving summary")
    save_summary(X_train, X_test, y_train, y_test, X_train_tfidf, X_test_tfidf)

    print("\nDone.")


if __name__ == "__main__":
    main()
