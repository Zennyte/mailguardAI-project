# MLP Neural Network Results

## Architecture Comparison

| Architecture | hidden_layer_sizes | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|---|---|---|---|---|---|
| arch1_(64,) | (64,) | 0.9896 | 0.9865 | 0.9858 | 0.9861 |
| arch2_(128,64) **(best)** | (128, 64) | 0.9902 | 0.9856 | 0.9871 | 0.9864 |

## Best Architecture: arch2_(128,64)

- hidden_layer_sizes: (128, 64)
- activation: relu
- max_iter: 50
- random_state: 42

## Best Metrics

- Accuracy:           0.9902
- Precision (macro):  0.9856
- Recall (macro):     0.9871
- F1 (macro):         0.9864

## Pipeline

TF-IDF (max_features=30000, ngram_range=(1,2)) -> TruncatedSVD (n_components=300) -> MLPClassifier

## Notes

- max_iter=50 is intentionally low for speed. A ConvergenceWarning is expected.
- The model still produces usable results within 50 iterations on this dataset.
- MLP does not natively support class_weight, so phishing may score lower than in linear models.
- Macro averages are used because the phishing class is underrepresented.
- Confusion matrix saved to `reports/figures/mlp_confusion_matrix.png`.
