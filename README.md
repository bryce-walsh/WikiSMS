# WikiSMS

## Overview

WikiSMS is a platform for browsing and retrieving information from Wikipedia through a text based SMS interface. 
The goal of this project is to provide access to the vast amount of information on Wikipedia to users without data plans.

## Quick Start Guide

The following guide describes how to get the server side of WikiSMS running on your machine:

### Backend dependency installation
Run the folowwing commands in a linux shell to install the python dependencies for the backend of this project:
* pip3 install pymediawiki
* pip3 install beautifulsoup4

### SMS dependency installation
Run the folowwing commands to install the python dependencies for the sms part of this project:
(If errors occur try using pip instead of pip3 or adding --user to the end of the command)
* pip3 install twilio
* Must setup Flask (use link below)
  * https://www.twilio.com/docs/sms/quickstart/python#receive-and-reply-to-inbound-sms-messages-with-flask
* Must setup ngrok (use link below)
  * https://ngrok.com/download
  
### Running the service
* Once everything is installed and FLask and ngrok are ready:
    * Clone this repository onto your machine
    * Run the backend_driver with:
      * python3 sms_backend_driver.py
    * Activate ngrok with:
      * ./ngrok http 5000
    * Then:
      * copy the URL in the https heading from ngrok
      * login to twilio with email: ciard1998@gmail.com pwd: CDRproject2018 or your own account
      * click on the # symbol in left heading bar
      * click on the phone number
      * scroll down to messaging
      * In "a message comes in" paste the URL and add "/sms" to it and click save
    * Then send your first query to the twillio number found in constants.py

