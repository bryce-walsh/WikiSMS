# Driver for backend communications with the frontend

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from backend import sidebar_parameters
from backend import check_sidebar
import sms_backend as be
import constants as const

app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])

def main():
	client = be.make_client()
	recent_messages = client.messages.list()
	recipient = recent_messages[0].from_
	message = recent_messages[0].body
	if(message[const.KEYWORD_START:const.KEYWORD_END] == const.TITLE):
		return be.sms_first_reply(str(message[const.MESSAGE_START:]))
	else:
		user_messages = client.messages.list(from_=recipient)
		title = user_messages[1].body[const.MESSAGE_START:]
		return be.sms_second_reply(title, message)



if __name__ == "__main__":
    app.run()