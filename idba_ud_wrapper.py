#!/usr/bin/python

#PYTHON SCRIPT 
#written by: Richard Wolfe
#
#to run type: python idba_ud_wrapper.py -r <joined reads> -o <outputfile> 
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
#   -r --merged_reads   <string>      (required)    
#   -o --output_dir  <string>      (required)        

#
#   Example command to run :
#

import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse
import os       #to run system commands
import resource #to keep track of memory usage




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
#parser.add_argument('-f', '--forward_reads', type=argparse.FileType('rU'), help='forward reads file',required=True)
parser.add_argument('-r', '--merged_reads', help='name of merged forward and reverse reads file', required=True)
parser.add_argument('-o', '--output_dir', help='name of output directory', required=True)

#get the args
args = parser.parse_args()

#additional argument tests

#get full paths
#forward_file_name = os.path.basename(args.forward_reads.name)
#reverse_file_name = os.path.basename(args.reverse_reads.name)


#close the files so there are no problems
#args.forward_reads.close()
#args.reverse_reads.close()


# idba_ud -r R1R2_All_trimmed.fa -o idba_assembled_output

cmd = 'idba_ud -r ' + args.merged_reads + ' -o ' + args.output_dir

print 'executing cmd = ', cmd

retvalue = os.system(cmd) #returns 0 if no error in command

if retvalue != 0:  #if command failed
	print "ERROR command did not return 0 and failed"
	sys.exit(1)  #return 0 if sucess




#print "Maximum amount of memory used (in MB) = " , resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
print "Maximum amount of memory used (in MB) = " , resource.getrusage(resource.RUSAGE_BOTH).ru_maxrss / 1000






print "Script finished..."
