"""
compare_models.py

Reads the best result from each model's results CSV and produces a
side-by-side comparison table ranked by macro F1-score.
"""

import os
import pandas as pd

RESULTS_DIR = os.path.join("reports", "results")

# Each entry: (display name, csv filename, hyperparameter column name)
MODEL_FILES = [
    ("Naive Bayes",          "naive_bayes_results.csv",          "alpha"),
    ("Logistic Regression",  "logistic_regression_results.csv",  "C"),
    ("Linear SVM",           "linear_svm_results.csv",           "C"),
    ("Random Forest",        "random_forest_results.csv",        "n_estimators"),
    ("MLP Neural Network",   "mlp_results.csv",                  "architecture"),
]


def load_best_row(csv_name, hyperparam_col):
    path = os.path.join(RESULTS_DIR, csv_name)
    if not os.path.isfile(path):
        print(f"  [SKIP] Not found: {path}")
        return None
    df = pd.read_csv(path)
    if "f1_macro" not in df.columns:
        print(f"  [SKIP] No f1_macro column in {csv_name}")
        return None
    best_row = df.loc[df["f1_macro"].idxmax()]
    hyperparam_value = best_row[hyperparam_col] if hyperparam_col in best_row else "n/a"
    return {
        "best_hyperparam_col": hyperparam_col,
        "best_hyperparam_val": hyperparam_value,
        "accuracy":        round(best_row["accuracy"], 4),
        "precision_macro": round(best_row["precision_macro"], 4),
        "recall_macro":    round(best_row["recall_macro"], 4),
        "f1_macro":        round(best_row["f1_macro"], 4),
    }


def save_comparison_csv(rows):
    path = os.path.join(RESULTS_DIR, "model_comparison.csv")
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Saved: {path}")


def save_comparison_summary(rows):
    lines = [
        "# Model Comparison Summary\n\n",
        "Models are ranked by macro F1-score.\n",
        "Macro averages are used because the phishing class is underrepresented (~7%).\n\n",
        "## Results Table\n\n",
        "| Rank | Model | Best Setting | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |\n",
        "|---|---|---|---|---|---|---|\n",
    ]
    for i, row in enumerate(rows, start=1):
        setting = f"{row['best_hyperparam_col']}={row['best_hyperparam_val']}"
        lines.append(
            f"| {i} | {row['model']} | {setting} | {row['accuracy']:.4f} | "
            f"{row['precision_macro']:.4f} | {row['recall_macro']:.4f} | {row['f1_macro']:.4f} |\n"
        )

    best_model = rows[0]["model"]
    lines += [
        "\n## Model Selection for Platform Integration\n\n",
        "**Selected model: Logistic Regression**\n\n",
        "Logistic Regression is chosen as the exported model for the MailGuard platform "
        "because:\n\n",
        "- It supports `predict_proba()`, which provides a confidence score per class.\n",
        "- The confidence score is shown to the user in the platform (e.g. 93% phishing).\n",
        "- It is fast at inference time — one prediction takes milliseconds.\n",
        "- It is explainable and easy to describe during a presentation.\n",
        "- Its macro F1-score is competitive with the other models on this dataset.\n\n",
        f"Note: The model with the highest macro F1-score overall was **{best_model}**. "
        "If confidence scores are not required, that model could also be used.\n\n",
        "## Confusion Matrix Files\n\n",
        "| Model | File |\n",
        "|---|---|\n",
        "| Naive Bayes | `reports/figures/naive_bayes_confusion_matrix.png` |\n",
        "| Logistic Regression | `reports/figures/logistic_regression_confusion_matrix.png` |\n",
        "| Linear SVM | `reports/figures/linear_svm_confusion_matrix.png` |\n",
        "| Random Forest | `reports/figures/random_forest_confusion_matrix.png` |\n",
        "| MLP Neural Network | `reports/figures/mlp_confusion_matrix.png` |\n",
    ]

    path = os.path.join(RESULTS_DIR, "model_comparison_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Saved: {path}")


def main():
    print("=" * 60)
    print("Model Comparison")
    print("=" * 60)
    print()

    rows = []
    for display_name, csv_name, hyperparam_col in MODEL_FILES:
        print(f"Reading {csv_name} ...")
        best = load_best_row(csv_name, hyperparam_col)
        if best is None:
            continue
        row = {"model": display_name}
        row.update(best)
        rows.append(row)
        print(f"  Best {hyperparam_col}={best['best_hyperparam_val']}  "
              f"f1={best['f1_macro']:.4f}  acc={best['accuracy']:.4f}")

    if not rows:
        print("\nNo model results found. Run the training scripts first.")
        return

    rows.sort(key=lambda r: r["f1_macro"], reverse=True)

    print("\nRanked by macro F1:\n")
    for i, row in enumerate(rows, start=1):
        print(f"  {i}. {row['model']:<22}  f1={row['f1_macro']:.4f}  acc={row['accuracy']:.4f}")

    save_comparison_csv(rows)
    save_comparison_summary(rows)

    print("\nDone.")


if __name__ == "__main__":
    main()
