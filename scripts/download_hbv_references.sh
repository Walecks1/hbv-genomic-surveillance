#!/usr/bin/env bash

set -euo pipefail

METADATA="data/phylogeny/hbv_reference_metadata.tsv"
OUTDIR="data/phylogeny/references"

mkdir -p "${OUTDIR}"

tail -n +2 "${METADATA}" |
while IFS=$'\t' read -r accession genotype subgenotype role country rationale
do
    outfile="${OUTDIR}/${accession}.fasta"

    if [[ -s "${outfile}" ]]; then
        echo "${accession}: already downloaded — skipping."
        continue
    fi

    echo "Downloading ${accession} (${genotype}/${subgenotype})"

    curl -fsSL \
      "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=${accession}&rettype=fasta&retmode=text" \
      -o "${outfile}"

    sleep 0.4

done

echo "Reference retrieval complete."
