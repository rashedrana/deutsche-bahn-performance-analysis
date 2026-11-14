"""Compile the analysis dataset from Deutsche Bahn's published key figures.

Unlike the sister projects (which download OWID/IEA series), Deutsche Bahn
publishes its annual key figures only inside its reports (Daten & Fakten /
Facts & Figures / Integrated Reports). This script therefore assembles the
dataset from values transcribed from those publications; every series is
documented, with its source publication, in data/sources.md. Nothing here
is estimated or interpolated: where no consistent published figure exists,
the cell is left empty (NaN) and the gap is documented in data/sources.md.

Sources used (see data/sources.md for the full audit trail):
  * Deutsche Bahn, Daten & Fakten 2013 (multi-year summaries, quality table)
  * Deutsche Bahn, Facts & Figures 2019 and 2024 (Strong Rail target pages,
    quality figures, 10-year summaries)
  * Deutsche Bahn, Facts & Figures 2020 (punctuality/passenger chains)
  * Deutsche Bahn, Integrated Report 2020 and 2024 (key figures)
  * Deutsche Bahn, Geschäftsbericht 2011 (2010/2011 punctuality)
  * Deutsche Bahn, annual results press releases, March 2015 / March 2016
    (2014 passengers, revenues and the 2014->2015 investment growth rate)
  * Deutscher Bundestag, Drucksache 19/1983 (Federal Government answer of
    30 Apr 2018; punctuality table supplied by DB AG) - regional 2014 and
    cross-checks for 2010-2017
Output: data/db_performance.csv
"""
import numpy as np
import pandas as pd

NAN = np.nan

# year: (punctuality LD %, punctuality regional %, LD passengers mn,
#        regional passengers mn, rail passengers Germany mn,
#        revenues EUR mn, gross capital expenditures EUR mn,
#        infrastructure-related delay lost units per day)
ROWS = {
    2010: (72.4, NAN, 126, 1824, 1950, 34410, 6891, NAN),
    2011: (80.0, 95.1, 125, 1801, 1926, 37979, 7501, NAN),
    2012: (79.1, 94.9, 131, 1844, 1974, 39296, 8053, NAN),
    2013: (73.9, 94.6, 131, 1885, 2016, 39107, 8224, NAN),
    2014: (76.5, 94.9, 129, 1901, 2030, 39720, NAN, NAN),
    2015: (74.4, 94.2, 131.9, 1883, 2015, 40403, 9344, NAN),
    2016: (78.9, 94.8, 139.0, 1883, 2022, 40557, 9510, NAN),
    2017: (78.5, 94.4, 142.2, 1933, 2075, 42693, 10464, NAN),
    2018: (74.9, 94.0, 147.9, 1940, 2088, 44065, 11205, NAN),
    2019: (75.9, 94.3, 150.7, 1972, 2123, 44430, 13093, NAN),
    2020: (81.8, 95.8, 81.3, 1215, 1297, 39901, 14402, 3317),
    2021: (75.2, 94.6, 82, 1121, 1203, 47075, 15387, 3861),
    2022: (65.2, 92.2, 132, 1605, 1737, 52085, 15098, 5162),
    2023: (64.0, 91.4, 140.3, 1697, 1837, 26087, 15917, 5279),
    2024: (62.5, 90.7, 133.4, 1733, 1867, 26203, 18247, 5998),
}

COLUMNS = ["year", "punctuality_long_distance_pct", "punctuality_regional_pct",
           "passengers_long_distance_mn", "passengers_regional_mn",
           "passengers_rail_germany_mn", "revenues_eur_mn",
           "gross_capex_eur_mn", "infra_delay_lost_units_per_day"]


def main():
    df = pd.DataFrame([{"year": y, **dict(zip(COLUMNS[1:], vals))}
                       for y, vals in sorted(ROWS.items())])
    df.to_csv("data/db_performance.csv", index=False)
    print(df.to_string(index=False))
    print("\nwrote data/db_performance.csv", df.shape)


if __name__ == "__main__":
    main()
