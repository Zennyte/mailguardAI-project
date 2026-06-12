# Final Model Summary

## Model

- Type: Logistic Regression
- C: 10.0
- class_weight: balanced
- max_iter: 1000

## Pipeline

TfidfVectorizer -> LogisticRegression

The pipeline is a single sklearn `Pipeline` object. It accepts raw email text and returns predictions directly.

## Why Logistic Regression

- It is explainable — easy to describe during a university presentation.
- It is fast at inference time — predictions take milliseconds.
- It supports `predict_proba()`, which provides a confidence score per class.
  The MailGuard platform uses this to show users a confidence percentage.
- Its macro F1-score is competitive with all other trained models.

## Test Set Metrics

- Accuracy:           0.9913
- Precision (macro):  0.9870
- Recall (macro):     0.9893
- F1 (macro):         0.9882

## Exported File

- Path: `models\mail_detection_pipeline.joblib`
- Format: joblib

## Platform Integration

Copy the exported file to the platform backend:

```
mailguard-platform/backend/app/ml/mail_detection_pipeline.joblib
```

The backend loads it with:

```python
import joblib
pipeline = joblib.load('app/ml/mail_detection_pipeline.joblib')
prediction = pipeline.predict([email_text])[0]
probabilities = pipeline.predict_proba([email_text])[0]
confidence = float(max(probabilities))
```
