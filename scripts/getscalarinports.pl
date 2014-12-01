#!/usr/bin/perl

# Use:
# 	getscalarinports file.v module_name
#

my $file 	= $ARGV[0];
my $mod	= $ARGV[1];

open my $info, $file or die "Could not open $file: $!";

# first construct a string for the module defination
$modDecl = "";
$portDecl = "";

$flag = 0;
$ansi = 0;


while( my $line = <$info>)  {   
	chomp($line);
	if($flag==0 && $line=~ m/^module/){
		#print "--- flag = 0";
      	chomp($line);
      	$modDecl = $modDecl . $line; 			
      	$flag = 1;
      	
      	if($line=~ m/\x29\x3b/) #);
      	{
           	 $flag = 2;
             if($modDecl !~ m/\b$mod\b/){
             	#print "+++ $modName\n";
             	$modDecl="";
             	$flag = 0;
             }
        }
    } elsif($flag==1){
      	chomp($line);
      	$modDecl = $modDecl . $line;
      	
      	if($line=~ m/\x29\x3b/) #);
        {
             $flag = 2;
             if($modDecl !~ m/\b$mod\b/){
             	#print "+++ $modName\n";
             	$modDecl="";
             	$flag = 0;
             }

      	}
	} elsif($flag==2) { # it does not handle multi-line port declaration
		
		#print "--- flag == 2 modName = $modName [$modDecl]\n";
      	if($line =~ m/endmodule/){
			last;
		}
		chomp($line);
		$line =~ s/^\s+//;
		$line =~ s/reg//;	# remove reg
		$line =~ s/\,/\;/;	# replace ',' by ';' if any 
		
		if($line =~ m/input/){
			#print "===> $line\n";
			getPorts($line);
			
		}
	}  
	
	if($flag == 2) {
		# check whether the module uses ANSI style or not!
		if($modDecl=~ m/input|output|inout/){
			$ansi = 1;
			#$pars = build_decl($modDecl);
			last;
		}
	}
}



#print "Debug: $modDecl\n";
#print "Debug: $pars\n";
#print "Debug: $ansi\n";

if($ansi == 1)
{
	$pars = form_decl($modDecl);
	#print "==* $pars *==\n";
	
	my @values = split(',', $pars);

	foreach my $line (@values) {
		
		if($line =~ m/input/ && $line !~ m/\[/){
			#print "==$line==\n";
			# remove input and ;
			$line =~ s/input//g;
			$line =~ s/;//g;
		
			# Trim spaces
			$line =~ s/^\s+//;
			$line =~ s/\s+$//;
			
			print "$line\n";
		}
	}
} 

#now get the module name
sub form_decl{
	my $s = $_[0];
	my $tmp = "(";
	my $port;
	
	$s =~ s/module//;
	$s =~ s/reg//;
	$s =~ s/\;//;
	
	$i1 = index($s,"input");
	$i2 = index($s,"output");
	$i3 = index($s,"inout");

	$i1 = 1000000 if($i1<0);
	$i2 = 1000000 if($i2<0);
	$i3 = 1000000 if($i3<0);
	
	$i=$i1 if($i1<$i2);
	$i=$i3 if($i3<$i);
	
	#print "emit: $s\n";
	#print "$i ($i1, $i2, $i3)\n";
	$s = substr($s, $i);	
	
	$s =~ s/\)/ /g;
	
	return $s;
}


sub getModName{
	$s = $_[0];
	if($s =~ m/^module\s+([^\s\(]*)/) {
		return $1;
	} else {
		return "";
	}
}


sub getPorts{
	$s = $_[0];
	#print "=>$s\n";
	if($s =~ m/\[/) {
		return;
	} else {
		#print $s;
		# remove input and ;
		$s =~ s/input//g;
		$s =~ s/;//g;
		
		# Trim spaces
		$s =~ s/^\s+//;
		$s =~ s/\s+$//;
		@sentences = split /,/, $s;
		foreach my $sentence(@sentences) {
		# Remove newlines for readability.
		# Replace them with spaces.
		$sentence =~ s/[\n\r\f]/ /g;
	
		# Trim space from the start and end.
		$sentence =~ s/^\s*|\s*$//;
		print "$sentence\n";
	}	
	}
}