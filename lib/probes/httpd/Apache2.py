import os
from datetime import datetime,timedelta

class Apache2(object):

    def __init__(self, options):
        if not options: options = {}

        if 'log_path' in options:
            self.logPath = options['log_path']
        else:
            # No log path given, we test a couple sane defaults
            # to see if we can handle this ourselves.
            possible_paths = [
                '/var/log/apache2/access.log',
                '/var/log/apache2/access_log'
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    print "Found an Apache2 log file in %s" % (path,) 
                    self.logPath = path

        self.lastSize = 0
        self.retNone = {"transfer": 0,
                        "requests": 0,
                        }

    def report(self, interval=5):
        delta = timedelta(seconds = interval)
        currSize = os.path.getsize(self.logPath)
        if self.lastSize != currSize:
            log = open(self.logPath)
            log.seek(self.lastSize,0) # i dont care, i love it, i love it
            self.lastSize = currSize
            currentDateTime = datetime.now()
            limiter = currentDateTime - delta

            while True:
                line = log.readline()[:-1]
                #print "#" + line + "#"
                if line == "":
                    #print "just oldies here."
                    return self.retNone
                logLineDate = line.split('"')[0].replace("]","[").split("[")[1] # [*]
                logDateTime = datetime.strptime(logLineDate[0:-6], "%d/%b/%Y:%H:%M:%S") # [*] [*]
                if logDateTime < limiter:
                    continue
                else:
                    log.seek(-1*len(line)-1,1) # omitted one important line!
                    break


            requests = 0
            transfer = 0
            ips = {} 
            for line in log:
                requests += 1
                splitted = line.split('"')
                print splitted
                ipDateMesh = splitted[0]
                getLinkMesh = splitted[1]
                code, size = splitted[2].split()
                if size != "-":
                    transfer += int(size)
                #fromLink = splitted[3] # it's optional!
                #splitted[4] # is always blank
                #browser = splitted[5]
                ipDateMesh = ipDateMesh.replace("]","[")
                asdf = ipDateMesh.split("[")
                date = asdf[1]
                ip,meta0,meta1 = asdf[0].split()
                if  ips.has_key(ip):
                    ips[ip] += 1
                else:
                    ips[ip] = 1
                header, link, protocol = splitted[1].split()
                code, size = splitted[2].split()
                # sure, we have a lot of info, lets leave them for next features. 
        
            log.close()
            
            return {"transfer":transfer,
                    "requests":requests,
                    "ips": ips,
                    }
        else:
            return self.retNone
