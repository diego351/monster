import commands
import time
class SystemInfo(object):
    def __init__(self,options):
        self.hostname = commands.getoutput("hostname")
        self.os = commands.getoutput("uname -a")
        self.boottime = int(time.time())
    
    def report(self):
        f = open("/proc/uptime","r")
        sec = int(float(f.readline().split()[0]))

        return {
                "uptime": sec,
                "hostname": self.hostname,
                "os": self.os,
                "boottime": self.boottime,
                }
