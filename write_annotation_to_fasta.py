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
# extracts sequences from a fasta file 
#  matches to the first whitespace in the header line
#
#   -i <fasta file> (required) file to extract sequences from
#   -o <file name>  (required) name of file to write sequences into
#   -n <file name>  (required) file of header id names to search for
#   -e <T or F>     (required) exclude header names, T = exclude names, F = include names

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
parser.add_argument('-i', '--input', type=argparse.FileType('r'), help='Input fast file name',required=True)
parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Output file name', required=True)
parser.add_argument('-a', '--ann_file', type=argparse.FileType('r'), help='File with the annotations', required=True)
parser.add_argument('-j', '--job_id', help='Job id that will be added to scaffold EX ORIG_scaffold_0_1', required=True)

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

ids = []
annotations = []

line = args.ann_file.readline()
while line:
	line = line.rstrip() #remove endline
	columns = line.split("\t")  #split line on tabs
	columns[0] = columns[0].rstrip()  #in case there are spaces after id

	ids.append(columns[0])
	annotations.append(columns[1])


	line = args.ann_file.readline() #read next line

#read the annotations into a lists annotation and id 
#annotations = args.ann_file.readlines()
#remove the \n from each line in ids
#for index in xrange(len(annotations)):
	#annotations[index] = annotations[index].rstrip() #removes whitespace from right of string
#close the file

args.ann_file.close()	



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

	#the seq is found 
	#get the id from the header line
	items = header.split() #splits on all whitespace
	items[0] = items[0].replace(">", "")  #remove >

	if items[0] in ids:
		index = ids.index(items[0])
		#args.output.write(">" + args.job_id + "_" + items[0] + "_" + annotations[index] + "\n")
		args.output.write(">" + args.job_id + "_" + items[0] + " " + annotations[index] + "\n")
		args.output.write(sequence + "\n")
		output_sequences += 1
	else:
		#args.output.write(">" + args.job_id + "_" + items[0] + "_Unknown_Function\n")
		args.output.write(">" + args.job_id + "_" + items[0] + " Unknown_Function\n")
		args.output.write(sequence + "\n")	
		output_sequences += 1



#close the files
args.input.close()
args.output.close()


print "Lines in ids list = ", len(ids)
print "Lines in annotation list = ", len(annotations)

print "Lines read from input file = ", input_lines
print "Sequences in input file = ", input_sequences
print "Sequences written to output file = ", output_sequences

print "Script finished..."
