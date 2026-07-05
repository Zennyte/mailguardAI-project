# Project Report - MailGuard AI Platform

Raporti i projektit per Lab Course 2. Do te plotesohet gjate zhvillimit.

## 1. Introduction

_Short description of the project and its goal._

## 2. Relation to the ML Project

_How the platform uses the trained model from the Machine Learning project._

## 3. Architecture

_Backend (FastAPI, layered: controllers -> services -> repositories), frontend (React + Vite), databases (PostgreSQL + MongoDB)._

## 4. Features

_Authentication, email scanning, real-time notifications, history, search, import/export, reports, CMS._

Additional features implemented so far:

- **Machine Learning Integration** — the exported Logistic Regression pipeline
  classifies emails as safe/spam/phishing with confidence scores.
- **Advanced Search Functionality** — one search endpoint covers 5 lists
  (scans, email messages, notifications, reports, CMS pages) with text, label,
  status, and date filters plus sorting.
- **Data Import/Export** — export of 5 lists as CSV/JSON/XLSX and import into
  5 lists from the same formats, with row validation and skip counts.

## 5. Database Design

_Summary + link to DATABASE_DESIGN.md and the ERD._

## 6. How to Run

_Setup and run instructions (see README)._

## 7. Conclusions

_To be written at the end._
