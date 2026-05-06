from pathlib import Path

import pandas as pd


RAW_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def test_required_source_files_exist():
    expected_files = [
        "locations.csv",
        "germplasm.csv",
        "traits.csv",
        "trials.csv",
        "observations.csv",
    ]

    for file_name in expected_files:
        assert (RAW_DATA_DIR / file_name).exists(), f"Missing {file_name}"


def test_observations_have_valid_required_fields():
    observations = pd.read_csv(RAW_DATA_DIR / "observations.csv")

    required_columns = [
        "observation_id",
        "trial_id",
        "germplasm_id",
        "trait_id",
        "rep",
        "block",
        "plot",
        "raw_value",
    ]

    for column in required_columns:
        assert column in observations.columns

    assert observations["observation_id"].notna().all()
    assert observations["trial_id"].notna().all()
    assert observations["germplasm_id"].notna().all()
    assert observations["trait_id"].notna().all()


def test_observation_references_are_valid():
    observations = pd.read_csv(RAW_DATA_DIR / "observations.csv")
    trials = pd.read_csv(RAW_DATA_DIR / "trials.csv")
    germplasm = pd.read_csv(RAW_DATA_DIR / "germplasm.csv")
    traits = pd.read_csv(RAW_DATA_DIR / "traits.csv")

    assert set(observations["trial_id"]).issubset(set(trials["trial_id"]))
    assert set(observations["germplasm_id"]).issubset(set(germplasm["germplasm_id"]))
    assert set(observations["trait_id"]).issubset(set(traits["trait_id"]))


def test_yield_values_are_non_negative():
    observations = pd.read_csv(RAW_DATA_DIR / "observations.csv")
    yield_rows = observations[observations["trait_id"] == "T001"].copy()

    yield_rows["numeric_value"] = pd.to_numeric(
        yield_rows["raw_value"],
        errors="coerce",
    )

    assert yield_rows["numeric_value"].notna().all()
    assert (yield_rows["numeric_value"] >= 0).all()