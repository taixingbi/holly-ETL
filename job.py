import csv
import pandas as pd

# ---------- Extract ----------
df = pd.read_json("input/job-descriptions.json")

# ---------- Transform ----------
# standardize column names
df.columns = df.columns.str.strip().str.lower()

# normalize job code: strip leading zeros
df["code"] = df["code"].astype(str).str.lstrip("0").astype(int)


def truncate_description(desc):
    """First clause, max 144 chars. Handle leading '.\n' -> ' ' (preserve leading space)."""
    s = desc.replace("\n", " ")
    if s.startswith(". "):
        s = " " + s[2:]  # ".\n" -> " "
    first = s.split(",")[0] if "," in s else s[:150]
    return first[:144] if len(first) > 144 else first


df["description"] = df["description"].apply(truncate_description)

# sort by jurisdiction, then code (match expected order)
df = df.sort_values(["jurisdiction", "code"]).reset_index(drop=True)

# select columns
df = df[["jurisdiction", "code", "title", "description"]]

# ---------- Load ----------
with open("output/job_descriptions_clean.csv", "w", newline="") as f:
    header_writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
    header_writer.writerow(["jurisdiction", "code", "title", "description"])
    data_writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    for _, row in df.iterrows():
        data_writer.writerow(
            [row["jurisdiction"], row["code"], row["title"], row["description"]]
        )

print("✅ job_descriptions_clean.csv created")
