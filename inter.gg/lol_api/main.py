import json
import sys
from dotenv import load_dotenv
import requests
import pandas as pd
import os

load_dotenv()
api_key = os.getenv("api_key")
base_url = "https://euw1.api.riotgames.com"
seconde_base_url = "https://europe.api.riotgames.com"


class Account:
	def __init__(self, username):
		self.id = None
		self.games = []
		self.username = username

	def get_id(self):
		method_pseudo = "/lol/summoner/v4/summoners/by-name/"
		url_pseudo = base_url + method_pseudo + self.username + "?api_key=" + api_key
		api_response_text = requests.get(url_pseudo).text
		api_response_json = json.loads(api_response_text)
		print(api_response_json)
		self.id = api_response_json["puuid"]


def get_x_last_games(id, x):
	method_match = f"/lol/match/v5/matches/by-puuid/{id}/ids" + "?start=0&count=" + str(x) + "&api_key=" + api_key
	url_match = seconde_base_url + method_match
	api_response_text = requests.get(url_match).text
	return json.loads(api_response_text)


def get_match_data(Account):
	method_data_match = "/lol/match/v5/matches/"
	win = 0
	for id in Account.games:
		url_data_match = seconde_base_url + method_data_match + id + "?api_key=" + api_key
		api_response_text = requests.get(url_data_match).text
		api_response_json = json.loads(api_response_text)
		participants_list = api_response_json["metadata"]["participants"]
		for index, participant in enumerate(participants_list):
			if participant == Account.id:
				position = index
		df = pd.DataFrame(api_response_json["info"]["participants"])
		if (df["win"][position] == True):
			win += 1
	winrate = win / len(Account.games) * 100
	return(f"Winrate : {winrate} %")


if __name__ == '__main__':
	Account = Account(sys.argv[1])
	Account.get_id()
	Account.games = get_x_last_games(Account.id, sys.argv[2])
	get_match_data(Account)
