class MemInfo:
    def __init__(self, probe_opts):
        pass

    def report(self):
        f = open("/proc/meminfo","r")
        txt = f.read()
        spl = txt.split("\n")

       
        for line in spl:
            if "MemFree" in line:
                tmp = line.split()
                free = int(tmp[1])
                continue
            elif "MemTotal" in line:
                tmp = line.split()
                total = int(tmp[1])
                continue
            elif "Cached" in line and not "SwapCached" in line: # kernel naming -,-
                tmp = line.split()
                cached = int(tmp[1])
                continue
       
        free += cached
        used = total - free
    
        return { 
                "free": free,
                "used": used,
                "total": total,
        }
