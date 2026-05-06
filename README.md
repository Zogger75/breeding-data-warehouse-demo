# Breeding Data Warehouse Demo

![Python Tests](https://github.com/Zogger75/breeding-data-warehouse-demo/actions/workflows/python-tests.yml/badge.svg)

A portfolio data engineering project demonstrating how raw crop breeding trial data can be transformed into an analytics-ready warehouse.The project uses realistic wheat breeding trial data to show:

- CSV data ingestion
- Data validation
- ETL pipeline design
- Staging tables
- Dimensional modeling
- Fact and dimension tables
- Analytics-ready SQL views
- SQLite local demo mode
- Exported sample reporting outputs

## Business Context

Crop breeding programs collect large volumes of trial data across locations, years, germplasm lines, traits, plots, replications, and experimental designs.

This demo shows how raw trial exports can be standardized into a warehouse structure that supports reporting, analytics, and downstream decision-making.

Example questions supported by the warehouse:

- Which breeding lines had the highest average yield?
- How complete is the trial data by location?
- What traits were collected at each site?
- How does germplasm performance vary across traits and environments?

## Architecture

The project follows a simple ETL and warehouse flow:

```text
Raw CSV files
   |
   v
Python ETL pipeline
   |
   v
SQLite local demo warehouse
   |
   v
Staging tables
   |
   v
Dimension and fact tables
   |
   v
Reporting views
   |
   v
Sample analytics CSV outputs
```

## Project Structure

```text
breeding-data-warehouse-demo/
|
|-- data/
|   |-- raw/              Source CSV files
|   |-- processed/        Local SQLite database output
|   `-- sample_outputs/   Exported analytics CSVs
|
|-- database/
|   |-- schema/           PostgreSQL schema scripts
|   `-- seed/             Optional seed/load scripts
|
|-- etl/                  Python ETL pipeline
|
|-- analytics/            Validation and output export scripts
|
|-- docs/                 Project documentation
|
`-- tests/                Data quality and transformation tests
```

## Local Demo Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the ETL Pipeline

```bash
python -m etl.run_pipeline
```

This creates a local SQLite warehouse at:

```text
data/processed/breeding_dw_demo.sqlite
```

## Validate the Warehouse

```bash
python -m analytics.validate_warehouse
```

This prints expected versus actual row counts and sample analytics results.

## Export Sample Outputs

```bash
python -m analytics.export_sample_outputs
python -m analytics.export_data_quality_report
```

This creates reviewer-friendly CSV files in:

```text
data/sample_outputs/
```

Current sample outputs include:

- `top_yielding_lines.csv`
- `trial_completeness.csv`
- `trait_summary_by_location.csv`
- `germplasm_performance.csv`
- 'data_quality_report.csv'

## Run Tests

```bash
python -m pytest
```

The tests validate source file presence, required columns, valid references, and basic trait value rules.

## Warehouse Model

The demo uses a simple star schema.

Dimension tables:

- `dim_location`
- `dim_germplasm`
- `dim_trait`
- `dim_trial`

Fact table:

- `fact_observation`

Reporting views:

- `vw_observation_detail`
- `vw_trait_summary_by_location`
- `vw_germplasm_performance`
- `vw_trial_completeness`
- `vw_top_yielding_lines`

## Technology Stack

- Python
- pandas
- SQLAlchemy
- SQLite
- PostgreSQL-compatible schema scripts
- pytest

## Portfolio Notes

This project is designed to demonstrate data engineering and solution architecture skills using an agricultural research domain.

It highlights:

- Domain-aware data modeling
- ETL pipeline organization
- Data quality testing
- Analytics-ready warehouse design
- Reviewer-friendly local execution
- Professional documentation

## Future Enhancements

Planned or potential enhancements:

- PostgreSQL deployment mode
- Docker-based setup
- Power BI dashboard
- dbt model layer
- GitHub Actions CI workflow
- Additional data quality reports
- Pedigree relationship fact tables
- Multi-year and multi-environment trial expansion
