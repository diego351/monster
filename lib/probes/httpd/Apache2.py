import os
from termcolor import cprint
from datetime import datetime, timedelta
from urllib2 import urlopen
import json


class Apache2(object):

    def __init__(self, options):

        log_path_list = [
            "/var/log/apache2/access.log",
            "/var/log/apache2/access_log",
            "/var/log/httpd/access_log",
        ]
        if 'log_file' in options:
            self.logPath = options['log_file']
        else:
            for log in log_path_list:
                if os.path.exists(log):
                    self.logPath = log
                    cprint(
                        "You didn't add Apache2 log file in your config file, but fortunately Apache2 probe figured it out on themself!", "red")

        self.lastSize = 0
        self.retNone = {
            "transfer": 0,
            "requests": 0,
            "ips": [],
        }
        self.ip_to_geo = {}

    def report(self, interval=5):
        delta = timedelta(seconds=interval)
        currSize = os.path.getsize(self.logPath)
        if self.lastSize != currSize:
            log = open(self.logPath)
            log.seek(self.lastSize, 0)  # i dont care, i love it, i love it
            self.lastSize = currSize
            currentDateTime = datetime.now()
            limiter = currentDateTime - delta

            while True:
                line = log.readline()[:-1]
                # print "#" + line + "#"
                if line == "":
                    # print "just oldies here."
                    return self.retNone
                logLineDate = line.split('"')[
                    0].replace("]", "[").split("[")[1]  # [*]
                logDateTime = datetime.strptime(
                    logLineDate[0:-6], "%d/%b/%Y:%H:%M:%S")  # [*] [*]
                if logDateTime < limiter:
                    continue
                else:
                    # omitted one important line!
                    log.seek(-1 * len(line) - 1, 1)
                    break

            requests = 0
            transfer = 0
            ips = {}
            for line in log:
                requests += 1
                splitted = line.split('"')
                #print splitted
                ipDateMesh = splitted[0]
                getLinkMesh = splitted[1]
                code, size = splitted[2].split()
                if size != "-":
                    transfer += int(size)
                # fromLink = splitted[3] # it's optional!
                # splitted[4] # is always blank
                #browser = splitted[5]
                ipDateMesh = ipDateMesh.replace("]", "[")
                asdf = ipDateMesh.split("[")
                date = asdf[1]
                ip, meta0, meta1 = asdf[0].split()
                if ip in ips:
                    ips[ip] += 1
                else:
                    ips[ip] = 1
                #header, link, protocol = splitted[1].split()
                #code, size = splitted[2].split()
                # sure, we have a lot of info, lets leave them for next
                # features.

            log.close()
            # gathered all data from

            for ip in ips:
                if ":" in ip:
                    print "ipv6 still out of support"
                    continue

                if ip not in self.ip_to_geo:
                    link = "http://freegeoip.net/json/%s" % (ip)
                    dzejson = urlopen(link).read()
                    foo = json.loads(dzejson)
                    self.ip_to_geo[ip] = {
                        "longitude": float(foo["longitude"]),
                        "latitude": float(foo["latitude"]),
                        "number": int(ips[ip]),
                        "ip": ip,
                    }
            #
            a = []
            for ip in ips:
                a.append(self.ip_to_geo[ip])

            return {
                "transfer": transfer,
                "requests": requests,
                "ips": a,
            }

        else:
            return self.retNone
