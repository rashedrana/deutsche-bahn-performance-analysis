# SQL query results (SQLite, bahn.db)

Queries are defined in `sql/queries.sql`; the database is built from `data/db_performance.csv` by `src/build_db.py`.

## Q1: The full compiled series

```sql
SELECT * FROM db_performance ORDER BY year;
```

|   year |   punctuality_long_distance_pct |   punctuality_regional_pct |   passengers_long_distance_mn |   passengers_regional_mn |   passengers_rail_germany_mn |   revenues_eur_mn |   gross_capex_eur_mn |   infra_delay_lost_units_per_day |
|-------:|--------------------------------:|---------------------------:|------------------------------:|-------------------------:|-----------------------------:|------------------:|---------------------:|---------------------------------:|
|   2010 |                            72.4 |                      nan   |                         126   |                     1824 |                         1950 |             34410 |                 6891 |                              nan |
|   2011 |                            80   |                       95.1 |                         125   |                     1801 |                         1926 |             37979 |                 7501 |                              nan |
|   2012 |                            79.1 |                       94.9 |                         131   |                     1844 |                         1974 |             39296 |                 8053 |                              nan |
|   2013 |                            73.9 |                       94.6 |                         131   |                     1885 |                         2016 |             39107 |                 8224 |                              nan |
|   2014 |                            76.5 |                       94.9 |                         129   |                     1901 |                         2030 |             39720 |                  nan |                              nan |
|   2015 |                            74.4 |                       94.2 |                         131.9 |                     1883 |                         2015 |             40403 |                 9344 |                              nan |
|   2016 |                            78.9 |                       94.8 |                         139   |                     1883 |                         2022 |             40557 |                 9510 |                              nan |
|   2017 |                            78.5 |                       94.4 |                         142.2 |                     1933 |                         2075 |             42693 |                10464 |                              nan |
|   2018 |                            74.9 |                       94   |                         147.9 |                     1940 |                         2088 |             44065 |                11205 |                              nan |
|   2019 |                            75.9 |                       94.3 |                         150.7 |                     1972 |                         2123 |             44430 |                13093 |                              nan |
|   2020 |                            81.8 |                       95.8 |                          81.3 |                     1215 |                         1297 |             39901 |                14402 |                             3317 |
|   2021 |                            75.2 |                       94.6 |                          82   |                     1121 |                         1203 |             47075 |                15387 |                             3861 |
|   2022 |                            65.2 |                       92.2 |                         132   |                     1605 |                         1737 |             52085 |                15098 |                             5162 |
|   2023 |                            64   |                       91.4 |                         140.3 |                     1697 |                         1837 |             26087 |                15917 |                             5279 |
|   2024 |                            62.5 |                       90.7 |                         133.4 |                     1733 |                         1867 |             26203 |                18247 |                             5998 |

## Q2: The worst long-distance punctuality years (below 70%)

```sql
SELECT year, punctuality_long_distance_pct
FROM db_performance
WHERE punctuality_long_distance_pct < 70
ORDER BY year;
```

|   year |   punctuality_long_distance_pct |
|-------:|--------------------------------:|
|   2022 |                            65.2 |
|   2023 |                            64   |
|   2024 |                            62.5 |

## Q3: Period averages - pre-COVID decade, COVID years, flat-fare era

```sql
SELECT CASE
         WHEN year <= 2019 THEN '2010-2019 pre-COVID'
         WHEN year <= 2021 THEN '2020-2021 COVID'
         ELSE '2022-2024 flat-fare era' END AS period,
       ROUND(AVG(punctuality_long_distance_pct), 1) AS avg_ld_punctuality,
       ROUND(AVG(punctuality_regional_pct), 1) AS avg_reg_punctuality,
       ROUND(AVG(passengers_long_distance_mn), 1) AS avg_ld_passengers_mn,
       ROUND(AVG(passengers_regional_mn), 0) AS avg_reg_passengers_mn,
       ROUND(AVG(gross_capex_eur_mn), 0) AS avg_gross_capex_eur_mn
FROM db_performance
GROUP BY period
ORDER BY MIN(year);
```

| period                  |   avg_ld_punctuality |   avg_reg_punctuality |   avg_ld_passengers_mn |   avg_reg_passengers_mn |   avg_gross_capex_eur_mn |
|:------------------------|---------------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|
| 2010-2019 pre-COVID     |                 76.5 |                  94.6 |                  135.4 |                    1887 |                     9365 |
| 2020-2021 COVID         |                 78.5 |                  95.2 |                   81.7 |                    1168 |                    14895 |
| 2022-2024 flat-fare era |                 63.9 |                  91.4 |                  135.2 |                    1678 |                    16421 |

## Q4: Year-on-year changes in long-distance punctuality and total passengers

```sql
SELECT year,
       ROUND(punctuality_long_distance_pct
             - LAG(punctuality_long_distance_pct) OVER (ORDER BY year), 1)
         AS ld_punctuality_change_pp,
       ROUND(100.0 * (passengers_rail_germany_mn
             - LAG(passengers_rail_germany_mn) OVER (ORDER BY year))
             / LAG(passengers_rail_germany_mn) OVER (ORDER BY year), 1)
         AS total_passengers_change_pct
FROM db_performance
ORDER BY year;
```

|   year |   ld_punctuality_change_pp |   total_passengers_change_pct |
|-------:|---------------------------:|------------------------------:|
|   2010 |                      nan   |                         nan   |
|   2011 |                        7.6 |                          -1.2 |
|   2012 |                       -0.9 |                           2.5 |
|   2013 |                       -5.2 |                           2.1 |
|   2014 |                        2.6 |                           0.7 |
|   2015 |                       -2.1 |                          -0.7 |
|   2016 |                        4.5 |                           0.3 |
|   2017 |                       -0.4 |                           2.6 |
|   2018 |                       -3.6 |                           0.6 |
|   2019 |                        1   |                           1.7 |
|   2020 |                        5.9 |                         -38.9 |
|   2021 |                       -6.6 |                          -7.2 |
|   2022 |                      -10   |                          44.4 |
|   2023 |                       -1.2 |                           5.8 |
|   2024 |                       -1.5 |                           1.6 |

