from twilio.rest import Client

# Funtion to generate a client object for the Twilio account
def make_client():
	account_sid = 'ACace136eec48e0b51b54ccadc38236267'
	auth_token = 'f4a9b76b529979805290c0c8beb60771'
	client = Client(account_sid, auth_token)
	return client

# Function to send an SMS message to the passed in recipient 
# with the passed in message body
def send_sms(recipient, message):
	twilio_number = '+14703750399'
	client = make_client()
	message = client.messages.create(
									from_=twilio_number,
									body=message,
									to=recipient)

# For Testing Purposes:
# recipient = '+16784515323'
# message = 'Testing send_sms function'
# send_sms(recipient, message)