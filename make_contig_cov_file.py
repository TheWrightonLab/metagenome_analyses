#!/usr/bin/python

#PYTHON SCRIPT 
#written by: Richard Wolfe
#
#to run type: python convert_velvet_to_ida_output.py -i <inputfile> -o <outputfile> 
#         or: ./convert_velvet_to_ida_output.py -i <inputfile> -o <outputfile> 
#
#   if error: /usr/bin/python^M: bad interpreter: No such file or directory
#      -there is a windows endl after shebang
#      -open in vi 
#         once in vi type:
#           :set ff=unix<return>
#           :x<return>
#
#    -s  scaffold file
#    -o  output file
#    -b  bowtie sam file   (Optional if not supplied then reads and cov will be 0)
#
#
#
#
#   make a contig coverage file
#                       reads    length  gc       cov
#       scaffold_0      295348  478516  60.72   61.7217
#       scaffold_1      255602  369697  60.48   69.1382
#       scaffold_8      182939  338702  61.2    54.0118
#       scaffold_4      205429  300854  61.33   68.282
#       scaffold_2      156721  291172  60.16   53.8242
#       scaffold_5      182272  280216  60.76   65.047
#   

import sys      #for exit command and maxint
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse

def make_cov_table():

	ids = []
	genome_len = []
	filtrate = []
	F02 = []
	F08 = []
	pellet = []

	import glob     #for * in file name
	dir_files = glob.glob('contig_cov_*')   #put all files in this directory in a list

	

	if len(dir_files) == 0:
		print ("Error ... No contig_cov_ files in this directory")
		sys.exit(1)

	for item in dir_files:
		print item

		#extract id and sample from file name
		#id =  item.replace("contig_cov_","")
		id = item.replace(".txt", "")
		id = id.replace("contig_cov_Pellet_", "")
		id = id.replace("contig_cov_F02_", "")
		id = id.replace("contig_cov_F08_", "")
		id = id.replace("contig_cov_filtrate_", "")
		print id

		if id not in ids:
			ids.append(id)
			filtrate.append(0.0)
			F02.append(0.0)
			F08.append(0.0)
			pellet.append(0.0)
			genome_len.append(0)

		f = open(item, "rU")
		line = f.readline()

		#reads = 0
		bp_mapped = 0
		bp_scaffolds = 0

		while line:
			avg_read_len = 0.0

			if float(line.split()[1]) != 0:
				avg_read_len = (float(line.split()[4]) * float(line.split()[2])) / float(line.split()[1])		
			

			bp_mapped = bp_mapped + int(avg_read_len * float(line.split()[1]))

			bp_scaffolds = bp_scaffolds + int(line.split()[2])

			line = f.readline()

		print "bp_mapped = ",bp_mapped
		print "bp_scaffolds = ",bp_scaffolds

		#percent_mapped = 0.0
		avg_cov = float(bp_mapped) / float(bp_scaffolds)

		print "avg_cov = ", avg_cov

		
		
		index = ids.index(id)

		genome_len[index] = bp_scaffolds

		if item.startswith("contig_cov_Pellet_"):
			#sample = "Pellet"
			#percent_mapped = reads / pellet_reads
			pellet[index] = avg_cov
		elif item.startswith("contig_cov_F02_"):
			#sample = "F02"
			#percent_mapped = reads / F02_reads 
			F02[index] = avg_cov
		elif item.startswith("contig_cov_F08_"):
			#sample = "F08"
			#percent_mapped = reads / F08_reads 
			F08[index] = avg_cov
		elif item.startswith("contig_cov_filtrate_"):
			#sample = "Filtrate"
			#percent_mapped = reads / filtrate_reads
			filtrate[index] = avg_cov
		else:
			print "Error... No sample name"
			sys.exit(1)

		

		#read the file and get number of reads that mapped
		#sys.exit()
		

	#print the table

	out_file = open(args.make_cov_table,"w")

	out_file.write("File\tGenome_length\tFiltrate\tF02\tF08\tPellet\n")

	i = 0
	while i < len(ids):
		out_file.write(ids[i] + "\t" + str(genome_len[i]) + "\t" + str(filtrate[i]) + "\t" + str(F02[i]) + "\t" + str(F08[i]) + "\t" + str(pellet[i]) + "\n")

		i += 1



	print ""
	print "Number of contig_cov_ files in directory = ",len(dir_files)

	print ""
	print "Script finished..."
	sys.exit(0)


