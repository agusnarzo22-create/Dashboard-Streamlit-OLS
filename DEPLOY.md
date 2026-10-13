# Cara Deploy — Online agar Dosen Bisa Melihat

Dashboard ini adalah aplikasi **Streamlit**. Cara paling praktis & gratis untuk
mengonlinekannya adalah **Streamlit Community Cloud** (dari pembuat Streamlit sendiri).

Hasil akhir: link publik seperti `https://dashboard-ols-kota-jambi.streamlit.app`
yang bisa dibuka dosen dari HP/laptop mana pun, tanpa install apa pun.

---

## Langkah 1 — Buat repository di GitHub

1. Buka https://github.com/new
2. **Repository name:** `Dashboard-Streamlit-OLS-Kota-Jambi`
3. Pilih **Public** (wajib — Streamlit Cloud butuh repo publik di paket gratis)
4. **Jangan** centang "Add a README file" (nanti bentrok)
5. Klik **Create repository**

## Langkah 2 — Push kode dari komputermu

Buka PowerShell di folder ini, lalu jalankan:

```powershell
cd C:\Users\Advan\OneDrive\Dokumen\AltProject\DataScience\Dashboard-Streamlit-OLS-Kota-Jambi
git push -u origin main
```

Saat diminta login, pilih **Sign in with your browser** (Git Credential Manager akan
membuka browser). Setelah berhasil, refresh halaman GitHub — `app.py`,
`requirements.txt`, dan folder `data/` akan terlihat di sana.

> Folder `.venv/` **tidak** ikut ter-upload (sudah dikecualikan lewat `.gitignore`). Ini benar.

## Langkah 3 — Deploy di Streamlit Community Cloud

1. Buka https://share.streamlit.io
2. Klik **Continue with GitHub** → izinkan akses (authorize)
3. Klik **Create app** (atau **New app**)
4. Isi form:
   - **Repository:** `agusnarzo22-create/Dashboard-Streamlit-OLS-Kota-Jambi`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** pilih nama, mis. `dashboard-ols-kota-jambi`
5. Klik **Deploy!**

Proses build pertama memakan 2–5 menit (meng-install pandas, statsmodels, plotly,
streamlit di server mereka). Setelah selesai, aplikasi langsung online.

## Langkah 4 — Bagikan ke dosen

Copy link-nya, contoh:

```
https://dashboard-ols-kota-jambi.streamlit.app
```

Link ini bisa dibuka siapa saja. Kalau dosen membuka dan muncul tulisan
_"This app has gone to sleep"_ → tinggal klik **Yes, get this app back up!**
(mode gratis akan "tidur" bila tidak ada yang mengakses beberapa hari).

---

## Kalau ada perubahan kode

Setiap kali kamu `git push` ke branch `main`, Streamlit Cloud **otomatis**
membangun ulang aplikasinya. Tidak perlu deploy ulang secara manual.

```powershell
git add .
git commit -m "update dashboard"
git push
```

---

## Ringkasan berkas yang dibutuhkan

| Berkas | Fungsi |
|---|---|
| `app.py` | Aplikasi Streamlit (main file) |
| `requirements.txt` | Daftar dependensi — dibaca otomatis oleh Streamlit Cloud |
| `data/dataset_fiskal_97_hipoFull.csv` | Dataset (cadangan offline; app mengambil dari URL dulu) |
| `.gitignore` | Mencegah `.venv/` ikut ter-upload |

## Catatan

- Aplikasi ini **tidak butuh database** — semua data dibaca dari CSV, jadi cocok
  dengan paket gratis Streamlit Cloud.
- `requirements.txt` sengaja tidak di-pin ke versi spesifik agar build di server
  selalu berhasil.
