from pathlib import Path
import subprocess
import pandas as pd


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

INVENTORY = Path("metadata/manual_sra_inventory.tsv")
GLUE = Path("results/genotyping/hbv_glue_results.tsv")
PHYLO = Path("results/phylogeny/genotype_concordance.tsv")

ALIGNMENT_DIR = Path("results/alignment")
VARIANT_DIR = Path("results/variants")
CONSENSUS_DIR = Path("results/consensus")

OUTPUT = Path("results/statistics/hbv_master_analysis.tsv")


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def read_flagstat(sample):
    """
    Extract mapping statistics from samtools flagstat output.
    """

    path = ALIGNMENT_DIR / sample / f"{sample}.flagstat.txt"

    metrics = {
        "total_reads": None,
        "primary_reads": None,
        "mapped_reads": None,
        "mapping_percent": None,
        "properly_paired_reads": None,
        "properly_paired_percent": None
    }

    if not path.exists():
        return metrics

    with open(path) as handle:
        for line in handle:

            if "in total" in line:
                metrics["total_reads"] = int(line.split()[0])

            elif "primary" in line and "primary mapped" not in line and \
                    "primary duplicates" not in line:
                try:
                    metrics["primary_reads"] = int(line.split()[0])
                except ValueError:
                    pass

            elif "primary mapped (" in line:
                metrics["mapped_reads"] = int(line.split()[0])

                percent = line.split("(")[1].split("%")[0]
                metrics["mapping_percent"] = float(percent)

            elif "properly paired (" in line:
                metrics["properly_paired_reads"] = int(line.split()[0])

                percent = line.split("(")[1].split("%")[0]
                metrics["properly_paired_percent"] = float(percent)

    return metrics


def read_coverage(sample):
    """
    Extract samtools coverage statistics.
    """

    path = ALIGNMENT_DIR / sample / f"{sample}.coverage.tsv"

    metrics = {
        "coverage_percent": None,
        "mean_depth": None,
        "mean_baseq": None,
        "mean_mapq": None
    }

    if not path.exists():
        return metrics

    df = pd.read_csv(path, sep="\t")

    if df.empty:
        return metrics

    row = df.iloc[0]

    metrics["coverage_percent"] = float(row["coverage"])
    metrics["mean_depth"] = float(row["meandepth"])
    metrics["mean_baseq"] = float(row["meanbaseq"])
    metrics["mean_mapq"] = float(row["meanmapq"])

    return metrics


def consensus_length(sample):
    """
    Calculate consensus sequence length.
    """

    if sample == "LA005":
        candidates = [
            CONSENSUS_DIR / sample / "LA005_haploid_consensus.fasta",
            CONSENSUS_DIR / sample / "LA005_consensus.fasta"
        ]
    else:
        candidates = [
            CONSENSUS_DIR / sample / f"{sample}_consensus.fasta"
        ]

    fasta = next(
        (f for f in candidates if f.exists()),
        None
    )

    if fasta is None:
        return None

    sequence = []

    with open(fasta) as handle:
        for line in handle:
            if not line.startswith(">"):
                sequence.append(line.strip())

    return len("".join(sequence))


def variant_statistics(sample):
    """
    Obtain variant statistics from the final normalized,
    filtered haploid VCF using bcftools stats.
    """

    candidates = [
        VARIANT_DIR / sample /
        f"{sample}.haploid.filtered.norm.vcf.gz",

        VARIANT_DIR / sample /
        f"{sample}.haploid.filtered.vcf.gz"
    ]

    vcf = next(
        (f for f in candidates if f.exists()),
        None
    )

    metrics = {
        "variant_records": None,
        "snps": None,
        "indels": None,
        "multiallelic_sites": None,
        "ts": None,
        "tv": None,
        "ts_tv_ratio": None
    }

    if vcf is None:
        return metrics

    result = subprocess.run(
        ["bcftools", "stats", str(vcf)],
        capture_output=True,
        text=True,
        check=True
    )

    for line in result.stdout.splitlines():

        fields = line.split("\t")

        if line.startswith("SN"):

            label = fields[2].strip()
            value = fields[3].strip()

            if label == "number of records:":
                metrics["variant_records"] = int(value)

            elif label == "number of SNPs:":
                metrics["snps"] = int(value)

            elif label == "number of indels:":
                metrics["indels"] = int(value)

            elif label == "number of multiallelic sites:":
                metrics["multiallelic_sites"] = int(value)

        elif line.startswith("TSTV"):

            metrics["ts"] = int(fields[2])
            metrics["tv"] = int(fields[3])
            metrics["ts_tv_ratio"] = float(fields[4])

    return metrics


# ---------------------------------------------------------
# Read project-level metadata
# ---------------------------------------------------------

inventory = pd.read_csv(
    INVENTORY,
    sep="\t",
    keep_default_na=False
)

glue = pd.read_csv(
    GLUE,
    sep="\t",
    keep_default_na=False
)

phylo = pd.read_csv(
    PHYLO,
    sep="\t",
    keep_default_na=False
)


# ---------------------------------------------------------
# Build one row per biological sample
# ---------------------------------------------------------

rows = []

for _, sample_row in inventory.iterrows():

    if sample_row["inclusion"] != "Include":
        continue

    sample = sample_row["sample_id"]

    row = {
        "sample_id": sample,
        "run": sample_row["run"],
        "biosample": sample_row["biosample"],
        "raw_spots": sample_row["spots"],
        "raw_bases_M": sample_row["bases_M"],
        "raw_size_mb": sample_row["size_mb"],
        "raw_gc_percent": sample_row["gc_percent"]
    }

    row.update(read_flagstat(sample))
    row.update(read_coverage(sample))
    row.update(variant_statistics(sample))

    row["consensus_length"] = consensus_length(sample)

    rows.append(row)


master = pd.DataFrame(rows)


# ---------------------------------------------------------
# Add HBV-GLUE information
# ---------------------------------------------------------

glue_columns = [
    "sample_id",
    "genotype",
    "subgenotype",
    "closest_reference"
]

master = master.merge(
    glue[glue_columns],
    on="sample_id",
    how="left"
)


# ---------------------------------------------------------
# Add phylogenetic information
# ---------------------------------------------------------

phylo_columns = [
    "sample_id",
    "closest_phylo_reference",
    "phylo_genotype",
    "nearest_ref_distance",
    "genotype_concordance",
    "interpretation"
]

master = master.merge(
    phylo[phylo_columns],
    on="sample_id",
    how="left"
)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

master.to_csv(
    OUTPUT,
    sep="\t",
    index=False
)

print(master.to_string(index=False))
print(f"\nSamples: {len(master)}")
print(f"Saved: {OUTPUT}")

echo "end"
