from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from sms_send import make_client

app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])
def pull_incoming_message():
	client = make_client()
	recent_messages = client.messages.list()
	message = recent_messages[0].body
	return message

def pull_incoming_number():
	client = make_client()
	recent_messages = client.messages.list()
	number = recent_messages[0].from_
	return number

print(pull_incoming_message())
print(pull_incoming_number())