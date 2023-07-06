import time
import subprocess

import os
while True:
    # Start the program as a subprocess
    process = subprocess.Popen(["scrapy", "crawl", "steam_discussion"], cwd=f"{os.getcwd()}/steam_detector_post/steam_detector_post/spiders/")

    # Wait for the specified interval
    time.sleep(60)  # Sleep for 60 seconds (1 minute)

    # Terminate the subprocess
    process.terminate()
    process.wait()
