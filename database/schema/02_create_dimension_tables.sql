-- ============================================================
-- 02_create_dimension_tables.sql
-- Purpose: Create warehouse dimension tables
-- ============================================================

DROP TABLE IF EXISTS dim_trial CASCADE;
DROP TABLE IF EXISTS dim_location CASCADE;
DROP TABLE IF EXISTS dim_germplasm CASCADE;
DROP TABLE IF EXISTS dim_trait CASCADE;

CREATE TABLE dim_location (
    location_key    SERIAL PRIMARY KEY,
    location_id     VARCHAR(20) UNIQUE NOT NULL,
    location_name   VARCHAR(100) NOT NULL,
    province        VARCHAR(50),
    country         VARCHAR(50),
    latitude        NUMERIC(9, 6),
    longitude       NUMERIC(9, 6)
);

CREATE TABLE dim_germplasm (
    germplasm_key   SERIAL PRIMARY KEY,
    germplasm_id    VARCHAR(20) UNIQUE NOT NULL,
    line_name       VARCHAR(100) NOT NULL,
    line_type       VARCHAR(50),
    pedigree        TEXT
);

CREATE TABLE dim_trait (
    trait_key       SERIAL PRIMARY KEY,
    trait_id        VARCHAR(20) UNIQUE NOT NULL,
    trait_name      VARCHAR(100) NOT NULL,
    trait_category  VARCHAR(50),
    unit            VARCHAR(50),
    data_type       VARCHAR(50)
);

CREATE TABLE dim_trial (
    trial_key       SERIAL PRIMARY KEY,
    trial_id        VARCHAR(20) UNIQUE NOT NULL,
    trial_name      VARCHAR(150) NOT NULL,
    crop            VARCHAR(50),
    trial_year      INTEGER,
    location_id     VARCHAR(20),
    design          VARCHAR(50),
    rep_count       INTEGER
);