# Siapkan bot saksi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/witness/

Biarkan proses terpisah memeriksa jurnal tersebut dan mempublikasikan titik pemeriksaan yang ditandatangani ke saluran Anda.

## Dua server, dua kunci penandatanganan

HOST A / COLLECTOR**Akun + jurnal**

Kunci penandatanganan Pengumpul Sesi Telegram

Titik akhir checkpoint yang hanya dapat dibaca

← minta jawaban yang ditandatangani →

HOST B / WITNESS**Verifikasi + simpan**

Sidik jari pengumpul yang disematkan Kunci penandatanganan saksi terpisah

Jurnal sendiri + token bot

Witness → Telegram Bot API →**Saluran Anda · posting TGW1 yang ditandatangani**

Witness melakukan verifikasi sendiri. Akses pengumpul bersifat hanya baca. Publikasi bot menggunakan koneksi dan token Witness; tidak ada sesi akun yang diberikan kepada Witness.

03 / KEPUTUSAN CHECKPOINTContoh jawaban

TERAKHIR DITERIMA**120 catatan**`head 9c7d…`

JAWABAN BERIKUTNYA**128 catatan**`head a4f2…`

Diterima: jumlahnya bertambah, tanda tangan terverifikasi, dan kuncinya cocok. Saksi mempertahankan batas baru ini.

Semua contoh jawaban mengasumsikan adanya tanda tangan yang valid dan kunci yang disematkan. Hash yang disebutkan di sini hanyalah ilustrasi singkat. Jumlah yang lebih besar saja tidak dapat membuktikan bahwa seluruh prefiks lama tetap tidak berubah; bandingkan ekspor tersebut dengan titik pemeriksaan yang disimpan.

## Siapkan bot dan saluran

Buat bot menggunakan BotFather dan izinkan bot tersebut untuk memposting di saluran yang Anda kendalikan. Pilih komputer atau server untuk TgWitness. Host dan operator yang terpisah memberikan kemandirian yang lebih kuat dibandingkan dengan menjalankan proses kedua di server pengumpul data.

## Tiga langkah di bagian Ekstra

1. **Akses hanya baca.** Buka **Ekstra → Bot di saluran Anda**, buat token saksi, dan simpan berkas akses. Fitur ini memungkinkan Anda membaca titik pemeriksaan dan status kesehatan, bukan percakapan atau pengaturan pengumpul.
2. **Saluran dan interval.** Masukkan saluran dan alamat pengumpul yang dapat dijangkau dari saksi. Simpan berkas pengaturan.
3. **Peluncuran.** Gabungkan `witness.json`, `witness-token.txt`, dan `bot-token.txt` yang dibuat di host saksi. Jalankan perintah di bawah ini di lingkungan proyek yang telah diinstal.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Mengunduh berkas-berkas tersebut tidak akan memulai proses pencatatan. Pastikan posting pertama yang telah ditandatangani muncul di saluran, lalu simpan sidik jari kunci publik alat tersebut secara terpisah.

## Pilih seberapa sering ingin mempublikasikan

Setiap kali pemeriksaan dipublikasikan, akan tercipta catatan eksternal yang teratur. Dengan interval lima menit, hal ini berarti sekitar 288 posting per ruang kerja per hari. Pengaturan lanjutan juga menawarkan publikasi terkait perubahan atau masalah, proxy, serta alamat Bot API khusus.

**Apa sebenarnya yang dibuktikan oleh bot tersebut?**

Saksi meminta titik pemeriksaan yang ditandatangani dari pengumpul, memverifikasinya dengan kunci yang diharapkan, dan menyimpan jurnal terpisah yang ditandatangani. Alat ini mencatat respons yang hilang dan jawaban yang ditolak, serta pemeriksaan yang berhasil. Publikasi masih bergantung pada apakah saksi sedang berjalan dan dapat mengakses Bot API Telegram.

Alat ini memeriksa status jurnal yang dilaporkan oleh pengumpul. Alat ini tidak memantau setiap pesan Telegram secara mandiri. Untuk itu, tambahkan uji pengiriman terkontrol.

## Periksa bukti tersebut nanti

Simpan jurnal saksi, postingan saluran, dan sidik jari yang disimpan secara independen. [Prosedur verifikasi lengkap](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/#verify) membandingkan semuanya dengan ekspor yang telah ditandatangani oleh pengumpul.
