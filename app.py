#! /usr/bin/env python3

import time
from decouple import config
from lib import monitor
from lib import collections

"""
runDaemon:

This function has the only purpose to assemble
all subroutines together and run them. It's the main
function of the whole monitoring service, so to say.
"""
def runDaemon():
    runner = monitor.Monitor(collections.COMPONENTS, collections.HOSTNAMES)
    while(True):
        runner.runAll()
        time.sleep(int(config('DELAY')))

if __name__ == "__main__":
    runDaemon()