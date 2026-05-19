"""Pandemic analysis plots — mirrors the earthquake/famines analytical pattern.

Conventions:
- WHO-monitored modern era starts ~1900 (germ theory + global health agencies)
- Pre-1900 entries kept in plots but excluded from trend fits
- Cumulative-vs-constant-rate for very rare events (≥1M-death pandemics)
- Power-law fit on the tail only (≥1M deaths)
- Partial decades shaded
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

HERE = Path(__file__).parent
PLOTS = HERE / "plots"
PLOTS.mkdir(exist_ok=True)

CATALOG_START = 1900     # post-germ-theory: pre-1900 is anecdotal
GREAT_PANDEMIC_THRESHOLD = 1_000_000
PARTIAL_DECADE_START = 2020

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
    "font.size": 10, "axes.titlesize": 12,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linestyle": "--",
})


def load_events() -> pd.DataFrame:
    df = pd.read_csv(HERE / "pandemics.csv")
    df["end_year"] = df["end_year"].fillna(df["start_year"]).astype(int)
    df["midpoint"] = (df["start_year"] + df["end_year"]) / 2
    df["duration"] = df["end_year"] - df["start_year"] + 1
    return df


def fmt_thousands(x, _):
    return f"{int(x):,}"


def plot_01_history(df: pd.DataFrame):
    """Pandemic deaths over time, bubble = deaths_estimate (log-sized)."""
    fig, ax = plt.subplots(figsize=(11, 5.5))
    sizes = np.clip(np.sqrt(df["deaths_estimate"]) / 30, 30, 1200)
    colors = np.where(df["deaths_estimate"] >= GREAT_PANDEMIC_THRESHOLD, "#cc3322", "#888888")
    ax.scatter(df["midpoint"], df["deaths_estimate"], s=sizes, c=colors,
                alpha=0.6, edgecolor="black", linewidth=0.5)
    ax.set_yscale("log")
    ax.set_ylabel("Deaths (log scale)")
    ax.set_xlabel("Year")
    ax.set_title("Pandemic deaths over time — bubble size ∝ deaths, red = ≥1M deaths")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_thousands))
    # Annotate the biggest
    big = df.nlargest(6, "deaths_estimate")
    for _, row in big.iterrows():
        ax.annotate(row["name"].split("(")[0][:20], (row["midpoint"], row["deaths_estimate"]),
                    xytext=(5, 5), textcoords="offset points", fontsize=8, alpha=0.85)
    ax.set_xlim(-500, 2030)
    plt.tight_layout()
    plt.savefig(PLOTS / "01_pandemics_history.png")
    plt.close()


def plot_02_decadal_counts_by_band(df: pd.DataFrame):
    """Stacked bars: pandemics per decade by death band."""
    bands = [(100_000, 1_000_000, "100k–1M", "#bbdd99"),
             (1_000_000, 10_000_000, "1M–10M", "#dd9966"),
             (10_000_000, np.inf, "≥10M", "#cc3322")]
    modern = df[df["start_year"] >= CATALOG_START].copy()
    modern["decade"] = (modern["start_year"] // 10) * 10

    fig, ax = plt.subplots(figsize=(10, 5))
    decades = np.arange(CATALOG_START, 2030, 10)
    bottom = np.zeros(len(decades))
    for lo, hi, label, color in bands:
        counts = []
        for d in decades:
            in_decade = modern[(modern["decade"] == d) &
                                (modern["deaths_estimate"] >= lo) &
                                (modern["deaths_estimate"] < hi)]
            counts.append(len(in_decade))
        ax.bar(decades, counts, width=8, bottom=bottom, label=label,
                color=color, edgecolor="black", linewidth=0.4)
        bottom += counts
    # Shade partial 2020s
    ax.axvspan(PARTIAL_DECADE_START, PARTIAL_DECADE_START + 10,
                color="grey", alpha=0.18, label="partial decade")
    ax.set_xlabel("Decade")
    ax.set_ylabel("Pandemics per decade")
    ax.set_title(f"Pandemic onsets per decade by death band (catalog starts {CATALOG_START})")
    ax.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(PLOTS / "02_decadal_counts_by_band.png")
    plt.close()


def plot_03_great_pandemic_timing(df: pd.DataFrame):
    """Cumulative ≥1M-death pandemic count vs constant-rate reference."""
    great = df[df["deaths_estimate"] >= GREAT_PANDEMIC_THRESHOLD].copy()
    great = great.sort_values("start_year")
    modern_great = great[great["start_year"] >= CATALOG_START].copy()
    modern_great["n"] = np.arange(1, len(modern_great) + 1)

    if len(modern_great) < 2:
        return
    span_yr = modern_great["start_year"].iloc[-1] - CATALOG_START
    rate = len(modern_great) / span_yr  # per year
    yrs = np.arange(CATALOG_START, 2026)
    expected = rate * (yrs - CATALOG_START)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ax = axes[0]
    ax.step(modern_great["start_year"], modern_great["n"], where="post",
            color="#cc3322", linewidth=2, label="Observed cumulative ≥1M")
    ax.plot(yrs, expected, color="gray", linestyle="--",
            label=f"Constant rate ({rate:.3f}/yr)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative count of ≥1M-death pandemics")
    ax.set_title(f"Cumulative vs constant-rate ({CATALOG_START}+)")
    ax.legend()
    for _, row in modern_great.iterrows():
        ax.annotate(row["name"].split("(")[0][:15],
                    (row["start_year"], row.get("n", 0)),
                    xytext=(3, -10), textcoords="offset points",
                    fontsize=7, alpha=0.7)

    # Inter-event intervals
    ax = axes[1]
    intervals = np.diff(modern_great["start_year"].values)
    if len(intervals) > 0:
        ax.bar(range(len(intervals)), intervals,
                color="#cc3322", alpha=0.7, edgecolor="black", linewidth=0.4)
        ax.axhline(intervals.mean(), color="gray", linestyle="--",
                    label=f"mean = {intervals.mean():.1f} yr")
        labels = [f"{a}→{b}" for a, b in zip(modern_great["start_year"].values[:-1],
                                              modern_great["start_year"].values[1:])]
        ax.set_xticks(range(len(intervals)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Years between great pandemics")
        ax.set_title("Inter-event intervals")
        ax.legend()
    plt.tight_layout()
    plt.savefig(PLOTS / "03_great_pandemic_timing.png")
    plt.close()


def plot_04_magnitude_distribution(df: pd.DataFrame):
    """Log-log survival function with power-law fit on the tail."""
    deaths = df["deaths_estimate"].dropna().values
    deaths = np.sort(deaths)[::-1]
    n = len(deaths)
    survival = np.arange(1, n + 1)

    # Power-law fit on the upper tail (≥200k, matching famines-tracking choice)
    tail_mask = deaths >= 200_000
    if tail_mask.sum() >= 5:
        x_tail = np.log10(deaths[tail_mask])
        y_tail = np.log10(survival[tail_mask])
        slope, intercept = np.polyfit(x_tail, y_tail, 1)
        alpha = -slope
    else:
        alpha = None

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.loglog(deaths, survival, "o", color="#cc3322", alpha=0.7,
                markeredgecolor="black", markersize=6, label="Pandemics")
    if alpha is not None:
        xs = np.logspace(np.log10(200_000), np.log10(deaths.max()), 50)
        ys = 10 ** (intercept) * xs ** slope
        ax.loglog(xs, ys, "--", color="gray",
                    label=f"Power-law fit (α={alpha:.2f}, tail ≥200k)")
    ax.set_xlabel("Deaths (log)")
    ax.set_ylabel("Survival count P(X≥x)")
    ax.set_title("Pandemic death-toll distribution (Gutenberg-Richter analog)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(PLOTS / "04_magnitude_distribution.png")
    plt.close()


def main():
    df = load_events()
    print(f"Loaded {len(df)} pandemics; {df['start_year'].min()}–{df['end_year'].max()}")
    print(f"≥1M deaths: {(df['deaths_estimate'] >= GREAT_PANDEMIC_THRESHOLD).sum()}")
    print(f"≥10M deaths: {(df['deaths_estimate'] >= 10_000_000).sum()}")
    plot_01_history(df)
    plot_02_decadal_counts_by_band(df)
    plot_03_great_pandemic_timing(df)
    plot_04_magnitude_distribution(df)
    print(f"Wrote 4 plots to {PLOTS}/")


if __name__ == "__main__":
    main()
