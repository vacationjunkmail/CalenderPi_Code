#!/usr/bin/perl 
use Data::Dumper;
use DateTime::Format::ISO8601;
use strict;
use warnings;
my $basename = "A123456789_chlor_a_2019-07-09_GIBS.tar";
print("$basename\n");

if($basename =~ m/(.*)(?=_[0-9]{4}-[0-9]{2}-[0-9]{2})/i)
{
	print("$1\n\n");
	my $file = $1;
	#$file = $file =~ /(?<=_)/;
	$file = $file =~ m/(.*)(?<=(_))/;
	print("$file = $1\n");
}

$basename = 'SNPP_VIIRS.20180703T230600.L2.OC.nc';
my @perl_time_array = split /\./, $basename;
print "$perl_time_array[1]\n";
my $capture_date = $perl_time_array[1] =~ m/(.*)(?=T)/;
print "$capture_date $1\n";
my $dt = DateTime::Format::ISO8601->parse_datetime($perl_time_array[1]);
print "one \n$dt\n\n";

my $clean_date = $dt->ymd;
print "date two $clean_date";
print "\n\n";
