# Driver module for backend communications with the user

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import sms_backend as sms_be
import backend_constants as const

app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])

def main():
	# Get Twillio client object, user phone number, and recent messages 
	client, user, message, recent_messages = sms_be.get_recent_messages()
	try:
		# Pull the inidcator from the recieved sms for which step the user is at
		message_indicator = sms_be.get_message_indicator(recent_messages)
	except: 
		# If no messages exist with the user, respond with the welcome message
		return sms_be.sms_welcome_message()
	# Respond with the goodbye message
	if(message.lower() == const.EXIT.lower()):
		return sms_be.sms_goodbye_message()
	# Restart the user search and respond with the welcome message
	elif(message.lower() == const.RESTART.lower()):
		return sms_be.sms_welcome_message()
	elif(message.lower() == const.LINK.lower()):
		return sms_be.sms_send_link(client, user, message_indicator)
	# Respond with the sidebar parameters from the page name the user sent
	elif(message_indicator == const.WELCOME or message_indicator == const.AMBIG_TITLE):	
		return sms_be.sms_sidebar_reply(message)
	# Respond with value of the given key or get the query from the user
	elif(message_indicator == const.INFO):
		return sms_be.process_keyword(client, user, message)
	# Respond with the search results from parsing the main text
	elif(message_indicator == const.SEARCH):
		return sms_be.process_search(client, user, message)
	# Respond with new results from a follow up query
	elif(message_indicator == const.RESULTS):
		return sms_be.process_new_search(client, user, message)
	# Respond with the welcome message
	else:																		
		return sms_be.sms_welcome_message()								
																					 
if __name__ == "__main__":														
    app.run()	
