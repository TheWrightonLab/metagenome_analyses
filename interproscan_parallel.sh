#!/bin/bash
#interproscan_parallel.sh
# split a fasta file into 25 sections and run ipr on 75 processors
#
#by Richard Wolfe
#
#   command:   ./interproscan_parallel.sh   fastafile.faa  3360
#
#   $2 is the number of lines in each file (number of sequences X 2)
#   For example: if there are 100 sequences in the fasta file, we want 25 files
#   so 4 sequences per file so $2 would be 8

#make sure input fasta file is 1 sequence line
pullseq.py -i $1 -o modified_$1 -m 1

#make sure no *
sed -i "s/\*//" modified_$1

#split into 25 files  there are 100 sequences, so we want 4 sequences per files
# so 8 lines per file
split -l $2  modified_$1 file_
   
#echo 'iperscan logfile' > logfile

#make a lock so somebody else has to wait until this script is done
#if lock file exists then wait 5 seconds

#echo ' '
#echo 'Checking every 5 seconds to see if another instance of interproscan_parallel.sh is active'
#echo 'If this is last line displayed then we are waiting for other instance to complete'
#echo 'You can remove the lockfile at /opt/scripts/bin/Phylogeny_Protpipe/locks/mylock.txt'
#echo ' '


#while true
#do
#	file="/opt/scripts/bin/Ph*/locks/mylock.txt"
#        if [ -f $file ]
#        then
#                #echo "Waiting 5 seconds for file to be unlocked"
#                #echo "Another instance is in use , if not then remove file at"
#                #echo "/opt/scripts/bin/Phylogeny_Protpipe/locks/mylock.txt"
#                sleep 5
#        else
#		echo 'lock file was not found' 
#                break
#        fi
#done


#make the lockfile
#echo "Making a lockfile"
#echo "If you kill the job now you may have to kill grand child processes"
#echo "file is locked" > /opt/scripts/bin/Phylogeny_Protpipe/locks/mylock.txt


#interproscan.sh  -i file_aa  -o file_aa.iprscan -f TSV -iprlookup -goterms >> logfile_aa
#interproscan.sh  -i file_ab  -o file_ab.iprscan -f TSV -iprlookup -goterms >> logfile_ab
#interproscan.sh  -i file_ac  -o file_ac.iprscan -f TSV -iprlookup -goterms >> logfile_ac
#interproscan.sh  -i file_ad  -o file_ad.iprscan -f TSV -iprlookup -goterms >> logfile_ad
#interproscan.sh  -i file_ae  -o file_ae.iprscan -f TSV -iprlookup -goterms >> logfile_ae
#interproscan.sh  -i file_af  -o file_af.iprscan -f TSV -iprlookup -goterms >> logfile_af
#interproscan.sh  -i file_ag  -o file_ag.iprscan -f TSV -iprlookup -goterms >> logfile_ag
#interproscan.sh  -i file_ah  -o file_ah.iprscan -f TSV -iprlookup -goterms >> logfile_ah
#interproscan.sh  -i file_ai  -o file_ai.iprscan -f TSV -iprlookup -goterms >> logfile_ai
#interproscan.sh  -i file_aj  -o file_aj.iprscan -f TSV -iprlookup -goterms >> logfile_aj
#interproscan.sh  -i file_ak  -o file_ak.iprscan -f TSV -iprlookup -goterms >> logfile_ak
#interproscan.sh  -i file_al  -o file_al.iprscan -f TSV -iprlookup -goterms >> logfile_al
#interproscan.sh  -i file_am  -o file_am.iprscan -f TSV -iprlookup -goterms >> logfile_am
#interproscan.sh  -i file_an  -o file_an.iprscan -f TSV -iprlookup -goterms >> logfile_an
#interproscan.sh  -i file_ao  -o file_ao.iprscan -f TSV -iprlookup -goterms >> logfile_ao
#interproscan.sh  -i file_ap  -o file_ap.iprscan -f TSV -iprlookup -goterms >> logfile_ap
#interproscan.sh  -i file_aq  -o file_aq.iprscan -f TSV -iprlookup -goterms >> logfile_aq
#interproscan.sh  -i file_ar  -o file_ar.iprscan -f TSV -iprlookup -goterms >> logfile_ar
#interproscan.sh  -i file_as  -o file_as.iprscan -f TSV -iprlookup -goterms >> logfile_as
#interproscan.sh  -i file_at  -o file_at.iprscan -f TSV -iprlookup -goterms >> logfile_at
#interproscan.sh  -i file_au  -o file_au.iprscan -f TSV -iprlookup -goterms >> logfile_au
#interproscan.sh  -i file_av  -o file_av.iprscan -f TSV -iprlookup -goterms >> logfile_av
#interproscan.sh  -i file_aw  -o file_aw.iprscan -f TSV -iprlookup -goterms >> logfile_aw
#interproscan.sh  -i file_ax  -o file_ax.iprscan -f TSV -iprlookup -goterms >> logfile_ax
#interproscan.sh  -i file_ay  -o file_ay.iprscan -f TSV -iprlookup -goterms >> logfile_ay

#interproscan needs python 2.7
source /opt/python2.7_environment/bin/activate

for f in file_a*
do
  echo " "
  echo "Running $f through interproscan"
  #/opt/my_interproscan_5.11-51.0/interproscan-5.11-51.0/interproscan.sh -i $f -o $f.iprscan -f TSV -iprlookup -goterms > log$f

  #without panther use  -appl ProDom,Hamap,SMART,ProSiteProfiles,ProSitePatterns,SUPERFAMILY,PRINTS,Gene3D,PIRSF,Pfam,TIGRFAM,Coils

  #without lookup service and only -appl TIGRFAM,Pfam,ProSiteProfiles,ProSitePatterns
  /opt/my_interproscan_5.11-51.0/interproscan-5.11-51.0/interproscan.sh -i $f -o $f.iprscan -f TSV -dp -appl TIGRFAM,Pfam,ProSiteProfiles,ProSitePatterns -iprlookup -goterms > log$f

done

#deactivate python 2.7
deactivate

echo ' '
echo '25 interproscan scripts have been completed'
echo 'you may check each logfile for status'

#wait

#remove the lock file
#rm -f /opt/scripts/bin/Phylogeny_Protpipe/locks/mylock.txt
#echo 'Removing the lock file'

echo 'Finished with the 25 scripts'

echo 'Finished with the 25 interproscan scripts'
echo 'Should have made 25 files file_aa.iprscan ... file_ax.iprscan'
echo 'If less than 25 files were made than either 25 input files were not made or errors'
echo 'Number of *.iprscan files:'
ls *.iprscan | wc -l
echo ' '



