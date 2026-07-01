import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd

# Page config
st.set_page_config(
    page_title="Bryggja — Swedish Labour Market",
    page_icon="🇸🇪",
    layout="wide"
)

# Connect to database
DB_PATH = "/Users/skolan/Desktop/projects/bryggja-data/bryggja.db"

@st.cache_data
def load_data():
    conn = duckdb.connect(DB_PATH, read_only=True)
    locations = conn.execute("SELECT * FROM main.jobs_by_location").df()
    titles    = conn.execute("SELECT * FROM main.jobs_by_title LIMIT 20").df()
    pipeline  = conn.execute("SELECT * FROM main.daily_pipeline").df()
    total     = conn.execute("SELECT COUNT(*) FROM main.stg_jobs").fetchone()[0]
    conn.close()
    return locations, titles, pipeline, total

locations, titles, pipeline, total = load_data()

# Header
st.title("🇸🇪 Bryggja — Swedish Labour Market Dashboard")
st.caption("Live data from Arbetsförmedlingen · Built with Python, dbt, and DuckDB")

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", f"{total:,}")
col2.metric("Cities with openings", len(locations))
col3.metric("Unique job titles", len(titles))
col4.metric("Top city", locations.iloc[0]['location'] if len(locations) > 0 else "—")

st.divider()

# Two columns layout
left, right = st.columns(2)

with left:
    st.subheader("Jobs by city")
    st.caption("Which Swedish cities have the most openings right now")
    top_cities = locations.head(12)
    fig = px.bar(
        top_cities,
        x="job_count",
        y="location",
        orientation="h",
        color="job_count",
        color_continuous_scale="teal",
        labels={"job_count": "Job openings", "location": "City"},
    )
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Most in-demand roles")
    st.caption("Top job titles by number of openings")
    top_titles = titles.head(15)
    fig2 = px.bar(
        top_titles,
        x="job_count",
        y="role_name",
        orientation="h",
        color="job_count",
        color_continuous_scale="blues",
        labels={"job_count": "Openings", "role_name": "Role"},
    )
    fig2.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Pipeline health
st.subheader("Pipeline health")
st.caption("When data was loaded and how much")
st.dataframe(
    pipeline.rename(columns={
        "load_date": "Load date",
        "jobs_loaded": "Jobs loaded",
        "locations_covered": "Cities covered",
        "companies_seen": "Companies",
        "earliest_job_date": "Oldest job",
        "latest_job_date": "Newest job"
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()

# Raw data explorer
st.subheader("Explore jobs by city")
selected_city = st.selectbox(
    "Pick a city",
    options=["All"] + sorted(locations["location"].tolist())
)

conn = duckdb.connect(DB_PATH, read_only=True)
if selected_city == "All":
    jobs = conn.execute("""
        SELECT title, company, location, posted_date
        FROM main.stg_jobs
        ORDER BY posted_date DESC
        LIMIT 50
    """).df()
else:
    jobs = conn.execute("""
        SELECT title, company, location, posted_date
        FROM main.stg_jobs
        WHERE location = ?
        ORDER BY posted_date DESC
        LIMIT 50
    """, [selected_city]).df()
conn.close()

st.dataframe(
    jobs.rename(columns={
        "title": "Job title",
        "company": "Company",
        "location": "City",
        "posted_date": "Posted"
    }),
    use_container_width=True,
    hide_index=True
)

st.caption(f"Showing {len(jobs)} jobs · Data refreshes when you run load_jobs.py")
