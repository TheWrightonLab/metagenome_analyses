#!/usr/bin/python

#PYTHON SCRIPT 
#written by: Richard Wolfe
#
#to run type: python pullseq_header_name.py -i <inputfile> -o <outputfile> -n <file with names> -e <exclude T or F>
#         or: ./pullseq.py -i <inputfile> -o <outputfile> -m <min sequence length>
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
# extracts sequences from a fasta file that belong to a list of scaffolds
#  the sequences are labeled as:  >scaffold_0_1
#    the scaffold this sequences belong to is scaffold_0 and is gene 1
#  the list is simliar to this: ORIG_scaffold_0
#
#   -i <fasta file> (required) scaffold file to extract sequences from
#   -o <file name>  (required) name of file to write sequences into
#   -s <file name>  (required) file of scaffold ids to extract
#   

import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse


#create an argument parser object
#description will be printed when help is used
parser = argparse.ArgumentParser(description='A script to extract sequences from a fasta file')

#add the available arguments -h and --help are aqdded by default
#if the input file does not exist then program will exit
#if output file does not exit it will be created
# args.input is the input file Note: cant write to this file because read only
# args.output is the output file
# args.m is the minimum seq length
parser.add_argument('-i', '--input', type=argparse.FileType('r'), help='Input file name',required=True)
parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Output file name', required=True)
parser.add_argument('-s', '--scaffold', type=argparse.FileType('r'), help='File of scaffold ids to extract', required=True)


#get the args
args = parser.parse_args()

#additional argument tests
#if args.excluded != "T":
#	if args.excluded != "F":
#		print "Error: argument -e must be T or F"
#		sys.exit(0)

#Test print the args
#print args

input_lines = 0
input_sequences = 0
output_lines = 0
output_sequences = 0

#read the ids into a list
ids = args.scaffold.readlines()
#remove the \n from each line in ids
# ids should be a list of the gene ids ex: scaffold_1 0r gene1
for index in xrange(len(ids)):
	ids[index] = ids[index].rstrip() #removes whitespace from right of string
	#line = ids[index].split('_')   #split on underscore
	#ids[index] = line[-2] + '_' + line[-1]  #should be scaffold_3
#close the file
args.scaffold.close()	


#read first line should be header line starts with ">"
line = args.input.readline()
input_lines = input_lines + 1

#if the file is not empty keep reading one at a time
while line:
	sequence = ""
	header = ""	

	#input_lines = input_lines + 1
	line = line.rstrip()  #remove whitespace at end includung endl
	header = line
	input_sequences = input_sequences + 1

	#read sequence
	line = args.input.readline()
	input_lines = input_lines + 1
	line = line.rstrip()  #remove whitespace at end includung endl
	

	while line:
		#input_lines = input_lines + 1
		#if line starts with > it is the header line for next sequence
		if line.startswith('>'):   #">" in line:
			#input_sequences = input_sequences + 1
			break   #break out of this while loop
				
		else: #this is the seq
			line = line.rstrip()  #remove whitespace at end includung endl
			sequence = sequence + line 
			#read another line
			line = args.input.readline()
			input_lines = input_lines + 1

	#the seq is found go through the ids and see ifthe header starts with an id
	#found = False;
	#the header should be id_1 or id_X where X is gene number
	#we want to remove the _X and get the id
	header_split = header.split() #split the header on whitespace
	str = header_split[0].lstrip('>') #remove leading >
	scaf = str.split('_')
	#str = scaf[0] + '_' + scaf[1]
	str = scaf[0]
	i = 1
	while i < len(scaf) - 1:
		str = str + "_" + scaf[i]		
		i += 1

	#if i == 1:
	#	print "Error .. there was no gene number"
	#	sys.exit(1)

	#print str

	if str in ids:
		args.output.write(header + "\n")
		args.output.write(sequence + "\n")
		output_sequences = output_sequences + 1

	



#close the files
args.input.close()
args.output.close()

print "number of scaffolds = ", len(ids)
print "Lines read from input file = ", input_lines
print "Sequences in input file = ", input_sequences
print "Sequences written to output file = ", output_sequences

print "Script finished..."
