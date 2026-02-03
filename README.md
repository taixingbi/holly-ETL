# holly-ETL

ETL pipelines for salary and job description data.

## Setup

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

```bash
python salary.py   # input/salaries.json → output/salaries_clean.csv
python job.py      # input/job-descriptions.json → output/job_descriptions_clean.csv
```

Or use Jupyter:

```bash
jupyter notebook
```

## Project Structure

| Path | Description |
|------|-------------|
| `input/` | Source JSON files |
| `output/` | Generated CSV files |
| `salary.py` | Salaries ETL (wide → long format) |
| `job.py` | Job descriptions ETL |
