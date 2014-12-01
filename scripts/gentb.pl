#!/usr/bin/perl

# gentb
# Verilog testbench Generator
# Arguements:
#	DUT_module_name		verilog_file	tb_module_name
#

my $modName = $ARGV[0];
my $file 	= $ARGV[1];
my $tbModName = $ARGV[2];
my $timeScale = $ARGV[3];
my $clocked	= $ARGV[4];
my $clk		= $ARGV[5];	# arguments 5, 6 & 7 are only used if arg 4 is 1
my $rst		= $ARGV[6];
my $period	= $ARGV[7];

my $modDecl = "";
#my $modName	= "";

my $ansi = 0;
my $pars = "";

open my $info, $file or die "Could not open $file: $!";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);
$year = $year + 1900;
$mon += 1;

print "// Automatically Generated Testbench for module $modName\n";
print "// Generated on $mday/$mon/$year $hour:$min:$sec \n\n";
print "`timescale ".$timeScale."ns/1ns\n\n";

print "module $tbModName;\n";

# first construct a string for the module defination
$flag = 0;


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
             if($modDecl !~ m/\b$modName\b/){
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
             if($modDecl !~ m/\b$modName\b/){
             	#print "+++ $modName\n";
             	$modDecl="";
             	$flag = 0;
             }

      	}
	} elsif($flag==2) {
		
		#print "--- flag == 2 modName = $modName [$modDecl]\n";
      	if($line =~ m/endmodule/){
			last;
		}
		chomp($line);
		$line =~ s/^\s+//;

		$line =~ s/reg//;	# remove reg
		#$line =~ s/\,/\;/;	# replace ',' by ';' if any 
		
		
		if($line =~ m/input/){
			
			$line =~ s/input/reg/g;
			print "$line \n";
			
		}
		
		if($line =~ m/output/){
			$line =~ s/output/wire/g;
			print "$line \n";
			
		}
	}  
	
	if($flag == 2) {
		# check whether the module uses ANSI style or not!
		if($modDecl=~ m/input|output|inout/){
			$ansi = 1;
			$pars = emit_reg_wire($modDecl);
			last;
		}
	}
}

#print "pars: $pars\n";

$modName = getModName($modDecl);
print "\n";
print $modName;
print " DUT (";

#print "===>$ansi\n";
if($ansi==0) {
processPars($modDecl);
} else {
processPars($pars);
}
print " );\n\n";
print "initial begin\n \$dumpfile (\"$tbModName.vcd\");\n \$dumpvars (1,$tbModName);\n #1000 \$finish;\t\t//simulate for 1000 ticks only\nend\n\n"; 
if($clocked == 1){
	print "// Clock Generator \ninitial  $clk = 0;\nalways #".$period/2 . " $clk = ~$clk;\n\n";
	print "// Reset Generator goes here\n// Change to match your design\n";
	print "initial begin\n $rst = 0;\n @ (negedge $clk);\n @ (negedge $clk);\n $rst = 1;\nend\n\n";
} else {
	print ("initial begin\n// Write your test case here\n\nend\n\n");
}
print "endmodule\n\n";


#now get the module name
sub getModName{
	$s = $_[0];
	if($s =~ m/^module\s+([^\s\(]*)/) {
		return $1;
	} else {
		return "";
	}
}

sub emit_reg_wire{
	my $s = $_[0];
	my $tmp = "(";
	my $port;
	
	$s =~ s/module//;
	$s =~ s/reg//;
	$s =~ s/\;//;
	
	# check to see if there is a module parameter
	if(index($s,"#")>-1){
		$s =~ m/\#\s*\((.*?)\)/;
		print "$1;\n";
	}
	
	$i1 = index($s,"input");
	$i2 = index($s,"output");
	$i3 = index($s,"inout");

	$i1 = 1000000 if($i1<0);
	$i2 = 1000000 if($i2<0);
	$i3 = 1000000 if($i3<0);
	
	$i = $i2;
	$i=$i1 if($i1<$i2);
	$i=$i3 if($i3<$i);
	
	#print "emit: $s\n";
	#print "$i ($i1, $i2, $i3)\n";
	$s = substr($s, $i);	
	
	#print "1st port at $i, $s\n";
	
	$s =~ s/\)/ /g;
	
	#print "emit: $s\n";
	
	my @values = split(',', $s);

	foreach my $line (@values) {
		chomp($line);
		$line =~ s/^\s+//;
		
		$port = $line;
		$port =~ m/[input|output|inout]\s+(?:\[[^]]+\]\s+)*(\w+)/;
		$tmp = "$tmp$1,"; 
		if($line =~ m/input/){
			$line =~ s/input/reg/g;
			print "$line; \n";
		}
		if($line =~ m/output/){
			$line =~ s/output/wire/g;
			print "$line; \n";
		}
	}
	
	return $tmp;
}

sub processPars{
	my $s = $_[0];
	#print "===> $s\n";
	my $cnt=0;
	$s =~ m/\(([^\)]+)/;
	#print $1;
	my @values = split(',', $1);

	foreach my $val (@values) {
		$val =~ s/^\s+//;
		$val =~ s/\s+$//;
    	print ".$val($val)";
    	print ", " if ++$cnt != scalar(@values);
  }
}