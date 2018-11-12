# Functions module associated with backend communications to the frontend

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from backend import sidebar_parameters
from backend import check_sidebar
import backend_constants as const

'''
make_client function
Parameters: none
Returns: client object
Purpose: makes a client object associated with the backend twilio account
'''
def make_client():
	account_sid = const.SID
	auth_token = const.TOKEN
	client = Client(account_sid, auth_token)
	return client

'''
sms_first_reply function
Parameters: string for the title to search wikipedia for
Returns: string for the response to send to the front end
Purpose: Pulls the infobox keywords from the wikipedia page 
		 associated with the passed in title and sends the
		 information back to the front end
'''
def sms_first_reply(title):
	keywords = sidebar_parameters(title)
	options = ''
	for keyword in keywords:
		options = keyword + const.NEW_LINE + options
	resp = MessagingResponse()
	resp.message(str(options))
	return str(resp)

'''
sms_second_reply function
Parameters: string for the title to search wikipedia for
			string for the hint to search the given page for
Returns: string for the response to send to the front end
Purpose: Pulls the infobrmation related to the passed in hint on the
		 passed in wikipedia page and send the information back to the 
		 front end
'''
def sms_second_reply(title, hint):
	resp = MessagingResponse()
	info = check_sidebar(title, hint)
	resp.message(str(info))
	return str(resp)

'''
send_sms function
Parameters: string for the sender's phone numbr
			string for the body of the message to send
			string for the recipient's phone number
Returns: nothing
Purpose: Sends the given message from the passed in sender's 
		 number to the passed in recipient's number
'''
def send_sms(sender, message, recipient):
	client = make_client()
	message = client.messages.create(
									from_=sender,
									body=message,
									to=recipient)