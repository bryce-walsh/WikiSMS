# Constants Module

# Twilio Constants 
SID = "AC700de6d0d7ff9600f15ecbb84fefbf07" # Twilio account sid
TOKEN = "e4dd1d3d81024a250f6ff50242ba591b" # Twilio authentication token
BACK_END_NUMBER = "16782646845"	   		   # Twilio backend phone number

# Constants to Distinguish User Text Messages and Requests
WELCOME = "*"		# Keyword to distinguish message with the page title
AMBIG_TITLE = "?" 	# Keyword to distinguish message with ambiguous title
INFO = "**"			# Keyword to distriguish message with sidebar parameter
SEARCH = "***"		# Keyword to distinguish message with query string
RESULTS = "****"	# Keyword to distinguish message with the results
OTHER = "Other"		# Keyword to distinguish is user is parsing main text
RESTART = "Restart" # Keyword to restart the user search
EXIT = "Exit"		# Keyword to quit the program

# Constants for instructional response messages to send to the user
WELCOME_MESSAGE = "* \nWelcome to wikiSMS. Please respond with the name of"\
				   + " the page you would like to get information about."\
				   + " If you make a typo at any point, just reply with the"\
				   + " word restart to start over."
PAGE_NOT_FOUND = "* \nThe page you requested could not be found. "\
			      + "Please respond with another page name."
INFO_MESSAGE = "** \nPlease respond with one of the following keywords "\
				 + "that matches what you are searching for, or respond with"\
				 + " other if none of the following apply:\n"
QUERY_MESSAGE = "*** \nYou have selected the other option. Please respond with"\
				   + " the specific piece of information you are looking for."
NO_INFO = " could not be found within the page for "
SEARCH_AGAIN = "\nPlease respond with exit if you are finished, "\
			 + "restart if you would like information from a new page, "\
			 + "or enter another keyword."
GOODBYE_MESSAGE = "Thank you for using WikiSMS."

# Constants for array/string indices 
INDICATOR_INDEX = 0		# Index of message containing keyword for current step
INDICATOR_STRING = 7	# Index of keyword in indicator message
INFO_TITLE = 1			# Index of SMS with the title when parsing sidebar
QUERY_TITLE = 2			# Index of SMS with the title when parsing main text
RESULT_TITLE = 0		# Index of SMS with the title when searching again
RESULT_INDEX = 1		# Index of SMS with the potential last search's results
TITLE_LENGTH = 6		# Int for the length of the title phrase

# Miscellaneous Constants
NEW_LINE = '\n'			# New line character 
BODY = "Body"			# String for body attribute of Flask request
SPACE = ' '				# Char for an space character
EMPTY = ''				# Char for an empty character
TITLE = "Page: "		# String for the title heading for the results sms
QUERY = "Query: "		# String for the query heading for the results sms
RESULT = "Result: "		# String for the results heading for the results sms
