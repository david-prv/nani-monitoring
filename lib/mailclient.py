#! /usr/bin/env python3

from pickletools import optimize
import smtplib
from decouple import config
from colorama import Fore
from colorama import Style 

"""
Class Emailer:

This class is a short wrapper for smtplib
email clients. We adjusted it for our purposes.
It is not generalized.
"""
class Emailer:
    def __init__(self, sender, secret, suppress):
        self._sender = sender
        self._secret = secret
        self.suppress = suppress
        self.error = 0
    
    def sendEmail(self, status, content, receiver):
        body = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(self._sender, receiver, status, content)

        try:
            smtp = smtplib.SMTP(config('SMTP_SERVER'), config('SMTP_PORT'))
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self._sender, self._secret)
            if not self.suppress:
                smtp.sendmail(self._sender, receiver, body)
            print(("[Suppressed] " if self.suppress else "") + f"{self._sender} -> {receiver}: [{Fore.GREEN if status == 'UP' else Fore.RED}{status}{Style.RESET_ALL}] {content}")
            smtp.close()
        except Exception as err:
            self.error = 1
            print(f"Error! {err}")
