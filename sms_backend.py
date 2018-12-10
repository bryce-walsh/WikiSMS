# Functions module associated with backend communications to the user

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import backend as be
import backend_constants as const

'''
get_recent_messages function
Parameters: None
Returns: client object for the associated Twilio account
		 string for the phone number of the user interacting with the app
		 array of message objects for the recent messages to the user
Purpose: Pulls the recent messages to the user who just sent a message and 
		 pulls the user's phone number and a client object for the Twillio 
		 account
'''
def get_recent_messages():
	client = make_client()
	message = request.values.get(const.BODY, None)
	if(True):
		recent_messages = client.messages.list()
		user = const.EMPTY
		for sms in recent_messages:
			if(sms.body == message):
				user = sms.from_
				recent_messages = client.messages.list(to=user)
				break
	return client, user, message, recent_messages

'''
get_message_indicator function
Parameters: array of the recent messages sent to the user
Returns: string for the indicator in the most recent sms to the user
Purpose: Pulls the indicator from the most recent sms the user received
'''
def get_message_indicator(recent_messages):
	message_indicator = recent_messages[const.INDICATOR_INDEX].body
	body_words = message_indicator.split(const.SPACE)
	message_indicator = body_words[const.INDICATOR_STRING]
	return message_indicator

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
sms_welcome_message function
Parameters: None
Returns: Messaging Response to send to the front end
Purpose: Sends the intiial welcome message to the user 
		 with instructions for how to proceed
'''
def sms_welcome_message():
	resp = MessagingResponse()
	resp.message(str(const.WELCOME_MESSAGE))
	return str(resp)

'''
sms_send_next function
Parameters: client object associated to the Twilio account
			string for the user's phone number
Returns: Nessaging Response object to send back to the user
Purpose: Sends the user the next occurance of the query they are searching
'''
def sms_send_next(client, user):
	resp = MessagingResponse()
	recent_messages = client.messages.list(from_=user)
	count = 0
	for sms in recent_messages:
		if(sms.body.lower() == const.NEXT.lower()):
			count += const.INCREMENT
		else:
			break
	result_sms = client.messages.list(to=user)[const.RESULT_TITLE].body
	start = result_sms.find(const.TITLE) + const.TITLE_LENGTH
	title = result_sms[start:result_sms.find(const.NEW_LINE, start)]
	start = result_sms.find(const.QUERY) + len(const.QUERY)
	query = result_sms[start:result_sms.find(const.NEW_LINE, start)]
	try:
		info = be.search_main_text(title, query, count)
		response = compile_results(title, query, info, False)
	except:
		response = compile_results(title, query, const.LAST_OCCURANCE, False)
	resp.message(str(response))
	return str(resp)

def sms_show_more(client, user):
	resp = MessagingResponse()
	result_sms = client.messages.list(to=user)[const.RESULT_TITLE].body
	start = result_sms.find(const.TITLE) + const.TITLE_LENGTH
	title = result_sms[start:result_sms.find(const.NEW_LINE, start)]
	start = result_sms.find(const.QUERY) + len(const.QUERY)
	query = result_sms[start:result_sms.find(const.NEW_LINE, start)]
	start = result_sms.find(const.RESULT) + len(const.RESULT)
	result = result_sms[start:result_sms.find(const.NEW_LINE, start)]
	info = be.read_more(title, result)
	response = compile_results(title, query, info, False)
	resp.message(str(response))
	return str(resp)

'''
sms_send_link function
Parameters: None
Returns: Messaging Response object to send back to the user
Purpose: Sends the link of the title page back to the user
'''
def sms_send_link(client, user, message_indicator):
	resp = MessagingResponse()
	user_sms = client.messages.list(from_=user)
	sent_messages = client.messages.list(to=user)
	result_sms = sent_messages[const.RESULT_TITLE].body
	start = result_sms.find(const.TITLE) + const.TITLE_LENGTH
	title = result_sms[start:result_sms.find(const.NEW_LINE, start)]
	link = be.wikipedia_url(title)
	resp.message(str(compile_results(title, const.LINK, link, True)))
	return str(resp)

'''
sms_ambig_reply function
Parameters: string for the message the user just sent
Returns: String for the response message to send to the front end
Purpose: Sends sidebar parameters after the user clarifies the title
'''
def sms_ambig_reply(client, user, message):
	resp = MessagingResponse()
	user_messages = client.messages.list(from_=user)
	title = user_messages[const.AMBIG_INDEX].body
	try:
		keywords = sorted(be.sidebar_parameters(title))
	except Exception as error:
		keywords = sorted(be.suggestions(title, error))
	title = keywords[int(message)-const.INCREMENT]
	keywords = sorted(be.sidebar_parameters(title))
	opt = const.EMPTY
	index = const.INCREMENT
	for keyword in keywords:
		opt = opt + str(index) + const.PERIOD + const.SPACE + keyword +\
			  const.NEW_LINE
		index += const.INCREMENT
	opt = opt + const.LINK_MESSAGE + const.OTHER_MESSAGE
	opt =  const.INFO + const.SPACE + const.NEW_LINE + const.TITLE + title +\
		   const.NEW_LINE + const.BLURB + str(be.first_sentence(title)) +\
		   const.NEW_LINE + const.INFO_MESSAGE + opt
	resp.message(str(opt))
	return str(resp)

'''
sms_goodbye_message function
Parameters: None
Returns: String for the response message to send to the front end
Purpose: Sends the final goodbye message
'''
def sms_goodbye_message():
	resp = MessagingResponse()
	resp.message(str(const.GOODBYE_MESSAGE))
	return str(resp)

'''
sms_sidebar_reply function
Parameters: string for the title to search Wikipedia for
Returns: string for the response to send to the front end
Purpose: Pulls the infobox keywords from the Wikipedia page 
		 associated with the passed in title and sends the
		 information back to the front end
