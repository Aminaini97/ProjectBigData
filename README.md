
# Analisis Sentimen tentang Slogan Work-Life Balance

Nama: Aminah Nur'aini Muchayati  

NRP: 5024231034

## Pendahuluan

Proyek ini berfokus pada pengumpulan dan analisis sentimen komentar publik terkait topik Work-Life Balance (WLB) dari platform Reddit dan YouTube. Tujuannya adalah untuk memahami persepsi masyarakat terhadap konsep WLB, yang sering menjadi topik diskusi di media sosial. Dengan menggunakan teknik web crawling dan analisis sentimen berbasis Natural Language Processing (NLP), proyek ini mengidentifikasi apakah komentar cenderung positif, negatif, atau netral. Inspirasi proyek ini berasal dari tren dan diskusi WLB yang banyak muncul di TikTok, meskipun data yang dikumpulkan berasal dari Reddit dan YouTube. Alasan tidak melakukan crawling langsung di TikTok adalah karena keterbatasan akses API dan regulasi privasi yang ketat, sehingga Reddit dan YouTube dipilih sebagai sumber data yang lebih mudah diakses dan diolah. Dengan menganalisis data dari kedua platform ini, proyek ini berupaya memberikan gambaran tentang opini publik terhadap slogan yang sering digaungkan di dunia kerja modern.

## Fitur Proyek

- Crawling data komentar dari Reddit dan YouTube berdasarkan kata kunci terkait WLB.
- Pra-pemrosesan data: pembersihan teks, penghapusan stopword, dan normalisasi.
- Terjemahan komentar (jika diperlukan) menggunakan Google Translate API.
- Analisis sentimen menggunakan model TextBlob,Transformers, dsb.
- Visualisasi hasil analisis (wordcloud, grafik, dsb).
- Integrasi hasil ke Tableau Desktop untuk analisis lanjutan.

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
   - Jalankan `analisis.py` untuk mendapatkan label sentimen.

5. **Visualisasi & Integrasi Tableau Desktop**
   - Hasil akhir (CSV) dapat diimpor ke Tableau Desktop untuk analisis dan visualisasi lebih lanjut.

## Integrasi dengan Tableau Desktop

- Import file CSV hasil analisis ke Tableau Desktop.
- Buat dashboard dan visualisasi sesuai kebutuhan (misal: distribusi sentimen, wordcloud, dsb).

## Catatan

- Pastikan API key Reddit dan YouTube sudah diatur di script crawling.
- Install semua dependensi dengan `pip install -r requirements.txt` (buat file requirements jika belum ada).
- Beberapa library membutuhkan resource tambahan (misal: `nltk.download('stopwords')`).

---

## Hasil Analisis Sentimen

Distribusi Sentimen (%) per Platform:

| Sentiment | Negative | Neutral | Positive |
|-----------|----------|---------|----------|
| Reddit    |  11.11   | 50.00   |  38.89   |
| YouTube   |  11.16   | 53.67   |  35.16   |

- Sebagian besar komentar di kedua platform menunjukkan sentimen **netral**.
- Sentimen positif juga cukup signifikan, sedangkan sentimen negatif relatif kecil.
- Topik yang sering muncul meliputi stres kerja, burnout, dan tantangan menjaga keseimbangan antara pekerjaan dan kehidupan pribadi.
- Visualisasi wordcloud memperlihatkan kata-kata kunci seperti "kerja", "waktu", "keluarga", dan "lelah" sering muncul dalam diskusi.

## Evaluasi Hasil & Saran Perbaikan

### Apakah Hasil Sudah Optimal?

Distribusi sentimen yang didominasi oleh kategori netral adalah hal yang umum dalam analisis komentar publik, terutama jika data berasal dari diskusi informatif, tanya jawab, atau berbagi pengalaman tanpa ekspresi emosi yang kuat. Namun, proporsi sentimen positif yang cukup besar juga menunjukkan adanya pengalaman baik yang dibagikan, sementara sentimen negatif yang kecil bisa berarti:

- Topik Work-Life Balance memang lebih sering didiskusikan secara netral atau positif.
- Model analisis sentimen yang digunakan cenderung "conservative" dalam mendeteksi emosi negatif.
- Data yang diambil belum sepenuhnya mewakili seluruh spektrum opini (misal: sampling bias, kata kunci kurang variatif).

## Kesimpulan

Analisis sentimen terhadap komentar publik mengenai Work-Life Balance di Reddit dan YouTube menunjukkan bahwa mayoritas diskusi bersifat netral, dengan proporsi sentimen positif yang juga cukup besar dan sentimen negatif yang relatif kecil. Hal ini mengindikasikan bahwa masyarakat cenderung membahas isu ini secara informatif dan berbagi pengalaman tanpa banyak ekspresi emosi ekstrem. Namun, masih terdapat tantangan dan keluhan terkait stres kerja dan burnout yang perlu diperhatikan. Untuk mendapatkan gambaran yang lebih komprehensif dan akurat, disarankan melakukan perluasan data, tuning model, serta validasi manual pada hasil analisis. Temuan ini dapat menjadi dasar bagi perusahaan, pembuat kebijakan, maupun individu untuk meningkatkan perhatian terhadap pentingnya keseimbangan antara pekerjaan dan kehidupan pribadi.

---

### Saran Perbaikan

1. **Perluasan Kata Kunci & Sumber Data:**
   - Tambahkan kata kunci lain yang relevan atau gunakan platform tambahan jika memungkinkan.
2. **Tuning Model Sentimen:**
   - Coba beberapa model analisis sentimen (misal: fine-tuning model transformer, menggunakan model khusus bahasa Indonesia).
3. **Pra-pemrosesan Lebih Lanjut:**
   - Pastikan data sudah dibersihkan dengan baik, termasuk deteksi sarcasm, slang, atau konteks lokal.
4. **Analisis Manual Sampling:**
   - Lakukan validasi manual pada sebagian data untuk memastikan label sentimen sudah sesuai.
5. **Visualisasi & Eksplorasi Lanjutan:**
   - Buat visualisasi tambahan (misal: distribusi sentimen per topik, per waktu, dsb) untuk menemukan insight lebih dalam.

Dengan langkah-langkah di atas, hasil analisis sentimen dapat menjadi lebih representatif dan akurat untuk pengambilan keputusan atau penelitian lanjutan.
