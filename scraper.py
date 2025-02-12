import asyncio

from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

MINIMUM_TWEETS = 10
QUERY = '(from:elonmusk) lang:en until:2020-01-01 since:2018-01-01'


async def get_tweets(client, tweets):
    if tweets is None:
        # * get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(
            f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets


# * login credentials
email = "beboy27375@owlny.com"
password = "*J&pw%iE3SvQcypxh"
username = "TestDevstone"

# * create a csv file
with open('tweets.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(
        ['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])


async def main():
    # * authenticate to X.com
    # ! 1) use the login credentials. 2) use cookies.
    client = Client(language='en-US')
    await client.login(auth_info_1=username, auth_info_2=email,
                       password=password)
    client.save_cookies('cookies.json')

    client.load_cookies('cookies.json')

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:

        try:
            # tweets = await get_tweets(client, tweets)
            tweets = await client.search_tweet('Sanremo2025', product='Top')
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(
                f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text,
                          tweet.created_at, tweet.retweet_count,
                          tweet.favorite_count]

            with open('tweets.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')


if __name__ == '__main__':
    asyncio.run(main())
