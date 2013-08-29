from datetime import datetime,timedelta

class Apache2(object):

    def __init__(self, path = "/var/log/apache2/access.log"):
        self.logPath = path

    def report(self, interval=5):
        delta = timedelta(seconds = interval)
        log = open(self.logPath, "r") #try catch?
        currentDateTime = datetime.now()
        limiter = currentDateTime - delta

        retNone = {"transfer": 0,
                    "requests": 0,
                    }

        while True:
            line = log.readline()
            if line == "":
                return retNone
            logLineDate = line.split('"')[0].replace("]","[").split("[")[1] # [*]
            logDateTime = datetime.strptime(logLineDate[0:-6], "%d/%b/%Y:%H:%M:%S") # [*] [*]
            if logDateTime < limiter:
                continue
            else:
                break
        #so we ommited outdated log lines
        if not log:
            return retNone

        requests = 0
        transfer = 0
        for line in log:
            requests += 1
            splitted = line.split('"')
            ipDateMesh = splitted[0]
            getLinkMesh = splitted[1]
            code, size = splitted[2].split()
            if size != "-":
                transfer += int(size)
            fromLink = splitted[3] # it's optional!
            splitted[4] # is always blank
            browser = splitted[5]
            ipDateMesh = ipDateMesh.replace("]","[")
            asdf = ipDateMesh.split("[")
            date = asdf[1]
            ip,meta0,meta1 = asdf[0].split()
            header, link, protocol = splitted[1].split()
            code, size = splitted[2].split()
            # sure, we have a lot of info, lets leave them for next features. 

        return {"transfer":transfer,
                "requests":requests,
                }
