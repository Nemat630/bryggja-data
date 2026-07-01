# 🇸🇪 Bryggja — Swedish Labour Market Data Pipeline

A complete modern data stack that ingests live Swedish job postings, transforms them with dbt, and visualises insights in an interactive dashboard.

## What it does

- Fetches real-time job listings from **Arbetsförmedlingen's open API** (no key required)
- Loads raw data into **DuckDB** — a fast, local analytical database
- Transforms and cleans data using **dbt** with staging and mart models
- Runs automated **data quality tests** on every model
- Displays results in a live **Streamlit + Plotly dashboard**

## Key findings (as of July 2026)

- 🏙️ **Stockholm** accounts for 38% of all data/tech job openings in Sweden
- 👷 **Data Engineer** is the #1 most in-demand role (27 openings)
- ⚡ **Elektriker** has the widest geographic spread — 19 openings in 14 cities
- 🤖 **Machine Learning Engineer** ranks #4 with 9 openings

## Architecture

```
Arbetsförmedlingen API
        ↓
  load_jobs.py (Python ELT)
        ↓
  DuckDB — raw.jobs
        ↓
  dbt — stg_jobs (cleaned, tested)
        ↓
  dbt — marts (jobs_by_location, jobs_by_title, daily_pipeline)
        ↓
  Streamlit Dashboard (localhost:8501)
```

## Tech stack

| Layer | Tool | Why |
|---|---|---|
| Source | Arbetsförmedlingen JobSearch API | Free, open, no key needed |
| Extract & Load | Python + requests | Simple ELT script |
| Warehouse | DuckDB | Fast local analytics, single file |
| Transform | dbt-duckdb | Industry standard, testable SQL |
| Quality | dbt tests (not_null, unique) | Automated data validation |
| Dashboard | Streamlit + Plotly | Interactive, Python-native |

## How to run

```bash
# 1. Install dependencies
pip install duckdb requests dbt-duckdb streamlit plotly

# 2. Load fresh data
python load_jobs.py

# 3. Transform with dbt
cd bryggja_dbt && dbt run && dbt test

# 4. Launch dashboard
cd .. && streamlit run dashboard.py
```

## What I learned

- How to design a layered data warehouse (raw → staging → mart)
- Writing dbt models with Jinja templating and `{{ ref() }}` dependencies
- Automated data quality testing with dbt schema tests
- Connecting a Python ELT pipeline to a downstream transformation layer
- Building interactive data visualisations with Plotly and Streamlit

## Data source

[Arbetsförmedlingen JobSearch API](https://jobsearch.api.jobtechdev.se) — open Swedish government data, refreshed daily.
