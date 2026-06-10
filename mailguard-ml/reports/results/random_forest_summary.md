# Random Forest Results

## Hyperparameter Comparison

| n_estimators | max_depth | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|---|---|---|---|---|---|
| 100 | 30 | 0.9808 | 0.9814 | 0.9658 | 0.9734 |
| 100 | None | 0.9811 | 0.9826 | 0.9651 | 0.9736 |
| 200 | 30 | 0.9814 | 0.9825 | 0.9669 | 0.9745 |
| 200 **(best)** | None | 0.9819 | 0.9835 | 0.9673 | 0.9752 |

## Best Settings

- n_estimators: 200
- max_depth:     None
- class_weight:  balanced

## Best Metrics

- Accuracy:           0.9819
- Precision (macro):  0.9835
- Recall (macro):     0.9673
- F1 (macro):         0.9752

## Pipeline

TF-IDF (max_features=30000, ngram_range=(1,2)) -> TruncatedSVD (n_components=300) -> RandomForest

## Notes

- TruncatedSVD reduces TF-IDF features from 30000 to 300 before Random Forest.
- Macro averages are used because the phishing class is underrepresented.
- Random Forest is slower to train than linear models on this dataset size.
- Confusion matrix saved to `reports/figures/random_forest_confusion_matrix.png`.
