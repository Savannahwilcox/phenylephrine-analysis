# explore.py
# looking at the raw phenylephrine data before filtering
# want to see what fields there are + what values they have

import json

with open("data/raw/phenylephrine_ndc_raw.json") as f:
    records = json.load(f)

print("total records:", len(records))
print()

# print one full record to see all the fields
print("first record:")
print(json.dumps(records[0], indent=2))
print()


# helper to print counts biggest first
def print_counts(title, counts):
    print(title)
    for value in sorted(counts, key=counts.get, reverse=True):
        print("  ", counts[value], value)
    print()


# product type (otc vs prescription etc)
product_types = {}
for r in records:
    pt = r.get("product_type")
    product_types[pt] = product_types.get(pt, 0) + 1
print_counts("product type:", product_types)

# route is a list bc some products have more than one
routes = {}
for r in records:
    for route in r.get("route", []):
        routes[route] = routes.get(route, 0) + 1
print_counts("route:", routes)

# marketing category (otc monograph, nda, etc)
categories = {}
for r in records:
    cat = r.get("marketing_category")
    categories[cat] = categories.get(cat, 0) + 1
print_counts("marketing category:", categories)

# dates are text like 20240115 so sorting them works
dates = []
missing = 0
for r in records:
    if r.get("marketing_start_date"):
        dates.append(r["marketing_start_date"])
    else:
        missing = missing + 1
dates.sort()

print("marketing start date:")
print("   earliest:", dates[0])
print("   latest:", dates[-1])
print("   missing:", missing)
