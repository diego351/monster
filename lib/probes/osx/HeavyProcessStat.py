import commands

class HeavyProcessStat(object):
    def __init__(self,options=None):
        if not options: options = {}

        if "proc_number" in options:
            self.howMany = int(options["proc_number"])
        else:
            self.howMany = 5

    def report(self):
        howMany = self.howMany
        proc = {}
        out = commands.getoutput("ps xrco %cpu,command") # -o for custom format, -r for cpu sorting, -c for just process name (not full path, -x for all processes)
        for line in out.split("\n")[1:]: #ommiting shit
            s = line.split(" ", 3) # btw how to not pass a separator (use default separator == any whitespace) and split with max split? Any ideas? "\s" separator doesn't seem to work
            if proc.has_key(s[3]): # this is nessesary since we can have processes with not unique name like "Google Chrome"
                proc[s[3]] += float(s[2])
            else:
                proc[s[3]] = float(s[2])
                howMany -= 1

            if howMany == 0: # means we already gathered top 5 proceses with unique name!
                break

        return proc




