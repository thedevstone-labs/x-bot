import asyncio
from typing import List

from twikit import Tweet

from scraper import Scraper
from utils import init_logger, load_config


async def main():
    init_logger()
    self__config = load_config()
    scraper: Scraper = Scraper(self__config.auth, skip_login=True)
    await scraper.login()
    tweets: List[Tweet] = await scraper.get_tweets(self__config.scraper.query,
                                                   self__config.scraper.tweet_number)
    scraper.save_tweets(tweets)


if __name__ == '__main__':
    asyncio.run(main())
