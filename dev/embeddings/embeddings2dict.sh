#!/usr/bin/env bash

lt-print -H ../../eng-uum.autobil.bin  | hfst-txt2fst | hfst-minimise -o eng-uum.autobil.hfst

cat embeddings.tsv | awk -F'\t' '{ OFS=FS; $NF=1- $NF; }1' > embeddings-weight.tsv

hfst-strings2fst -Sj embeddings-weight.tsv  | hfst-minimise | hfst-compose -1 - -2 eng-uum.autobil.hfst | hfst-minimise | hfst-union -1 - -2 eng-uum.autobil.hfst | hfst-minimise -o eng-uum.fuzzybil.hfst

hfst-expand -c0 -w -p "cat<n>" eng-uum.fuzzybil.hfst | sort -k2

