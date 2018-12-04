from mediawiki import MediaWiki
from bs4 import BeautifulSoup
import parsing_constants as const
import pprint

pp = pprint.PrettyPrinter(indent=4)
wikipedia = MediaWiki()

#Returns the first 160 characters of the given query page if it exists
def get_first_160(query):
	page = wikipedia.page(query)
	return page.summarize(chars=160)

#Returns the fields for which there is information in the infobox of the
#page
def sidebar_parameters(title):
	infobox = parse_infobox(title)
	return list(infobox.keys())

#Returns a list of the subject headings for the given page
def subject_headings(title):
	page = wikipedia.page(title)
	return page.sections

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
		middleBegin = int(((candidateLength/2) - (const.MIDDLE_LEN/2)))
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

#Example use
#print("Sidebar fields for Tufts University:")
#print(sidebar_parameters("Tufts University"))
#print()
#print("Tufts University Motto:")
#print(check_sidebar("Tufts University", "Motto"))
#print()

title = input("Please enter page title: ")
print("These are the sidebar parameters for this page: ")
pp.pprint(sidebar_parameters(title))
parameter = input ("For which parameter would you like the value? ")
if parameter == "Other":
	hint = input("What infomation are you looking for? ")
	print(search_main_text(title, hint))
else:
	print(check_sidebar(title, parameter))
