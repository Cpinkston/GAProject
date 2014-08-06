from bs4 import BeautifulSoup
import urllib2
import sys

def siteData(site):
	url = urllib2.urlopen(site)
	data = url.info()
	html = url.read()
	return url, data, html

if __name__ == "__main__":
	site, info, content = siteData('http://sports.espn.go.com/nhl/boxscore?gameId=400484244')
	print site