import time
from multiprocessing import Process
from probes.LoadAvg import LoadAvg

class Foreman(object):
    
    def __init__(self, diary):
        self.diary = diary
        # Hardcoding some things for now.
        self.probes = {
            'LoadAvg': LoadAvg()        
        }

        self.worker_ps = None

    def start(self):
        self.worker_ps = Process(target=self.run)
        self.worker_ps.start()

    def stop(self):
        print "[!] Telling the foreman to take a break.."
        self.worker_ps.terminate()

    def run(self):
        while True:
            self.probe_system()
            time.sleep(2)

    def probe_system(self):
        probe_time = int(time.time())
        print "[*] Probing system, probe time: %s" % (time.ctime(probe_time))
        
        self.diary.write_load(self.probes['LoadAvg'].report())
