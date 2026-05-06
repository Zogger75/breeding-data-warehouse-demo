"""
Export sample analytics outputs for the Breeding Data Warehouse Demo.

This script reads reporting views from the local warehouse and exports
reviewer-friendly CSV files into data/sample_outputs/.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from etl.config import DATABASE_URL, PROJECT_ROOT


SAMPLE_OUTPUT_DIR = PROJECT_ROOT / "data" / "sample_outputs"

OUTPUT_QUERIES = {
    "top_yielding_lines.csv": """
        SELECT *
        FROM vw_top_yielding_lines;
    """,
    "trial_completeness.csv": """
        SELECT *
        FROM vw_trial_completeness
        ORDER BY trial_id;
    """,
    "trait_summary_by_location.csv": """
        SELECT *
        FROM vw_trait_summary_by_location
        ORDER BY trial_year, location_name, trait_name;
    """,
    "germplasm_performance.csv": """
        SELECT *
        FROM vw_germplasm_performance
        ORDER BY trait_name, avg_value DESC;
    """,
}


def export_query_to_csv(output_file: Path, query: str) -> None:
    """
    Export a SQL query result to a CSV file.

    Args:
        output_file: Destination CSV file path.
        query: SQL query to execute.
    """
    engine = create_engine(DATABASE_URL)

    dataframe = pd.read_sql_query(query, engine)
    dataframe.to_csv(output_file, index=False)

    print(f"Exported {len(dataframe)} rows to {output_file}")


def main() -> None:
    """
    Export all configured sample analytics outputs.
    """
    print("Exporting sample analytics outputs...")

    SAMPLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for file_name, query in OUTPUT_QUERIES.items():
        output_file = SAMPLE_OUTPUT_DIR / file_name
        export_query_to_csv(output_file, query)

    print("Sample analytics export completed successfully.")


if __name__ == "__main__":
    main()