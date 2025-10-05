from deep_translator import GoogleTranslator
import time
import pandas as pd
# Import os TIDAK diperlukan karena file berada dalam folder yang sama


# 1. DEFINISI FILE INPUT


# Pastikan nama file ini sudah BENAR dan file ada di folder yang sama
FILE_NAME = "youtube_comments_clean.csv" 
COLUMN_KOMENTAR = "clean_text" # Kolom yang akan diterjemahkan

try:
    # Memuat file CSV menggunakan nama file langsung
    df = pd.read_csv(FILE_NAME)
    print(f"✅ File {FILE_NAME} berhasil dimuat. Total baris: {len(df)}")
except FileNotFoundError as e:
    # Jika masih gagal, cek ejaan file di folder
    print(f"❌ ERROR: File '{FILE_NAME}' TIDAK DITEMUKAN di folder ini. Cek ejaan file.")
    exit()


# 2. FUNGSI DAN EKSEKUSI TRANSLASI


translator = GoogleTranslator(source='id', target='en')

def batch_translate_safe(texts, batch_size=100):
    results = []
    total = len(texts)
    
    for i in range(0, total, batch_size):
        batch = texts[i:i + batch_size]
        print(f"🔄 Menerjemahkan batch {i}-{i + len(batch)} ...")
        
        try:
            batch_translated = []
            for text in batch:
                # Menghindari error pada baris kosong
                if not isinstance(text, str) or text.strip() == "":
                    batch_translated.append("")
                    continue
                
                translated = translator.translate(text)
                batch_translated.append(translated)
                time.sleep(0.3)  # jeda antar permintaan
            
            results.extend(batch_translated)
        except Exception as e:
            print(f"⚠️ Batch gagal diterjemahkan ({i}-{i + len(batch)}): {e}")
            results.extend([""] * len(batch))
            time.sleep(5) # Jeda lebih lama setelah error

    return results

# Jalankan terjemahan pada kolom yang bersih
df["translated"] = batch_translate_safe(df[COLUMN_KOMENTAR].tolist())

# Simpan hasilnya
df.to_csv("hasil_terjemahan.csv", index=False)
print("✅ Translasi selesai dan disimpan ke 'hasil_terjemahan.csv'")