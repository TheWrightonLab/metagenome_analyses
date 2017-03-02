# Metagenomic-Analyses

This is all of the scripts to analyze metagenomic data the way we do in the Wrighton lab. Using the comprehensive scripts outlined below you should be able to informatically repeat all of our computational steps.

We have also broken up all of these individual steps into separate repositories as they are cited in the paper.

#Assemblies with IDBA-ud
This script assembles quality trimmed, joined reads. We use sickle to quality trim our reads.
https://github.com/najoshi/sickle

Dependencies

IDBA-ud https://github.com/loneknightpy/idba

AMPHORA2 https://github.com/martinwu/AMPHORA2 

python

Run this command as follows:

python idba_ud_wrapper.py -r R1R2_trimmed.fastq -o idba_ud_assembled/

#16S reconstruction from raw reads using EMIRGE

This script uses unassembled quality trimmed reads to reconstruct 16S and estimate abundance

Dependencies

EMIRGE https://github.com/csmiller/EMIRGE

python 2.6

Run this command as follows

python emirge_pipeline.py -f forwardreads -r reversereads -i jobid -e emailaddress

#Building an OTU table from EMIRGE fasta file in QIIME

COMING SOON

#Quicklooks to look at coverage, scaffolds and Uniref taxonomy. 
This is a bash script that has 10 positions
This is the main script: QUICKLOOKS_PIPELINE.sh

Software dependencies

  bowtie2
  
  prodigal
  
  usearch
  
 Additional script dependencies:
  perl_quicklook1.pl
  
  contig_stats.pl
  
  make_contig_cov_file.py
  
  pullseq.py
  
  add_missing_annotations.py
  
These scripts need to be placed in the same directory you are working in or be executable from a root directory. Alternatively you can alter the QUICKLOOKS_PIPELINE.sh script to call to the scripts where you have placed them on your machine.

Run this command as follows:

bash QUICKLOOKS_PIPELINE scaffold.fa forward.reads.fastq reverse.reads.fastq min.length.of.contigs. Job.id BOWTIE email NA threads 0.0001

$1 = path to scaffold.fa file Ex ../scaffold.fa

   -this could be a degapped scaffold file such as 100_percent_scaffold_degap
   
$2 = path to forward reads Ex  ../../R1_All_trimmed.fastq or NA if NO_BOWTIE

$3 = path to reverse reads Ex: ../../R2_All_trimmed.fastq or NA if NO_BOWTIE

$4 = min length of cotigs  Ex:  1000

$5 = Job ID  Ex: F02_w 

   -can be anything (no spaces) just added to front of scaffold as an id
   
   -ex: F02_4_scafold_67 or F_0_@_scaffold_67
   
$6 = BOWTIE or NO_BOWTIE  

     note if NO_BOWTIE is used then $2 and $3 can say NA because these files are not used
     
$7 = email or NO_EMAIL

$8 = NA if BOWTIE or if NO_BOWTIE and you dont want contig stats

     or path to Contig_coverage_score_100_Final_paired.txt (file with stats) when NO_BOWTIE 
     
$9 = number of threads

$10 = evalue default should be 0.0001

#annotation pipeline to annotate metagenomic data using KEGG, UniProt, NCBI, PFAM and IPERscan
This script takes a scaffold fasta file of nucleic acids, calls genes using prodigal and then annotates those genes against KEGG, NCBI, PFAM and Uniprot databaseses. The result of this script is multiple prodigal files for gene mapping, the specific database hits, and then a summary directory with a text file containing the full annotation, an annotated amino acid fasta file with the best hit for the protein, and an annotated nucleic acid fasta file (genes) with the annotation.

use annotate_fasta.sh

Software dependencies

  prodigal

  KEGG

  interproscan

  ublast

  uniref

For sotware, be sure the script calls to the correct database name depending on the software that you have and databases you use. This is completely set up for our server, but should be transferrable with a few tweaks.

Additional dependent scripts:

pullcontigs.pl

ANNOTATION_PIPELINE_IPER_OPTION.sh

make_fasta_seq_single_line.py

interproscan_parallel.sh

parallel_PfamScan.py

convert_pfam_to_iperscan.py

reverse_best_hits.sh

perl1.pl

perl2.pl

perl4_NEW.pl

pull_all_contig_annotations.py

perl6.pl

write_annotation_to_fasta.py

Dependent scripts must me in the same directory, or executable from a root directory.

Run this command as follows

#Single copy genes to identify bin completion and misbins

This script uses AMPHORA2 to call open reading frames and then 



Dependencies

MarkerScanner.pl
MarkerAlignTrim.pl
Phylotyping.pl
single_copy_genes_make_table.py

-i --input_file   <string>      (required)    
-o --output_file  <string>      (required)       
-e --evalue 	  <string>		(required)
-t --type		  <string>		(required)
-p --processors	  <string>		(required)
-s --seq_type 	  <string>		(required)
-c --OSC		  <string>		(optional)  



Run this script as follows
python single_copy_genes.py -i <inputfasta> -o <outputfile> -e <evalue> -t <type> -s <DNA or amino acid> -p <processors> 
