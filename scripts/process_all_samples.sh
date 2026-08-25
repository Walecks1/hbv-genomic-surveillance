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

    R1="data/raw/${sample_id}/${sample_id}_R1.fastq"
    R2="data/raw/${sample_id}/${sample_id}_R2.fastq"

    if [[ ! -s "${R1}" || ! -s "${R2}" ]]; then
        echo "ERROR: Missing FASTQ files for ${sample_id}"
        continue
    fi

    echo "=== Processing ${sample_id} ==="

    scripts/process_hbv_sample.sh \
        "${sample_id}" \
        "${R1}" \
        "${R2}"

done
