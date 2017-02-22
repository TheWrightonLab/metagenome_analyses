#!/usr/bin/perl
#####################################################################################################
# This program provides information about scaffolds and contigs in the input file.
# Written by: Itai Sharon, itai.sharon@gmail.com
# Dates: 05/May/2010: version 1.00
#	 08/Sep/2010: changed command line, added max and min length, add out-prefix, added option
# 		      for fasta output of relevant sequences, fixed a bug in output of last sequence
#	 09/Sep/2013: Fixed a small bug that affected summary of sequence lengths at the beginning
#		      of the summary report.
#
# Written by Itai Sharon, itai.sharon@gmail.com
#####################################################################################################
use strict;

my $num_sequencess = 0;
my %sequence_info = ();
my $total_bps = 0;
my $total_sequences = 0;
my %length_dist = ();

#####################################################################################################
sub store_info {
	my ($sname, $sseq, $desc) = @_;
	return if(!defined($sname));

	my $slength = length($sseq);
	my $gc = ($sseq =~ tr/GC/GC/);
	my $Ns = ($sseq =~ tr/N/N/); 
	$sequence_info{$sname}{'GC'} = int(10000*$gc/$slength)/100;
	$sequence_info{$sname}{'valid'} = int(10000*($slength-$Ns)/$slength)/100;
	$sequence_info{$sname}{'length'} = $slength;
	$sequence_info{$sname}{'desc'} = $desc;
	$sequence_info{$sname}{'seq'} = $sseq;
	$total_bps += $slength;
	$total_sequences++;
	$length_dist{$slength}++;
}

#####################################################################################################
sub usage {
	my $msg = ($#_ > -1)? $_[0] : undef;
	print STDERR "$msg\n" if defined($msg);
	print STDERR "\nUsage: $0 -i <sequence fasta file> [-o <out-prefix>] [-fasta <T/F>]\n";
	print STDERR "                             [-min_length <length>] [-max_length <length>]\n";
	die "\n";
}

#####################################################################################################
my $sequence_file = undef;
my ($min_length, $max_length) = (0, 4000000000);
my $out_name = undef;
my $fasta = 0;
my $i = 0;

(($#ARGV > 0) && ($#ARGV%2 == 1)) or usage("Incorrect arguments");
while($i < $#ARGV) {
	my $flag = $ARGV[$i++];
	my $param = $ARGV[$i++];

	if($flag eq '-i') {
		$sequence_file = $param;
		(-e $sequence_file) or die "\nError: input file $param does not exist (-i)\n";
	}
	elsif($flag eq '-o') {
		$out_name = $param;
	}
	elsif($flag eq '-min_length') {
		$min_length = $param;
	}
	elsif($flag eq '-max_length') {
		$max_length = $param;
	}
	elsif($flag eq '-fasta') {
		$fasta = ($param eq 'T');
	}
	else {
		usage("Unknown flag: $flag");
	}
}

defined($sequence_file) or die "\nInput sequence file was not supplied (-i)\n\n";
(-e $sequence_file) or die "\nError: input file $sequence_file does not exist (-i)\n";
#defined($out_name) or die "\nOutput name was not supplied\n\n";
defined($out_name) or $out_name = $sequence_file;

open(IN, $sequence_file) or die "\nCannot read $sequence_file\n\n";
my ($sname, $sseq, $sdesc) = (undef, '', undef);
my $lnum = 0;
while(<IN>) {
	$lnum++;
	chomp;
	if($_ =~ />(\S+)(\s+(.+))?/) {
		my ($next_sname, $next_desc) = ($1, $3);
		if((length($sseq) >= $min_length) && (length($sseq) <= $max_length)) {
#			print STDERR '.';
			store_info($sname, $sseq, $sdesc);
		}
		($sname, $sdesc, $sseq) = ($next_sname, $next_desc, '');
	}
	else {
		$sseq .= $_;
	}
}
close(IN);

# Last contig
if((length($sseq) >= $min_length) && (length($sseq) <= $max_length)) {
	store_info($sname, $sseq, $sdesc);
}

open(SUM, ">$out_name.summary.txt") or die "\nCannot write to $out_name.summary.txt\n\n";
print SUM "\nLength distribution\n";
print SUM "===================\n\n";
print SUM "Range    \t# reads (%)\t# bps (%)\n";
my @breakpoints = (0, 100, 500, 1000, 5000, 10000, 20000, 50000, 100000, 500000, 1000000, 1000000000);
my ($bp, $bpi) = ($breakpoints[1], 1);
my ($n, $nbp) = (0, 0);
my ($bps_so_far, $N50) = (0, undef);
foreach my $sname (sort {$sequence_info{$a}{'length'} <=> $sequence_info{$b}{'length'};} keys %sequence_info) {
	if($sequence_info{$sname}{'length'} > $breakpoints[$bpi]) {
		print SUM $breakpoints[$bpi-1], "-$bp:  \t$n (", (int(10000*$n/$total_sequences)/100), "%)\t$nbp (", (int(10000*$nbp/$total_bps)/100), "%)\n"; 
		($bp, $n, $nbp) = ($breakpoints[++$bpi], 0, 0);
		while($sequence_info{$sname}{'length'} > $bp) {
			print SUM $breakpoints[$bpi-1], "-$bp:  \t0 (0%)   \t0 (0%)\n";
			$bp = $breakpoints[++$bpi];
		}		
	}
	$n++;
	$nbp += $sequence_info{$sname}{'length'};
	$bps_so_far += $sequence_info{$sname}{'length'};
	$N50 = $sequence_info{$sname}{'length'} if(!defined($N50) && ($bps_so_far >= $total_bps/2));
}
print SUM $breakpoints[$bpi-1], "-:     \t$n (", (int(10000*$n/$total_sequences)/100), "%)\t$nbp (", (int(10000*$nbp/$total_bps)/100), "%)\n"; 

print SUM "\nGenral Information\n";
print SUM "==================\n\n";
print SUM "Total number of sequences: $total_sequences\n";
print SUM "Total number of bps:       $total_bps\n";
print SUM "Average sequence length:   ", (int(100*$total_bps/$total_sequences)/100), " bps.\n"; 
print SUM "N50:                       $N50", " bps\n";

print SUM "\nSequence parameters\n";
print SUM "===================\n\n";

print SUM "Sequence\tlength\tG+C\tNon-Ns\tdescription\n";
my $i = 1;

foreach my $sname (reverse sort {$sequence_info{$a}{'length'} <=> $sequence_info{$b}{'length'};} keys %sequence_info) {
	print SUM "$i. $sname\t", $sequence_info{$sname}{'length'}, "\t", $sequence_info{$sname}{'GC'}, "\t", $sequence_info{$sname}{'valid'}, "\t", $sequence_info{$sname}{'desc'}, "\n";
	$i++;
}
close(SUM);

if($fasta) {
	open(FASTA, ">$out_name.fasta") or die "\nCannot write to $out_name.fasta\n\n";
	foreach my $sname (reverse sort {$sequence_info{$a}{'length'} <=> $sequence_info{$b}{'length'};} keys %sequence_info) {
		$sequence_info{$sname}{'seq'} =~ s/(.{60})/$1\n/g;
		chomp($sequence_info{$sname}{'seq'});
		print FASTA ">$sname /length=", $sequence_info{$sname}{'length'}, " /%G+C=", $sequence_info{$sname}{'GC'}, " /description=", $sequence_info{$sname}{'desc'}, "\n", 
			    $sequence_info{$sname}{'seq'}, "\n";
	}
	close(FASTA);
}

print STDERR "\nFinished successfully\n";
