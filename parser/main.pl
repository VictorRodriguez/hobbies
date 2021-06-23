#!/usr/bin/perl

$x = 10;

use warnings;

my $filename   = $ARGV[0];

if (!defined($filename)) {
  $filename = 'logs/test.txt';
}


open(FH, '<', $filename) or die $!;

while(<FH>){
	if ($_ =~ /f64Longitude \(deg\) = (\d+)/) {
    	print "$1\n";
	}
}

close(FH);
