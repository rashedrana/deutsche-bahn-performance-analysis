# Data sources and audit trail

Dataset: `data/db_performance.csv` (compiled by `src/compile_data.py`).
All values are transcribed from published sources listed below — no
estimates, no interpolation. Empty cells mean: no consistent published
figure could be verified (see "Gaps and decisions").

## Primary sources (Deutsche Bahn publications)

1. **Deutsche Bahn AG, *Daten & Fakten 2013*** (as of 14 March 2014),
   ir.deutschebahn.com/fileadmin/Deutsch/2013/Berichte/2013_duf_de.pdf
   — Multi-year summaries (pp. 26–31): passengers by unit, revenues,
   gross/net capital expenditures, 2010–2013. Quality table (p. 8):
   punctuality DB Bahn Fernverkehr / DB Bahn Regio, 2011–2013.
2. **Deutsche Bahn AG, *Geschäftsbericht 2011*** — punctuality 2010/2011:
   long-distance 72.4% / 80.0% (five-minute punctuality report).
3. **Deutsche Bahn AG, *Facts & Figures 2019*** (Strong Rail targets page
   and quality figures) — punctuality long-distance/regional 2015–2019;
   passengers long-distance (131.9 / 139.0 / 142.2 / 147.9 / 150.7 mn) and
   regional (1,883 / 1,883 / 1,933 / 1,940 / 1,972 mn), 2015–2019.
4. **Deutsche Bahn AG, *Facts & Figures 2020*** — long-distance
   punctuality 2020 (81.8%); long-distance passengers 2020 (81.3 mn);
   regional passengers 2020 (1,215 mn).
5. **Deutsche Bahn AG, *Facts & Figures 2024*** (March 2025),
   ir.deutschebahn.com/fileadmin/Deutsch/2025/DB_DuF_e_2024.pdf
   — Mid-term restructuring targets page: punctuality long-distance
   2020–2024 (81.8 / 75.2 / 65.2 / 64.0 / 62.5) and DB Regional
   2020–2024 (95.8 / 94.6 / 92.2 / 91.4 / 90.7, third-weighted);
   infrastructure-related delays (lost units per day) 2020–2024
   (3,317 / 3,861 / 5,162 / 5,279 / 5,998). Quality figures 2022–2024.
   10-year summaries: passengers by unit, statement of income (revenues),
   cash flow/capital expenditures, 2015–2024.
6. **Deutsche Bahn AG, *Integrated Report 2024*** (ibir.deutschebahn.com)
   — key figures: revenues 2023/2024 (€26,087 mn / €26,203 mn, continuing
   operations); rail passengers in Germany 2023/2024 (1,837 / 1,867 mn);
   long-distance passengers 2023/2024 (140.3 / 133.4 mn); punctuality
   table 2022–2024.
7. **Deutsche Bahn AG, *Integrated Report 2020*** — rail passengers in
   Germany 2020 (1,297 mn); DB rail passenger transport punctuality
   2020 (95.2%, all DB passenger services).
8. **Deutsche Bahn AG, annual results press releases** (ir.deutschebahn.com):
   March 2015 (financial year 2014): rail passengers in Germany 2014
   2,030 mn (+14 mn); long-distance passengers 129 mn (−1.5%); regional
   passengers +16 mn (→ 1,901 mn); revenues 2014 €39,720 mn (+€601 mn).
   March 2016 (financial year 2015): revenues 2015 €40,468 mn as
   originally reported; gross capital expenditures +2.4% in 2015.

## Official cross-check sources

9. **Deutscher Bundestag, Drucksache 19/1983** (answer of the Federal
   Government, BMVI letter of 30 April 2018; table supplied by DB AG):
   punctuality (≤5:59 min) 2010–2017 — long-distance 72.4 / 80.0 / 79.1 /
   73.9 / 76.5 / 74.4 / 78.9 / 78.5; regional 91.5 / 93.2 / 95.1 / 94.6 /
   94.9 / 94.2 / 94.8 / 94.4. Used here for **regional 2014 (94.9%)** and
   as a cross-check (see discrepancies below). Companion papers:
   Drucksache 19/3247 (delay minutes; long-distance punctuality
   2012–2017 identical) and Drucksache 19/9205 (train-related
   punctuality series 2009–2018, "Quelle: DB AG").
10. **tagesschau / dpa** (January 2025), reporting DB's official annual
    figures: long-distance punctuality 2024 = 62.5% (2023: 64.0%),
    the lowest in the dpa series back to 2003 (best: 84.3% in 2004);
    regional trains 2024 = 90.3% of stops on time.
11. **Destatis (Federal Statistical Office)**, press release April 2020
    (via Clean Energy Wire): 151 million long-distance rail passengers
    in Germany in 2019 (all operators) — cross-checks DB's 150.7 mn.

## Series-by-series provenance

