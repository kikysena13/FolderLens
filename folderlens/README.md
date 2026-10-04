# FolderLens

FolderLens adalah CLI sederhana untuk melihat struktur folder project dan mendapatkan ringkasan singkat berdasarkan nama file, ekstensi, nama folder, serta pola struktur yang umum. FolderLens **tidak membuka isi file**.

## Fitur

- Menampilkan tree folder dan file secara recursive.
- Memungkinkan pengguna memilih subfolder tertentu melalui menu interaktif atau opsi CLI.
- Menghitung jumlah folder dan file yang dipindai.
- Mengatur folder tambahan yang dilewati dan membatasi kedalaman scan.
- Mengekspor laporan ke JSON atau Markdown, baik ke terminal maupun file.
- Mengenali beberapa bahasa, teknologi, konfigurasi, dokumentasi, dan folder umum.
- Melewati direktori besar/umum seperti `.git`, `node_modules`, `venv`, `build`, dan `dist`.
- Melewati symlink agar tidak mengikuti loop atau memindai target di luar folder.
- Menangani folder yang tidak dapat dibaca dengan aman.
- Menampilkan menu interaktif jika dijalankan tanpa argumen.
- Menggunakan [Rich](https://github.com/Textualize/rich) untuk menu dan output terminal.

## Requirements

- Python 3.10 atau lebih baru
- Windows, Linux, atau macOS
- Rich (dipasang otomatis melalui `pyproject.toml` atau `requirements.txt`)

## Installation

FolderLens membutuhkan Python 3.10+ dan library Rich. Buka terminal pada folder project ini, lalu pasang project dalam mode editable (Rich akan ikut dipasang sebagai dependency):

```text
python -m pip install -e .
```

Alternatifnya, jalankan file langsung dengan `python folderlens.py`.

## Usage

```text
python folderlens.py
python folderlens.py .
python folderlens.py "B:\\ProjectSaya"
python folderlens.py . --include src tests
python folderlens.py . --exclude generated cache --max-depth 3
python folderlens.py . --format json --output report.json
python folderlens.py . --format markdown --output report.md
python folderlens.py --help
python folderlens.py --version
python folderlens.py -v
```

Tanpa argumen, program membuka menu Rich. Pilih `1` untuk menganalisis folder (path kosong berarti folder saat ini), lalu pilih nomor subfolder yang ingin dianalisis. Kosongkan pilihan untuk memindai semuanya. Pilih `2` untuk bantuan, `3` untuk versi, atau `0` untuk keluar.

Untuk CLI, `--include` menerima satu atau beberapa path subfolder relatif terhadap folder project. Folder yang tidak dipilih tidak dipindai atau ditampilkan:

```text
folderlens . --include src tests
folderlens "B:\\ProjectSaya" --include app\\Http resources\\views
```

Atur pemindaian dengan `--exclude` (nama folder dicocokkan tanpa membedakan huruf besar/kecil; folder bawaan seperti `.git` dan `node_modules` tetap dilewati) dan `--max-depth` (kedalaman folder maksimum; `0` hanya memindai file di root):

```text
folderlens . --exclude generated cache
folderlens . --max-depth 2
folderlens . --include src tests --exclude snapshots --max-depth 4
```

`--format` mendukung `text` (default), `json`, dan `markdown`. Gunakan `--output` untuk menyimpan laporan ke file; folder tujuan harus sudah ada. Format JSON cocok untuk pipeline/script, sedangkan Markdown siap dimasukkan ke dokumentasi:

```text
folderlens . --format json --output report.json
folderlens . --format markdown --output docs/structure.md
folderlens . --format json
```

Setelah instalasi editable, perintah berikut juga tersedia:

```text
folderlens
folderlens .
folderlens -v
```

Jika path tidak ditemukan, FolderLens menampilkan pesan error yang jelas dan tidak membuat atau mengubah file apa pun.

## Example output

```text
[1] PROJECT STRUCTURE

📁 my-project/
├── 📁 src/
│   ├── 📄 main.py
│   └── 📄 utils.py
├── 📁 tests/
│   └── 📄 test_main.py
├── 📄 README.md
└── 📄 requirements.txt

[2] PROJECT SUMMARY

Type: Python Project
Folders: 2
Files: 5
Detected components:
- Source code
- Test directory
- Dependency/build configuration
- Documentation

[3] DETECTED TECHNOLOGIES

- Python
- Markdown

[4] STRUCTURE EXPLANATION

Project ini terlihat seperti python project.
Folder `src` kemungkinan berisi source code utama.
Folder `tests` atau `test` digunakan untuk menyimpan pengujian.
File konfigurasi Python tersebut biasanya mencatat dependency project.
File README kemungkinan berisi dokumentasi project.
```

## Project structure

```text
folderlens/
├── folderlens.py   # CLI dan validasi input
├── analyzer.py     # Pemindaian metadata serta analisis project
├── formatter.py    # Format output terminal
├── ui.py           # Tampilan tree, summary, dan menu Rich
├── README.md       # Dokumentasi
├── pyproject.toml  # Konfigurasi instalasi, dependency, dan command folderlens
├── requirements.txt # Dependency Rich
└── .gitignore
```

## Catatan keamanan dan privasi

FolderLens hanya membaca nama file dan metadata folder; isi file tidak dibuka. Symlink tetap dilewati untuk menghindari loop atau pemindaian target di luar project. Laporan yang diekspor berisi nama dan struktur path, jadi periksa isinya sebelum membagikan laporan project privat.
