import json
import os
import subprocess

api_key = os.environ["RC_KEY"]
fields = "names,codes,region,population,area,languages,currencies,borders"
countries = []
offset = 0

while True:
    url = (
        "https://api.restcountries.com/countries/v5"
        f"?limit=100&offset={offset}&response_fields={fields}"
    )

    response = subprocess.run(
        ["curl", "-fsS", "--max-time", "30", "-H", "@-", url],
        input=f"Authorization: Bearer {api_key}\n",
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(response.stdout)["data"]
    page = data["objects"]
    countries.extend(page)
    print(f"Page: {len(page)} records")

    if not data["meta"]["more"]:
        break

    if not page:
        raise RuntimeError("The API returned an empty page unexpectedly.")
    offset += len(page)

print(f"Total downloaded: {len(countries)}")
print(f"Total expected:   {data['meta']['total']}")
from pathlib import Path

output = Path("/tmp/countries_raw.json")
output.write_text(
    json.dumps(countries, indent=2, ensure_ascii=False),
    encoding="utf-8",
)
print(f"Saved {len(countries)} records to {output}")