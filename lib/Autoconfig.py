import ConfigParser
import sys
import subprocess
from termcolor import cprint

def first_time():
    cprint("\n[#] First time? I'll be gentle. Let's see..", "white", "on_blue")

    # Let's start some mediocre autoconfig magic.
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.optionxform = str

    # Configure probes ..
    config.add_section('probes')
    
    # Enable Load & MemInfo probes, those should work everywhere.
    # Figure out OS from sys.platform
    # See: http://docs.python.org/2/library/sys.html#sys.platform
    if sys.platform == 'darwin':
        print "[+] You're on OS X. Enabling LoadAvg and MemInfo HeavyProcessStat probes.."
        config.set('probes', 'osx.LoadAvg', None)
        config.set('probes', 'osx.MemInfo', None)
        config.set('probes', 'osx.HeavyProcessStat', None)
    elif sys.platform == 'linux2':
        print "[+] You're on some flavor of Linux.. Enabling LoadAvg and MemInfo probes."
        config.set('probes', 'linux.LoadAvg', None)
        config.set('probes', 'linux.MemInfo', None)
        config.set('probes', 'linux.HeavyLoadStat', None)
    else:
        cprint("Are you running this on a refrigerator?", "red")
        return False

    # Let's find some running services.
    suspects = {
        'httpd': 'httpd.Apache2',
        'apache2': 'httpd.Apache2',
        'nginx': 'httpd.Nginx',
        'postgres': 'db.Postgres',
        'mysql': 'db.MySQL'
    }

    ps_out = subprocess.check_output(['ps', '-A'])
    for ps_line in ps_out.split("\n"):
        for suspect in suspects:
            if ps_line.find(suspect) != -1:
                probe_name = suspects[suspect]
                cprint("[+] Found %s. Loading the %s probe.." % (suspect, probe_name))
                config.set('probes', probe_name, None)

                # Remove the probe from `suspects` many services have multiple processes
                # and there's no need to go through this crap all over again.
                del(suspects[suspect])

                # Stop searching through this line, we got what we needed.
                break
   
    cprint("[*] Okay, autoconfig done. Hang in there.", "cyan")
    cprint("    (if I missed something, just edit the ./config.cfg file I created)\n") 

    try:
        config_file = open('config.cfg', 'wb') 
        config.write(config_file)
    except:
        cprint("[x] I tried, but couldn't write the config to a file.", "red")
        return False

    return True
