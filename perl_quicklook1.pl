#!/usr/bin/perl
#	
#	Script by - Swapnil _Shevate <sshevate@iupui.edu>
#	Edited by Richard Wolfe

$numargs = @ARGV;
$file1=$ARGV[0]; #ublast file
$file2=$ARGV[1]; #contig coverage score file


open IN, "$file1" or die "Cannot open file";
open IN1, "$file2" or die "Cannot open $!";


@uniref=<IN>; #read the ublast file into array
close(IN);
$len1=$#uniref; #this is last index and not length of array
$undrscr="_";

#read the contig coverage file into a hash
my %hash;
while ($line = <IN1>) 
{
	chomp $line; # remove newline
	my ($key, $value) = split '\t', $line, 2;
	$hash{$key} = $value;
}

#go through the ublast file
for ($j=0; $j<=$len1; $j++) 
{
		chomp($uniref[$j]);
		#@uni_out=split("\t", $uniref[$j]);
		@uni_out = split(' ',$uniref[$j]); #split on any space including tab and endline
		@uni_out1=split("_", $uni_out[0]);
		
		#I changed because this reads scaffold_0_12 only
		#we want xxx_xxx_xxx_0_12
		#$contig_id= join "", $uni_out1[0], $undrscr, $uni_out1[1];
		
		$len_id = $#uni_out1; #the last index of the array
		$contig_id = $uni_out1[0];
		
		for ($i = 1; $i < $len_id; $i++){ #dont add last element
			$contig_id  = $contig_id.$undrscr.$uni_out1[$i];
		
		}
		
		
		@uni_out4=split('\*', $uni_out[9], 2);
		@uni_out5=split("n=", $uni_out4[1]);
		@uni_out2=split("Tax=", $uni_out[9]);
		@uni_out3=split("RepID=", $uni_out2[1]);
		$tax= $uni_out3[0];
		$tax =~ s/\*/\_/g;

		#print "$ARGV[2]"; #jobid
                print "$contig_id\t$uni_out1[$len_id]\t"; #last element
		if (exists $hash{$contig_id}) 		# if the element in the hash exists in the array
		{	
			print "$hash{$contig_id}";
			
		} 	
		else{ #Iadded incase the the contig_id not in the hash
 			print "NA\tNA\tNA\tNA";
                        
		}#end else
		print "\t$uni_out4[0]\t$uni_out5[0]\t$tax\t$uni_out[10]\t$uni_out[18]\t$uni_out[19]\n";
	} #end  for
