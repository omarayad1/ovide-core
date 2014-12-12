import subprocess


def compile_to_vvp(filename, filename_test):
    c = 'iverilog -o %s.vvp %s %s' % (filename[0:-2], filename, filename_test)
    p = subprocess.Popen(
        [c],
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.STDOUT
    )
    data, err = p.communicate()
    return __format_error__(data)


def __format_error__(error):
    error_data = error.split('\n')
    err = []
    for e in error_data:
        try:
            err.append({'line': e.split(':')[1], 'error': e.split(':')[-1]})
        except IndexError:
            pass
    return err