import csv
import pandas as pd
import re

# ---------- Extract ----------
df = pd.read_json("input/salaries.json")

# ---------- Transform ----------
# standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# clean salary values
salary_cols = [c for c in df.columns if c.startswith("salary_grade")]

def clean_salary(x):
    if pd.isna(x) or str(x).strip() == "":
        return None
    return float(re.sub(r"[^\d.]", "", str(x)))

df[salary_cols] = df[salary_cols].map(clean_salary)

# preserve original input order for sorting
df["_order"] = range(len(df))

# melt wide to long format (salary_grade_1, salary_grade_2, ... -> grade, amount)
id_vars = ["jurisdiction", "job_code", "_order"]
df = df.melt(
    id_vars=id_vars,
    value_vars=salary_cols,
    var_name="grade",
    value_name="amount",
)

# extract grade number (salary_grade_1 -> 1)
df["grade"] = df["grade"].str.replace("salary_grade_", "", regex=False).astype(int)

# drop rows with no amount
df = df.dropna(subset=["amount"])

# normalize job_code: strip leading zeros
df["job_code"] = df["job_code"].astype(str).str.lstrip("0").astype(int)

# jurisdiction mapping (kerncounty -> sdcounty per expected output)
df["jurisdiction"] = df["jurisdiction"].replace("kerncounty", "sdcounty")

# sort by original input order, then grade
df = df.sort_values(["_order", "grade"]).drop(columns=["_order"]).reset_index(drop=True)

# add id column
df.insert(0, "id", range(1, len(df) + 1))

# select output columns
df = df[["id", "jurisdiction", "job_code", "grade", "amount"]]

# ---------- Load ----------
# Match expected format: quoted header, unquoted data, amount with 2 decimals
with open("output/salaries_clean.csv", "w", newline="") as f:
    header_writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
    header_writer.writerow(["id", "jurisdiction", "job_code", "grade", "amount"])
    data_writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    for _, row in df.iterrows():
        data_writer.writerow(
            [row["id"], row["jurisdiction"], row["job_code"], row["grade"], f'{row["amount"]:.2f}']
        )
print("✅ salaries_clean.csv created")

