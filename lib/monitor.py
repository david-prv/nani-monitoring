#! /usr/bin/env python3

import smtplib
import requests
import socket
from decouple import config

"""
Class Emailer:

This class is a short wrapper for smtplib
email clients. We adjusted it for our purposes.
It is not generalized.
"""
class Emailer:
    def __init__(self, sender, secret):
        self._sender = sender
        self._secret = secret
    
    def sendEmail(self, status, content, receiver):
        body = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(self._sender, receiver, status, content)

        print(f"{self._sender} -> {receiver}: [{status}] {content}")

        try:
            mail = smtplib.SMTP(config('SMTP_SERVER'), config('SMTP_PORT'))
            mail.ehlo()
            mail.starttls()
            mail.login(self._sender, self._secret)
            mail.sendmail(self._sender, receiver, body)
            mail.close()
        except Exception as err:
            print(f"Error! Could not send email: {err}")

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

    def frontend_checker(self):
        # this subroutine tries to connect to one of
        # our web pages
        sess = requests.Session()
        addr = self.findHostByLabel("Frontend")
        try:
            r = sess.get(addr)
            return "Maintenance" not in r.text
        except Exception as err:
            self.errCollection['Frontend'] = err
            return False
    
    def backend_checker(self):
        # only check if the server
        # does still respond to sockets. If not: we assume that
        # the server has run into internal errors.
        ip = self.findHostByLabel("Backend")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            location = (ip, 22)
            r = s.connect_ex(location)
            return r == 0
        except Exception as err:
            self.errCollection['Backend'] = err
            return False

    def mc_checker(self, index):
        # uses the mcsrvstat.us api v2 and checks
        # for the only state
        hostname = self.getHostName(index)
        label = self.getLabel(index)
        sess = requests.Session()
        try:
            r = sess.get(f"https://api.mcsrvstat.us/2/{hostname}")
            return '"online":false' not in r.text
        except Exception as err:
            self.errCollection[label] = err
            return False

    def ts_checker(self, index):
        # uses the cleanvoice.ru api, queries the hostname
        # and checks for errors. If no error occurs: server is offline
        hostname = self.getHostName(index)
        label = self.getLabel(index)
        sess = requests.Session()
        try:
            r = sess.get(f"https://api.cleanvoice.ru/ts3/?address={hostname}&ext=false")
            return '"error"' not in r.text
        except Exception as err:
            self.errCollection[label] = err
            return False

    def db_checker(self):
        # TODO
        pass

    def smtp_checker(self):
        # TODO
        pass

    def dns_checker(self, index):
        # TODO
        pass

    def getMessage(self, key):
        if key in self.errCollection.keys():
            return self.errCollection[key]
        else:
            return ""

    def getHostName(self, index):
        try:
            return self.hostnames[index]['hostname']
        except KeyError as err:
            print(f"Error! {err}")


    def getLabel(self, index):
        try:
            return self.hostnames[index]['label']
        except KeyError as err:
            print(f"Error! {err}")

    def findHostByLabel(self, label):
        for i in range(len(self.hostnames)):
            if label in self.hostnames[i].values():
                return self.hostnames[i]['hostname']
            else:
                Exception("No host could be found")

    def findLabelByHost(self, host):
        for i in range(len(self.hostnames)):
            if host in self.hostnames[i].keys():
                return self.hostnames[i]['label']
            else:
                Exception("No label could be found")

    def runAll(self):
        # Initialize mail client
        mailClient = Emailer(config('SENDER'), config('SECRET'))

        # Run tests
        try: 
            mailClient.sendEmail("UP" if self.frontend_checker() == True else "DOWN", self.getMessage('Frontend'), self.components['Frontend'])
            mailClient.sendEmail("UP" if self.backend_checker() == True else "DOWN", self.getMessage('Backend'), self.components['Backend'])
            mailClient.sendEmail("UP" if self.mc_checker(0) == True else "DOWN", self.getMessage('Minecraft-001'), self.components['Minecraft-001'])
            mailClient.sendEmail("UP" if self.mc_checker(1) == True else "DOWN", self.getMessage('Minecraft-002'), self.components['Minecraft-002'])
            mailClient.sendEmail("UP" if self.ts_checker(2) == True else "DOWN", self.getMessage('Teamspeak-001'), self.components['Teamspeak-001'])
            # mailClient.sendEmail("UP" if self.db_checker() == True else "DOWN", self.getMessage('Database'), self.components['Database'])
            # mailClient.sendEmail("UP" if self.smtp_checker() == True else "DOWN", self.getMessage('External SMTP'), self.components['External SMTP'])
            # mailClient.sendEmail("UP" if self.dns_checker(3) == True else "DOWN", self.getMessage('External DNS 1'), self.components['External DNS 1'])
            # mailClient.sendEmail("UP" if self.dns_checker(4) == True else "DOWN", self.getMessage('External DNS 2'), self.components['External DNS 2'])
        except Exception as err:
            print(f"Error! {err}")