## Q5: The COVID window in detail (2019 baseline vs 2020-2022)

```sql
SELECT year, punctuality_long_distance_pct, punctuality_regional_pct,
       passengers_long_distance_mn, passengers_regional_mn,
       passengers_rail_germany_mn
FROM db_performance
WHERE year BETWEEN 2019 AND 2022
ORDER BY year;
```

|   year |   punctuality_long_distance_pct |   punctuality_regional_pct |   passengers_long_distance_mn |   passengers_regional_mn |   passengers_rail_germany_mn |
|-------:|--------------------------------:|---------------------------:|------------------------------:|-------------------------:|-----------------------------:|
|   2019 |                            75.9 |                       94.3 |                         150.7 |                     1972 |                         2123 |
|   2020 |                            81.8 |                       95.8 |                          81.3 |                     1215 |                         1297 |
|   2021 |                            75.2 |                       94.6 |                          82   |                     1121 |                         1203 |
|   2022 |                            65.2 |                       92.2 |                         132   |                     1605 |                         1737 |

## Q6: Recovery by 2024 relative to 2019 (percent of the 2019 level)

```sql
SELECT ROUND(100.0 * a.passengers_long_distance_mn
             / b.passengers_long_distance_mn, 1) AS ld_passengers_pct_of_2019,
       ROUND(100.0 * a.passengers_regional_mn
             / b.passengers_regional_mn, 1) AS reg_passengers_pct_of_2019,
       ROUND(100.0 * a.passengers_rail_germany_mn
             / b.passengers_rail_germany_mn, 1) AS total_passengers_pct_of_2019,
       ROUND(a.punctuality_long_distance_pct
             - b.punctuality_long_distance_pct, 1) AS ld_punctuality_change_pp,
       ROUND(a.punctuality_regional_pct
             - b.punctuality_regional_pct, 1) AS reg_punctuality_change_pp
FROM db_performance a, db_performance b
WHERE a.year = 2024 AND b.year = 2019;
```

|   ld_passengers_pct_of_2019 |   reg_passengers_pct_of_2019 |   total_passengers_pct_of_2019 |   ld_punctuality_change_pp |   reg_punctuality_change_pp |
|----------------------------:|-----------------------------:|-------------------------------:|---------------------------:|----------------------------:|
|                        88.5 |                         87.9 |                           87.9 |                      -13.4 |                        -3.6 |

## Q7: Gross capital expenditures by period (EUR million; 2014 not published)

```sql
SELECT CASE WHEN year <= 2019 THEN '2010-2019' ELSE '2020-2024' END AS period,
       COUNT(gross_capex_eur_mn) AS years_available,
       SUM(gross_capex_eur_mn) AS total_gross_capex_eur_mn,
       ROUND(AVG(gross_capex_eur_mn), 0) AS avg_gross_capex_eur_mn
FROM db_performance
GROUP BY period
ORDER BY MIN(year);
```

| period    |   years_available |   total_gross_capex_eur_mn |   avg_gross_capex_eur_mn |
|:----------|------------------:|---------------------------:|-------------------------:|
| 2010-2019 |                 9 |                      84285 |                     9365 |
| 2020-2024 |                 5 |                      79051 |                    15810 |

## Q8: Years in which investment rose but long-distance punctuality fell

```sql
SELECT year,
       ROUND(100.0 * (gross_capex_eur_mn
             - LAG(gross_capex_eur_mn) OVER (ORDER BY year))
             / LAG(gross_capex_eur_mn) OVER (ORDER BY year), 1)
         AS capex_change_pct,
       ROUND(punctuality_long_distance_pct
             - LAG(punctuality_long_distance_pct) OVER (ORDER BY year), 1)
         AS ld_punctuality_change_pp
FROM db_performance
WHERE gross_capex_eur_mn IS NOT NULL
ORDER BY year;
```

|   year |   capex_change_pct |   ld_punctuality_change_pp |
|-------:|-------------------:|---------------------------:|
|   2010 |              nan   |                      nan   |
|   2011 |                8.9 |                        7.6 |
|   2012 |                7.4 |                       -0.9 |
|   2013 |                2.1 |                       -5.2 |
|   2015 |               13.6 |                        0.5 |
|   2016 |                1.8 |                        4.5 |
|   2017 |               10   |                       -0.4 |
|   2018 |                7.1 |                       -3.6 |
|   2019 |               16.8 |                        1   |
|   2020 |               10   |                        5.9 |
|   2021 |                6.8 |                       -6.6 |
|   2022 |               -1.9 |                      -10   |
|   2023 |                5.4 |                       -1.2 |
|   2024 |               14.6 |                       -1.5 |

## Q9: Infrastructure-related delays vs long-distance punctuality (2020-2024)

```sql
SELECT year, infra_delay_lost_units_per_day, punctuality_long_distance_pct
FROM db_performance
WHERE infra_delay_lost_units_per_day IS NOT NULL
ORDER BY year;
```

|   year |   infra_delay_lost_units_per_day |   punctuality_long_distance_pct |
|-------:|---------------------------------:|--------------------------------:|
|   2020 |                             3317 |                            81.8 |
|   2021 |                             3861 |                            75.2 |
|   2022 |                             5162 |                            65.2 |
|   2023 |                             5279 |                            64   |
|   2024 |                             5998 |                            62.5 |
