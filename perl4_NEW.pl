#!/usr/bin/perl
#	
#	Script by - Swapnil _Shevate <swapnil2188@gmail.com>
# Modified by Richard Wolfe
#

$numargs = @ARGV;


$file1=$ARGV[0];$file2=$ARGV[1];$file3=$ARGV[2];$file4=$ARGV[3];$file5=$ARGV[4];



open IN1, "$file1" or die "Cannot open file";
open IN2, "$file2" or die "Cannot open file";
open IN3, "$file3" or die "Cannot open file";
open IN4, "$file4" or die "Cannot open file";
open IN5, "$file5" or die "Cannot open file";
 

@unib6=<IN1>;
@keggb6=<IN2>;
@unirbh=<IN3>;
@keggrbh=<IN4>;
@ipr=<IN5>;
close(IN1);close(IN2);close(IN3);close(IN4);close(IN5);
$len1=$#unib6;$len2=$#keggb6;$len3=$#unirbh;$len4=$#keggrbh;$len5=$#ipr;


for ($i = 0; $i <= $len1; $i++)
{
   chomp($unib6[$i]);
   @unib6_1 = split("\t", $unib6[$i]);
   print "$unib6_1[0]\tBLAST:$unib6_1[12](db=UNIREF evalue=$unib6_1[10] bit_score=$unib6_1[11] identity=$unib6_1[2])\n";
}

for ($i = 0; $i <= $len2; $i++)
{
   chomp($keggb6[$i]);
   @keggb6_1 = split("\t", $keggb6[$i]);
   print "$keggb6_1[0]\tBLAST:$keggb6_1[12](db=KEGG evalue=$keggb6_1[10] bit_score=$keggb6_1[11] identity=$keggb6_1[2])\n";
}

for ($i = 0; $i <= $len3; $i++)
{
   chomp($unirbh[$i]);
   @unirbh1 = split("\t", $unirbh[$i]);
   print "$unirbh1[0]\tRBH:$unirbh1[2](db=UNIREF)\n";
}

for ($i = 0; $i <= $len4; $i++)
{
   chomp($keggrbh[$i]);
   @keggrbh1 = split("\t", $keggrbh[$i]);
   print "$keggrbh1[0]\tRBH:$keggrbh1[2](db=KEGG)\n";
}

for ($i = 0; $i <= $len5; $i++)
{
   chomp($ipr[$i]); #remove endline
   $ipr[$i] =~ s/^\s+|\s+$//g;  #remove leading and trailng whitespace
   if ($ipr[$i] ne ""){ #if not a blank line
       @ipr1 = split("\t", $ipr[$i]);
       print "$ipr1[0]\tIPRSCAN:$ipr1[12](db=$ipr1[3] db_id=$ipr1[4] evalue=$ipr1[8] interpro_id=$ipr1[11] interpro_description=$ipr1[5])\n";
   }
}

