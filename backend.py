from mediawiki import MediaWiki
from mediawiki import exceptions
from bs4 import BeautifulSoup
import parser_constants as const
import pprint
import string
import operator
import sys

pp = pprint.PrettyPrinter(indent=4)
wikipedia = MediaWiki()

# Returns the first sentence of the given title page
def first_sentence(title):
	page = wikipedia.page(title)
	return page.summarize(sentences=1)

# Returns the wikipedia link for the given title
def wikipedia_url(title):
	page = wikipedia.page(title)
	return page.url

# Returns the fields for which there is information in the infobox of the
# page
def sidebar_parameters(title):
	infobox = parse_infobox(title)
	return list(infobox.keys())

# Returns a list of the subject headings for the given page
def subject_headings(title):
	page = wikipedia.page(title)
	return page.sections

# Returns the first possible pages to be passed to the user based on the given error.
def format_error(error):
	print(error.title)
	return error.options[0:2]

# Searches the sidebar of the page with the given title and 
# Returns the string associated with the hint if one is found
def check_sidebar(title, hint):
	infobox = parse_infobox(title)
	for key in infobox.keys():
		if hint.lower() in key.lower():
			return infobox[key]

# Searches the main text of the page and makes a best guess
# as to what 160 char response is most likely to contain the information
# The optional index parameter specifies which rank in the results 
# to be returned. If none is given, will return the highest ranked result.
def search_main_text(title, hint, index = 0):
	page = wikipedia.page(title)
	content = page.content
	candidates = search_content(content, hint)
	sortedCandidates = sort_by_proximity(candidates, title, hint)
	if sortedCandidates:
		return sortedCandidates[index][0]
	else:
		return None
# Given the title of a page and the last_response given, gives the next 
# response-length chunk of characters
def read_more(title, last_response):
	page = wikipedia.page(title)
	content = page.content
	contentLength = len(content)
	responseLength = len(last_response)
	halfResponseLen = responseLength // 2
	for i in range(responseLength, contentLength - responseLength):
		candidate = content[i-halfResponseLen:i+halfResponseLen]
		if candidate == last_response:
			result = content[i + halfResponseLen : (i + halfResponseLen) + const.RESPONSE_LEN]
	if result:
		return result
	else:
		return None 

# Returns a list of (candidate, proximity) tuples, sorted by 
# the proximity of the hint word to the title of the page
def sort_by_proximity(candidates,title,hint):
	candidatesWithProximity = {}
	for candidate in candidates:
		candidateProximity = proximity(candidate, title, hint)
		candidatesWithProximity[candidate] = candidateProximity
	sortedCandidates = sorted(candidatesWithProximity.items(), key=operator.itemgetter(1))
	return sortedCandidates

# Returns a list of candidate responses based on the given content 
# and hint
def search_content(content, hint):
	contentLength = len(content)
	candidates = []
	halfResponseLen = const.RESPONSE_LEN // 2
	i = halfResponseLen
	while i < contentLength - halfResponseLen:
		candidate = content[i-halfResponseLen:i+halfResponseLen]
		candidateLength = len(candidate)
		middleBegin = (candidateLength//2) - (const.MIDDLE_LEN//2)
		middleEnd = (candidateLength//2) + (const.MIDDLE_LEN//2)
		middle = candidate[middleBegin:middleEnd]
		if middle.lower().find(hint.lower()) != -1:
			candidates.append(candidate)
			i += const.MIDDLE_LEN
		i += 1
	return candidates

# Returns the proximity (distance in letters) between
# the given title and the given hint within the given candidate
def proximity(candidate, title, hint):
	candidate = candidate.lower()
	hint = hint.lower()
	title = title.lower()
	hintIndex = candidate.index(hint)
	candidateLeft = candidate[0:hintIndex]
	candidateRight = candidate[hintIndex:len(candidate)]
	if title in candidateLeft:
	 	titleIndexLeft = candidate.index(title)
	 	proximityLeft = hintIndex - titleIndexLeft
	else:
		proximityLeft = sys.maxsize
	if title in candidateRight:
	 	titleIndexRight = candidate.index(title)
	 	proximityRight = titleIndexRight - hintIndex
	else:
		proximityRight = sys.maxsize
	return min(proximityLeft, proximityRight)

# Returns a dictionary where the keys are the parameters
# of the given page's infobox and the values are the values
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

# Test the proximity method
def test_proximity():
	while True:
		#candidate = input("Candidate: ")
		candidate = "The quick brown fox jumped over the lazy dog"
		hint = input("Hint: ")
		title = input("Title: ")
		print(proximity(candidate, title, hint))

# Test the read_more method
def test_read_more(title):
	hint = input("Please enter hint: ")
	originalResponse = search_main_text(title, hint)
	print("Original Response:" + originalResponse)
	nextResponse = read_more(title, originalResponse)
	print("Next Response:" + nextResponse)

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
	#test_suggestions(title)
	#test_proximity()
	test_read_more(title)
	#simulate_text(title)

def test_backend():
	while True:
		title = input("Please enter page title: ")
		run_tests(title)

test_backend()

