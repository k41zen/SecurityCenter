# Introduction

Here are a couple of scripts I've quickly knocked up (so to speak) to help me with automating SecurityCenter scans whilst at the same time giving the right useful information to the right people.

##

#### sc-scan-webhook
This script allows you to start predefined scans with Tenable's Security through the API, send a webhook notification message to a Google chat room, monitor for the scan to complete successfully and then sends another webhook notification message stating the scan is complete.

As different target groups were being scanned on different days, the script also starts the right scan for the day of the week. On top of that, the script sends a customised webhook notification stating which group is being scanned and also includes the scan resultID.

##

#### sc-getscans.py
A script that lists scans which have a "running" state within SecurityCenter. 

##

#### ToDo
Modify the sc-scan-webhook script to handle scans that rollover after a longer period of time.

#### License
This project is licensed under the MIT license.

##
