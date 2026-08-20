import pandas as pd
import requests
from io import StringIO
import time

# --------------------------------------------------
# 1. Input file
# --------------------------------------------------

input_file = "metadata/manual_sra_inventory.tsv"

metadata = pd.read_csv(input_file, sep="\t")

runs = metadata["run"].dropna().unique()

print(f"Runs found: {len(runs)}")


# --------------------------------------------------
# 2. NCBI E-utilities endpoint
# --------------------------------------------------

url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


# --------------------------------------------------
# 3. Retrieve RunInfo for each run
# --------------------------------------------------

results = []

for run in runs:

    print(f"Retrieving {run}...")

    params = {
        "db": "sra",
        "id": run,
        "rettype": "runinfo",
        "retmode": "text",
        "tool": "hbv_genomics_project",
        "email": "olawaleadejumobi08@gmail.com"
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    run_data = pd.read_csv(StringIO(response.text))

    results.append(run_data)

    # Respect NCBI request-rate guidance
    time.sleep(0.4)


# --------------------------------------------------
# 4. Combine all runs
# --------------------------------------------------

automated_metadata = pd.concat(
    results,
    ignore_index=True
)


# --------------------------------------------------
# 5. Save result
# --------------------------------------------------

output_file = "metadata/automated_sra_metadata.tsv"

automated_metadata.to_csv(
    output_file,
    sep="\t",
    index=False
)

print(f"Saved: {output_file}")
