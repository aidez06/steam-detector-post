import requests
import re
import xml.etree.ElementTree as ET

class SteamDataFetcher:
    api_calls = 0

    def __init__(self,api_key:str,steam_profile:str) -> None:
        self.api_key = api_key
        self.steam_profile = steam_profile
        steam_id_64 = self.convert_url_to_steamid64()

    def convert_url_to_steamid64(self,custom_url):
        url = f"https://steamcommunity.com/id/{custom_url}?xml=1"
        response = requests.get(url)
        if "https://steamcommunity.com/id/" in url: 
            if response.status_code == 200:
                xml_data = response.content
                root = ET.fromstring(xml_data)
                steamid64 = root.find("steamID64").text
                return steamid64
            else:
                return None
        else:
            steamid64 = re.search(r"\d+", url).group()
            return steamid64
    def get_csgo_playtime(self):
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.api_key}&steamid={self.steam_id}&format=json"
        response = requests.get(url)
        self.number_api_calls()

        if response.status_code == 200:
            data = response.json()
            games = data["response"]["games"]

            csgo = next((game for game in games if game["appid"] == 730), None)
            if csgo:
                playtime_forever = csgo["playtime_forever"] / 60
               
                return playtime_forever 
            else:
                return None, None
        else:
            return None, None
    @staticmethod
    def number_api_calls():
        SteamDataFetcher.api_calls +=1

    
    

