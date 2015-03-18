from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from sets import Set
import sys, re

YOSEMITE = True

visited = Set()
emails = Set()

phantom_bin = 'phantomjs/bin/phantomjs'
if YOSEMITE:
	phantom_bin += '_yosemite'

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

cap = dict(DesiredCapabilities.PHANTOMJS)
cap["phantomjs.page.settings.userAgent"] = user_agent
driver = webdriver.PhantomJS(phantom_bin, desired_capabilities=cap)
root = ''
salt = '938475sfasdg34'

def search(page):
	"Traverse Website Depth-First"
	if page is None:
		return
	driver.get(page)
	same_domain = False
	cookies = driver.get_cookies()
	for c in cookies:
		if 'name' in c and 'value' in c:
			if c['name'] == 'root' and c['value'] == salt:
				print "  page is in same domain..."
				same_domain = True
	if not same_domain:
		print "  page is in different domain"
		visited.add(page)
		return
	print "Searching page: ", page
	for email in scrape(page):
		print "  Found email: ",email
		emails.add(email)
	visited.add(page)
	for link in get_links(page):
		print "  Found link: ", link
		if link not in visited:
			search(link)

def scrape(page):
	"Return a list of the unique emails on a page"
	print "Scraping: ", page
	driver.get(page)
	data = driver.page_source
	found = Set()
	email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
	for match in email_pattern.findall(data):
		found.add(match)
	return list(found)

def get_links(page):
	"Return a list of unique links on a page, or None"
	print "Getting links on: ",page
	found = Set()
	driver.get(page)
	cookies = driver.get_cookies()
	for elem in driver.find_elements_by_tag_name('a'):
		link = elem.get_attribute('href')
		found.add(link)
	return found


def main():
	print 'Domain: ',sys.argv[1]
	root = sys.argv[1]
	if root.find('http://') < 0:
		root = 'http://' + root
	driver.get(root)
	driver.add_cookie({'name' : 'root', 'value' : salt, 'domain':root[7:], 'path' : '/', 
		'secure' : False})
	search(root)
	driver.delete_cookie('root')
	for email in emails:
		print email

if __name__ == '__main__':
	main()