def make_table():

	#go through all contig_cov files in the dir and make a table
	#
	# ex filename: contig_cov_F08_BACT33.fa.txt
	#
	# 		Filtrate   F02     F08    Pellet
	#   Bact33.fa     value   value  ...
	#   ...
	#    value = reads mapped/filtrate reads

	filtrate_reads = 89488910.0
	F02_reads = 295029380.0
	F08_reads = 73814516.0
	pellet_reads = 82116428.0

	ids = []
	filtrate = []
	F02 = []
	F08 = []
	pellet = []

	import glob     #for * in file name
	dir_files = glob.glob('contig_cov_*')   #put all files in this directory in a list

	

	if len(dir_files) == 0:
		print ("Error ... No contig_cov_ files in this directory")
		sys.exit(1)

	for item in dir_files:
		print item

		#extract id and sample from file name
		#id =  item.replace("contig_cov_","")
		id = item.replace(".txt", "")
		id = id.replace("contig_cov_Pellet_", "")
		id = id.replace("contig_cov_F02_", "")
		id = id.replace("contig_cov_F08_", "")
		id = id.replace("contig_cov_filtrate_", "")
		print id

		sample = ""
		

		if id not in ids:
			ids.append(id)
			filtrate.append(0.0)
			F02.append(0.0)
			F08.append(0.0)
			pellet.append(0.0)

		f = open(item, "rU")
		line = f.readline()

		reads = 0
		while line:
			
			reads = reads + int(line.split()[1])

			line = f.readline()

		print "reads = ",reads

		percent_mapped = 0.0

		index = ids.index(id)

		if item.startswith("contig_cov_Pellet_"):
			#sample = "Pellet"
			#percent_mapped = reads / pellet_reads
			pellet[index] = reads / pellet_reads
		elif item.startswith("contig_cov_F02_"):
			#sample = "F02"
			#percent_mapped = reads / F02_reads 
			F02[index] = reads / F02_reads
		elif item.startswith("contig_cov_F08_"):
			#sample = "F08"
			#percent_mapped = reads / F08_reads 
			F08[index] = reads / F08_reads
		elif item.startswith("contig_cov_filtrate_"):
			#sample = "Filtrate"
			#percent_mapped = reads / filtrate_reads
			filtrate[index] = reads / filtrate_reads
		else:
			print "Error... No sample name"
			sys.exit(1)

		#print sample 
		print "percent = ",percent_mapped

		#read the file and get number of reads that mapped
		#sys.exit()


	#print the table

	out_file = open(args.make_table,"w")

	out_file.write("File\tFiltrate\tF02\tF08\tPellet\n")

	i = 0
	while i < len(ids):
		out_file.write(ids[i] + "\t" + str(filtrate[i]) + "\t" + str(F02[i]) + "\t" + str(F08[i]) + "\t" + str(pellet[i]) + "\n")

		i += 1

	print ""
	print "Number of contig_cov_ files in directory = ",len(dir_files)

	print ""
	print "Script finished..."
	sys.exit(0)


#create an argument parser object
#description will be printed when help is used
parser = argparse.ArgumentParser(description='A script to ')

#add the available arguments -h and --help are aqdded by default
#if the input file does not exist then program will exit
#if output file does not exit it will be created
# args.input is the input file Note: cant write to this file because read only
# args.output is the output file
# args.m is the minimum seq length
parser.add_argument('-s', '--scaffold_file', type=argparse.FileType('rU'), help='scaffold file name') #,required=True)
parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Output file name') #, required=True)
parser.add_argument('-b', '--sam_file', type=argparse.FileType('rU'), help='bowtie sam file name')
parser.add_argument('--make_table', help='file name to make of a table from all contig_cov files in current directory')
parser.add_argument('--make_cov_table', help='file name to make of a table from all contig_cov files in current directory')


#get the args
args = parser.parse_args()

if args.make_cov_table:
	make_cov_table()

if args.scaffold_file == None or args.output == None or args.sam_file == None: #if 1 of these args not supplied
	if args.make_table == None:
		print "You must supply -s and -o and -b or just --make_table"
		sys.exit(1)

if args.make_table:
	if args.scaffold_file or args.output or args.sam_file:
		print "Error .. you can only use --make_table with no other arguments"
		sys.exit(1)
	else:
		make_table()


#Test print the args
#print args

#arg test
#if args.sam_file != "NONE":
#	if not os.path.isfile(args.sam_file):
#		print ("-b is not a file or NONE")
#		sys.exit(0)

input_lines = 0
input_sequences = 0
output_lines = 0
output_sequences = 0

sam_lines = 0
sam_header_lines = 0
sam_data_lines = 0

reads_not_mapped = 0
reads_mapped = 0

scaffold = 0

ids = []    #a list of tupples
reads = []
reads_bp_count = []
#lengths = []
#gc_content = []
#coverage = []

#read first line should be header line starts with ">"
line = args.scaffold_file.readline()

print "Reading scaffold file"

