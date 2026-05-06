"""
Warehouse validation script for the Breeding Data Warehouse Demo.

This script connects to the configured warehouse database and prints basic
validation checks and sample analytics results. It helps reviewers confirm
that the ETL pipeline loaded the expected data.
"""

from sqlalchemy import create_engine, text

from etl.config import DATABASE_URL


EXPECTED_TABLE_COUNTS = {
    "dim_location": 5,
    "dim_germplasm": 8,
    "dim_trait": 7,
    "dim_trial": 5,
    "fact_observation": 40,
}


def get_table_count(table_name: str) -> int:
    """
    Return the number of rows in a warehouse table.

    Args:
        table_name: Name of the table to count.

    Returns:
        Number of rows in the table.
    """
    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        result = connection.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar_one()

    return int(result)


def print_table_counts() -> None:
    """
    Print expected and actual row counts for core warehouse tables.
    """
    print("\nWarehouse Table Counts")
    print("-" * 60)

    for table_name, expected_count in EXPECTED_TABLE_COUNTS.items():
        actual_count = get_table_count(table_name)
        status = "PASS" if actual_count == expected_count else "CHECK"

        print(
            f"{status:5} | {table_name:20} "
            f"expected={expected_count:<3} actual={actual_count:<3}"
        )


def print_top_yielding_lines(limit: int = 5) -> None:
    """
    Print sample analytics output from the top-yielding-lines view.

    Args:
        limit: Number of rows to display.
    """
    engine = create_engine(DATABASE_URL)

    query = text(
        """
        SELECT
            germplasm_id,
            line_name,
            line_type,
            yield_observation_count,
            avg_yield_kg_ha
        FROM vw_top_yielding_lines
        LIMIT :limit;
        """
    )

    with engine.begin() as connection:
        rows = connection.execute(query, {"limit": limit}).fetchall()

    print("\nTop Yielding Lines")
    print("-" * 60)

    for row in rows:
        print(
            f"{row.germplasm_id:8} | "
            f"{row.line_name:15} | "
            f"{row.line_type:12} | "
            f"n={row.yield_observation_count:<2} | "
            f"avg_yield={row.avg_yield_kg_ha}"
        )


def print_trial_completeness() -> None:
    """
    Print trial completeness summary from the warehouse view.
    """
    engine = create_engine(DATABASE_URL)

    query = text(
        """
        SELECT
            trial_id,
            location_name,
            trial_year,
            observation_count,
            germplasm_count,
            trait_count,
            plot_count
        FROM vw_trial_completeness
        ORDER BY trial_id;
        """
    )

    with engine.begin() as connection:
        rows = connection.execute(query).fetchall()

    print("\nTrial Completeness")
    print("-" * 60)

    for row in rows:
        print(
            f"{row.trial_id:10} | "
            f"{row.location_name:15} | "
            f"{row.trial_year} | "
            f"observations={row.observation_count:<3} | "
            f"germplasm={row.germplasm_count:<2} | "
            f"traits={row.trait_count:<2} | "
            f"plots={row.plot_count:<2}"
        )


def main() -> None:
    """
    Run warehouse validation checks and print sample analytics outputs.
    """
    print("Validating Breeding Data Warehouse Demo...")

    print_table_counts()
    print_top_yielding_lines()
    print_trial_completeness()

    print("\nValidation completed.")


if __name__ == "__main__":
    main()