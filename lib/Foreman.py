import time
import os
import sys
from multiprocessing import Process
from probes.osx import MemInfo
from probes.osx import LoadAvg

class Foreman(object):
    
    def __init__(self, diary):
        self.diary = diary
        self.probes = {}
        self.worker_ps = None

    def load_probes(self, probe_list):
        for probe in probe_list:
            os_name, stat_name = probe.split('.')
            # This isn't perfect: we're importing the OS-representing
            # module too many times. Will do for now.
            mod = __import__('probes.' + os_name, fromlist=[stat_name])
            klass = getattr(mod, stat_name)
            self.probes[stat_name] = klass()

        print self.probes

    def start(self):
        print "[&] Foreman.start() in %s." % (os.getpid(),)
        self.worker_ps = Process(target=self.run)
        self.worker_ps.start()

    def stop(self):
        print "[!] Telling the foreman to take a break.."
        self.worker_ps.terminate()
        self.worker_ps.join()

    def run(self):
        print "[&] Foreman run(): %s." % (os.getpid(),)
        while True:
            self.probe_system()
            time.sleep(2)

    def probe_system(self):
        probe_time = int(time.time())
        #print "[*] Probing system, probe time: %s" % (time.ctime(probe_time))
        
        self.diary.write_load(self.probes['LoadAvg'].report())
        self.diary.write_mem_info(self.probes['MemInfo'].report())
