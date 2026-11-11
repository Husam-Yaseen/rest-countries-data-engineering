import csv
import json
from pathlib import Path

countries = json.loads(
    Path("/tmp/countries_raw.json").read_text(encoding="utf-8")
)

with open("/tmp/countries_flat.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "country", "code", "region", "population", "area_km2",
        "languages", "currencies", "borders",
    ])

    for country in countries:
        writer.writerow([
            (country.get("names") or {}).get("common"),
            (country.get("codes") or {}).get("alpha_3"),
            country.get("region"),
            country.get("population"),
            (country.get("area") or {}).get("kilometers"),
            " | ".join(item["name"] for item in country.get("languages") or []),
            " | ".join(item["code"] for item in country.get("currencies") or []),
            " | ".join(country.get("borders") or []),
        ])

print(f"Created /tmp/countries_flat.csv with {len(countries)} rows")