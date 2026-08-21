# HBV Dataset Selection

## Dataset

BioProject: PRJNA737147

## Scientific purpose

This project uses publicly available hepatitis B virus (HBV)
whole-genome sequencing data to develop a reproducible
short-read viral genomics workflow.

## Dataset inclusion criteria

A sequencing run was considered eligible for the primary workflow if it:

1. belonged to PRJNA737147;
2. represented HBV whole-genome sequencing;
3. used an Illumina platform;
4. used paired-end sequencing;
5. had publicly accessible sequencing data.

## Exclusion criteria

Runs were excluded from the primary workflow if they:

- were not HBV whole-genome sequencing;
- lacked accessible raw sequencing data;
- used an incompatible sequencing platform;
- used a single-end or otherwise incompatible sequencing layout.

Samples failing these criteria were retained in the metadata inventory
where possible and their exclusion documented.

## Dataset assessment

The selected BioProject contained 15 sequencing runs.

All 15 runs satisfied the predefined technical inclusion criteria:

- Illumina: 15/15
- WGS: 15/15
- PCR selection: 15/15
- paired-end: 15/15
- public data: 15/15

Therefore, all 15 runs were retained for the primary workflow.

## Metadata limitations

Clinical and epidemiological variables were not used as inclusion
criteria unless required by the scientific question. Missing metadata
will be documented rather than used as a reason for arbitrary exclusion.

## Validation

Run-level metadata were manually verified against the NCBI SRA records
before automation was implemented.
