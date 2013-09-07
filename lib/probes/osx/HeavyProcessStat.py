import commands

class HeavyProcessStat(object):
    def __init__(self,options):
        if "proc_number" in options:
            self.howMany = int(options["proc_number"])
        else:
            self.howMany = 5

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
            cpuList.append({"process": process})
            cpuList.append({"value": cpuDict[process]})
            cpu.List.append({"tendency": 0})

        for process in memDict:
            memList.append({"process": process})
            memList.append({"value": memDict[process]})
            memList.append({"tendency": 0})
        

            
        return {
                "cpuList": cpuList,
                "memList": memList,
                }




