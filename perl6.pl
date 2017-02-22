#!/usr/bin/perl
#	
#	Script by - Swapnil _Shevate <swapnil2188@gmail.com>
use List::MoreUtils qw( minmax );
$numargs = @ARGV;
$file1=$ARGV[0];
open IN, "$file1" or die "Cannot open file";
@anno=<IN>;
close(IN);
$len=$#anno;
#open OUT1, ">ANNOTATION_FINAL_OUT_06272012_PH_1_scaffold_11.genes3_FINAL_RANKED.txt";

for($i=0; $i<=$len; $i++)
{
	chomp($anno[$i]);
	@anno4=split("\t", $anno[$i]);
	#print OUT1 "$#anno4\n";
	push(@array, $#anno4);
}	
my ($min, $max) = minmax @array;
#print "$max\n";
for($i=0; $i<=$len; $i++)
{
	chomp($anno[$i]);
	@anno4=split("\t", $anno[$i],7);

	print "$anno4[0]\t";
	#print OUT1 "$anno4[1]\n";
	#print OUT1 "\A\t$anno4[1]\t$anno4[2]\n";
	#for($j=1; $j<=7; $j++)
	#{		
		#if(($anno4[1] =~ /^RBH.+db=KEGG\)$/) && ($anno4[2] =~ /^RBH.+db=UNIREF\)$/))
 		if($anno4[1] =~ /^RBH.+db=KEGG\)$/)
		{	
			print "A\t$anno4[1]\t$anno4[2]\t$anno4[3]\t$anno4[4]\t$anno4[5]\t$anno4[6]\t$anno4[7]\n";
			#last;
		#}elsif(($anno4[1] =~ /^RBH.+db=KEGG\)$/) && ($anno4[2] =~ /^BLAST.+db=KEGG.+\)$/))
		}elsif($anno4[1] =~ /^RBH.+db=UNIREF\)$/)
		{		
			print "B\t$anno4[1]\t$anno4[2]\t$anno4[3]\t$anno4[4]\t$anno4[5]\t$anno4[6]\t$anno4[7]\n";
			#last;
		#}elsif(($anno4[1] =~ /^RBH.+db=UNIREF\)$/) && ($anno4[2] =~ /^BLAST.+db=UNIREF.+\)$/))
		#{		
		#	print "B\t$anno4[1]\t$anno4[2]\t$anno4[3]\t$anno4[4]\t$anno4[5]\t$anno4[6]\t$anno4[7]\n";
			#last;
		#}elsif(($anno4[1] =~ /^RBH.+db=UNIREF\)$/) && ($anno4[2] =~ /^BLAST.+db=KEGG.+\)$/))
		#{		
		#	print "B\t$anno4[1]\t$anno4[2]\t$anno4[3]\t$anno4[4]\t$anno4[5]\t$anno4[6]\t$anno4[7]\n";
			#last;
		}elsif($anno4[1] =~ /^BLAST.+db=KEGG.+\)$/)
		{
			print "C\t$anno4[1]\t$anno4[2]\t$anno4[3]\t$anno4[4]\t$anno4[5]\t$anno4[6]\t$anno4[7]\n";
			#last;
		}elsif($anno4[1] =~ /^BLAST.+db=UNIREF.+\)$/)
		{
			print "D\t$anno4[1]\t$anno4[2]\t$anno4[3]\t$anno4[4]\t$anno4[5]\t$anno4[6]\t$anno4[7]\n";
			#last;
		}elsif($anno4[1] =~ /^IPRSCAN.+\)$/)
		{
			print "E\t$anno4[1]\t$anno4[2]\t$anno4[3]\t$anno4[4]\t$anno4[5]\t$anno4[6]\t$anno4[7]\n";
			#last;
		}else{  #Should never get here There is no ranking for this sequence  I added this code
			print "ERROR\t$anno4[1]\t$anno4[2]\t$anno4[3]\t$anno4[4]\t$anno4[5]\t$anno4[6]\t$anno4[7]\n";
		}
	#}
}
#close (OUT1);
