import subprocess
import ftp_utils


def compile_to_vvp(filename, filename_test):
    ftp_utils.download_file_to_tmp(filename)
    ftp_utils.download_file_to_tmp(filename_test)
    c = 'iverilog -o ./tmp/%s.vvp ./tmp/%s ./tmp/%s' % (filename[0:-2], filename, filename_test)
    p = subprocess.Popen(
        [c],
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.STDOUT
    )

    data, err = p.communicate()
    if __format_error__(data) != []:
        return __format_error__(data)
    else:
        ftp_utils.upload_file_from_tmp('%s.vvp' % filename[0:-2])


def __format_error__(error):
    error_data = error.split('\n')
    err = []
    for e in error_data:
        try:
            err.append({'line': e.split(':')[1], 'error': e.split(':')[-1]})
        except IndexError:
            pass
    return err