for fasta in results/consensus/*/*_consensus.fasta; do
    sample=$(basename "$fasta" _consensus.fasta)

    sed "1s/.*/>${sample}/" "$fasta"
done > results/consensus/combined/HBV_consensus_all.fasta
