#! /usr/bin/env python3

import requests
import socket
import mysql.connector
from lib import mailclient
from lib import ping
from decouple import config

"""
Class Monitor:

Monitor is a collection of subroutines, which will perform
simple checking tasks like: Try socket connections, lookup
domain names via a specific DNS server, etc.
Their only purpose is to return a boolean indicating if a service might
be running or not.

Can be seen as a collection of blackbox unit tests.
"""
class Monitor:
    def __init__(self, components, hostnames):
        self.components = components
        self.hostnames = hostnames
        self.errCollection = {}
        self.session = requests.Session()

    def frontend_checker(self) -> bool:
        # this subroutine tries to connect to one of
        # our web pages
        try:
            addr = self.findHostByLabel("Frontend")
            r = self.session.get(addr)
            return "Maintenance" not in r.text
        except Exception as err:
            self.errCollection['Frontend'] = err
            return False
    
    def backend_checker(self) -> bool:
        # only check if the server
        # does still respond to sockets. If not: we assume that
        # the server has run into internal errors.
        try:
            ip = self.findHostByLabel("Backend")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            location = (ip, 22)
            r = s.connect_ex(location)
            return r == 0
        except Exception as err:
            self.errCollection['Backend'] = err
            return False

    def mc_checker(self, index) -> bool:
        # uses the mcsrvstat.us api v2 and checks
        # for the only state
        try:
            hostname = self.getHostName(index)
            label = self.getLabel(index)
            r = self.session.get(f"https://api.mcsrvstat.us/2/{hostname}")
            return '"online":false' not in r.text
        except Exception as err:
            self.errCollection[label] = err
            return False

    def ts_checker(self, index) -> bool:
        # uses the cleanvoice.ru api, queries the hostname
        # and checks for errors. If no error occurs: server is offline
        try:
            hostname = self.getHostName(index)
            label = self.getLabel(index)
            r = self.session.get(f"https://api.cleanvoice.ru/ts3/?address={hostname}&ext=false")
            return '"error"' not in r.text
        except Exception as err:
            self.errCollection[label] = err
            return False

    def db_checker(self) -> bool:
        # just try to connect to the server with correct
        # credentials, but do not expect to be successful,
        # just check if there's a timeout error (connection_timeout = 0.5s)
        # or a general connection error
        # (then, the server's offline or address unresolveable)
        try:
            mysql.connector.connect(
                host=config('SQL_HOST'),
                user=config('SQL_USER'),
                password=config('SQL_PASS'),
                connection_timeout=0.5
            )
        except Exception as err:
            error = f"{err}"
            if "(timed out)" not in error: self.errCollection["Database"] = err
            return "(timed out)" in error

    def smtp_checker(self, client) -> bool:
        # Checks for error stage in a SMTPLib
        # mailClient, passed by the runAll() function
        return client.error == 0

    def dns_checker(self, index) -> bool:
        # Calls ping util and tries to run a
        # hostsystem subprocess, called ping.
        # It will try to execute a ping command instruction
        try:
            hostname = self.getHostName(index)
            label = self.getLabel(index)
            return ping.ping(hostname)
        except Exception as err:
            self.errCollection[label] = err
            return False

    def getMessage(self, key) -> str:
        if key in self.errCollection.keys():
            return self.errCollection[key]
        else:
            return ""

    def getHostName(self, index) -> str:
        try:
            return self.hostnames[index]['hostname']
        except KeyError as err:
            Exception(err)


    def getLabel(self, index) -> str:
        try:
            return self.hostnames[index]['label']
        except KeyError as err:
            Exception(err)

    def findHostByLabel(self, label) -> str:
        for i in range(len(self.hostnames)):
            if label in self.hostnames[i].values():
                return self.hostnames[i]['hostname']
            else:
                Exception("No host could be found")

    def findLabelByHost(self, host) -> str:
        for i in range(len(self.hostnames)):
            if host in self.hostnames[i].keys():
                return self.hostnames[i]['label']
            else:
                Exception("No label could be found")

    def runAll(self) -> None:
        # Run tests
        try: 
            mailClient = mailclient.Emailer(config('SENDER'), config('SECRET'))
            if self.smtp_checker(mailClient): mailClient.sendEmail("UP", self.getMessage('External SMTP'), self.components['External SMTP'])
            else: Exception("Could not establish SMTP connection!")
            mailClient.sendEmail("UP" if self.frontend_checker() == True else "DOWN", self.getMessage('Frontend'), self.components['Frontend'])
            mailClient.sendEmail("UP" if self.backend_checker() == True else "DOWN", self.getMessage('Backend'), self.components['Backend'])
            mailClient.sendEmail("UP" if self.mc_checker(0) == True else "DOWN", self.getMessage('Minecraft-001'), self.components['Minecraft-001'])
            mailClient.sendEmail("UP" if self.mc_checker(1) == True else "DOWN", self.getMessage('Minecraft-002'), self.components['Minecraft-002'])
            mailClient.sendEmail("UP" if self.ts_checker(2) == True else "DOWN", self.getMessage('Teamspeak-001'), self.components['Teamspeak-001'])
            mailClient.sendEmail("UP" if self.db_checker() == True else "DOWN", self.getMessage('Database'), self.components['Database'])
            mailClient.sendEmail("UP" if self.dns_checker(3) == True else "DOWN", self.getMessage('External DNS 1'), self.components['External DNS 1'])
            mailClient.sendEmail("UP" if self.dns_checker(4) == True else "DOWN", self.getMessage('External DNS 2'), self.components['External DNS 2'])
        except Exception as err:
            print(f"Error! {err}")
