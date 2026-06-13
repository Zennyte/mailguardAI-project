# MailGuard AI — Machine Learning Project Report

**Subject:** Machine Learning
**Project:** MailGuard AI
**Repository:** mailguard-ml

---

## 1. Introduction

This report describes the machine learning component of the MailGuard AI project.
The goal of this component is to train an email classification model that can
identify whether an email is safe, spam, or a phishing attempt.

The trained model is exported and integrated into the MailGuard AI web platform,
where users can submit an email's subject and body and receive a prediction with
a confidence score.

---

## 2. Problem Statement

Email remains one of the most common attack vectors for cybercriminals.
Phishing emails trick users into clicking malicious links or revealing sensitive
information. Spam emails waste time and clutter inboxes. A system that can
automatically classify emails into one of three categories — safe, spam, or
phishing — helps users identify threats before interacting with suspicious content.

**Classification task:** multi-class text classification
**Input:** raw email text (subject + body combined)
**Output:** one of three labels — `safe`, `spam`, or `phishing`

---

## 3. Dataset Description

Six publicly available email datasets were used. All datasets contain raw email
text and were selected because they provide subject and body fields rather than
pre-extracted numeric features.

| Dataset | Rows | Classes |
|---|---|---|
| CEAS_08.csv | 39,154 | safe (0), spam (1) |
| enron_spam_data.csv | 33,716 | ham → safe, spam |
| messages.csv (Ling-Spam) | 2,893 | safe (0), spam (1) |
| SpamAssasin.csv | 5,809 | safe (0), spam (1) |
| Nazario.csv | 1,565 | all phishing |
| Nigerian_Fraud.csv | 3,332 | all phishing |

**Excluded datasets:**
- `spambase.data` — contains numeric features, not raw text
- Any dataset that merges spam and phishing into a single binary class

---

## 4. Dataset Cleaning and Merging

Each dataset had different column names, label formats, and encodings.
The preparation script (`src/prepare_dataset.py`) handles all of this.

**Steps applied:**

1. Each dataset loaded with encoding fallback (utf-8 → latin-1 → cp1252).
2. Subject and body columns renamed to a unified schema.
3. Labels mapped to final string values:
   - `0` or `ham` → `safe`
   - `1` or `spam` → `spam`
   - All rows in Nazario and Nigerian_Fraud → `phishing`
4. Subject and body combined into a single `text` column.
5. Rows with empty `text` removed.
6. Duplicate email texts removed across all datasets.
7. All datasets concatenated into one file.

**Output:** `data/processed/email_dataset_combined.csv`
with columns: `source_dataset`, `subject`, `body`, `text`, `label`

---

## 5. Final Dataset Shape and Label Distribution

| Label | Count | Percentage |
|---|---|---|
| safe | 39,377 | 57.8% |
| spam | 23,854 | 35.0% |
| phishing | 4,845 | 7.1% |
| **Total** | **68,076** | |

The phishing class is underrepresented at approximately 7%. This is expected
because fewer labeled phishing datasets are publicly available. All classifiers
that support it use `class_weight='balanced'` to compensate.

---

## 6. Preprocessing

**Train/test split:**
- 80% training, 20% test
- Stratified by label to preserve class proportions
- `random_state=42` for reproducibility

**Text vectorization — TF-IDF:**
- The `text` column (subject + body) is the only input feature.
- TF-IDF converts text into a matrix of term importance scores.
- Settings used:
  - `max_features=30000` — vocabulary capped at 30,000 tokens
  - `ngram_range=(1,2)` — includes single words and two-word phrases
  - `min_df=2` — ignores terms that appear in fewer than 2 documents
  - `max_df=0.95` — ignores terms that appear in more than 95% of documents

For Random Forest and MLP Neural Network, TruncatedSVD with 300 components
is applied after TF-IDF to reduce dimensionality before training.

---

## 7. Models Trained

Five classifiers were trained and evaluated.

### 7.1 Multinomial Naive Bayes

A simple probabilistic classifier well suited for text classification.
Hyperparameter tested: `alpha` = 0.1, 0.5, 1.0.
Does not support `class_weight`.

### 7.2 Logistic Regression

A linear classifier that models class probabilities using the logistic function.
Hyperparameter tested: `C` = 0.1, 1, 10.
Uses `class_weight='balanced'` and `max_iter=1000`.
Selected as the final exported model (see Section 9).

