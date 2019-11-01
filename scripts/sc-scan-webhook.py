#!/usr/bin/env python3
# encoding: utf-8

import sys
import re
import time
import socket
import requests
import json
import calendar

from datetime import date
from tenable.sc import TenableSC

class SC2Webhook():

    def __init__(self):
        self.ip = '<IP>'
        self.login = '<username>'
        self.password = '<password>'
        self.policyID = 'policy ID>'
        self.credentialID = '<credential ID>'
        self.repository = '<repo ID>'
        self.reportID = '<report ID>'
        self.email_on_launch = 'false'
        self.email_on_complete = 'false'
        self.URL = '<webhook URL>'

    def run(self):
        if len (sys.argv) != 3:
            print ("Usage: python2 sc-scan-webhook.py [scan ID] 'target list to add to message text sent in webhook'")
            sys.exit(1)

        scanID = sys.argv[1]
        if ScanID == "test":
            sys.exit()
        targetTXT = sys.argv[2]

        try:
            sc = TenableSC(self.ip)

            print ("Logging in to SecurityCenter")
            response = sc.login(self.login, self.password)

            targets = targetTXT
            print ('targets set: ' + targets)

            results =  self.run_scan(sc, targets, scanID)

            sc.logout()

        except Exception as ex:
            print ('Error: ' + str(ex))

    def run_scan(self, sc, targets, scanID):
        print ("Launching Scan " + scanID)
        running = sc.scans.launch(int(scanID))

        print('The Scan Result ID is {}'.format(
            running['scanResult']['id']))
        resultID = running['scanResult']['id']

        print ('Sending message to Google Chat Room')
        message = {'text': "This is an automated message from SecurityCenter. As per the vulnerability scanning schedule, automated scans of *" + targets + "*  has now begun (*scan ID =  " + resultID + "*). As always, we don't expect any service issues but if you do see something which you feel is as a result, then please reply to this message to let the InfoSec team know. \n\nAnother message will be sent to this room when this scan is complete."}
        requests.post(self.URL, data = json.dumps(message))

#       print ('targets still: ' + targets)
        return self.get_scan_results(sc, resultID, targets)

    def get_scan_results(self, sc, resultID, targets):
        results = {}
        while True:
            results = sc.scan_instances.details(int(resultID))
            running = (results['running'].lower() == 'true')
            status = results['status'].lower()
            print (status)
            if (not running and status == 'completed'):
                message = {'text': "This is an automated message from SecurityCenter to let you know that the vulnerability scanning of all *" + targets + "* (*scan ID =  " + resultID + "*) has completed for today."}
                print ('Sending scan finished to Google Chat group')
                requests.post(self.URL, data = json.dumps(message))
                break
            elif (status == 'error'):
                self.error("Error: " + results['errorDetails'])
            time.sleep(60)

        print (running)
        print (status)

if __name__ == '__main__':
    SC2Webhook().run()
