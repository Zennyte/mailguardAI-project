"""
run_clustering.py

Runs K-Means clustering on the combined email dataset.
True labels are removed before clustering and used only for comparison afterwards.

Tests k=2, 3, 4, 5 and evaluates using silhouette score, ARI, and NMI.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    adjusted_rand_score,
    normalized_mutual_info_score,
)

DATA_FILE = os.path.join("data", "processed", "email_dataset_combined.csv")
FIGURES_DIR = os.path.join("reports", "figures")
RESULTS_DIR = os.path.join("reports", "results")

RANDOM_STATE = 42
K_VALUES = [2, 3, 4, 5]

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_FILE)
    X_text = df["text"].fillna("").astype(str)
    y_true = df["label"]
    return X_text, y_true


def build_tfidf(X_text):
    print("Fitting TF-IDF ...")
    vectorizer = TfidfVectorizer(max_features=30000, ngram_range=(1, 2), min_df=2, max_df=0.95)
    X_tfidf = vectorizer.fit_transform(X_text)
    print(f"TF-IDF shape: {X_tfidf.shape}")
    return X_tfidf


def reduce_dimensions(X_tfidf, n_components):
    print(f"Applying TruncatedSVD (n_components={n_components}) ...")
    svd = TruncatedSVD(n_components=n_components, random_state=RANDOM_STATE)
    X_reduced = svd.fit_transform(X_tfidf)
    explained = svd.explained_variance_ratio_.sum()
    print(f"Explained variance: {explained:.2%}")
    return X_reduced


def run_kmeans(X_reduced, y_true):
    results = []
    for k in K_VALUES:
        print(f"  Running KMeans k={k} ...")
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        cluster_labels = km.fit_predict(X_reduced)

        sil = silhouette_score(X_reduced, cluster_labels, sample_size=10000, random_state=RANDOM_STATE)
        ari = adjusted_rand_score(y_true, cluster_labels)
        nmi = normalized_mutual_info_score(y_true, cluster_labels)

        results.append({
            "k": k,
            "silhouette_score": round(sil, 4),
            "adjusted_rand_index": round(ari, 4),
            "normalized_mutual_info": round(nmi, 4),
        })
        print(f"    silhouette={sil:.4f}  ARI={ari:.4f}  NMI={nmi:.4f}")

    return results


def plot_clusters_k3(X_2d, y_true):
    print("\nPlotting k=3 clusters ...")
    km = KMeans(n_clusters=3, random_state=RANDOM_STATE, n_init=10)
    cluster_labels = km.fit_predict(X_2d)

    colors = ["#2196f3", "#f44336", "#4caf50"]
    cluster_names = ["Cluster 0", "Cluster 1", "Cluster 2"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left plot: K-Means cluster assignments
    for i, (color, name) in enumerate(zip(colors, cluster_names)):
        mask = cluster_labels == i
        axes[0].scatter(X_2d[mask, 0], X_2d[mask, 1], c=color, label=name,
                        alpha=0.3, s=5, rasterized=True)
    axes[0].set_title("K-Means Clusters (k=3)")
    axes[0].set_xlabel("SVD Component 1")
    axes[0].set_ylabel("SVD Component 2")
    axes[0].legend(markerscale=3)

    # Right plot: true labels for comparison
    label_colors = {"safe": "#4caf50", "spam": "#f44336", "phishing": "#ff9800"}
    for label, color in label_colors.items():
        mask = pd.Series(y_true.values) == label
        axes[1].scatter(X_2d[mask.values, 0], X_2d[mask.values, 1],
                        c=color, label=label, alpha=0.3, s=5, rasterized=True)
    axes[1].set_title("True Labels (for comparison)")
    axes[1].set_xlabel("SVD Component 1")
    axes[1].set_ylabel("SVD Component 2")
    axes[1].legend(markerscale=3)

    plt.suptitle("2D SVD Projection — K-Means (k=3) vs True Labels", fontsize=12)
    plt.tight_layout()

    path = os.path.join(FIGURES_DIR, "kmeans_clusters_k3.png")
    plt.savefig(path, dpi=100)
    plt.close()
    print(f"Saved: {path}")


def save_results_csv(results):
    path = os.path.join(RESULTS_DIR, "clustering_results.csv")
    pd.DataFrame(results).to_csv(path, index=False)
    print(f"Saved: {path}")


def save_summary(results):
    df = pd.DataFrame(results)
    best_sil = df.loc[df["silhouette_score"].idxmax()]
    best_ari = df.loc[df["adjusted_rand_index"].idxmax()]
    best_nmi = df.loc[df["normalized_mutual_info"].idxmax()]
    k3_row = df[df["k"] == 3].iloc[0]

    lines = [
        "# K-Means Clustering Summary\n\n",
        "## Setup\n\n",
        "- Algorithm: K-Means\n",
        "- Pipeline: TF-IDF -> TruncatedSVD (100 components) -> KMeans\n",
        "- True labels were removed before clustering.\n",
        "- True labels are used only afterwards to calculate ARI and NMI.\n\n",
        "## Results\n\n",
        "| k | Silhouette Score | Adjusted Rand Index | Normalized Mutual Info |\n",
        "|---|---|---|---|\n",
    ]
    for row in results:
        lines.append(
            f"| {row['k']} | {row['silhouette_score']:.4f} | "
            f"{row['adjusted_rand_index']:.4f} | {row['normalized_mutual_info']:.4f} |\n"
        )

    lines += [
        "\n## Key Findings\n\n",
        f"- Best silhouette score: k={int(best_sil['k'])} ({best_sil['silhouette_score']:.4f})\n",
        f"- Best ARI:              k={int(best_ari['k'])} ({best_ari['adjusted_rand_index']:.4f})\n",
        f"- Best NMI:              k={int(best_nmi['k'])} ({best_nmi['normalized_mutual_info']:.4f})\n\n",
        "## k=3 Focus\n\n",
        "Since the dataset has 3 real classes (safe, spam, phishing), k=3 is the main comparison point.\n\n",
        f"- Silhouette Score:      {k3_row['silhouette_score']:.4f}\n",
        f"- Adjusted Rand Index:   {k3_row['adjusted_rand_index']:.4f}\n",
        f"- Normalized Mutual Info:{k3_row['normalized_mutual_info']:.4f}\n\n",
        "## Interpretation\n\n",
        "- Clustering is **unsupervised** — the model sees no labels during training.\n",
        "- A perfect ARI of 1.0 would mean clusters align exactly with real labels.\n",
        "- A low ARI is expected because safe/spam emails often share vocabulary.\n",
        "- The 2D scatter plot (SVD components 1 and 2) shows cluster separation visually.\n",
        "- The right panel shows the true labels for direct comparison.\n",
        "- Scatter plot saved to `reports/figures/kmeans_clusters_k3.png`.\n",
    ]

    path = os.path.join(RESULTS_DIR, "clustering_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Saved: {path}")


def main():
    print("=" * 60)
    print("K-Means Clustering")
    print("=" * 60)

    print("\nLoading data ...")
    X_text, y_true = load_data()
    print(f"Rows: {len(X_text)}")

    X_tfidf = build_tfidf(X_text)

    print("\nReducing to 100 components for clustering ...")
    X_100 = reduce_dimensions(X_tfidf, n_components=100)

    print("\nReducing to 2 components for visualization ...")
    X_2d = reduce_dimensions(X_tfidf, n_components=2)

    print("\nRunning KMeans for k = 2, 3, 4, 5:\n")
    results = run_kmeans(X_100, y_true)

    plot_clusters_k3(X_2d, y_true)
    save_results_csv(results)
    save_summary(results)

    print("\nDone.")


if __name__ == "__main__":
    main()
