# clean.py
# filter down to oral otc phenylephrine products (the ones the fda order is about)
# then count how many were listed after the vote and after the proposed order

import csv
import json

with open("data/raw/phenylephrine_ndc_raw.json") as f:
    records = json.load(f)

# keep a product only if ALL of these are true:
# - its otc (not prescription, not bulk ingredient)
# - you swallow it (oral)
# - its sold under the otc monograph
# - its a finished product, not a raw material
kept = []
for r in records:
    is_otc = r.get("product_type") == "HUMAN OTC DRUG"
    is_oral = "ORAL" in r.get("route", [])
    is_monograph = r.get("marketing_category", "").startswith("OTC MONOGRAPH")
    is_finished = r.get("finished") == True

    if is_otc and is_oral and is_monograph and is_finished:
        kept.append(r)

print("started with:", len(records))
print("oral otc monograph products:", len(kept))
print()

# key dates
VOTE = "20230912"      # fda advisers vote 16-0
PROPOSAL = "20241108"  # fda proposes removing it

after_vote = []
after_proposal = []
for r in kept:
    start = r.get("marketing_start_date", "")
    if start > VOTE:
        after_vote.append(r)
    if start > PROPOSAL:
        after_proposal.append(r)

print("listed after the sept 2023 vote:", len(after_vote))
print("listed after the nov 2024 proposal:", len(after_proposal))
print()

# show the newest ones so i can check them by eye
after_proposal.sort(key=lambda r: r["marketing_start_date"], reverse=True)
print("newest products listed after the proposal:")
for r in after_proposal[:15]:
    print("  ", r["marketing_start_date"], "|", r.get("labeler_name"), "|", r.get("brand_name"))

# save the filtered list to a csv so i can open it in excel
with open("data/oral_otc_phenylephrine.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["product_ndc", "brand_name", "labeler_name", "dosage_form", "marketing_start_date", "generic_name"])
    for r in kept:
        writer.writerow([
            r.get("product_ndc"),
            r.get("brand_name"),
            r.get("labeler_name"),
            r.get("dosage_form"),
            r.get("marketing_start_date"),
            r.get("generic_name"),
        ])

print()
print("saved data/oral_otc_phenylephrine.csv")
