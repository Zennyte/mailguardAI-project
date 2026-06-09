# Logistic Regression Results

## C Value Comparison

| C | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|---|---|---|---|---|
| 0.1 | 0.9791 | 0.9694 | 0.9799 | 0.9746 |
| 1 | 0.9880 | 0.9816 | 0.9872 | 0.9844 |
| 10 **(best)** | 0.9913 | 0.9870 | 0.9893 | 0.9882 |

## Best C: 10

- Accuracy:           0.9913
- Precision (macro):  0.9870
- Recall (macro):     0.9893
- F1 (macro):         0.9882

## Settings

- class_weight: balanced
- max_iter: 1000
- solver: lbfgs (default)

## Notes

- Macro averages are used because the phishing class is underrepresented.
- class_weight='balanced' helps the model learn phishing despite fewer examples.
- This model is the chosen export for the MailGuard platform.
- Confusion matrix saved to `reports/figures/logistic_regression_confusion_matrix.png`.
