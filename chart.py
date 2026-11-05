# chart.py
# bar chart of new oral otc phenylephrine listings per quarter, 2021 to now
# with the fda vote and the proposed order marked
#
# only going back to 2021 on purpose. the ndc directory only has products
# that are listed right now, so older years are missing stuff that got
# discontinued. recent years are way less affected by that

import csv
from pathlib import Path

import matplotlib.pyplot as plt

# read the filtered csv from clean.py
rows = []
with open("data/oral_otc_phenylephrine.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# make a list of every quarter from 2021 q1 to 2026 q4
quarters = []
for year in range(2021, 2027):
    for q in range(1, 5):
        quarters.append(str(year) + " Q" + str(q))

# count listings per quarter
counts = {}
for label in quarters:
    counts[label] = 0

for row in rows:
    date = row["marketing_start_date"]  # like 20240115
    year = int(date[0:4])
    month = int(date[4:6])
    q = (month - 1) // 3 + 1  # jan-mar = 1, apr-jun = 2, etc
    label = str(year) + " Q" + str(q)
    if label in counts:
        counts[label] = counts[label] + 1

values = []
for label in quarters:
    values.append(counts[label])

# print the numbers too so i can double check the chart
for label in quarters:
    print(label, counts[label])

# draw it
fig, ax = plt.subplots(figsize=(11, 5))
x = list(range(len(quarters)))
ax.bar(x, values, color="#4a6fa5")

# mark the vote (sept 2023 = 2023 q3) and proposal (nov 2024 = 2024 q4)
vote_i = quarters.index("2023 Q3")
prop_i = quarters.index("2024 Q4")
ax.axvline(vote_i, color="gray", linestyle="--")
ax.axvline(prop_i, color="black", linestyle="--")
top = max(values)
ax.text(vote_i + 0.15, top, "FDA advisers vote\n16-0 it doesn't work", fontsize=9, va="top")
ax.text(prop_i + 0.15, top * 0.75, "FDA proposes\nremoving it", fontsize=9, va="top")

ax.set_xticks(x)
ax.set_xticklabels(quarters, rotation=60, ha="right", fontsize=8)
ax.set_ylabel("New product listings")
ax.set_title("New oral OTC phenylephrine product listings by quarter, 2021-2026")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.text(0.01, 0.01,
         "Source: openFDA NDC Directory, pulled Nov 5, 2026. 2026 Q4 is partial. "
         "Only products currently listed are included.",
         fontsize=7, color="gray")

plt.tight_layout(rect=(0, 0.03, 1, 1))

Path("charts").mkdir(exist_ok=True)
plt.savefig("charts/listings_by_quarter.png", dpi=200)
print()
print("saved charts/listings_by_quarter.png")
