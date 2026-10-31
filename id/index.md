# Pesan bisa berubah. Simpan apa yang Anda lihat.

Canonical page: https://phishdestroy.github.io/TgWitness/id/

[Sumber terbuka / v0.7.0](https://phishdestroy.github.io/TgWitness/id/docs/reference/changelog/)

Rekam pesan Telegram, pertahankan perubahannya, dan ekspor catatan yang telah ditandatangani.

[Buka demo](https://phishdestroy.github.io/TgWitness/demo/?lang=id)[Panduan pengaturan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=id)

Demo ini menggunakan data fiktif. Tidak diperlukan login Telegram.

 [Pengambilan melalui GitHub Actions (pratinjau)](https://phishdestroy.github.io/TgWitness/id/docs/capture/) [Salinan di luar situs S3: pengaturan dan pemulihan](https://phishdestroy.github.io/TgWitness/id/#s3)

SEBUAH PESAN, MELINTASI WAKTU #0042

Northstar · PenelitianSumber fiktif / pesan 42

1. **Pesan yang terdeteksi:**09:41:02

   Pengarahan dimulai di 14:00.
2. **Pengeditan dipertahankan**09:43:18

   Pengarahan dimulai di 15:00.

   Versi sebelumnya tetap dipertahankan
3. **Pemberitahuan penghapusan**10:06:45

   Konten yang direkam tetap tersimpan di jurnal Anda.

Tiga pengamatan. Satu riwayat. CONTOH

Pesan tersebut menghilang. Riwayat yang terekam tetap ada.

## Setiap perubahan yang terekam. Tepat di tempat yang Anda butuhkan.

Jelajahi antarmuka dengan data demonstrasi fiktif.

TgWitness / Percakapan yang disimpanRUANG KERJA PENGAMATAN ANDA

![Percakapan Telegram yang disimpan dalam tema gelap, dengan suntingan dan pesan yang dihapus tetap disimpan dalam konteksnya](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Percakapan yang Disimpan Tampilan percakapan yang familiar, dengan catatan pengeditan dan pemberitahuan penghapusan yang terekam di samping pesan-pesan tersebut.

TgWitness / JurnalRUANG KERJA LOKAL

![Jurnal yang berisi pesan yang teramati, pengeditan, pemberitahuan penghapusan, dan peristiwa yang tercakup](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Jurnal: Garis waktu yang dapat dicari mengenai apa yang teramati oleh akun Anda, termasuk gangguan.

TgWitness / Riwayat pengeditanRUANG KERJA LOKAL

![Panel detail yang membandingkan versi pesan sebelumnya yang terekam dengan versi yang telah diedit](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Riwayat pengeditan: Bandingkan versi yang telah direkam tanpa menimpa catatan sebelumnya.

TgWitness / Ekspor yang ditandatanganiRUANG KERJA LOKAL

![Fitur ekspor ruang kerja yang menyediakan berkas ZIP, JSONL, CSV, dan laporan HTML offline yang telah ditandatangani](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Ekspor yang ditandatangani Bawa jurnal tersebut bersama Anda, lengkap dengan daftar isi dan verifikator independen.

01 / PENANGKAPAN

### Anda yang menentukan cakupannya.

Obrolan yang dipilih, folder Telegram, atau seluruh akun. Ruang kerja terpisah untuk setiap akun.

[Bandingkan mode pengumpulan](https://phishdestroy.github.io/TgWitness/id/guides/modes.html#scope)

02 / PRESERVE

### Perubahan menambah nilai pada cerita.

Versi yang "Captured", pemberitahuan penghapusan, dan celah pengamatan tetap tercatat dalam jurnal.

[Lihat matriks peristiwa](https://phishdestroy.github.io/TgWitness/id/guides/modes.html#events)

03 / PENYERAHAN

### Sebuah catatan yang dapat diakses di mana saja.

ZIP yang ditandatangani, file yang dipertahankan, dan laporan offline. Perlindungan kata sandi opsional.

[Ekspor dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/exports/)

## Ubah satu byte. Rantai blok akan memberitahukannya kepada Anda.

Setiap peristiwa tertaut ke hash sebelumnya dan dilengkapi dengan tanda tangan Ed25519.

![Peristiwa yang direkam terhubung ke hash sebelumnya, dilengkapi tanda tangan, dan disimpan dalam format ekspor yang dapat diverifikasi.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Mengubah catatan yang telah direkam akan mengubah hash-nya dan merusak verifikasi catatan yang tertaut.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Titik pemeriksaan yang disimpan secara terpisah memungkinkan penerima membandingkan jurnal yang diekspor dengan catatan sebelumnya.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Lihat apa yang ditetapkan oleh masing-masing mekanisme verifikasi, serta di mana batasannya tetap berada.

[Jelajahi delapan tingkat bukti](https://phishdestroy.github.io/TgWitness/id/guides/modes.html#levels)

## Siap untuk ditinjau oleh pihak lain.

Serahkan hasil pengamatan, berkas, dan laporan HTML offline dalam satu paket yang telah ditandatangani.

[Baca model bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/)

tgwitness-evidence.zipPAKET YANG TELAH DITANDATANGANI

- 01

  Pengamatan asliCatatan JSONL + tabel CSV
- 02

  Konteks yang mudah dipahamiLaporan HTML offline + media yang disimpan
- 03

  Verifikasi independenManifest yang ditandatangani + verifikator mandiri

Tanda tangan mendeteksi adanya manipulasi berdasarkan kunci tepercaya. Tanda tangan tersebut tidak membuktikan asal pesan dari Telegram atau menjamin pencatatan yang lengkap. Isi jurnal dan media memerlukan penyimpanan terenkripsi yang disediakan oleh Anda.

## Salinan S3. Pemeriksaan eksternal.

Simpan salinan terenkripsi dan tambahkan pemeriksaan independen.

Dinonaktifkan secara default

### Salin semuanya ke penyimpanan yang kompatibel dengan S3

Jurnal, file, titik pemeriksaan berstempel waktu, dan ekspor obrolan — dienkripsi sebelum diunggah ke AWS S3 atau penyimpanan yang kompatibel.

**Pengaturan penyimpanan dan pemulihan**

Enkripsi sisi klien

`AES-256-GCM` mengenkripsi objek di mesin ini. Penyedia menerima objek yang telah dienkripsi.

Pencadangan terjadwal atau manual

Salin sekarang, atau pilih interval antara 1 hingga 1.440 menit. Periksa kemajuan di panel.

Object Lock

Pilih jangka waktu penyimpanan dan mode jika bucket mendukungnya. Panel tersebut melaporkan apakah penyimpanan telah dikonfirmasi pada objek yang diunggah.

Pemulihan yang terverifikasi

Unduh kunci enkripsi dan simpan secara terpisah. Pulihkan di mesin lain; berkas-berkas tersebut hanya akan dipublikasikan setelah diverifikasi.

![Panel salinan lengkap di luar situs: titik akhir, wilayah, bucket, kunci akses, jadwal, penguncian objek, dan kontrol kunci pemulihan](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Panel lengkap dengan opsi lanjutan yang diperluas. Tidak ada kredensial penyimpanan yang ditampilkan.

Jurnal dan media`AES-256-GCM`Penyimpanan yang kompatibel dengan S3

[Konfigurasikan S3 dan pulihkan salinan](https://phishdestroy.github.io/TgWitness/id/docs/exports/#s3)[Baca detail verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Yang tidak dilakukan** Alat ini tidak dapat memulihkan pesan tanpa kunci dekripsi yang diekspor atau menggantikan saksi independen.

### Pemberitahuan · Apprise

Pemberitahuan masalah, perubahan obrolan, dan ringkasan harian melalui Apprise: aplikasi pesan instan, email, atau webhook JSON Anda sendiri.

**Tidak dilakukan**: Pesan teks tidak akan dikirim kecuali Anda mengaktifkan kutipan.

 [Konfigurasikan tujuan pemberitahuan](https://phishdestroy.github.io/TgWitness/id/docs/reference/operations/#notifications)

### Cap waktu eksternal

Lakukan hashing titik pemeriksaan waktu dengan RFC 3161 dan OpenTimestamps.

**Yang tidak dilakukan** Situs ini tidak menganggap tanda terima kalender yang masih tertunda sebagai cap waktu Bitcoin yang telah dikonfirmasi.

 [Periksa bukti cap waktu](https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/)

### Saksi independen

Host terpisah menyimpan pengamatan yang telah ditandatangani dan dapat menerbitkan `TGW1` titik pemeriksaan.

**Yang tidak dilakukan** Hal ini tidak menjadikan dua ruang kerja pada satu host pengumpul sebagai saksi yang independen.

 [Siapkan saksi](https://phishdestroy.github.io/TgWitness/id/docs/witness/)

### Pemulihan dan celah yang terlihat

Lanjutkan setelah restart. Melakukan pemeriksaan ulang dan `coverage.json` menampilkan pesan yang berhasil dipulihkan serta celah-celah yang ada.

**Yang tidak dilakukan** Alat ini tidak merekonstruksi setiap pengeditan yang terlewatkan atau pesan yang hilang.

 [Periksa kontinuitas dan celah](https://phishdestroy.github.io/TgWitness/id/guides/modes.html#continuity)

## Ruang kerja pertama Anda dimulai di sini.

Coba demo-nya terlebih dahulu. Hubungkan akun khusus Anda saat sudah siap. Windows, Linux, macOS, atau Docker.

[Baca panduan pengaturan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=id)

**Satu sesi yang diimpor, satu klien yang sedang berjalan.**

Jangan menjalankan kunci TData/sesi yang diimpor di Telegram Desktop dan TgWitness secara bersamaan. Telegram dapat membatalkan otorisasi bersama (AUTH_KEY_DUPLICATED). Untuk penggunaan paralel, buat login TgWitness terpisah melalui nomor telepon atau QR.

[Baca peringatan impor sesi](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=id#session-warning)

**Silakan lihat terlebih dahulu sebelum Anda terhubung.**

Cobalah ruang kerja fiktif ini tanpa akun Telegram.

[Buka demo online →](https://phishdestroy.github.io/TgWitness/demo/?lang=id)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Perintah instalasi lokal**

LANGKAH 01

### Unduh sumbernya.

[Unduh berkas ZIP sumber](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) dan ekstrak, atau kloning repositori:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Peluncuran sumber memerlukan Python 3.11+. Peluncur Windows menawarkan instalasi jika Python tidak terpasang.

[Telusuri rilis](https://github.com/phishdestroy/TgWitness/releases)

Tidak ada Python di Windows? [Unduh paket portabel](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip), ekstrak, lalu klik dua kali berkas `TgWitness.cmd`.

LANGKAH 02

### Pilih cara menjalankannya.

Klik dua kali `Start.cmd`, atau jalankan di PowerShell:

```
.\Start.cmd
```

Hanya ingin menjelajah? Klik dua kali `scripts\Demo.cmd` untuk demo terisolasi. Tidak perlu login ke Telegram.

Tersedia dengan Python 3.11+ dan `venv`:

```
sh start.sh
```

Untuk membuka jurnal fiktif tersebut, jalankan perintah `sh start.sh --demo`.

Dengan Docker yang sudah berjalan dan Compose 2.20+ yang sudah terinstal:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Perintah kedua menampilkan token panel pribadi Anda. Simpanlah di perangkat Anda.

Buka [127.0.0.1:8787](http://127.0.0.1:8787) setelah diluncurkan.

Untuk instalasi dari sumber, tokennya adalah `data/live/panel-token.txt`. Masuk ke Telegram dapat menggunakan pengaturan API bawaan atau pasangan kunci Anda sendiri dari [my.telegram.org](https://my.telegram.org). [Panduan pengaturan lengkap ↗](https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/)

**TgWitness 0.7.0** [Apa yang baru →](https://phishdestroy.github.io/TgWitness/id/docs/reference/changelog/) · [Fitur dan batasan yang diketahui →](https://phishdestroy.github.io/TgWitness/id/docs/reference/features/)

## Petunjuk yang jelas. Langkah selanjutnya yang bermanfaat.

[Jelajahi panduan ↗](https://phishdestroy.github.io/TgWitness/id/docs/)

[### Mode, skenario, dan tingkat bukti Empat mode pengumpulan. Delapan tingkat verifikasi. Temukan alur kerja yang sesuai untuk kasus Anda.](https://phishdestroy.github.io/TgWitness/id/guides/modes.html)

[01 ### Hubungkan akun Impor melalui telepon, QR, dan sesi yang didukung.](https://phishdestroy.github.io/TgWitness/id/docs/accounts/)[02 ### Pilih proxy Daftar MTProxy publik atau rute Anda sendiri.](https://phishdestroy.github.io/TgWitness/id/docs/proxies/)[03 ### Siapkan bot saksi Titik pemeriksaan yang ditandatangani di saluran Telegram Anda.](https://phishdestroy.github.io/TgWitness/id/docs/witness/)[04 ### Ekspor dan verifikasi Bagikan riwayat yang terekam dan periksa integritasnya.](https://phishdestroy.github.io/TgWitness/id/docs/exports/)

## Kelola arsip.

Memuat riwayat, meninjau sumber AI, menghubungkan klien MCP, mengenali media yang disimpan, dan mengirim webhook yang ditandatangani.

Tersedia dari sumber saat ini. Versi pratinjau portabel 0.7.0 dirilis sebelum alat-alat ini.

[Jelajahi alur kerja](https://phishdestroy.github.io/TgWitness/id/docs/archive/)

## Sebelum Anda memulai.

**Apakah halaman ini terhubung ke Telegram?**

Tidak. Ini adalah halaman proyek statis yang berisi contoh dan tangkapan layar fiktif. Aplikasi sebenarnya berjalan di komputer atau server Anda; proses masuk dilakukan di sana.

**Apakah alat ini dapat memulihkan pesan yang dihapus sebelum direkam?**

Tidak. TgWitness menyimpan konten yang terdeteksi oleh akun Anda selama proses pengumpulan data berlangsung. Cuplikan riwayat yang diambil kemudian tidak dapat merekonstruksi pengeditan yang terlewat atau pesan yang telah dihapus.

**Apakah seluruh jurnal saya dienkripsi?**

Kredensial akun dan rahasia penandatanganan disimpan dalam brankas terenkripsi. Pesan dan lampiran lokal memerlukan disk atau volume terenkripsi. Ekspor dapat secara opsional menggunakan ZIP AES-256 yang dilindungi kata sandi.

**Apakah ini berafiliasi dengan Telegram?**

Tidak. TgWitness adalah proyek independen yang menggunakan Telethon, yang didistribusikan di bawah Lisensi MIT. Anda mengotorisasi akun Anda sendiri, baik menggunakan pengaturan API bawaan maupun pasangan API Anda sendiri.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Jelajahi terlebih dahulu. Lakukan pengaturan saat sudah siap.

[Buka demo](https://phishdestroy.github.io/TgWitness/demo/?lang=id)[Panduan pengaturan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=id)