#if the file is not empty keep reading one at a time
while line:
	sequence = ""
	header = ""	

	input_lines += 1
	line = line.rstrip()  #remove whitespace at end includung endl
	header = line
	input_sequences += 1

	#read sequence
	line = args.scaffold_file.readline()
	
	line = line.rstrip()  #remove whitespace at end includung endl
	

	while line:
		
		#if line starts with > it is the header line for next sequence
		if line.startswith('>'):   #">" in line:
			break   #break out of this while loop
				
		else: #this is the seq
			input_lines += 1
			line = line.rstrip()  #remove whitespace at end includung endl
			sequence = sequence + line 

			#read another line
			line = args.scaffold_file.readline()
			

	#the seq is found 
	#get id from header
	header = header.replace(">","") #replace the >
	header = header.split()[0] #get first word
	
	
	reads.append(0)
	reads_bp_count.append(0)

	#calculate gc content
	cg = 0.0
	for char in sequence:
		if char == "C" or char == "c" or char == "G" or char == "g":
			cg += 1.0
		
	cg = cg / len(sequence) * 100.0  #will be %
	cg = '%.3f'%(cg)  #only 3 places after decimal and rounds
		

	tup = (header,cg,len(sequence))
	ids.append(tup)

		
#close the file
args.scaffold_file.close()

print "Sorting scaffold file ... number of scaffolds = ",len(ids)

#sort the tuples on id Ex:scaffold_1 ....
#new_list = sorted(ids, key=lambda item: item[0])  #sort on first item in tuple - returns a new list
ids.sort(key=lambda item: item[0])  #sort on first item in tuple - sort in place

#test print the tuples
#i = 0
#for item in ids:
#	if i < 200:
#		print item
#	i += 1

#sys.exit()
	

mapped_sam = [] #list of tuples

#if sam file then go through and get reads and coverage
if args.sam_file:
	print "Starting to read SAM file"

	line = args.sam_file.readline()


	while line:
		line = line.rstrip() #remove endline
		sam_lines += 1

		#print progress
		if sam_lines % 1000000 == 0:
			print "Reading SAM file line ",sam_lines
			#break #test on 1st million lines


		if line.startswith("@"): #this is a header line
			sam_header_lines += 1
			line = args.sam_file.readline()
			continue

		#process the data line
		sam_data_lines += 1
		
		cols = line.split()
		id = cols[2]

		if int(cols[1]) & 4: #flag bit 4 is on
			reads_not_mapped += 1
		
		else:
			reads_mapped += 1

			#read_length = len(cols[9])

			#index = ids.index(id)
			#index = ids_dict[id]

			#reads[index] += 1
			#reads_bp_count[index] = reads_bp_count[index] + read_length

			tup = (id, len(cols[9]))
			mapped_sam.append(tup)

		line = args.sam_file.readline()


print "Sorting sam file ... number of reads that mapped = ",len(mapped_sam)

#sort the tuples on id Ex:scaffold_1 ....
#new_mapped = sorted(mapped_sam, key=lambda item: item[0])  #sort on first item in tuple - returns new list
mapped_sam.sort(key=lambda item: item[0])  #sort on first item in tuple - sort in place

#test print 1st 200 tuples
#i = 0
#for item in mapped_sam:
#	print item
#	if i > 200:
#		break
#	i += 1
	
#because both are sorted we can go through each list 1 time
print "Getting number of reads and number of basepairs that mapped"
ids_index = 0
for item in mapped_sam:
	#if item[0] != "scaffold_0":
	#	break

	while item[0] != ids[ids_index][0]:  #update the index 
		ids_index += 1
	
	read_len = item[1]
	reads_bp_count[ids_index] = reads_bp_count[ids_index] + read_len

	reads[ids_index] += 1




#############################################################
#print results to output file
#   make a contig coverage file
#                       reads    length  gc       cov
#       scaffold_0      186656  77408   46.47   241.133
#       scaffold_1      141225  63744   50      221.55
#       scaffold_2      120809  54525   55.11   221.566
#       scaffold_13     109246  48685   48.23   224.394
#       scaffold_3      91634   46485   49.93   197.126
#       scaffold_4      94311   44893   48.15   210.08
#       scaffold_59     102236  42712   48.54   239.361

print "Printing results to output file"

i = 0
while i < len(ids):
	args.output.write(ids[i][0] + "\t" + str(reads[i]) + "\t" + str(ids[i][2]) + "\t" + str(ids[i][1]) + "\t")
	cov = reads_bp_count[i] * 1.0 / ids[i][2] # * 1.0 to make a double
	args.output.write(str(cov) + "\n")
	output_sequences += 1
	i += 1



args.output.close()

print ""
print "Lines read from scaffold file = ", input_lines
print "Sequences in scaffold file = ", input_sequences
print "Sequences written to output file = ", output_sequences

print ""
print "Lines in sam file = ",sam_lines
print "Header lines in sam file = ", sam_header_lines
print "Data lines = read lines in sam file = ", sam_data_lines

print ""
print "Reads that did not map = ",reads_not_mapped 
print "Reads that mapped = ", reads_mapped



print ""
print "Script finished..."
