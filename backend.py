from mediawiki import MediaWiki
from bs4 import BeautifulSoup
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
		if hint in key:
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
	if result:
		return result
	else:
		return "The information was not found"

def search_content(content, hint):
	contentLength = len(content)
	for i in range(80,contentLength - 80):
		candidate = content[i-80:i+80]
		candidateLength = len(candidate)
		middleBegin = int(((candidateLength/2) - 10))
		middleEnd = int(((candidateLength/2) + 10))
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

# title = input("Please enter page title: ")
# sidebarOrMain = input("Do you think the information is in the sidebar (S) or the main text (T)? ")
# if sidebarOrMain == "S":
# 	print("These are the sidebar parameters for this page: ")
# 	pp.pprint(sidebar_parameters(title))
# 	hint = input ("Which parameter do you want the value for? ")
# 	print(check_sidebar(title, hint))
# elif sidebarOrMain == "T":
# 	print("These are the section headings for this page:")
# 	pp.pprint(subject_headings(title))
# 	heading = input("Which heading do you think contains the information? ")
# 	hint = input("What infomation are you looking for? ")
# 	print(search_main_text(title, hint, heading))
# else:
# 	print("Please try again")

