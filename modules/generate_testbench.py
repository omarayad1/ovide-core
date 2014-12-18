import ftp_utils

def get_timescale(s):
    aa = s.split()
    word = aa[aa.index('`timescale') + 1]
    return word.split('(')[0]

def get_module_name(s):
    aa = s.split()
    word = aa[aa.index('module') + 1]
    return word.split('(')[0]


def get_regs(s):
    regs = []
    aa = s.split()
    while 'input' in aa:
        word = aa[aa.index('input') + 1]
        word = word.replace(';', ',')
        regs.append(word.split(',')[0])
        del aa[aa.index('input')]
    return regs


def get_wires(s):
    wires = []
    aa = s.split()
    while 'output' in aa:
        word = aa[aa.index('output') + 1]
        word = word.replace(';', ',')
        wires.append(word.split(',')[0])
        del aa[aa.index('output')]
    return wires


def generate_testbench(filename):
    ftp_utils.download_file_to_tmp(filename)
    module = open('./tmp/%s' % filename, 'r').read()
    out = ""
    modname = get_module_name(module)
    tbmodname = modname + "_tb"

    clk = "clk"
    rst = "rst"
    period = 3

    timescale = getTs(module)

    out += "// Automatically Generated Testbench for module " + modname + "\n"
    out += "// Generated on  \n"
    out += "`timescale " + timescale + "\n \n"
    out += "module " + tbmodname + "; \n \n"

    regs = get_regs(module)
    wires = get_wires(module)

    for i in regs:
        out += "reg " + i + "; \n"

    for i in wires:
        out += "wire " + i + "; \n"

    out += "\n"

    out += modname + " DUT ( "

    for i in regs:
        out += "." + i + "(" + i + ")"
        out += ", "

    for i in wires:
        out += "." + i + "(" + i + ")"
        if i != wires[-1]:
            out += ", "

    out += " ); \n \n"

    out += "initial begin \n"
    out += "$dumpfile (" + '"' + tbmodname + ".vcd" + '"' + "); \n"
    out += "$dumpvars (1, " + tbmodname + ".v); \n"
    out += "#1000 $finish; \n"
    out += "end\n \n"

    if clk != "":
        out += "// Clock Generator \n"
        out += "initial " + clk + " = 0; \n"
        out += "always #" + str(period/2.0) + " " + clk + " = ~" + clk + "; \n \n"
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
    testbench_file = open('./tmp/%s_tb.v' % filename[0:-2], 'w')
    testbench_file.write(out)
    testbench_file.close()
    ftp_utils.upload_file_from_tmp('%s_tb.v' % filename[0:-2])
    return out