#!/usr/bin/python

#PYTHON SCRIPT 
#written by: Richard Wolfe
#
#to run type: python single_copy_genes.py -i <inputfile> -o <outputfile> -m <min sequence length>
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
# Display the gene cluster that contains the gen of interest
#  Ex: scaffold_10_35 will show all the genes from each organism that are in the same ITEP cluster
#
        

#
#  This script makes a fasta seq on a single line
#
#
#


import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse
#import os       #to run system commands
#import datetime #to make timestamp
#import glob     #for * in file name
#import re       #for reg expressions
#from string import maketrans #to make translate table for string timetable

import toolbox #import my toolbox with defs

def run_exit():
	
	print ""
	print "Script finished..."

	sys.exit(0)

	return






print "Script started ..."


#create an argument parser object
#description will be printed when help is used
parser = argparse.ArgumentParser(description='A script to put the sequence on a single line')

#add the available arguments -h and --help are added by default
#if the input file does not exist then program will exit
#if output file does not exit it will be created
# args.input is the input file Note: cant write to this file because read only
# args.output is the output file
# args.m is the minimum seq length
parser.add_argument('-i', '--input_file', type=argparse.FileType('rU'), help='Input fasta file',required=True)
parser.add_argument('-o', '--out_file', type=argparse.FileType('w'), help='output file',required=True)

#get the args
args = parser.parse_args()

#additional argument tests


input_lines = 0
input_seqs = 0
out_lines = 0
out_seqs = 0

line = args.input_file.readline()

while line:
	
	
	header,sequence,line,s_lines = toolbox.read_fasta(line,args.input_file)

	#the seq is found go through the ids and see ifthe header starts with an id
	#Note the header and sequence still have endlines	

	input_seqs += 1
	input_lines += (1 + s_lines) #the header line and the seq lines

	#print "processing seqs = ", input_seqs

	sequence = sequence.replace("\n", "")
	
	#write the seq to outfile
	args.out_file.write(header)
	args.out_file.write(sequence + "\n")
	out_seqs += 1
	out_lines += 2
	
     


print ""
print "lines in input file = ",input_lines
print "sequences in input file = ",input_seqs
print ""
print "lines wrote to out file = ", out_lines
print "sequences wrote to out file = ", out_seqs
print ""

run_exit()
