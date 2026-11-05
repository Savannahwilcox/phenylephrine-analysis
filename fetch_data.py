"""
fetch_data.py

Step 1 of the phenylephrine analysis: download raw records from the
openFDA NDC Directory and save them to disk, untouched.

Rule we follow: this script only DOWNLOADS. It never filters, cleans,
or changes anything. Every later script reads from the raw file this
one saves. That way, if you make a mistake later, you never have to
re-download, and anyone can check your work from the same starting point.

Run it from your project folder with your venv active:
    python fetch_data.py
"""

import json
import time
from pathlib import Path

import requests

BASE_URL = "https://api.fda.gov/drug/ndc.json"

# openFDA returns at most 1,000 records per request. To get more, you
# ask for the next "page" using `skip`. This is called pagination.
PAGE_SIZE = 1000

# The two ingredients we're comparing. We search broadly here on purpose
# (any product listing that ingredient, any route). Narrowing to oral OTC
# products happens later in clean.py, where you can see and explain
# every filter. Searching broadly first also lets you look at what you're
# throwing away, which is part of checking your work.
INGREDIENTS = {
    "phenylephrine": 'active_ingredients.name:"PHENYLEPHRINE"',
    "pseudoephedrine": 'active_ingredients.name:"PSEUDOEPHEDRINE"',
}

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_all(search: str) -> list[dict]:
    """Page through every result for one search and return them as a list."""
    results = []
    skip = 0

    while True:
        params = {"search": search, "limit": PAGE_SIZE, "skip": skip}
        response = requests.get(BASE_URL, params=params, timeout=60)

        # openFDA returns a 404 when you've paged past the last result.
        # That's how we know we're done.
        if response.status_code == 404:
            break
        response.raise_for_status()

        payload = response.json()
        batch = payload["results"]
        results.extend(batch)

        total = payload["meta"]["results"]["total"]
        print(f"  got {len(results)} of {total}")

        skip += PAGE_SIZE
        if skip >= total:
            break

        # Be polite to a free public API. Without an API key you're
        # limited to a few requests per minute and 1,000 per day.
        time.sleep(1)

    return results


if __name__ == "__main__":
    for name, search in INGREDIENTS.items():
        print(f"Fetching {name}...")
        records = fetch_all(search)

        out_path = RAW_DIR / f"{name}_ndc_raw.json"
        with open(out_path, "w") as f:
            json.dump(records, f, indent=2)

        print(f"Saved {len(records)} records to {out_path}\n")

    # Write down WHEN you pulled the data. The NDC Directory changes
    # constantly, so your README needs to say which day's version you used.
    (RAW_DIR / "pulled_on.txt").write_text(time.strftime("%Y-%m-%d"))
