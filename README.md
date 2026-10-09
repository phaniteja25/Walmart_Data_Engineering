# Walmart Data Engineering

End-to-end retail data pipeline: raw CSVs → Postgres (Neon) → CDC ingestion into Databricks → dbt medallion layers (silver technical, silver business, gold dims/fact) → orchestrated by Airflow running in Docker.

## Project layout

```
walmart_dataset/        Source CSVs + DDL for the raw Postgres schema
scripts/                load_raw.data.py – loads CSVs into Postgres `raw.*` tables
Walmart_dbt/            dbt project (walmart_proj_dbt) for local development
airflow-docker/         Airflow (Docker Compose) + DAGs + the dbt project it runs
  dags/orchestrator.py  CDC job → source freshness → silver_t → silver_b → gold
```

## Prerequisites

- Python 3.12 and [uv](https://docs.astral.sh/uv/)
- Docker Desktop
- A Postgres database (e.g. Neon) and a Databricks workspace with a SQL warehouse, a personal access token, and a CDC ingestion job

## 1. Clone and configure secrets

```bash
git clone <this-repo-url>
cd Walmart_Data_Engineering

cp .env.example .env                                # fill in your values
cp airflow-docker/.env.example airflow-docker/.env  # fill in your values
```

Secrets are only read from these `.env` files, which are git-ignored.

## 2. Load raw data into Postgres

```bash
uv sync                                  # creates .venv from uv.lock
set -a && source .env && set +a
psql "$WALMART_DB_URL" -f walmart_dataset/ddl/walmart_schema.sql
uv run python scripts/load_raw.data.py
```

## 3. Run dbt locally (optional)

```bash
set -a && source .env && set +a
cd Walmart_dbt/walmart_proj_dbt
uv run dbt debug --profiles-dir .
uv run dbt build --profiles-dir .
```

## 4. Run the pipeline in Airflow

```bash
cd airflow-docker
docker compose up airflow-init
docker compose up -d --build
```

Open http://localhost:8080 (login `airflow` / `airflow`), unpause the **orchestrator** DAG and trigger it.

Stop with `docker compose down` (add `-v` to wipe the Airflow metadata DB).
