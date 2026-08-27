awk '
/^>/ {
    if (name != "") {
        gaps=seq
        gsub(/[^-]/,"",gaps)

        amb=seq
        gsub(/[ACGTacgt-]/,"",amb)

        print name, length(seq), length(gaps), length(amb)
    }
    name=substr($0,2)
    seq=""
    next
}
{
    seq=seq $0
}
END {
    gaps=seq
    gsub(/[^-]/,"",gaps)

    amb=seq
    gsub(/[ACGTacgt-]/,"",amb)

    print name, length(seq), length(gaps), length(amb)
}' results/phylogeny/HBV_aligned.fasta

echo "done"
