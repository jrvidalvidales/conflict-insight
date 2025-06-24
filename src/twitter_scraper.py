# twitter_scraper.py
# Fetches tweets via Twitter API v2 using Tweepy.
# You’ll need a free Twitter Developer bearer token. This will go in your .env
# https://developer.x.com/en/portal/dashboard

import tweepy
from src.sentiment_analysis import SentimentAnalyzer
from typing import List

class TwitterScraper:
    def __init__(self, bearer_token: str):
        self.client = tweepy.Client(bearer_token=bearer_token)

    def fetch_tweets(self, query: str, max_results: int = 10) -> List[str]:
        tweets = self.client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["text", "lang"]
        )
        if not tweets.data:
            return []
        return [t.text for t in tweets.data if t.lang == "en"]