# Dataset Inspection Summary

Generated from: `src/inspect_datasets.py`
Datasets location: `data/raw/`

---

## Detected Files

| # | File | Rows | Columns |
|---|---|---|---|
| 1 | CEAS_08.csv | 39,154 | 7 |
| 2 | Nazario.csv | 1,565 | 7 |
| 3 | Nigerian_Fraud.csv | 3,332 | 7 |
| 4 | SpamAssasin.csv | 5,809 | 7 |
| 5 | enron_spam_data.csv | 33,716 | 5 |
| 6 | messages.csv | 2,893 | 3 |
| | **Total** | **86,469** | |

All 6 files were read successfully on the first attempt (utf-8 encoding).

---

## Per-Dataset Details

### 1. CEAS_08.csv

- **Shape:** 39,154 rows × 7 columns
- **Columns:** `sender`, `receiver`, `date`, `subject`, `body`, `label`, `urls`
- **Subject column:** `subject`
- **Body column:** `body`
- **Label column:** `label` (integer)
- **Label value counts:**
  - `1` → 21,842 (spam)
  - `0` → 17,312 (safe)

---

### 2. Nazario.csv

- **Shape:** 1,565 rows × 7 columns
- **Columns:** `sender`, `receiver`, `date`, `subject`, `body`, `urls`, `label`
- **Subject column:** `subject`
- **Body column:** `body`
- **Label column:** `label` (integer)
- **Label value counts:**
  - `1` → 1,565 (all rows)
- **Note:** The numeric label value of `1` is misleading. Per the dataset specification, every row in Nazario is a phishing email and must be mapped to `phishing` based on the source name, not the numeric label.

---

### 3. Nigerian_Fraud.csv

- **Shape:** 3,332 rows × 7 columns
- **Columns:** `sender`, `receiver`, `date`, `subject`, `body`, `urls`, `label`
- **Subject column:** `subject`
- **Body column:** `body`
- **Label column:** `label` (integer)
- **Label value counts:**
  - `1` → 3,332 (all rows)
- **Note:** Same situation as Nazario. The `urls` column showed `0` for the first few rows while `label` showed `1`. The numeric label is not used for mapping. Every row is mapped to `phishing` by source name.

---

### 4. SpamAssasin.csv

- **Shape:** 5,809 rows × 7 columns
- **Columns:** `sender`, `receiver`, `date`, `subject`, `body`, `label`, `urls`
- **Subject column:** `subject`
- **Body column:** `body`
- **Label column:** `label` (integer)
- **Label value counts:**
  - `0` → 4,091 (safe)
  - `1` → 1,718 (spam)

---

### 5. enron_spam_data.csv

- **Shape:** 33,716 rows × 5 columns
- **Columns:** `Unnamed: 0`, `Subject`, `Message`, `Spam/Ham`, `Date`
- **Subject column:** `Subject` (capital S — different from others)
- **Body column:** `Message` (not `body` — different from others)
- **Label column:** `Spam/Ham` (string values — different from others)
- **Label value counts:**
  - `spam` → 17,171
  - `ham` → 16,545
- **Notes:**
  - Has an unnamed index column (`Unnamed: 0`) that should be dropped.
  - Column names use different casing and naming conventions compared to all other datasets.
  - Some `Message` values appear to be NaN (e.g. row 0 in the sample).

---

### 6. messages.csv

- **Shape:** 2,893 rows × 3 columns
- **Columns:** `subject`, `message`, `label`
- **Subject column:** `subject`
- **Body column:** `message` (not `body` — different from CEAS/Nazario/Nigerian/SpamAssassin)
- **Label column:** `label` (integer)
- **Label value counts:**
  - `0` → 2,412 (safe)
  - `1` → 481 (spam)
- **Notes:**
  - Smallest column set — only 3 columns. No sender, receiver, date, or urls.
  - Some subject values appear to be NaN (e.g. row 1 in the sample).

---

## Identified Issues

| # | Issue | Affected Datasets | Impact |
|---|---|---|---|
| 1 | Body column named `Message` instead of `body` | enron_spam_data | Must rename during preparation |
| 2 | Body column named `message` instead of `body` | messages | Must rename during preparation |
| 3 | Subject column named `Subject` (capital S) | enron_spam_data | Must rename during preparation |
| 4 | Label column named `Spam/Ham` with string values (`ham`/`spam`) | enron_spam_data | Must rename and remap during preparation |
| 5 | Unnamed index column (`Unnamed: 0`) | enron_spam_data | Must be dropped |
| 6 | Phishing label is numeric `1` but must be overridden to `phishing` | Nazario, Nigerian_Fraud | Label must be assigned by source, not by column value |
| 7 | Missing subject values (NaN) in some rows | messages, Nazario | Handle with empty string or combined text fallback |
| 8 | Missing body/message values (NaN) in some rows | enron_spam_data, messages | Handle with empty string or combined text fallback |
| 9 | Phishing class is heavily underrepresented | Nazario + Nigerian_Fraud combined | Use `class_weight='balanced'` in all classifiers |

---

## Estimated Class Distribution After Mapping

| Final Label | Source | Count |
|---|---|---|
| safe | CEAS_08 (label=0) | 17,312 |
| safe | enron_spam_data (ham) | 16,545 |
| safe | SpamAssasin (label=0) | 4,091 |
| safe | messages (label=0) | 2,412 |
| **safe total** | | **~40,360 (~47%)** |
| spam | CEAS_08 (label=1) | 21,842 |
| spam | enron_spam_data (spam) | 17,171 |
| spam | SpamAssasin (label=1) | 1,718 |
| spam | messages (label=1) | 481 |
| **spam total** | | **~41,212 (~48%)** |
| phishing | Nazario (all rows) | 1,565 |
| phishing | Nigerian_Fraud (all rows) | 3,332 |
| **phishing total** | | **~4,897 (~6%)** |
| **Grand total** | | **~86,469** |

Phishing is underrepresented at approximately 6%. This is expected and must be handled with `class_weight='balanced'` in the classifiers.

---

## Proposed Column Mapping for Preparation Script

| source_dataset | subject column | body/text column | original label column | original label values | final label mapping |
|---|---|---|---|---|---|
| CEAS_08 | `subject` | `body` | `label` | `0` / `1` | `0` → safe, `1` → spam |
| enron_spam_data | `Subject` | `Message` | `Spam/Ham` | `ham` / `spam` | `ham` → safe, `spam` → spam |
| messages | `subject` | `message` | `label` | `0` / `1` | `0` → safe, `1` → spam |
| SpamAssasin | `subject` | `body` | `label` | `0` / `1` | `0` → safe, `1` → spam |
| Nazario | `subject` | `body` | *(ignored)* | *(all 1)* | all rows → phishing |
| Nigerian_Fraud | `subject` | `body` | *(ignored)* | *(all 1)* | all rows → phishing |

### Unified output columns

After preparation, every dataset will be normalized to:

```
source_dataset | subject | body | text | label
```

- `source_dataset`: name of the source file (for documentation only, not used in training)
- `subject`: normalized subject column
- `body`: normalized body/message column
- `text`: combined field (`subject + " " + body`) used as the main model input
- `label`: final string label — one of `safe`, `spam`, `phishing`
