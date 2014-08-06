from bs4 import BeautifulSoup
import urllib2
import sys

def siteData(site):
	url = urllib2.urlopen(site)
	data = url.info()
	html = url.read()
	return data, html

if __name__ == "__main__":
	info, content = siteData('http://sports.espn.go.com/nhl/boxscore?gameId=400484244')
	print info
	print len(content)