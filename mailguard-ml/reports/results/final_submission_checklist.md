# ML Project Submission Checklist

Use this checklist before submission or presentation to confirm
all required components are in place.

---

## Dataset

- [x] Raw datasets placed in `data/raw/` (not committed)
- [x] Datasets inspected with `src/inspect_datasets.py`
- [x] Datasets cleaned, merged, and saved to `data/processed/email_dataset_combined.csv`
- [x] Dataset inspection results documented in `reports/results/dataset_inspection_summary.md`
- [x] Column mapping documented in `reports/results/dataset_column_mapping.md`
- [x] Combined dataset summary documented in `reports/results/combined_dataset_summary.md`
- [x] Exploratory data analysis completed with charts in `reports/figures/`

## Preprocessing

- [x] Train/test split implemented (80/20, stratified)
- [x] TF-IDF vectorizer configured and fitted on training data only
- [x] Preprocessing summary saved to `reports/results/preprocessing_summary.md`

## Classifiers

- [x] Multinomial Naive Bayes trained and evaluated
- [x] Logistic Regression trained and evaluated
- [x] Linear SVM trained and evaluated
- [x] Random Forest trained and evaluated (with TruncatedSVD pipeline)
- [x] MLP Neural Network trained and evaluated (with TruncatedSVD pipeline)
- [x] At least 5 classifiers trained — satisfied

## Neural Network

- [x] Architecture 1: hidden_layer_sizes=(64,)
- [x] Architecture 2: hidden_layer_sizes=(128, 64)
- [x] Both architectures compared and best one selected
- [x] At least 2 neural network architectures tested — satisfied

## Hyperparameter Testing

- [x] Naive Bayes: alpha tested (0.1, 0.5, 1.0)
- [x] Logistic Regression: C tested (0.1, 1, 10)
- [x] Linear SVM: C tested (0.1, 1, 10)
- [x] Random Forest: n_estimators and max_depth tested
- [x] MLP: two architectures compared

## Evaluation Metrics

- [x] Accuracy reported for all models
- [x] Precision (macro) reported for all models
- [x] Recall (macro) reported for all models
- [x] F1-score (macro) reported for all models
- [x] Confusion matrices generated and saved for all models

## Model Comparison

- [x] All model results combined in `reports/results/model_comparison.csv`
- [x] Ranked comparison summary in `reports/results/model_comparison_summary.md`
- [x] Best model for export identified and justified

## Clustering

- [x] K-Means clustering implemented
- [x] k=2, 3, 4, 5 tested
- [x] Silhouette score, ARI, and NMI calculated
- [x] 2D scatter plot saved to `reports/figures/kmeans_clusters_k3.png`
- [x] Clustering summary saved to `reports/results/clustering_summary.md`
- [x] Clustering experiment documented in project report

## Final Model Export

- [x] Final Logistic Regression pipeline trained
- [x] Exported to `models/mail_detection_pipeline.joblib`
- [x] Smoke test passed (load and predict one sample)
- [x] Final model metrics saved to `reports/results/final_model_metrics.csv`
- [x] Final model summary saved to `reports/results/final_model_summary.md`

## Documentation

- [x] README updated with setup instructions and run order
- [x] `requirements.txt` complete
- [x] Project report draft completed: `reports/results/ml_project_report_draft.md`
- [x] This checklist completed

## Git

- [ ] All scripts committed with logical commit messages
- [ ] No raw datasets committed
- [ ] No processed CSV committed
- [ ] `models/mail_detection_pipeline.joblib` committed (or marked as local-only)
- [ ] Both team members have commits in the repository
