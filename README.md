
# HBV Genomic Surveillance & Molecular Epidemiology

## Project status

Currenty working through Phases 2-7, from raw sequence QC to genotyping, using LA005 as the pilot sample. 

Phase 1 — Dataset selection and metadata curation, already completed.

## Overview

This project is my attempt to develop a documented reproducible bioinformatics workflow for
whole-genome hepatitis B virus (HBV) sequencing data. The broader aim is to develop a workflow 
that can later be adapted to other viral pathogens.

The projected starts with publicly available raw sequencing data and will progress through:

- raw sequence quality control
- read preprocessing
- reference mapping and genome reconstruction
- variant analysis
- consensus seqeuence generation
- genotype analysis
- phylogenetics
- statistical analysis
- molecular epidemiological interpretation
- data visualization 

Once the analytical workflow is working properly, I plan to convert it into Nextflow, 
containerize it and add interactive data visualization layer and automated testing.

## Scientific question

How reliably can a reproducible whole-genome sequencing workflow
reconstruct HBV genomes and resolve viral genotype structure from
Illumina short-read data?

## Project Roadmap

| Phase | Task | Progress |
|------|------|----------|
| 1 | Build the scientific dataset | Complete |
| 2 | Raw sequence QC | LA005 completed |
| 3 | Pre-processing | LA005 completed |
| 4 | Reference mapping / genome reconstruction | LA005 completed |
| 5 | Variant analysis | LA005 completed |
| 6 | Consensus sequences | LA005 pilot completed |
| 7 | Genotyping | In progress |
| 8 | Phylogenetic analysis | Not started |
| 9 | Statistical analysis | Not started |
| 10 | Dashboard | Not started |
| 11 | Convert workflow into Nextflow | Not started |
| 12 | Containerisation | Not started |
| 13 | Automated testing | Not started |
| 14 | Documentation | Ongoing |

The remaining samples will be processed through the same workflow after checking the pilot stages.

## Dataset
The dataset is from NCBI BioProject **PRJNA737147**

I selected 15 HBV whole-genome sequencing runs generated using Illumina MiSeq. Before 
starting the sequence aalysis, I manually checked the SRA records and created a curated 
inventory containing the sample, Biosample, experiments and run accessions together with the 
basic sequencing information.

The dataset selction process is documented in:

`docs/dataet_selection.md`

The manually verified SRA inventory is available in:

`metadata/manual_sra_inventory.tsv`

I also wrote the scripts to retrieve SRA metadata and check the manually curated inventory:

`scripts/retrieve_sra_metadata.py`

`scripts/validate_sra_inventory.py`

One limitation of this dataset is the lack of detailed epidemiological and clinical metadata. 
This limits the epidemiological questions that can be reasonal=bly addressed with this dataset.



## Pilot Analysis - LA005

I used **LA005 (SRR14811416)** as the first sample to work throughthe pipeline before scaling the 
analysis to all 15 samples.

The raw data contained 42,344 paired end reads.


### Raw read QC and preprocessing 

FastQC was used to inspect the raw reads R1 was generally high quality, while R2 showed a decline 
in per-base sequence quality.

The reads were then processed woth `fastp`.

After filtering:

- 41,387 read pairs were retained 
- R1 Q30 increased from 93.67% to 94.21%
- R2 Q30 increased from 73.65% to 75.12%
- 2,398 reads contained adapter sequence that was trimmed.


### Reference mapping

The processed reads were mapped against the HBV reference sequence **NC_003977.2**
using BWA-MEM2.

For LA005:

- 253 primer reads mapped
- 0.31% of primary reads mapped to the HBV reference 
- genome coverage was 100%
- mean depth was approximately14.6×

The low mapping percentage is an improtant observation and will be compared across the 
remaining samples rather than treated as a successful mapping result simply because the
genome was fully covered.


### Variant Analysis

Initial variant calling identified 280 recordds:

- 279 SNPs
- 1 indel

After moving to haploid calling and applying the current filering criteria, 98 variants remained:

- 97 SNPs
- 1 indel 

The filtering strategy will be reassessed as more samples are processed.

### Consensus sequence 

A pilot consensus sequence has been generated for LA005.

This step also raised an important issue with reference-based consensus sequence generation: 
positions without sufficient evidence can retain the reference base.
Before using the consensus seqences for final genotype and phylogenetic analysis,
I will therefore evaluate coverage-aware masking of poorly supported positions.



### Next Step

The immediate next step is genotype analysis of the LA005 pilot sequence, beginning with HBV-GLUE.

After this, the workflow will be applied to the remaining samples and the resulting genotypes will 
later be evaluated by phylogenetic placement against the appropriate HBV reference sequences.


## Reproducibility

The project is being developed under Git version control.

The software environment is recorded in:

`environment.yml`

The current workflow uses tools including:

- SRA Toolkit
- FastQC
- fastp
- bwa-mem2
- samtools
- BCFtools
- MultiQC

The analystical steps are being worked through manually first. 
Once I am satisfied that the workflow and the underlying decisions are sound, the pipeline will be 
moved into Nextflow and subsequently containerised and tested.



## Author

Olawale Adejumobi

