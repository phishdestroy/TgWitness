# Pencarian teks lengkap

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/search/

Temukan pesan yang disimpan berdasarkan bentuk kata, frasa persis, domain, dan @nama pengguna, dengan hasil yang paling sesuai ditampilkan terlebih dahulu, serta indeks yang terikat pada jurnal yang ditandatangani.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/id/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Analisis arsip](https://phishdestroy.github.io/TgWitness/id/docs/reference/analysis/) · [OCR dan transkripsi lokal](https://phishdestroy.github.io/TgWitness/id/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Pratinjau.** Di **Jurnal**, pilih **"Kecocokan terbaik · bentuk kata"** di sebelah bidang pencarian. Hasil diurutkan menggunakan algoritma BM25 dan mencakup bentuk lain dari kata yang sama: *"перевод"* menemukan *"переводом"* dan *"переводы"*, *"transfer"* menemukan *"transfers"*, frasa dalam bahasa Mandarin ditemukan tanpa spasi. Opsi **"Terbaru terlebih dahulu · teks persis"** mempertahankan pencarian substring sebelumnya di seluruh catatan.

Indeks merupakan data turunan. Indeks ini dibangun ulang dari jurnal yang ditandatangani, tidak pernah ditandatangani sendiri, dan tidak pernah dimasukkan ke dalam ekspor. Catatan asli tidak berubah.

**On this page**

- [Search syntax](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#search-syntax)
- [Languages](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#languages)
- [Where the index lives](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#where-the-index-lives)
- [Results and the signed journal](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#results-and-the-signed-journal)
- [Recognized text](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#recognized-text)
- [Access](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#access)
- [Ask the archive and MCP](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#ask-the-archive-and-mcp)
- [Dependencies](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#dependencies)
- [Benchmark](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#benchmark)

## Sintaks pencarian

| Tulis | Menemukan |
| --- | --- |
| `перевод карта` | Catatan yang mengandung kedua kata tersebut, dalam bentuk apa pun |
| `"переводом на карту"` | Frasa persis ini, dalam urutan ini |
| `бонус OR подарок` | Salah satu kata |
| `перевод -казино` | Catatan tanpa kata yang dikecualikan |
| `example.com` | Domain dan subdomainnya, termasuk dalam tautan tersembunyi dan URL tombol |
| `@username`, `t.me/username` | Penyebutan dan tautan akun tersebut, serta pesan yang dikirimkannya |
| `#tag` | Tagar |
| `+79991234567`, alamat dompet, alamat email | Nilai yang sama dalam bentuk teks atau tautan |
| `from:@username`, `from:123456` | Pesan dari pengirim tersebut |
| `chat:-1001234567890` | Satu obrolan; hal ini hanya dapat membatasi akses Anda sendiri |
| `id:42` | Versi pesan 42 yang disimpan |
| `since:2026-01-01 until:2026-01-31` | Periode pengamatan; tanggal tanpa waktu mencakup sepanjang hari |
| `kind:edited` | Hanya pengeditan (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Teks yang dikenali sebagai pengganti, atau bersama dengan, pesan |

Kata depan dan kata fungsi lainnya diabaikan jika terdapat kata lain di sekitarnya. Huruf yang mirip yang tercampur dalam sebuah kata (misalnya huruf Latin *"a"* di dalam kata Cyrillic), huruf Unicode lebar penuh dan dekoratif, serta karakter tak terlihat, dinormalisasi.

## Bahasa

Bahasa ditentukan per catatan berdasarkan skrip dan huruf-hurufnya:

| Skrip | Pencocokan |
| --- | --- |
| Huruf Sirilik | Lema bahasa Rusia dan Ukraina dengan [pymorphy3](https://github.com/no-plagiarism/pymorphy3). Tanpa kamus Ukraina opsional, digunakan stemmer Ukraina yang ringan |
| Latin | Stemmer Snowball bahasa Inggris; tanda diakritik diabaikan |
| Bahasa Mandarin, Jepang, Korea, Thailand, Laos, Khmer, Myanmar | Pasangan karakter yang tumpang tindih: frasa apa pun ditemukan tanpa spasi. Kueri dalam bahasa Mandarin dipisahkan menjadi kata-kata menggunakan Jieba |
| Skrip lainnya | Kata-kata yang tepat |

Kamus Ukraina (`pymorphy3-dicts-uk`) didistribusikan di bawah lisensi GPL-3.0, sehingga tidak diinstal secara default. Instal dengan `pip install "tgwitness[uk-dictionary]"`; indeks akan mendeteksi penganalisis baru dan membangun ulang dirinya sendiri.

## Di mana indeks tersebut berada

| Mode | Penyimpanan | Penggunaan |
| --- | --- | --- |
| Di disk (default) | `search/fulltext.sqlite3` di direktori workspace | Arsip berukuran besar; tetap utuh meskipun sistem di-restart |
| Hanya di memori | Tidak ada data yang disimpan di disk; dibangun ulang setiap kali dijalankan | Tidak ada salinan turunan dari teks pesan di disk |
| Mati | Tanpa indeks; **Yang terbaru terlebih dahulu · teks yang tepat** tetap dipertahankan | Instalasi minimal |

Administrator utama memilih mode di bawah **Jurnal → Filter → Indeks pencarian** untuk setiap ruang kerja. `TGWITNESS_FULLTEXT=disk|memory|off` menetapkan pengaturan default untuk ruang kerja yang tidak memiliki pilihan sendiri. Beralih ke "memori" atau "mati" akan menghapus berkas tersebut. Berkas indeks memiliki perlindungan yang sama dengan jurnal: berkas tersebut disimpan di direktori data pribadi. Berkas ini tidak dienkripsi, dan tidak termasuk dalam cadangan atau salinan di luar lokasi.

Catatan baru diindeks di latar belakang dalam hitungan detik; pencarian juga mengindeks backlog singkat terlebih dahulu, sehingga catatan yang baru saja disimpan dapat ditemukan. Jurnal yang sudah ada diindeks setelah pembaruan tanpa memblokir panel; hingga saat itu, hasil pencarian mencakup catatan yang telah diindeks dan jurnal menampilkan kemajuan proses. **Pembuatan ulang indeks** dimulai kembali dari catatan pertama.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` panel harus dihentikan (kode keluar 3 jika tidak). Dengan `--json`, keluaran standar hanya menampilkan hasilnya; kemajuan ditampilkan di kesalahan standar.

## Hasil dan jurnal yang ditandatangani

Indeks menyimpan nomor urut dan hash dari catatan jurnal terakhir yang dicakupnya serta memeriksa keduanya dengan jurnal saat dibuka. Jurnal yang diganti, dipulihkan, atau diedit akan memicu proses pembaruan indeks. Setiap respons melaporkan posisi ini, dan setiap pencocokan dibaca kembali dari jurnal yang ditandatangani berdasarkan nomor urutnya: indeks menentukan catatan mana yang akan ditampilkan dan urutannya, bukan isinya. Akses obrolan diterapkan pada bidang obrolan jurnal itu sendiri, bukan pada konten indeks.

## Teks yang dikenali

OCR dan transkrip tetap berada dalam artefak terenkripsinya. Indeksnya hanya ada di memori dan dibangun kembali saat pekerjaan pengenalan selesai. Hasil yang cocok muncul dalam `media.saved` catatannya, diberi label sebagai pengenalan mesin beserta mesin, model, dan kutipan; hasil tersebut tidak pernah ditampilkan sebagai teks yang dikirim di Telegram. Indeks yang sama digunakan untuk **Pencarian Teks yang Telah Dikenali**, yang juga tetap mencocokkan substring biasa.

## Akses

Akses yang dibatasi pada obrolan hanya menemukan catatan dari obrolan tersebut, termasuk teks yang dikenali dari lampirannya. `chat:` dan filter lainnya hanya dapat mempersempit kumpulan tersebut. Status indeks yang ditampilkan pada akses terbatas tidak mencakup total jurnal. Hanya administrator utama yang dapat mengubah mode atau membangun ulang indeks.

## Tanyakan kepada arsip dan MCP

**Minta arsip** untuk mengambil sumbernya dari indeks ini setelah selesai: hasil pencocokan terbaik di seluruh obrolan yang dipilih, dengan teks yang disimpan dihitung satu kali. Hingga 24 sumber dikirim; teks panjang dipotong di sekitar bagian yang cocok dan ditandai sebagai terpotong. Pertanyaan tentang perubahan terbaru, versi pesan yang disimpan, dan pencarian saat indeks masih dalam proses pembuatan menggunakan pengambilan kronologis sebelumnya. Pratinjau menunjukkan metode mana yang digunakan.

Klien MCP dapat memanggil `search_messages` dengan `ranked=true` dan halaman dengan `next_offset`. Koneksi yang dibatasi cakupannya hanya menerima obrolan mereka sendiri.

Ranked pagination covers at most the first 1,000 results, regardless of page size. Narrow the query, chat or period to inspect further matches. Newest-first searches order messages, OCR and transcription results before selecting each page.

## Ketergantungan

| Paket | Lisensi | Mengapa |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Lema bahasa Rusia dan Ukraina; kamus dimuat secara lokal |
| snowballstemmer | BSD-3-Klausul | Bentuk dasar kata dalam bahasa Inggris, Python murni |
| jieba | MIT | Segmentasi kueri bahasa Mandarin, Python murni (hanya distribusi sumber) |
| pymorphy3-dicts-uk (opsional) | GPL-3.0 | Kamus bahasa Ukraina lengkap |

SQLite FTS5 dengan `unicode61` tokenizer; ini merupakan bagian dari SQLite dalam build Python saat ini. Tanpa itu, pencarian kecocokan terbaik akan melaporkan bahwa fitur tersebut tidak tersedia.

## Tolok ukur

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`membuat jurnal terverifikasi yang deterministik berisi campuran pesan dalam bahasa Rusia, Ukraina, Inggris, Mandarin, dan Jepang beserta tautan dan handle di 200 obrolan, membangun indeks, serta mengukur waktu pencarian tipikal (50 hasil, median dari 7 kali eksekusi).

Diuji pada Windows 11, Intel Core i9-13900K, 128 GB RAM, Python 3.12.10, SQLite 3.49.1, data pada drive exFAT, alat analisis `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Ukuran | Hasil |
| --- | --- |
| Jurnal yang ditandatangani | 1.000.000 pesan, 1,50 GiB, ditulis dalam 19 menit |
| Pembuatan indeks dari jurnal | 71 detik, sekitar 14.141 pesan per detik |
| Berkas indeks | 58 MiB, 3,8% dari jurnal |
| Cari segera setelah catatan baru | Median 8 ms, p95 9 ms |
| Pencarian substring sebelumnya, jurnal yang sama | `перевод` 3,2 detik, `银行转账` 2,6 detik, `verify-account.example` 2,6 detik |

| Cari | Catatan yang cocok | Kecocokan terbaik, median | hal. 95 | Yang terbaru terlebih dahulu, median |
| --- | --- | --- | --- | --- |
| Kata umum, bentuk kata: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Dua kata: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Kata langka: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Frasa yang tepat: `"переказ коштів на картку"` | tidak dihitung | 35 ms | 36 ms | 6 ms |
| Domain beserta subdomainnya: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @username: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Bahasa Mandarin tanpa spasi: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Bahasa Jepang: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Bentuk dasar dalam bahasa Inggris: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| ATAU dan pengecualian: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Filter obrolan: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Filter periode: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Sebuah frasa yang tepat diperiksa secara harfiah pada kandidat berdasarkan urutan peringkat hingga halaman penuh, sehingga jumlahnya tidak dihitung. Waktu yang dibutuhkan bertambah seiring dengan jumlah catatan yang cocok; mempersempit obrolan atau periode akan mempercepat pencarian yang luas. Korpus sintetis ini mengulang kosakata yang terbatas, sehingga kata-kata umum cocok dengan jauh lebih banyak catatan daripada dalam obrolan nyata.
