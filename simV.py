#!/usr/bin/env python
import os
import subprocess
from Paths import *
import datetime

if "check_output" not in dir( subprocess ):
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f


def cmdNwait(c):
    try:
        r = subprocess.check_output(c, shell=True)
    except:
        r = ''
    return r

class simV:
                    
    def __init__(self, dotVFile, postfix):
        self.file_location = dotVFile 
        self.temp_file = temp_file + '__' + postfix + '.txt'
        self.destination_file = destination_file + '__' + postfix  + '.txt'
        self.compiled_File = compiled_File + '__' + postfix  + '.vvp'
        self.jsontemp_file = jsontemp_file + '__' + postfix + '.txt'

    def buildV(self, directory=''):
        errors = self.checkForStopCall()
        if errors == '':
            c = 'verilator --lint-only ' + self.file_location + ' -I' + directory + ' > ' + self.temp_file + ' 2>&1'
            p = cmdNwait(c)
            errors = open(self.temp_file, 'r').read()
        if errors:
            return self.formatVerilatorError(errors)
        return 'no'
    
    def checkForStopCall(self):
        errors = ''
        c = open(self.file_location, 'r')
        t = c.read()
        c.close()
        t = t.split('\n')
        for i in t:
            if '$stop' in i and not '//' in i:
                errors += str(i) + ': warning, $stop calls cause the simulator to get stuck, please comment it.\n'
            elif '$stop' in i and '//' in i:
                if i.index('//') < i.index('$stop'):
                    pass
                else:
                    errors += str(i) + ': warning, $stop calls cause the simulator to get stuck, please comment it.\n'
        return errors
    
    def formatVerilatorError(self, errorsString):
        errors = errorsString.split('\n')
        formatted = []
        for error in errors:
            errorSplit = error.split(':')
            try:
                line = str(int(errorSplit[2]))
                e = error[error.find(line) + len(line) + 2:]
                formatted.append({'line':line, 'error':e})
            except:
                pass
        
        z = open(APP_ROOT + 'csce495one/static/commands.html', 'r')
        x = z.read()
        z.close()
        z = open(APP_ROOT + 'csce495one/static/commands.html', 'w')
        x = (datetime.datetime.now()+datetime.timedelta(minutes=480)).strftime("%I:%M:%S %p")+ ' ' + str(errorsString) + '<br/>' + x
        z.write(x)
        z.close()
        return formatted
    
    def errors(self):
        errors = self.checkForStopCall()
        if errors == '':
            c = 'iverilog -o ' + self.destination_file + ' -c ' + self.file_location + ' > ' + self.temp_file + ' 2>&1'
            p = cmdNwait(c)
            errors = open(self.temp_file, 'r').read()
        if errors:
            return self.formatError(errors)
        return False
    
    def formatError(self, error):
        errors = error.split('\n')
        err = []
        for e in errors:
            try:
                if '.tb.v' in e:
                    err.append({'line':e.split(':')[1], 'error':e.split(':')[-1]})
                else:
                    err.append({'line':e.split('___')[1].split(':')[0] + ':' + e.split('___')[1].split(':')[1], 'error':e.split(':')[-1]})
            except:
                pass
        return err
    
    def generateVCD(self):
        if self.errors():
            return False
        comF = self.compiled_File
        c = 'iverilog -o ' + comF + ' -c ' + self.file_location
        
        
        p = cmdNwait(c)

        c = '/var/www/html/csce495one/temp/'
        os.chdir(c)
        
        c = 'vvp ' + comF

        p = cmdNwait(c)

        data = open(comF, 'r').read()
        data = data.split('"$dumpfile", "')[1]
        data = data.split('";')[0]
        self.vcd_file = data
        self.abs_vcd_file = '/var/www/html/csce495one/temp/' + data
        return True
    
    def getJson(self):
        if self.generateVCD():
            c = PERLPATH + "  " + Pscript + self.abs_vcd_file + ' > ' + self.jsontemp_file
            #print c
            
            p = cmdNwait(c)
            o = open(self.jsontemp_file, 'r')
            d = o.read()
            o.close()            
            return self.formatJson(d.replace('\n', ''))
        return self.errors()
    
    def formatJson(self, jsonData):
        jsonData = jsonData.replace('\n', '')
        jsonData = jsonData.replace('signal', '"signal"')
        
        data = eval(jsonData.replace('true', 'True').replace('false', 'False'))
        
        c = data.pop('signal', None)
        
        for x in range(len(c)):
            c[x] = str(c[x])
        
        return c