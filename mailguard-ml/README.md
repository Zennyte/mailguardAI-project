# MailGuard AI - Machine Learning Project

This is the machine learning part of the MailGuard AI university project.

The goal is to train a model that can classify emails into three categories:

- **safe** - a normal, legitimate email
- **spam** - unwanted bulk or promotional email
- **phishing** - a malicious email trying to steal information

---

## Project Goal

This part of the project covers:

1. Loading and merging several public email datasets into one clean file
2. Exploring the data and checking class distribution
3. Training and comparing multiple ML classifiers
4. Running K-Means clustering on the same dataset
5. Exporting the best model for use in the MailGuard AI web platform

---

## Datasets

Several public email datasets are used and merged into one unified format.

Raw dataset files are **not committed to GitHub**. You need to place them manually inside:

```
data/raw/
```

Expected files:
- `CEAS_08.csv`
- `enron_spam_data.csv`
- `messages.csv`
- `SpamAssasin.csv`
- `Nazario.csv`
- `Nigerian_Fraud.csv`

After running `prepare_dataset.py`, the combined dataset will have these columns:

| Column | Description |
|---|---|
| `source_dataset` | Which dataset this row came from |
| `subject` | Email subject line |
| `body` | Email body text |
| `text` | Subject and body combined (used as model input) |
| `label` | Final label: `safe`, `spam`, or `phishing` |

---

## Folder Structure

```
mailguard-ml/
  data/
    raw/           Place raw dataset CSV files here (not committed)
    processed/     Combined dataset saved here (not committed)
  src/             All Python scripts
  models/          Exported model file saved here
  reports/
    figures/       Charts and confusion matrix images
    results/       Metric tables, summaries, and the report draft
  README.md
  requirements.txt
```

---

## Installation

Make sure you have Python 3.11 or newer installed.

```bash
pip install -r requirements.txt
```

---

## How to Run the Project

Run the scripts in this order from the root of the repository:

```bash
python src/inspect_datasets.py
python src/prepare_dataset.py
python src/explore_dataset.py
python src/preprocess.py
python src/train_naive_bayes.py
python src/train_logistic_regression.py
python src/train_linear_svm.py
python src/train_random_forest.py
python src/train_mlp.py
python src/compare_models.py
python src/run_clustering.py
python src/export_model.py
```

Each script prints progress and saves its output to `reports/`.

---

## Models Used

- **Multinomial Naive Bayes** - simple probabilistic classifier, good baseline for text
- **Logistic Regression** - linear classifier, chosen as the final model
- **Linear SVM** - strong linear classifier for text classification
- **Random Forest** - ensemble of decision trees, uses TruncatedSVD to reduce features first
- **MLP Neural Network** - two architectures tested: (64,) and (128, 64) hidden layers
- **K-Means Clustering** - unsupervised experiment to see if emails naturally group together

---

## Final Model

The final exported model is **Logistic Regression**.

It was chosen because:
- it is simple and easy to explain
- it is fast at prediction time
- it gives a confidence score for each class using `predict_proba()`
- its performance is competitive with the other models

The exported file is saved to:

```
models/mail_detection_pipeline.joblib
```

This file is a scikit-learn `Pipeline` containing the TF-IDF vectorizer and the
Logistic Regression classifier together. The MailGuard AI platform backend loads
this file directly to make predictions.

---

## Notes

- Raw datasets are listed in `.gitignore` and will not be committed
- The processed dataset (`data/processed/`) is also not committed and must be generated locally by running `prepare_dataset.py`
- The model file (`models/mail_detection_pipeline.joblib`) can be committed or regenerated locally by running `export_model.py`
- All generated charts and metric files are saved under `reports/figures/` and `reports/results/`
