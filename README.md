# 🐰 AmberDash

> **A Federal Campaign Finance Audit Pipeline & Web Dashboard**  
> *A full-stack data pipeline tracking U.S. federal campaign expenditure data across Senate battleground races.*

---

## Project Overview
**Project AmberDash** is an automated campaign finance audit tool designed to ingest, clean, categorize, and visualize federal disbursement records from the OpenFEC API. By combining an automated ETL (Extract, Transform, Load) backend with a high-performance relational database and an interactive Streamlit web dashboard, AmberDash provides transparency into political spending trends across key target states.

---

## Tech Stack & Architecture

* **Backend & ETL Pipeline:** Python (`requests`, `pandas`, `re`)
* **Database & Relational Model:** SQLite 3
* **Frontend Web Application:** Streamlit
* **Version Control & CI/CD:** Git, GitHub
* **Target Data Source:** OpenFEC API (Schedule B Operating Expenditures)

---

## Features & Capabilities

- **Automated API Ingestion:** Batched retrieval of campaign spending records with automatic error handling and rate-limit management.
- **Regex Data Transformation:** Structured standardization of messy spending descriptions into clean, audit-ready expenditure categories (e.g., Media/Advertising, Payroll, Consulting, Travel).
- **Interactive Multi-Filter Dashboard:** Real-time analytics filtering by political party affiliation, battleground target state, and expenditure categories.
- **Granular Transaction Inspector:** Searchable raw data table allowing users to query individual recipient payments and descriptions.

---

## Repository Structure

```text
├── AmberDash.py                   # Streamlit web dashboard entry point
├── senate_pipeline.py       # OpenFEC API ETL ingestion script
├── clean_transform.py       # Data transformation & regex categorization rules
├── db_ingest.py             # SQLite database ingestion module
├── .env.example             # Environment variable template
├── requirements.txt         # Project dependencies
├── assets/                  # Custom branding & media assets
│   └── logo.png             # Project AmberDash logo
└── data/                    # Local SQLite database & cached datasets
    └── amberdash.db