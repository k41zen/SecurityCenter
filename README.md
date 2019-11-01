
[![Build Status](https://travis-ci.com/k41zen/SecurityCenter.svg?branch=master)](https://travis-ci.com/k41zen/SecurityCenter)![GitHub](https://img.shields.io/github/languages/code-size/k41zen/SecurityCenter)![GitHub](https://img.shields.io/github/last-commit/k41zen/SecurityCenter)![GitHub](https://img.shields.io/maintenance/yes/2019)![github](https://img.shields.io/github/license/k41zen/SecurityCenter)

# Introduction

Here are a couple of scripts I've quickly knocked up (so to speak) to help me with building on the awesome job that Tenable's SecurityCenter does, but improve on it limitations.

The first script (*sc-scan-webhook*) allows you to take your manual scanning schedule and fully automate those scans using cron. Why not just use the scan schedule option in SecurityCenter I hear you ask? Well, I needed the ability to be able to notify people (teams that monitor Production systems) that planned vulnerability scans are taking place and not to raise any system alerts. And, at the time of writing this, SecurityCenter can only send email notifications. I needed something to send a message to a chat room. I needed webhooks.

The script sends a custom webhook chat message, starts a scan, monitors that scan and when finished and complete sends another webhook chat message saying the scan has completed.

The second script (*sc-getrunning*) fills another feature hole in SecurityCenter by showing you scans which have a "running" state. At the time of writing this, SecurityCenter can't do this outside of the GUI. In fact, it can't do this on the built in SecurityCenter dashboards either so you have to grant more privileges to be able to let people see this information. The plan is to integrate this script with a bot in the chat room somehow to allow people to ask the bot to show them what scanning jobs are running.

## Tested with
This has been tested using pyTenable 0.3.27 and Tenable's SecurityCenter 5.11.x.

## Introduction
Once downloaded, install the dependencies needed for this script, run the following command:

	pip install -r requirements.txt

## Deployment
Both scripts utilise the TenableSC API wrapper to run as shown in the code snippet below:

```python
	from tenable.sc import TenableSC
```

More information on this API wrapper can be found here: https://pytenable.readthedocs.io/en/stable/sc.html

## sc-scan-webhook
This script allows you to start predefined scans with Tenable's Security through the API, send a webhook notification message to a Google chat room, monitor for the scan to complete successfully and then sends another webhook notification message stating the scan is complete.

### Configuration
Before you can begin to run this script there's some information you need to provide it. This is information which is specific to you and your environment and you can find this in the init section of the script as shown below:

``` python
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
```

The field *self.ip* is the IP address of your SecurityCenter instance. The *self.login* and *self.password* field are for the user which authenticates to SecurityCenter to run the scans. I've created a "scan-automation" user within SecurityCenter for auditing purposes but feel free to choose which ever user you wish.

The field *self.policyID* is the ID for the policy which your scan is already configured to use in SecurityCenter. Find the scan you wish to run, then on the settings tab note the name of the policy selected. Then find this policy under the Policies tab and click view to see its ID value. This is the value you need to set self.policyID to.

The field *self.credentialID* is the credential which the policy has been configured to use.

The field *self.repositoryID* is the repo ID value which your SecurityCenter instance is using.

The fields *self.reportID*, *self.email_on_launch* and *self.email_on_complete* are all optional fields which I've left here for future updates to the script.

The final field *self.URL* is the webhook URL of the chat room where the messages will be sent at the start of our scans and when they have completed.

### Usage
Once this information has been provided you're ready to run the script. The script needs 2 command line arguments to run. The first is the ID of the scan in SecurityCenter that you want the script to run. The second argument is the target text which will be used to send the message to the chat room to let people know what targets are being scanned.

Here's an example:

	# python3 sc-scan-webhook  1889      "Linux Servers (Group C) in both the PDC and SDC"
	           [script name]   [ID]                   [target text]

Here's a screenshot of an example webhook message sent at the start of the scan to a Google Chat room:

![alt test](images/sc-scan-webhook-start-scan.png)

Here's a screenshot of an example webhook message sent when the scan has completed successfully:

![alt test](images/sc-scan-webhook-scan-completed.png)

## sc-getrunning.py

At the time of writing this it's not possible to display, outside of the SecurityCenter GUI, a list of running jobs within SecurityCenter. A feature request does exist but not sure on when this is likely to be implemented.

Whilst that works its way through the "system", this script displays scans which have a "running" state within SecurityCenter.

### Configuration
As with *sc-scan-webhook.py* there are some values which need to be configured in the script in the following code section:

``` python
def main():
    hostip = '<IP>'
    username = '<username>'
    password = '<password>'
```
The field *hostip* is the IP address of your SecurityCenter instance. The *username* and *password* field are for the user which authenticates to SecurityCenter to run the scans. I've created a scan-automation user within SecurityCenter for auditing purposes but feel free to choose which ever user you wish.

### Usage

	# python sc-getrunning.py

### Versioning
- v1.0 - original script
- v1.01 - added day intelligence in to sc-scan-webhook to be able modify the target text message sent based on the day of the week (DOTW)
- v1.02 - remove change made in v1.1 and added a second command line argument to take in target text passed from the command line by the scheduled cron job

### ToDo
- Modify the sc-scan-webhook script to handle scans that rollover after a longer period of time.

### License
This project is licensed under the MIT license.
