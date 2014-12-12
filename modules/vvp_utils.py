import subprocess


def get_output(filename):
    c = 'vvp %s' % filename
    p = subprocess.Popen(
        [c],
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.STDOUT
    )
    data, err = p.communicate()
    return data.split('\n')


def get_vcd_filename(filename):
    verilog_file_data = open(filename).read()
    vcd_file_name = verilog_file_data.split('"$dumpfile", "')[1].split('";')[0]
    return vcd_file_name