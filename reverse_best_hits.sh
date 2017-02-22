#!/bin/bash

#Script by Richard Wolfe
#
# Performs a ublast hit to a uniref database
# Performs a ublast to kegg
# makes a database from the input fasta file
# Perform uniref database ublast to input sequences
# Perform keg database ublast to input sequences
# runs a python script to report the sequences in both uniref ublast
# runs python script to report sequences in both kegg ublasts
#
#  To run:  ./reverse_best_hits.sh   file.faa num_threads
#  file.faa is a fasta file of protein sequences
# 
#  NOTE: each usearch runs on all 80 processors so DO NOT run in parallel


#check if files exist from a previous run
for f in renamed_ublast_uniref90.b6 renamed_ublast_KEGG.b6 uniref90_ublast_renamed.b6 KEGG_ublast_renamed.b6 renamed_ublast_uniref90.b6.BIT_SCORE60.b6 renamed_ublast_KEGG.b6.BIT_SCORE60.b6 uniref90_ublast_renamed.b6_BIT_SCORE_300 KEGG_ublast_renamed.b6_BIT_SCORE_300 renamed.unirbh.txt renamed.keggrbh.txt 
do
   if [ -f $f ]
   then
      echo "Error .. File $f already exists"
      exit 1
   fi
done


#get filenames from path so we dont include the path
#in the new file names
fname=$(basename $1)

echo $fname1


echo "Performing fasta file ublast uniref database" 

usearch -ublast $1  -db /ORG-Data/Database/UniRef/uniref90.udb -maxhits 1 -evalue 0.0001 -blast6out renamed_ublast_uniref90.b6 -threads $2



echo "Performing fasta file ublast kegg  database"

usearch -ublast $1 -db /ORG-Data/Database/KEGG/kegg-all-orgs_12102013.pep.udb -maxhits 1 -evalue 0.0001 -blast6out renamed_ublast_KEGG.b6 -threads $2



echo " "
echo 'Making a uclust database'
echo ' '
usearch -makeudb_ublast  $1  -output $fname.udb

echo ' '
echo 'running usearch uniref90 in reverse'


echo ' '
usearch -ublast /ORG-Data/Database/UniRef/uniref90.fasta -db $fname.udb -maxhits 1 -evalue 0.0001 -blast6out uniref90_ublast_renamed.b6 -threads $2


echo ' '
echo 'running usearch KEGG in reverse'
echo ' '

usearch -ublast /ORG-Data/Database/KEGG/kegg-all-orgs_12102013.pep -db $fname.udb -maxhits 1 -evalue 0.0001 -blast6out KEGG_ublast_renamed.b6 -threads $2


(
echo 'Removing all data except id from ublast report'
awk '{print $1 "\t" $(NF-10) "\t" $(NF-9) "\t" $(NF-8) "\t" $(NF-7) "\t" $(NF-6) "\t" $(NF-5) "\t" $(NF-4) "\t" $(NF-3) "\t" $(NF-2) "\t" $(NF-1) "\t" $(NF) }'   renamed_ublast_uniref90.b6  > temp1

echo 'Removing hits with a bit score <= 60'
awk ' $12 > 60 { print $0 }'  temp1 > renamed_ublast_uniref90.b6.BIT_SCORE60.b6

echo 'remove temp file temp1'
rm -f temp1
) &

(
echo 'Removing all data except id from ublast report'
awk '{print $1 "\t" $(NF-10) "\t" $(NF-9) "\t" $(NF-8) "\t" $(NF-7) "\t" $(NF-6) "\t" $(NF-5) "\t" $(NF-4) "\t" $(NF-3) "\t" $(NF-2) "\t" $(NF-1) "\t" $(NF) }'   renamed_ublast_KEGG.b6 > temp2

echo 'Removing hits with a bit score <= 60'
awk ' $12 > 60 { print $0 }'  temp2 > renamed_ublast_KEGG.b6.BIT_SCORE60.b6

echo 'remove temp file temp2'
rm -f temp2
) &

(
echo ' '
echo 'removing annotation data info from uniref90_ublast_contigs_100.b6'
echo ' '
awk '{print $1 "\t" $(NF-10) "\t" $(NF-9) "\t" $(NF-8) "\t" $(NF-7) "\t" $(NF-6) "\t" $(NF-5) "\t" $(NF-4) "\t" $(NF-3) "\t" $(NF-2) "\t" $(NF-1) "\t" $(NF) }'  uniref90_ublast_renamed.b6  > temp4

echo ' '
echo 'Removing hits with a bit score <= 300'
echo ' '
awk ' $12 > 300 { print $0 }'  temp4 > uniref90_ublast_renamed.b6_BIT_SCORE_300

echo 'remove temp file temp4'
rm -f temp4
) &

(
echo ' '
echo 'removing annotation data info from KEGG_ublast_renamed.b6'
echo ' '
awk '{print $1 "\t" $(NF-10) "\t" $(NF-9) "\t" $(NF-8) "\t" $(NF-7) "\t" $(NF-6) "\t" $(NF-5) "\t" $(NF-4) "\t" $(NF-3) "\t" $(NF-2) "\t" $(NF-1) "\t" $(NF) }'  KEGG_ublast_renamed.b6  > temp3

echo ' '
echo 'Removing hits with a bit score <= 300'
echo ' '
awk ' $12 > 300 { print $0 }'  temp3 > KEGG_ublast_renamed.b6_BIT_SCORE_300

echo 'remove temp file temp3'
rm -f temp3
) &


#wait for all 4 to finish
wait



echo ' '
echo 'Selecting hits that are in the forward hits and revers hits'
echo ' '
(
rbh.rb --forward renamed_ublast_uniref90.b6.BIT_SCORE60.b6  --reverse uniref90_ublast_renamed.b6_BIT_SCORE_300  > renamed.unirbh.txt
) &



echo ' '
echo 'Selecting hits that are in the forward hits and revers hits'
echo ' '

(
rbh.rb --forward renamed_ublast_KEGG.b6.BIT_SCORE60.b6  --reverse KEGG_ublast_renamed.b6_BIT_SCORE_300  > renamed.keggrbh.txt 
) &

wait

echo ' '
echo 'Script finished'
echo ' '
