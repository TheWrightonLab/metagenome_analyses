#!/usr/bin/python

#PYTHON SCRIPT 
#written by: Richard Wolfe
#
#to run type: python single_copy_genes.py -i <inputfasta> -o <outputfile> -e <evalue>
#	-t <type> -s <DNA or amino acid> -p <processors> 
#         or: ./single_copy_genes.py attributes
#
#   if error: /usr/bin/python^M: bad interpreter: No such file or directory
#      -there is a windows endl after shebang
#      -open in vi 
#         once in vi type:
#           :set ff=unix<return>
#           :x<return>
#
#
#
# 
#
#   -i --input_file   <string>      (required)    
#   -o --output_file  <string>      (required)       
#	-e --evalue 	  <string>		(required)
#	-t --type		  <string>		(required)
#	-p --processors	  <string>		(required)
#	-s --seq_type 	  <string>		(required)
#	-c --OSC		  <string>		(optional)  
#
# this script runs AMPHORA2 pipeline and finds single copy genes
# 
#   -input file would be a DNA fasta file for example Methanohalophilus_348_143_42_scaffold.fa which
#     was made by using pullseq to pull certain scaffolds from the scaffold.fa file
#   -output file  is the name you want to call the output file
#
#   Example command to run :
#      python single_copy_genes.py -i Methanohalophilus_348_143_42_scaffold.fa -o Methanohalophilus_348_143_42_phylotype_1e-10.result -e 1e-10 -t Archaea -p 20
#

import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse
import os       #to run system commands
import datetime #to make timestamp
import glob     #for * in file name
from string import maketrans #to make translate table for string timetable




print "Script started ..."


#create an argument parser object
#description will be printed when help is used
parser = argparse.ArgumentParser(description='A script to run AMPHORA2')

#add the available arguments -h and --help are added by default
#if the input file does not exist then program will exit
#if output file does not exit it will be created
# args.input is the input file Note: cant write to this file because read only
# args.output is the output file
# args.m is the minimum seq length
parser.add_argument('-i', '--input_file', type=argparse.FileType('r'), help='input file',required=True)
parser.add_argument('-o', '--output_file', type=argparse.FileType('w'), help='output filen', required=True)
parser.add_argument('-e', '--evalue', help='evalue', required=True)
parser.add_argument('-t', '--type', help='type: Archaea, Bacteria, Mixed', required=True)
parser.add_argument('-p', '--processors', type=int, help='number of processors', required=True)
parser.add_argument('-s', '--seq_type', help='seq_type: DNA or PROT sequence', required=True)
parser.add_argument('-c', '--OSC', help='running on OSC or NO_OSC',default='NO_OSC')


#get the args
args = parser.parse_args()

#additional argument tests
if args.type != 'Archaea':
	if args.type != 'Bacteria':
		if args.type != 'Mixed':
			print "Error: argument -t not Archaea, Bacteria, or Mixed"
			sys.exit(0)
if args.seq_type != 'DNA':
	if args.seq_type != 'PROT':
		print "Error: argument -s not DNA or PROT"
		sys.exit(0)

if args.OSC:
	if args.OSC != "OSC":
		if args.OSC != "NO_OSC":
			print "Error ... -c must be OSC or NO_OSC"
			sys.exit(1)

if args.processors <= 0:
	print "Error: argument --processors <= 0"
	sys.exit(0)


#Test print the args
#print args

#set paths
marker_scanner = "/opt/AMPHORA2/Scripts/MarkerScanner.pl"
marker_align_trim = "/opt/AMPHORA2/Scripts/MarkerAlignTrim.pl"
phylotyping = "/opt/AMPHORA2/Scripts/Phylotyping.pl"
make_table = "/opt/scripts/bin/Phylogeny_Protpipe/single_copy_genes_make_table.py"

if args.OSC == 'OSC':
	marker_scanner = "/users/PAS1018/osu9681/bin/AMPHORA2/Scripts/MarkerScanner.pl"
	marker_align_trim = "/users/PAS1018/osu9681/bin/AMPHORA2/Scripts/MarkerAlignTrim.pl"
	phylotyping = "/users/PAS1018/osu9681/bin/AMPHORA2/Scripts/Phylotyping.pl"
	make_table = "/users/PAS1018/osu9681/bin/single_copy_genes_make_table.py"


#check if files exist from a previous time
#if os.path.isfile('*.aln') or os.path.isfile('*.mask') or os.path.isfile('*.pep') or os.path.isfile('*.phylotype'):
#	print("Files exist from previous run. Please delete or move to a different folder")
#        sys.exit(0)

aln_files = glob.glob('*.aln')   #put all files in the list
mask_files = glob.glob('*.mask')  #
pep_files = glob.glob('*.pep')
phylo_files = glob.glob('*.phylotype')

if len(aln_files) > 0  or len(mask_files) > 0 or len(pep_files) > 0 or len(phylo_files) > 0:
	print("Files exist from previous run. Please delete or move to a different folder")
	sys.exit(0)

