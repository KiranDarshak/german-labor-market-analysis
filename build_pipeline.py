import sys
sys.path.insert(0, 'data')
from raw_series import long_run, west_only_pre1991, state_snapshot_2025
import pandas as pd

# ---------------- BRONZE ----------------
bronze_rows = []
for (year, de_c, de_r, w_c, w_r, e_c, e_r) in long_run:
    bronze_rows.append({"year": year, "region": "Germany", "unemployed_count": de_c, "unemployment_rate_pct": de_r})
    bronze_rows.append({"year": year, "region": "West Germany", "unemployed_count": w_c, "unemployment_rate_pct": w_r})
    bronze_rows.append({"year": year, "region": "East Germany", "unemployed_count": e_c, "unemployment_rate_pct": e_r})
for (year, w_c, w_r) in west_only_pre1991:
    bronze_rows.append({"year": year, "region": "West Germany", "unemployed_count": w_c, "unemployment_rate_pct": w_r})
bronze = pd.DataFrame(bronze_rows).sort_values(["year","region"])
bronze.to_csv("data/bronze_unemployment_annual.csv", index=False)

bronze_snapshot = pd.DataFrame(state_snapshot_2025, columns=["region","rate_2025_pct","rate_2024_pct"])
bronze_snapshot.to_csv("data/bronze_state_snapshot_2025.csv", index=False)

# ---------------- SILVER ----------------
silver = bronze.copy()
silver.to_csv("data/silver_unemployment_annual.csv", index=False)

# ---------------- GOLD ----------------
# mart 1: east-west convergence gap, 1991-2025
piv = bronze[bronze["year"]>=1991].pivot_table(index="year", columns="region", values="unemployment_rate_pct")
mart_gap = piv.reset_index()
mart_gap["east_west_gap_pp"] = (mart_gap["East Germany"] - mart_gap["West Germany"]).round(1)
mart_gap.to_csv("data/mart_east_west_convergence.csv", index=False)

# mart 2: long-run west germany / germany series with key economic-event flags
long_west = bronze[bronze["region"]=="West Germany"].sort_values("year").copy()
events = {
    1967: "Post-war recession",
    1974: "Oil crisis",
    1982: "Second oil shock peak",
    1991: "Reunification",
    2005: "Hartz reforms era peak",
    2009: "Global financial crisis",
    2020: "COVID-19",
}
long_west["event"] = long_west["year"].map(events)
long_west.to_csv("data/mart_long_run_west_germany.csv", index=False)

# mart 3: 2025 state snapshot (partial, as-reported)
bronze_snapshot.to_csv("data/mart_state_snapshot_2025.csv", index=False)

print(mart_gap.tail(10).to_string(index=False))
print("---")
print("Gap 2005:", mart_gap[mart_gap.year==2005]["east_west_gap_pp"].values)
print("Gap 2025:", mart_gap[mart_gap.year==2025]["east_west_gap_pp"].values)
print("Peak gap:", mart_gap.loc[mart_gap["east_west_gap_pp"].idxmax()])
