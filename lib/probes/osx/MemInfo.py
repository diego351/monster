#import subprocess
import commands
import math


class MemInfo:

    def __init__(self, options):
        pass

    def report(self):
        output = commands.getoutput("vm_stat")
        splitted = output.split("\n")
        pageSize = int(splitted[0].split()[7])
        free = int(splitted[1].split()[2][:-1])
        active = int(splitted[2].split()[2][:-1])
        inactive = int(splitted[3].split()[2][:-1])
        speculative = int(splitted[4].split()[2][:-1])
        wired = int(splitted[5].split()[3][:-1])

        pageSizeShift = int(math.sqrt(pageSize >> 10))
        free += speculative
        total = active + inactive + wired + free

        # as power!

        return {
            "free": free >> (10 - pageSizeShift),
            "total": total >> (10 - pageSizeShift),
            "active": active >> (10 - pageSizeShift),
            "inactive": inactive >> (10 - pageSizeShift),
            "wired": wired >> (10 - pageSizeShift),
        }
