# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from sms_send import make_client
from sms_recieve import process_message


app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def pull_wiki_info():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    client = make_client()
    resp = MessagingResponse()
    messages = client.messages.list()
    resp.message(process_message(messages[0]))
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)