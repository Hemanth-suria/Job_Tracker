"""
app.py — Streamlit dashboard for the Job Tracker.
Run with: streamlit run app.py
"""
import streamlit as st
from db import init_db, upsert_jobs, fetch_jobs, update_status, stats, get_distinct_locations
from fetcher import fetch_remote_jobs

st.set_page_config(page_title="Job Tracker", page_icon="💼", layout="wide")
init_db()

st.title("💼 Job Listings Tracker")
st.caption("Live remote job postings, saved locally, with application-status tracking.")

# ---------------- Sidebar: fetch new jobs ----------------
with st.sidebar:
    st.header("🔍 Fetch New Jobs")
    search_term = st.text_input("Search keyword", value="python")
    category = st.selectbox(
        "Category (optional)",
        ["", "software-dev", "data", "product", "design", "marketing",
         "sales", "customer-service", "writing"],
    )
    if st.button("Fetch Jobs", type="primary"):
        with st.spinner("Fetching from Remotive API..."):
            try:
                jobs = fetch_remote_jobs(search=search_term, category=category)
                added = upsert_jobs(jobs)
                st.success(f"Fetched {len(jobs)} jobs — {added} new added.")
            except Exception as e:
                st.error(f"Fetch failed: {e}")

    st.divider()
    st.header("📊 Stats")
    for status, count in stats().items():
        st.metric(status, count)

# ---------------- Main: browse & filter ----------------
col1, col2, col3 = st.columns([3, 1, 1.5])
with col1:
    keyword = st.text_input("Search saved jobs", placeholder="e.g. 'data engineer' or company name")
with col2:
    status_filter = st.selectbox("Status", ["All", "New", "Interested", "Applied", "Rejected", "Offer"])
with col3:
    location_options = ["All"] + get_distinct_locations()
    location_filter = st.selectbox("Country / Location", location_options)

results = fetch_jobs(keyword=keyword, status=status_filter, location=location_filter)
st.write(f"**{len(results)} job(s) found**")

for job in results:
    with st.expander(f"{job['title']}  —  {job['company']}  ({job['location'] or 'N/A'})"):
        st.markdown(f"**Category:** {job['category']}  |  **Posted:** {job['published_at']}")
        st.markdown(f"[View original posting]({job['url']})")
        st.write(job["description"][:600] + ("..." if len(job["description"]) > 600 else ""))

        new_status = st.selectbox(
            "Update status",
            ["New", "Interested", "Applied", "Rejected", "Offer"],
            index=["New", "Interested", "Applied", "Rejected", "Offer"].index(job["status"]),
            key=f"status_{job['id']}",
        )
        if new_status != job["status"]:
            update_status(job["id"], new_status)
            st.rerun()
