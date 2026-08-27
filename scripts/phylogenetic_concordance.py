from Bio import Phylo
import pandas as pd

TREE = "results/phylogeny/HBV_ML.treefile"
GLUE = "results/genotyping/hbv_glue_results.tsv"
OUT = "results/phylogeny/genotype_concordance.tsv"

study_samples = [
    "3269", "3274", "3319", "3358", "3658",
    "3768", "3791", "4070", "4312", "LA005",
    "N005", "N011", "N060", "N199", "PO04"
]

tree = Phylo.read(TREE, "newick")
glue = pd.read_csv(GLUE, sep="\t")

reference_names = [
    tip.name
    for tip in tree.get_terminals()
    if tip.name.startswith("REF_")
]


def parse_reference(ref):
    parts = ref.split("_")

    genotype = parts[1]

    # Everything between genotype and accession is subgenotype
    accession = parts[-1]
    subgenotype = "_".join(parts[2:-1])

    return genotype, subgenotype, accession


rows = []

for sample in study_samples:

    distances = []

    for ref in reference_names:
        distance = tree.distance(sample, ref)
        distances.append((distance, ref))

    distances.sort()

    nearest_distance, nearest_ref = distances[0]

    phylo_genotype, phylo_subgenotype, accession = \
        parse_reference(nearest_ref)

    # Examine the node connecting sample and nearest reference
    ancestor = tree.common_ancestor(
        {"name": sample},
        {"name": nearest_ref}
    )

    node_support = ancestor.name if ancestor.name else "NA"
    clade_size = len(ancestor.get_terminals())

    glue_row = glue.loc[
        glue["sample_id"] == sample
    ].iloc[0]

    glue_genotype = str(glue_row["genotype"])
    glue_subgenotype = str(glue_row["subgenotype"])

    genotype_concordance = (
        "Concordant"
        if glue_genotype == phylo_genotype
        else "Discordant"
    )

    rows.append({
        "sample_id": sample,
        "hbv_glue_genotype": glue_genotype,
        "hbv_glue_subgenotype": glue_subgenotype,
        "closest_phylo_reference": nearest_ref,
        "phylo_genotype": phylo_genotype,
        "nearest_ref_distance": round(nearest_distance, 6),
        "nearest_node_support": node_support,
        "nearest_node_taxa": clade_size,
        "genotype_concordance": genotype_concordance
    })


df = pd.DataFrame(rows)

df.to_csv(
    OUT,
    sep="\t",
    index=False
)

print(df.to_string(index=False))
print(f"\nSaved: {OUT}")
