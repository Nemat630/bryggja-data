/*
  jobs_by_location.sql

  Answers: Which Swedish cities have the most job openings?
  This becomes a bar chart or map in Metabase.

  Notice: we use {{ ref('stg_jobs') }} instead of raw.jobs
  This is dbt's way of saying "use the clean version"
  dbt automatically knows stg_jobs must run first.
*/

SELECT
    location,
    COUNT(*)          AS job_count,
    COUNT(DISTINCT company) AS unique_companies,
    MIN(posted_date)  AS oldest_posting,
    MAX(posted_date)  AS newest_posting
FROM {{ ref('stg_jobs') }}
WHERE location != 'Unknown'
GROUP BY location
ORDER BY job_count DESC
