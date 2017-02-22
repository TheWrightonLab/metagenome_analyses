#!/usr/bin/python

#PYTHON SCRIPT 
#written by: Richard Wolfe
#
#to run type: python longest_sequence.py -i <inputfile> 
#         or: ./longest_sequence.py -i <inputfile> 
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
#
#   
#   -i <pfam file> 
#   
#   -o <output file name>
#   -p pfam data file  Ex:/opt/PfamScam/Data_files/Pfam-A.hmm.dat (has the annotations for each pfam)
#
#




import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse
import os       #to run system commands




#create an argument parser object
#description will be printed when help is used
parser = argparse.ArgumentParser(description='A script to extract sequences from a fasta file')

#add the available arguments -h and --help are aqdded by default
#if the input file does not exist then program will exit
#if output file does not exit it will be created
# args.input is the input file Note: cant write to this file because read only
# args.output is the output file
# args.m is the minimum seq length
parser.add_argument('-i', '--input_file', type=argparse.FileType('rU'), help='pfam file name',required=True)
parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Output file name',required=True)
parser.add_argument('-p', '--pfam_data_file', type=argparse.FileType('rU'), help='pfam file name',required=True)


#get the args
args = parser.parse_args()




#Test print the args
#print args

input_lines = 0
header_lines = 0
pfam_lines = 0
output_lines = 0
no_desc = 0


#read the pfam file and get the descriptions for each pfam
pfam_ac = []
pfam_de = []

data_lines = 0
pfam_ac_lines = 0
pfam_de_lines = 0

line = args.pfam_data_file.readline()

while line:
	data_lines += 1
	if line.startswith("#=GF AC"):
		pfam_ac_lines += 1
		columns = line.split()
		pfam_ac.append(columns[2]) #add this pfam id to list

		line = args.pfam_data_file.readline()
		data_lines += 1
		if line.startswith("#=GF DE"):
			pfam_de_lines += 1
			
			col = line.split()  #this also removes endl
			desc = col[2]
			#because we split on spaces we need to get rest ot line
			i = 3
			while i < len(col):
				desc = desc + " " + col[i]
				i += 1
			
			pfam_de.append(desc)  #add the description

		else:
			#should not get here
			print "Error... next line was not the description"
			sys.exit(1)
			
	line = args.pfam_data_file.readline()
	



#read first line 
line = args.input_file.readline()


#if the file is not empty keep reading one at a time
while line:

	input_lines += 1
	line = line.rstrip() #remove endline
	if line.startswith('#') or line == "":
		header_lines += 1
	else:
		pfam_lines += 1
		columns = line.split()  #split on tabs
		
		#print columns
		pfam_col = columns[5].split(".")  #the number is PF12099.4 and we want to remove .
                pfam_num = pfam_col[0]
		e_value = columns[12]
	
		#need to get description from pfam database
  		pfam_desc = "Not in data file"
		

		if columns[5] in pfam_ac:
			index = pfam_ac.index(columns[5])
			pfam_desc = pfam_de[index]
		else:
			no_desc += 1

		#write to output file
		args.output.write(columns[0] + "\t" + "1234567890" + "\t" + "99" + "\t" + "Pfam" + "\t" + pfam_num + "\t" + pfam_desc + "\t" + "9" + "\t" + "999" + "\t" + e_value + "\t" + "T" + "\t" + "99-99-9999" + "\t" + "IPR999999" + "\t" + pfam_desc + "\n")
		output_lines += 1
                
   
	line = args.input_file.readline()

#close the file
args.input_file.close()




print "Lines read from pfam data file = ",data_lines
print "pfam acessions numbers found = ", pfam_ac_lines
print "pfam descriptions found = ", pfam_de_lines

print " "
print "Lines read read from pfam file = ", input_lines
print "Header lines in pfam file = ", header_lines
print "Pfam lines in  pfam file = ", pfam_lines
print "Lines wrote to output file = ", output_lines

print "Pfams not found in data file = ", no_desc

print "Script finished..."
