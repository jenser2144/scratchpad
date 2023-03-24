import csv
import json

import requests

class SteamApi:
    """Class to interact with Steam API"""

    def __init__(self, api_key: str):
        """Instantiate SteamApi class

        Args:
            api_key (str): Steam API key

        Returns:

        """

        self.api_key = api_key
        self.base_url = "http://api.steampowered.com"

    def get_player_summaries(self, steamid: str) -> list:
        """Get player summaries

        Args:
            steamid (str): Steam player id

        Returns:
            list: List of dictionaries of player summary data

        """

        url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v0002/"
        querystring = {
            "key": self.api_key,
            "steamids": steamid
        }

        payload = ""
        response = requests.get(
            url=url,
            data=payload,
            params=querystring
        )

        return json.loads(response.text)

    def get_friend_list(self, steamid: str) -> list:
        """Get friends list

        Args:
            steamid (str): Steam player id

        Returns:
            list: List of dictionaries of player summary data

        """

        url = f"{self.base_url}/ISteamUser/GetFriendList/v0001/"
        querystring = {
            "key": self.api_key,
            "steamid": steamid,
            "relationship": "friend"
        }

        payload = ""
        response = requests.get(
            url=url,
            data=payload,
            params=querystring
        )

        return json.loads(response.text)

    def get_owned_games(self, steamid: str) -> dict:
        """Get owned games

        Args:
            steamid (str): Steam player id

        Returns:
            dict: Dictionary containing list of owned games

        """

        url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
        querystring = {
            "key": self.api_key,
            "steamid": steamid,
            "format": "json"
        }

        payload = ""
        response = requests.get(
            url=url,
            data=payload,
            params=querystring
        )

        return json.loads(response.text)

    def get_achievements(self, steamid: str, gameid: str) -> dict:
        """Get achievements for a game

        Args:
            steamid (str): Steam player id
            gameid (str): Game id

        Returns:
            dict: Dictionary containing list of achievements for the game
        """

        url = f"{self.base_url}/ISteamUserStats/GetPlayerAchievements/v1"
        querystring = {
            "appid": gameid,
            "key": self.api_key,
            "steamid": steamid
        }

        payload = ""
        response = requests.get(
            url=url,
            data=payload,
            params=querystring
        )

        return json.loads(response.text)
