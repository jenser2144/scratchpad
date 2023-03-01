import csv
from os import environ

from steam_api import SteamApi

steam_api_key = environ.get("STEAM_API_KEY")

sa = SteamApi(
    api_key=steam_api_key
)

player_summary_response = sa.get_player_summaries(
    steamid="76561198056269216"
)

# Write player summary results to csv file
with open("/Users/joseph.enser/Downloads/steam_player_summaries.csv", "w") as f:
    writer = csv.writer(f)
    for i, player in enumerate(player_summary_response.get("response").get("players")):
        if i == 0:
            writer.writerow(player.keys())
        writer.writerow(player.values())
