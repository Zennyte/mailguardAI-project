# Dataset Column Mapping

This file defines exactly how each raw dataset will be loaded and normalized
inside `prepare_dataset.py`.

It is based on the inspection results documented in:
`reports/results/dataset_inspection_summary.md`

---

## Final Target Schema

After preparation every dataset row will be normalized to these columns:

| Column | Description |
|---|---|
| `source_dataset` | Name of the source file (documentation only — not used in training) |
| `subject` | Normalized email subject |
| `body` | Normalized email body/message |
| `text` | Combined field: `subject + " " + body` — main input to the model |
| `label` | Final string label: `safe`, `spam`, or `phishing` |

---

## Column Mapping Table

| Dataset file | source_dataset name | Subject column | Body/message column | Original label column | Original label values | Final label mapping | Notes |
|---|---|---|---|---|---|---|---|
| CEAS_08.csv | `CEAS_08` | `subject` | `body` | `label` | `0` / `1` | `0` → safe, `1` → spam | Clean structure. Drop: `sender`, `receiver`, `date`, `urls`. |
| enron_spam_data.csv | `enron_spam_data` | `Subject` | `Message` | `Spam/Ham` | `ham` / `spam` | `ham` → safe, `spam` → spam | Column names differ in case and naming. Rename `Subject`→`subject`, `Message`→`body`. Drop: `Unnamed: 0`, `Date`. Some `Message` values are NaN — treat as empty string. |
| messages.csv | `messages` | `subject` | `message` | `label` | `0` / `1` | `0` → safe, `1` → spam | Uses `message` instead of `body`. Rename `message`→`body`. Drop nothing (only 3 columns). Some `subject` values are NaN — treat as empty string. |
| SpamAssasin.csv | `SpamAssasin` | `subject` | `body` | `label` | `0` / `1` | `0` → safe, `1` → spam | Clean structure. Drop: `sender`, `receiver`, `date`, `urls`. |
| Nazario.csv | `Nazario` | `subject` | `body` | *(ignored)* | *(all 1)* | all rows → phishing | Label column is numeric `1` for all rows but is not used. Phishing label assigned by source name. Drop: `sender`, `receiver`, `date`, `urls`, `label`. |
| Nigerian_Fraud.csv | `Nigerian_Fraud` | `subject` | `body` | *(ignored)* | *(all 1)* | all rows → phishing | Same as Nazario. Label column is ignored. Phishing label assigned by source name. Drop: `sender`, `receiver`, `date`, `urls`, `label`. |

---

## Datasets Excluded from Final Model

The following datasets are excluded because they are incompatible with the
raw-text classification approach used in this project:

| Dataset | Reason for exclusion |
|---|---|
| `spambase.data` | Contains numeric feature vectors extracted from emails, not raw email text. Cannot be merged with text-based datasets. |
| Any duplicate Enron/Ling-Spam variants | A clean version (`enron_spam_data.csv`) is already included. Additional variants would introduce duplicates. |
| Raw SpamAssassin folder | A cleaned CSV version (`SpamAssasin.csv`) is already included. |
| Any dataset that merges phishing and spam into a single binary class | This project requires three distinct labels (safe / spam / phishing). A binary phishing+spam class cannot be split reliably after the fact. |

The final model is trained only on raw email text. Any dataset that provides
pre-extracted numeric features is not compatible and is excluded.

---

## Rules for `prepare_dataset.py`

These rules must be followed when implementing the preparation script.

1. **Do not use `source_dataset` as a training feature.**
   It is added only for documentation and traceability. It must never be passed
   to the vectorizer or classifier.

2. **Combine subject and body into a single `text` column.**
   Use: `text = subject + " " + body`
   Handle NaN values before combining (replace with empty string).

3. **Remove rows where `text` is empty or whitespace only.**
   A row with no content cannot be classified meaningfully.

4. **Remove duplicate email texts.**
   Drop rows where the `text` column is an exact duplicate of another row.
   Duplicates across datasets are possible (e.g. the same spam message appearing
   in two sources).

5. **Keep only the three final labels: `safe`, `spam`, `phishing`.**
   Any row that does not map cleanly to one of these three labels must be
   dropped rather than guessed.

6. **Save the final combined dataset to:**
   `data/processed/email_dataset_combined.csv`
   with columns: `source_dataset`, `subject`, `body`, `text`, `label`

---

## Expected Row Counts After Mapping

| Final label | Approximate count | % of total |
|---|---|---|
| safe | ~40,360 | ~47% |
| spam | ~41,212 | ~48% |
| phishing | ~4,897 | ~6% |
| **Total** | **~86,469** | |

Phishing is underrepresented at approximately 6%. All classifiers must use
`class_weight='balanced'` where supported to compensate.
