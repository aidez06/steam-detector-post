# ignition_bot.py

import time

from scrapy.crawler import CrawlerProcess
from steam_detector_post.steam_detector_post.spiders.steam_discussion import SteamDiscussion

while True:
    # Instantiate the crawler process and configure the settings
    process = CrawlerProcess(settings={
        'DOWNLOAD_DELAY': 60,  # Set the delay to 60 seconds (1 minute)
        'LOG_ENABLED': False,  # Disable logging (optional)
    })

    # Add your spider to the process
    process.crawl(SteamDiscussion)

    # Start the crawling process
    process.start()

    # Wait for the specified interval before running the spider again
    time.sleep(60)  # Sleep for 60 seconds (1 minute) before the next run
