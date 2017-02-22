#!/usr/bin/perl
#	
#this script edited by Richard Wolfe
#changed path to the 2 databases
#
# Script by - Swapnil _Shevate <swapnil2188@gmail.com>
$numargs = @ARGV;
#print "$numargs\n";print "$ARGV[0]\n";print "$ARGV[1]\n";print "$ARGV[2]\n";print "$ARGV[3]\n";
$file1=$ARGV[0];
#$file2=$ARGV[1];#$file3=$ARGV[2];# print "$file1\n";# $file4=$ARGV[3];
###############################################################
####Step -1 
if($file1 =~ m/keggrbh/)
{
open IN, "$file1" or die "Cannot open file";
#open IN1, "/scripts/bin/Phylogeny_Protpipe/kegg-all-orgs_12102013_HEADERS_1.pep" or die "Cannot open file";
#open IN1, "/opt/bin/bio/KEGG/kegg-all-orgs_12102013_HEADERS_1.pep" or die "Cannot open file";
open IN1, "/ORG-Data/Database/KEGG/kegg-all-orgs_12102013_HEADERS_1.pep" or die "Cannot open file";
@kegg=<IN>;
close(IN);
$len1=$#kegg;
#open OUT, ">OUT1.txt";
my %hash;
while ($line = <IN1>) 
{
	chomp $line;
	my ($key, $value) = split ' ', $line, 2; #Double space present here for kegg- line divided into 2 parts - same as array split
	$hash{$key} = $value;
}
for($i=0; $i<=$len1; $i++)
{
	#print OUT "$key $hash{$key}\n";
	chomp($kegg[$i]);
	@scaff1=split(" ", $kegg[$i]);
	#print OUT "$scaff1[2]\n";
	if (exists $hash{$scaff1[2]}) 		# if the element in the hash exists in the array
	{	
		print "$scaff1[0]\t$scaff1[2]\t$hash{$scaff1[2]}\n";
	} 
}
close(IN1);
#close(OUT);
###############################################################
####Step -2
}elsif($file1 =~ m/unirbh/)
{
open IN2, "$file1" or die "Cannot open file";
#open IN3, "/scripts/bin/Phylogeny_Protpipe/uniref100_HEADERS_1.fasta" or die "Cannot open file";
#open IN3, "/opt/bin/bio/UniRef/uniref100_HEADERS_1.fasta" or die "Cannot open file";
open IN3, "/ORG-Data/Database/UniRef/uniref90_HEADERS.fasta" or die "Cannot open file";
@uni=<IN2>;
close(IN2);
$len2=$#uni;
#open OUT1, ">OUT2.txt";
my %hash1;
while ($line1 = <IN3>) 
{
	chomp $line1;
	my ($key1, $value1) = split ' ', $line1, 2; #Double space present here for kegg- line divided into 2 parts - same as array split
	$hash1{$key1} = $value1;
}
for($j=0; $j<=$len2; $j++)
{
	#print OUT "$key $hash{$key}\n";
	chomp($uni[$j]);
	@scaff2=split(" ", $uni[$j]);
	#print OUT "$scaff1[2]\n";
	if (exists $hash1{$scaff2[2]}) 		# if the element in the hash exists in the array
	{	
		print "$scaff2[0]\t$scaff2[2]\t$hash1{$scaff2[2]}\n";
	} 
}
close(IN3);
#close(OUT1);
###############################################################
}
