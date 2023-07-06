import scrapy
from typing import Generator
from steam_detector_post.items import SteamDetectorPostItem
from scrapy.dupefilters import RFPDupeFilter

class SteamDiscussion(scrapy.Spider):

    name = "steam_discussion"

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        urls = [
            'https://steamcommunity.com/app/730/tradingforum/',
            'https://steamcommunity.com/groups/CSGOTrader/discussions',
            'https://steamcommunity.com/groups/CS2Trading/discussions'
        ]
        custom_settings = {
            'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
            'DUPEFILTER_DEBUG': True,  # Enable debug mode to see when duplicates are filtered
            'FEEDS': {'data_saved.json': {'format': 'json', 'overwrite': True}}
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        post_discussion = response.css('a.forum_topic_overlay')

        for index,post  in enumerate(post_discussion):
            title = response.css('div.forum_topic_name')[index]
            text = [t.strip() for t in title.css('::text').extract()]
            text = [t for t in text if t]  # Remove empty strings
            title_post = text[0]
            print(title_post)

            yield response.follow(url=post.attrib['href'], callback=self.get_post, meta={'title_post':  title_post})

    def get_post(self, response):
        title_post = response.meta.get('title_post')
        link = response.css('div.forum_op_header a.popup_menu_item.tight')
        view_post = link.css('a:contains("View Posts")').css('::attr(href)').get()
        steam_profile = link.css('a:contains("View Profile")').css('::attr(href)').get()
        yield response.follow(url=view_post, callback=self.number_post, meta={'steam_profile': steam_profile,'title_post': title_post})

    def number_post(self, response):
        post_item = SteamDetectorPostItem()
        title_post = response.meta.get('title_post')
        steam_profile = response.meta.get('steam_profile')
        max_post_length = 1

        if len(response.css('div.searchresult_matches')) <= max_post_length:
            post_item['title'] = title_post
            post_item['profile'] = steam_profile
            yield post_item
