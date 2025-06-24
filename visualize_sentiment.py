# visualize_sentiment.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load sentiment CSVs
twitter = pd.read_csv("outputs/twitter_sentiment.csv")
reddit = pd.read_csv("outputs/reddit_sentiment.csv")
timeline = pd.read_csv("outputs/timeline_sentiment.csv")

# Tag each with source
twitter["source"] = "Twitter"
reddit["source"] = "Reddit"
timeline["source"] = "Timeline"

# Combine
df_all = pd.concat([twitter, reddit, timeline], ignore_index=True)

# Plot sentiment distribution by source
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
sns.countplot(data=df_all, x="source", hue="label",
              palette={"POSITIVE": "#66bb6a", "NEGATIVE": "#ef5350"})
plt.title("Sentiment Distribution by Source")
plt.xlabel("Source")
plt.ylabel("Number of Posts")
plt.tight_layout()
plt.savefig("outputs/sentiment_by_source.png")
plt.show()