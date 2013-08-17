

class LoadAvg(object):

    def __init__(self):
        pass

    def report(self):
        
        f = open("/proc/loadavg","r")
        spl = f.read().split()
        f.close()
        return {
            '1min': spl[0],
            '5min': spl[1],
            '15min': spl[2],
        }

