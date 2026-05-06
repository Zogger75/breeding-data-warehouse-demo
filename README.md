# Breeding Data Warehouse Demo

![Python Tests](https://github.com/Zogger75/breeding-data-warehouse-demo/actions/workflows/python-tests.yml/badge.svg)

A portfolio data engineering project demonstrating how raw crop breeding trial data can be transformed into an analytics-ready warehouse.

The project uses realistic wheat breeding trial data to show:

- CSV data ingestion
- Data validation
- ETL pipeline design
- Staging tables
- Dimensional modeling
- Fact and dimension tables
- Analytics-ready SQL views
- SQLite local demo mode
- Exported sample reporting outputs
- Data quality reporting
- Power BI dashboard reporting

## Business Context

Crop breeding programs collect trial data across locations, years, germplasm lines, traits, plots, replications, and experimental designs.

This demo shows how raw breeding trial exports can be standardized into a warehouse structure that supports reporting, analytics, quality checks, and downstream decision-making.

Example questions supported by the warehouse:

- Which breeding lines had the highest average yield?
- How complete is the trial data by location?
- What traits were collected at each site?
- How does germplasm performance vary across traits and environments?
- Did the source data and warehouse outputs pass validation checks?

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
   |
   v
Power BI dashboard
```

More detail is available in:

```text
docs/architecture.md
docs/data_dictionary.md
docs/local_demo_setup.md
```

## Project Structure

```text
breeding-data-warehouse-demo/
|
|-- .github/
|   `-- workflows/        GitHub Actions test workflow
|
|-- analytics/            Validation and output export scripts
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
|-- docs/                 Project documentation
|
|-- etl/                  Python ETL pipeline
|
|-- powerbi/
|   |-- screenshots/      Dashboard screenshots for GitHub preview
|   `-- breeding_data_warehouse_dashboard.pbix
|
`-- tests/                Data quality and transformation tests
```

## Source Data

The demo uses sample wheat breeding trial CSV files:

```text
data/raw/locations.csv
data/raw/germplasm.csv
data/raw/traits.csv
data/raw/trials.csv
data/raw/observations.csv
```

The source data includes:

- Trial locations
- Germplasm lines
- Trait definitions
- Trial metadata
- Plot-level observations

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
- GitHub Actions
- Power BI

## Local Demo Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The local demo uses SQLite by default. The SQLite database is created automatically when the ETL pipeline runs.

## Environment Settings

The project includes an example environment file:

```text
.env.example
```

For local SQLite demo mode:

```env
DATABASE_URL=sqlite:///data/processed/breeding_dw_demo.sqlite
```

For PostgreSQL mode, update the connection string when PostgreSQL is available:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/breeding_dw_demo
```

Do not commit your local `.env` file.

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

Expected core warehouse counts:

```text
dim_location: 5
dim_germplasm: 8
dim_trait: 7
dim_trial: 5
fact_observation: 40
```

## Export Sample Analytics Outputs

```bash
python -m analytics.export_sample_outputs
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

## Export Data Quality Report

```bash
python -m analytics.export_data_quality_report
```

This creates:

```text
data/sample_outputs/data_quality_report.csv
```

The data quality report includes checks for:

- Source file presence
- Required columns
- Valid observation references
- Numeric and non-negative yield values
- Expected warehouse row counts

## Run Tests

```bash
python -m pytest
```

The tests validate source file presence, required columns, valid references, and basic trait value rules.

The GitHub Actions workflow also runs these tests automatically on push and pull request events.

## Power BI Dashboard

This project includes a Power BI report built from the exported warehouse analytics outputs.

The dashboard demonstrates how the warehouse can support reporting for trial completeness, germplasm performance, yield summaries, trait summaries by location, and data quality monitoring.

Power BI file:

```text
powerbi/breeding_data_warehouse_dashboard.pbix
```

Dashboard pages:

- Executive Summary
- Data Quality
- Germplasm Performance
- Trait Summary by Location

### Executive Summary

The Executive Summary page provides a high-level view of the demo warehouse, including total observations, trials, locations, germplasm lines, top yielding wheat lines, and trial completeness.

![Executive Summary](powerbi/screenshots/executive_summary.png)

### Data Quality

The Data Quality page summarizes validation checks across source files, references, numeric values, and warehouse row counts.

![Data Quality](powerbi/screenshots/data_quality.png)

### Germplasm Performance

The Germplasm Performance page allows users to compare average trait values by germplasm line and filter by selected trait.

![Germplasm Performance](powerbi/screenshots/germplasm_performance.png)

### Trait Summary by Location

The Trait Summary by Location page summarizes average trait values by trial location and supports filtering by trait.

![Trait Summary by Location](powerbi/screenshots/trait_summary_by_location.png)

## PostgreSQL Schema Scripts

PostgreSQL-compatible schema scripts are included under:

```text
database/schema/
```

Scripts:

- `01_create_staging_tables.sql`
- `02_create_dimension_tables.sql`
- `03_create_fact_tables.sql`
- `04_create_views.sql`

The local runnable demo currently uses SQLite for no-admin setup convenience. The PostgreSQL scripts demonstrate how the same warehouse model could be deployed to a production-style relational database.

## Portfolio Notes

This project is designed to demonstrate data engineering and solution architecture skills using an agricultural research domain.

It highlights:

- Domain-aware data modeling
- ETL pipeline organization
- Data quality testing
- Analytics-ready warehouse design
- Reviewer-friendly local execution
- Automated testing with GitHub Actions
- Professional documentation
- Dashboard reporting with Power BI

## Future Enhancements

Potential future enhancements:

- PostgreSQL deployment mode
- Docker-based setup
- dbt model layer
- Larger multi-year sample dataset
- Power BI publishing workflow
- Additional data quality reports
- Pedigree relationship fact tables
- Multi-environment trial analysis
- Trait correlation analysis
- GitHub Actions workflow that runs the ETL and validates warehouse output
