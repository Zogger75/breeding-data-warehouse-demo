# Breeding Data Warehouse Demo

A portfolio project demonstrating how raw crop breeding trial data can be transformed into an analytics-ready data warehouse.

## Project Goals

This project demonstrates:

- Extracting raw breeding trial data from CSV files
- Cleaning and validating trial, location, germplasm, trait, and observation data
- Loading data into a PostgreSQL warehouse
- Modeling breeding data using dimension and fact tables
- Creating SQL views for reporting and analytics

## Planned Warehouse Model

The demo warehouse will use a simple star schema:

- `dim_trial`
- `dim_location`
- `dim_germplasm`
- `dim_trait`
- `fact_observation`

## Project Structure

```text
data/         Raw, processed, and sample output data
database/     SQL schema and seed scripts
etl/          Python ETL pipeline
analytics/    SQL analysis queries and reporting views
docs/         Architecture notes, screenshots, and documentation
tests/        Data quality and transformation tests