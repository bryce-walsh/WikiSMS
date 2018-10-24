from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from sms_send import make_client
from backend import *

app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])

# Function to pull the message body for the most recently recieved SMS
def pull_incoming_message():
	client = make_client()
	recent_messages = client.messages.list()
	message = recent_messages[0].body
	return message

# Function to pull the sender's number for the most recently recieved SMS
def pull_incoming_number():
	client = make_client()
	recent_messages = client.messages.list()
	number = recent_messages[0].from_
	return number

def process_message(message):
	title, type_,category,hint = message.split("\n");
	scrape_wiki(title, type_, category, hint);


# For Testing Purposes:
# print(pull_incoming_message())
# print(pull_incoming_number())

