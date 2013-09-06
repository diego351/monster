class LoadAvg(object):

    def __init__(self, options):
        pass

    def report(self):
        
        f = open("/proc/loadavg","r")
        spl = f.read().split()
        f.close()
        return {
            '1min': float(spl[0]),
            '5min': float(spl[1]),
            '15min': float(spl[2]),
        }

