import scrapy
from typing import Generator

class SteamDiscussion(scrapy.Spider):

    name = "steam_discussion"

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        urls = [
            'https://steamcommunity.com/app/730/tradingforum/',
            'https://steamcommunity.com/groups/CSGOTrader/discussions',
            'https://steamcommunity.com/groups/CS2Trading/discussions'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        post_discussion = response.css('a.forum_topic_overlay')

        for post in post_discussion:
            yield response.follow(url=post.attrib['href'], callback=self.get_post)

    def get_post(self, response):
        link = response.css('div.forum_op_header a.popup_menu_item.tight')
        view_post = link.css('a:contains("View Posts")').css('::attr(href)').get()
        steam_profile = link.css('a:contains("View Profile")').css('::attr(href)').get()
        yield response.follow(url=view_post, callback=self.number_post, meta={'steam_profile': steam_profile})

    def number_post(self, response):
        steam_profile = response.meta.get('steam_profile')
        max_post_length = 3

        if len(response.css('div.searchresult_matches')) <= max_post_length:
            # Scrape the posts using the provided steam_profile URL
            # ...
            # Replace the following print statement with your scraping logic
            print(f"Scraping posts from {steam_profile}")
        else:
            print("Number of posts exceeds the maximum length.")

        # Continue with the rest of your code
