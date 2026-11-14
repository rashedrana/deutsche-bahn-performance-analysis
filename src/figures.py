"""Publication-quality figures for the Deutsche Bahn analysis.

All figures are drawn from data/db_performance.csv (and, for Figure 7,
the two-break model of src/analysis.py refitted from the same CSV).
Saved as PNG (200 dpi) in outputs/figures/.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm

plt.rcParams.update({"font.size": 10, "axes.grid": True,
                     "grid.alpha": 0.3, "figure.dpi": 200})
LD = "punctuality_long_distance_pct"
RG = "punctuality_regional_pct"
PLD = "passengers_long_distance_mn"
PRG = "passengers_regional_mn"
CAP = "gross_capex_eur_mn"
INF = "infra_delay_lost_units_per_day"


def shade(ax):
    ax.axvspan(2019.5, 2021.5, color="grey", alpha=0.15)
    ax.axvspan(2021.5, 2024.5, color="orange", alpha=0.10)
    ax.text(2020.5, ax.get_ylim()[1], " COVID-19", fontsize=8, va="top")
    ax.text(2023.0, ax.get_ylim()[1], " flat-fare era\n (9-Euro-Ticket,\n"
            " Deutschlandticket)", fontsize=8, va="top")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"outputs/figures/{name}", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def main():
    df = pd.read_csv("data/db_performance.csv")
    y = df.year

    # Fig 1: long-distance punctuality + pre-COVID trend extended
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(y, df[LD], "o-", color="#c00", lw=2, label="Long-distance punctuality")
    pre = df[df.year <= 2019]
    X = sm.add_constant((pre.year - 2010).astype(float).values)
    m = sm.OLS(pre[LD].values, X).fit()
    xs = np.arange(2010, 2025)
    ax.plot(xs, m.params[0] + m.params[1] * (xs - 2010), "--", color="grey",
            label="2010–2019 trend, extended")
    ax.axhline(80, color="green", ls=":", lw=1.2,
               label="DB long-term target (80%)")
    ax.set_ylabel("Trains arriving < 6 min late (%)")
    ax.set_title("Figure 1. Long-distance punctuality: flat for a decade, "
                 "then a regime break")
    ax.set_xlim(2009.5, 2024.5)
    ax.legend(fontsize=8, loc="lower left")
    shade(ax)
    save(fig, "fig1_ld_punctuality.png")

    # Fig 2: regional punctuality
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    d = df.dropna(subset=[RG])
    ax.plot(d.year, d[RG], "o-", color="#06c", lw=2,
            label="Regional punctuality (DB Regio)")
    ax.axhline(95, color="green", ls=":", lw=1.2,
               label="DB Regional target (95%)")
    ax.set_ylabel("Trains arriving < 6 min late (%)")
    ax.set_title("Figure 2. Regional punctuality: slow erosion, then the "
                 "same post-2021 break")
    ax.set_xlim(2010.5, 2024.5)
    ax.set_ylim(89, 97)
    ax.legend(fontsize=8, loc="lower left")
    shade(ax)
    save(fig, "fig2_regional_punctuality.png")

    # Fig 3: stacked passengers
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(y, df[PRG], color="#06c", label="Regional (DB Regio)")
    ax.bar(y, df[PLD], bottom=df[PRG], color="#c00",
           label="Long-distance (DB Fernverkehr)")
    ax.set_ylabel("Passengers (million per year)")
    ax.set_title("Figure 3. Rail passengers in Germany (DB): the COVID "
                 "collapse and the incomplete recovery")
    ax.legend(fontsize=8)
    save(fig, "fig3_passengers_stacked.png")

    # Fig 4: indexed passengers, 2019 = 100
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    base_ld = df.loc[df.year == 2019, PLD].iloc[0]
    base_rg = df.loc[df.year == 2019, PRG].iloc[0]
    ax.plot(y, 100 * df[PLD] / base_ld, "o-", color="#c00", lw=2,
            label="Long-distance")
    ax.plot(y, 100 * df[PRG] / base_rg, "s-", color="#06c", lw=2,
            label="Regional")
    ax.axhline(100, color="grey", ls="--", lw=1)
    ax.set_ylabel("Passengers (index, 2019 = 100)")
    ax.set_title("Figure 4. Passenger recovery: both segments still below "
                 "2019 in 2024")
    ax.set_xlim(2009.5, 2024.5)
    ax.legend(fontsize=8, loc="lower left")
    shade(ax)
    save(fig, "fig4_passengers_indexed.png")

    # Fig 5: capex bars + punctuality line
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    d = df.dropna(subset=[CAP])
    ax.bar(d.year, d[CAP] / 1000, color="#999", alpha=0.75,
           label="Gross capital expenditures (left axis)")
    ax.set_ylabel("Gross capital expenditures (€ billion)")
    ax2 = ax.twinx()
    ax2.plot(y, df[LD], "o-", color="#c00", lw=2,
             label="Long-distance punctuality (right axis)")
    ax2.set_ylabel("Long-distance punctuality (%)", color="#c00")
    ax2.grid(False)
    ax.set_title("Figure 5. Investment rose 165% while punctuality fell "
                 "to a record low")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper left")
    save(fig, "fig5_capex_punctuality.png")

    # Fig 6: scatter punctuality vs LD passengers, coloured by era
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    eras = [("2010–2019", df.year <= 2019, "#06c"),
            ("2020–2021 COVID", (df.year >= 2020) & (df.year <= 2021), "grey"),
            ("2022–2024", df.year >= 2022, "#c00")]
    for name, mask, c in eras:
        ax.scatter(df.loc[mask, PLD], df.loc[mask, LD], c=c, s=70,
                   label=name, edgecolor="k", zorder=3)
    for _, r in df.iterrows():
        ax.annotate(int(r.year), (r[PLD], r[LD]), fontsize=7,
                    xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("Long-distance passengers (million)")
    ax.set_ylabel("Long-distance punctuality (%)")
    ax.set_title("Figure 6. Punctuality vs long-distance demand: the "
                 "pandemic paradox (2020) and the post-2021 regime")
    ax.legend(fontsize=8)
    save(fig, "fig6_scatter_punct_demand.png")

    # Fig 7: two-break model, actual vs fitted (LD punctuality)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    t = (df.year - 2010).astype(float)
    X = np.column_stack([np.ones(len(df)), t,
                         ((df.year >= 2020) & (df.year <= 2021)).astype(float),
                         (df.year >= 2022).astype(float)])
    m = sm.OLS(df[LD].values, X).fit()
    ax.plot(y, df[LD], "o", color="#c00", ms=7, label="Actual")
    ax.plot(y, m.fittedvalues, "-", color="#06c", lw=2,
            label=f"Two-break model (R² = {m.rsquared:.2f})")
    ax.set_ylabel("Long-distance punctuality (%)")
    ax.set_title("Figure 7. Two structural breaks explain long-distance "
                 "punctuality far better than a trend")
    ax.set_xlim(2009.5, 2024.5)
    ax.legend(fontsize=8, loc="lower left")
    shade(ax)
    save(fig, "fig7_break_model.png")

    # Fig 8: infrastructure delays + LD punctuality, 2020-2024
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    d = df.dropna(subset=[INF])
    ax.bar(d.year, d[INF], color="#c60", alpha=0.8, width=0.55,
           label="Infrastructure-related delays (left axis)")
    ax.set_ylabel("Lost units per day")
    ax2 = ax.twinx()
    ax2.plot(d.year, d[LD], "o-", color="#c00", lw=2,
             label="Long-distance punctuality (right axis)")
    ax2.set_ylabel("Long-distance punctuality (%)", color="#c00")
    ax2.grid(False)
    ax.set_title("Figure 8. Infrastructure-related delays rose 81% in "
                 "four years (2020–2024)")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=8, loc="center left")
    save(fig, "fig8_infra_delays.png")


if __name__ == "__main__":
    main()
