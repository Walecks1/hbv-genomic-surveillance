from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# =========================================================
# Paths
# =========================================================

INPUT = Path("results/statistics/hbv_master_analysis.tsv")
OUTDIR = Path("results/statistics/figures")

OUTDIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# Read data
# =========================================================

df = pd.read_csv(
    INPUT,
    sep="\t",
    keep_default_na=False
)

numeric_cols = [
    "mapping_percent",
    "coverage_percent",
    "mean_depth",
    "variant_records",
    "snps",
    "indels"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# Genotype order used consistently across figures
genotype_order = ["A", "D", "E"]

df["genotype"] = pd.Categorical(
    df["genotype"],
    categories=genotype_order,
    ordered=True
)


# =========================================================
# Figure 1 — Genotype distribution
# =========================================================

genotype_counts = (
    df["genotype"]
    .value_counts(sort=False)
    .reindex(genotype_order)
    .fillna(0)
)

fig, ax = plt.subplots(figsize=(6, 5))

bars = ax.bar(
    genotype_counts.index,
    genotype_counts.values
)

ax.set_xlabel("HBV genotype")
ax.set_ylabel("Number of samples")
ax.set_title("HBV genotype distribution")

ax.set_ylim(
    0,
    max(genotype_counts.values) + 2
)

for bar, count in zip(
    bars,
    genotype_counts.values
):
    percent = count / len(df) * 100

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.15,
        f"{int(count)} ({percent:.1f}%)",
        ha="center",
        va="bottom"
    )

fig.tight_layout()

fig.savefig(
    OUTDIR / "genotype_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# =========================================================
# Figure 2 — Mapping percentage by sample
# =========================================================

plot_df = df.sort_values(
    ["genotype", "sample_id"]
).copy()

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.bar(
    plot_df["sample_id"],
    plot_df["mapping_percent"]
)

ax.set_xlabel("Sample")
ax.set_ylabel("Mapped reads (%)")
ax.set_title(
    "HBV read mapping to NC_003977.2"
)

ax.set_ylim(0, 105)

ax.tick_params(
    axis="x",
    rotation=45
)

# Put genotype above each bar
for bar, genotype in zip(
    bars,
    plot_df["genotype"]
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(genotype),
        ha="center",
        va="bottom",
        fontsize=8
    )

fig.tight_layout()

fig.savefig(
    OUTDIR / "mapping_percentage_by_sample.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# =========================================================
# Figure 3 — Mean sequencing depth
# =========================================================

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.bar(
    plot_df["sample_id"],
    plot_df["mean_depth"]
)

ax.set_xlabel("Sample")
ax.set_ylabel("Mean depth (×)")
ax.set_title(
    "Mean HBV genome sequencing depth"
)

ax.tick_params(
    axis="x",
    rotation=45
)

fig.tight_layout()

fig.savefig(
    OUTDIR / "mean_depth_by_sample.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# =========================================================
# Figure 4 — Variants relative to mapping reference
# =========================================================

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.bar(
    plot_df["sample_id"],
    plot_df["variant_records"]
)

ax.set_xlabel("Sample")
ax.set_ylabel("Number of retained variants")
ax.set_title(
    "Variants relative to HBV reference NC_003977.2"
)

ax.tick_params(
    axis="x",
    rotation=45
)

# Genotype labels above bars
for bar, genotype in zip(
    bars,
    plot_df["genotype"]
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 3,
        str(genotype),
        ha="center",
        va="bottom",
        fontsize=8
    )

fig.tight_layout()

fig.savefig(
    OUTDIR / "variants_by_sample.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# =========================================================
# Figure 5 — Mapping percentage by genotype
# =========================================================

groups = []

labels = []

for genotype in genotype_order:

    values = df.loc[
        df["genotype"] == genotype,
        "mapping_percent"
    ].dropna()

    if len(values) > 0:
        groups.append(values)
        labels.append(genotype)


fig, ax = plt.subplots(figsize=(6, 5))

ax.boxplot(
    groups,
    tick_labels=labels
)

ax.set_xlabel("HBV genotype")
ax.set_ylabel("Mapped reads (%)")
ax.set_title(
    "Mapping percentage by HBV genotype"
)

fig.tight_layout()

fig.savefig(
    OUTDIR / "mapping_percentage_by_genotype.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# =========================================================
# Finish
# =========================================================

print("\n=== Phase 9 figures generated ===\n")

for file in sorted(OUTDIR.glob("*.png")):
    print(file)
