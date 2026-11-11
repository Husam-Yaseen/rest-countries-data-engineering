import csv
from collections import Counter

import matplotlib.pyplot as plt

with open("/tmp/countries_clean.csv", encoding="utf-8", newline="") as file:
    counts = Counter(row["region"] for row in csv.DictReader(file))

regions, totals = zip(*counts.most_common())
plt.figure(figsize=(9, 5))
plt.bar(regions, totals)
plt.title("Number of records by region")
plt.ylabel("Number of records")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("/tmp/records_by_region.png", dpi=150)
print("Saved /tmp/records_by_region.png")
with open("/tmp/countries_clean.csv", encoding="utf-8", newline="") as file:
    rows = list(csv.DictReader(file))

top_10 = sorted(rows, key=lambda row: int(row["population"]), reverse=True)[:10]
names = [row["country"] for row in top_10]
populations = [int(row["population"]) / 1_000_000 for row in top_10]

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(names, populations)
ax.invert_yaxis()
ax.set_title("Top 10 records by population")
ax.set_xlabel("Population (millions)")
fig.tight_layout()
fig.savefig("/tmp/top_10_population.png", dpi=150)
plt.close(fig)
from math import log10

areas = [float(row["area_km2"]) for row in rows]
log_areas = [log10(area) for area in areas if area > 0]

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(log_areas, bins=15, edgecolor="white")
ax.set_title("Distribution of land areas")
ax.set_xlabel("Area in km² (log10 scale)")
ax.set_ylabel("Number of records")
fig.tight_layout()
fig.savefig("/tmp/area_distribution.png", dpi=150)
plt.close(fig)
points = []
for row in rows:
    area = float(row["area_km2"])
    population = int(row["population"])
    if area > 0 and population > 0:
        points.append((area, population))

x, y = zip(*points)
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(x, y, alpha=0.55)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Area and population")
ax.set_xlabel("Area (km², log scale)")
ax.set_ylabel("Population (log scale)")
fig.tight_layout()
fig.savefig("/tmp/area_vs_population.png", dpi=150)
plt.close(fig)

print(f"Records excluded from this chart: {len(rows) - len(points)}")
populations_by_region = {}

for row in rows:
    population = int(row["population"])
    if population > 0:
        populations_by_region.setdefault(row["region"], []).append(population)

regions = sorted(populations_by_region)
values = [populations_by_region[region] for region in regions]

fig, ax = plt.subplots(figsize=(9, 5))
ax.boxplot(values, tick_labels=regions)
ax.set_yscale("log")
ax.set_title("Population distribution by region")
ax.set_ylabel("Population (log scale)")
ax.tick_params(axis="x", labelrotation=30)
fig.tight_layout()
fig.savefig("/tmp/population_by_region.png", dpi=150)
plt.close(fig)