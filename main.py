import urllib2
from sets import Set


visited = Set()
emails = Set()

def search(page) {
	"Traverse Website Depth-First"
	if page is None:
		return
	for email in scrape(page):
		emails.add(email)
	visited.add(page)
	for link in get_links(page):
		if link not in visited:
			search(link)
}

def scrape(page):
	"Return a list of the unique emails on a page"
	found = Set()
	pass

def get_links(page):
	"Return a list of unique links on a page, or None"
	found = Set()
	pass
