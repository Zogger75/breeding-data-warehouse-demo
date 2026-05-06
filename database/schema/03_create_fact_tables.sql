-- ============================================================
-- 03_create_fact_tables.sql
-- Purpose: Create warehouse fact tables
-- ============================================================

DROP TABLE IF EXISTS fact_observation;

CREATE TABLE fact_observation (
    observation_key SERIAL PRIMARY KEY,
    observation_id  VARCHAR(20) UNIQUE NOT NULL,

    trial_key       INTEGER NOT NULL REFERENCES dim_trial(trial_key),
    location_key    INTEGER NOT NULL REFERENCES dim_location(location_key),
    germplasm_key   INTEGER NOT NULL REFERENCES dim_germplasm(germplasm_key),
    trait_key       INTEGER NOT NULL REFERENCES dim_trait(trait_key),

    trial_year      INTEGER,
    rep             INTEGER,
    block           INTEGER,
    plot            VARCHAR(20),

    raw_value       VARCHAR(100),
    numeric_value   NUMERIC(12, 4),

    source_system   VARCHAR(100) DEFAULT 'CSV Demo Source',
    load_timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fact_observation_trial
    ON fact_observation(trial_key);

CREATE INDEX idx_fact_observation_location
    ON fact_observation(location_key);

CREATE INDEX idx_fact_observation_germplasm
    ON fact_observation(germplasm_key);

CREATE INDEX idx_fact_observation_trait
    ON fact_observation(trait_key);

CREATE INDEX idx_fact_observation_year
    ON fact_observation(trial_year);