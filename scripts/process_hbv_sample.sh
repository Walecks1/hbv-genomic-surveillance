#!/usr/bin/env bash

set -euo pipefail

SAMPLE=$1
R1=$2
R2=$3

REF="data/reference/HBV_NC_003977.2.fasta"

echo "=== Processing ${SAMPLE} ==="

mkdir -p results/trimmed/${SAMPLE}
mkdir -p results/qc/trimmed/${SAMPLE}
mkdir -p results/alignment/${SAMPLE}
mkdir -p results/variants/${SAMPLE}
mkdir -p results/consensus/${SAMPLE}

# 1. Read filtering
fastp \
  -i "${R1}" \
  -I "${R2}" \
  -o results/trimmed/${SAMPLE}/${SAMPLE}_R1.trimmed.fastq.gz \
  -O results/trimmed/${SAMPLE}/${SAMPLE}_R2.trimmed.fastq.gz \
  -h results/qc/trimmed/${SAMPLE}/${SAMPLE}_fastp.html \
  -j results/qc/trimmed/${SAMPLE}/${SAMPLE}_fastp.json \
  --thread 4

# 2. Alignment
bwa-mem2 mem \
  -t 4 \
  "${REF}" \
  results/trimmed/${SAMPLE}/${SAMPLE}_R1.trimmed.fastq.gz \
  results/trimmed/${SAMPLE}/${SAMPLE}_R2.trimmed.fastq.gz \
| samtools sort \
  -o results/alignment/${SAMPLE}/${SAMPLE}.sorted.bam

samtools index \
  results/alignment/${SAMPLE}/${SAMPLE}.sorted.bam

# 3. Alignment QC
samtools flagstat \
  results/alignment/${SAMPLE}/${SAMPLE}.sorted.bam \
  > results/alignment/${SAMPLE}/${SAMPLE}.flagstat.txt

samtools coverage \
  results/alignment/${SAMPLE}/${SAMPLE}.sorted.bam \
  > results/alignment/${SAMPLE}/${SAMPLE}.coverage.tsv

# 4. Haploid variant calling
bcftools mpileup \
  -f "${REF}" \
  -q 20 \
  -Q 20 \
  -Ou \
  results/alignment/${SAMPLE}/${SAMPLE}.sorted.bam \
| bcftools call \
  -mv \
  --ploidy 1 \
  -Oz \
  -o results/variants/${SAMPLE}/${SAMPLE}.haploid.vcf.gz

bcftools index -t \
  results/variants/${SAMPLE}/${SAMPLE}.haploid.vcf.gz

# 5. Filter variants
bcftools filter \
  -i 'DP>=10 && QUAL>=30' \
  results/variants/${SAMPLE}/${SAMPLE}.haploid.vcf.gz \
  -Oz \
  -o results/variants/${SAMPLE}/${SAMPLE}.haploid.filtered.vcf.gz

bcftools index -t \
  results/variants/${SAMPLE}/${SAMPLE}.haploid.filtered.vcf.gz

# 6. Normalize
bcftools norm \
  -f "${REF}" \
  results/variants/${SAMPLE}/${SAMPLE}.haploid.filtered.vcf.gz \
  -Oz \
  -o results/variants/${SAMPLE}/${SAMPLE}.haploid.filtered.norm.vcf.gz

bcftools index -t \
  results/variants/${SAMPLE}/${SAMPLE}.haploid.filtered.norm.vcf.gz

# 7. Consensus
bcftools consensus \
  -f "${REF}" \
  results/variants/${SAMPLE}/${SAMPLE}.haploid.filtered.norm.vcf.gz \
  > results/consensus/${SAMPLE}/${SAMPLE}_consensus.fasta

echo "=== ${SAMPLE} complete ==="
