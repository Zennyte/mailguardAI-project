# Naive Bayes Results

## Alpha Comparison

| Alpha | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|---|---|---|---|---|
| 0.1 **(best)** | 0.9703 | 0.9702 | 0.9670 | 0.9679 |
| 0.5 | 0.9702 | 0.9666 | 0.9661 | 0.9656 |
| 1.0 | 0.9694 | 0.9689 | 0.9646 | 0.9661 |

## Best Alpha: 0.1

- Accuracy:           0.9703
- Precision (macro):  0.9702
- Recall (macro):     0.9670
- F1 (macro):         0.9679

## Notes

- Macro averages are used because the phishing class is underrepresented.
- Confusion matrix saved to `reports/figures/naive_bayes_confusion_matrix.png`.
