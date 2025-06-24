# reddit_scraper.py
# Retrieves recent post titles from a subreddit using PRAW.
# You’ll need to create a Reddit app to get your client_id, client_secret, and user_agent
# https://www.reddit.com/prefs/apps

import praw
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class RedditScraper:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def fetch_titles(self, subreddit: str, limit: int = 10) -> List[str]:
        try:
            return [
                post.title
                for post in self.reddit.subreddit(subreddit).new(limit=limit)
                if post.title
            ]
        except Exception as e:
            print(f"Reddit fetch error: {e}")
            return []