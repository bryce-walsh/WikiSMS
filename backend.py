from mediawiki import MediaWiki

wikipedia = MediaWiki()

def get_response(query):
  page = wikipedia.page(query)
  return page.summarize(chars=160)

print(get_response("Washington (state)"))
