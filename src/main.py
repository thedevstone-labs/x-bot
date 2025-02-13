import asyncio
from pathlib import Path
from typing import List

from twikit import Tweet

from analyzer import Analyzer
from scraper import Scraper
from utils import get_path, init_logger, load_config


async def main():
    init_logger()
    self__config = load_config()
    tweet_path: Path = get_path("./tweets.csv")
    # Scraping
    # scraper: Scraper = Scraper(self__config.auth, skip_login=True)
    # await scraper.login()
    # tweets: List[Tweet] = await scraper.get_tweets(self__config.scraper.query,
    #                                                self__config.scraper.tweet_number)
    #
    # scraper.save_tweets(tweets, tweet_path)
    # Data Analysis
    analyzer: Analyzer = Analyzer(tweet_path)


if __name__ == '__main__':
    asyncio.run(main())
