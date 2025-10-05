import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
import nltk
import numpy as np
import os
import re

# --- 1. KONFIGURASI DAN SETUP OFFLINE ---
try:
    # Memastikan file stopwords sudah diunduh (hanya perlu sekali)
    nltk.download('stopwords', quiet=True) 
    from nltk.corpus import stopwords
except Exception as e:
    print(f"❌ ERROR: Gagal memuat NLTK atau stopwords. Pastikan NLTK terinstal dan sudah diunduh. {e}")
    exit()

# File input (mengandung kolom 'translated' dan 'Platform')
FILE_PATH = 'data_komentar_gabungan_final.csv'
COLUMN_TEXT_TO_ANALYZE = 'translated' # <-- KUNCI: Menganalisis teks Bahasa Inggris

# Stopwords Inggris dan tambahan domain
english_stopwords = set(stopwords.words('english'))
custom_stopwords = english_stopwords.union(set(['wlb', 'work', 'life', 'balance', 'job', 'just', 'get', 'like', 'one', 'really']))


# --- 2. MUAT DATA ---
try:
    df = pd.read_csv(FILE_PATH)
    df[COLUMN_TEXT_TO_ANALYZE] = df[COLUMN_TEXT_TO_ANALYZE].astype(str).fillna('')
    df = df[df[COLUMN_TEXT_TO_ANALYZE].str.strip() != '']
    is_platform_available = 'Platform' in df.columns
    print(f"✅ Data berhasil dimuat. Total komentar: {len(df)}")
except FileNotFoundError:
    print(f"❌ Error: File '{FILE_PATH}' tidak ditemukan.")
    exit()


# --- 3. FUNGSI ANALISIS SENTIMEN LOKAL (TextBlob) ---

def analyze_sentiment_textblob(text):
    """Analisis sentimen sederhana TextBlob (khusus English)."""
    if not text.strip():
        return "neutral"
    
    # TextBlob membutuhkan string, dan akan otomatis membersihkan beberapa karakter
    analysis = TextBlob(text)
    
    # Ambang batas polaritas (bisa disesuaikan)
    if analysis.sentiment.polarity > 0.1:
        return "positive"
    elif analysis.sentiment.polarity < -0.1:
        return "negative"
    return "neutral"

# Lakukan Analisis Sentimen
df["Sentiment"] = df[COLUMN_TEXT_TO_ANALYZE].apply(analyze_sentiment_textblob)

print("\n--- Hasil Sentimen Global (TextBlob) ---")
sentimen_dist = df['Sentiment'].value_counts(normalize=True) * 100
print("Distribusi Sentimen (%):")
print(sentimen_dist.round(2))


# --- 4. ANALISIS FREKUENSI KATA & WORDCLOUD ---

# Gabungkan semua kata
all_words = " ".join(df[COLUMN_TEXT_TO_ANALYZE]).lower()
# Tokenisasi sederhana (memecah berdasarkan spasi) dan filtering stopwords/panjang
all_words_list = re.findall(r'\b\w+\b', all_words) # Lebih baik dari split()
filtered_words = [w for w in all_words_list if w not in custom_stopwords and len(w) > 2]
word_freq = Counter(filtered_words).most_common(100)

# Simpan frekuensi kata
pd.DataFrame(word_freq, columns=["word", "frequency"]).to_csv("word_frequency_results.csv", index=False)
print("✅ Frekuensi kata disimpan ke 'word_frequency_results.csv'")

# Fungsi Word Cloud
def generate_wordcloud(word_frequency_dict, title, color_map='viridis'):
    wc = WordCloud(width=1000, height=500, background_color='white',
                   colormap=color_map, max_words=100).generate_from_frequencies(word_frequency_dict)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=18)
    plt.show()

# Word Cloud Keseluruhan (gunakan 100 kata teratas)
generate_wordcloud(dict(word_freq), "Word Cloud: Kata Kunci Utama (Offline)", 'Blues')


# --- 5. ANALISIS TREN (Perbandingan Platform) ---

if is_platform_available:
    print("\n--- Hasil Tren: Komparasi Platform ---")
    
    platform_sentiment = df.groupby('Platform')['Sentiment'].value_counts(normalize=True).mul(100).unstack(fill_value=0)

    print("Distribusi Sentimen (%) per Platform:")
    print(platform_sentiment.round(2))

    # Visualisasi Tren Sentimen per Platform (Bar Chart)
    platform_sentiment.plot(kind='bar', figsize=(10, 6))
    plt.title('Perbandingan Distribusi Sentimen WLB Berdasarkan Platform (Offline)')
    plt.ylabel('Persentase Komentar (%)')
    plt.xlabel('Platform')
    plt.xticks(rotation=0)
    plt.legend(title='Sentimen')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.show()
else:
    print("\n--- Analisis Tren Dilewati: Kolom 'Platform' tidak ditemukan. ---")

# 6. Simpan Hasil Akhir
df.to_csv('hasil_analisis_offline_final.csv', index=False)
print(f"\n🎉 Proses Selesai! Hasil lengkap disimpan di 'hasil_analisis_offline_final.csv'")