# timeline_detector.py
# Uses Google News RSS to extract geopolitical headlines and entity tags.

import feedparser
import pandas as pd
import spacy
from datetime import datetime

class TimelineDetector:
    def __init__(self, query: str = "Iran"):
        self.query = query
        self.url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        self.nlp = spacy.load("en_core_web_sm")

    def extract_events(self) -> pd.DataFrame:
        feed = feedparser.parse(self.url)
        events = []

        for entry in feed.entries:
            title = entry.title
            summary = entry.get("summary", "")
            published = entry.get("published_parsed")
            date = datetime(*published[:6]) if published else datetime.now()
            link = entry.link

            doc = self.nlp(summary)
            entities = list(set(ent.text for ent in doc.ents if ent.label_ in {"PERSON", "GPE", "ORG", "EVENT"}))

            events.append({
                "date": date.date(),
                "title": title,
                "entities": entities,
                "source": link
            })

        if not events:
            print("No RSS articles found.")
            return pd.DataFrame()

        return pd.DataFrame(events).sort_values("date", ascending=False).reset_index(drop=True)