"""
train_random_forest.py

Trains a Random Forest classifier on the combined email dataset.
Uses TF-IDF + TruncatedSVD to reduce dimensionality before training.
Tests combinations of n_estimators and max_depth, picks best by macro F1.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
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
LABELS = ["safe", "spam", "phishing"]

# Hyperparameter combinations to try
PARAM_GRID = [
    {"n_estimators": 100, "max_depth": 30},
    {"n_estimators": 100, "max_depth": None},
    {"n_estimators": 200, "max_depth": 30},
    {"n_estimators": 200, "max_depth": None},
]

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_and_split():
    df = pd.read_csv(DATA_FILE)
    X = df["text"].fillna("").astype(str)
    y = df["label"]
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)


def build_tfidf_svd(X_train, X_test):
    print("Fitting TF-IDF ...")
    vectorizer = TfidfVectorizer(max_features=30000, ngram_range=(1, 2), min_df=2, max_df=0.95)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Applying TruncatedSVD (n_components=300) ...")
    svd = TruncatedSVD(n_components=300, random_state=RANDOM_STATE)
    X_train_svd = svd.fit_transform(X_train_tfidf)
    X_test_svd = svd.transform(X_test_tfidf)

    explained = svd.explained_variance_ratio_.sum()
    print(f"SVD explained variance: {explained:.2%}")

    return X_train_svd, X_test_svd


def evaluate(model, X_test_svd, y_test):
    y_pred = model.predict(X_test_svd)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="macro", zero_division=0),
        "f1": f1_score(y_test, y_pred, average="macro", zero_division=0),
        "y_pred": y_pred,
    }


def param_label(params):
    depth = params["max_depth"] if params["max_depth"] is not None else "None"
    return f"n_estimators={params['n_estimators']}  max_depth={depth}"


def save_confusion_matrix(y_test, y_pred, best_params):
    cm = confusion_matrix(y_test, y_pred, labels=LABELS)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=LABELS)

    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(ax=ax, colorbar=False)
    depth = best_params["max_depth"] if best_params["max_depth"] is not None else "None"
    ax.set_title(
        f"Random Forest — Confusion Matrix\n"
        f"n_estimators={best_params['n_estimators']}  max_depth={depth}"
    )
    plt.tight_layout()

    path = os.path.join(FIGURES_DIR, "random_forest_confusion_matrix.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def save_results_csv(results):
    rows = []
    for params, metrics in results:
        rows.append({
            "n_estimators": params["n_estimators"],
            "max_depth": str(params["max_depth"]),
            "accuracy": round(metrics["accuracy"], 4),
            "precision_macro": round(metrics["precision"], 4),
            "recall_macro": round(metrics["recall"], 4),
            "f1_macro": round(metrics["f1"], 4),
        })
    path = os.path.join(RESULTS_DIR, "random_forest_results.csv")
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Saved: {path}")


def save_summary(results, best_params, best_metrics):
    depth_str = str(best_params["max_depth"]) if best_params["max_depth"] is not None else "None"
    lines = [
        "# Random Forest Results\n\n",
        "## Hyperparameter Comparison\n\n",
        "| n_estimators | max_depth | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |\n",
        "|---|---|---|---|---|---|\n",
    ]
    for params, m in results:
        d = str(params["max_depth"]) if params["max_depth"] is not None else "None"
        is_best = (params == best_params)
        marker = " **(best)**" if is_best else ""
        lines.append(
            f"| {params['n_estimators']}{marker} | {d} | {m['accuracy']:.4f} | "
            f"{m['precision']:.4f} | {m['recall']:.4f} | {m['f1']:.4f} |\n"
        )
    lines += [
        f"\n## Best Settings\n\n",
        f"- n_estimators: {best_params['n_estimators']}\n",
        f"- max_depth:     {depth_str}\n",
        f"- class_weight:  balanced\n\n",
        "## Best Metrics\n\n",
        f"- Accuracy:           {best_metrics['accuracy']:.4f}\n",
        f"- Precision (macro):  {best_metrics['precision']:.4f}\n",
        f"- Recall (macro):     {best_metrics['recall']:.4f}\n",
        f"- F1 (macro):         {best_metrics['f1']:.4f}\n\n",
        "## Pipeline\n\n",
        "TF-IDF (max_features=30000, ngram_range=(1,2)) -> TruncatedSVD (n_components=300) -> RandomForest\n\n",
        "## Notes\n\n",
        "- TruncatedSVD reduces TF-IDF features from 30000 to 300 before Random Forest.\n",
        "- Macro averages are used because the phishing class is underrepresented.\n",
        "- Random Forest is slower to train than linear models on this dataset size.\n",
        "- Confusion matrix saved to `reports/figures/random_forest_confusion_matrix.png`.\n",
    ]
    path = os.path.join(RESULTS_DIR, "random_forest_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Saved: {path}")


def main():
    print("=" * 60)
    print("Random Forest Training")
    print("=" * 60)

    print("\nLoading and splitting data ...")
    X_train, X_test, y_train, y_test = load_and_split()
    print(f"Train: {len(X_train)}  Test: {len(X_test)}")

    print()
    X_train_svd, X_test_svd = build_tfidf_svd(X_train, X_test)

    print("\nTraining Random Forest with different settings:\n")
    results = []
    for params in PARAM_GRID:
        label = param_label(params)
        print(f"  Training {label} ...")
        model = RandomForestClassifier(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
        model.fit(X_train_svd, y_train)
        metrics = evaluate(model, X_test_svd, y_test)
        results.append((params, metrics))
        print(f"  -> acc={metrics['accuracy']:.4f}  prec={metrics['precision']:.4f}  "
              f"rec={metrics['recall']:.4f}  f1={metrics['f1']:.4f}")

    best_params, best_metrics = max(results, key=lambda x: x[1]["f1"])
    print(f"\nBest settings by macro F1: {param_label(best_params)}")

    print("\nRe-training best model ...")
    best_model = RandomForestClassifier(
        n_estimators=best_params["n_estimators"],
        max_depth=best_params["max_depth"],
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    best_model.fit(X_train_svd, y_train)
    best_metrics = evaluate(best_model, X_test_svd, y_test)

    print("\nClassification report (best model):\n")
    print(classification_report(y_test, best_metrics["y_pred"], target_names=LABELS))

    save_confusion_matrix(y_test, best_metrics["y_pred"], best_params)
    save_results_csv(results)
    save_summary(results, best_params, best_metrics)

    print("\nDone.")


if __name__ == "__main__":
    main()
