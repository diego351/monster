import sys
import signal

sys.path.append('lib')

from Artist import Artist
from Foreman import Foreman
from Diary import Diary

try:
    diary = Diary()
    diary.start()

    foreman = Foreman(diary)
    foreman.start()

    artist = Artist(diary)
    artist.start()

    print "[-] All done, running. Ctrl-C to exit."

    signal.pause()

except KeyboardInterrupt:
    print

    artist.stop()
    foreman.stop()
    diary.stop()

    print "[*] Exiting cleanly... was it good for you?"
    exit()
