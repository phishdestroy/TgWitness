# Carian penuh

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/search/

Cari mesej yang disimpan mengikut bentuk kata, frasa tepat, domain dan @nama pengguna, padanan terbaik diutamakan, dengan indeks diikat kepada jurnal yang disahkan.

[Analisis arkib](https://phishdestroy.github.io/TgWitness/ms/docs/reference/analysis/) · [OCR tempatan dan transkripsi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Pratinjau.** Dalam **Jurnal**, pilih **Padanan terbaik · bentuk kata** di sebelah medan carian. Keputusan disusun mengikut BM25 dan memadankan bentuk lain bagi kata yang sama: *перевод* menemui *переводом* dan *переводы*, *transfer* menemui *transfers*, frasa Cina ditemui tanpa ruang. **Terbaru dahulu · teks tepat** mengekalkan carian subrentetan sebelumnya merentasi keseluruhan rekod.

Indeks adalah data terbitan. Ia dibina semula daripada jurnal yang disahkan, tidak pernah disahkan sendiri dan tidak pernah dieksport. Rekod asal tidak berubah.

## Sintaks carian

| Tulis | Menemui |
| --- | --- |
| `перевод карта` | Rekod yang mengandungi kedua-dua perkataan, dalam apa jua bentuk |
| `"переводом на карту"` | Ungkapan tepat, dalam susunan ini |
| `бонус OR подарок` | Mana-mana perkataan |
| `перевод -казино` | Merekod tanpa perkataan yang dikecualikan |
| `example.com` | Domain dan subdomainnya, juga dalam pautan tersembunyi dan URL butang |
| `@username`, `t.me/username` | Sebutan dan pautan akaun, serta mesej yang dihantarnya |
| `#tag` | Tagar |
| `+79991234567`, alamat dompet, alamat e-mel | Nilai yang sama dalam teks atau pautan |
| `from:@username`, `from:123456` | Mesej daripada penghantar tersebut |
| `chat:-1001234567890` | Satu sembang; ia hanya boleh mengehadkan akses anda sendiri |
| `id:42` | Versi yang disimpan bagi mesej 42 |
| `since:2026-01-01 until:2026-01-31` | Tempoh pemerhatian; tarikh tanpa masa merangkumi sepanjang hari |
| `kind:edited` | Hanya suntingan (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Teks yang diiktiraf sebagai ganti, atau bersama, mesej |

Preposisi dan kata fungsi lain diabaikan apabila terdapat perkataan lain. Huruf yang kelihatan serupa yang dicampurkan ke dalam perkataan (huruf Latin *a* di dalam perkataan Sirilik), huruf lebar penuh dan huruf hiasan Unicode serta aksara tidak kelihatan dinormalisasikan.

## Bahasa

Bahasa dikesan bagi setiap rekod berdasarkan skrip dan hurufnya:

| Skrip | Padanan |
| --- | --- |
| Sirilik | Lemma Rusia dan Ukraine dengan [pymorphy3](https://github.com/no-plagiarism/pymorphy3). Tanpa kamus Ukraine pilihan, pemungot batang ringan Ukraine digunakan |
| Latin | Pemangkas stem English Snowball; diacritik diabaikan |
| Bahasa Cina, Jepun, Korea, Thai, Laos, Khmer, Myanmar | Pasangan aksara bertindih: mana-mana frasa ditemui tanpa ruang. Soalan Cina dipecahkan kepada perkataan menggunakan jieba |
| Skrip lain | Kata-kata tepat |

Kamus Ukraine (`pymorphy3-dicts-uk`) diedarkan di bawah GPL-3.0, jadi ia tidak dipasang secara lalai. Pasang ia dengan `pip install "tgwitness[uk-dictionary]"`; indeks mengesan penganalisis baru dan membina semula dirinya.

## Di mana indeks berada

| Mod | Penyimpanan | Gunakan |
| --- | --- | --- |
| Pada cakera (laluan lalai) | `search/fulltext.sqlite3` dalam direktori ruang kerja | Arkib besar; tahan terhadap permulaan semula |
| Hanya dalam memori | Tiada apa-apa pada cakera; dibina semula setiap kali permulaan | Tiada salinan terbitan teks mesej pada cakera |
| Padam | Tiada indeks; **yang terbaru dahulu · teks tepat** kekal | Pemasangan minimum |

Pentadbir utama memilih mod di bawah **Jurnal → Penapis → Indeks carian** untuk setiap ruang kerja. `TGWITNESS_FULLTEXT=disk|memory|off` Menetapkan lalai untuk ruang kerja yang tiada pilihan sendiri. Menukar kepada memori atau dimatikan akan memadam fail tersebut. Fail indeks mempunyai perlindungan yang sama seperti jurnal: ia terletak di direktori data peribadi. Ia tidak disulitkan, dan bukan sebahagian daripada sandaran atau salinan luar tapak.

Rekod baharu diindeks di latar belakang dalam beberapa saat; carian juga mengindeks timbunan rekod lama yang pendek terlebih dahulu, supaya rekod yang disimpan sebentar tadi dapat ditemui. Jurnal sedia ada diindeks selepas kemas kini tanpa menyekat panel; sehingga saat itu, keputusan merangkumi rekod yang telah diindeks dan jurnal memaparkan kemajuan. **Membina semula indeks** bermula semula daripada rekod pertama.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` perlu panel dihentikan (kod keluar 3 jika tidak). Dengan `--json`, keluaran piawai hanya mengandungi keputusan; kemajuan dihantar ke ralat piawai.

## Keputusan dan jurnal yang disahkan

Indeks menyimpan nombor urutan dan hash rekod jurnal terakhir yang diliputinya dan menyemak keduanya dengan jurnal apabila ia dibuka. Jurnal yang diganti, dipulihkan atau disunting menyebabkan pembinaan semula. Setiap respons melaporkan kedudukan ini, dan setiap padanan dibaca semula daripada jurnal berterasima berdasarkan nombor urutannya: indeks menentukan rekod mana yang hendak dipaparkan dan dalam susunan apa, bukan kandungannya. Akses sembang diterapkan pada medan sembang jurnal itu sendiri, bukan pada kandungan indeks.

## Teks yang diiktiraf

OCR dan transkrip kekal dalam artifak yang disulitkan. Indeks mereka wujud hanya dalam memori dan dibina semula apabila tugas pengecaman selesai. Keputusan muncul pada `media.saved` rekodnya, dilabel sebagai pengecaman mesin dengan enjin, model dan petikan; ia tidak pernah dipaparkan sebagai teks yang dihantar dalam Telegram. Indeks yang sama digunakan untuk **Cari teks yang diiktiraf**, yang masih juga mengpadankan subrentetan biasa.

## Akses

Akses skop sembang hanya menemui rekod daripada sembang anda, termasuk teks yang diiktiraf daripada lampirannya. `chat:` dan penapis lain hanya boleh menyempitkan set itu. Status indeks yang dipaparkan kepada akses berlingkup mengabaikan jumlah jurnal. Hanya pentadbir utama boleh menukar mod atau membina semula indeks.

## Tanya arkib dan MCP

**Permintaan arkib** mendapatkan sumbernya daripada indeks ini apabila ia lengkap: padanan terbaik merentasi sembang terpilih, dengan teks yang disimpan dikira sekali sahaja. Sehingga 24 sumber dihantar; teks panjang dipotong di sekitar padanan mereka dan ditandakan sebagai dipendekkan. Soalan mengenai perubahan terkini, versi simpanan satu mesej, dan carian semasa indeks masih dibina menggunakan pengambilan kronologi sebelumnya. Pratonton menunjukkan kaedah yang digunakan.

Klien MCP boleh memanggil `search_messages` dengan `ranked=true` dan halaman dengan `next_offset`Sambungan berbeza menerima hanya sembang mereka.

Ranked pagination covers at most the first 1,000 results, regardless of page size. Narrow the query, chat or period to inspect further matches. Newest-first searches order messages, OCR and transcription results before selecting each page.

## Kebergantungan

| Pakej | Lesen | Mengapa |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Lemma Rusia dan Ukraine; kamus dimuat secara tempatan |
| snowballstemmer | Klausul BSD-3 | Asas bahasa Inggeris, Python tulen |
| jieba | MIT | Segmentasi pertanyaan Cina, Python tulen (edaran sumber sahaja) |
| pymorphy3-dicts-uk (pilihan) | GPL-3.0 | Kamus Ukraine lengkap |

SQLite FTS5 dengan `unicode61` penoken diperlukan; ia adalah sebahagian daripada SQLite dalam binaan Python semasa. Tanpa ia, carian padanan terbaik melaporkan bahawa ia tidak tersedia.

## Penanda aras

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`mencipta jurnal berasingan deterministik yang mengandungi mesej campuran Rusia, Ukraine, Inggeris, Cina dan Jepun dengan pautan dan pemegang dalam 200 sembang, membina indeks dan mencatat masa carian tipikal (50 keputusan, median daripada 7 larian).

Diukur pada Windows 11, Intel Core i9-13900K, 128 GB RAM, Python 3.12.10, SQLite 3.49.1, data pada pemacu exFAT, penganalisis `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Ukur | Keputusan |
| --- | --- |
| Jurnal yang ditandatangani | 1,000,000 mesej, 1.50 GiB, ditulis dalam 19 minit |
| Indeks binaan daripada jurnal | 71 s, kira-kira 14,141 mesej sesaat |
| Fail indeks | 58 MiB, 3.8% daripada jurnal |
| Cari sejurus selepas rekod baru | Median 8 ms, p95 9 ms |
| Carian substring sebelumnya, jurnal yang sama | `перевод` 3.2 s, `银行转账` 2.6 s, `verify-account.example` 2.6 s |

| Cari | Rekod padanan | Padanan terbaik, median | p95 | Yang terbaru dahulu, median |
| --- | --- | --- | --- | --- |
| Kata biasa, bentuk kata: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Dua perkataan: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Kata jarang: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Frasa tepat: `"переказ коштів на картку"` | tidak dikira | 35 ms | 36 ms | 6 ms |
| Domain dengan subdomain: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @nama pengguna: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Bahasa Cina tanpa ruang: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Jepun: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Akar bahasa Inggeris: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| ATAU dan pengecualian: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Penapis sembang: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Penapis tempoh: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Sebuah frasa tepat diperiksa secara harfiah pada calon dalam susunan pangkat sehingga halaman penuh, jadi jumlahnya tidak dikira. Masa meningkat selari dengan bilangan rekod yang sepadan; mengehadkan sembang atau tempoh menjadikan carian luas lebih pantas. Korpus sintetik mengulangi perbendaharaan kata yang kecil, jadi perkataan biasa sepadan dengan lebih banyak rekod berbanding sembang sebenar.
