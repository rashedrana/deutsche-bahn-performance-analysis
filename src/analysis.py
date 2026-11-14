"""Deutsche Bahn performance, 2010-2024: punctuality, passengers, investment.

Main analysis for the project *deutsche-bahn-performance-analysis*.
Data: data/db_performance.csv, compiled by src/compile_data.py from
Deutsche Bahn's published annual key figures (Daten & Fakten / Facts &
Figures / Integrated Reports), cross-checked against Bundestag papers
and press reporting - see data/sources.md for the full audit trail.

The study is built around two structural breaks:
  * the COVID-19 shock (2020-2021), and
  * the flat-fare era that began with the 9-Euro-Ticket (Jun-Aug 2022)
    and continued with the Deutschlandticket (from 1 May 2023, EUR 49).
Breaks are modelled as level-shift dummies in OLS trend models, with
Chow-style F-tests against the no-break model. All headline numbers are
written to outputs/results.json; nothing in the README or the paper is
typed by hand.
"""
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm

LD = "punctuality_long_distance_pct"
RG = "punctuality_regional_pct"
PLD = "passengers_long_distance_mn"
PRG = "passengers_regional_mn"
PDE = "passengers_rail_germany_mn"
REV = "revenues_eur_mn"
CAP = "gross_capex_eur_mn"
INF = "infra_delay_lost_units_per_day"


def ols(y, X):
    return sm.OLS(np.asarray(y, float), X).fit()


def trend(df, col, y0, y1):
    """OLS of col on time over [y0, y1]: slope, R^2, p(slope)."""
    d = df[(df.year >= y0) & (df.year <= y1)].dropna(subset=[col])
    X = sm.add_constant((d.year - y0).astype(float).values)
    m = ols(d[col], X)
    return {"slope_per_year": round(float(m.params[1]), 3),
            "r2": round(float(m.rsquared), 3),
            "p_slope": float(m.pvalues[1]), "n": int(len(d))}


def break_model(df, col, log=False, covid=True, shift2022=True,
                dticket=False):
    """OLS: y ~ t + covid(2020-21) + shift2022(2022-24) [+ dticket(2023-24)].
    Returns coefficients, p-values, R^2 and the Chow-style F-test of the
    full model against the no-break trend model."""
    d = df.dropna(subset=[col]).copy()
    t = (d.year - 2010).astype(float)
    cols = {"const": np.ones(len(d)), "t": t}
    if covid:
        cols["covid"] = ((d.year >= 2020) & (d.year <= 2021)).astype(float)
    if shift2022:
        cols["post2022"] = (d.year >= 2022).astype(float)
    if dticket:
        cols["dticket"] = (d.year >= 2023).astype(float)
    X = pd.DataFrame(cols)
    y = np.log(d[col]) if log else d[col]
    m = ols(y, X.values)
    base = ols(y, sm.add_constant(t.values))
    ftest = m.f_test(np.eye(len(cols))[2:]) if len(cols) > 2 else None
    out = {"r2": round(float(m.rsquared), 3), "n": int(len(d))}
    for i, name in enumerate(cols):
        out[f"coef_{name}"] = round(float(m.params[i]), 4)
        out[f"p_{name}"] = float(m.pvalues[i])
    if ftest is not None:
        out["f_breaks_vs_trend"] = round(float(ftest.fvalue), 2)
        out["p_breaks_vs_trend"] = float(ftest.pvalue)
    out["rss_ratio_check"] = round(float(base.ssr / m.ssr), 3)
    return out


def corr(df, a, b):
    d = df.dropna(subset=[a, b])
    r = float(np.corrcoef(d[a], d[b])[0, 1])
    from scipy import stats
    p = float(stats.pearsonr(d[a], d[b])[1])
    return {"r": round(r, 3), "p": p, "n": int(len(d))}


