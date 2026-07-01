# Computer Graphics - Conic Curve Generator

## Deployment Website

https://conic-curves.streamlit.app/

---

## Deskripsi Proyek

Proyek ini merupakan implementasi pembangkitan kurva parametrik pada mata kuliah Grafika Komputer. Program dibuat menggunakan Python, NumPy, dan Matplotlib untuk memvisualisasikan berbagai jenis kurva konik berdasarkan persamaan parametriknya.

Kurva yang dapat dibangkitkan:

* Lingkaran (Circle)
* Elips (Ellipse)
* Parabola (Parabola)
* Hiperbola (Hyperbola)

Program juga menampilkan perbandingan antara resolusi rendah dan resolusi tinggi untuk menunjukkan pengaruh jumlah titik terhadap kualitas visualisasi kurva.

---

## Fitur Program

* Visualisasi Lingkaran
* Visualisasi Elips
* Visualisasi Parabola
* Visualisasi Hiperbola
* Input parameter kurva secara interaktif
* Input Step Besar dan Step Kecil
* Menampilkan koordinat hasil perhitungan
* Menampilkan pusat (Center) atau vertex
* Perbandingan Resolusi Rendah dan Resolusi Tinggi
* Menampilkan rumus parametrik pada grafik
* Dark Theme Visualization

---

## Persamaan Parametrik

### 1. Lingkaran

x = xc + r cos(θ)

y = yc + r sin(θ)

Keterangan:

* (xc, yc) = pusat lingkaran
* r = radius

---

### 2. Elips

x = xc + a cos(θ)

y = yc + b sin(θ)

Keterangan:

* (xc, yc) = pusat elips
* a = semi mayor
* b = semi minor

---

### 3. Parabola

x = xp + at²

y = yp + 2at

Keterangan:

* (xp, yp) = vertex parabola
* a = parameter parabola

---

### 4. Hiperbola

x = xc + a sec(θ)

y = yc + b tan(θ)

Keterangan:

* (xc, yc) = pusat hiperbola
* a = semi-sumbu transversal
* b = semi-sumbu konjugasi

---

## Teknologi yang Digunakan

* Python 3.12+
* NumPy
* Matplotlib
* Jupyter Notebook / VS Code

---

# Cara Menjalankan Program

## 1. Clone Repository

```bash
git clone https://github.com/NaufalArkaan/Computer-Graphics-Conic-Curves.git
```

Masuk ke folder project:

```bash
cd Computer-Graphics-Conic-Curves
```

---

## 2. Membuat Virtual Environment

```bash
python -m venv venv
```

---

## 3. Mengaktifkan Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```

Jika berhasil, terminal akan menampilkan:

```bash
(venv)
```

---

## 4. Install Dependency

```bash
pip install -r requirements.txt
```

---

## 5. Membuka Project

```bash
code .
```

---

## 6. Memilih Kernel Notebook

Pada VS Code:

1. Buka file notebook (.ipynb)
2. Klik "Select Kernel"
3. Pilih Python Environment
4. Pilih environment venv

Contoh:

```text
.\venv\Scripts\python.exe
```

---

## 7. Menjalankan Program

Jalankan seluruh cell notebook atau jalankan cell satu per satu sesuai kebutuhan.

---

# Struktur Project

```
├── ⚙️ .gitignore
├── 📄 Note-Elips.txt
├── 📄 Note-Hiperbola.txt
├── 📄 Note-Lingkaran.txt
├── 📝 README.md
├── 🐍 app.py
├── 📄 kurva_parametrik.ipynb
├── 📄 kurva_parametrik_V2.ipynb
├── 📄 kurva_parametrik_V3.ipynb
├── 📄 kurva_parametrik_V4.ipynb
└── 📄 requirements.txt
```

---

# Dependency

Isi file requirements.txt:

```txt
numpy==2.4.6
matplotlib==3.10.9
ipykernel==7.2.0
```

---

# Kolaborasi Tim

Sebelum mulai bekerja:

```bash
git pull
```

Setelah melakukan perubahan:

```bash
git add .
git commit -m "Deskripsi perubahan"
git push
```

---

# Catatan

Folder virtual environment (venv) tidak diunggah ke GitHub karena setiap anggota tim akan membuat virtual environment masing-masing.

Pastikan file `.gitignore` berisi:

```gitignore
venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
```

---

# Tujuan Pembelajaran

Melalui proyek ini mahasiswa dapat:

* Memahami konsep kurva parametrik
* Memahami representasi geometris kurva konik
* Memahami pengaruh resolusi terhadap visualisasi kurva
* Mengimplementasikan persamaan matematika ke dalam program komputer
* Menggunakan Python sebagai alat visualisasi grafika komputer

---

## Anggota Kelompok

* Syahrial Nur Faturrahman (202410370110009)
* Restu Gilang Saputra (202410370110014)
* Naufal Arkaan (202410370110020)

---

Mata Kuliah Grafika Komputer

Universitas Muhammadiyah Malang
