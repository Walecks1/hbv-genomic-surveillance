#!/usr/bin/env bash

set -euo pipefail

METADATA="data/phylogeny/hbv_reference_metadata.tsv"
REFDIR="data/phylogeny/references"
OUTPUT="data/phylogeny/hbv_references.fasta"

> "${OUTPUT}"

tail -n +2 "${METADATA}" |
while IFS=$'\t' read -r accession genotype subgenotype role country rationale
do

    fasta="${REFDIR}/${accession}.fasta"

    if [[ ! -s "${fasta}" ]]; then
        echo "ERROR: Missing ${fasta}" >&2
        exit 1
    fi

    header="REF_${genotype}_${subgenotype}_${accession}"

    sed "1s/.*/>${header}/" "${fasta}" \
      >> "${OUTPUT}"

done

echo "Reference FASTA written to ${OUTPUT}"
