#!/usr/bin/perl

$x = 10;

use warnings;

my $filename   = $ARGV[0];
my $dynamic_regex = 'f64Longitude \(deg\) = (\d+)';

if (!defined($filename)) {
  $filename = 'logs/test.txt';
}


open(FH, '<', $filename) or die $!;

while(<FH>){
	if ($_ =~ /$dynamic_regex/) {
		print "$1\n";
	}
}

close(FH);
