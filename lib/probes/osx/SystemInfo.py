import commands

class SystemInfo(object):
    def __init__(self):
        self.hostname = commands.getoutput("hostname")
        self.os = commands.getoutput("uname -a")
        self.boottime = int(commands.getoutput("sysctl kern.boottime").split()[4][:-1])
    def report(self,options):

        currentSec = int(commands.getoutput("date +%s"))

        return {
                "uptime": currentSec - self.boottime,
                "hostname": self.hostname,
                "os": self.os,
                }
