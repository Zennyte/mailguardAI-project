# EDA Summary
Dataset: `data\processed\email_dataset_combined.csv`
Shape: 68076 rows, 8 columns

## Label Distribution
| Label | Count | % |
|---|---|---|
| safe | 39377 | 57.8% |
| spam | 23854 | 35.0% |
| phishing | 4845 | 7.1% |

## Source Distribution
| Source | Count |
|---|---|
| CEAS_08 | 38963 |
| enron_spam_data | 15590 |
| SpamAssasin | 5802 |
| Nigerian_Fraud | 3293 |
| messages | 2876 |
| Nazario | 1552 |

## Text Length Statistics
| Column | Mean | Min | Max | Median |
|---|---|---|---|---|
| subject_length | 36 | 0 | 2657 | 32 |
| body_length | 1793 | 0 | 4560711 | 742 |
| text_length | 1830 | 3 | 4560761 | 782 |

## Notes
- Phishing is the smallest class (~7%). Use `class_weight='balanced'` in all classifiers.
- Some emails have very long bodies. TF-IDF with a token limit handles this naturally.
- Text length is clipped at 5000 characters in the histogram for readability.
