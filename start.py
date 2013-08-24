import sys
import os
import signal
import config

sys.path.append('lib')

from Artist import Artist
from Foreman import Foreman
from Diary import DiaryManager

try:
    diary_manager = DiaryManager()
    diary_manager.start()
    diary = diary_manager.Diary()

    foreman = Foreman(diary)
    foreman.load_probes(config.probes)
    foreman.start()

    artist = Artist(diary)
    artist.start()

    print "[-] We're PID %s." % (os.getpid(),)
    print "[-] All done, running. Ctrl-C to exit."
    signal.pause()

except KeyboardInterrupt:
    print

    artist.stop()
    foreman.stop()

    print "[*] Exiting cleanly... was it good for you?"
    exit()
