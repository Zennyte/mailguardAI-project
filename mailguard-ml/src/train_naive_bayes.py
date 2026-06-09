"""
train_naive_bayes.py

Trains a Multinomial Naive Bayes classifier on the combined email dataset.
Tests multiple alpha values and picks the best one by macro F1-score.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    ConfusionMatrixDisplay,
    confusion_matrix,
)

DATA_FILE = os.path.join("data", "processed", "email_dataset_combined.csv")
FIGURES_DIR = os.path.join("reports", "figures")
RESULTS_DIR = os.path.join("reports", "results")

TEST_SIZE = 0.2
RANDOM_STATE = 42
ALPHA_VALUES = [0.1, 0.5, 1.0]
LABELS = ["safe", "spam", "phishing"]

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_and_split():
    df = pd.read_csv(DATA_FILE)
    X = df["text"].fillna("").astype(str)
    y = df["label"]
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)


def build_tfidf(X_train, X_test):
    vectorizer = TfidfVectorizer(max_features=30000, ngram_range=(1, 2), min_df=2, max_df=0.95)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    return X_train_tfidf, X_test_tfidf


def evaluate(model, X_test_tfidf, y_test):
    y_pred = model.predict(X_test_tfidf)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="macro", zero_division=0),
        "f1": f1_score(y_test, y_pred, average="macro", zero_division=0),
        "y_pred": y_pred,
    }


def save_confusion_matrix(y_test, y_pred, alpha):
    cm = confusion_matrix(y_test, y_pred, labels=LABELS)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=LABELS)

    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(ax=ax, colorbar=False)
    ax.set_title(f"Naive Bayes — Confusion Matrix (alpha={alpha})")
    plt.tight_layout()

    path = os.path.join(FIGURES_DIR, "naive_bayes_confusion_matrix.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def save_results_csv(results):
    rows = []
    for alpha, metrics in results.items():
        rows.append({
            "alpha": alpha,
            "accuracy": round(metrics["accuracy"], 4),
            "precision_macro": round(metrics["precision"], 4),
            "recall_macro": round(metrics["recall"], 4),
            "f1_macro": round(metrics["f1"], 4),
        })
    path = os.path.join(RESULTS_DIR, "naive_bayes_results.csv")
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Saved: {path}")


def save_summary(results, best_alpha):
    best = results[best_alpha]
    lines = [
        "# Naive Bayes Results\n\n",
        "## Alpha Comparison\n\n",
        "| Alpha | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |\n",
        "|---|---|---|---|---|\n",
    ]
    for alpha, m in results.items():
        marker = " **(best)**" if alpha == best_alpha else ""
        lines.append(
            f"| {alpha}{marker} | {m['accuracy']:.4f} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1']:.4f} |\n"
        )
    lines += [
        f"\n## Best Alpha: {best_alpha}\n\n",
        f"- Accuracy:           {best['accuracy']:.4f}\n",
        f"- Precision (macro):  {best['precision']:.4f}\n",
        f"- Recall (macro):     {best['recall']:.4f}\n",
        f"- F1 (macro):         {best['f1']:.4f}\n\n",
        "## Notes\n\n",
        "- Macro averages are used because the phishing class is underrepresented.\n",
        "- Confusion matrix saved to `reports/figures/naive_bayes_confusion_matrix.png`.\n",
    ]
    path = os.path.join(RESULTS_DIR, "naive_bayes_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Saved: {path}")


def main():
    print("=" * 60)
    print("Naive Bayes Training")
    print("=" * 60)

    print("\nLoading and splitting data ...")
    X_train, X_test, y_train, y_test = load_and_split()
    print(f"Train: {len(X_train)}  Test: {len(X_test)}")

    print("\nFitting TF-IDF ...")
    X_train_tfidf, X_test_tfidf = build_tfidf(X_train, X_test)

    print("\nTraining Naive Bayes with different alpha values:\n")
    results = {}
    for alpha in ALPHA_VALUES:
        model = MultinomialNB(alpha=alpha)
        model.fit(X_train_tfidf, y_train)
        metrics = evaluate(model, X_test_tfidf, y_test)
        results[alpha] = metrics
        print(f"  alpha={alpha}  acc={metrics['accuracy']:.4f}  "
              f"prec={metrics['precision']:.4f}  rec={metrics['recall']:.4f}  "
              f"f1={metrics['f1']:.4f}")

    best_alpha = max(results, key=lambda a: results[a]["f1"])
    print(f"\nBest alpha by macro F1: {best_alpha}")

    best_model = MultinomialNB(alpha=best_alpha)
    best_model.fit(X_train_tfidf, y_train)
    best_metrics = evaluate(best_model, X_test_tfidf, y_test)

    print("\nClassification report (best model):\n")
    print(classification_report(y_test, best_metrics["y_pred"], target_names=LABELS))

    save_confusion_matrix(y_test, best_metrics["y_pred"], best_alpha)
    save_results_csv(results)
    save_summary(results, best_alpha)

    print("\nDone.")


if __name__ == "__main__":
    main()
