import time
import os
import sys
from multiprocessing import Process
from termcolor import cprint

from probes.osx import MemInfo
from probes.osx import LoadAvg


class Foreman(object):

    def __init__(self, diary, args):
        self.args = args
        self.diary = diary
        self.probes = {}
        self.worker_ps = None

    def load_probes(self, config):
        for probe in config.options('probes'):
            os_name, stat_name = probe.split('.')
            # This isn't perfect: we're importing the OS-representing
            # module too many times. Will do for now.
            mod = __import__('probes.' + os_name, fromlist=[stat_name])
            klass = getattr(mod, stat_name)
            # We check if this probe has a config section.
            # If it does, we turn it into a dict and pass to the
            # probe's constructor so it can deal with it.
            if probe in config.sections():
                probe_opts = dict(config.items(probe))
            else:
                probe_opts = {}

            try:
                self.probes[stat_name] = klass(probe_opts)
                print "[*] %s loaded and ready." % (probe,)
            except Exception as e:

                cprint(
                    "[x] Looks like you lack some prerequisites to run %s:" %
                    (probe,), "yellow")
                print str(e)

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
            time.sleep(self.args['interval'])

    def probe_system(self):
        probe_time = int(time.time())
        # Note: remember about .iter() vs .iteritems()
        for probe_name, probe_obj in self.probes.iteritems():
            # Signature follows .write("MemInfo", MemInfo.report())
            self.diary.write(probe_name, probe_obj.report())
