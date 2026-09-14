# German Labor Market: East-West Convergence (1956–2025)

A Bronze → Silver → Gold pipeline on real, official German unemployment data, tracking Germany's post-reunification East-West labor market convergence and the long historical arc of the West German/German unemployment rate back to 1956.

## Tools

Python · Pandas · matplotlib — pipeline structured the same way as my [German Motorcycle Market Analysis](https://github.com/KiranDarshak/germany-motorcycle-market-analysis) and [German Electricity Market Analysis](https://github.com/KiranDarshak/german-electricity-market-analysis) projects (Bronze/Silver/Gold Medallion architecture).

## Data sources

- **Statistisches Bundesamt (Destatis), "Lange Reihen" series** — [Registrierte Arbeitslose und Arbeitslosenquote nach Gebietsstand](https://www.destatis.de/DE/Themen/Wirtschaft/Konjunkturindikatoren/Lange-Reihen/Arbeitsmarkt/lrarb003ga.html), sourced from Statistik der Bundesagentur für Arbeit. Annual unemployment count and rate for Germany, former West Germany, and the new federal states (former East Germany), 1956–2025.
- **Statistisches Landesamt Baden-Württemberg** press release, ["Arbeitslosigkeit 2025 erneut gestiegen"](https://www.statistik-bw.de/presse/pressemitteilungen/pressemitteilung/arbeitslosigkeit-2025-erneut-gestiegen/) — a handful of individual 2025 state-level rates explicitly quoted in the release.

## Pipeline

- **Bronze** (`data/bronze_unemployment_annual.csv`, `data/bronze_state_snapshot_2025.csv`) — figures exactly as published.
- **Silver** (`data/silver_unemployment_annual.csv`) — standardized long format (year, region, count, rate).
- **Gold** — three marts:
  - `mart_east_west_convergence.csv` — East/West/Germany rates side by side, 1991–2025, with a computed year-by-year percentage-point gap
  - `mart_long_run_west_germany.csv` — full 1956–2025 West German/German series with key economic-event flags
  - `mart_state_snapshot_2025.csv` — the individual 2025 state figures explicitly reported by Destatis/Statistik-BW (**not** all 16 Bundesländer — see Notes)

## Key findings

- **The East-West unemployment gap has narrowed from 10.8 percentage points at its widest (2001: East 18.8% vs West 8.0%) to just 2.2pp in 2025 (East 8.6% vs West 6.4%)** — real convergence, though the gap hasn't fully closed even 35 years after reunification.
- **Nationwide unemployment has risen for three straight years**: 5.8% (2022) → 6.2% (2023) → 6.5% (2024) → 6.8% (2025).
- **The 1956–2025 view puts today's rate in historical context**: still well below the mid-2000s Hartz-reform-era peak (11.0% in 2005) and the 2009 financial-crisis level (8.7%), but above the pre-pandemic low of 5.1% (2019).
- **State-level spread in 2025 is wide**: from 4.0% in Bavaria to 11.5% in Bremen, an almost 3x difference within one country.

## Repo structure

```
data/
  bronze_unemployment_annual.csv
  bronze_state_snapshot_2025.csv
  silver_unemployment_annual.csv
  mart_east_west_convergence.csv
  mart_long_run_west_germany.csv
  mart_state_snapshot_2025.csv
  raw_series.py                 # raw figures as published, source of truth for bronze layer
build_pipeline.py               # Bronze -> Silver -> Gold transform
make_charts.py                  # chart generation
east_west_convergence.png
long_run_unemployment.png
state_snapshot_2025.png
README.md
```

## Notes on data

The West/East/Germany annual series (1956–2025) is complete and official. The 2025 individual-state snapshot is **partial by nature of the source** — it includes only the states a Baden-Württemberg state-statistics press release happened to name with an exact figure (Bavaria, Baden-Württemberg, Hamburg, Berlin, Bremen) alongside the national average; it is presented as a snapshot, not a full 16-state ranking. A natural follow-up would pull the complete state-by-state series from Destatis GENESIS-Online (registration required for full API access).
