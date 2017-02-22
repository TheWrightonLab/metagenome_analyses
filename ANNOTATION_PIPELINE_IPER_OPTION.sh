#!/bin/bash

#ANNOTATION_PIPELINE_IPER_OPTION.sh  script to run pipeline
#
#  written by Richard Wolfe
#
#   $1 = protein sequences fasta file from prodigal
#        >scaffold_0_1
#        GFSP......
#   $2 = gene sequences fasta file from prodigal
#        >scaffold_0_1 
#         Note: if this file does not exist, then will just make errors on screen
#        ACTG.......
#   $3 = NOT_USED
#        the list of contigs to pull from the above 2 files
#        All_contogstopull.txt
#        ORIG_scaffold_0  (will pull scaffold_0_0....scafold_0_1...)
#        Note: ORIG can be anything but must have an _ before Ex: pre_fix_scaffold_0
#   $4 = An id that is added in front of the scaffold_4_24 in the final 2 fasta files 
#        and the annotation file. Can be anything Ex: T82_8
#        
#   $5 = IPER or NO_IPER or PFAM
#        if want to run iperscan or the PFAM script
#   $6 = number of threads

#make sure 6 attributes
#check if 6th variable is empty
if [ -z $6 ]
then
  echo "You did not provide 6 attributes"
  exit 1
fi

#check if valid string for $5
if [ "$5" == "IPER" ]
then
   echo "Iperscan option is selected"
elif [ "$5" == "PFAM" ]
then
   echo "PFAM scripts will be run"
elif [ "$5" == "NO_IPER" ]
then
   echo "Iperscan will not be performed"
else
   echo "Variable 5 must be either IPER or NO_IPER"
   exit 1
fi

#exit

#get filenames from path so we dont include the path
#in the new file names
fname1=$(basename $1)
fname2=$(basename $2)
echo $fname1
echo $fname2

#check if files already exist so we dont overwrite 
#with new files
#only checks a few 
for f in $fname1.3 combined.iprscan renamed_ublast_uniref90.b6 renamed_ublast_KEGG.b6 uniref90_ublast_renamed.b6 KEGG_ublast_renamed.b6 renamed.unirbh.txt renamed.unirbh.txt renamed_ublast_uniref90.b6.BIT_SCORE60.b6 renamed_ublast_KEGG.b6.BIT_SCORE60.b6 uniref90_ublast_renamed.b6_BIT_SCORE_300 KEGG_ublast_renamed.b6_BIT_SCORE_300 
do
   if [ -f $f ]
   then
      echo "Error .. File $f already exists"
      exit 1
   fi
done


 

if [ "$5" == "IPER" ]
then


#make sequences in fasta file on single line
python make_fasta_seq_single_line.py -i $1 -o $fname1.3


echo ' '
echo 'Calculating the number of lines to put in the iperscan files'
echo ' '
numLines=`cat $fname1.3 | wc -l`
numSeq1=$(( numLines / 2 ))
echo "There are $numLines lines in the file $fname1.3"
echo "There are $numSeq1 sequences in the file $fname1.3"
numLines=$(( numLines / 2))
numLines=$(( numLines / 25 ))
numLines=$(( numLines + 1 ))
numLines=$(( numLines * 2 ))
numSeq1=$(( numLines / 2 ))

echo "There will be $numLines lines in each iperscan file"
echo "There will be $numSeq1 sequences in each iperscan file"
#echo 'A sequence takes 2 lines'
echo ' '

#exit
################


#run interproscan
echo " "
echo "Running parallel interproscan"
echo " "

interproscan_parallel.sh  $fname1.3 $numLines



#calculating the number of sequences in the split files
iprlines=`cat file_* | wc -l`
iprscanresults=`cat file_*.iprscan | wc -l`
iperlines=$(( iprlines - iprscanresults ))
iprsequences=$(( iperlines / 2 ))

echo ' '
echo "The total number of sequences that were in all of the 25 split files = $iprsequences"
echo ' '

#calculate the number of sequences in the iprscan results
iprseqcount=0

for f in file_a*
do
  #if there is an output file from iperscan
  if [ -f $f.iprscan ]
  then
     #count the lines in the input file
     filesequences=`cat $f | wc -l`
     iprseqcount=$(( iprseqcount + filesequences ))
  fi
done


#This should not happen but just in case
file="file_az.iprscan"
if [ -f $file ]
then
   echo ' '
   echo 'ERROR MORE THAN 25 iperscan files were made'
fi

iprseqcount=$(( iprseqcount / 2 ))
echo ' '
echo "The number of sequences that made it through iperscan = $iprseqcount"
echo ' '

if (( $iprseqcount != $iprsequences ))
then
   echo ' '
   echo 'NOT ALL OF THE SEQUENCES WENT THROUGH IPRSCAN'
   echo ' '
else
   echo ' '
   echo 'All of the sequences went through iprscan'
   echo ' '
fi

##################################################
echo ' '
echo 'Combining the 25 iperscan results into the file combined.iprscan' 
echo ' '
cat file_a*.iprscan > combined.iprscan

rm -f file_a*.iprscan
rm -f file_a*

####end if iperscan

#if we are using the local pfam ddatabase 
elif [ "$5" == "PFAM" ]
then
  #run the protein file through the pfam scan
  #/opt/PfamScan/pfam_scan.pl -fasta $1 -dir /opt/PfamScan/Data_files -outfile pfam_scan_output.txt
  python parallel_PfamScan.py -n $6 -f $1 -o pfam_scan_output.txt --OSC F

  #convert the output file to the same as it would be from iperscan
  python convert_pfam_to_iperscan.py -i pfam_scan_output.txt -o combined.iprscan  -p /opt/PfamScan/Data_files/Pfam-A.hmm.dat


