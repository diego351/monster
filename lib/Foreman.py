import time
from multiprocessing import Process
from probes.osx import LoadAvg

class Foreman(object):
    
    def __init__(self, diary):
        self.diary = diary
        # Hardcoding some things for now.
        self.probes = {
            'LoadAvg': LoadAvg()        
        }

        self.worker_ps = None

    def arm_probe(self, probe_name):
        # I need to think this through, I'm falling asleep right now.
        os_name, stat_name = probe_name.split('.')
        self.probes[stat_name] = __import__('probes.' + probe_name).__call__()
        print "Loaded probe from config file: %s" % (probe_name,)
        print self.probes

    def start(self):
        self.worker_ps = Process(target=self.run)
        self.worker_ps.start()

    def stop(self):
        print "[!] Telling the foreman to take a break.."
        self.worker_ps.terminate()

    def run(self):
        while True:
            self.probe_system()
            time.sleep(1)

    def probe_system(self):
        probe_time = int(time.time())
        #print "[*] Probing system, probe time: %s" % (time.ctime(probe_time))
        
        self.diary.write_load(self.probes['LoadAvg'].report())
