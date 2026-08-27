import pandas as pd
from pathlib import Path

INPUT = Path("results/statistics/hbv_master_analysis.tsv")
OUTDIR = Path("results/statistics")

OUTDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT, sep="\t", keep_default_na=False)

# Convert relevant fields to numeric
numeric_cols = [
    "mapping_percent",
    "properly_paired_percent",
    "coverage_percent",
    "mean_depth",
    "mean_baseq",
    "mean_mapq",
    "variant_records",
    "snps",
    "indels",
    "ts_tv_ratio",
    "consensus_length",
    "nearest_ref_distance"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


# =========================================================
# 9.2 Dataset / QC summary
# =========================================================

summary_metrics = [
    "mapping_percent",
    "properly_paired_percent",
    "coverage_percent",
    "mean_depth",
    "mean_baseq",
    "mean_mapq",
    "variant_records",
    "snps",
    "indels",
    "consensus_length"
]

summary_rows = []

for metric in summary_metrics:

    if metric not in df.columns:
        continue

    values = df[metric].dropna()

    summary_rows.append({
        "metric": metric,
        "n": len(values),
        "mean": values.mean(),
        "sd": values.std(),
        "median": values.median(),
        "q1": values.quantile(0.25),
        "q3": values.quantile(0.75),
        "min": values.min(),
        "max": values.max()
    })

qc_summary = pd.DataFrame(summary_rows)

qc_summary.to_csv(
    OUTDIR / "dataset_qc_summary.tsv",
    sep="\t",
    index=False,
    float_format="%.3f"
)


# =========================================================
# 9.3 Genotype distribution
# =========================================================

genotype_counts = (
    df["genotype"]
    .value_counts()
    .rename_axis("genotype")
    .reset_index(name="n")
)

genotype_counts["percent"] = (
    genotype_counts["n"] /
    genotype_counts["n"].sum() * 100
)

genotype_counts.to_csv(
    OUTDIR / "genotype_distribution.tsv",
    sep="\t",
    index=False,
    float_format="%.1f"
)


# =========================================================
# 9.4 Mapping / coverage statistics
# =========================================================

mapping_columns = [
    "sample_id",
    "genotype",
    "mapping_percent",
    "properly_paired_percent",
    "coverage_percent",
    "mean_depth",
    "mean_baseq",
    "mean_mapq"
]

mapping_table = df[
    [c for c in mapping_columns if c in df.columns]
].copy()

mapping_table.to_csv(
    OUTDIR / "mapping_coverage_by_sample.tsv",
    sep="\t",
    index=False
)


# =========================================================
# 9.5 Variant burden
# =========================================================

variant_columns = [
    "sample_id",
    "genotype",
    "variant_records",
    "snps",
    "indels",
    "ts",
    "tv",
    "ts_tv_ratio"
]

variant_table = df[
    [c for c in variant_columns if c in df.columns]
].copy()

variant_table.to_csv(
    OUTDIR / "variant_summary_by_sample.tsv",
    sep="\t",
    index=False
)


# =========================================================
# 9.6 Genotype-stratified descriptive analysis
# =========================================================

genotype_metrics = [
    "mapping_percent",
    "coverage_percent",
    "mean_depth",
    "variant_records",
    "snps",
    "indels",
    "consensus_length",
    "nearest_ref_distance"
]

genotype_summary_rows = []

for genotype, group in df.groupby("genotype"):

    for metric in genotype_metrics:

        if metric not in group.columns:
            continue

        values = group[metric].dropna()

        if len(values) == 0:
            continue

        genotype_summary_rows.append({
            "genotype": genotype,
            "metric": metric,
            "n": len(values),
            "mean": values.mean(),
            "sd": values.std(),
            "median": values.median(),
            "q1": values.quantile(0.25),
            "q3": values.quantile(0.75),
            "min": values.min(),
            "max": values.max()
        })

genotype_summary = pd.DataFrame(genotype_summary_rows)

genotype_summary.to_csv(
    OUTDIR / "genotype_stratified_summary.tsv",
    sep="\t",
    index=False,
    float_format="%.3f"
)


# =========================================================
# 9.7 HBV-GLUE / phylogenetic concordance
# =========================================================

total = len(df)

concordant = (
    df["genotype_concordance"] == "Concordant"
).sum()

discordant = total - concordant

concordance_summary = pd.DataFrame([{
    "total_samples": total,
    "concordant": concordant,
    "discordant": discordant,
    "concordance_percent": concordant / total * 100
}])

concordance_summary.to_csv(
    OUTDIR / "genotype_concordance_summary.tsv",
    sep="\t",
    index=False,
    float_format="%.1f"
)


# =========================================================
# Console summary
# =========================================================

print("\n=== PHASE 9 SUMMARY ===\n")

print("Samples analysed:", len(df))

print("\nGenotype distribution:")
print(genotype_counts.to_string(index=False))

print("\nDataset QC:")
print(qc_summary.to_string(index=False))

print("\nGenotype-level phylogenetic concordance:")
print(concordance_summary.to_string(index=False))

print("\nGenerated:")
print(" - dataset_qc_summary.tsv")
print(" - genotype_distribution.tsv")
print(" - mapping_coverage_by_sample.tsv")
print(" - variant_summary_by_sample.tsv")
print(" - genotype_stratified_summary.tsv")
print(" - genotype_concordance_summary.tsv")
