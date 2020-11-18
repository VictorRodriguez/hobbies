my $str = 'Aug 27 13:59:36 topas user.info POS[548]: 00:11:33.989304 <GPS> Input To Sensor Fusion - f64Longitude (deg) = 13286667';
if ($str =~ /f64Longitude \(deg\) = (\d+)/) {
    print $1;
}
