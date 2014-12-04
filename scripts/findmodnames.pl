#!/usr/bin/perl

# Use:
#	findmodnames	file.v
#

my $file = $ARGV[0];
open my $info, $file or die "Could not open $file: $!";

# first construct a string for the module defination
$modDecl = "";
$portDecl = "";

$flag = 0;
while( my $line = <$info>)  {   
	if($flag==0 && $line=~ m/^module/){
		chomp($line);
		#print $line;
		$modDecl = $modDecl . $line; 			
		$flag = 1;
		if($line=~ m/\x29\x3b/) #);
		{
			$flag = 0;
			print getModName($modDecl) . "\n";
			$modDecl = "";
		}
	} elsif($flag==1){
		chomp($line);
		$modDecl = $modDecl . $line; 
		if($line=~ m/\x29\x3b/) #);
		{
			$flag = 0;
			print getModName($modDecl) . "\n";
			$modDecl = "";
		}
	}
}

#print $modDecl;

#now get the module name

sub getModName{
	$s = $_[0];
	if($s =~ m/^module\s+([^\s\(]*)/) {
		return $1;
	} else {
		return "";
	}
}
