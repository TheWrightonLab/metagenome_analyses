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
# 
#
#   -i --input_file   <string>      (required)    
#   -o --output_file  <string>      (required)         
#   -g --gene_file
#


import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse
import os       #to run system commands
#import datetime #to make timestamp
#from string import maketrans #to make translate table for string timetable




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
parser.add_argument('-g', '--gene_file', type=argparse.FileType('r'), help='fasta file used to make ublast',required=True)
parser.add_argument('-s', '--scaffold_file', type=argparse.FileType('r'), help='file with scaffold data in it',required=True)

#get the args
args = parser.parse_args()


#additional argument tests
#if args.type != 'Archaea':
#	if args.type != 'Bacteria':
#		if args.type != 'Mixed':
#			print "Error: argument -t not Archaea, Bacteria, or Mixed"
#			sys.exit(0)

#Test print the args
#print args



print 'Reading fasta file and extracting gene ids'


#extract col 1 and print to a new file
gene_ids = []  #an empty list

output_lines = 0


line = args.gene_file.readline()  #read 
while line:   #if file not empty
	if line.startswith('>'):   #">" in line:
		line = line.lstrip('>') #remove the caret
		columns = line.split()  #splits on all whitespace
		
        	gene_ids.append(columns[0])  #this will be scaffold_X_X
          
	
	line = args.gene_file.readline()  #read next line      

args.gene_file.close()  #close the file

print "number of sequences read from input file = " + str(len(gene_ids))


#go through uclust file and remove all the ids included from the list
#if it is not in the list then print it out to the file with a 0 count

input_lines = 0
#input_sequences = 0

#read first line 
line = args.input_file.readline()

#get the prefix from the first id (we need later)
#Ex: Filtrate_w_

#prefix = ""  #blank
#cols = line.split()
#col1 = cols[0]
#cols = col1.split('_')
#start = 0
#while start < len(cols) - 2:
#	prefix = prefix + str(cols[start]) + "_"
#	start = start + 1

#print "prefix = " + prefix


#if the file is not empty keep reading one at a time
while line:
	input_lines = input_lines + 1
	
	columns = line.split()
	id = columns[0] + "_" + columns[1]  #filtrate_w_scaffold_0
        #scaf = id.split('_')
	#id = scaf[-2] + "_" + str(scaf[-1]) + "_" + str(columns[1])

	gene_ids.remove(id)

	args.output_file.write(line) #write the line back out to the file
        output_lines = output_lines + 1

	#read next line
	line = args.input_file.readline()
	
	#print "reading sequence " + str(input_sequences)


#the sequences that are left in the list were not annotated by uclust
#read the scaffold data into a new list

print "Reading scaffold data file"

#read first line 
line = args.scaffold_file.readline()

scaffold_lines = 0
scaffold_data = [] #an empty list

#if the file is not empty keep reading one at a time
while line:
	scaffold_lines = scaffold_lines + 1
	line = line.rstrip() #remove endline

	if line != "":  #in case a blank line
        	scaffold_data.append(line)
	
	#read next line
	line = args.scaffold_file.readline()
	
	#print "reading scaffold data line " + str(scaffold_lines)

print "Writing unannotated genes to the output file"

#data_found = 0

#go through the list and print to the outputfile
for item in gene_ids:
	s = item.split("_")
	#scaff = s[0] + "_" + str(s[1])
	#gene_num = s[2]
	gene_num = s[-1] #last element
	scaff = s[0]
	i = 1
	while i < len(s) - 1:
		scaff = scaff + "_" + s[i]
		i += 1

	#get the scaffold data
	data_found = 0
	for data in scaffold_data:
		#print "data = " + data
		cols = data.split()
		if scaff == cols[0]:
			data_found = 1
			#print "Data found for gene " + str(data_found)
			#need to print to file
			args.output_file.write(scaff + "\t" + str(gene_num) + "\t" + str(cols[1]) + "\t" + str(cols[2]) + "\t" + str(cols[3]) + "\t" + str(cols[4]) + "\n")
			output_lines = output_lines + 1
			break

	if data_found == 0: #the scaffold data was not found
		args.output_file.write(scaff + "\t" + str(gene_num) + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\n")
                output_lines = output_lines + 1




print "lines read from uclust file = " + str(input_lines)
print "Number of genes with no hits = " + str(len(gene_ids))
print "lines wrote to output file = " + str(output_lines)
print "Number of lines read from scafold data file = " + str(scaffold_lines)



print "Script finished..."