else
  #iperscan was not selected
  #make an empty file
  echo " "
  echo "Making an empty combined.iperscan file because iperscan was not run"
  echo " "
  echo " " > combined.iprscan
fi



#run reverse best hits on the pulled sequences
echo ' '
echo 'Running the reverse best hits'
echo ' '

reverse_best_hits.sh $1 $6

#this makes 11 files


perl perl1.pl renamed_ublast_uniref90.b6.BIT_SCORE60.b6  > renamed_ublast_uniref90.b6.BIT_SCORE60.b6.OUT1.txt
perl perl1.pl renamed_ublast_KEGG.b6.BIT_SCORE60.b6 > renamed_ublast_KEGG.b6.BIT_SCORE60.b6.OUT1.txt

perl perl2.pl renamed.unirbh.txt > renamed.unirbh.txt.OUT1.txt
perl perl2.pl renamed.keggrbh.txt > renamed.keggrbh.txt.OUT1.txt


SUBSTRING1="$4"

#Pulling all the annotations from unirbh, keggrbh, uniref, kegg, iprscan
perl perl4_NEW.pl renamed_ublast_uniref90.b6.BIT_SCORE60.b6.OUT1.txt renamed_ublast_KEGG.b6.BIT_SCORE60.b6.OUT1.txt  renamed.unirbh.txt.OUT1.txt renamed.keggrbh.txt.OUT1.txt combined.iprscan > ANNOTATION_OUT_$fname1.3.txt

#Arranging the Annotations in sequence according to database preference - RBH-KEGG, RBH-UNIREF, BLAST-KEGG, BLAST-UNIREF, IPRSCAN  
grep "RBH" ANNOTATION_OUT_$fname1.3.txt | grep "db=KEGG" > RBH_KEGG1
grep "RBH" ANNOTATION_OUT_$fname1.3.txt | grep "db=UNIREF" >> RBH_KEGG1
grep "BLAST" ANNOTATION_OUT_$fname1.3.txt | grep "db=KEGG" >> RBH_KEGG1
grep "BLAST" ANNOTATION_OUT_$fname1.3.txt | grep "db=UNIREF" >> RBH_KEGG1
grep "IPRSCAN" ANNOTATION_OUT_$fname1.3.txt >> RBH_KEGG1

#Pulling annotations for same contig/scaffold on same line
python pull_all_contig_annotations.py -i RBH_KEGG1 -o  ANNOTATION_OUT_$fname1.3.txt_FINAL.txt

#Ranking system - All databases - A, 4 databases(One RBH atleast) - B, 3 databases(One BLAST atleast) - C, 2 databases(One BLAST atleast) - D, 1 database(IPRSCAN only) - E
perl perl6.pl ANNOTATION_OUT_$fname1.3.txt_FINAL.txt > $SUBSTRING1.ANNOTATION_OUT.txt_FINAL_RANKED.txt

#Adding headers to the .faa and .fna files with binned contigs
(
python write_annotation_to_fasta.py -i $1 -o $fname1.3.4 -a ANNOTATION_OUT_$fname1.3.txt_FINAL.txt -j $4
) &

#check if this file exists
if [ -f $2 ]
then
(
python write_annotation_to_fasta.py -i $2 -o $fname2.3.4 -a ANNOTATION_OUT_$fname1.3.txt_FINAL.txt -j $4
)&
fi

wait	

#i added so prefix is added to output file
#sed -i "s/scaffold_/$4_scaffold_/g" $SUBSTRING1.ANNOTATION_OUT.txt_FINAL_RANKED.txt
sed -i "s/^/$4_/g" $SUBSTRING1.ANNOTATION_OUT.txt_FINAL_RANKED.txt

#i added so that the sequences with out an annotation are added to the results file
grep 'Unknown_Function' $fname1.3.4 > $SUBSTRING1.$fname1.3.4.5_unknown_headers
sed  -i "s/>//g" $SUBSTRING1.$fname1.3.4.5_unknown_headers

awk -F' Unknown_Function' '{print $1 "\tF\tUnknown Function"}' $SUBSTRING1.$fname1.3.4.5_unknown_headers >> $SUBSTRING1.ANNOTATION_OUT.txt_FINAL_RANKED.txt

#All the required files copied to results directory
mkdir annotation_results
cp $SUBSTRING1.ANNOTATION_OUT.txt_FINAL_RANKED.txt annotation_results/$4_ANNOTATION_OUT.txt
cp $fname1.3.4 annotation_results/$4_ANNOTATED_$fname1
cp $fname2.3.4 annotation_results/$4_ANNOTATED_$fname2

rm -f $SUBSTRING1.ANNOTATION_OUT.txt_FINAL_RANKED.txt 


echo " "
echo "Removing intermediate files"
echo " "
rm -f ANNOTATION_OUT_$fname1.3.txt
rm -f ANNOTATION_OUT_$fname1.3.txt_FINAL.txt
rm -f RBH_KEGG1
    	
rm -f $fname1.3.4
rm -f $fname2.3.4 
rm -f $SUBSTRING1.$fname1.3.4.5_unknown_headers


echo "Step3 Completed Successfully!"
echo "All the Analysis steps completed Successfully!"
echo "Results were written to the folder:  annotation_results"
echo " "

echo ' '
echo 'Annotation pipeline has completed'
echo ' ' 
