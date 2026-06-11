"""
train_mlp.py

Trains two MLP neural network architectures on the combined email dataset.
Uses TF-IDF + TruncatedSVD to reduce dimensionality before training.
Picks the better architecture by macro F1-score.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neural_network import MLPClassifier
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

ARCHITECTURES = [
    {"hidden_layer_sizes": (64,),      "label": "arch1_(64,)"},
    {"hidden_layer_sizes": (128, 64),  "label": "arch2_(128,64)"},
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


def save_confusion_matrix(y_test, y_pred, arch_label):
    cm = confusion_matrix(y_test, y_pred, labels=LABELS)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=LABELS)

    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(ax=ax, colorbar=False)
    ax.set_title(f"MLP — Confusion Matrix\n{arch_label}")
    plt.tight_layout()

    path = os.path.join(FIGURES_DIR, "mlp_confusion_matrix.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def save_results_csv(results):
    rows = []
    for arch, metrics in results:
        rows.append({
            "architecture": arch["label"],
            "hidden_layer_sizes": str(arch["hidden_layer_sizes"]),
            "accuracy": round(metrics["accuracy"], 4),
            "precision_macro": round(metrics["precision"], 4),
            "recall_macro": round(metrics["recall"], 4),
            "f1_macro": round(metrics["f1"], 4),
        })
    path = os.path.join(RESULTS_DIR, "mlp_results.csv")
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Saved: {path}")


def save_summary(results, best_arch, best_metrics):
    lines = [
        "# MLP Neural Network Results\n\n",
        "## Architecture Comparison\n\n",
        "| Architecture | hidden_layer_sizes | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |\n",
        "|---|---|---|---|---|---|\n",
    ]
    for arch, m in results:
        marker = " **(best)**" if arch["label"] == best_arch["label"] else ""
        lines.append(
            f"| {arch['label']}{marker} | {arch['hidden_layer_sizes']} | {m['accuracy']:.4f} | "
            f"{m['precision']:.4f} | {m['recall']:.4f} | {m['f1']:.4f} |\n"
        )
    lines += [
        f"\n## Best Architecture: {best_arch['label']}\n\n",
        f"- hidden_layer_sizes: {best_arch['hidden_layer_sizes']}\n",
        f"- activation: relu\n",
        f"- max_iter: 50\n",
        f"- random_state: {RANDOM_STATE}\n\n",
        "## Best Metrics\n\n",
        f"- Accuracy:           {best_metrics['accuracy']:.4f}\n",
        f"- Precision (macro):  {best_metrics['precision']:.4f}\n",
        f"- Recall (macro):     {best_metrics['recall']:.4f}\n",
        f"- F1 (macro):         {best_metrics['f1']:.4f}\n\n",
        "## Pipeline\n\n",
        "TF-IDF (max_features=30000, ngram_range=(1,2)) -> TruncatedSVD (n_components=300) -> MLPClassifier\n\n",
        "## Notes\n\n",
        "- max_iter=50 is intentionally low for speed. A ConvergenceWarning is expected.\n",
        "- The model still produces usable results within 50 iterations on this dataset.\n",
        "- MLP does not natively support class_weight, so phishing may score lower than in linear models.\n",
        "- Macro averages are used because the phishing class is underrepresented.\n",
        "- Confusion matrix saved to `reports/figures/mlp_confusion_matrix.png`.\n",
    ]
    path = os.path.join(RESULTS_DIR, "mlp_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Saved: {path}")


def main():
    print("=" * 60)
    print("MLP Neural Network Training")
    print("=" * 60)

    print("\nLoading and splitting data ...")
    X_train, X_test, y_train, y_test = load_and_split()
    print(f"Train: {len(X_train)}  Test: {len(X_test)}")

    print()
    X_train_svd, X_test_svd = build_tfidf_svd(X_train, X_test)

    print("\nTraining MLP architectures:\n")
    results = []
    for arch in ARCHITECTURES:
        print(f"  Training {arch['label']} ...")
        model = MLPClassifier(
            hidden_layer_sizes=arch["hidden_layer_sizes"],
            activation="relu",
            max_iter=50,
            random_state=RANDOM_STATE,
        )
        model.fit(X_train_svd, y_train)
        metrics = evaluate(model, X_test_svd, y_test)
        results.append((arch, metrics))
        print(f"  -> acc={metrics['accuracy']:.4f}  prec={metrics['precision']:.4f}  "
              f"rec={metrics['recall']:.4f}  f1={metrics['f1']:.4f}")

    best_arch, best_metrics = max(results, key=lambda x: x[1]["f1"])
    print(f"\nBest architecture by macro F1: {best_arch['label']}")

    print("\nRe-training best architecture ...")
    best_model = MLPClassifier(
        hidden_layer_sizes=best_arch["hidden_layer_sizes"],
        activation="relu",
        max_iter=50,
        random_state=RANDOM_STATE,
    )
    best_model.fit(X_train_svd, y_train)
    best_metrics = evaluate(best_model, X_test_svd, y_test)

    print("\nClassification report (best architecture):\n")
    print(classification_report(y_test, best_metrics["y_pred"], target_names=LABELS))

    save_confusion_matrix(y_test, best_metrics["y_pred"], best_arch["label"])
    save_results_csv(results)
    save_summary(results, best_arch, best_metrics)

    print("\nDone.")


if __name__ == "__main__":
    main()
