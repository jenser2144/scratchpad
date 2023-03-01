import csv
from os import environ
from pathlib import Path

from steam_api import SteamApi

steam_api_key = environ.get("STEAM_API_KEY")
steamid = "76561198056269216"

sa = SteamApi(
    api_key=steam_api_key
)

player_summary_response = sa.get_player_summaries(
    steamid=steamid
)

downloads_dir = Path.home() / "Downloads"

# Write player summary results to csv file
with open(f"{downloads_dir}/steam_player_summaries.csv", "w") as f:
    writer = csv.writer(f)
    for i, player in enumerate(player_summary_response.get("response").get("players")):
        if i == 0:
            writer.writerow(player.keys())
        writer.writerow(player.values())

friend_list_response = sa.get_friend_list(
    steamid=steamid
)

with open(f"{downloads_dir}/steam_friends_list.csv", "w") as f:
    writer = csv.writer(f)
    for i, friend in enumerate(friend_list_response.get("friendslist").get("friends")):
        if i == 0:
            writer.writerow(friend.keys())
        writer.writerow(friend.values())
