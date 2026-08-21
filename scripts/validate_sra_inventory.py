

import pandas  as pd
INPUT = "metadata/manual_sra_inventory.tsv"

df  = pd.read_csv(INPUT, sep="\t")

print("Number of records:", len(df))
print("Number of columns:", len(df.columns))
print(df.columns.to_list())

print("\nFirst five records:")

print(df.head()) 

#	Required columns
required_columns = [
	"sample_id", 
	"biosample", 
	"sra_sample",
	"experiment",
	"run",
	"platform", 
	"layout",
	"read1_mean_length",
	"read2_mean_length", 
	"spots",
	"bases_M",
	"size_mb", 
	"gc_percent", 
	"data_status",
	"inclusion", 
]


missing_columns = [
	col for col in required_columns
	if col not in df.columns
]

if missing_columns:
	print("ERROR: Missing columns:", missing_columns)
else: 
	print("PASS: All required columns present")

# 	Check duplicate run accessions
duplicates = df["run"].duplicated().sum()

if duplicates ==0:
	print("PASS: No duplicate run accessions")
else: 
	print(f"WARNING: {duplicates}  duplicate run accessions")

#	Check layout 
if df["layout"].eq("PAIRED").all():
	print("PASS: Allsamples are paired-end")
else:
	print("WARNING: Mixed sequencing layouts")


#	Check inclusion
included = (df["inclusion"] == "Include").sum()
excluded = (df["inclusion"] == "Exclude").sum()

print (f"Included samples: {included}")
print (f"Excluded samples: {excluded}")

#	Check GC Content
invalid_gc = df[
	(pd.to_numeric(df["gc_percent"], errors="coerce") < 0) |
	(pd.to_numeric(df["gc_percent"], errors="coerce") > 100)
]

if len(invalid_gc) == 0:
	print("PASS: GC percentages within valid range")
else :
	print("WARNING: Invalid GC percemtages detected")

print("\nValidation complete.")

