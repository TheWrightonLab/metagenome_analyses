#!/usr/bin/python

#PYTHON SCRIPT 
#
#
#to run type: python name.py -i <inputfile> -o <outputfile> -m <min sequence length>
#
#written by Richard Wolfe
#
# extracts sequences from a fasta file 
#
#   -i <fasta file> (required) file to extract sequences from
#   -o <file name>  (required) name of file to write sequences into
#   -m <int>        (required) minimum sequence length to extract


import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse



#paramaters
inputfile = ''  #blank space
outputfile = ''

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
parser.add_argument('-m', type=int, help='Minimum sequence length', required=True)

#get the args
args = parser.parse_args()

#additional argument tests
if args.m < 1:
	print "Error: argument -m < 1"
	sys.exit(0)

#Test print the args
#print args

input_lines = 0
input_sequences = 0
output_lines = 0
output_sequences = 0


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
	if len(sequence) >= args.m:
		args.output.write(header + "\n")
		args.output.write(sequence + "\n")
		output_sequences = output_sequences + 1



#close the files
args.input.close()
args.output.close()

print "Lines read from input file = ", input_lines
print "Sequences in input file = ", input_sequences
print "Sequences written to output file = ", output_sequences

print "Script finished..."
