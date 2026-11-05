# chart.py
# bar chart of new oral otc phenylephrine listings per year, 2021 to now
# with the fda vote and the proposed order marked
#
# only going back to 2021 on purpose. the ndc directory only has products
# that are listed right now, so older years are missing stuff that got
# discontinued. recent years are way less affected by that

import csv
from pathlib import Path

import matplotlib.pyplot as plt

# use arial (falls back to helvetica if arial isnt there)
plt.rcParams["font.family"] = ["Arial", "Helvetica", "sans-serif"]

RED = "#cc0000"
LIGHT_RED = "#f0a0a0"  # for 2026 since the year isnt over

# read the filtered csv from clean.py
rows = []
with open("data/oral_otc_phenylephrine.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

years = [2021, 2022, 2023, 2024, 2025, 2026]

# count listings per year
counts = {}
for y in years:
    counts[y] = 0

for row in rows:
    year = int(row["marketing_start_date"][0:4])
    if year in counts:
        counts[year] = counts[year] + 1

# print the numbers so i can double check
for y in years:
    print(y, counts[y])

values = []
colors = []
for y in years:
    values.append(counts[y])
    if y == 2026:
        colors.append(LIGHT_RED)
    else:
        colors.append(RED)

fig, ax = plt.subplots(figsize=(9, 5))
x = list(range(len(years)))
bars = ax.bar(x, values, color=colors, width=0.65)

# put the number on top of each bar
for i in range(len(values)):
    ax.text(x[i], values[i] + 2, str(values[i]), ha="center", fontsize=11)

# dashed lines roughly where in the year each event happened
# each bar spans index - 0.5 to index + 0.5, so sept 12 is about 70% through 2023
# and nov 8 is about 85% through 2024
vote_x = years.index(2023) - 0.5 + 0.70
prop_x = years.index(2024) - 0.5 + 0.85
top = max(values)

ax.axvline(vote_x, color="gray", linestyle="--", linewidth=1)
ax.axvline(prop_x, color="black", linestyle="--", linewidth=1)
ax.text(vote_x - 0.05, top * 1.42, "Sept 2023:\nFDA advisers vote\n16-0 it doesn't work",
        fontsize=9, ha="right", va="top")
ax.text(prop_x + 0.05, top * 1.42, "Nov 2024:\nFDA proposes\nremoving it",
        fontsize=9, ha="left", va="top")

labels = []
for y in years:
    if y == 2026:
        labels.append("2026\n(through Nov 5)")
    else:
        labels.append(str(y))
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)

ax.set_ylim(0, top * 1.45)
ax.set_ylabel("New product listings", fontsize=11)
ax.set_title("New oral phenylephrine cold medicines listed with the FDA each year",
             fontsize=13, pad=12)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.text(0.01, 0.01,
         "Source: openFDA NDC Directory, pulled Nov 5, 2026. OTC monograph products taken by mouth. "
         "Only currently listed products are included.",
         fontsize=7.5, color="gray")

plt.tight_layout(rect=(0, 0.03, 1, 1))

Path("charts").mkdir(exist_ok=True)
plt.savefig("charts/listings_by_year.png", dpi=200)
print()
print("saved charts/listings_by_year.png")
