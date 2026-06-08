# MailGuard ML

Machine Learning component of the **MailGuard AI** project.

## Purpose

This repository trains and exports an email classification model that labels
emails as **safe**, **spam**, or **phishing**. The exported model is later used
by the MailGuard AI platform to scan emails.

## Note

This repository is for the **Machine Learning** part of MailGuard AI only.

Raw datasets should be placed in `data/raw/`, but they are **not committed** to
the repository (see `.gitignore`).

## How to inspect raw datasets

```
pip install -r requirements.txt
python src/inspect_datasets.py
```
