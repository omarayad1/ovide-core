// Automatically Generated Testbench for module NAND2gate
// Generated on 15/12/2014 1:4:29 

`timescale ns/1ns

module batee5_tb.v;
reg A; 
reg B; 
wire F; 

NAND2gate DUT (.A(A), .B(B), .F(F) );

initial begin
 $dumpfile ("batee5_tb.v.vcd");
 $dumpvars (1,batee5_tb.v);
 #1000 $finish;		//simulate for 1000 ticks only
end

initial begin
// Write your test case here

end

endmodule

