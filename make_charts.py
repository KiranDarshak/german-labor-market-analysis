import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

gap = pd.read_csv("data/mart_east_west_convergence.csv")
longrun = pd.read_csv("data/mart_long_run_west_germany.csv")
snap = pd.read_csv("data/mart_state_snapshot_2025.csv")

BLUE = "#2b6cb0"
ORANGE = "#dd6b20"
GRAY = "#718096"
GREEN = "#2f855a"

# Chart 1: East vs West convergence, 1991-2025, with gap
fig, ax = plt.subplots(figsize=(7.8,4.8), dpi=150)
ax.plot(gap["year"], gap["East Germany"], color=ORANGE, marker='o', markersize=3, linewidth=2, label="East Germany")
ax.plot(gap["year"], gap["West Germany"], color=BLUE, marker='o', markersize=3, linewidth=2, label="West Germany")
ax.fill_between(gap["year"], gap["West Germany"], gap["East Germany"], color=ORANGE, alpha=0.12)
peak_row = gap.loc[gap["east_west_gap_pp"].idxmax()]
ax.annotate(f"Widest gap: {peak_row['east_west_gap_pp']:.1f}pp ({int(peak_row['year'])})",
            xy=(peak_row["year"], peak_row["East Germany"]), xytext=(peak_row["year"]-9, peak_row["East Germany"]+2.5),
            fontsize=9, arrowprops=dict(arrowstyle="->", color="#555"))
last_row = gap.iloc[-1]
ax.annotate(f"2025 gap: {last_row['east_west_gap_pp']:.1f}pp",
            xy=(last_row["year"], last_row["East Germany"]), xytext=(last_row["year"]-11, last_row["East Germany"]+3),
            fontsize=9, arrowprops=dict(arrowstyle="->", color="#555"))
ax.set_ylabel("Unemployment rate (%)")
ax.set_title("Germany's East-West Unemployment Gap Has Nearly Closed", fontsize=12, fontweight='bold')
ax.legend(frameon=False, loc='upper right')
ax.spines[['top','right']].set_visible(False)
ax.yaxis.grid(True, color='#e5e5e5', linewidth=0.8)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig("east_west_convergence.png", dpi=150)
plt.close()

# Chart 2: long-run West Germany / Germany unemployment rate with event markers
fig, ax = plt.subplots(figsize=(8.5,4.8), dpi=150)
ax.plot(longrun["year"], longrun["unemployment_rate_pct"], color=GRAY, linewidth=1.8)
ev = longrun.dropna(subset=["event"])
ax.scatter(ev["year"], ev["unemployment_rate_pct"], color=ORANGE, zorder=5, s=35)
for _, row in ev.iterrows():
    ax.annotate(row["event"], xy=(row["year"], row["unemployment_rate_pct"]),
                xytext=(0, 10), textcoords="offset points", fontsize=8, ha='center', color="#333")
ax.set_ylabel("Unemployment rate (%)")
ax.set_title("West Germany / Germany Unemployment Rate, 1956–2025", fontsize=12, fontweight='bold')
ax.spines[['top','right']].set_visible(False)
ax.yaxis.grid(True, color='#e5e5e5', linewidth=0.8)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig("long_run_unemployment.png", dpi=150)
plt.close()

# Chart 3: 2025 state snapshot (partial)
snap_sorted = snap.sort_values("rate_2025_pct")
colors = [GREEN if "national" in r.lower() else BLUE for r in snap_sorted["region"]]
fig, ax = plt.subplots(figsize=(6.8,3.8), dpi=150)
bars = ax.barh(snap_sorted["region"], snap_sorted["rate_2025_pct"], color=colors)
for bar, val in zip(bars, snap_sorted["rate_2025_pct"]):
    ax.text(val+0.15, bar.get_y()+bar.get_height()/2, f"{val:.1f}%", va='center', fontsize=9)
ax.set_xlabel("Unemployment rate, 2025 (%)")
ax.set_title("2025 Snapshot: A Few States Compared\n(as reported by Destatis/Statistik-BW; not all 16 states)", fontsize=11, fontweight='bold')
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig("state_snapshot_2025.png", dpi=150)
plt.close()
print("done")
