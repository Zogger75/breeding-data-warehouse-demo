"""
Export a data quality report for the Breeding Data Warehouse Demo.

This script performs source-data and warehouse-level validation checks and
writes the results to data/sample_outputs/data_quality_report.csv.

The goal is to provide a reviewer-friendly artifact showing how data quality
rules are evaluated as part of the demo warehouse workflow.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from etl.config import DATABASE_URL, PROJECT_ROOT


RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SAMPLE_OUTPUT_DIR = PROJECT_ROOT / "data" / "sample_outputs"
REPORT_FILE = SAMPLE_OUTPUT_DIR / "data_quality_report.csv"


SOURCE_FILES = {
    "locations": RAW_DATA_DIR / "locations.csv",
    "germplasm": RAW_DATA_DIR / "germplasm.csv",
    "traits": RAW_DATA_DIR / "traits.csv",
    "trials": RAW_DATA_DIR / "trials.csv",
    "observations": RAW_DATA_DIR / "observations.csv",
}


REQUIRED_COLUMNS = {
    "locations": ["location_id", "location_name", "province", "country"],
    "germplasm": ["germplasm_id", "line_name", "line_type", "pedigree"],
    "traits": ["trait_id", "trait_name", "trait_category", "unit", "data_type"],
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


def add_result(
    results: list[dict[str, str]],
    check_name: str,
    status: str,
    details: str,
) -> None:
    """
    Add one data quality check result to the report list.

    Args:
        results: List of report result dictionaries.
        check_name: Name of the data quality check.
        status: PASS, FAIL, or CHECK.
        details: Human-readable check details.
    """
    results.append(
        {
            "check_name": check_name,
            "status": status,
            "details": details,
        }
    )


def read_source_file(file_key: str) -> pd.DataFrame:
    """
    Read a configured raw source CSV file.

    Args:
        file_key: Source file key from SOURCE_FILES.

    Returns:
        Source data as a DataFrame.
    """
    return pd.read_csv(SOURCE_FILES[file_key])


def check_source_files_exist(results: list[dict[str, str]]) -> None:
    """
    Check that all required source files exist.
    """
    for file_key, file_path in SOURCE_FILES.items():
        status = "PASS" if file_path.exists() else "FAIL"
        add_result(
            results,
            f"{file_key}_file_exists",
            status,
            str(file_path),
        )


def check_required_columns(results: list[dict[str, str]]) -> None:
    """
    Check that each source file contains required columns.
    """
    for file_key, required_columns in REQUIRED_COLUMNS.items():
        dataframe = read_source_file(file_key)
        missing_columns = sorted(set(required_columns) - set(dataframe.columns))

        if missing_columns:
            add_result(
                results,
                f"{file_key}_required_columns",
                "FAIL",
                f"Missing columns: {missing_columns}",
            )
        else:
            add_result(
                results,
                f"{file_key}_required_columns",
                "PASS",
                "All required columns are present.",
            )


def check_observation_references(results: list[dict[str, str]]) -> None:
    """
    Check that observation foreign-key-style references exist in source files.
    """
    observations = read_source_file("observations")
    trials = read_source_file("trials")
    germplasm = read_source_file("germplasm")
    traits = read_source_file("traits")

    reference_checks = {
        "observation_trial_ids_are_valid": (
            set(observations["trial_id"]),
            set(trials["trial_id"]),
        ),
        "observation_germplasm_ids_are_valid": (
            set(observations["germplasm_id"]),
            set(germplasm["germplasm_id"]),
        ),
        "observation_trait_ids_are_valid": (
            set(observations["trait_id"]),
            set(traits["trait_id"]),
        ),
    }

    for check_name, (observed_values, valid_values) in reference_checks.items():
        invalid_values = sorted(observed_values - valid_values)

        if invalid_values:
            add_result(
                results,
                check_name,
                "FAIL",
                f"Invalid references found: {invalid_values}",
            )
        else:
            add_result(
                results,
                check_name,
                "PASS",
                "All references are valid.",
            )


def check_yield_values(results: list[dict[str, str]]) -> None:
    """
    Check that yield values are numeric and non-negative.
    """
    observations = read_source_file("observations")
    yield_rows = observations[observations["trait_id"] == "T001"].copy()

    yield_rows["numeric_value"] = pd.to_numeric(
        yield_rows["raw_value"],
        errors="coerce",
    )

    non_numeric_count = int(yield_rows["numeric_value"].isna().sum())
    negative_count = int((yield_rows["numeric_value"] < 0).sum())

    if non_numeric_count == 0 and negative_count == 0:
        add_result(
            results,
            "yield_values_are_numeric_and_non_negative",
            "PASS",
            f"Checked {len(yield_rows)} yield observations.",
        )
    else:
        add_result(
            results,
            "yield_values_are_numeric_and_non_negative",
            "FAIL",
            f"Non-numeric values: {non_numeric_count}; negative values: {negative_count}",
        )


def get_table_count(table_name: str) -> int:
    """
    Return row count for a warehouse table.

    Args:
        table_name: Warehouse table name.

    Returns:
        Number of rows in the table.
    """
    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        count = connection.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar_one()

    return int(count)


def check_warehouse_counts(results: list[dict[str, str]]) -> None:
    """
    Check that core warehouse tables contain expected row counts.
    """
    expected_counts = {
        "dim_location": 5,
        "dim_germplasm": 8,
        "dim_trait": 7,
        "dim_trial": 5,
        "fact_observation": 40,
    }

    for table_name, expected_count in expected_counts.items():
        actual_count = get_table_count(table_name)
        status = "PASS" if actual_count == expected_count else "CHECK"

        add_result(
            results,
            f"{table_name}_row_count",
            status,
            f"Expected {expected_count}; actual {actual_count}.",
        )


def export_data_quality_report() -> None:
    """
    Run all data quality checks and export the report to CSV.
    """
    results: list[dict[str, str]] = []

    check_source_files_exist(results)
    check_required_columns(results)
    check_observation_references(results)
    check_yield_values(results)
    check_warehouse_counts(results)

    SAMPLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    report = pd.DataFrame(results)
    report.to_csv(REPORT_FILE, index=False)

    print(f"Exported {len(report)} data quality checks to {REPORT_FILE}")


def main() -> None:
    """
    Script entry point.
    """
    print("Exporting data quality report...")
    export_data_quality_report()
    print("Data quality report export completed successfully.")


if __name__ == "__main__":
    main()