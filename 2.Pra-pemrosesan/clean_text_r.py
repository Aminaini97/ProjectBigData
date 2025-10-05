import os
import pandas as pd
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re
import emoji

# 1️PENYIAPAN DATASET 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_INPUT = os.path.join(BASE_DIR, '..', '1.Crawl_Data', 'reddit_crawl.csv') 
COLUMN_KOMENTAR = 'selftext'               # Ganti dengan nama kolom yang berisi teks komentar di CSV

try:
    df = pd.read_csv(FILE_INPUT)
    # Pastikan kolom komentar diubah ke string dan mengisi NaN dengan string kosong
    df[COLUMN_KOMENTAR] = df[COLUMN_KOMENTAR].astype(str).fillna('')
    print(f"✅ Data '{FILE_INPUT}' berhasil dimuat. Total baris: {len(df)}")
except FileNotFoundError:
    print(f"❌ ERROR: File '{FILE_INPUT}' tidak ditemukan. Pastikan file ada di direktori yang sama.")
    exit()

# FUNGSI PEMBERSINAN (PRE-PROCESSING)
# Stopword remover Sastrawi
factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()

def clean_text(text):
    # 1. Cek input, jika bukan string atau kosong/spasi, kembalikan string kosong
    # Ini sudah menangani baris yang kosong atau hanya spasi.
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # 2. Lowercase
    text = text.lower()
    
    # 3. Hapus URL
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # 4. Hapus tag HTML <...>
    text = re.sub(r'<.*?>', '', text)
    
    # 5. Hapus tanggal (format umum)
    text = re.sub(r'\b\d{1,4}[-/]\d{1,2}[-/]\d{1,4}\b', '', text)
    
    # 6. Hapus angka
    text = re.sub(r'\d+', '', text)
    
    # 7. Hapus emoji
    text = emoji.replace_emoji(text, replace='')
    
    # 8. Hapus karakter non-alphanumeric selain spasi
    text = re.sub(r'[^\w\s]', '', text)
    
    # 9. Hapus extra spasi dan trim ujung
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 10. Hapus stopwords
    text = stopword_remover.remove(text)
    
    return text.strip()

# APLIKASI DAN FILTERING BARIS KOSONG
# Terapkan fungsi ke kolom komentar
df["clean_text"] = df[COLUMN_KOMENTAR].apply(clean_text)

# Hitung data sebelum filtering
total_data_awal = len(df)

# **LANGKAH PENTING: Hapus baris di mana 'clean_text' menjadi string kosong ("")**
# Baris kosong terjadi jika komentar asli hanya berisi stopwords, link, atau angka yang semuanya terhapus.
df_clean = df[df['clean_text'].astype(bool)].copy() 

# Hitung data setelah filtering
total_data_bersih = len(df_clean)

#Simpan hasil
FILE_OUTPUT = "reddit_crawl_clean.csv"
df_clean.to_csv(FILE_OUTPUT, index=False)

print(f"\n✅ Cleaning selesai! Data bersih disimpan di '{FILE_OUTPUT}'")
print(f"Total data awal: {total_data_awal}")
print(f"Total baris yang dihapus (karena kosong/tidak relevan): {total_data_awal - total_data_bersih}")
print(f"Total data siap analisis: {total_data_bersih}")