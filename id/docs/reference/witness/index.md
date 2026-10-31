# Saksi independen

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/

Jalankan TgWitness dengan kunci dan botnya sendiri, publikasikan titik pemeriksaan yang ditandatangani ke saluran, dan periksa ekspor data berdasarkan titik pemeriksaan tersebut.

[Pengaturan bot dan proxy dalam bahasa Rusia](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Sebuah pengumpul menandatangani jurnalnya sendiri, sehingga siapa pun yang mengendalikan pengumpul dan kuncinya secara prinsip dapat mengubah atau memotong jurnal tersebut dan menandatanganinya kembali. Witness membuat hal tersebut dapat terdeteksi. Ini adalah proses terpisah — wadah lain, atau lebih tepatnya server yang dijalankan oleh pihak lain — yang setiap beberapa menit mengambil bagian awal jurnal yang telah ditandatangani oleh pengumpul, menandatangani apa yang dilihatnya dengan kuncinya sendiri, menyimpannya dalam jurnalnya sendiri, dan mempostingnya ke saluran Telegram.

Diagram alur · Pengumpul → Witness (titik pemeriksaan yang ditandatangani: jumlah catatan + hash header); Witness → Jurnal saksi, kunci sendiri; Witness → Saluran Telegram (postingan yang ditandatangani melalui botnya sendiri); Berkas ZIP Bukti → verify.py; Jurnal saksi, kunci sendiri → verify.py; Saluran Telegram → verify.py (Ekspor dari Telegram Desktop atau halaman t.me/s) · Pengumpul · Witness · Jurnal saksi, kuncisendiri · Saluran Telegram · Berkas ZIP Bukti · verify.py · titik pemeriksaan yang · ditandatangani: jumlah · catatan + hash header · postingan yang · ditandatangani melalui · botnya sendiri · Ekspor dari Telegram Desktop · atau halaman t.me/s

**Diagram dalam bentuk teks**

1. Pengumpul → Witness (titik pemeriksaan yang ditandatangani: jumlah catatan + hash header)
2. Witness → Jurnal saksi, kunci sendiri
3. Witness → Saluran Telegram (postingan yang ditandatangani melalui botnya sendiri)
4. Berkas ZIP Bukti → verify.py
5. Jurnal saksi, kunci sendiri → verify.py
6. Saluran Telegram → verify.py (Ekspor dari Telegram Desktop atau halaman t.me/s)

## Apa yang diperoleh oleh TgWitness, dan apa yang tidak

| Saksi tersebut memiliki | Saksi tersebut tidak pernah memiliki |
| --- | --- |
| **Token saksi** yang hanya dapat dibaca untuk satu ruang kerja | Sesi Telegram atau kredensial API pengumpul |
| Kunci Ed25519 dan jurnal miliknya sendiri | Brankas pengumpul, kunci penandatanganan, atau token panel |
| Token bot Telegram miliknya sendiri | Isi pesan: bagian awal berisi jumlah catatan dan hash |

Token dibuat di halaman **Witness** panel, ditampilkan sekali, dan disimpan hanya sebagai SHA-256. Token ini membuka tepat satu titik akhir, `GET /api/witness/head`, yang mengembalikan titik pemeriksaan yang baru ditandatangani beserta penghitung koleksi tanpa konten yang ditandatangani dan status kesehatan operasional. Token ini tidak dapat membuka panel, membaca isi pesan, atau mengubah pengaturan, dan token panel tidak diterima di sana. Cabut token di halaman yang sama. Pengumpul mencatat saat kunci saksi baru mulai melakukan pemeriksaan (`witness.seen`) dan menampilkan pemeriksaan terakhir per token; seorang saksi yang belum melakukan pemeriksaan dalam 2,5 interval akan ditandai sebagai terlambat.

Saksi baru mengirimkan tantangan acak pada setiap jajak pendapat; pernyataan penangkapan mengulanginya di bawah tanda tangan pengumpul. Penghitung terikat pada titik pemeriksaan yang tepat dan disertakan dalam posting saksi yang ditandatangani. Kepala warisan tetap diterima oleh saksi mandiri. Pertumbuhan jurnal saja tidak pernah dihitung sebagai pesan baru.

## Apa yang diperiksa dan dicatat

Setiap interval (secara default 10 menit), TgWitness:

1. mengambil header itu sendiri (pengumpul tidak dapat memaksa atau melewatkannya);
2. memverifikasi tanda tangan pengumpul, kunci pengumpul yang disematkan (`--collector-fingerprint`, atau kunci pertama yang terlihat), jumlah yang tidak berkurang, serta kepala yang tidak berubah pada jumlah yang tidak berubah;
3. menambahkan catatan yang ditandatangani ke jurnalnya sendiri: `witness.anchor` dengan status `ok`, `key_changed`, `rollback` (jumlah catatan lebih sedikit daripada sebelumnya), `fork` (panjangnya sama, head-nya berbeda) atau `invalid` (jawaban gagal verifikasi), atau `witness.no_response` ketika pengumpul tidak menjawab;
4. mengunggah hasilnya ke saluran, yang telah ditandatangani, termasuk "tidak ada jawaban" selama TgWitness sedang berjalan dan dapat mengakses Bot API. ID unggahan dicatat (`witness.posted`), begitu pula unggahan yang gagal (`witness.post_failed`).

Sebuah posting terlihat seperti ini; baris terakhir berisi pernyataan yang telah ditandatangani:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Jalankan TgWitness

Anda memerlukan bot Telegram (buatlah dengan @BotFather), sebuah saluran di mana bot tersebut menjadi administrator, serta alamat pengumpul yang dapat diakses oleh saksi — melalui HTTPS di luar jaringan pribadi (lihat profil HTTPS pada [bagian penerapan](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/)).

Buka **Ekstra → Bot di saluran Anda → Atur bot** di panel. Tiga langkah mencakup akses baca-saja, saluran Anda, dan interval, lalu meluncurkan saksi. Kebijakan publikasi, proxy HTTP/SOCKS5 opsional, dan alamat API Bot khusus terdapat di **pengaturan Lanjutan** . Formulir ini mengunduh `witness.json` dengan kunci pengumpul ruang kerja ini yang disematkan. Unduh token hanya-baca yang baru dibuat dengan **Simpan berkas akses** sebagai `witness-token.txt` ; letakkan berkas tersebut beserta `bot-token.txt` yang dibuat di host saksi di samping berkas JSON tersebut. Pengumpul tidak pernah menerima token bot. Pengunduhan tidak akan memulai layanan atau mempublikasikan pesan. Tidak ada saksi proyek yang dihosting yang secara implisit didaftarkan.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

Perintah pertama memeriksa berkas konfigurasi dan berkas rahasia tanpa permintaan jaringan atau pembuatan kunci. Jalur dalam JSON bersifat relatif terhadap berkas tersebut; jalur CLI/lingkungan bersifat relatif terhadap direktori kerja. Simpan sidik jari saksi di luar hostnya. Indikator "last-poll" pengumpul hanya mengonfirmasi permintaan; publikasi dilaporkan oleh Proof atau diperiksa di jurnal saksi dan saluran.

Jika panel berada di balik terowongan SSH, tampilkan hanya titik akhir saksi yang dibatasi pada nama host HTTPS terpisah dengan [contoh Caddy ini](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). Ruang kerja default kemudian menggunakan `https://witness.example.org`, sedangkan ruang kerja lainnya menggunakan `https://witness.example.org/profiles/ID`. Token tetap diperlukan; panel dan rute API lainnya tidak diteruskan oleh host virtual tersebut.

Pilih `all` untuk titik pemeriksaan yang diterbitkan secara teratur. Interval lima menit berarti sekitar 288 posting per ruang kerja per hari. `changes`/`problems` sengaja tidak mempublikasikan beberapa pemeriksaan. MTProxy diperuntukkan bagi klien Telegram pengumpul data. Pemantauan HTTP dan API Bot HTTPS Telegram menggunakan rute langsung/HTTP/SOCKS5 ([API Bot](https://core.telegram.org/bots/api)) masing-masing.

**Di samping pengumpul, dengan Docker** (host yang sama — proses dan kunci independen, tetapi operator yang sama): masukkan nilai-nilai ke dalam `.env` dan jalankan profil tersebut.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

Jika menggunakan gambar yang telah dipublikasikan, gunakan kode `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**Di server orang lain** (saksi independen yang sesungguhnya): salin repositori ke sana, atur `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` ditambah tiga nilai di atas di `.env`, lalu

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

atau tanpa Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Opsi

| Opsi | Lingkungan | Default | Arti |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Interval waktu antara pemeriksaan, 1–1.440 |
| `--timeout` | `_TIMEOUT` | 30 | Waktu tunggu untuk pengumpul data dan Bot API, 5–600 detik |
| `--post` | `_POST` | `all` | `all`: setiap pemeriksaan; `changes`: masalah baru; `problems`: hanya masalah dan jawaban yang hilang |
| `--title` | `_TITLE` | `TgWitness witness` | Kata-kata pertama dari setiap postingan saluran |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Simpan kunci pengumpul alih-alih mempercayai jawaban pertama |
| `--proxy` | `_PROXY` | langsung | `socks5://host:port` atau `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Alamat API Bot, misalnya server API Bot lokal |
| `--data-dir` | `_DATA` | `witness-data` | Kunci saksi dan jurnal |
| `--config` | `_CONFIG` | – | Berkas JSON dengan salah satu opsi di atas |

Alamat pengumpul, token, dan saluran berasal dari `--collector`, `--token`, atau `--token-file`, `--bot-token`, `--bot-token-file`, dan `--channel`, atau `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, dan `_CHANNEL`, yang menjaga kerahasiaan di luar daftar proses.

Sebuah berkas konfigurasi menggunakan nama opsi dengan garis bawah, ditambah `texts`, yang menggantikan kata-kata dalam postingan saluran:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Kunci `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Baris perintah lebih diutamakan daripada lingkungan, dan lingkungan lebih diutamakan daripada berkas. Opsi atau kunci teks yang tidak dikenal akan menghentikan proses pencatatan dengan menampilkan pesan, bukan diabaikan. Penyusunan kata tidak pernah memengaruhi verifikasi: verify.py memeriksa token yang ditandatangani di akhir setiap posting. Dengan `--post changes` atau `problems`, pemeriksaan yang tidak diposting tetap ada di jurnal saksi dan `verify.py` mencantumkannya sebagai tidak pernah diposting; catatan awal menyebutkan kebijakan tersebut. Setiap pemeriksaan tetap muncul di jurnal, sehingga semakin sedikit posting berarti semakin sedikit waktu Telegram yang independen, bukan semakin sedikit pemeriksaan.

Tanpa saluran, TgWitness tetap menyimpan jurnalnya. Simpan sidik jari kunci TgWitness (`python -m tgwitness.witness fingerprint`) di tempat lain.

## Verifikasi

Dari sisi saksi, ekspor jurnalnya:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Kemudian, di mana saja, dengan berkas ZIP yang telah ditandatangani oleh pengumpul dan saluran yang diekspor dari Telegram Desktop (*Ekspor riwayat obrolan* → JSON menghasilkan `result.json` ) atau halaman publik `https://t.me/s/…` -nya:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` memeriksa jurnal saksi (rantai dan tanda tangan), kemudian memastikan bahwa **setiap head yang dilihat saksi merupakan bagian dari jurnal yang diekspor**: catatan pada hitungan tersebut harus memiliki hash yang persis sama. Head yang tidak cocok akan gagal verifikasi — jurnal tersebut telah diubah setelah saksi melihatnya. Alat ini juga melaporkan header yang terlihat setelah ekspor, anomali yang dicatat oleh saksi, jawaban yang gagal, periode yang titik periksa pencocokannya terdapat dalam ekspor ini ("Disaksikan dari X hingga Y"), dan celah. Titik periksa selanjutnya tidak memperpanjang periode tersebut. Hasilnya mencakup nomor catatan terakhir yang cocok dan jumlah catatan berikutnya tanpa titik pemeriksaan yang cocok. Hanya jawaban yang ditandatangani oleh kunci ekspor itu sendiri yang dihitung: ekspor yang ditandatangani oleh kunci yang tidak pernah dilihat saksi dilaporkan sebagai tidak disaksikan, dan tanpa `--fingerprint`, penandatanganannya tetap tidak terikat. Dengan `--channel`, setiap posting yang ditandatangani harus cocok dengan jurnal saksi catatan demi catatan: posting yang diubah gagal verifikasi, sedangkan posting yang hilang dicantumkan. Tanggal dalam ekspor JSON Telegram yang disediakan merupakan metadata yang dapat diedit, di luar token saksi yang ditandatangani. Kecocokan token tidak mengautentikasi tanggal publikasi; hasilnya secara eksplisit melaporkan bahwa verifikasi waktu publikasi tidak dilakukan.

### Memerlukan batas ekspor yang disaksikan

Untuk serah terima yang harus menyertakan catatan akhir yang disaksikan, tambahkan `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Hal ini memerlukan sidik jari saksi yang disimpan secara independen dan titik pemeriksaan yang cocok tepat di akhir ekspor ini. Titik pemeriksaan yang hanya mencakup awalan sebelumnya tidak memadai. Hentikan sementara pengumpulan, biarkan saksi mengamati keadaan akhir, dan ekspor sebelum penulisan jurnal lebih lanjut; jika jurnal berubah, simpan titik pemeriksaan lain dan ekspor keadaan tersebut. Titik pemeriksaan yang lebih baru saja tidak dapat memverifikasi hash akhir dari ekspor yang lebih pendek. Ketika `--channel` juga disertakan, postingan yang diklaim hilang atau kumpulan kecocokan yang kosong akan gagal dalam pemeriksaan ketat ini. Tanpa bendera tersebut, pemeriksaan integritas biasa tetap melaporkan catatan yang tidak disaksikan tanpa menolak arsip yang sebaliknya utuh.

Penanda ini memastikan konsistensi dengan catatan saksi yang disediakan dan disematkan. Operator tetap harus memastikan independensi saksi dan menyimpan catatannya secara terpisah. Penanda ini tidak menjamin kebenaran pesan, kelengkapan pengumpulan, atau durasi operasi yang diukur secara independen.

Sebuah "witness" menunjukkan apa yang dilaporkan oleh pengumpul pada saat-saat tersebut dan bahwa ekspor yang dilakukan kemudian sesuai dengan laporan tersebut. "Witness" ini tidak menunjukkan bahwa pengumpul telah merekam semua yang dikirimkan oleh Telegram, atau bahwa isi pesan tersebut benar. Sebuah "witness" yang dijalankan oleh operator yang sama pada mesin yang sama memiliki kredibilitas yang lebih rendah daripada yang dijalankan oleh orang lain.

Peningkatan jumlah saja tidak dapat membuktikan kontinuitas "append-only" secara daring: perbandingan offline harus mencocokkan setiap hash prefiks yang disimpan dengan ekspor lengkap dari pengumpul. Waktu henti saksi dan kegagalan publikasi menyebabkan interval tanpa titik acuan eksternal. Postingan yang hilang dapat dilaporkan berdasarkan jurnal saksi yang disimpan; baik saluran maupun server yang dikendalikan oleh operator yang sama bukanlah arsip pihak ketiga yang tidak dapat diubah.
