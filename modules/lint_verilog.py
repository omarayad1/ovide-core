import subprocess


def check_for_errors(filename):
    p = subprocess.Popen(
        ["verilator --lint-only %s" % filename],
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.STDOUT
    )
    data, err = p.communicate()
    return __format_errors__(data)


def __format_errors__(error_message):
    errors = error_message.split('\n')
    formatted = []
    for error in errors:
        error_split = error.split(':')
        try:
            line = int(error_split[2])
            e = error[error.find(str(line)) + len(str(line)) + 2:]
            formatted.append({'line': line, 'error': e})
        except ValueError:
            pass
        except IndexError:
            pass
    return formatted