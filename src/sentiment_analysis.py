# sentiment_analysis.py
# Uses Hugging Face transformers to analyze text sentiment.

from transformers import pipeline
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis")
        print("Device set to use", self.classifier.device)

    def clean_text(self, text: str) -> str:
        return " ".join(text.split()).strip()

    def analyze(self, texts: list[str]) -> pd.DataFrame:
        cleaned = [self.clean_text(t) for t in texts if t]
        predictions = self.classifier(cleaned)
        return pd.DataFrame({
            "text": cleaned,
            "label": [pred["label"] for pred in predictions],
            "score": [pred["score"] for pred in predictions]
        })