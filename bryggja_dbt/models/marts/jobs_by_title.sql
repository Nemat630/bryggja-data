/*
  jobs_by_title.sql

  Answers: What are the most in-demand job roles right now in Sweden?
  This becomes a ranking chart in Metabase.

  We extract the first 3 words of each title to group similar jobs:
  "Data Engineer" and "Data Engineer (Stockholm)" count as the same role.
*/

WITH title_cleaned AS (
    SELECT
        -- Take just the first meaningful part of the title
        -- Split on common separators and take the first part
        SPLIT_PART(
            SPLIT_PART(title, ' –', 1),
            ' -', 1
        ) AS role_name,
        location,
        company,
        posted_date
    FROM {{ ref('stg_jobs') }}
),

aggregated AS (
    SELECT
        role_name,
        COUNT(*)                    AS job_count,
        COUNT(DISTINCT location)    AS cities_hiring,
        COUNT(DISTINCT company)     AS companies_hiring,
        MAX(posted_date)            AS most_recent
    FROM title_cleaned
    WHERE LENGTH(role_name) > 3
    GROUP BY role_name
)

SELECT *
FROM aggregated
WHERE job_count >= 1
ORDER BY job_count DESC
LIMIT 50
