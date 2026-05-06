"""
Load module for the Breeding Data Warehouse Demo.

This module loads transformed breeding trial data into staging, dimension,
and fact tables using SQLAlchemy. The current implementation supports a
no-admin SQLite demo mode and is structured so PostgreSQL support can be
added later with minimal changes.
"""

import pandas as pd
from sqlalchemy import Engine, create_engine, text


def create_database_engine(database_url: str) -> Engine:
    """
    Create a SQLAlchemy database engine.

    Args:
        database_url: SQLAlchemy-compatible database connection string.

    Returns:
        SQLAlchemy Engine.
    """
    return create_engine(database_url)


def initialize_sqlite_schema(engine: Engine) -> None:
    """
    Create SQLite-compatible warehouse tables and views.

    Args:
        engine: SQLAlchemy database engine.
    """
    statements = [
        "DROP VIEW IF EXISTS vw_top_yielding_lines;",
        "DROP VIEW IF EXISTS vw_trial_completeness;",
        "DROP VIEW IF EXISTS vw_germplasm_performance;",
        "DROP VIEW IF EXISTS vw_trait_summary_by_location;",
        "DROP VIEW IF EXISTS vw_observation_detail;",
        "DROP TABLE IF EXISTS fact_observation;",
        "DROP TABLE IF EXISTS dim_trial;",
        "DROP TABLE IF EXISTS dim_trait;",
        "DROP TABLE IF EXISTS dim_germplasm;",
        "DROP TABLE IF EXISTS dim_location;",
        "DROP TABLE IF EXISTS stg_observations;",
        "DROP TABLE IF EXISTS stg_trials;",
        "DROP TABLE IF EXISTS stg_traits;",
        "DROP TABLE IF EXISTS stg_germplasm;",
        "DROP TABLE IF EXISTS stg_locations;",
        """
        CREATE TABLE stg_locations (
            location_id TEXT PRIMARY KEY,
            location_name TEXT NOT NULL,
            province TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL
        );
        """,
        """
        CREATE TABLE stg_germplasm (
            germplasm_id TEXT PRIMARY KEY,
            line_name TEXT NOT NULL,
            line_type TEXT,
            pedigree TEXT
        );
        """,
        """
        CREATE TABLE stg_traits (
            trait_id TEXT PRIMARY KEY,
            trait_name TEXT NOT NULL,
            trait_category TEXT,
            unit TEXT,
            data_type TEXT
        );
        """,
        """
        CREATE TABLE stg_trials (
            trial_id TEXT PRIMARY KEY,
            trial_name TEXT NOT NULL,
            crop TEXT,
            trial_year INTEGER,
            location_id TEXT,
            design TEXT,
            rep_count INTEGER
        );
        """,
        """
        CREATE TABLE stg_observations (
            observation_id TEXT PRIMARY KEY,
            trial_id TEXT NOT NULL,
            germplasm_id TEXT NOT NULL,
            trait_id TEXT NOT NULL,
            rep INTEGER,
            block INTEGER,
            plot TEXT,
            raw_value TEXT
        );
        """,
        """
        CREATE TABLE dim_location (
            location_key INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id TEXT UNIQUE NOT NULL,
            location_name TEXT NOT NULL,
            province TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL
        );
        """,
        """
        CREATE TABLE dim_germplasm (
            germplasm_key INTEGER PRIMARY KEY AUTOINCREMENT,
            germplasm_id TEXT UNIQUE NOT NULL,
            line_name TEXT NOT NULL,
            line_type TEXT,
            pedigree TEXT
        );
        """,
        """
        CREATE TABLE dim_trait (
            trait_key INTEGER PRIMARY KEY AUTOINCREMENT,
            trait_id TEXT UNIQUE NOT NULL,
            trait_name TEXT NOT NULL,
            trait_category TEXT,
            unit TEXT,
            data_type TEXT
        );
        """,
        """
        CREATE TABLE dim_trial (
            trial_key INTEGER PRIMARY KEY AUTOINCREMENT,
            trial_id TEXT UNIQUE NOT NULL,
            trial_name TEXT NOT NULL,
            crop TEXT,
            trial_year INTEGER,
            location_id TEXT,
            design TEXT,
            rep_count INTEGER
        );
        """,
        """
        CREATE TABLE fact_observation (
            observation_key INTEGER PRIMARY KEY AUTOINCREMENT,
            observation_id TEXT UNIQUE NOT NULL,
            trial_key INTEGER NOT NULL,
            location_key INTEGER NOT NULL,
            germplasm_key INTEGER NOT NULL,
            trait_key INTEGER NOT NULL,
            trial_year INTEGER,
            rep INTEGER,
            block INTEGER,
            plot TEXT,
            raw_value TEXT,
            numeric_value REAL,
            source_system TEXT DEFAULT 'CSV Demo Source',
            load_timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def load_staging_tables(
    engine: Engine,
    transformed_data: dict[str, pd.DataFrame],
) -> None:
    """
    Load transformed source data into staging tables.
    """
    table_map = {
        "locations": "stg_locations",
        "germplasm": "stg_germplasm",
        "traits": "stg_traits",
        "trials": "stg_trials",
        "observations": "stg_observations",
    }

    for source_name, table_name in table_map.items():
        dataframe = transformed_data[source_name].copy()

        if source_name == "observations" and "numeric_value" in dataframe.columns:
            dataframe = dataframe.drop(columns=["numeric_value"])

        dataframe.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
        )


def load_dimension_tables(engine: Engine) -> None:
    """
    Load warehouse dimension tables from staging tables.
    """
    statements = [
        """
        INSERT OR IGNORE INTO dim_location
        SELECT NULL, location_id, location_name, province, country, latitude, longitude
        FROM stg_locations;
        """,
        """
        INSERT OR IGNORE INTO dim_germplasm
        SELECT NULL, germplasm_id, line_name, line_type, pedigree
        FROM stg_germplasm;
        """,
        """
        INSERT OR IGNORE INTO dim_trait
        SELECT NULL, trait_id, trait_name, trait_category, unit, data_type
        FROM stg_traits;
        """,
        """
        INSERT OR IGNORE INTO dim_trial
        SELECT NULL, trial_id, trial_name, crop, trial_year, location_id, design, rep_count
        FROM stg_trials;
        """,
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def load_fact_observation(engine: Engine) -> None:
    """
    Load the fact_observation table by joining staging observations to dimensions.
    """
    statement = """
    INSERT OR IGNORE INTO fact_observation (
        observation_id,
        trial_key,
        location_key,
        germplasm_key,
        trait_key,
        trial_year,
        rep,
        block,
        plot,
        raw_value,
        numeric_value
    )
    SELECT
        so.observation_id,
        dt.trial_key,
        dl.location_key,
        dg.germplasm_key,
        dtr.trait_key,
        dt.trial_year,
        so.rep,
        so.block,
        so.plot,
        so.raw_value,
        CAST(so.raw_value AS REAL)
    FROM stg_observations so
    JOIN dim_trial dt
        ON so.trial_id = dt.trial_id
    JOIN dim_location dl
        ON dt.location_id = dl.location_id
    JOIN dim_germplasm dg
        ON so.germplasm_id = dg.germplasm_id
    JOIN dim_trait dtr
        ON so.trait_id = dtr.trait_id;
    """

    with engine.begin() as connection:
        connection.execute(text(statement))


def create_reporting_views(engine: Engine) -> None:
    """
    Create SQLite-compatible analytics views.
    """
    statements = [
        """
        CREATE VIEW vw_observation_detail AS
        SELECT
            fo.observation_id,
            dt.trial_id,
            dt.trial_name,
            dt.crop,
            dt.trial_year,
            dl.location_name,
            dl.province,
            dg.germplasm_id,
            dg.line_name,
            dg.line_type,
            dtr.trait_id,
            dtr.trait_name,
            dtr.trait_category,
            dtr.unit,
            fo.rep,
            fo.block,
            fo.plot,
            fo.raw_value,
            fo.numeric_value,
            fo.load_timestamp
        FROM fact_observation fo
        JOIN dim_trial dt ON fo.trial_key = dt.trial_key
        JOIN dim_location dl ON fo.location_key = dl.location_key
        JOIN dim_germplasm dg ON fo.germplasm_key = dg.germplasm_key
        JOIN dim_trait dtr ON fo.trait_key = dtr.trait_key;
        """,
        """
        CREATE VIEW vw_trait_summary_by_location AS
        SELECT
            trial_year,
            location_name,
            trait_name,
            unit,
            COUNT(*) AS observation_count,
            ROUND(AVG(numeric_value), 2) AS avg_value,
            ROUND(MIN(numeric_value), 2) AS min_value,
            ROUND(MAX(numeric_value), 2) AS max_value
        FROM vw_observation_detail
        WHERE numeric_value IS NOT NULL
        GROUP BY trial_year, location_name, trait_name, unit;
        """,
        """
        CREATE VIEW vw_germplasm_performance AS
        SELECT
            germplasm_id,
            line_name,
            line_type,
            trait_name,
            unit,
            COUNT(*) AS observation_count,
            ROUND(AVG(numeric_value), 2) AS avg_value,
            ROUND(MIN(numeric_value), 2) AS min_value,
            ROUND(MAX(numeric_value), 2) AS max_value
        FROM vw_observation_detail
        WHERE numeric_value IS NOT NULL
        GROUP BY germplasm_id, line_name, line_type, trait_name, unit;
        """,
        """
        CREATE VIEW vw_trial_completeness AS
        SELECT
            trial_id,
            trial_name,
            location_name,
            trial_year,
            COUNT(*) AS observation_count,
            COUNT(DISTINCT germplasm_id) AS germplasm_count,
            COUNT(DISTINCT trait_id) AS trait_count,
            COUNT(DISTINCT plot) AS plot_count
        FROM vw_observation_detail
        GROUP BY trial_id, trial_name, location_name, trial_year;
        """,
        """
        CREATE VIEW vw_top_yielding_lines AS
        SELECT
            germplasm_id,
            line_name,
            line_type,
            COUNT(*) AS yield_observation_count,
            ROUND(AVG(numeric_value), 2) AS avg_yield_kg_ha
        FROM vw_observation_detail
        WHERE trait_name = 'Yield'
          AND numeric_value IS NOT NULL
        GROUP BY germplasm_id, line_name, line_type
        ORDER BY avg_yield_kg_ha DESC;
        """,
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))