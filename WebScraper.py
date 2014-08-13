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

def extractTable(html, number):
	playersData = []
	table = BeautifulSoup(html).find_all('table', class_='mod-data')
	heads = table[3].find_all('thead')
	bodies = table[3].find_all('tbody')[number].find_all('tr')
	for i in range(0,len(bodies)):
		data = [td.text for td in bodies[i]]
		playersData.append(data)

	frame = pd.DataFrame(playersData[0])
	return playersData

def extractLabels(contents):
	table = BeautifulSoup(contents).find_all('table', class_='mod-data')
	heads = table[3].find_all('thead')
	headers = heads[1].find_all('tr')[1].find_all('th')[1:]
	headers = [th.text for th in headers]
	columns = ['player'] + headers
	
	return columns

def returnData(webPage):
	site, info, content = siteData(webPage)

	away_team = pd.DataFrame(columns=extractLabels(content))
	home_team = pd.DataFrame(columns=extractLabels(content))
	away_team_data = extractTable(content,0)
	home_team_data = extractTable(content,2)
	for i in range(0,len(home_team_data)):
		home_team.loc[i] = home_team_data[i]
	for i in range(0,len(away_team_data)):
		away_team.loc[i] = away_team_data[i]	
	
	return away_team, home_team

def getGameInfo(webPage):
	site, info, content = siteData(webPage)

	Date = ""
	homeTeam = ""
	awayTeam = ""

	table = BeautifulSoup(content).find_all('div', class_='matchup ')
	teams = [h3.text for h3 in table]
	rawTeams = teams[0].replace(")", " ").split(" ")
	
	if rawTeams[0] == "Red" or rawTeams[0] == "Blue" or rawTeams[0] == "Maple":
		awayTeam = rawTeams[0]
		homeTeam = rawTeams[5]
	else:
		awayTeam = rawTeams[0]
		homeTeam = rawTeams[4]
	
	table2 = BeautifulSoup(content).find_all('div', class_='game-time-location')
	date = table2[0].find('p')
	Date = date.text

	return Date, homeTeam, awayTeam

if __name__ == "__main__":
	
	template = 'http://sports.espn.go.com/nhl/boxscore?gameId='
	gameId = 400484252

	for i in range(0,3):
		WebPage = template + str(gameId)

		date, home, away = getGameInfo(WebPage)
		away_team, home_team = returnData(WebPage)
		
		away_team['TEAM'] = away
		away_team['DATE'] = date
		away_team['TYPE'] = 'Away'
		away_team['OPPONENT'] = home

		home_team['TEAM'] = home
		home_team['DATE'] = date
		home_team['TYPE'] = 'Home'
		home_team['OPPONENT'] = away

		print away_team
		print home_team
		gameId += 1
