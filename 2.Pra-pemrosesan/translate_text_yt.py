from deep_translator import GoogleTranslator
import time
import pandas as pd
import os 
import numpy as np # Diperlukan untuk membagi data frame menjadi batch

# --- 1. Definisi File Input dan Output ---
FILE_NAME = "youtube_crawl_clean.csv" 
COLUMN_KOMENTAR = "clean_text" 
BATCH_SIZE = 100 # Ukuran batch per permintaan API. Bisa diubah.
SLEEP_TIME_AFTER_BATCH = 1 # Jeda 1 detik setelah menerjemahkan 100 item

try:
    df = pd.read_csv(FILE_NAME)
    print(f"✅ File {FILE_NAME} berhasil dimuat. Total baris: {len(df)}")
except FileNotFoundError as e:
    print(f"❌ ERROR: File '{FILE_NAME}' TIDAK DITEMUKAN di folder ini. Cek ejaan file.")
    exit()

# --- 2. Fungsi dan Eksekusi Translasi Cepat ---

# Inisialisasi translator
# Catatan: GoogleTranslator secara default hanya dapat memproses hingga ~5000 karakter per permintaan.
translator = GoogleTranslator(source='en', target='id')

def batch_translate_optimized(df, column_to_translate, batch_size, sleep_time):
    texts = df[column_to_translate].astype(str).tolist()
    results = []
    total = len(texts)
    
    # Filter teks kosong/non-string dan isi dengan placeholder agar indeks tetap
    clean_texts = [text if isinstance(text, str) and text.strip() != "" else "" for text in texts]
    
    # Menghitung jumlah batch
    num_batches = int(np.ceil(total / batch_size))
    
    for k in range(num_batches):
        i = k * batch_size
        batch = clean_texts[i:i + batch_size]
        
        # Hapus placeholder (teks kosong) dari batch terjemahan
        texts_to_translate = [t for t in batch if t]
        
        print(f"🔄 Menerjemahkan batch {i}-{i + len(batch)} ({len(texts_to_translate)} item yang valid)...")
        
        # Simpan indeks teks kosong (placeholder) untuk digabungkan kembali nanti
        empty_indices = [idx for idx, text in enumerate(batch) if not text]
        
        batch_translated_results = []
        
        if texts_to_translate:
            try:
                # KUNCI: Menerjemahkan seluruh list (batch) dalam satu permintaan API
                translated_list = translator.translate_batch(texts_to_translate)
                
                # Gabungkan hasil terjemahan dengan placeholder kembali
                j = 0
                for idx in range(len(batch)):
                    if idx in empty_indices:
                        batch_translated_results.append("")
                    else:
                        # Ambil hasil terjemahan dari list
                        batch_translated_results.append(translated_list[j])
                        j += 1
                        
            except Exception as e:
                print(f"⚠️ Peringatan: Batch gagal diterjemahkan ({i}-{i + len(batch)}). Menggunakan string kosong.")
                print(f"Detail error: {e}")
                batch_translated_results = [""] * len(batch)
            
            # Jeda antar permintaan batch
            time.sleep(sleep_time) 
        else:
            # Jika semua item di batch kosong
            batch_translated_results = [""] * len(batch)
            
        results.extend(batch_translated_results)

    return results

# Jalankan terjemahan pada kolom yang bersih
# HANYA JALANKAN INI SATU KALI SAJA. WAKTU AKAN JAUH LEBIH CEPAT!
df["translated_fast"] = batch_translate_optimized(df, COLUMN_KOMENTAR, BATCH_SIZE, SLEEP_TIME_AFTER_BATCH)

# Simpan hasilnya
df.to_csv("hasil_terjemahan_cepat.csv", index=False)
print("✅ Translasi selesai dan disimpan ke 'hasil_terjemahan_cepat.csv'")