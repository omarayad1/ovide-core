import re

modee = ''''timescale 1ns / 1ps
module NAND2gate(A, B, F);
   	input A;
      	input B;
       	output F;
	reg F;
	always @ (A or B) begin
		F = ~(A & B);
	end
endmodule
'''


#Returns module name
def getModName(s):
	aa = s.split()
	word = aa[aa.index('module') + 1]
	return word.split('(')[0] 

def getRegs(s):
	regs = []
	aa = s.split()
	while 'input' in aa:
		word = aa[aa.index('input') + 1]
		word = word.replace(';',',')
		regs.append( word.split(',')[0])
		del aa[aa.index('input')]
	return regs
	
def getWires(s):	
	wires = []
	aa = s.split()
	while 'output' in aa:
		word = aa[aa.index('output') + 1]
		word = word.replace(';',',')
		wires.append( word.split(',')[0])
		del aa[aa.index('output')]
	return wires



def genTB(module):
	out = ""
	modname = getModName(module)
	tbmodname = modname + "_tb"

	clk = "clk"
	rst = "rst"
	period = 3

	timescale = 1#getTs(module)


	out += "// Automatically Generated Testbench for module " + modname + "\n"
	out += "// Generated on  \n"
	out += "`timescale " + str(timescale) + "ns/1ns \n \n"
	out += "module " + tbmodname + "; \n \n"

	regs = getRegs(module)
	wires = getWires(module)
	
	for i in regs:
		out += "reg " + i + "; \n"

	for i in wires:
		out += "wire " + i + "; \n"

	out += "\n"

	out += modname + " DUT ( "

	for i in regs:
		out += "." + i + "(" + i +  ")"
		# if i != regs[-1]:
		out += ", "

	for i in wires:
		out += "." + i + "(" + i +  ")"
		if i != wires[-1]:
			out += ", "

	out += " ); \n \n"

	out += "initial begin \n"
	out += "$dumpfile (" + '"' +tbmodname  + ".vcd" + '"' + "); \n"
	out += "$dumpvars (1, "+  tbmodname + ".v); \n"
	out += "#1000 $finish; \n"
	out += "end\n \n"

	if clk != "":
		out += "// Clock Generator \n"
		out += "initial " + clk + " = 0; \n"
		out += "always #" + str(period/2.0) +" "+  clk + " = ~" + clk + "; \n \n"
		out += "// Reset generator goes here, change to match your design  \n"

	out += "initial begin \n"
	if clk != "":
		out += rst + " = 0; \n"
		out += "@ (negedge clk); \n"
		out += rst + " = 1; \n"
	else:
		out += "// Write your test case here \n"
	out += "end\n \n"
	out += "endmodule\n"

	return out

print genTB(modee)