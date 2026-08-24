

#	LA005 raw-read retrieval

##	Sample

- Sample ID: LA005
- Biosample: SAMN19694648
- Experiment: SRX11143886
- Run: SRR14811416
- Bioproject: PRJNA737147


##	Retrieval 

Raw reads were retrieved from the nCBI Sequnece Read Archive using "fasterq-dump".

Command:

```bash

fasterq-dump SRR14811416 --split-files --threads 4 --outdir data/raw/LA005

```


The resulting paired-end reads were renamed:

LA005_R1.fastq
LA005_R2.fastq
