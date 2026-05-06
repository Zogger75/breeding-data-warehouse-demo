"""
Load module for the Breeding Data Warehouse Demo.

This module loads transformed breeding trial data into PostgreSQL staging,
dimension, and fact tables.
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


def load_staging_tables(
    engine: Engine,
    transformed_data: dict[str, pd.DataFrame],
) -> None:
    """
    Load transformed source data into staging tables.

    Args:
        engine: SQLAlchemy database engine.
        transformed_data: Dictionary of transformed DataFrames.
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

    Args:
        engine: SQLAlchemy database engine.
    """
    statements = [
        """
        INSERT INTO dim_location (
            location_id,
            location_name,
            province,
            country,
            latitude,
            longitude
        )
        SELECT
            location_id,
            location_name,
            province,
            country,
            latitude,
            longitude
        FROM stg_locations
        ON CONFLICT (location_id) DO NOTHING;
        """,
        """
        INSERT INTO dim_germplasm (
            germplasm_id,
            line_name,
            line_type,
            pedigree
        )
        SELECT
            germplasm_id,
            line_name,
            line_type,
            pedigree
        FROM stg_germplasm
        ON CONFLICT (germplasm_id) DO NOTHING;
        """,
        """
        INSERT INTO dim_trait (
            trait_id,
            trait_name,
            trait_category,
            unit,
            data_type
        )
        SELECT
            trait_id,
            trait_name,
            trait_category,
            unit,
            data_type
        FROM stg_traits
        ON CONFLICT (trait_id) DO NOTHING;
        """,
        """
        INSERT INTO dim_trial (
            trial_id,
            trial_name,
            crop,
            trial_year,
            location_id,
            design,
            rep_count
        )
        SELECT
            trial_id,
            trial_name,
            crop,
            trial_year,
            location_id,
            design,
            rep_count
        FROM stg_trials
        ON CONFLICT (trial_id) DO NOTHING;
        """,
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def load_fact_observation(engine: Engine) -> None:
    """
    Load the fact_observation table by joining staging observations to dimensions.

    Args:
        engine: SQLAlchemy database engine.
    """
    statement = """
    INSERT INTO fact_observation (
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
        NULLIF(so.raw_value, '')::NUMERIC
    FROM stg_observations so
    JOIN dim_trial dt
        ON so.trial_id = dt.trial_id
    JOIN dim_location dl
        ON dt.location_id = dl.location_id
    JOIN dim_germplasm dg
        ON so.germplasm_id = dg.germplasm_id
    JOIN dim_trait dtr
        ON so.trait_id = dtr.trait_id
    ON CONFLICT (observation_id) DO NOTHING;
    """

    with engine.begin() as connection:
        connection.execute(text(statement))


def clear_staging_tables(engine: Engine) -> None:
    """
    Clear staging tables before loading fresh source data.

    Args:
        engine: SQLAlchemy database engine.
    """
    statement = """
    TRUNCATE TABLE
        stg_observations,
        stg_trials,
        stg_traits,
        stg_germplasm,
        stg_locations;
    """

    with engine.begin() as connection:
        connection.execute(text(statement))