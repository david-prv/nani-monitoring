#! /usr/bin/env python3

import smtplib
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
        try:
            self._smtp =  smtplib.SMTP(config('SMTP_SERVER'), config('SMTP_PORT'))
        except Exception as err:
            Exception(err)
    
    def sendEmail(self, status, content, receiver):
        body = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(self._sender, receiver, status, content)

        print(f"{self._sender} -> {receiver}: [{status}] {content}")

        try:
            mail = self._smtp
            mail.ehlo()
            mail.starttls()
            mail.login(self._sender, self._secret)
            mail.sendmail(self._sender, receiver, body)
            mail.close()
        except Exception as err:
            Exception(err)
