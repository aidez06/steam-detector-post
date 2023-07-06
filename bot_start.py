import time
from steam_detector_post.steam_detector_post.spiders.steam_discussion import SteamDiscussion

while True:
    spider = SteamDiscussion()
    spider.start_requests()

    # Wait for the specified interval before running the spider again
    time.sleep(60)  # Sleep for 60 seconds (1 minute) before the next run
