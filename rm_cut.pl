#!/usr/bin/perl
###############################################################################
# 
# Author: chenhe
# Created Time: Mon 30 Jun 2014 11:50:16 AM CST
# 
###############################################################################

use strict;
use warnings;

die "Usage: $0 <PE.sam>\n", if ( $#ARGV != 0 );

my $FILE;

open $FILE, '<', $ARGV[0] or die "Can't open $ARGV[0]: $!\n";

while ( my $first = <$FILE> )
{
	if ( $first =~ m/^@/o )
	{
		print $first;
		next;
	}

	my $second = <$FILE>;

	my @first  = split /\t/, $first;
	my @second = split /\t/, $second;

	my $name1 = $first[0];
	my $name2 = $second[0];
	die "$name1 and $name2 NOT same!\n", if ( $name1 ne $name2 );

	my $q1 = $first[4];
	my $q2 = $second[4];
	next, if (  ( $q1 < 20 ) or ( $q2 < 20 )  );

	my $chr1 = $first[2];
	my $chr2 = $second[2];
	next, if (  ( $chr1 =~ m/random/o ) or ( $chr2 =~ m/random/o )  );

#	my $flag1 = 1;
#	my $flag2 = 1;
#	$flag1 = ( $first  =~ m/\tXS:i:\d+/ || $first  =~ m/\tXS:i:-\d+/) ? $flag1 : 0;
#	$flag2 = ( $second =~ m/\tXS:i:\d+/ || $first  =~ m/\tXS:i:-\d+/) ? $flag2 : 0;
#	next, if (  ( not defined $flag1 ) or ( not defined $flag2 )  );

#	$flag1 = ( $flag1 =~ s/^X0:i:(\d+)$/$1/o ) ? $flag1 : 0;
#	$flag2 = ( $flag2 =~ s/^X0:i:(\d+)$/$1/o ) ? $flag2 : 0;
	my $seq1 = $first[9];
	my $seq2 = $first[9];
	next, if (  ( $seq1 =~ m/\*/o ) or ( $seq2 =~ m/\*/o )  );


#	if ( ($flag1 == 1) && ($flag2 == 1) )

#	{
#		print $first, $second;
#	}
#	else{
		print $first, $second;
#	}
}

close $FILE;

