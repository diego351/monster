import commands

class LoadAvg(object):

    def __init__(self, options):
        pass

    def report(self):
        #raw_values = check_output(['sysctl', '-n', 'vm.loadavg'])i
        raw_values = commands.checkoutput("sysctl -n vm.loadavg")
        load_values = raw_values.split()[1:4]
        return {
            '1min': float(load_values[0]),
            '5min': float(load_values[1]),
            '15min': float(load_values[2]),
        }
