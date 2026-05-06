-- ============================================================
-- 04_create_views.sql
-- Purpose: Create analytics-ready reporting views
-- ============================================================

DROP VIEW IF EXISTS vw_observation_detail;
DROP VIEW IF EXISTS vw_trait_summary_by_location;
DROP VIEW IF EXISTS vw_germplasm_performance;
DROP VIEW IF EXISTS vw_trial_completeness;
DROP VIEW IF EXISTS vw_top_yielding_lines;

CREATE VIEW vw_observation_detail AS
SELECT
    fo.observation_id,
    dt.trial_id,
    dt.trial_name,
    dt.crop,
    dt.trial_year,
    dl.location_name,
    dl.province,
    dg.germplasm_id,
    dg.line_name,
    dg.line_type,
    dtr.trait_id,
    dtr.trait_name,
    dtr.trait_category,
    dtr.unit,
    fo.rep,
    fo.block,
    fo.plot,
    fo.raw_value,
    fo.numeric_value,
    fo.load_timestamp
FROM fact_observation fo
JOIN dim_trial dt
    ON fo.trial_key = dt.trial_key
JOIN dim_location dl
    ON fo.location_key = dl.location_key
JOIN dim_germplasm dg
    ON fo.germplasm_key = dg.germplasm_key
JOIN dim_trait dtr
    ON fo.trait_key = dtr.trait_key;

CREATE VIEW vw_trait_summary_by_location AS
SELECT
    trial_year,
    location_name,
    trait_name,
    unit,
    COUNT(*) AS observation_count,
    ROUND(AVG(numeric_value), 2) AS avg_value,
    ROUND(MIN(numeric_value), 2) AS min_value,
    ROUND(MAX(numeric_value), 2) AS max_value
FROM vw_observation_detail
WHERE numeric_value IS NOT NULL
GROUP BY
    trial_year,
    location_name,
    trait_name,
    unit;

CREATE VIEW vw_germplasm_performance AS
SELECT
    germplasm_id,
    line_name,
    line_type,
    trait_name,
    unit,
    COUNT(*) AS observation_count,
    ROUND(AVG(numeric_value), 2) AS avg_value,
    ROUND(MIN(numeric_value), 2) AS min_value,
    ROUND(MAX(numeric_value), 2) AS max_value
FROM vw_observation_detail
WHERE numeric_value IS NOT NULL
GROUP BY
    germplasm_id,
    line_name,
    line_type,
    trait_name,
    unit;

CREATE VIEW vw_trial_completeness AS
SELECT
    trial_id,
    trial_name,
    location_name,
    trial_year,
    COUNT(*) AS observation_count,
    COUNT(DISTINCT germplasm_id) AS germplasm_count,
    COUNT(DISTINCT trait_id) AS trait_count,
    COUNT(DISTINCT plot) AS plot_count
FROM vw_observation_detail
GROUP BY
    trial_id,
    trial_name,
    location_name,
    trial_year;

CREATE VIEW vw_top_yielding_lines AS
SELECT
    germplasm_id,
    line_name,
    line_type,
    COUNT(*) AS yield_observation_count,
    ROUND(AVG(numeric_value), 2) AS avg_yield_kg_ha
FROM vw_observation_detail
WHERE trait_name = 'Yield'
  AND numeric_value IS NOT NULL
GROUP BY
    germplasm_id,
    line_name,
    line_type
ORDER BY
    avg_yield_kg_ha DESC;