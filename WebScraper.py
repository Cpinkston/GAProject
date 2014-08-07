from bs4 import BeautifulSoup
import urllib2
import sys
import pandas as pd

def siteData(site):
	url = urllib2.urlopen(site)
	data = url.info()
	html = url.read()
	return url, data, html

def extractTable(html):
	table = BeautifulSoup(html).find('table', class_='mod-data')
	#heads = table.find_all('thead')
	#bodies = table.find_all('tbody')

	team_1 = table.th.text
	team_1_players = bodies[0].find_all('tr') + bodies[1].find_all('tr')
	team_1_players = get_players(team_1_players, team_1)
	players = players.append(team_1_players)


if __name__ == "__main__":
	site, info, content = siteData('http://sports.espn.go.com/nhl/boxscore?gameId=400484245')

	table = BeautifulSoup(content).find_all('table', class_='mod-data')
	heads = table[3].find_all('thead')
	headers = heads[1].find_all('tr')[1].find_all('th')[1:]
	headers = [th.text for th in headers]
	columns = ['id', 'team', 'player'] + headers

	players = pd.DataFrame(columns=columns)

	#extractTable(content)
	print(players)