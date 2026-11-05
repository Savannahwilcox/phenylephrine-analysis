# fetch_data.py
# downloads phenylephrine + pseudoephedrine records from the openfda ndc directory
# just saves the raw data, no filtering here (do that in clean.py)

import json
import time
from pathlib import Path

import requests

BASE_URL = "https://api.fda.gov/drug/ndc.json"
PAGE_SIZE = 1000  # api max per request

# search broad for now, narrow down to oral otc later
searches = {
    "phenylephrine": 'active_ingredients.name:"PHENYLEPHRINE"',
    "pseudoephedrine": 'active_ingredients.name:"PSEUDOEPHEDRINE"',
}

raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)


def fetch_all(search):
    results = []
    skip = 0

    while True:
        params = {"search": search, "limit": PAGE_SIZE, "skip": skip}
        response = requests.get(BASE_URL, params=params, timeout=60)

        # 404 means no more results
        if response.status_code == 404:
            break
        response.raise_for_status()

        data = response.json()
        results = results + data["results"]

        total = data["meta"]["results"]["total"]
        print("got", len(results), "of", total)

        skip = skip + PAGE_SIZE
        if skip >= total:
            break

        time.sleep(1)  # dont hit the rate limit

    return results


for name in searches:
    print("fetching", name)
    records = fetch_all(searches[name])

    out_path = raw_dir / (name + "_ndc_raw.json")
    with open(out_path, "w") as f:
        json.dump(records, f, indent=2)

    print("saved", len(records), "records to", out_path)

# save the date i pulled it since the directory changes
(raw_dir / "pulled_on.txt").write_text(time.strftime("%Y-%m-%d"))
