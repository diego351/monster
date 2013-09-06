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
        print "[+] You're on OS X. Enabling LoadAvg, MemInfo and HeavyProcessStat probes."
        config.set('probes', 'osx.LoadAvg', None)
        config.set('probes', 'osx.MemInfo', None)
        config.set('probes', 'osx.HeavyProcessStat', None)
    elif sys.platform == 'linux2':
        print "[+] You're on some flavor of Linux. Enabling LoadAvg, MemInfo and HeavyProcessStat probes."
        config.set('probes', 'linux.LoadAvg', None)
        config.set('probes', 'linux.MemInfo', None)
        config.set('probes', 'linux.HeavyProcessStat', None)
    else:
        cprint("Are you running this on a refrigerator?", "red")
        return False

    
    # Let's find some running services
    prompts = {
                "username": "Gimme username below:",
                "password": "Gimme password below:",
                "database": "Gimme database name below:",
            }
    # It's going to be flexible like niggas pants
    suspects = {
        'httpd': {
                    "probe": "httpd.Apache2",
                    "requirements": [], # means it's totally independent
                    "modules":  ["os", "datetime"],
                },
                
        'apache2': {
                    "probe": "httpd.Apache2",
                    "requirements": [],
                    "modules":  ["os", "datetime"],
                },

        'nginx': {
                    "probe": "httpd.Nginx",
                    "requirements": [],
                     "modules":  ["os", "datetime"],
                },
                
        'postgres': {
                    "probe": "db.Postgres",
                    "requirements":  ["username", "password", "db"],
                    "modules":  ["psycopg2"],
                },
        'mysql': {
                    "probe": "db.MySQL",
                    "requirements": ["username", "password"],
                    "modules":  ["MySQLdb"],
                },
             }

    ps_out = subprocess.check_output(['ps', '-A'])
    for ps_line in ps_out.split("\n"):
        for suspect in suspects:
            if ps_line.find(suspect) != -1:
                probe_name = suspects[suspect]["probe"]
                cprint("[+] Found %s. Loading the %s probe.." % (suspect, probe_name))

                for mod in suspects[suspect]["modules"]:
                 # check whether mod is importable
                    try:
                        __import__(mod)
                    except ImportError:
                        cprint("Seems like %s library is missing. How about 'pip install %s'?" %(mod,mod),"red")



                config.set('probes', probe_name, None)
                if  suspects[suspect]["requirements"]:
                    config.add_section(probe_name) # if requirements list isn't empty
                for req in suspects[suspect]["requirements"]: # If theres no requirements, it's not gonna be executed, I believe
                    cprint(prompts[req], "cyan") # print proper prompt
                    raw = raw_input()
                    config.set(probe_name, req, raw) # how about encoding?
                    # THIS IS PERFECT PLACE TO PRECHECK PROBE CONFIGURATION



                


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
