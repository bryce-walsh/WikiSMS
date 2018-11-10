from mediawiki import MediaWiki

wikipedia = MediaWiki()

#Returns the first 160 characters of the given query page if it exists
def get_first_160(query):
  page = wikipedia.page(query)
  return page.summarize(chars=160)

#Scrapes Wikipedia for a 160 char response
def scrape_wiki(title, type_, category, hint):
  return get_first_160(title)


#print(get_response("Tufts University"))