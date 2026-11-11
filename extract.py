import json
import os
import subprocess

url = "https://api.restcountries.com/countries/v5?limit=1&response_fields=names.common"
api_key = os.environ["RC_KEY"]

response = subprocess.check_output(
    ["curl", "-fsS", url, "-H", f"Authorization: Bearer {api_key}"],
    text=True,
)

result = json.loads(response)
print(result["data"]["objects"][0]["names"]["common"])