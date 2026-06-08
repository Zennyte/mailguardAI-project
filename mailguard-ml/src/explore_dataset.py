"""
explore_dataset.py

Exploratory data analysis for the combined email dataset.
Reads data/processed/email_dataset_combined.csv and prints stats,
saves charts to reports/figures/, and saves a summary to reports/results/.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = os.path.join("data", "processed", "email_dataset_combined.csv")
FIGURES_DIR = os.path.join("reports", "figures")
RESULTS_DIR = os.path.join("reports", "results")

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_data():
    if not os.path.isfile(DATA_FILE):
        print(f"File not found: {DATA_FILE}")
        print("Run src/prepare_dataset.py first.")
        return None
    df = pd.read_csv(DATA_FILE)
    df["subject_length"] = df["subject"].fillna("").astype(str).str.len()
    df["body_length"] = df["body"].fillna("").astype(str).str.len()
    df["text_length"] = df["text"].fillna("").astype(str).str.len()
    return df


def print_overview(df):
    print("=" * 60)
    print("Dataset overview")
    print("=" * 60)
    print(f"\nShape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")

    print("\nMissing values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("  None")
    else:
        print(missing[missing > 0].to_string())

    print("\nLabel distribution:")
    counts = df["label"].value_counts()
    pcts = df["label"].value_counts(normalize=True) * 100
    for label in counts.index:
        print(f"  {label:<12} {counts[label]:>6}  ({pcts[label]:.1f}%)")

    print("\nSource distribution:")
    source_counts = df["source_dataset"].value_counts().dropna()
    if source_counts.empty:
        print("  (source_dataset column is empty)")
    else:
        for source, count in source_counts.items():
            print(f"  {source:<22} {count:>6}")

    print("\nText length statistics (characters):")
    for col in ["subject_length", "body_length", "text_length"]:
        stats = df[col].describe()
        print(f"  {col}:")
        print(f"    mean={stats['mean']:.0f}  min={stats['min']:.0f}  "
              f"max={stats['max']:.0f}  median={df[col].median():.0f}")


def plot_label_distribution(df):
    counts = df["label"].value_counts()
    colors = ["#4caf50", "#f44336", "#ff9800"]

    fig, ax = plt.subplots(figsize=(6, 4))
    counts.plot(kind="bar", ax=ax, color=colors, edgecolor="black")
    ax.set_title("Label Distribution")
    ax.set_xlabel("Label")
    ax.set_ylabel("Count")
    ax.set_xticklabels(counts.index, rotation=0)

    for i, count in enumerate(counts):
        ax.text(i, count + 200, str(count), ha="center", fontsize=9)

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "label_distribution.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def plot_source_distribution(df):
    counts = df["source_dataset"].value_counts().dropna()
    if counts.empty:
        print("  [SKIP] source_dataset column is empty — skipping source chart.")
        return

    fig, ax = plt.subplots(figsize=(8, 4))
    counts.plot(kind="bar", ax=ax, color="#2196f3", edgecolor="black")
    ax.set_title("Source Dataset Distribution")
    ax.set_xlabel("Source")
    ax.set_ylabel("Count")
    ax.set_xticklabels(counts.index, rotation=20, ha="right")

    for i, count in enumerate(counts):
        ax.text(i, count + 200, str(count), ha="center", fontsize=8)

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "source_distribution.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def plot_text_length_histogram(df):
    clipped = df["text_length"].clip(upper=5000)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(clipped, bins=60, color="#9c27b0", edgecolor="black", alpha=0.8)
    ax.set_title("Text Length Distribution (clipped at 5000 chars)")
    ax.set_xlabel("Text length (characters)")
    ax.set_ylabel("Count")

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "text_length_distribution.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def save_eda_summary(df):
    counts = df["label"].value_counts()
    pcts = df["label"].value_counts(normalize=True) * 100
    source_counts = df["source_dataset"].value_counts()

    lines = [
        "# EDA Summary\n",
        f"Dataset: `{DATA_FILE}`\n",
        f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n",
        "\n## Label Distribution\n",
        "| Label | Count | % |\n",
        "|---|---|---|\n",
    ]
    for label in counts.index:
        lines.append(f"| {label} | {counts[label]} | {pcts[label]:.1f}% |\n")

    lines += [
        "\n## Source Distribution\n",
        "| Source | Count |\n",
        "|---|---|\n",
    ]
    for source, count in source_counts.items():
        lines.append(f"| {source} | {count} |\n")

    lines += [
        "\n## Text Length Statistics\n",
        "| Column | Mean | Min | Max | Median |\n",
        "|---|---|---|---|---|\n",
    ]
    for col in ["subject_length", "body_length", "text_length"]:
        s = df[col].describe()
        lines.append(
            f"| {col} | {s['mean']:.0f} | {s['min']:.0f} | {s['max']:.0f} | {df[col].median():.0f} |\n"
        )

    lines += [
        "\n## Notes\n",
        "- Phishing is the smallest class (~7%). Use `class_weight='balanced'` in all classifiers.\n",
        "- Some emails have very long bodies. TF-IDF with a token limit handles this naturally.\n",
        "- Text length is clipped at 5000 characters in the histogram for readability.\n",
    ]

    path = os.path.join(RESULTS_DIR, "eda_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Saved: {path}")


def main():
    df = load_data()
    if df is None:
        return

    print_overview(df)

    print("\n[Plots]")
    plot_label_distribution(df)
    plot_source_distribution(df)
    plot_text_length_histogram(df)

    print("\n[Summary]")
    save_eda_summary(df)

    print("\nDone.")


if __name__ == "__main__":
    main()
