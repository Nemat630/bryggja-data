/*
  daily_pipeline.sql

  Answers: How many jobs were loaded each day? Is the pipeline healthy?
  This becomes the pipeline monitoring chart in Metabase.
  This is exactly "övervaka ELT-pipelines" from the job posting.
*/

SELECT
    CAST(loaded_at AS DATE)   AS load_date,
    COUNT(*)                  AS jobs_loaded,
    COUNT(DISTINCT location)  AS locations_covered,
    COUNT(DISTINCT company)   AS companies_seen,
    MIN(posted_date)          AS earliest_job_date,
    MAX(posted_date)          AS latest_job_date
FROM {{ ref('stg_jobs') }}
GROUP BY CAST(loaded_at AS DATE)
ORDER BY load_date DESC
