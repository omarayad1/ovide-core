import subprocess
import ftp_utils
from vcdparser import parse_vcd, get_endtime, get_timescale


def __check_if_dumps_vcd_correctly__(filename):
    ftp_utils.download_file_to_tmp(filename)
    vcd_name = __get_vcd_filename__(filename)
    if vcd_name.find("./tmp/") < 0:
        file_instance = open('./tmp/%s' % filename, 'r+')
        data = file_instance.read()
        data = data.replace('"$dumpfile", "', '"$dumpfile", "./tmp/', 1)
        file_instance.seek(0)
        file_instance.write(data)
        file_instance.close()
    ftp_utils.upload_file_from_tmp(filename)


def __upload_dump_files__(filename):
    vcd_name = __get_vcd_filename__(filename)
    if vcd_name != -1:
        ftp_utils.upload_file_from_tmp(vcd_name.replace('./tmp/', ''))


def __get_vcd_filename__(filename):
    ftp_utils.download_file_to_tmp(filename)
    verilog_file_data = open("./tmp/%s" % filename, 'r').read()
    vcd_file_name = verilog_file_data.split('"$dumpfile"')[1].split('"')[1]

    return vcd_file_name


def get_output(filename):
    __check_if_dumps_vcd_correctly__(filename)
    ftp_utils.download_file_to_tmp(filename)
    c = 'vvp ./tmp/%s' % filename
    p = subprocess.Popen(
        [c],
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.STDOUT
    )
    data, err = p.communicate()
    __upload_dump_files__(filename)
    return data.split('\n')


def get_wave(filename):
    ftp_utils.download_file_to_tmp(filename)
    vcd = parse_vcd("./tmp/%s" % filename)
    units = get_timescale()
    i = 0
    time = 0
    endtime = get_endtime()
    data = {'file': filename, 'scale': units, 'endtime': endtime, 'signals': []}
    for key, value in vcd.iteritems():
        name = value['nets'][0]['hier'] + "." + value['nets'][0]['name']
        size = value['nets'][0]['size']
        data['signals'].append({'name': name, 'size': size, 'wave': []})
        time = 0

        for item in value['tv']:
            wavestruct = []
            val = item[1]
            wavestruct.append(item[0])
            if val.find('z') > -1:
                wavestruct.append('z')
            elif val.find('x') > -1:
                wavestruct.append('x')
            else:
                wavestruct.append(val)
            data['signals'][i]['wave'].append(wavestruct)
        i += 1
    return data