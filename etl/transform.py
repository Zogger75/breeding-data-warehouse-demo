"""
Transform module for the Breeding Data Warehouse Demo.

This module cleans, validates, and prepares raw breeding trial data for loading
into staging and warehouse tables.
"""

import pandas as pd


REQUIRED_COLUMNS = {
    "locations": [
        "location_id",
        "location_name",
        "province",
        "country",
        "latitude",
        "longitude",
    ],
    "germplasm": [
        "germplasm_id",
        "line_name",
        "line_type",
        "pedigree",
    ],
    "traits": [
        "trait_id",
        "trait_name",
        "trait_category",
        "unit",
        "data_type",
    ],
    "trials": [
        "trial_id",
        "trial_name",
        "crop",
        "trial_year",
        "location_id",
        "design",
        "rep_count",
    ],
    "observations": [
        "observation_id",
        "trial_id",
        "germplasm_id",
        "trait_id",
        "rep",
        "block",
        "plot",
        "raw_value",
    ],
}


def validate_required_columns(
    source_name: str,
    dataframe: pd.DataFrame,
    required_columns: list[str],
) -> None:
    """
    Validate that a DataFrame contains all required columns.

    Args:
        source_name: Name of the source dataset.
        dataframe: DataFrame to validate.
        required_columns: Required column names.

    Raises:
        ValueError: If required columns are missing.
    """
    missing_columns = sorted(set(required_columns) - set(dataframe.columns))

    if missing_columns:
        raise ValueError(
            f"{source_name} is missing required columns: {missing_columns}"
        )


def clean_text_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Trim leading and trailing whitespace from text columns.

    Args:
        dataframe: DataFrame to clean.

    Returns:
        Cleaned DataFrame.
    """
    cleaned = dataframe.copy()

    for column in cleaned.select_dtypes(include=["object"]).columns:
        cleaned[column] = cleaned[column].astype(str).str.strip()

    return cleaned


def transform_source_data(
    extracted_data: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """
    Transform all extracted source datasets.

    Args:
        extracted_data: Dictionary of raw source DataFrames.

    Returns:
        Dictionary of cleaned and validated DataFrames.
    """
    transformed_data = {}

    for source_name, dataframe in extracted_data.items():
        validate_required_columns(
            source_name=source_name,
            dataframe=dataframe,
            required_columns=REQUIRED_COLUMNS[source_name],
        )

        transformed_data[source_name] = clean_text_columns(dataframe)

    transformed_data["observations"]["numeric_value"] = pd.to_numeric(
        transformed_data["observations"]["raw_value"],
        errors="coerce",
    )

    return transformed_data