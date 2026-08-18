# 💼 Job Listings Tracker

A mini full-stack Python project: fetches live remote job postings from a public API,
stores them locally in SQLite (with de-duplication), and provides an interactive
dashboard to search, filter, and track your application status per job.

## Features
- Pulls live listings from the [Remotive API](https://remotive.com/api-documentation) (free, no key required)
- SQLite storage with automatic de-duplication on refetch
- Search/filter saved jobs by keyword or application status
- Track status per job: New → Interested → Applied → Rejected → Offer
- Simple stats panel (counts per status)
- Streamlit dashboard — runs locally or deploys free on Streamlit Community Cloud

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Project structure
```
job_tracker/
├── app.py          # Streamlit UI
├── db.py           # SQLite schema, inserts, queries
├── fetcher.py       # API client for Remotive
├── requirements.txt
└── README.md
```

## Deploying it live (for your resume link)
1. Push this folder to a public GitHub repo.
2. Go to https://share.streamlit.io, connect your GitHub, pick the repo, set
   the entry file to `app.py`. Free tier is enough for this.
3. Add the live link + repo link to your resume/portfolio.

## Ideas to extend (good for interview talking points)
- Add a "match score" that compares your resume text against each job description (TF-IDF or an LLM call) — turns this into an NLP/ML project.
- Schedule the fetch daily (e.g., with `cron` or GitHub Actions) and email yourself a digest of new matches.
- Add authentication so multiple users can each track their own applications.
- Swap SQLite for Postgres and deploy on Render/Railway to show you can work with a "real" database.
- Add charts (jobs found per day, application funnel conversion) using `plotly`.

## Why this project is resume-worthy
It demonstrates, in one small codebase: consuming a third-party REST API,
designing a database schema, writing clean data-access functions, and building
a usable UI — the same shape of work as many real backend/data engineering tasks,
just scoped small enough to finish in a day or two.
