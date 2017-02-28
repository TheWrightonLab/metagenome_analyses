# Metagenomic-Analyses

This is all of the scripts to analyze metagenomic data the way we do in the Wrighton lab. Using the comprehensive scripts outlined below you should be able to informatically repeat all of our computational steps.

We have also broken up all of these individual steps into separate repositories as they are cited in the paper.

#Assemblies with IDBA-ud
This script assembles quality trimmed, joined reads. We use sickle to quality trim our reads.
https://github.com/najoshi/sickle

This script has the following dependencies:
IDBA-ud https://github.com/loneknightpy/idba
AMPHORA2 https://github.com/martinwu/AMPHORA2
python

Run this command as follows:

python idba_ud_wrapper.py -r R1R2_trimmed.fastq -o idba_ud_assembled/

#16S reconstruction from raw reads using EMIRGE


#Building an OTU table from EMIRGE fasta file
#Quicklooks to look at coverage, scaffolds and Uniref taxonomy
#annotation pipeline to annotate metagenomic data using KEGG, UniProt, NCBI, PFAM and IPERscan
#Single copy genes to identify bin completion and misbins
