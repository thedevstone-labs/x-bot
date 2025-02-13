import logging
from pathlib import Path

import pandas as pd
from pandas import DataFrame

logger = logging.getLogger(__file__)


class Analyzer:
    def __init__(self, tweet_path: Path):
        df: DataFrame = pd.read_csv(tweet_path, parse_dates=['created_at'],
                                    dtype={'id': int,
                                           'username': 'string',
                                           'text': 'string',
                                           'retweets': int,
                                           'likes': int})
        df.set_index('id', inplace=True)
        df['created_at'] = pd.to_datetime(df['created_at'])
        print(df.describe())
