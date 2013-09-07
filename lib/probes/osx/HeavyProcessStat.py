import commands

class HeavyProcessStat(object):
    def __init__(self,options):
        if "proc_number" in options:
            self.howMany = int(options["proc_number"])
        else:
            self.howMany = 5

        self.prevCpuDict = {}
        self.prevMemDict = {}


    def report(self):
        howMany = self.howMany
        cpuDict = {}
        memDict = {}
        outCpu = commands.getoutput("ps xrco %cpu,command") # -o for custom format, -r for cpu sorting, -c for just process name (not full path, -x for all processes)
        outMem = commands.getoutput("ps xmco %mem,command")
        for line in outCpu.split("\n")[1:]: #ommiting shit
            s = line.split(None, 1) # btw how to not pass a separator (use default separator == any whitespace) and split with max split? Any ideas? "\s" separator doesn't seem to work
            if cpuDict.has_key(s[1]): # this is nessesary since we can have processes with not unique name like "Google Chrome"
                cpuDict[s[1]] += float(s[0])
            else:
                cpuDict[s[1]] = float(s[0])
                howMany -= 1


            if howMany == 0: # means we already gathered top 5 proceses with unique name!
                break

        howMany = self.howMany
        
        for line in outMem.split("\n")[1:]: #ommiting shit
            s = line.split(None, 1) # btw how to not pass a separator (use default separator == any whitespace) and split with max split? Any ideas? "\s" separator doesn't seem to work
            if memDict.has_key(s[1]): # this is nessesary since we can have processes with not unique name like "Google Chrome"
                memDict[s[1]] += float(s[0])
            else:
                memDict[s[1]] = float(s[0])
                howMany -= 1

            if howMany == 0: # means we already gathered top 5 proceses with unique name!
                break

        memList = []
        cpuList = []

        for process in cpuDict:
            if self.prevCpuDict.has_key(process):
                if cpuDict[process] > self.prevCpuDict[process]:
                    tendency = 1
                elif cpuDict[process] == self.prevCpuDict[process]:
                    tendency = 0
                elif cpuDict[process] < self.prevCpuDict[process]:
                    tendency = -1
            else:
                tendency = 1   


            cpuList.append({
                            "process": process,
                            "value": cpuDict[process],
                            "tendency": tendency,
                            })

        self.prevCpuDict = cpuDict

        for process in memDict:
            if self.prevMemDict.has_key(process):
                if memDict[process] > self.prevMemDict[process]:
                    tendency = 1
                elif memDict[process] == self.prevMemDict[process]:
                    tendency = 0
                elif memDict[process] < self.prevMemDict[process]:
                    tendency = -1
            else:
                tendency = 1   
            memList.append({
                            "process": process,
                            "value": memDict[process],
                            "tendency": 0,
                            })
        self.prevMemDict = memDict
        

            
        return {
                "cpuList": cpuList,
                "memList": memList,
                }




