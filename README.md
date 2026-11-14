# Deutsche Bahn Performance, 2010–2024: Punctuality, Passengers and Two Structural Breaks

A reproducible data-analysis project on the performance of Deutsche Bahn (DB), Germany's national railway, across fifteen years that contain two structural breaks: the COVID-19 pandemic (2020–2021) and the flat-fare era that began with the 9-Euro-Ticket (summer 2022) and continued with the Deutschlandticket (from May 2023). Using DB's own published annual key figures, the project shows that long-distance punctuality was essentially *flat* for a decade — and then collapsed by more than twelve percentage points within three years, even though investment rose to record levels and passenger numbers had still not recovered to their pre-pandemic level by 2024.

**Data (100% real, published sources):** every value comes from Deutsche Bahn's own annual publications — the *Daten & Fakten* / *Facts & Figures* booklets (2013, 2019, 2020, 2024 editions), the Integrated Reports and Geschäftsberichte, and DB's annual-results press releases — cross-checked against the German Bundestag's published answers to parliamentary questions (Drucksachen 19/1983, 19/3247, 19/9205, which reproduce DB AG's own punctuality tables), Destatis and dpa/tagesschau reporting of DB's official figures. The compiled dataset (8 series, 2010–2024) ships in `data/db_performance.csv`; `data/sources.md` documents the source of every series, the cross-checks performed, the discrepancies found (and how they were resolved), and the two cells that were deliberately left empty because no consistent published figure exists (regional punctuality 2010; gross capital expenditures 2014).

## Key findings

1. **Long-distance punctuality did not decline gradually — it broke.** From 2010 to 2019 it oscillated around ~76.5% with no trend (OLS slope +0.04 percentage points per year, p = 0.91). After a pandemic spike to a series-record 81.8% in 2020, it fell to 65.2% (2022), 64.0% (2023) and 62.5% (2024) — 13.4 points below 2019 and the lowest value in the published record. Extending the 2010–2019 trend predicts 76.8% for 2024; the actual shortfall is 14.3 points.
2. **Two-break models fit the data far better than any trend.** For long-distance punctuality, adding level shifts for COVID-19 (2020–2021) and the post-2022 era raises R² from 0.34 to 0.83 (Chow-style F = 15.6, p < 0.001); the post-2022 shift is −12.2 points (p = 0.003). Regional punctuality shows the same pattern at a higher level: a slow pre-2020 erosion (−0.11 points per year), a +1.4-point COVID shift, and a −2.1-point post-2022 shift (model R² = 0.94).
3. **The pandemic produced a punctuality paradox.** In 2020 long-distance passengers collapsed by 46.1% (150.7 → 81.3 million) while long-distance punctuality hit its record high — emptier railways ran on time. Across the whole window, punctuality and passenger volume are only weakly related (r = −0.27, not significant); the co-movement is driven by the two break regimes, not by demand itself.
4. **The recovery was still incomplete at the end of 2024.** Rail passengers in Germany reached only 87.9% of their 2019 level (1,867 vs 2,123 million): long-distance 88.5% (133.4 vs 150.7 million), regional 87.9% (1,733 vs 1,972 million). Regional ridership rebounded +43.2% in 2022 (the 9-Euro-Ticket summer) and grew a further +5.7% in the Deutschlandticket's first full year — but from a deep trough: at its 2024 growth rate (+2.1%), regional ridership would need about six more years to regain 2019. Long-distance ridership actually *fell* 4.9% in 2024.
5. **A break model with a dedicated Deutschlandticket dummy (2023–2024) finds no measurable level effect on regional ridership beyond trend and COVID recovery** (−5.4%, p = 0.36) — by the end of 2024, the flat-fare era had restored growth but not levels. This is an honest null result for annual data: monthly studies cited in the paper find clear first-month gains from a low base.
6. **Investment and punctuality moved in opposite directions.** Gross capital expenditures rose 164.8%, from €6,891 million (2010) to a record €18,247 million (2024); the 2020–2024 total (€79.1 billion) exceeded 2015–2019 (€53.6 billion) by half. The raw correlation between investment and long-distance punctuality is negative (r = −0.60) — but it is entirely a post-2019 phenomenon (pre-2020: r = +0.01): money and failure both surged in the same regime, and the dataset cannot separate construction disruption, backlog effects and lags.
7. **Infrastructure-related delays surged.** DB's own restructuring metric — lost units per day caused by the infrastructure — rose 80.8%, from 3,317 (2020) to 5,998 (2024), tracking the punctuality collapse almost one-for-one (r = −0.98, five annual observations, descriptive only).

