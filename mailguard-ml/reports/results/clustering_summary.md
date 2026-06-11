# K-Means Clustering Summary

## Setup

- Algorithm: K-Means
- Pipeline: TF-IDF -> TruncatedSVD (100 components) -> KMeans
- True labels were removed before clustering.
- True labels are used only afterwards to calculate ARI and NMI.

## Results

| k | Silhouette Score | Adjusted Rand Index | Normalized Mutual Info |
|---|---|---|---|
| 2 | 0.4353 | 0.0438 | 0.0895 |
| 3 | 0.4431 | 0.0667 | 0.1220 |
| 4 | 0.2742 | 0.0238 | 0.1403 |
| 5 | 0.1963 | -0.0008 | 0.1498 |

## Key Findings

- Best silhouette score: k=3 (0.4431)
- Best ARI:              k=3 (0.0667)
- Best NMI:              k=5 (0.1498)

## k=3 Focus

Since the dataset has 3 real classes (safe, spam, phishing), k=3 is the main comparison point.

- Silhouette Score:      0.4431
- Adjusted Rand Index:   0.0667
- Normalized Mutual Info:0.1220

## Interpretation

- Clustering is **unsupervised** — the model sees no labels during training.
- A perfect ARI of 1.0 would mean clusters align exactly with real labels.
- A low ARI is expected because safe/spam emails often share vocabulary.
- The 2D scatter plot (SVD components 1 and 2) shows cluster separation visually.
- The right panel shows the true labels for direct comparison.
- Scatter plot saved to `reports/figures/kmeans_clusters_k3.png`.
