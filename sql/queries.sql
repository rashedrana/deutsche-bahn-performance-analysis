-- Deutsche Bahn performance 2010-2024: analysis queries (SQLite).
-- Table: db_performance (one row per year), built by src/build_db.py from
-- data/db_performance.csv (Deutsche Bahn published key figures; sources
-- and audit trail in data/sources.md).

-- Q1: The full compiled series
SELECT * FROM db_performance ORDER BY year;

-- Q2: The worst long-distance punctuality years (below 70%)
SELECT year, punctuality_long_distance_pct
FROM db_performance
WHERE punctuality_long_distance_pct < 70
ORDER BY year;

-- Q3: Period averages - pre-COVID decade, COVID years, flat-fare era
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

-- Q4: Year-on-year changes in long-distance punctuality and total passengers
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

-- Q5: The COVID window in detail (2019 baseline vs 2020-2022)
SELECT year, punctuality_long_distance_pct, punctuality_regional_pct,
       passengers_long_distance_mn, passengers_regional_mn,
       passengers_rail_germany_mn
FROM db_performance
WHERE year BETWEEN 2019 AND 2022
ORDER BY year;

-- Q6: Recovery by 2024 relative to 2019 (percent of the 2019 level)
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

-- Q7: Gross capital expenditures by period (EUR million; 2014 not published)
SELECT CASE WHEN year <= 2019 THEN '2010-2019' ELSE '2020-2024' END AS period,
       COUNT(gross_capex_eur_mn) AS years_available,
       SUM(gross_capex_eur_mn) AS total_gross_capex_eur_mn,
       ROUND(AVG(gross_capex_eur_mn), 0) AS avg_gross_capex_eur_mn
FROM db_performance
GROUP BY period
ORDER BY MIN(year);

-- Q8: Years in which investment rose but long-distance punctuality fell
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

-- Q9: Infrastructure-related delays vs long-distance punctuality (2020-2024)
SELECT year, infra_delay_lost_units_per_day, punctuality_long_distance_pct
FROM db_performance
WHERE infra_delay_lost_units_per_day IS NOT NULL
ORDER BY year;
