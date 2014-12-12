// nand2gate_tb.v

// 2-input NAND gate testbench

// ------------------------------------------------------------------
// Copyright (c) 2006 Susan Lysecky, University of Arizona
// Permission to copy is granted provided that this header remains
// intact. This software is provided with no warranties.
// ------------------------------------------------------------------

`timescale 1ns / 1ps

module Testbench;

   reg A_t, B_t;
   wire F_t;

   NAND2gate NAND2gate_1(A_t, B_t, F_t);
   
   initial
   begin
     $dumpfile("test.vcd");
     $dumpvars(0,Testbench);
      //case 0
      A_t <= 0; B_t <= 0;
      #1 $display("F_t = %b", F_t);
	  
      //case 1
      A_t <= 0; B_t <= 1;
      #1 $display("F_t = %b", F_t);
	  
      //case 2
      A_t <= 1; B_t <= 0;
      #1 $display("F_t = %b", F_t);
	  
      //case 3
      A_t <= 1; B_t <= 1;
      #1 $display("F_t = %b", F_t);
	  
   end
endmodule
