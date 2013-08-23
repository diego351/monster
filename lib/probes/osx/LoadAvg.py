from subprocess import check_output

class LoadAvg(object):

    def report(self):
        raw_values = check_output(['sysctl', '-n', 'vm.loadavg'])
        load_values = raw_values.split()[1:4]
        return {
            '1min': load_values[0],
            '5min': load_values[1],
            '15min': load_values[2],
        }

