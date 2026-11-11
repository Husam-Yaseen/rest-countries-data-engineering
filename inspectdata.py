import csv
from collections import Counter

with open("/tmp/countries_flat.csv", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print(f"Total rows: {len(rows)}")

print("\nEmpty cells by column:")
for column in reader.fieldnames:
    empty = sum(1 for row in rows if not row[column].strip())
    print(f"{column}: {empty}")

codes = Counter(row["code"].strip() for row in rows if row["code"].strip())
duplicates = {code: count for code, count in codes.items() if count > 1}
print(f"\nRepeated country codes: {duplicates or 'None'}")
from math import isfinite
from statistics import median, quantiles

for column in ("population", "area_km2"):
    numbers = []
    invalid = 0

    for row in rows:
        try:
            value = float(row[column])
        except ValueError:
            invalid += 1
            continue

        if not isfinite(value) or value < 0:
            invalid += 1
        else:
            numbers.append(value)

    print(f"\n{column}: {invalid} invalid values")
    if len(numbers) >= 2:
        q1, _, q3 = quantiles(numbers, n=4, method="inclusive")
        spread = q3 - q1
        unusual = sum(
            n < q1 - 1.5 * spread or n > q3 + 1.5 * spread
            for n in numbers
        )
        print(f"Min: {min(numbers)}, Median: {median(numbers)}, Max: {max(numbers)}")
        print(f"Potential outliers: {unusual}")