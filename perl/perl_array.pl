#!/usr/bin/perl 

my @first_array = ('one','two','three','four');

my @second_array = ('two','four');

foreach my $item (@first_array)
{
        #print("$item ");
	my $found = grep(/$item/, @second_array);
	if($found > 0)
	{
		print("$item $found\n");	
	}
	#print("$found\n");
}
use POSIX qw(strftime);
my $now_string = strftime "%a %b %e %H:%M:%S %Y",localtime;
print "$now_string\n";

