from selenium import webdriver
from sets import Set
import sys, re

visited = Set()
emails = Set()
driver = webdriver.PhantomJS('../phantomjs-2.0.0-macosx/bin/phantomjs_yosemite')
root = ''

def search(page):
	"Traverse Website Depth-First"
	for email in scrape(page):
		emails.add(email)
	visited.add(page)
	for link in get_links(page):
		if link not in visited:
			search(link)

def scrape(page):
	"Return a list of the unique emails on a page"
	driver.get(page)
	data = driver.page_source
	found = Set()
	email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
	for match in email_pattern.findall(data):
		found.add(match)
	return list(found)

def get_links(page):
	"Return a list of unique links on a page, or None"
	found = Set()
	driver.get(page)
	cookies = driver.get_cookies()
	for c in cookies:
		if 'name' in c and 'value' in c:
			if c['name'] == 'root' and c['value'] == root:
				for elem in driver.find_elements_by_tag_name('a'):
					link = elem.get_attribute('href')
					found.add(link)
	return found

if __name__ == '__main__':
	main()

def main():
	print len(sys.argv)
	print sys.argv[1]
	root = sys.argv[1]
	driver.get(root)
	driver.add_cookie({'name' : 'root', 'value' : 'true', 'domain':root, 'path' : '/', 
		'secure' : False})
	search(root)
	driver.delete_cookie('root')
	for email in emails:
		print email
