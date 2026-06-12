"""
export_model.py

Trains the final Logistic Regression pipeline and exports it to:
    models/mail_detection_pipeline.joblib

This exported file is intended to be copied into the MailGuard platform backend:
    mailguard-platform/backend/app/ml/mail_detection_pipeline.joblib

The pipeline object contains:
    TfidfVectorizer -> LogisticRegression

Calling pipeline.predict(["some email text"]) returns the label.
Calling pipeline.predict_proba(["some email text"]) returns class probabilities.
"""

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

DATA_FILE = os.path.join("data", "processed", "email_dataset_combined.csv")
MODELS_DIR = "models"
RESULTS_DIR = os.path.join("reports", "results")
MODEL_FILE = os.path.join(MODELS_DIR, "mail_detection_pipeline.joblib")
LR_RESULTS_FILE = os.path.join(RESULTS_DIR, "logistic_regression_results.csv")

TEST_SIZE = 0.2
RANDOM_STATE = 42
LABELS = ["safe", "spam", "phishing"]

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def pick_best_c():
    """Read the best C value from previous LR results, fall back to C=1."""
    if os.path.isfile(LR_RESULTS_FILE):
        df = pd.read_csv(LR_RESULTS_FILE)
        if "f1_macro" in df.columns and "C" in df.columns:
            best_c = df.loc[df["f1_macro"].idxmax(), "C"]
            print(f"Read best C={best_c} from {LR_RESULTS_FILE}")
            return float(best_c)
    print("LR results file not found — using default C=1")
    return 1.0


def load_and_split():
    df = pd.read_csv(DATA_FILE)
    X = df["text"].fillna("").astype(str)
    y = df["label"]
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)


def build_pipeline(best_c):
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=30000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
        )),
        ("clf", LogisticRegression(
            C=best_c,
            class_weight="balanced",
            max_iter=1000,
        )),
    ])


def save_metrics_csv(metrics):
    path = os.path.join(RESULTS_DIR, "final_model_metrics.csv")
    pd.DataFrame([metrics]).to_csv(path, index=False)
    print(f"Saved: {path}")


def save_summary(metrics, best_c):
    lines = [
        "# Final Model Summary\n\n",
        "## Model\n\n",
        "- Type: Logistic Regression\n",
        f"- C: {best_c}\n",
        "- class_weight: balanced\n",
        "- max_iter: 1000\n\n",
        "## Pipeline\n\n",
        "TfidfVectorizer -> LogisticRegression\n\n",
        "The pipeline is a single sklearn `Pipeline` object. "
        "It accepts raw email text and returns predictions directly.\n\n",
        "## Why Logistic Regression\n\n",
        "- It is explainable — easy to describe during a university presentation.\n",
        "- It is fast at inference time — predictions take milliseconds.\n",
        "- It supports `predict_proba()`, which provides a confidence score per class.\n",
        "  The MailGuard platform uses this to show users a confidence percentage.\n",
        "- Its macro F1-score is competitive with all other trained models.\n\n",
        "## Test Set Metrics\n\n",
        f"- Accuracy:           {metrics['accuracy']:.4f}\n",
        f"- Precision (macro):  {metrics['precision_macro']:.4f}\n",
        f"- Recall (macro):     {metrics['recall_macro']:.4f}\n",
        f"- F1 (macro):         {metrics['f1_macro']:.4f}\n\n",
        "## Exported File\n\n",
        f"- Path: `{MODEL_FILE}`\n",
        "- Format: joblib\n\n",
        "## Platform Integration\n\n",
        "Copy the exported file to the platform backend:\n\n",
        "```\n",
        "mailguard-platform/backend/app/ml/mail_detection_pipeline.joblib\n",
        "```\n\n",
        "The backend loads it with:\n\n",
        "```python\n",
        "import joblib\n",
        "pipeline = joblib.load('app/ml/mail_detection_pipeline.joblib')\n",
        "prediction = pipeline.predict([email_text])[0]\n",
        "probabilities = pipeline.predict_proba([email_text])[0]\n",
        "confidence = float(max(probabilities))\n",
        "```\n",
    ]
    path = os.path.join(RESULTS_DIR, "final_model_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Saved: {path}")


def main():
    print("=" * 60)
    print("Exporting Final Model Pipeline")
    print("=" * 60)

    best_c = pick_best_c()

    print("\nLoading and splitting data ...")
    X_train, X_test, y_train, y_test = load_and_split()
    print(f"Train: {len(X_train)}  Test: {len(X_test)}")

    print("\nTraining final pipeline ...")
    pipeline = build_pipeline(best_c)
    pipeline.fit(X_train, y_train)
    print("Training complete.")

    print("\nEvaluating on test set ...")
    y_pred = pipeline.predict(X_test)
    metrics = {
        "model":           "LogisticRegression",
        "best_C":          best_c,
        "accuracy":        round(accuracy_score(y_test, y_pred), 4),
        "precision_macro": round(precision_score(y_test, y_pred, average="macro", zero_division=0), 4),
        "recall_macro":    round(recall_score(y_test, y_pred, average="macro", zero_division=0), 4),
        "f1_macro":        round(f1_score(y_test, y_pred, average="macro", zero_division=0), 4),
    }

    print(f"\n  Accuracy:           {metrics['accuracy']:.4f}")
    print(f"  Precision (macro):  {metrics['precision_macro']:.4f}")
    print(f"  Recall (macro):     {metrics['recall_macro']:.4f}")
    print(f"  F1 (macro):         {metrics['f1_macro']:.4f}")

    print("\nClassification report:\n")
    print(classification_report(y_test, y_pred, target_names=LABELS))

    print(f"Saving pipeline to {MODEL_FILE} ...")
    joblib.dump(pipeline, MODEL_FILE)
    print("Pipeline saved.")

    # Quick smoke test — load back and predict one sample
    print("\nSmoke test (load and predict one sample) ...")
    loaded = joblib.load(MODEL_FILE)
    sample = ["Congratulations! You have won a $1000 gift card. Click here now."]
    pred = loaded.predict(sample)[0]
    proba = loaded.predict_proba(sample)[0]
    classes = loaded.classes_
    confidence = float(max(proba))
    print(f"  Input:      {sample[0]}")
    print(f"  Prediction: {pred}")
    print(f"  Confidence: {confidence:.2%}")
    print(f"  All probabilities: { {c: round(p, 4) for c, p in zip(classes, proba)} }")

    save_metrics_csv(metrics)
    save_summary(metrics, best_c)

    print("\nDone.")


if __name__ == "__main__":
    main()
