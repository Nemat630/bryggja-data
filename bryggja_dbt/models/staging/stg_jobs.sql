/*
  stg_jobs.sql — Staging model for raw job data

  Reads raw.jobs and produces a clean, reliable table.
  Every other model builds on top of this one.
*/

WITH source AS (

    -- Read all raw data
    SELECT * FROM raw.jobs

),

cleaned AS (

    SELECT
        job_id,

        -- Clean title: remove extra whitespace
        TRIM(title) AS title,

        -- Clean company name
        -- DuckDB doesn't have INITCAP, so we just trim and uppercase
        -- We'll keep it clean but not change case
        TRIM(company) AS company,

        -- Location: use 'Unknown' if empty or null
        CASE
            WHEN TRIM(location) IS NULL OR TRIM(location) = ''
            THEN 'Unknown'
            ELSE TRIM(location)
        END AS location,

        -- Convert posted_date string to a proper DATE
        TRY_CAST(posted_date AS DATE) AS posted_date,

        loaded_at

    FROM source

),

deduplicated AS (

    -- If the same job appears twice, keep only the most recent
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY job_id
            ORDER BY loaded_at DESC
        ) AS row_num
    FROM cleaned

)

-- Final output: no duplicates, no empty titles
SELECT
    job_id,
    title,
    company,
    location,
    posted_date,
    loaded_at
FROM deduplicated
WHERE row_num = 1
  AND title IS NOT NULL
  AND TRIM(title) != ''
