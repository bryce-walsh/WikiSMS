from backend import *

print()
query = input("Enter a Wikipedia page title: ")
print()
print("The first 160 characters of the Wikipedia page for " + query + " are:")
print(get_response(query))
print()