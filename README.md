# Analisis Sentimen tentang Slogan Work-Life Balance

Nama: Aminah Nur'aini Muchayati  
NRP: 5024231034

## Pendahuluan

Proyek ini berfokus pada pengumpulan dan analisis sentimen komentar publik terkait topik Work-Life Balance (WLB) dari platform Reddit dan YouTube. Tujuannya adalah untuk memahami persepsi masyarakat terhadap konsep WLB, yang sering menjadi topik diskusi di media sosial. Dengan menggunakan teknik web crawling dan analisis sentimen berbasis Natural Language Processing (NLP), proyek ini mengidentifikasi apakah komentar cenderung positif, negatif, atau netral.

## Fitur Proyek

- Crawling data komentar dari Reddit dan YouTube berdasarkan kata kunci terkait WLB.
- Pra-pemrosesan data: pembersihan teks, penghapusan stopword, dan normalisasi.
- Terjemahan komentar (jika diperlukan) menggunakan Google Translate API.
- Analisis sentimen menggunakan model NLP (TextBlob, Transformers, dsb).
- Visualisasi hasil analisis (wordcloud, grafik, dsb).
- Integrasi hasil ke Metabase untuk analisis lanjutan.

## Struktur Folder

```
1.Crawl_Data/
    - crawl_from_r.py      # Crawling Reddit
    - crawl_from_yt.py     # Crawling YouTube
2.Pra-pemrosesan/
    - clean_text_r.py      # Cleaning Reddit data
    - clean_text_yt.py     # Cleaning YouTube data
    - translate_text_r.py  # Translate Reddit data
    - translate_text_yt.py # Translate YouTube data
3.Penggabungan/
    - gabung.py            # Gabungkan data
analisis.py                # Analisis sentimen & visualisasi
sentiment_analysis.py      # Analisis sentimen (Transformers)
main.py                    # Pipeline utama (opsional)
```

## Library yang Digunakan

- `pandas` – manipulasi data
- `praw` – crawling Reddit
- `google-api-python-client` – crawling YouTube
- `deep_translator` – terjemahan otomatis
- `textblob`, `transformers` – analisis sentimen
- `wordcloud`, `matplotlib` – visualisasi
- `nltk`, `Sastrawi`, `emoji`, `re`, `numpy`, `os`, `time` – pra-pemrosesan dan utilitas

## Cara Menjalankan

1. **Crawling Data**
   - Jalankan `crawl_from_r.py` untuk mengambil data dari Reddit.
   - Jalankan `crawl_from_yt.py` untuk mengambil komentar dari YouTube.

2. **Pra-pemrosesan**
   - Jalankan script di folder `2.Pra-pemrosesan` untuk membersihkan dan menerjemahkan data.

3. **Penggabungan Data**
   - Gabungkan data Reddit & YouTube dengan `gabung.py`.

4. **Analisis Sentimen**
   - Jalankan `analisis.py` atau `sentiment_analysis.py` untuk mendapatkan label sentimen.

5. **Visualisasi & Integrasi Metabase**
   - Hasil akhir (CSV) dapat diimpor ke Metabase untuk analisis dan visualisasi lebih lanjut.

## Integrasi dengan Metabase

- Import file CSV hasil analisis ke Metabase.
- Buat dashboard dan visualisasi sesuai kebutuhan (misal: distribusi sentimen, wordcloud, dsb).

## Catatan

- Pastikan API key Reddit dan YouTube sudah diatur di script crawling.
- Install semua dependensi dengan `pip install -r requirements.txt` (buat file requirements jika belum ada).
- Beberapa library membutuhkan resource tambahan (misal: `nltk.download('stopwords')`).

---

Silakan modifikasi sesuai kebutuhan spesifik proyek Anda!
