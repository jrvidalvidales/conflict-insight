# run_pipeline.py
# Main pipeline for Conflict Insight:
# - Loads credentials
# - Fetches Twitter, Reddit, and Timeline data
# - Runs sentiment analysis
# - Exports results to outputs/ folder

import os
import time
import pandas as pd
from dotenv import load_dotenv
from tweepy.errors import TooManyRequests
from src.twitter_scraper import TwitterScraper
from src.reddit_scraper import RedditScraper
from src.sentiment_analysis import SentimentAnalyzer
from src.timeline_detector import TimelineDetector

# Load environment variables
load_dotenv()

# === Ensure outputs folder exists ===
os.makedirs("outputs", exist_ok=True)

# === Credentials ===
twitter_token = os.getenv("TWITTER_BEARER_TOKEN")
reddit_id = os.getenv("REDDIT_CLIENT_ID")
reddit_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_agent = os.getenv("REDDIT_USER_AGENT")

# === Initialize Components ===
print("Initializing data scrapers and sentiment engine...")
twitter = TwitterScraper(bearer_token=twitter_token)
reddit = RedditScraper(client_id=reddit_id, client_secret=reddit_secret, user_agent=reddit_agent)
analyzer = SentimentAnalyzer()

# === Twitter Sentiment ===
print("\nFetching tweets about 'Iran Israel conflict'...")
try:
    tweets = twitter.fetch_tweets("Iran Israel conflict", max_results=10)
except TooManyRequests:
    print("Rate limit hit. Waiting 15 minutes...")
    time.sleep(900)
    tweets = twitter.fetch_tweets("Iran Israel conflict", max_results=10)

if tweets:
    df_twitter = analyzer.analyze(tweets)
    df_twitter.to_csv("outputs/twitter_sentiment.csv", index=False)
    print("Saved Twitter sentiment to outputs/twitter_sentiment.csv")
else:
    print("No tweets found.")

# === Reddit Sentiment ===
print("\nFetching Reddit posts from r/worldnews...")
reddit_posts = reddit.fetch_titles("worldnews", limit=10)

if reddit_posts:
    df_reddit = analyzer.analyze(reddit_posts)
    df_reddit.to_csv("outputs/reddit_sentiment.csv", index=False)
    print("Saved Reddit sentiment to outputs/reddit_sentiment.csv")
else:
    print("No Reddit posts found.")

# === Timeline Extraction & Sentiment ===
print("\nScraping headlines and extracting timeline events...")
timeline = TimelineDetector(query="Israel OR Iran OR Gaza")
df_timeline = timeline.extract_events()

if not df_timeline.empty:
    print(f"Extracted {len(df_timeline)} timeline events. Running sentiment analysis...")
    df_sentiment = analyzer.analyze(df_timeline["title"].tolist())
    df_combined = df_timeline.join(df_sentiment[["label", "score"]])
    df_combined.to_csv("outputs/timeline_sentiment.csv", index=False)
    print("Saved timeline sentiment to outputs/timeline_sentiment.csv")
else:
    print("No timeline events extracted.")