| Series | 2010–2013 | 2014 | 2015–2019 | 2020–2024 |
| --- | --- | --- | --- | --- |
| Punctuality, long-distance (%) | DuF 2013 quality table (2011–13); GB 2011 (2010) | DB Fernverkehr AG *Geschäftsbericht 2014* (76.5%); Bundestag 19/1983 agrees | F&F 2019 | F&F 2024; IBIR 2024 (2022–24) |
| Punctuality, regional (%) | DuF 2013 quality table, DB Bahn Regio (2011–13) | Bundestag 19/1983 (DB AG data) | F&F 2019 | F&F 2024 (third-weighted) |
| Passengers, long-distance (mn) | DuF 2013 multi-year summary (rounded) | DB press release Mar 2015 | F&F 2019 (one decimal) | F&F 2020 (2020); F&F 2024 10-year summary (2021–22, rounded); IBIR 2024 (2023–24, one decimal) |
| Passengers, regional (mn) | DuF 2013 multi-year summary ("Regional- und Stadtverkehr, DB Bahn Regio und Sonstige") | DB press release Mar 2015 (+16 mn on 2013) | F&F 2019 / F&F 2024 | F&F 2024 |
| Passengers, rail Germany (mn) | DuF 2013 performance table (2012–13 published: 1,974 / 2,016); 2010 = published total (1,950); 2011 = sum of published components | DB press release Mar 2015 (2,030) | F&F 2019 / IBIR (2018–19 published: 2,088 / 2,123); 2015–17 = sum of published components | IBIR 2020 (2020: 1,297); F&F 2024 (2022–24: 1,737 / 1,837 / 1,867); 2021 = sum of published components |
| Revenues (€ mn) | DuF 2013 multi-year income statement | DB press release Mar 2015 (€39,720 mn, adjusted) | F&F 2024 10-year income statement (as restated) | F&F 2024 10-year income statement; IBIR 2024 |
| Gross capital expenditures (€ mn) | DuF 2013 multi-year cash flow table | — gap (see below) | F&F 2024 10-year cash flow table | F&F 2024 |
| Infrastructure-related delays (lost units/day) | — | — | — | F&F 2024 (series published from 2020) |

## Gaps and decisions

- **Regional punctuality 2010 — left empty.** The only 2010 figure in
  the official material (91.5%, Geschäftsbericht 2011 and Bundestag
  19/1983) refers to *all* DB local transport (Nahverkehr), a different
  aggregate from the DB (Bahn) Regio business unit published from 2011
  (95.1%). Mixing the two would silently change the series definition,
  so the regional series starts in 2011.
- **Gross capital expenditures 2014 — left empty.** The figure is not
  contained in the multi-year summaries consulted (DuF 2013 ends 2013;
  F&F 2024 begins 2015). DB's 2015 results press release states only
  that 2015 gross capex rose 2.4% (to €9,344 mn), implying ≈ €9.1 bn
  for 2014; an implied value is not a published value, so the cell
  stays empty.
- **Revenues are not one consistent scope.** DB restated its reporting
  repeatedly: IFRS 16 from 2019; DB Arriva shown as a discontinued
  operation from 2022 (€52,085 mn for 2022 vs €56,296 mn originally
  reported); DB Schenker from 2023, so 2023–2024 revenues
  (€26,087 mn / €26,203 mn) cover continuing operations only and are
  **not comparable** with earlier years. The dataset stores the values
  as published in the chains above; the analysis uses revenues
  descriptively only and excludes them from the break regressions.
- **Rounding seams.** Long-distance passengers 2010–2014 and 2021–2022
  are published rounded to whole millions in the multi-year summaries;
  other years have one decimal. Germany rail-passenger totals marked
  "sum of published components" in the table above can differ by ±1 mn
  from DB's published totals (e.g. components for 2024 sum to
  1,866.4 mn; DB publishes 1,867 mn — the published total is used).

## Discrepancies found while cross-checking

- Long-distance punctuality 2010: 72.4% (GB 2011; Bundestag 19/1983)
  vs 72.6% (Bundestag 19/9205). We use 72.4%.
- Regional punctuality 2012: 94.9% (DuF 2013, DB Bahn Regio) vs 95.1%
  (Bundestag 19/1983). We use the DB publication (94.9%). The
  Bundestag table's 2011 regional value (93.2%) equals DB's
  *Regionalzüge* sub-aggregate in DuF 2013, not the Regio business
  unit (95.1%), which is why the Bundestag table is used only for
  2014, where no DB quality table was available.
- Regional punctuality 2020: 95.8% (F&F 2024, third-weighted business
  unit) vs 95.6% of stops reported by dpa (all regional services).
  Different aggregates; we use DB's business-unit figure.
- Long-distance punctuality 2015–2017 and 2022–2024 agree *exactly*
  across DB publications, the Bundestag tables and press reporting —
  these are the anchor points of the dataset.
