"""Build the SQLite database and run the documented SQL queries.

Creates bahn.db from data/db_performance.csv, executes every query in
sql/queries.sql and writes the results to outputs/sql_results.md.
"""
import sqlite3
import pandas as pd

COLS = {
    "year": "INTEGER PRIMARY KEY",
    "punctuality_long_distance_pct": "REAL",
    "punctuality_regional_pct": "REAL",
    "passengers_long_distance_mn": "REAL",
    "passengers_regional_mn": "REAL",
    "passengers_rail_germany_mn": "REAL",
    "revenues_eur_mn": "REAL",
    "gross_capex_eur_mn": "REAL",
    "infra_delay_lost_units_per_day": "REAL",
}


def main():
    df = pd.read_csv("data/db_performance.csv")
    con = sqlite3.connect("bahn.db")
    con.execute("DROP TABLE IF EXISTS db_performance")
    con.execute("CREATE TABLE db_performance (%s)" % ", ".join(
        f"{c} {t}" for c, t in COLS.items()))
    df.to_sql("db_performance", con, if_exists="append", index=False)

    sql = open("sql/queries.sql").read()
    blocks = [b.strip() for b in sql.split("\n\n") if b.strip()]
    out = ["# SQL query results (SQLite, bahn.db)\n",
           "Queries are defined in `sql/queries.sql`; the database is built "
           "from `data/db_performance.csv` by `src/build_db.py`.\n"]
    for block in blocks:
        lines = [ln for ln in block.splitlines() if ln.strip()]
        title = lines[0].lstrip("- ").strip()
        query = "\n".join(ln for ln in lines if not ln.startswith("--"))
        if not query.strip():
            continue  # file header comment block
        res = pd.read_sql_query(query, con)
        out.append(f"## {title}\n")
        out.append("```sql\n" + query.strip() + "\n```\n")
        out.append(res.to_markdown(index=False) + "\n")
    open("outputs/sql_results.md", "w").write("\n".join(out))
    n = con.execute("SELECT COUNT(*) FROM db_performance").fetchone()[0]
    con.close()
    print(f"bahn.db built ({n} yearly rows); outputs/sql_results.md written")


if __name__ == "__main__":
    main()