'''
def sms_sidebar_reply(title):
	resp = MessagingResponse()
	try:
		keywords = sorted(be.sidebar_parameters(title))
		options = const.EMPTY
		index = const.INCREMENT
		for keyword in keywords:
			options = options + str(index) + const.PERIOD + const.SPACE +\
			 		  keyword + const.NEW_LINE
			index += const.INCREMENT
		options = options + const.LINK_MESSAGE + const.OTHER_MESSAGE
		options =  const.INFO + const.SPACE + const.NEW_LINE + const.TITLE +\
				   title + const.NEW_LINE + const.BLURB +\
				   str(be.first_sentence(title)) + const.NEW_LINE +\
				   const.INFO_MESSAGE + options
		resp.message(str(options))
	except Exception as error:
		keywords = sorted(be.suggestions(title, error))
		index = const.INCREMENT
		options = const.EMPTY
		for keyword in keywords:
			options = options + str(index) + const.PERIOD + const.SPACE +\
					  keyword + const.NEW_LINE
			index += const.INCREMENT
		options = const.AMBIG_TITLE + const.AMBIG_MESSAGE + options
		options = options[0:-1]
		resp.message(str(options))
	return str(resp)

'''
process_keyword function
Parameters: client object for the associated Twillio account
			string for the phone number of the user
			string for the body of the message the user sent
Returns: Messaging Response object to send back to the user
Purpose: Processes the keyword that the user sent and sends back the
		 requested information or gets the query if the user selected other
'''
def process_keyword(client, user, message):
	if(message.lower() == const.OTHER.lower()):
		return sms_get_query_reply()
	else:
		user_messages = client.messages.list(to=user)
		title_sms = user_messages[const.INFO_TITLE].body
		start = title_sms.find(const.TITLE) + len(const.TITLE)
		title = title_sms[start:title_sms.find(const.NEW_LINE, start)]
		keywords = sorted(be.sidebar_parameters(title))
		try:
			keyword = keywords[int(message)-const.INCREMENT]
			return sms_search_infobox_reply(title, keyword)	
		except:
			return sms_sidebar_reply(title)

'''
get_query_reply function
Parameters: None
Returns: string for the response to send to the front end
Purpose: Sends a message to the front end asking for the phrase
		 to search the main text for
'''
def sms_get_query_reply():
	resp = MessagingResponse()
	resp.message(str(const.QUERY_MESSAGE))
	return str(resp)

'''
sms_second_reply function
Parameters: string for the title to search wikipedia for
			string for the query to search the given page for
Returns: string for the response to send to the front end
Purpose: Pulls the infobrmation related to the passed in query on the
		 passed in wikipedia page and send the information back to the 
		 front end
'''
def sms_search_infobox_reply(title, query):
	resp = MessagingResponse()
	info = be.check_sidebar(title, query)
	response = compile_results(title, query, info, True)
	resp.message(str(response))
	return str(resp)

'''
compile_results function
Parameters: string for the title to search Wikipedia for
			string for the query that was searched for on the title page
			string for the results returned from the user requested search
Returns: string for the results that will be sent back to the user
Purpose: Compiles the message that will be sent back to the user for the results
'''
def compile_results(title, query, info, infobar):
	response = const.RESULTS + const.SPACE + const.NEW_LINE + const.TITLE\
			 + title + const.NEW_LINE + const.QUERY + query + const.NEW_LINE
	if(info == None):
		response += const.RESULT + query + const.NO_INFO + title
	else:
		response += const.RESULT + info
	response += const.NEW_LINE
	if(infobar):
		response += const.SEARCH_AGAIN
	else:
		response += const.SEARCH_AGAIN_NEXT
	return response 

'''
process_search function
Parameters: client object for the associated Twillio account
			string for the phone number of the user
			string for the body of the message the user sent
Returns: Messaging Response object to send back to the user
Purpose: Processes the query that the user sent and sends back the
		 requested information
'''
def process_search(client, user, message):
	sent_messages = client.messages.list(to=user)
	result_sms = sent_messages[const.RESULT_INDEX].body
	body_words = result_sms.split(const.SPACE)
	start = result_sms.find(const.TITLE) + const.TITLE_LENGTH
	title = result_sms[start:result_sms.find(const.NEW_LINE, start)]
	return sms_search_main_text_reply(title, message)	

'''
process_new_search function
Parameters: client object for the associated Twillio account
			string for the phone number of the user
			string for the body of the message the user sent
Returns: Messaging Response object to send back to the user
Purpose: Processes the keyword that the user sent and sends back the
		 requested information or gets the query if the user selected other
'''
def process_new_search(client, user, message):
	if(message.lower() == const.OTHER.lower()):
		return sms_get_query_reply()
	else:
		title_sms = client.messages.list(to=user)[const.RESULT_TITLE].body
		start = title_sms.find(const.TITLE) + const.TITLE_LENGTH
		title = title_sms[start:title_sms.find(const.NEW_LINE, start)]
		keywords = sorted(be.sidebar_parameters(title))
		keyword = keywords[int(message)-const.INCREMENT]
		return sms_search_infobox_reply(title, keyword)

'''
sms_search_main_text_reply function
Parameters: string for the title to search Wikipedia for
			string for the hint to search the main text for
			string for the heading to search within the title page
Returns: string for the response to send to the front end
Purpose: Searches the heading within the title page for the hint
		 and sends the information back to the front end
'''
def sms_search_main_text_reply(title, hint):
	info = be.search_main_text(title, hint)
	response = compile_results(title, hint, info, False)
	resp = MessagingResponse()
	resp.message(str(response))
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
