import os
import pandas as pd
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re
import emoji
# Import time untuk debugging/simulasi, tapi tidak diperlukan untuk cleaning ini
# import time 

# DEFINISI DATASET DAN PEMUATAN (WAJIB DITAMBAHKAN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_INPUT = os.path.join(BASE_DIR, '..', 'Crawl_Data', 'youtube_comments.csv') 
COLUMN_KOMENTAR = 'text'

try:
    # Memuat file CSV dan menamakannya 'df'
    df = pd.read_csv(FILE_INPUT) 
    # Pastikan kolom komentar diubah ke string
    df[COLUMN_KOMENTAR] = df[COLUMN_KOMENTAR].astype(str).fillna('')
    print(f"✅ Data '{FILE_INPUT}' berhasil dimuat. Total baris: {len(df)}")
except FileNotFoundError:
    print(f"❌ ERROR: File '{FILE_INPUT}' tidak ditemukan. Mohon periksa nama dan jalur file.")
    exit()

# FUNGSI PEMBERSINAN (PRE-PROCESSING)
# Stopword remover
factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()

def clean_text(text):
    # Tidak perlu mengimpor 're' di dalam fungsi
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # hapus tag HTML <...> (Tambahan: penting untuk scraping web/YT)
    text = re.sub(r'<.*?>', '', text) 
    
    # text lower
    text = text.lower()
    
    # hapus URL
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # hapus angka
    text = re.sub(r'\d+', '', text)
    
    # hapus emoji
    text = emoji.replace_emoji(text, replace='')
    
    # hapus karakter non-alphanumeric selain spasi
    text = re.sub(r'[^\w\s]', '', text)
    
    # hapus karakter non-ASCII (seperti yang ada di kode Anda)
    text = text.encode('ascii', 'ignore').decode('ascii') 
    
    # hapus extra spasi
    text = re.sub(r'\s+', ' ', text).strip()
    
    # hapus stopwords
    text = stopword_remover.remove(text)
    
    return text.strip()

# APLIKASI DAN PENYIMPANAN

# Terapkan fungsi clean_text ke kolom komentar yang benar
df["clean_text"] = df[COLUMN_KOMENTAR].apply(clean_text)

# Hapus baris di mana 'clean_text' menjadi string kosong ("")
total_data_awal = len(df)
df_clean = df[df['clean_text'].astype(bool)].copy() 
total_data_bersih = len(df_clean)

# Simpan hasil
df_clean.to_csv("youtube_comments_clean.csv", index=False)
print(f"\n✅ Cleaning selesai!")
print(f"Total data awal: {total_data_awal}")
print(f"Total data bersih (siap analisis): {total_data_bersih}")