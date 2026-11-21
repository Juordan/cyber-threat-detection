# 🛡️ Cyber Threat Detection

### Aplikasi Deteksi Phishing pada SMS, Email, dan URL Menggunakan Machine Learning

## 📌 Tentang Proyek

**Cyber Threat Detection** merupakan aplikasi berbasis web yang dikembangkan untuk mengidentifikasi potensi ancaman phishing pada pesan SMS, email, dan URL menggunakan pendekatan Machine Learning.

Phishing merupakan salah satu bentuk ancaman keamanan siber yang memanfaatkan pesan atau tautan palsu untuk mengelabui pengguna agar memberikan informasi sensitif atau melakukan tindakan yang merugikan.

Aplikasi ini mengintegrasikan tiga model Machine Learning yang dirancang untuk menganalisis karakteristik SMS, email, dan URL secara terpisah. Hasil analisis ditampilkan melalui antarmuka interaktif yang dibangun menggunakan Streamlit.

## 🎯 Tujuan Proyek

- Mengembangkan aplikasi deteksi phishing berbasis Machine Learning.
- Mengidentifikasi potensi smishing melalui pesan SMS.
- Menganalisis karakteristik email untuk mendeteksi indikasi phishing.
- Mengidentifikasi URL yang memiliki karakteristik mencurigakan.
- Mengintegrasikan model Machine Learning ke dalam aplikasi web interaktif.

## 🚀 Fitur Utama

### 1. SMS Phishing Detection

Fitur untuk mengidentifikasi pesan SMS yang berpotensi mengandung smishing (phishing melalui SMS).

Kemampuan:
- Menganalisis isi pesan SMS.
- Mengekstraksi karakteristik teks dan fitur numerik.
- Menggunakan model Multinomial Naive Bayes.
- Mengklasifikasikan pesan menjadi:
  - Ham
  - Smishing

### 2. Email Phishing Detection

Fitur untuk mengidentifikasi email yang berpotensi mengandung phishing.

Kemampuan:
- Membersihkan teks email melalui preprocessing.
- Menangani konten HTML dan karakter khusus.
- Mengekstraksi fitur teks menggunakan TF-IDF.
- Menggunakan model Linear Support Vector Classifier (Linear SVC).
- Mengklasifikasikan email menjadi:
  - Safe Email
  - Phishing Email

### 3. URL Phishing Detection

Fitur untuk mengidentifikasi URL berdasarkan karakteristik yang berpotensi mengindikasikan phishing.

Kemampuan:
- Mengekstraksi 27 fitur URL.
- Menganalisis panjang URL dan domain.
- Mengidentifikasi penggunaan karakter khusus.
- Menganalisis keberadaan HTTPS dan kata kunci tertentu.
- Menggunakan model Random Forest Classifier.
- Mengklasifikasikan URL menjadi:
  - Legitimate
  - Phishing

## 🧠 Model Machine Learning

Proyek ini menggunakan tiga algoritma Machine Learning yang disesuaikan dengan karakteristik masing-masing jenis data.

| Jenis Deteksi | Algoritma |
|---|---|
| SMS | Multinomial Naive Bayes |
| Email | Linear Support Vector Classifier |
| URL | Random Forest Classifier |

Setiap model memiliki tahapan preprocessing dan ekstraksi fitur yang berbeda sesuai dengan karakteristik data yang digunakan.

## 🛠️ Teknologi dan Library

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama |
| Streamlit | Pengembangan antarmuka aplikasi web |
| Pandas | Pengolahan dan manipulasi data |
| NumPy | Operasi numerik |
| Scikit-learn | Pengembangan dan implementasi model Machine Learning |
| Joblib | Penyimpanan dan pemuatan model |
| Git | Pengelolaan versi kode |
| Git LFS | Penyimpanan file model berukuran besar |

## 📁 Struktur Proyek

```text
Cyber-Threat-Detection/
│
├── models/
│   ├── best_sms_phishing_model.pkl
│   ├── email_model.pkl
│   └── url_model.pkl
│
├── preprocessors/
│   ├── email_text_preprocessor.py
│   ├── url_feature_extractor.py
│   └── url_feature_names.json
│
├── app.py
├── inspect_models.py
├── test_prediction.py
├── requirements.txt
├── .gitignore
├── .gitattributes
└── README.md
```

## ⚙️ Instalasi dan Konfigurasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi secara lokal.

### 1. Clone Repository

```bash
git clone https://github.com/Juordan/cyber-threat-detection.git
```

### 2. Masuk ke Direktori Proyek

```bash
cd cyber-threat-detection
```

### 3. Persiapkan Git LFS

File model Machine Learning disimpan menggunakan Git Large File Storage (Git LFS).

Pastikan Git dan Git LFS telah terinstal, kemudian jalankan:

```bash
git lfs install
git lfs pull
```

### 4. Buat Virtual Environment

Gunakan Python 3.12 untuk membuat lingkungan virtual:

```bash
python -m venv .venv
```

Aktifkan virtual environment pada Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalasi Dependencies

Instal seluruh library yang dibutuhkan:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## ▶️ Menjalankan Aplikasi

Setelah seluruh dependensi berhasil diinstal, jalankan aplikasi menggunakan:

```bash
python -m streamlit run app.py
```

Streamlit akan menampilkan alamat lokal aplikasi yang dapat dibuka melalui browser.

## 🔍 Pengujian Model

Untuk memeriksa apakah seluruh model dapat dimuat dengan benar:

```bash
python inspect_models.py
```

Untuk menjalankan pengujian prediksi:

```bash
python test_prediction.py
```

## 📊 Evaluasi Model

Berdasarkan hasil evaluasi model pada data pengujian:

| Model | Accuracy |
|---|---:|
| SMS - Multinomial Naive Bayes | 99,26% |
| Email - Linear SVC | 98,93% |
| URL - Random Forest | 92,78% |

*Catatan: Nilai akurasi merupakan hasil evaluasi masing-masing model pada dataset pengujiannya. Nilai tersebut tidak menjamin ketepatan setiap prediksi pada data baru.*

## ⚠️ Disclaimer

Cyber Threat Detection dikembangkan sebagai alat bantu untuk mengidentifikasi potensi ancaman phishing.

Hasil klasifikasi dihasilkan oleh model Machine Learning berdasarkan pola dan karakteristik data yang dipelajari selama proses pelatihan.

Hasil deteksi tidak dapat dijadikan satu-satunya dasar untuk menentukan keamanan suatu pesan, email, atau URL. Pengguna tetap disarankan melakukan verifikasi tambahan sebelum membuka tautan atau memberikan informasi pribadi.

## 👥 Tim Pengembang

Proyek ini dikembangkan secara kolaboratif oleh:

1. **Felicia Chelsey Hadi**
2. **Jonathan Hartono**
3. **Jordan Sebastian**

## 🔗 Repository

[Cyber Threat Detection - GitHub](https://github.com/Juordan/cyber-threat-detection)