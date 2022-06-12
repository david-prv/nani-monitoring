#! /usr/bin/env python3

import time
from decouple import config
from lib import argparser
from lib import monitor
from lib import collections

"""
runDaemon:

This function has the only purpose to assemble
all subroutines together and run them. It's the main
function of the whole monitoring service, so to say.
"""
def runDaemon():
    options = argparser.Argparser()
    options.parse()

    runner = monitor.Monitor(collections.COMPONENTS, collections.HOSTNAMES, options)
    while(True):
        runner.runAll()
        if options.repetitive: time.sleep(int(config('DELAY')))
        else: exit("Done.")

if __name__ == "__main__":
    runDaemon()
