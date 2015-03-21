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

def strip_protocol(url):
    "Take the protocol out of the url"
    return url.split('//')[-1]

def strip_fragment(url):
    "Take out the hashbang fragment"
    if url is not None:
        return url.split('#')[0]
    else:
        return None

def domain(url):
    "Return the domain name"
    return strip_protocol(url).split('/')[0]

def search(page):
    "Traverse Website Depth-First"
    if not page:
        return
    if domain(page).find(domain(root)) < 0:
        return
    driver.get(page)
    for email in scrape(page):
        emails.add(email)
    visited.add(strip_fragment(page))
    for link in get_links(page):
        if strip_fragment(link) not in visited:
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
    for elem in driver.find_elements_by_tag_name('a'):
        link = elem.get_attribute('href')
        found.add(link)
    return found

def main():
    print 'Url: ',sys.argv[1]
    global root
    root = sys.argv[1]
    if root.find('http://') < 0:
        root = 'http://' + root
    search(root)
    for email in emails:
        print email

if __name__ == '__main__':
    main()