### 7.3 Linear SVM (LinearSVC)

A linear support vector classifier optimized for text classification.
Hyperparameter tested: `C` = 0.1, 1, 10.
Uses `class_weight='balanced'`.
Does not natively produce probability outputs.

### 7.4 Random Forest

An ensemble of decision trees. Requires dense input, so TruncatedSVD(300)
is applied before training to reduce the TF-IDF matrix.
Hyperparameters tested:
- `n_estimators`: 100, 200
- `max_depth`: 30, None
Uses `class_weight='balanced'`.

### 7.5 MLP Neural Network

A multi-layer perceptron implemented using scikit-learn's `MLPClassifier`.
Two architectures were compared:

| Architecture | hidden_layer_sizes | Notes |
|---|---|---|
| Arch 1 | (64,) | Single hidden layer |
| Arch 2 | (128, 64) | Two hidden layers |

Both use `activation='relu'` and `max_iter=50`.
MLP does not support `class_weight`, so phishing performance may be weaker
compared to the linear models.

---

## 8. Evaluation Metrics

All models are evaluated using:

- **Accuracy** — percentage of correctly classified emails
- **Precision (macro)** — average precision across all three classes
- **Recall (macro)** — average recall across all three classes
- **F1-score (macro)** — harmonic mean of precision and recall, averaged across classes
- **Confusion matrix** — shows where the model confuses one class for another

Macro averages are used (not weighted) because the phishing class is small.
Weighted averages would underreport phishing performance, which is the most
critical class to get right.

---

## 9. Model Comparison

All results are stored in `reports/results/model_comparison.csv`.
Models are ranked by macro F1-score in `reports/results/model_comparison_summary.md`.

The comparison covers the best hyperparameter setting for each model.

---

## 10. Why Logistic Regression Was Selected for Export

The final exported model is Logistic Regression for the following reasons:

1. **Confidence scores** — `predict_proba()` returns a probability per class.
   The platform displays this as a confidence percentage (e.g. "93% phishing").
   LinearSVC does not support this natively.

2. **Speed** — a single TF-IDF + Logistic Regression prediction takes
   milliseconds, making it suitable for a real-time web application.

3. **Explainability** — Logistic Regression is easy to explain during a
   presentation. The model learns feature weights, and higher weights on
   words like "urgent", "winner", or "bank account" make intuitive sense.

4. **Competitive performance** — Logistic Regression achieves macro F1
   close to or equal to the best model on this dataset.

---

## 11. Clustering Experiment

K-Means clustering was performed on the same dataset to explore whether
the text content naturally separates into groups without using labels.

**Pipeline:** TF-IDF → TruncatedSVD(100) → KMeans

**k values tested:** 2, 3, 4, 5

**Metrics used:**
- Silhouette Score — measures how well separated the clusters are
- Adjusted Rand Index (ARI) — compares clusters to true labels
- Normalized Mutual Information (NMI) — measures shared information between clusters and labels

The true labels were removed before clustering and used only afterwards
for evaluation. Since clustering is unsupervised, the clusters do not need
to align perfectly with safe/spam/phishing.

A 2D scatter plot (SVD projection) was saved to
`reports/figures/kmeans_clusters_k3.png` showing k=3 clusters alongside
the true labels for visual comparison.

---

## 12. Conclusion

The MailGuard ML project successfully trained, compared, and exported a
three-class email classification model. The final Logistic Regression pipeline
achieves strong macro F1 performance across all three classes and is ready for
integration into the MailGuard AI platform.

The exported model file is:
`models/mail_detection_pipeline.joblib`

---

## 13. Limitations and Future Improvements

- **Phishing underrepresentation** — only ~7% of the dataset is phishing.
  More phishing datasets would improve model recall on this class.
- **No deep learning** — only scikit-learn models were used. A fine-tuned
  transformer (e.g. BERT) would likely perform better but is outside the
  scope of a university project.
- **No URL or header analysis** — the model uses only text content.
  Analyzing embedded URLs or email headers could catch more sophisticated attacks.
- **Dataset age** — some datasets (e.g. Enron, CEAS 2008) are over 15 years old.
  Phishing techniques have evolved and modern emails may differ significantly.
- **Clustering alignment** — K-Means clusters do not strongly align with real labels
  because safe and spam emails share a lot of vocabulary. This is expected.
