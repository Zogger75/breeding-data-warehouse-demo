-- ============================================================
-- 01_create_staging_tables.sql
-- Purpose: Create raw staging tables for breeding trial source data
-- ============================================================

DROP TABLE IF EXISTS stg_observations;
DROP TABLE IF EXISTS stg_trials;
DROP TABLE IF EXISTS stg_traits;
DROP TABLE IF EXISTS stg_germplasm;
DROP TABLE IF EXISTS stg_locations;

CREATE TABLE stg_locations (
    location_id     VARCHAR(20) PRIMARY KEY,
    location_name   VARCHAR(100) NOT NULL,
    province        VARCHAR(50),
    country         VARCHAR(50),
    latitude        NUMERIC(9, 6),
    longitude       NUMERIC(9, 6)
);

CREATE TABLE stg_germplasm (
    germplasm_id    VARCHAR(20) PRIMARY KEY,
    line_name       VARCHAR(100) NOT NULL,
    line_type       VARCHAR(50),
    pedigree        TEXT
);

CREATE TABLE stg_traits (
    trait_id        VARCHAR(20) PRIMARY KEY,
    trait_name      VARCHAR(100) NOT NULL,
    trait_category  VARCHAR(50),
    unit            VARCHAR(50),
    data_type       VARCHAR(50)
);

CREATE TABLE stg_trials (
    trial_id        VARCHAR(20) PRIMARY KEY,
    trial_name      VARCHAR(150) NOT NULL,
    crop            VARCHAR(50),
    trial_year      INTEGER,
    location_id     VARCHAR(20),
    design          VARCHAR(50),
    rep_count       INTEGER
);

CREATE TABLE stg_observations (
    observation_id  VARCHAR(20) PRIMARY KEY,
    trial_id        VARCHAR(20) NOT NULL,
    germplasm_id    VARCHAR(20) NOT NULL,
    trait_id        VARCHAR(20) NOT NULL,
    rep             INTEGER,
    block           INTEGER,
    plot            VARCHAR(20),
    raw_value       VARCHAR(100)
);