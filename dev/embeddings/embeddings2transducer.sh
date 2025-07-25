#!/usr/bin/env bash

cat eng-uum.embeddings.tsv | awk -F'\t' '{ OFS=FS; $NF=1- $NF; }1' > eng-uum.embeddings-weighted.tsv

hfst-strings2fst -Sj eng-uum.embeddings-weighted.tsv -o eng-uum.embeddings.hfst

hfst-expand -c0 -w -p "cat<n>" eng-uum.embeddings.hfst | sort -k2

