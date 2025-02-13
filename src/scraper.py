import asyncio
import csv
import logging
from datetime import datetime
from pathlib import Path
from random import randint
from typing import List

from twikit import Client, TooManyRequests, Tweet
from twikit.utils import Result

from utils import Auth, get_path

logger = logging.getLogger(__file__)


class Scraper:
    def __init__(self, auth: Auth, skip_login: bool = False):
        # Config load
        self.__auth: Auth = auth
        self.__skip_login: bool = skip_login
        self.__client = Client(language='en-US')

    async def login(self):
        """
        Login with client
        """
        cookie_path = get_path('cookies.json').as_posix()
        if self.__skip_login:
            await self.__client.login(auth_info_1=self.__auth.username,
                                      auth_info_2=self.__auth.email,
                                      password=self.__auth.password)
            self.__client.save_cookies(cookie_path)

        self.__client.load_cookies(cookie_path)

    @staticmethod
    def save_tweets(tweets: List[Tweet], csv_path: Path) -> None:
        """
        Save the tweets
        :param tweets: the list of tweets
        :param csv_path: the csv path
        """
        header = ["id", "username", "text", "created_at", "retweets",
                  "likes"]
        with csv_path.open("w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for idx, tweet in enumerate(tweets):
                writer.writerow([idx, tweet.user.name, tweet.text,
                                 tweet.created_at, tweet.retweet_count,
                                 tweet.favorite_count])
        logger.info("Saving complete")

    async def get_tweets(self, query: str, tweet_number: int = 100) -> \
            List[Tweet]:
        """
        Get the tweets
        :param query: the query
        :param tweet_number: the number of tweets
        :return: the list of tweets
        """
        tweets_result: Result[Tweet] | None = None
        tweets: List[Tweet] = []
        batch_size = 20
        tweet_count = 0
        while tweet_count < tweet_number:
            try:
                if not tweets:
                    logger.info(
                        f'{datetime.now()} - Getting {batch_size} tweets...')
                    tweets_result = await self.__client.search_tweet(query,
                                                                     product='Top',
                                                                     count=batch_size)
                else:
                    wait_time = randint(5, 10)
                    logger.info(
                        f'{datetime.now()} - Got {tweet_count} tweets: getting next {batch_size} tweets after {wait_time} seconds ...')
                    await asyncio.sleep(wait_time)
                    tweets_result = await tweets_result.next()
                # To list
                for tweet in tweets_result:
                    tweets.append(tweet)

                tweet_count += batch_size
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                logger.info(
                    f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
                wait_time = rate_limit_reset - datetime.now()
                await asyncio.sleep(wait_time.total_seconds())
                continue

            if not tweets:
                logger.info(f'{datetime.now()} - No more tweets found')
                break

        return tweets
