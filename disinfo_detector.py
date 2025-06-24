# disinfo_detector.py
# Flags potential disinformation in text content using basic heuristics

import re
import pandas as pd

def score_disinfo(text):
    score = 0
    text_lower = text.lower()

    # Heuristics: Punctuation and formatting
    if re.search(r"[!?]{3,}", text): score += 0.2
    if text.isupper() and len(text) > 10: score += 0.2

    # Language patterns often used in misinformation
    clickbait_terms = ["shocking", "you won't believe", "hidden agenda", "what they don't want you to know"]
    conspiracy_terms = ["deep state", "false flag", "great reset", "crisis actor", "chemtrails"]

    if any(term in text_lower for term in clickbait_terms): score += 0.3
    if any(term in text_lower for term in conspiracy_terms): score += 0.3

    # Denial or undermining truth
    if re.search(r"\b(not (true|real|verified|fact))\b", text_lower): score += 0.2

    return min(score, 1.0)

def detect_disinfo(df, text_column="text", threshold=0.5):
    df["disinfo_score"] = df[text_column].apply(score_disinfo)
    df["disinfo_flag"] = df["disinfo_score"] >= threshold
    return df