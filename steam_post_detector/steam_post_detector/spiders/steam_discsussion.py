import scrapy
from typing import Generator

class SteamDiscussion(scrapy.Spider):
    
    name = "steam_discussion"
    
    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        """You may include any steam discussions to be extracted inside on the array"""
        allowed_domains = ['https://steamcommunity.com']
        urls = [
            'https://steamcommunity.com/app/730/tradingforum/',
            'https://steamcommunity.com/groups/CSGOTrader/discussions'
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        # Your parsing logic goes here
        pass
