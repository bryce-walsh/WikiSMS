from mediawiki import MediaWiki
from bs4 import BeautifulSoup

wikipedia = MediaWiki()

#Returns the first 160 characters of the given query page if it exists
def get_first_160(query):
  page = wikipedia.page(query)
  return page.summarize(chars=160)

#Searches the sidebar of the page with the given title and 
#Returns the string associated with the hint if one is found
def check_sidebar(title, hint):
	infobox = parse_infobox(title)
	for key in infobox.keys():
		if hint in key:
			return infobox[key]

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
				parameter = parameter.text.strip()
				value = value.text.strip()
				infobox[parameter] = value
	return infobox

def sidebar_parameters(title):
	infobox = parse_infobox(title)
	return list(infobox.keys())

#Scrapes Wikipedia for a 160 char response
def scrape_wiki(title, type_, category, hint):
 	return check_sidebar(title,hint)

print("Sidebar fields for Tufts University:")
print(sidebar_parameters("Tufts University"))
print()
print("Tufts University Motto:")
print(check_sidebar("Tufts University", "Motto"))