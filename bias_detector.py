# bias_detector.py
# Automates submission of article text to IsItCap.com to extract media bias analysis

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def init_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    return webdriver.Chrome(options=chrome_options)

def get_bias_analysis(text, wait_time=10):
    driver = init_browser()
    driver.get("https://isitcap.com")

    try:
        # Find and fill textarea
        textarea = driver.find_element(By.ID, "fake-news-input")
        textarea.clear()
        textarea.send_keys(text)
        textarea.send_keys(Keys.RETURN)
        time.sleep(wait_time)  # let model run

        # Extract results
        bias_label = driver.find_element(By.ID, "bias-level").text
        confidence = driver.find_element(By.ID, "bias-confidence").text
        framing = driver.find_element(By.ID, "framing-feedback").text

        return {
            "bias_label": bias_label,
            "bias_confidence": confidence,
            "framing_summary": framing
        }

    except Exception as e:
        print("Error getting bias analysis:", e)
        return {
            "bias_label": None,
            "bias_confidence": None,
            "framing_summary": None
        }

    finally:
        driver.quit()

def apply_bias_detection(df, text_column="text", sample_limit=None):
    results = []
    for idx, row in df.iterrows():
        if sample_limit and idx >= sample_limit:
            break
        print(f"Analyzing bias for row {idx + 1}...")
        analysis = get_bias_analysis(row[text_column][:2000])  # limit input length
        results.append(analysis)

    bias_df = pd.DataFrame(results)
    return pd.concat([df.reset_index(drop=True), bias_df], axis=1)