## Related work

Several public projects analyse Deutsche Bahn *operational* data; this project is deliberately different in kind:

- **[piebro/deutsche-bahn-data](https://github.com/piebro/deutsche-bahn-data)** collects timetable and delay data from DB's public API several times a day (about 100 major stations from July 2024, all stations from November 2025) and publishes an open dataset and a statistics website. It is data infrastructure for station-level, high-frequency delay analysis — not an annual company-performance study, and it carries no econometric break analysis or paper.
- **[Splines/deutsche-bahn-analysis](https://github.com/Splines/deutsche-bahn-analysis)** (last updated 2023) analyses DB delays from operational data. Again: operational micro-data, not the official annual key figures, and no journal-style paper.
- **David Kriesel's "BahnMining"** (36C3 talk, 2019) mined years of scraped timetable data to expose systematic delay patterns. A conference talk based on scraped data — not a reproducible study of DB's published annual figures.

**How this project differs:** it uses only DB's *official annual key figures* from its published reports (each series with a documented source in `data/sources.md`), covers a long, consistent 2010–2024 window, applies econometric structural-break models to the two defining shocks of the period (COVID-19 and the Deutschlandticket era), adds a documented SQL component, and ships a fully reproducible dataset and a journal-format paper. The projects above can validate DB's statistics from below; this one audits them from the company's own publications.

## Project structure

```
deutsche-bahn-performance-analysis/
├── data/
│   ├── db_performance.csv     <- compiled dataset (8 series, 2010-2024)
│   └── sources.md             <- source of every series, cross-checks, gaps
├── src/
│   ├── compile_data.py        <- assembles the dataset from the sourced values
│   ├── analysis.py            <- trends, two-break OLS models, recovery, correlations
│   ├── build_db.py            <- builds bahn.db, runs the SQL queries
│   └── figures.py             <- all eight figures
├── sql/
│   └── queries.sql            <- 9 documented SQLite queries
├── outputs/
│   ├── results.json           <- every headline number (machine-readable)
│   ├── db_yearly.csv
│   ├── sql_results.md         <- query results
│   └── figures/               <- fig1..fig8 (PNG)
├── paper/
│   ├── paper.md               <- the scientific paper (Markdown)
│   ├── paper_twocol.md        <- identical text, two-column journal layout
│   └── build_journal.py       <- builds DOCX + PDF in both layouts
├── requirements.txt
└── README.md
```

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/compile_data.py   # writes data/db_performance.csv
python src/analysis.py       # writes outputs/results.json, outputs/db_yearly.csv
python src/build_db.py       # writes bahn.db, outputs/sql_results.md
python src/figures.py        # writes outputs/figures/*.png
python paper/build_journal.py paper/paper.md                    # single-column DOCX + PDF
python paper/build_journal.py paper/paper_twocol.md --two-col   # two-column journal DOCX + PDF
```

## Paper

Rana, R. (2026). *From Pandemic Shock to Deutschlandticket: Structural Breaks in Deutsche Bahn's Punctuality and Passenger Performance, 2010–2024.* Manuscript in `paper/` (two-column journal format and single-column version). The manuscript was prepared with AI assistance for data analysis and drafting, under the author's direction; all results were computed from the published sources listed in `data/sources.md` with the code in this repository. Paper PDFs are deliberately **not** included in this repository (only the Markdown and Word sources); the author will release the PDF with the journal submission.
