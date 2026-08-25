#!/usr/bin/env bash

set -euo pipefail

INVENTORY="metadata/manual_sra_inventory.tsv"

tail -n +2 "${INVENTORY}" | while IFS=$'\t' read -r \
sample_id biosample sra_sample experiment run platform layout \
read1 read2 spots bases size gc status inclusion

do
    if [[ "${inclusion}" != "Include" ]]; then
        continue
    fi

    echo "=== Downloading ${sample_id} (${run}) ==="

    mkdir -p "data/raw/${sample_id}"

    fasterq-dump "${run}" \
        --split-files \
        --threads 4 \
        --outdir "data/raw/${sample_id}"

    mv "data/raw/${sample_id}/${run}_1.fastq" \
       "data/raw/${sample_id}/${sample_id}_R1.fastq"

    mv "data/raw/${sample_id}/${run}_2.fastq" \
       "data/raw/${sample_id}/${sample_id}_R2.fastq"

    echo "=== ${sample_id} complete ==="
done
