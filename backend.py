from mediawiki import MediaWiki

wikipedia = MediaWiki()

#Returns the first 160 characters of the given query page if it exists
def get_response(query):
  page = wikipedia.page(query)
  return page.summarize(chars=160)


#print(get_response("Tufts University"))