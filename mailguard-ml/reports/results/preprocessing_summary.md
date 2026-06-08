# Preprocessing Summary

## Input Dataset

- Path: `data\processed\email_dataset_combined.csv`
- Total rows: 68076

## Train/Test Split

- Test size: 0.2 (80% train / 20% test)
- Random state: 42
- Stratified: yes

## Split Shapes

- X_train: 54460 rows
- X_test:  13616 rows

## Train Label Distribution

| Label | Count | % |
|---|---|---|
| safe | 31501 | 57.8% |
| spam | 19083 | 35.0% |
| phishing | 3876 | 7.1% |

## Test Label Distribution

| Label | Count | % |
|---|---|---|
| safe | 7876 | 57.8% |
| spam | 4771 | 35.0% |
| phishing | 969 | 7.1% |

## TF-IDF Settings

- max_features: 30000
- ngram_range: (1, 2)
- min_df: 2
- max_df: 0.95

## TF-IDF Matrix Shapes

- Train: 54460 rows x 30000 features
- Test:  13616 rows x 30000 features
