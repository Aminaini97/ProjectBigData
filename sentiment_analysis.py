import pandas as pd
from transformers import pipeline
import os

os.makedirs("../data/final", exist_ok=True)

df = pd.read_csv("../data/cleaned/reddit_cleaned.csv")

print("🧠 Memuat model IndoBERT...")
analyzer = pipeline("sentiment-analysis", model="indobenchmark/indobert-base-p1")

def analyze_sentiment(text):
    try:
        if not text or text.strip() == "":
            return "NETRAL"
        result = analyzer(text[:512])[0]  # Batasi ke 512 token
        return result["label"].upper()
    except Exception as e:
        print("⚠️ Error analisis:", e)
        return "NETRAL"

df["sentiment"] = df["cleaned_text"].apply(analyze_sentiment)
df.to_csv("../data/final/reddit_sentiment.csv", index=False)

print("✅ Analisis sentimen selesai. Hasil disimpan ke /data/final/")
