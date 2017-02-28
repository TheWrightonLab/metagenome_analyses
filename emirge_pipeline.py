#!/usr/bin/python

#PYTHON SCRIPT 
#written by: Richard Wolfe
#
#to run type: python emirge_pipeline.py -f <forwardreads> -r <reversereads> -i <jobid>
#         -e <emailaddress>
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
#   -f --forward_reads   <string>      (required)    
#   -r --reverse_reads  <string>      (required)         
#   -i --job_id
#   -e --email_address
#
#   Example command to run :
#

import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse
import os       #to run system commands
#import resource #to keep track of memory usage

def longest_reads(f):
	longest = 0

	line1 = f.readline()
	while line1:
		line2 = f.readline()
		line3 = f.readline()
		line4 = f.readline()

		line2 = line2.rstrip() #remove endline

		if len(line2) > longest:
			longest = len(line2)

		line1 = f.readline()


    	return longest;



print "Script started ..."


#create an argument parser object
#description will be printed when help is used
parser = argparse.ArgumentParser(description='A script to run emirge')

#add the available arguments -h and --help are added by default
#if the input file does not exist then program will exit
#if output file does not exit it will be created
# args.input is the input file Note: cant write to this file because read only
# args.output is the output file
# args.m is the minimum seq length
parser.add_argument('-f', '--forward_reads', type=argparse.FileType('rU'), help='forward reads file',required=True)
parser.add_argument('-r', '--reverse_reads', type=argparse.FileType('rU'), help='reverse reads', required=True)
parser.add_argument('-i', '--job_id', help='job id', required=True)
parser.add_argument('-e', '--email_address', help='email address', required=True)
parser.add_argument('-l', '--idba_log_file', type=argparse.FileType('rU'), help='idba_ud log file', required=True)
parser.add_argument('-p', '--processors', help='processors', required=True)

#get the args
args = parser.parse_args()

#additional argument tests

#get full paths
#forward_file_name = os.path.basename(args.forward_reads.name)
#reverse_file_name = os.path.basename(args.reverse_reads.name)


#close the files so there are no problems
#args.forward_reads.close()
#args.reverse_reads.close()

#make a working directory in the folder you are in
if not os.path.exists("emirge"):
	os.makedirs("emirge")
else:
	print "Error ... Directory already exists"
	sys.exit(1)




#gothrough the fastq reads files and calculate the longest reads
reads_length = []
reads_length.append(longest_reads(args.forward_reads))
args.forward_reads.close
reads_length.append(longest_reads(args.reverse_reads))
args.reverse_reads.close

max_length = max(reads_length)

print "longest forward read = ",reads_length[0]
print "longest reverse read = ",reads_length[1]
print "max length = ",max_length

#get distance mead and sd from idba_ud log file
#We want the last line that starts with "distance mean"
dist_mean = ""
sd = ""

line = args.idba_log_file.readline()
while line:
	if line.startswith("distance mean "):
		cols = line.split()
		dist_mean = cols[2]
		sd = cols[4]
		dist_mean = dist_mean.split(".")[0] #remove decimal point
		sd = sd.split(".")[0] #remove decimal point
	
	line = args.idba_log_file.readline()

if dist_mean == "" or sd == "":
	print "Error .. could not get distance mean or sd from log file"
	sys.exit(1)

print "Distance mean = " + dist_mean
print "sd = " + sd

#run emirge
cmd = "emirge.py emirge/DIR -1 " + args.forward_reads.name + " -2 " + args.reverse_reads.name + " -f /opt/EMIRGE-master/SSURef_111_candidate_db.fasta -b /opt/EMIRGE-master/SSU_candidate_db_btindex  -l " + str(max_length) + " -i " + dist_mean + " -s " + sd + " -n 50 -a " + args.processors + " --phred33"
print cmd
retvalue = os.system(cmd) #returns 0 if no error in command

if retvalue != 0:  #if command failed
	print "ERROR emirge.py command did not return 0 and failed"
	sys.exit(1)  #return 0 if sucess

#remove iter.00 to iter.49
cmd = "rm -r emirge/DIR/iter.0*"
retvalue = os.system(cmd) #returns 0 if no error in command

cmd = "rm -r emirge/DIR/iter.1*"
retvalue = os.system(cmd) #returns 0 if no error in command

cmd = "rm -r emirge/DIR/iter.2*"
retvalue = os.system(cmd) #returns 0 if no error in command

cmd = "rm -r emirge/DIR/iter.3*"
retvalue = os.system(cmd) #returns 0 if no error in command

cmd = "rm -r emirge/DIR/iter.4*"
retvalue = os.system(cmd) #returns 0 if no error in command

#rename the last emirge file
cmd = "emirge_rename_fasta.py emirge/DIR/iter.50 > emirge/DIR/" + args.job_id + ".fasta" 

retvalue = os.system(cmd) #returns 0 if no error in command

if retvalue != 0:  #if command failed
	print "ERROR emirge_rename_fasta.py command did not return 0 and failed"
	sys.exit(1)  #return 0 if sucess





#send email when done
cmd = 'echo "EMIRGE.sh job on ' + args.job_id + ' data has finished" | mail -s "Emirge Job Finished" ' + args.email_address
retvalue = os.system(cmd) #returns 0 if no error in command




#/ORG-Data/scripts/bin/Phylogeny_Protpipe/EMIRGE.sh  R1_All_trimmed.fastq R2_All_trimmed.fastq Filtrate_w wolfe.759@OSU.edu

#cmd = '/ORG-Data/scripts/bin/Phylogeny_Protpipe/EMIRGE.sh ' + forward_file_name + ' ' + reverse_file_name + ' ' + args.job_id + ' ' + args.email_address

#print 'executing cmd = ', cmd

#retvalue = os.system(cmd) #returns 0 if no error in command

#if retvalue != 0:  #if command failed
	#print "ERROR command did not return 0 and failed"
	#sys.exit(1)  #return 0 if sucess




#print "Maximum amount of memory used (in MB) = " , resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000





print "Script finished..."
