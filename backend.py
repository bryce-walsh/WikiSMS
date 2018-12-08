from mediawiki import MediaWiki
from mediawiki import exceptions
from bs4 import BeautifulSoup
import parser_constants as const
import pprint
import string

pp = pprint.PrettyPrinter(indent=4)
wikipedia = MediaWiki()

#Returns the first sentence of the given title page
def first_sentence(title):
	page = wikipedia.page(title)
	return page.summarize(sentences=1)

#Returns the wikipedia link for the given title
def wikipedia_url(title):
	page = wikipedia.page(title)
	return page.url

#Returns the fields for which there is information in the infobox of the
#page
def sidebar_parameters(title):
	# try:
	infobox = parse_infobox(title)
	# except exceptions.DisambiguationError as err:
	# 	print(err.options)
	# 	return list("A problem has occured")
	return list(infobox.keys())

#Returns a list of the subject headings for the given page
def subject_headings(title):
	page = wikipedia.page(title)
	return page.sections

#Returns the first possible pages to be passed to the user based on the given error.
def format_error(error):
	print(error.title)
	return error.options[0:2]

#Searches the sidebar of the page with the given title and 
#Returns the string associated with the hint if one is found
def check_sidebar(title, hint):
	infobox = parse_infobox(title)
	for key in infobox.keys():
		if hint.lower() in key.lower():
			return infobox[key]

#Searches the main text of the page and makes a best guess
#as to what 160 char response is most likely to contain the information
def search_main_text(title, hint, heading = None):
	page = wikipedia.page(title)
	if heading:
		content = page.section(heading)
		result = search_content(content, hint)
		if result:
			return result
		else:
			content = page.content
	else:
		content = page.content
	result = search_content(content, hint)
	return result

def search_content(content, hint):
	contentLength = len(content)
	for i in range(const.RESPONSE_LEN, contentLength - const.RESPONSE_LEN):
		candidate = content[i-const.RESPONSE_LEN:i+const.RESPONSE_LEN]
		candidateLength = len(candidate)
		middleBegin = int(((canWadidateLength/2) - (const.MIDDLE_LEN/2)))
		middleEnd = int(((candidateLength/2) + (const.MIDDLE_LEN/2)))
		middle = candidate[middleBegin:middleEnd]
		if middle.lower().find(hint.lower()) != -1:
			return candidate

#Returns a dictionary where the keys are the parameters
#of the given page's infobox and the values are the values
def parse_infobox(title):
	page = wikipedia.page(title)
	soup = BeautifulSoup(page.html, 'html.parser')
	info = soup.find('table', {'class': 'infobox'})
	#Inspired by the answer on:
	#https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
	info_body = info.find('tbody')
	rows = info_body.find_all("tr")
	infobox = {}
	for row in rows:
		parameter = row.find('th')
		if parameter != None:
			value = row.find('td')
			if value != None:
				parameter = parameter.get_text(" ", strip=True)
				parameter = parameter.replace("\xa0", ' ')
				value = value.get_text(" ",strip=True)
				infobox[parameter] = value
	return infobox

# Given the title of a page entered to be searched and the 
# error caused by searching it, returns suggestions for what 
# the user probably meant.
def suggestions(title, err):
	errName = err.__class__.__name__
	if errName == exceptions.PageError.__name__:
		results, suggestion = wikipedia.search(title, suggestion=True)
		return [string.capwords(suggestion)] + results
	if errName == exceptions.DisambiguationError.__name__:
		results = wikipedia.search(title)
		# First result is usually the page searched, not useful when Disambiguation
		return results[1:len(results)] 

# Test the suggestions method
def test_suggestions(title):
	print("--TESTING SUGGESTIONS--")
	try:
		page = wikipedia.page(title)
	except exceptions.PageError as err:
		print("Sorry, that's not a valid page title")
		print("Perhaps you meant one of the following?")
		print(suggestions(title, err))
	except exceptions.DisambiguationError as err:
		print("Sorry, that page title is not specific enough")
		print("Perhaps you were looking for one of the following?")
		print(suggestions(title, err))
	else:
		print("Congrats! That's a real page.")
		print("URL: " + wikipedia_url(title))
		print("First Sentece:" + first_sentence(title))		

# Simulate the front end for backend testing
def simulate_text(title):
	print("These are the sidebar parameters for this page: ")
	pp.pprint(sidebar_parameters(title))
	parameter = input ("For which parameter would you like the value? ")
	if parameter == "Other":
		hint = input("What infomation are you looking for? ")
		print(search_main_text(title, hint))
	else:
		print(check_sidebar(title, parameter))

def run_tests(title):
	test_suggestions(title)
	#simulate_text(title)

def test_backend():
	while True:
		title = input("Please enter page title: ")
		run_tests(title)

test_backend()

