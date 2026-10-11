# ml_experiment_tracker

A small Flask REST API for saving machine learning experiment runs.
You register an account, upload a CSV from a training run, and the API
saves the best accuracy and the final loss into a SQLite database, so you
can compare runs later.

I built this on my own to practice backend development.

## What it does
- Register an account (passwords are hashed with SHA-256 before saving)
- Upload an experiment: give it a results CSV (epoch, loss, accuracy).
  It reads the file with pandas, takes the best accuracy and the final loss,
  and saves them under a title
- Saves everything in a local SQLite database (tables are created on first run)

## Tech
Python, Flask, pandas, SQLite, pytest

## Endpoints
| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET  | /api/experiment    | Returns a sample experiment |
| POST | /register          | Create an account (username, password) |
| POST | /upload-experiment | Save a run (title, CSV filename) |

## How to run
```
pip install flask pandas
python3 app.py
```
The API runs on http://localhost:5000

Example (register, then save the sample run):
```
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "rokas", "password": "test123"}'

curl -X POST http://localhost:5000/upload-experiment \
  -H "Content-Type: application/json" \
  -d '{"title": "baseline", "filename": "sample_results.csv"}'
```

## Tests
```
python3 -m pytest -v
```
