# geo_mapper.py
# Extracts locations from timeline sentiment data and plots them on an interactive map

import os
import pandas as pd
import spacy
import folium
from geopy.geocoders import Nominatim
from tqdm import tqdm

# Load model and data
nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("outputs/timeline_sentiment.csv")
tqdm.pandas()

# Extract locations from news titles
def extract_location(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "GPE"]

df["locations"] = df["title"].progress_apply(extract_location)
df_exploded = df.explode("locations").dropna(subset=["locations"])

# Geocode each unique place
geolocator = Nominatim(user_agent="conflict-insight")
location_coords = {}

for loc in tqdm(df_exploded["locations"].unique(), desc="Geocoding"):
    try:
        geo = geolocator.geocode(loc)
        if geo:
            location_coords[loc] = (geo.latitude, geo.longitude)
    except:
        continue

# Plot with Folium
m = folium.Map(location=[20, 0], zoom_start=2)

for _, row in df_exploded.iterrows():
    loc = row["locations"]
    coords = location_coords.get(loc)
    if coords:
        color = "#66bb6a" if row["label"] == "POSITIVE" else "#ef5350"
        folium.CircleMarker(
            location=coords,
            radius=6,
            popup=f"{row['title']} ({row['label']})",
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

os.makedirs("outputs", exist_ok=True)
m.save("outputs/sentiment_map.html")
print("Saved interactive map to outputs/sentiment_map.html")