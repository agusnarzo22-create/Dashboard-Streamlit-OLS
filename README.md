# Dashboard Streamlit — Regresi OLS Belanja Modal vs IPM

Dashboard interaktif untuk menganalisis pengaruh **Belanja Modal Pendidikan (X1)** dan
**Belanja Modal Kesehatan (X2)** terhadap **Indeks Pembangunan Manusia / IPM (Y)**
menggunakan regresi linier berganda (*Ordinary Least Squares*).

## Fitur

- **Pemilih kota** di sidebar — pilih dari 97 kota, seluruh analisis dihitung ulang secara otomatis.
- **4 kartu KPI**: jumlah observasi, R², F-statistic, jumlah variabel signifikan.
- **Persamaan regresi** yang dirender dengan LaTeX.
- **Tabel koefisien** lengkap: koefisien, std. error, t-statistik, p-value, keputusan.
- **Visualisasi interaktif** (Plotly): 2 scatter + garis regresi, bar koefisien, tren IPM,
  dan **bidang regresi 3D** yang bisa diputar/di-zoom.
- **Data mentah** dalam expander + tombol unduh CSV.
- **Kesimpulan dinamis** yang menyesuaikan hasil estimasi tiap kota.

## Menjalankan secara lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Aplikasi akan terbuka otomatis di `http://localhost:8501`.

## Struktur berkas

```
Dashboard-Streamlit-OLS-Kota-Jambi/
├── app.py                                          # aplikasi Streamlit
├── requirements.txt                                # dependensi
├── README.md
├── .gitignore
└── data/
    └── dataset_fiskal_97_hipoFull.csv              # salinan dataset (fallback offline)
```

## Sumber data

Aplikasi mencoba memuat dataset dari URL GitHub terlebih dahulu; bila gagal (mis. offline),
otomatis memakai salinan lokal di `data/`. Dataset: panel fiskal 97 kota Indonesia (2014–2024),
**1.067 observasi**.

## Catatan interpretasi

Koefisien negatif pada belanja modal kesehatan umumnya **bukan** berarti belanja tersebut
merugikan IPM, melainkan mencerminkan pola *alokasi berbasis kebutuhan* (kota dengan IPM rendah
menganggarkan belanja modal kesehatan lebih besar) dan sifat belanja modal sebagai investasi
jangka panjang yang dampaknya baru terasa beberapa tahun kemudian.

---

Dibangun dengan Python · Pandas · Statsmodels · Plotly · Streamlit.
