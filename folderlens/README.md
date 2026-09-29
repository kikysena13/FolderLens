# FolderLens

FolderLens adalah CLI sederhana untuk melihat struktur folder project dan mendapatkan ringkasan singkat berdasarkan nama file, ekstensi, nama folder, serta pola struktur yang umum. FolderLens **tidak membuka isi file**.

## Fitur

- Menampilkan tree folder dan file secara recursive.
- Menghitung jumlah folder dan file yang dipindai.
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
python folderlens.py --help
python folderlens.py --version
python folderlens.py -v
```

Tanpa argumen, program membuka menu Rich. Pilih `1` untuk menganalisis folder (path kosong berarti folder saat ini), `2` untuk bantuan, `3` untuk versi, atau `0` untuk keluar. Setelah instalasi editable, perintah berikut juga tersedia:

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

## Future Improvements

- AI-generated explanation
- Export result to JSON
- Export result to Markdown
- File statistics
- Detect framework
- Detect programming language
- Git repository analysis
- Dependency detection
- Interactive terminal UI dengan Rich
