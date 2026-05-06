"""
Extract module for the Breeding Data Warehouse Demo.

This module reads raw CSV files from data/raw/ and returns pandas DataFrames.
It represents the "extract" phase of the ETL pipeline.
"""

from pathlib import Path

import pandas as pd


def read_csv_file(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the file contents.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")

    return pd.read_csv(file_path)


def extract_source_data(source_files: dict[str, Path]) -> dict[str, pd.DataFrame]:
    """
    Extract all configured source CSV files.

    Args:
        source_files: Dictionary mapping source names to file paths.

    Returns:
        Dictionary mapping source names to DataFrames.
    """
    extracted_data = {}

    for source_name, file_path in source_files.items():
        extracted_data[source_name] = read_csv_file(file_path)

    return extracted_data