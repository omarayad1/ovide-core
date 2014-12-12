<?php
/* 
	this file is based on fsm.php
	+ More comments
	+ command line arguments 
	+ integrate the in2json script

*/

$mod_name = "fsm";			// Verilog module name
$state_encoding = 2;		// 1-bin, 2-OHE, 3-Gray
$clk = "clk";				// clock input name
$clk_edge = "posedge";		// clock triggering edge
$rst = "rst";				// reset input name
$rst_edge = "negedge";		// reset triggering edge in case of Asynchronous reset (see below)
$rst_mode = 1;				// 1-Sync, 2-Async
$rst_level = 0;				// reset level in case of synchronous reset
$fsm_input = "x, y,z, w[ 2 : 0] , v [1:0], u ";
$fsm_output = "a, b, c"; 

if (!isset($argv[1])) {
    echo 'Missing FSM Json file name ';
    echo "\n";
    exit(0);
}

$json = file_get_contents($argv[1]);
$obj1 = json_decode($json);
$obj = $obj1->data;
$mod_name = $obj1->module_name; 


$mod_inputs = in2json($obj1->imports/*$fsm_input*/);
$inputs = json_decode($mod_inputs);

$err = 0;
$err_param = "";

$states = array();

// check for errors
// 1) Check for Reset State
$rst_state_cnt = 0;
$rst_state = "";
foreach($obj->nodes as $node)
{
	if($node->isAcceptState == 'true') {
		$rst_state_cnt++ ;
		$rst_state = $node->text;
	}
	array_push($states, $node->text);
}

if ($rst_state_cnt == 0) $err = 1 ;
if ($rst_state_cnt > 1) $err = 2 ;

// 2) Check for repeated states
$tmp = array_count_values($states);
//print_r($tmp);
//print_r($states);

foreach ($tmp as $key => $value) {
        if($value > 1) {
        	$err = 3;
        	$err_param = $key;
        	//echo "$key - $value\n";
        }
}

// 3) check the transition conditions


// Report Errors
switch ($err) {
	case 1: echo "Err ($err): Reset state is not defined\n";
	case 2: echo "Err ($err): More than one Reset state\n" ;
	case 3: echo "Err ($err): State: $err_param is not unique\n"  ;
}

// Code Generator
date_default_timezone_set('UTC');
echo "/*\n";
echo " * FSM Generator V0.01 \t\t\t\t\t *\n";
echo " * Generated on ". date('l jS \of F Y h:i:s A') . " \t *\n";
echo " */\n\n";

foreach($states as $state){
	echo "`define\t$state\t$width'b"; 
		
	if($state_encoding == 1){
		echo decbin($i)."\n";
	}
	else {
		echo decbin(pow(2,$i)). "\n";
	}
	$i = $i + 1;
}

$width_bin = ceil(log(count($states),2));
$width_ohe = count($states);

if($state_encoding == 1) $width = $width_bin;
else if($state_encoding == 2) $width = $width_ohe;


echo "\nmodule ".$mod_name."($clk, $rst";
foreach($inputs as $inp){
	echo ", $inp->name";
} 
echo ", state);\n";
echo "input $clk, $rst;\n";

foreach($inputs as $inp){
	echo "input ";
	if($inp->size > 1) echo "[$inp->to:$inp->from] ";
	echo "$inp->name;\n";
} 

echo "output [".($width-1)." : 0] state;\n";

// Generate the state codes
$i = 0;

echo "\n// Declare state flip flops\nreg [".($width-1)." : 0] state, nextstate;\n\n";

echo "always @ ( $clk_edge $clk ";
if($rst_mode==1) { 
	echo ") begin\n";
	echo "\tif( $rst == 1'b$rst_level)\n";
	echo "\t\tstate <= `$rst_state;\n\telse\n\t\tstate <= nextstate;\n";
}
echo "end\n\n";

echo "// next state logic\n";
echo "always @ (*) begin\n";
echo "\tcase (state)\n";

$i = 0;

foreach($states as $state){
	echo "\t\t`$state: ";
	transition($states, $obj->links, $i);
	$i = $i + 1;
}
echo "\tendcase\n";
echo "end\n";
echo "endmodule\n";


function transition($states, $links, $s)
{
	$next = "";
	foreach($links as $link)
	{
		if(($link->type == "SelfLink" && $link->node == $s) || ($link->type == "Link" && $link->nodeA == $s))
		{
			$pieces = explode("/", $link->text);
			if($link->type == "SelfLink") 
				$next=$link->node;
			else 
				$next=$link->nodeB;
			echo "\n\t\t\tif($pieces[0]) nextstate = `".$states[$next].";";
		}
	}
	echo "\n";
}

function in2json($fsm_input) {
	$inputs_obj = json_decode('{"inputs":[{"name":"", "size":0, "from":0, "to":0}]}');
	$pieces = explode(",",$fsm_input);
	
	$json = "[";
	$flag = 0;
	
	foreach($pieces as $var){
		$tmp = trim($var);
		if(strstr($tmp,"[") == FALSE)
		{
			$entry->name = $tmp;
			$entry->size = 1;
			$entry->from = 0;
			$entry->to = 0;
		} else {
			$ta0 = explode("[", $tmp, 2);
			$ta1 = explode(":", $ta0[1], 2);
			$ta2 = explode("]", $ta1[1], 2);
			
			$entry->name = trim($ta0[0]);
			$entry->size = ceil(trim($ta1[0])) - ceil(trim($ta2[0])) + 1;
			$entry->to = ceil(trim($ta1[0]));
			$entry->from = ceil(trim($ta2[0]));
		}
		if($flag == 0) $flag = 1;
		else $json = $json . ",";
		$json = $json . json_encode ($entry);
	}
	$json = $json . "]";
	return $json;

}