# run_disinfo.py

import pandas as pd
from disinfo_detector import detect_disinfo

sources = ["twitter_sentiment.csv", "reddit_sentiment.csv", "timeline_sentiment.csv"]
input_dir = "outputs"
output_dir = "outputs"

for filename in sources:
    path = f"{input_dir}/{filename}"
    df = pd.read_csv(path)

    # Use 'text' or 'title' depending on source
    text_col = "title" if "timeline" in filename else "text"
    df_flagged = detect_disinfo(df, text_column=text_col)

    out_path = f"{output_dir}/flagged_{filename}"
    df_flagged.to_csv(out_path, index=False)
    print(f"Disinfo detection complete: {out_path}")