import pandas as pd
import os

# ===============================================
# 1. DEFINISI FILE INPUT
# ===============================================

FILE_YOUTUBE = 'hasil_terjemahan_yt.csv'
FILE_REDDIT = 'hasil_terjemahan_r.csv'
FILE_OUTPUT = 'data_komentar_gabungan_final.csv'

# Kolom yang dijamin ADA dan RELEVAN di kedua file setelah cleaning:
# Asumsi: clean_text (ID) dan translated (EN) sudah ada di kedua file.
KOLOM_INTI = ['clean_text', 'translated'] 

# ===============================================
# 2. MUAT, TANDAI, DAN SELARASKAN DATA
# ===============================================

try:
    # --- Data YouTube ---
    df_youtube = pd.read_csv(FILE_YOUTUBE)
    
    # PERBAIKAN: Pilih hanya kolom inti yang dibutuhkan dari YouTube
    # Ini memastikan kolom-kolom tambahan YouTube tidak merusak DataFrame gabungan.
    # Kita harus memastikan kolom dalam KOLOM_INTI benar-benar ada di df_youtube
    df_youtube = df_youtube[KOLOM_INTI]
    
    df_youtube['Platform'] = 'YouTube'
    print(f"Data YouTube dimuat dan diselaraskan: {len(df_youtube)} baris.")

    # --- Data Reddit ---
    df_reddit = pd.read_csv(FILE_REDDIT)
    
    # PERBAIKAN: Pilih hanya kolom inti yang dibutuhkan dari Reddit
    # df_reddit seharusnya sudah memiliki kolom ini jika proses cleaning berhasil
    df_reddit = df_reddit[KOLOM_INTI] 
    
    df_reddit['Platform'] = 'Reddit'
    print(f"Data Reddit dimuat dan diselaraskan: {len(df_reddit)} baris.")

except FileNotFoundError as e:
    print(f"ERROR: Salah satu file tidak ditemukan. Detail: {e}")
    exit()
except KeyError as e:
    # Penting: Menangkap error jika salah satu kolom di KOLOM_INTI tidak ada di CSV
    print(f"ERROR: Kolom {e} tidak ditemukan di salah satu file CSV. Periksa output cleaning.")
    exit()

# ===============================================
# 3. GABUNGKAN DATA (Concatenate)
# ===============================================

# Menggabungkan kedua DataFrame yang sekarang memiliki struktur kolom yang sama
df_gabungan = pd.concat([df_youtube, df_reddit], ignore_index=True)

print(f"\nPenggabungan berhasil. Total data gabungan: {len(df_gabungan)} baris.")

# ===============================================
# 4. SIMPAN HASIL AKHIR
# ===============================================

# Penghapusan duplikasi
df_gabungan.drop_duplicates(subset=['clean_text', 'Platform'], inplace=True)
print(f"    Total data setelah penghapusan duplikasi: {len(df_gabungan)} baris.")

# Simpan DataFrame gabungan ke file CSV baru
df_gabungan.to_csv(FILE_OUTPUT, index=False, encoding='utf-8')

print(f"File gabungan siap digunakan: '{FILE_OUTPUT}'")