#######################################
#check the input fasta file  for problems
#check if illegal characters are in the first part of the header line
#Illegal characters in taxon-names are: tabulators, carriage returns, spaces, ":", ",", ")", "(", ";", "]", "[", "'"
#Ex: >rplB;_7 [1 - 825] 50S ribosomal protein L2; K02886 large subunit ribosomal protein L2(db=KEGG)
in_lines = 0
sequences = 0

line = args.input_file.readline()
while line:
	in_lines += 1
	if line.startswith(">"):
		sequences += 1
		cols = line.split() #split the line on spaces
		if ":" in cols[0] or "," in cols[0] or ")" in cols[0] or "(" in cols[0] or ";" in cols[0] or "[" in cols[0] or "]" in cols[0] or "'" in cols[0]:
			print "Error ... Illegal character in gene id. Id = " + cols[0]
			print "Please remove ilegal characters from input file and try again"
			sys.exit(1)
 
	line = args.input_file.readline()


print "Lines read from input file = ", in_lines
print "Number of sequences in input file = ",sequences

#close the files so there are no problems
args.input_file.close()
args.output_file.close()



#Step 1 
#perl /opt/AMPHORA2/Scripts/MarkerScanner.pl -Archaea -DNA ../Methanohalophilus_348_143_42_scaffold.fa -Evalue 1e-3

#cmd = 'perl /opt/AMPHORA2/Scripts/MarkerScanner.pl -' + args.type + ' -DNA ' + args.input_file.name + ' -Evalue ' + args.evalue

if args.seq_type == 'DNA':
	if args.type == 'Mixed':
        	cmd = 'perl ' + marker_scanner + ' -DNA ' + args.input_file.name + ' -Evalue ' + args.evalue
	else:
        	cmd = 'perl ' + marker_scanner + ' -' + args.type + ' -DNA ' + args.input_file.name + ' -Evalue ' + args.evalue
else:
	if args.type == 'Mixed':
        	cmd = 'perl ' + marker_scanner + ' ' + args.input_file.name + ' -Evalue ' + args.evalue
	else:
        	cmd = 'perl ' + marker_scanner + ' -' + args.type + ' ' + args.input_file.name + ' -Evalue ' + args.evalue



print 'executing cmd = ', cmd

retvalue = os.system(cmd) #returns 0 if no error in command

if retvalue != 0:  #if command failed
	print "ERROR command did not return 0 and failed"
	sys.exit(1)  #return 0 if sucess


#Step 2
#perl /opt/AMPHORA2/Scripts/MarkerAlignTrim.pl -WithReference -OutputFormat phylip

cmd = 'perl ' + marker_align_trim + ' -WithReference -OutputFormat phylip'

print 'executing cmd = ', cmd

retvalue = os.system(cmd) #returns 0 if no error in command

if retvalue != 0:  #if command failed
	print "ERROR command did not return 0 and failed"
	sys.exit(1)  #return 0 if sucess


#Step 3
#perl /opt/AMPHORA2/Scripts/Phylotyping.pl -CPUs 20 > Methanohalophilus_348_143_42_phylotype_1e-3.result

cmd = 'perl ' + phylotyping + ' -CPUs ' + str(args.processors) + ' > ' + args.output_file.name

print 'executing cmd = ', cmd

retvalue = os.system(cmd) #returns 0 if no error in command

if retvalue != 0:  #if command failed
	print "ERROR command did not return 0 and failed"
	sys.exit(1)  #return 0 if sucess

print 'Finished Step 3'


#############################
#check if amphora2 made the correct number of files
# there should be the same number of .aln .mask .pep .phylotype files
aln_files = glob.glob('*.aln')   #put all files in the list
mask_files = glob.glob('*.mask')  #
pep_files = glob.glob('*.pep')
phylo_files = glob.glob('*.phylotype')

print ""
print "Number of .aln files made = ", len(aln_files)
print "Number of .mask files made = ", len(mask_files)
print "Number of .pep files made = ", len(pep_files)
print "Number of .phylotype files made = ", len(phylo_files)

if len(aln_files) != len(mask_files)  or len(aln_files) != len(pep_files) or len(aln_files) != len(phylo_files):
	print("Error ... The number of files made is not the same")
	sys.exit(1)





print 'Making the new table'

#Step 4 Parse results and make a new table
#column 2 of the results file has the single copy genes
#we need to count the number of occurances of each gene

cmd = 'python ' + make_table + ' -i ' + args.output_file.name + ' -t ' + args.type
print 'executing cmd = ', cmd

retvalue = os.system(cmd) #returns 0 if no error in command

if retvalue != 0:  #if command failed
	print "ERROR command did not return 0 and failed"
	sys.exit(1)  #return 0 if sucess

print 'Finished Step 4'


#print 'Removing AMPHORA2 files that were created'

#cmd = 'rm -f *.aln'
#retvalue = os.system(cmd) #returns 0 if no error in command

#cmd = 'rm -f *.mask'
#retvalue = os.system(cmd) #returns 0 if no error in command

#cmd = 'rm -f *.pep'
#retvalue = os.system(cmd) #returns 0 if no error in command

#cmd = 'rm -f *.phylotype'
#retvalue = os.system(cmd) #returns 0 if no error in command



print "Script finished..."
