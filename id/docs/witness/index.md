# Siapkan bot saksi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/witness/

Proses terpisah memeriksa jurnal Anda dan menerbitkan checkpoint bertanda tangan ke sebuah kanal.

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

Buat bot dengan BotFather dan izinkan ia memposting di kanal Anda. Jalankan saksi di tempat lain: host lain, idealnya dikelola orang lain, jauh lebih berharga daripada proses kedua di samping kolektor.

## Tiga langkah di bagian Ekstra

1. **Akses baca-saja.** **Tambahan → Saksi independen**, buat token, simpan berkasnya. Ia membaca checkpoint dan status, tidak lebih.
2. **Kanal dan interval.** Kanal Telegram atau webhook Discord, ditambah alamat kolektor yang bisa dijangkau saksi. Simpan berkas pengaturan.
3. **Jalankan.** Taruh `witness.json`, `witness-token.txt`, dan `bot-token.txt` bersama di host saksi lalu jalankan:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Tunggu postingan bertanda tangan pertama di kanal, lalu simpan sidik jari saksi di tempat aman.

Lebih suka Discord? Simpan URL webhook sebagai `discord-webhook.txt`. Satu saksi memposting ke satu tempat; pemeriksaan panjang tiba di Discord sebagai berkas.

## Pilih seberapa sering ingin mempublikasikan

Memposting setiap pemeriksaan memberi catatan luar yang rutin: setiap lima menit berarti sekitar 288 postingan per hari per ruang kerja. Pengaturan lanjutan bisa memposting hanya saat ada perubahan atau masalah, memakai proxy, atau Bot API khusus.

**Apa sebenarnya yang dibuktikan oleh bot tersebut?**

Ia meminta checkpoint bertanda tangan dari kolektor, memeriksanya dengan kunci yang diharapkan, dan menyimpan jurnal bertanda tangan sendiri, termasuk jawaban yang terlewat dan ditolak.

Ia memeriksa keadaan jurnal, tidak mengamati Telegram sendiri. Untuk itu, lakukan uji pengiriman terkendali.

## Periksa bukti tersebut nanti

Simpan jurnal saksi, postingan, dan sidik jarinya. [Cara memeriksanya](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/#verify) terhadap ekspor kolektor.
