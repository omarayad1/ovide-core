from subprocess import call, Popen, PIPE
import subprocess
p = Popen(["bin/verilator", "--lint-only","tests/batee5.v"],stdout=PIPE, shell=True, stderr=subprocess.STDOUT)
data,err =  p.communicate()
print data,err
