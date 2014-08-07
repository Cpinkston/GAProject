from bs4 import BeautifulSoup
from pandas import DataFrame
import urllib2
import sys
import pandas as pd

def siteData(site):
	url = urllib2.urlopen(site)
	data = url.info()
	html = url.read()
	return url, data, html

def extractTable(html):
	playersData = []
	table = BeautifulSoup(html).find_all('table', class_='mod-data')
	heads = table[3].find_all('thead')
	bodies = table[3].find('tbody').find_all('tr')
	for i in range(0,len(bodies)):
		data = [td.text for td in bodies[i]]
		playersData.append(data)

	frame = pd.DataFrame(playersData[0])
	print type(frame)
	#team_1 = table.th.text
	#team_1_players = bodies[0].find_all('tr') + bodies[1].find_all('tr')
	#team_1_players = get_players(team_1_players, team_1)
	#players = players.append(team_1_players)
	return playersData

def extractLabels(contents):
	table = BeautifulSoup(contents).find_all('table', class_='mod-data')
	heads = table[3].find_all('thead')
	headers = heads[1].find_all('tr')[1].find_all('th')[1:]
	headers = [th.text for th in headers]
	columns = ['player'] + headers

	#players = pd.DataFrame(columns=columns)	
	return columns


if __name__ == "__main__":
	site, info, content = siteData('http://sports.espn.go.com/nhl/boxscore?gameId=400484245')

	players = pd.DataFrame(columns=extractLabels(content))
	team1data = extractTable(content)
	for i in range(0,len(team1data)):
		players.loc[i] = team1data[i]

	#players.loc[0] = team1data[0]	
	print players

	#players = pd.DataFrame.append((content))

	#extractTable(content)
	#print players