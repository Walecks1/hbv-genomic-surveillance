#!/usr/bin/env bash

set -euo pipefail

OUT="results/sample_summary.tsv"

printf "sample\tmapped_reads\tmapping_percent\tcoverage_percent\tmean_depth\tfiltered_variants\tconsensus_length\n" > "${OUT}"

for dir in results/alignment/*; do

    [[ -d "${dir}" ]] || continue

    SAMPLE=$(basename "${dir}")

    FLAGSTAT="results/alignment/${SAMPLE}/${SAMPLE}.flagstat.txt"
    COVERAGE="results/alignment/${SAMPLE}/${SAMPLE}.coverage.tsv"
    VCF="results/variants/${SAMPLE}/${SAMPLE}.haploid.filtered.norm.vcf.gz"
    FASTA="results/consensus/${SAMPLE}/${SAMPLE}_consensus.fasta"

    mapped_reads="NA"
    mapping_percent="NA"
    coverage_percent="NA"
    mean_depth="NA"
    filtered_variants="NA"
    consensus_length="NA"

    if [[ -f "${FLAGSTAT}" ]]; then
        mapped_line=$(grep " primary mapped (" "${FLAGSTAT}" | head -1 || true)

        if [[ -n "${mapped_line}" ]]; then
            mapped_reads=$(echo "${mapped_line}" | awk '{print $1}')
            mapping_percent=$(echo "${mapped_line}" | sed -n 's/.*(\([0-9.]*\)%.*/\1/p')
        fi
    fi

    if [[ -f "${COVERAGE}" ]]; then
        coverage_percent=$(awk 'NR==2 {print $6}' "${COVERAGE}")
        mean_depth=$(awk 'NR==2 {print $7}' "${COVERAGE}")
    fi

    if [[ -f "${VCF}" ]]; then
        filtered_variants=$(bcftools view -H "${VCF}" | wc -l)
    fi

    if [[ -f "${FASTA}" ]]; then
        consensus_length=$(
            grep -v "^>" "${FASTA}" |
            tr -d '\n' |
            wc -c
        )
    fi

    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
        "${SAMPLE}" \
        "${mapped_reads}" \
        "${mapping_percent}" \
        "${coverage_percent}" \
        "${mean_depth}" \
        "${filtered_variants}" \
        "${consensus_length}" \
        >> "${OUT}"

done

echo "Summary written to ${OUT}"