def main():
    df = pd.read_csv("data/db_performance.csv")
    R = {"years": [int(df.year.min()), int(df.year.max())],
         "n_years": int(len(df))}
    at = df.set_index("year")

    # --- Finding 1: levels and the punctuality decline -----------------------
    R["ld_punct_2010"] = float(at.loc[2010, LD])
    R["ld_punct_2019"] = float(at.loc[2019, LD])
    R["ld_punct_2020"] = float(at.loc[2020, LD])
    R["ld_punct_2024"] = float(at.loc[2024, LD])
    R["ld_punct_max_year"] = int(df.loc[df[LD].idxmax(), "year"])
    R["ld_punct_max"] = float(df[LD].max())
    R["ld_punct_change_2019_2024_pp"] = round(
        float(at.loc[2024, LD] - at.loc[2019, LD]), 1)
    R["ld_punct_change_2010_2024_pp"] = round(
        float(at.loc[2024, LD] - at.loc[2010, LD]), 1)
    R["reg_punct_2019"] = float(at.loc[2019, RG])
    R["reg_punct_2024"] = float(at.loc[2024, RG])
    R["reg_punct_change_2019_2024_pp"] = round(
        float(at.loc[2024, RG] - at.loc[2019, RG]), 1)
    R["reg_punct_max"] = float(df[RG].max())
    R["reg_punct_min_2024"] = float(at.loc[2024, RG])
    R["ld_trend_2010_2019"] = trend(df, LD, 2010, 2019)
    R["ld_trend_2010_2024"] = trend(df, LD, 2010, 2024)
    R["reg_trend_2011_2019"] = trend(df, RG, 2011, 2019)
    R["reg_trend_2011_2024"] = trend(df, RG, 2011, 2024)
    # counterfactual: 2010-2019 LD trend extended to 2022-2024
    pre = df[df.year <= 2019]
    Xm = sm.add_constant((pre.year - 2010).astype(float).values)
    tm = ols(pre[LD], Xm)
    for yr in (2022, 2023, 2024):
        pred = float(tm.params[0] + tm.params[1] * (yr - 2010))
        R[f"ld_punct_counterfactual_{yr}"] = round(pred, 1)
        R[f"ld_punct_gap_{yr}_pp"] = round(float(at.loc[yr, LD] - pred), 1)

    # --- Finding 2: the two-break models --------------------------------------
    R["model_ld_punct"] = break_model(df, LD)
    R["model_reg_punct"] = break_model(df, RG)
    R["model_ld_pax_log"] = break_model(df, PLD, log=True)
    R["model_reg_pax_log_shift"] = break_model(df, PRG, log=True)
    R["model_reg_pax_log_dticket"] = break_model(
        df, PRG, log=True, shift2022=False, dticket=True)
    for k in ["model_ld_punct", "model_reg_punct"]:
        m = R[k]
        m["post2022_pp"] = m["coef_post2022"]
    for k in ["model_ld_pax_log", "model_reg_pax_log_shift",
              "model_reg_pax_log_dticket"]:
        m = R[k]
        for name in ["covid", "post2022", "dticket"]:
            if f"coef_{name}" in m:
                m[f"{name}_pct"] = round(
                    float((np.exp(m[f"coef_{name}"]) - 1) * 100), 1)

    # --- Finding 3: COVID collapse and the incomplete recovery ----------------
    for col, key in [(PLD, "ld"), (PRG, "reg"), (PDE, "total")]:
        v19, v20, v21, v24 = (float(at.loc[y, col])
                              for y in (2019, 2020, 2021, 2024))
        R[f"pax_{key}_2019"] = v19
        R[f"pax_{key}_2020"] = v20
        R[f"pax_{key}_2021"] = v21
        R[f"pax_{key}_2024"] = v24
        R[f"pax_{key}_change_2019_2020_pct"] = round((v20 / v19 - 1) * 100, 1)
        R[f"pax_{key}_change_2019_2021_pct"] = round((v21 / v19 - 1) * 100, 1)
        R[f"pax_{key}_recovery_2024_pct_of_2019"] = round(v24 / v19 * 100, 1)
        R[f"pax_{key}_gap_2024_vs_2019"] = round(v24 - v19, 1)
    # regional rebound in the flat-fare era
    R["reg_pax_change_2021_2022_pct"] = round(
        float(at.loc[2022, PRG] / at.loc[2021, PRG] - 1) * 100, 1)
    R["reg_pax_change_2022_2023_pct"] = round(
        float(at.loc[2023, PRG] / at.loc[2022, PRG] - 1) * 100, 1)
    R["reg_pax_change_2023_2024_pct"] = round(
        float(at.loc[2024, PRG] / at.loc[2023, PRG] - 1) * 100, 1)
    R["ld_pax_change_2023_2024_pct"] = round(
        float(at.loc[2024, PLD] / at.loc[2023, PLD] - 1) * 100, 1)
    R["ld_pax_change_2021_2022_pct"] = round(
        float(at.loc[2022, PLD] / at.loc[2021, PLD] - 1) * 100, 1)
    g = float(at.loc[2024, PRG] / at.loc[2023, PRG])
    R["reg_pax_years_to_2019_at_2024_growth"] = round(
        float(np.log(at.loc[2019, PRG] / at.loc[2024, PRG]) / np.log(g)), 1)

    # --- Finding 4: investment rose, punctuality fell --------------------------
    cap = df.dropna(subset=[CAP])
    R["capex_2010"] = float(at.loc[2010, CAP])
    R["capex_2019"] = float(at.loc[2019, CAP])
    R["capex_2024"] = float(at.loc[2024, CAP])
    R["capex_change_2010_2024_pct"] = round(
        float(at.loc[2024, CAP] / at.loc[2010, CAP] - 1) * 100, 1)
    R["capex_sum_2015_2019_bn"] = round(
        float(df[(df.year >= 2015) & (df.year <= 2019)][CAP].sum()) / 1000, 1)
    R["capex_sum_2020_2024_bn"] = round(
        float(df[df.year >= 2020][CAP].sum()) / 1000, 1)
    R["capex_sum_available_years_bn"] = round(float(cap[CAP].sum()) / 1000, 1)
    R["capex_n_years_available"] = int(len(cap))

    # --- Finding 5: correlations ----------------------------------------------
    R["corr_ld_punct_capex"] = corr(df, LD, CAP)
    R["corr_ld_punct_ld_pax"] = corr(df, LD, PLD)
    R["corr_ld_punct_reg_punct"] = corr(df, LD, RG)
    R["corr_reg_punct_reg_pax"] = corr(df, RG, PRG)
    R["corr_ld_punct_infra_delays"] = corr(df, LD, INF)
    R["corr_reg_pax_reg_punct"] = R["corr_reg_punct_reg_pax"]
    pre19 = df[df.year <= 2019]
    R["corr_ld_punct_capex_pre2020"] = corr(pre19, LD, CAP)

    # --- Finding 6: infrastructure delays (2020-2024, descriptive) -------------
    R["infra_delays_2020"] = float(at.loc[2020, INF])
    R["infra_delays_2024"] = float(at.loc[2024, INF])
    R["infra_delays_change_2020_2024_pct"] = round(
        float(at.loc[2024, INF] / at.loc[2020, INF] - 1) * 100, 1)

    # --- Finding 7: revenues (descriptive only; scope breaks) ------------------
    R["revenues_2019"] = float(at.loc[2019, REV])
    R["revenues_2022"] = float(at.loc[2022, REV])
    R["revenues_change_2019_2022_pct"] = round(
        float(at.loc[2022, REV] / at.loc[2019, REV] - 1) * 100, 1)
    R["revenues_2024_continuing"] = float(at.loc[2024, REV])

    df.to_csv("outputs/db_yearly.csv", index=False)
    with open("outputs/results.json", "w") as f:
        json.dump(R, f, indent=2)
    print(json.dumps(R, indent=2))


if __name__ == "__main__":
    main()
