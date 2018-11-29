# Driver module for backend communications with the user

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import sms_backend as sms_be
import backend_constants as const

app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])

def main():
	client = sms_be.make_client()
	message = request.values.get(const.BODY, None)
	recent_messages = client.messages.list()
	user = const.EMPTY
	for sms in recent_messages:
		if(sms.body == message):
			user = sms.from_
			recent_messages = client.messages.list(to=user)
			break
	message_indicator = recent_messages[const.INDICATOR_INDEX].body
	body_words = message_indicator.split(const.SPACE)
	try:
		message_indicator = body_words[const.INDICATOR_STRING]
	except: 
		return sms_be.sms_welcome_message()

	if(message.lower() == const.EXIT.lower()):
		return sms_be.sms_goodbye_message()
	elif(message.lower() == const.RESTART.lower()):
		return sms_be.sms_welcome_message()
	elif(message.lower() == const.BACK.lower()):
		return sms_be.sms_resend_most_recent_message_reply(recent_messages)
	elif(message_indicator == const.WELCOME):	
		return sms_be.sms_sidebar_reply(message)
	elif(message_indicator == const.INFO):
		if(message.lower() == const.OTHER.lower()):
			return sms_be.sms_get_query_reply()
		else:
			user_messages = client.messages.list(from_=user)
			title = user_messages[const.INFO_TITLE].body
			return sms_be.sms_search_infobox_reply(title, message)
	elif(message_indicator == const.SEARCH):
		sent_messages = client.messages.list(to=user)
		result_sms = sent_messages[const.RESULT_INDEX].body
		body_words = result_sms.split(const.SPACE)
		if(body_words[const.INDICATOR_STRING] == const.RESULTS):
			start = result_sms.find(const.TITLE) + const.TITLE_LENGTH
			title = result_sms[start:result_sms.find(const.NEW_LINE, start)]
			return sms_be.sms_search_main_text_reply(title, message)
		else:
			user_messages = client.messages.list(from_=user)
			title = user_messages[const.QUERY_TITLE].body
			return sms_be.sms_search_main_text_reply(title, message)
	elif(message_indicator == const.RESULTS):
		if(message.lower() == const.OTHER.lower()):
			return sms_be.sms_get_query_reply()
		else:
			title_sms = client.messages.list(to=user)[const.RESULT_TITLE].body
			start = title_sms.find(const.TITLE)
			title = title_sms[start:title_sms.find(const.NEW_LINE, start)]
			return sms_be.sms_search_infobox_reply(title, message)
	else:																		
		return sms_be.sms_welcome_message()								
																					 
if __name__ == "__main__":														
    app.run()	
