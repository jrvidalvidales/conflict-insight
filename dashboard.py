# dashboard.py
# Streamlit dashboard for sentiment, disinformation, and media bias analysis

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load flagged data
df_twitter = pd.read_csv("outputs/flagged_twitter_sentiment.csv")
df_reddit = pd.read_csv("outputs/flagged_reddit_sentiment.csv")
df_news = pd.read_csv("outputs/flagged_timeline_sentiment.csv")

# Setup
st.set_page_config(page_title="Conflict Insight Dashboard", layout="wide")
st.title("Conflict Insight Dashboard")
st.caption("Sentiment, Disinformation, and Media Bias Analysis from Twitter, Reddit, and Global News")

# === SIDEBAR FILTERS ===
st.sidebar.header("Filters")
disinfo_only = st.sidebar.checkbox("Show disinformation only")
sentiment_filter = st.sidebar.multiselect(
    "Filter by sentiment",
    options=["POSITIVE", "NEGATIVE"],
    default=["POSITIVE", "NEGATIVE"]
)
bias_options = ["Left", "Center", "Right"]
selected_bias = st.sidebar.multiselect(
    "Bias detected in content",
    options=bias_options,
    default=bias_options
)

# === DATA SOURCE TOGGLES ===
st.sidebar.header("Data Sources")
show_twitter = st.sidebar.checkbox("Twitter", value=True)
show_reddit = st.sidebar.checkbox("Reddit", value=True)
show_news = st.sidebar.checkbox("Timeline", value=True)

# === FILTERING FUNCTION ===
def filter_data(df, label_col="label"):
    if disinfo_only and "disinfo_flag" in df.columns:
        df = df[df["disinfo_flag"]]
    if label_col in df.columns:
        df = df[df[label_col].isin(sentiment_filter)]
    if "bias_label" in df.columns:
        df = df[df["bias_label"].isin(selected_bias)]
    return df

df_twitter = filter_data(df_twitter)
df_reddit = filter_data(df_reddit)
df_news = filter_data(df_news, label_col="label")

# === HIGHLIGHTING DISINFO ===
def highlight_disinfo(row):
    if row.get("disinfo_flag"):
        return ["background-color: #ffe6e6"] * len(row)
    return [""] * len(row)

# === SENTIMENT DISTRIBUTION CHARTS ===
st.header("Sentiment Distribution")
chart_cols = []

if show_twitter:
    chart_cols.append(("Twitter", df_twitter))
if show_reddit:
    chart_cols.append(("Reddit", df_reddit))
if show_news:
    chart_cols.append(("Timeline", df_news))

if not chart_cols:
    st.info("No data source selected.")
else:
    col_objs = st.columns(len(chart_cols))
    for col, (label, df) in zip(col_objs, chart_cols):
        with col:
            if df.empty:
                st.warning(f"No data for {label}")
            else:
                fig, ax = plt.subplots()
                df["label"].value_counts().plot(kind="bar", ax=ax, color=["#66bb6a", "#ef5350"])
                ax.set_title(f"{label} Sentiment")
                ax.set_ylabel("Posts")
                st.pyplot(fig)

# === BIAS DISTRIBUTION CHARTS ===
st.header("Media Bias Distribution")
if not chart_cols:
    st.info("No sources available.")
else:
    col_objs = st.columns(len(chart_cols))
    for col, (label, df) in zip(col_objs, chart_cols):
        with col:
            if "bias_label" not in df or df.empty:
                st.warning(f"No bias data for {label}")
            else:
                st.bar_chart(df["bias_label"].value_counts())

# === DATA TABLES WITH BIAS ===
st.header("Flagged Content with Bias")

def render_table(df, source_label, text_col):
    if df.empty:
        st.info(f"No {source_label} posts to display.")
        return

    columns_to_show = [text_col, "label", "disinfo_flag"]
    bias_fields = ["bias_label", "bias_confidence", "framing_summary"]
    for field in bias_fields:
        if field in df.columns:
            columns_to_show.append(field)

    st.subheader(source_label)
    st.dataframe(df[columns_to_show].style.apply(highlight_disinfo, axis=1), use_container_width=True)

if show_twitter:
    render_table(df_twitter, "Twitter", "text")
if show_reddit:
    render_table(df_reddit, "Reddit", "text")
if show_news:
    render_table(df_news, "Timeline News", "title")