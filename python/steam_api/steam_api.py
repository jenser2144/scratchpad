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
            list: List dictionaries of player summary data

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
            list: List dictionaries of player summary data

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
