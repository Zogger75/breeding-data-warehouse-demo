# Architecture Overview

## Purpose

The Breeding Data Warehouse Demo shows how raw crop breeding trial data can be transformed into an analytics-ready warehouse.

The project demonstrates a simplified version of a real breeding data workflow, including:

- Raw trial data ingestion
- Data validation
- Staging tables
- Dimensional modeling
- Fact table loading
- Analytics-ready SQL views

## Source Data

Raw CSV files are stored in `data/raw/`.

Current source files:

- `locations.csv`
- `germplasm.csv`
- `traits.csv`
- `trials.csv`
- `observations.csv`

## ETL Flow

```text
CSV files
   â†“
Extract with pandas
   â†“
Validate and clean source data
   â†“
Load PostgreSQL staging tables
   â†“
Load warehouse dimension tables
   â†“
Load fact_observation
   â†“
Expose analytics views
```

## Warehouse Model

The warehouse uses a star schema.

Dimension tables:

- `dim_location`
- `dim_germplasm`
- `dim_trait`
- `dim_trial`

Fact table:

- `fact_observation`

## Analytics Layer

SQL views provide reporting-ready datasets for:

- Observation detail
- Trait summaries by location
- Germplasm performance
- Trial completeness
- Top-yielding lines

## Design Notes

This demo intentionally keeps the schema small and readable. In a production breeding data warehouse, additional dimensions would likely include:

- Season
- Program
- Nursery
- Study type
- Experimental design
- Observation unit
- Trial management metadata

## Repository Layout

```text
## Repository Layout

```text
breeding-data-warehouse-demo/
|
|-- data/
|   |-- raw/              Source CSV files
|   |-- processed/        Cleaned or exported datasets
|   `-- sample_outputs/   Example outputs for documentation
|
|-- database/
|   |-- schema/           PostgreSQL schema scripts
|   `-- seed/             Optional seed/load scripts
|
|-- etl/                  Python ETL pipeline
|
|-- analytics/
|   `-- sql/              Analysis and reporting SQL queries
|
|-- docs/                 Project documentation
|
`-- tests/                Data quality and transformation tests

## Pipeline Responsibilities

The ETL pipeline is divided into small modules:

| Module | Responsibility |
|---|---|
| `config.py` | Centralizes paths and database connection settings |
| `extract.py` | Reads raw CSV source files |
| `transform.py` | Validates required columns, trims text fields, and prepares numeric values |
| `load.py` | Loads staging, dimension, and fact tables |
| `run_pipeline.py` | Runs the full ETL process from start to finish |

## Data Modeling Approach

The project uses a dimensional model because it is easy to understand, query, and connect to reporting tools.

The central table is `fact_observation`, which stores plot-level trait observations. Each observation links to descriptive dimensions for trial, location, germplasm, and trait.

This structure supports common breeding analytics questions such as:

- Which lines performed best for yield?
- How does trait performance vary by location?
- Which trials have incomplete observations?
- Which germplasm lines have data across multiple environments?
- What traits were collected for each trial?

## Future Enhancements

Potential future additions include:

- Docker-based PostgreSQL setup
- Automated data quality report
- Power BI dashboard
- dbt models
- CI workflow with GitHub Actions
- Slowly changing dimensions
- Additional fact tables for trial metadata, genotype calls, and pedigree relationships
