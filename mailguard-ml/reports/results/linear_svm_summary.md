# Linear SVM Results

## C Value Comparison

| C | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|---|---|---|---|---|
| 0.1 | 0.9894 | 0.9847 | 0.9872 | 0.9859 |
| 1 **(best)** | 0.9924 | 0.9888 | 0.9908 | 0.9898 |
| 10 | 0.9923 | 0.9898 | 0.9891 | 0.9894 |

## Best C: 1

- Accuracy:           0.9924
- Precision (macro):  0.9888
- Recall (macro):     0.9908
- F1 (macro):         0.9898

## Settings

- class_weight: balanced
- max_iter: 1000 (default)

## Notes

- Macro averages are used because the phishing class is underrepresented.
- LinearSVC does not output probabilities natively.
- Confusion matrix saved to `reports/figures/linear_svm_confusion_matrix.png`.
