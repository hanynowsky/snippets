#!/usr/bin/env python3
import subprocess
import os, sys, tempfile
from time import gmtime, strftime
from datetime import datetime

# Snippet authored by <hanynowsky@gmail.com>
# WARNING: Beware that when using ASYNC processing, you get no return code

# Name of our program
PROGRAM = 'UNIVERSE SCAVENGER V0.1'
# Path of log file
LOGFILE = '/tmp/log.log'
# Our system commands
commands = [['sleep','5'], ['df', '-lh'], ['du','-sh'], ['sleep', '10'], ['sleep', '10'], ['sleep','11']]
IS_ASYNC = True

def run_processes(cmds):
    """ Run system commands """
    # A void list of processes objects
    processes = []
    try:
        # Create our processes. Standard output is redirected to a temporary file 
        for cmd in cmds:
            f = tempfile.TemporaryFile()
            p = subprocess.Popen(cmd, stdout=f)
            processes.append((p, f))

        # Open the log file in 'append' mode
        logfile = open(LOGFILE,'a')

        # Execute processes simultaneously 
        for p, f in processes:
            launch_message = str(p.args) + ' launched at: '+ datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + ": " + str(p.args)
            logfile.write(launch_message)
            if IS_ASYNC:
                p.poll()
            else:
                p.wait()
            f.seek(0)
            message = "\n##########################################\n" + \
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + ": " + str(p.args) + \
                    ' PID/RCODE: ' + str(p.pid) + '/' + str(p.returncode) +"\n" + \
                    f.read().decode() + "\n"
            logfile.write(message)
            if f:
                f.close()
    except Exception as e:
        print(e)
    finally:
        print('Info logged to  %s' % LOGFILE)

# Run program
if __name__ == '__main__':
    print('Launching %s' % PROGRAM)
    run_processes(commands)
