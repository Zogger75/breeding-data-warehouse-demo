"""
Main ETL pipeline runner for the Breeding Data Warehouse Demo.

Pipeline steps:
1. Extract raw CSV files from data/raw/
2. Validate and transform source data
3. Initialize the local warehouse schema
4. Load staging tables
5. Load warehouse dimension tables
6. Load warehouse fact tables
7. Create reporting views
"""

from etl.config import DATABASE_URL, PROCESSED_DATA_DIR, SOURCE_FILES
from etl.extract import extract_source_data
from etl.load import (
    create_database_engine,
    create_reporting_views,
    initialize_sqlite_schema,
    load_dimension_tables,
    load_fact_observation,
    load_staging_tables,
)
from etl.transform import transform_source_data


def main() -> None:
    """
    Run the complete ETL pipeline.
    """
    print("Starting Breeding Data Warehouse ETL pipeline...")

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Creating database connection...")
    engine = create_database_engine(DATABASE_URL)

    print("Extracting source data...")
    extracted_data = extract_source_data(SOURCE_FILES)

    print("Transforming source data...")
    transformed_data = transform_source_data(extracted_data)

    print("Initializing local warehouse schema...")
    initialize_sqlite_schema(engine)

    print("Loading staging tables...")
    load_staging_tables(engine, transformed_data)

    print("Loading dimension tables...")
    load_dimension_tables(engine)

    print("Loading fact table...")
    load_fact_observation(engine)

    print("Creating reporting views...")
    create_reporting_views(engine)

    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()