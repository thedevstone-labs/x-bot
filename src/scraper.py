import asyncio
import csv
import os
from datetime import datetime
from random import randint
from typing import List

from twikit import Client, TooManyRequests, Tweet
from twikit.utils import Result

from utils import load_config


def save_tweets(tweets: List[Tweet]) -> None:
    """
    Save the tweets
    :param tweets: the list of tweets
    """
    csv_file = "./tweets.csv"
    header = ["Tweet_count", "Username", "Text", "Created At", "Retweets",
              "Likes"]
    file_exists = os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0
    with open("./tweets.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        for idx, tweet in enumerate(tweets):
            writer.writerow([idx, tweet.user.name, tweet.text,
                             tweet.created_at, tweet.retweet_count,
                             tweet.favorite_count])


async def get_tweets(client: Client, query: str, tweet_number: int = 100) -> \
        List[Tweet]:
    tweets_result: Result[Tweet] | None = None
    tweets: List[Tweet] = []
    batch_size = 20
    tweet_count = 0
    while tweet_count < tweet_number:
        try:
            if not tweets:
                print(f'{datetime.now()} - Getting {batch_size} tweets...')
                tweets_result = await client.search_tweet(query,
                                                          product='Top',
                                                          count=batch_size)
            else:
                wait_time = randint(5, 10)
                print(
                    f'{datetime.now()} - Getting next {batch_size} tweets after {wait_time} seconds ...')
                await asyncio.sleep(wait_time)
                tweets_result = await tweets_result.next()
            # To list
            for tweet in tweets_result:
                tweets.append(tweet)

            tweet_count += batch_size
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(
                f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

    return tweets


async def main():
    # Parameters
    tweet_number = 100
    skip_login = False
    query = "Sanremo 2025"

    # Config load
    config = load_config()

    # Client
    client = Client(language='en-US')
    if skip_login:
        await client.login(auth_info_1=config['username'],
                           auth_info_2=config['email'],
                           password=config['password'])
        client.save_cookies('cookies.json')

    client.load_cookies('cookies.json')

    tweets: List[Tweet] = await get_tweets(client, query, tweet_number)
    save_tweets(tweets)


if __name__ == '__main__':
    asyncio.run(main())
