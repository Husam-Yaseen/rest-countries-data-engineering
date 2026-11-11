import csv

with open("/tmp/countries_flat.csv", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    columns = list(reader.fieldnames)
    rows = list(reader)

with open("/tmp/countries_clean.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns + ["code_missing"])
    writer.writeheader()

    for row in rows:
        row = {column: value.strip() for column, value in row.items()}
        row["code"] = row["code"].upper()
        row["code_missing"] = "yes" if not row["code"] else "no"
        writer.writerow(row)

print(f"Saved {len(rows)} rows to /tmp/countries_clean.csv")