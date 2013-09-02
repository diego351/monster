#!/usr/bin/env python

import ConfigParser
import os
import signal
import sys
from termcolor import cprint 

sys.path.append('lib')

from Artist import Artist
from Foreman import Foreman
from Diary import DiaryManager

try:
    # Read config file.
    config = ConfigParser.ConfigParser(allow_no_value=True)
    # Without the following, ConfigParser screws up, converting option 
    # name to lowercase.. we need them to preserve case, because we
    # look for sections based on the names in [probes]
    config.optionxform = str
    config.read('config.cfg')

    diary_manager = DiaryManager()
    diary_manager.start()
    diary = diary_manager.Diary()

    foreman = Foreman(diary)
    foreman.load_probes(config)
    foreman.start()

    artist = Artist(diary, config)
    artist.start()

    cprint("[-] We're PID %s." % (os.getpid(),), "cyan")
    cprint("[-] All done, running. Ctrl-C to exit.", "magenta")
    signal.pause()

except KeyboardInterrupt:
    print

    artist.stop()
    foreman.stop()

    cprint("[*] Exiting cleanly... was it good for you?", "magenta")
    exit()
