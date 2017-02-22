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
#   -n number of processors (required)
#   
#   -f protein fasta file (required)
#   -o output file name (required)
#   -i make iperscan file name (optional)
#      converts the output file into iperscan format




import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse
import os       #to run system commands

#import toolbox #import my toolbox with defs

import subprocess
import time
import datetime #to make timestamp


def run_process(str, fail_str=""):
	#returns the output
	#Example usage
	#  cmd = "bash /ORG-Data/scripts/run_pfamscan_all_files.sh " + tmp_dir
	#  output = toolbox.run_process(cmd)
	#  print output
	#The above commands will run the script and print any output to the screen
	#
	# if command fails and returns non-zero and there is a string 
	#    the string will be returned
	# fail_str is optional

	p = subprocess.Popen(str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

	#read data from stdout and stderr and store info in tuple
	(output, err) = p.communicate()

	#Wait for command to terminate and get return code
	p_status = p.wait()

	if p_status != 0: #if cmd failed
		if fail_str == "":
			print str
			print err
			print "ERROR command did not return 0 and failed"
			sys.exit(1)  #return 0 if sucess
		else:
			return fail_str

	return output


def read_fasta(line,f):
	#line = the first line of the fasta file it will be the header
	#f = an open file
	#
	#Note : head and sequence still have endlines
	#
	# Example usage:
	#
	#line = args.input_file.readline()
	#
	#while line:	
	#	header,sequence,line,s_lines = toolbox.read_fasta(line,args.input_file)
	#
	#	#the seq is found go through the ids and see ifthe header starts with an id
	#	#Note the header and sequence still have endlines	
	#
	#	input_seqs += 1
	#	input_lines += (1 + s_lines) #the header line and the seq lines
	#

	seqs_lines = 0

	head = line
	sequence = ""

	line = f.readline() #read next line until the next header or EOF

	while line:
		
		if line.startswith('>'):   #">" in line:
			break   #break out of this while loop
				
		else: #this is the seq
			#line = line.rstrip()  #remove whitespace at end includung endl
			sequence = sequence + line 
			#read another line
			line = f.readline()
			seqs_lines += 1


	return head,sequence,line,seqs_lines


def get_timestamp():
	#make a timestamp and return it
	i = datetime.datetime.now()
	timestamp = i.strftime('%m_%d_%Y_%H%M%S')
	#print timestamp

	return timestamp




print "Script started ..."


#create an argument parser object
#description will be printed when help is used
parser = argparse.ArgumentParser(description='A script to run PfamScan on multiple processors')

#add the available arguments -h and --help are aqdded by default
#if the input file does not exist then program will exit
#if output file does not exit it will be created
# args.input is the input file Note: cant write to this file because read only
# args.output is the output file
# args.m is the minimum seq length
parser.add_argument('-f', '--input_file', type=argparse.FileType('rU'), help='protein fasta file',required=True)
parser.add_argument('-n', '--processors', type=int, help='number of processors',required=True)
#parser.add_argument('-p', '--pfam_data_file', type=argparse.FileType('rU'), help='pfam file name',required=True)
parser.add_argument('-o', '--output_file', type=argparse.FileType('w'), help='output file',required=True)
parser.add_argument('-i', '--make_iper', type=argparse.FileType('w'), help='make iperscan file file_name')
parser.add_argument('--OSC', help='T or F if running on OSC', default="F")



#get the args
args = parser.parse_args()

if args.processors < 1 or args.processors > 80:
	print "Error ... processors needs to be from 1 to 80"
	sys.exit(1)

if args.OSC != "T":
	if args.OSC != "F":
		print "Error ... --OSC must be T or F"
		sys.exit(1)

args.output_file.close() #we only want the name
output_file = args.output_file.name

#Test print the args
#print args

input_lines = 0
input_sequences = 0

tmp_files = []


#make a temp directory
#timestamp = toolbox.get_timestamp()
timestamp = get_timestamp()
tmp_dir = timestamp + "_pscan_temp"

if not os.path.exists(tmp_dir):
	print "making temp directory " + tmp_dir
	os.makedirs(tmp_dir)
else:
	print "Error ... Directory already exists"
	sys.exit(1)





#make a list of open files

i = 0
while i < args.processors:
	filename = tmp_dir + "/file_" + str(i)
	f = open(filename, "w")
	tmp_files.append(f)

	i += 1




line = args.input_file.readline()

file_ptr = 0

while line:
	
	
	#header,sequence,line,s_lines = toolbox.read_fasta(line,args.input_file)
	header,sequence,line,s_lines = read_fasta(line,args.input_file)

	#the seq is found go through the ids and see ifthe header starts with an id
	#Note the header and sequence still have endlines	

	input_sequences += 1
	input_lines += (1 + s_lines) #the header line and the seq lines

	#write the seq to the file
	tmp_files[file_ptr].write(header)
	tmp_files[file_ptr].write(sequence)

	file_ptr += 1
	if file_ptr >= len(tmp_files):
		file_ptr = 0


#close all the files
for item in tmp_files:
	item.close()


#set paths
pfam_scan = "/opt/PfamScan/pfam_scan.pl"
pfam_dir = "/opt/PfamScan/Data_files"
convert_pfam = "/ORG-Data/scripts/bin/convert_pfam_to_iperscan.py"
pfam_hmm = "/opt/PfamScan/Data_files/Pfam-A.hmm.dat"

if args.OSC == "T":
	#Note the -I<path to libraries>
	pfam_scan = "perl -I/users/PAS1018/osu9681/bin/PfamScan /users/PAS1018/osu9681/bin/PfamScan/pfam_scan.pl"
	pfam_dir = "/users/PAS1018/osu9681/bin/PfamScan/Data_files"
	convert_pfam = "/users/PAS1018/osu9681/bin/convert_pfam_to_iperscan.py"
	pfam_hmm = "/users/PAS1018/osu9681/bin/PfamScan/Data_files/Pfam-A.hmm.dat"

#run all the files on the n processors using a bash script
#cmd = "bash /ORG-Data/scripts/run_pfamscan_all_files.sh " + tmp_dir
#output = toolbox.run_process(cmd)
#print output

#start the n processes on the files and wait

sub_process_list = [] #make a list of subprocesses

for item in tmp_files:
	
	cmd = pfam_scan + " -fasta " + item.name + " -dir " + pfam_dir + " -cpu 1  -outfile " +  item.name + "_pfam_output.txt"

	p = subprocess.Popen(cmd, shell=True)
	sub_process_list.append(p)

#see if all the processes are done
for p in sub_process_list:
	while p.poll() is None:
		time.sleep(1) #sleep for 1 second then check again

#the PfamScan output files will be in the temp folder
# file_0_pfam_output.txt .... file_79_pfam_output.txt
# we need to combine them into 1 file
# They will have aprox 29 header lines with a # and then the results

cmd = "cat " + tmp_dir + "/file_*_pfam_output.txt > " + output_file
#output = toolbox.run_process(cmd)
output = run_process(cmd)

#remove tmp dir and the temp files

if os.path.exists(tmp_dir):
	print "removing temp directory " + tmp_dir
	cmd = "rm -rf " + tmp_dir
	#toolbox.run_process(cmd)
	run_process(cmd)

if args.make_iper: #if make iperscan file option
	cmd = "python " + convert_pfam + " -i " + output_file + " -o " + args.make_iper.name + " -p " + pfam_hmm
	#toolbox.run_process(cmd)
	run_process(cmd)

print "Print lines read from input file = ",input_lines
print "Print sequences in input file = ",input_sequences
print ""
print "Number of temp files made = ",len(tmp_files)

print "Script finished..."
