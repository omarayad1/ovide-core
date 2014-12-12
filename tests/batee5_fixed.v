`timescale 1ns / 1ps
module NAND2gate(A, B, F);
   	input A;
      	input B;
       	output F;
	reg F;
	always @ (A or B) begin
		F = ~(A & B);
	end
endmodule
