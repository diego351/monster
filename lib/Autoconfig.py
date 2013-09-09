import ConfigParser
import sys
import subprocess
from termcolor import cprint
import os


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
            "requirements": [],  # means it's totally independent
            "modules":  ["os", "datetime"],
            "defaults": {
                "log_file": [
                    "/var/log/apache2/access.log",
                    "/var/log/apache2/access_log",
                ]
            }
        },

        'apache2': {
            "probe": "httpd.Apache2",
            "requirements": [],
            "modules":  ["os", "datetime", "requests"],
            "defaults": {
                "log_file": [
                    "/var/log/apache2/access.log",
                    "/var/log/apache2/access_log",
                ]
            }
        },

        'nginx': {
            "probe": "httpd.Nginx",
            "requirements": [],
            "modules":  ["os", "datetime"],
            "defaults": {
                "log_file": [
                    "/var/log/apache2/access.log",
                ]
            }
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
    mod_to_pip = {
        "MySQLdb": "mysql-python",
        "psycopg2": "psycopg2",
                    "requests": "requests",
    }

    ps_out = subprocess.check_output(['ps', '-A'])
    for ps_line in ps_out.split("\n"):
        for suspect in suspects:
            if ps_line.find(suspect) != -1:
                probe_name = suspects[suspect]["probe"]
                cprint("[+] Found %s. Loading the %s probe.." %
                       (suspect, probe_name))

                for mod in suspects[suspect]["modules"]:
                 # check whether mod is importable
                    try:
                        __import__(mod)
                    except ImportError:
                        cprint(
                            "Seems like %s library is missing. How about 'pip install %s'?" %
                            (mod, mod_to_pip[mod]), "red")

                config.set('probes', probe_name, None)
                # for one probe one section in config file
                config.add_section(probe_name)

                # first of all we want to check whether we can help user
                # somehow
                if "defaults" in suspects[suspect]:
                    for defa in suspects[suspect]["defaults"]:
                        luck = False
                        if "log_file" in defa:
                            # this default setting has for sure something in
                            # common with log files, lets find them
                            for f in suspects[suspect]["defaults"]["log_file"]:
                                if os.path.exists(f):
                                    # WE FOUND LOG IN A HOPELESS PLACE
                                    found = f
                                    luck = True
                                    break

                        if luck:
                            cprint("I found an %s log file at %s" %
                                   (probe_name, found), "green")
                            while True:
                                cprint(
                                    "Do you want to save it as %s default log file? [Y/n]" % (probe_name), "green")
                                choice = raw_input()
                                if 'Y' in choice or 'y' in choice or choice == "" and not ('N' in choice or 'n' in choice):
                                    # we keep it
                                    break
                                if 'N' in choice or 'n' in choice and not ('Y' in choice or 'y' in choice):
                                    luck = False
                                    break
                        if luck:  # if still luck
                            # like apache2,log_file,/var/..
                            config.set(probe_name, defa, found)
                        else:
                            cprint(
                                "Write then your own log file path below:", "green")
                            path = raw_input()
                            config.set(probe_name, defa, path)

                # If theres no requirements, it's not gonna be executed, I
                # believe
                for req in suspects[suspect]["requirements"]:
                    cprint(prompts[req], "cyan")  # print proper prompt
                    raw = raw_input()
                    config.set(probe_name, req, raw)  # how about encoding?
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
