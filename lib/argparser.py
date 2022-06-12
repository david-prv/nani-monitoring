#! /usr/bin/env python3

import sys

"""
Argparser Class:

This class will read commandline arguments, parse them,
and sets its own state corresponding to the provided args

Options:
    - ScriptName:       Changes with the actual filename. Standard is
                        path/to/file/app.py, which cannot be changed with commands

    - Repetitive:       Decides whether the monitor should run over and
                        over again, or stop after one iteration. Can be enabled
                        with --repetitive or -r

    - SuppressEmails:   Option to prevents emails to be sent. Useful
                        for development environments. Can be enabled with
                        --suppress-emails or -s

    - Turnus:           If repetitive mode is enabled, you can specifiy the turnus
                        in seconds by using --turnus <seconds> or -t <seconds> as
                        commandline argument. It will override the environment variable      

    - Help / Manual:    Shows manual page for this script. Use --help, -h or --manual, -m      
"""
class Argparser:
    def __init__(self):
        self.scriptName = ""
        self.repetitive = False
        self.suppressEmails = False
        self.turnus = None

    def manual(self):
        print('''
        Usage: app.py [options]
        
        Options:
            --repetitive, -t        Enable repetitive mode
            --suppress-emails, -s   Suppresses update emails to be sent
            --turnus <s>, -t <s>    Overrides turnus in seconds
            --help, -h              Shows this message and quits
        ''')
        exit()

    def parse(self):
        self.scriptName = sys.argv[0]

        for i in range(1, len(sys.argv)):
            cmd = sys.argv[i].lower()

            # repetitive
            if cmd == "--repetitive" or cmd == "-r":
                self.repetitive = True
            
            # suppress emails
            if cmd == "--suppress-emails" or cmd == "-s":
                self.suppressEmails = True

            if (cmd == "--help" or cmd == "-h" or
                cmd == "--manual" or cmd == "-m"):
                self.manual()

            # override turnus
            if cmd == "--turnus" or cmd == "-t":
                if i+1 <= (len(sys.argv) - 1):
                    seconds = int(sys.argv[i+1])
                    self.turnus = seconds
                    i += 1
                else:
                    self.manual()

