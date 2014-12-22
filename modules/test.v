// Automatically Generated Testbench for module NAND2gate
// Generated on  
`timescale 1ns/1ns 
 
module NAND2gate_tb; 
 
reg A; 
reg B; 
wire F; 

NAND2gate DUT ( .A(A) .B(B) .F(F)  ); 
 
initial begin 
$dumpfile ("NAND2gate_tb.vcd"); 
$dumpvars (1, NAND2gate_tb.v); 
#1000 $finish; 
end
 
// Clock Generator 
initial clk = 0; 
always #1.5 clk = ~clk; 
 
// Reset generator goes here, change to match your design  
initial begin 
rst = 0; 
@ (negedge clk); 
rst = 1; 
end
 
endmodule

