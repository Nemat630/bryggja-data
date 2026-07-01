import duckdb
import requests
from datetime import datetime, timezone

print("Connecting to database...")
conn = duckdb.connect("bryggja.db")

conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
conn.execute("""
    CREATE TABLE IF NOT EXISTS raw.jobs (
        job_id      VARCHAR,
        title       VARCHAR,
        company     VARCHAR,
        location    VARCHAR,
        posted_date VARCHAR,
        loaded_at   TIMESTAMP
    )
""")

# Clear old data so we don't get duplicates
conn.execute("DELETE FROM raw.jobs")
print("Table cleared — starting fresh load")

# Search for multiple types of jobs
keywords = ["data engineer", "data scientist", "machine learning", "analytiker", "elektriker", "sjukskoterska"]
total_loaded = 0

for keyword in keywords:
    print(f"\nFetching jobs for: '{keyword}'...")
    response = requests.get(
        "https://jobsearch.api.jobtechdev.se/search",
        params={"q": keyword, "limit": 50},
        headers={"accept": "application/json"}
    )
    jobs = response.json().get("hits", [])
    print(f"  Found {len(jobs)} jobs")

    loaded = 0
    for job in jobs:
        try:
            conn.execute("""
                INSERT INTO raw.jobs VALUES (?, ?, ?, ?, ?, ?)
            """, [
                job.get("id", ""),
                job.get("headline", ""),
                job.get("employer", {}).get("name", ""),
                job.get("workplace_address", {}).get("municipality", ""),
                job.get("publication_date", "")[:10] if job.get("publication_date") else None,
                datetime.now(timezone.utc)
            ])
            loaded += 1
        except Exception as e:
            pass  # skip duplicates silently

    print(f"  Loaded {loaded} into database")
    total_loaded += loaded

print(f"\nTotal jobs in database: {conn.execute('SELECT COUNT(*) FROM raw.jobs').fetchone()[0]}")

print("\nSample — first 10 jobs:")
rows = conn.execute("""
    SELECT title, company, location, posted_date
    FROM raw.jobs
    ORDER BY posted_date DESC
    LIMIT 10
""").fetchall()
for i, row in enumerate(rows, 1):
    print(f"  {i}. {row[0]} at {row[1]} — {row[2]} ({row[3]})")

conn.close()
print("\nDone! bryggja.db updated.")
