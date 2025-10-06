import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from textblob import TextBlob
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt 
import nltk
import numpy as np
import re
import io

# --- 0. Konfigurasi dan Setup ---

st.set_page_config(layout="wide", page_title="Dashboard WLB Indonesia")

try:
    # Memastikan file stopwords sudah diunduh (hanya perlu sekali)
    nltk.download('stopwords', quiet=True) 
    from nltk.corpus import stopwords
except Exception as e:
    st.error(f"❌ ERROR: Gagal memuat NLTK atau stopwords. Pastikan NLTK terinstal dan sudah diunduh.")
    st.stop()

# File input dan kolom
FILE_PATH = 'data_komentar_gabungan_final.csv'
COLUMN_TEXT_TO_ANALYZE = 'translated' 

# >>> PASTIKAN INI ADALAH NAMA KOLOM TANGGAL YANG BENAR DI CSV ANDA <<<
COLUMN_DATE = 'created_utc' 

# Stopwords Inggris dan tambahan domain
english_stopwords = set(stopwords.words('english'))
custom_stopwords = english_stopwords.union(set(['wlb', 'work', 'life', 'balance', 'job', 'just', 'get', 'like', 'one', 'really', 'day', 'time', 'people']))

# --- 1. Fungsi Analisis Data (Cached) ---

@st.cache_data 
def load_and_analyze_data(file_path):
    """Memuat, membersihkan, dan menganalisis data (hanya dijalankan sekali)."""
    try:
        df = pd.read_csv(file_path)
        df[COLUMN_TEXT_TO_ANALYZE] = df[COLUMN_TEXT_TO_ANALYZE].astype(str).fillna('')
        df = df[df[COLUMN_TEXT_TO_ANALYZE].str.strip() != '']
        
        is_platform_available = 'Platform' in df.columns
        is_date_available = COLUMN_DATE in df.columns

        # --- A. Sentimen ---
        def analyze_sentiment_textblob(text):
            if not text.strip(): return "neutral"
            analysis = TextBlob(text)
            if analysis.sentiment.polarity > 0.1: return "positive"
            elif analysis.sentiment.polarity < -0.1: return "negative"
            return "neutral"

        df["Sentiment"] = df[COLUMN_TEXT_TO_ANALYZE].apply(analyze_sentiment_textblob)

        # --- B. Tren Waktu ---
        if is_date_available:
            try:
                # Coba konversi dengan unit='s' (untuk UNIX timestamp)
                df['Date'] = pd.to_datetime(df[COLUMN_DATE], unit='s', errors='coerce') 
                
                # Jika semua gagal, coba lagi tanpa unit='s' (untuk string tanggal standar)
                if df['Date'].isnull().all():
                     df['Date'] = pd.to_datetime(df[COLUMN_DATE], errors='coerce')

                df.dropna(subset=['Date'], inplace=True)
                
                if df.empty:
                    st.warning("Semua data tanggal tidak valid dan dihapus. Analisis tren dibatalkan.")
                    is_date_available = False
                else:
                    df['is_negative'] = np.where(df['Sentiment'] == 'negative', 1, 0)
                    df['Date_M'] = df['Date'].dt.to_period('M').astype(str) # Agregasi bulanan
            except Exception as e:
                 st.error(f"Gagal memproses kolom tanggal '{COLUMN_DATE}'. Error: {e}")
                 is_date_available = False
        
        # --- C. Frekuensi Kata ---
        all_words = " ".join(df[COLUMN_TEXT_TO_ANALYZE]).lower()
        all_words_list = re.findall(r'\b\w+\b', all_words)
        filtered_words = [w for w in all_words_list if w not in custom_stopwords and len(w) > 2]
        word_freq = Counter(filtered_words).most_common(50)
        
        return df, word_freq, is_platform_available, is_date_available
        
    except FileNotFoundError:
        st.error(f"❌ Error: File '{file_path}' tidak ditemukan. Pastikan file ada.")
        st.stop()
        return pd.DataFrame(), [], False, False

# --- 2. EKSEKUSI DATA LOADING ---

# Variabel hasil analisis akan di-unpack di sini
df_analyzed, word_frequency, is_platform_available, is_date_available = load_and_analyze_data(FILE_PATH) 

if df_analyzed.empty:
    st.stop()

st.title("Dashboard Analisis Tren Work-Life Balance (Indonesia) 🇮🇩")
st.markdown("Visualisasi Sentimen, Frekuensi Kata, dan Tren Waktu dari data gabungan.")

# --- 3. VISUALISASI ---

col1, col2 = st.columns(2)

# =========================================================================
# VISUALISASI 1: DISTRIBUSI SENTIMEN GLOBAL (PIE CHART)
# =========================================================================
with col1:
    st.subheader("1. Distribusi Sentimen Global")
    sentiment_counts = df_analyzed['Sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    
    color_map = {'positive': 'mediumseagreen', 'negative': 'red', 'neutral': 'gray'}
    
    fig_pie = px.pie(sentiment_counts, 
                     names='Sentiment', 
                     values='Count', 
                     title='Proporsi Sentimen Keseluruhan',
                     color='Sentiment',
                     color_discrete_map=color_map)
    st.plotly_chart(fig_pie, use_container_width=True)

# =========================================================================
# VISUALISASI 2: FREKUENSI KATA (BAR CHART)
# =========================================================================
with col2:
    st.subheader("2. Kata Kunci Paling Sering Muncul")
    
    word_df = pd.DataFrame(word_frequency, columns=["word", "frequency"])
    fig_bar = px.bar(word_df.head(15), 
                     x='word', 
                     y='frequency', 
                     color='frequency',
                     title='Top 15 Kata Kunci Terkait WLB',
                     color_continuous_scale=px.colors.sequential.Plasma_r)
    fig_bar.update_xaxes(title_text="Kata Kunci")
    fig_bar.update_yaxes(title_text="Frekuensi")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---") 



# =========================================================================
# VISUALISASI 4: SENTIMEN PER PLATFORM (STACKED BAR CHART)
# =========================================================================
if is_platform_available:
    st.subheader("3. Komposisi Sentimen Berdasarkan Platform")
    
    platform_sentiment_data = df_analyzed.groupby('Platform')['Sentiment'].value_counts(normalize=True).mul(100).rename('Percentage').reset_index()
    
    sentiment_order = ['negative', 'neutral', 'positive']
    color_map_platform = {'negative': 'lightcoral', 'neutral': 'lightgray', 'positive': 'mediumseagreen'}

    fig_platform = px.bar(platform_sentiment_data,
                          x='Platform', 
                          y='Percentage', 
                          color='Sentiment',
                          category_orders={"Sentiment": sentiment_order},
                          color_discrete_map=color_map_platform,
                          title="Perbandingan Sentimen WLB antar Platform",
                          text_auto='.1f', 
                          height=500)
    
    fig_platform.update_layout(yaxis_title="Persentase Komentar (%)", xaxis_title="Platform")
    st.plotly_chart(fig_platform, use_container_width=True)
else:
    st.info("Visualisasi Sentimen per Platform dilewati karena kolom 'Platform' tidak ditemukan di data.")

st.markdown("---")

# Tampilkan Data Mentah
if st.checkbox('Tampilkan Data Hasil Analisis (DataFrame)'):
    st.dataframe(df_analyzed)

st.success("Dashboard WLB siap untuk dianalisis!")