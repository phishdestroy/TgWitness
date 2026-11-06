# Satu jurnal. Empat mode pengumpulan. Delapan tingkat verifikasi.

Canonical page: https://phishdestroy.github.io/TgWitness/id/guides/modes.html

Mode, skenario, dan tingkat bukti

TgWitness mencatat apa yang diamati oleh akun yang terhubung. Pihak ketiga dapat memverifikasi integritas catatan tersebut dengan membandingkannya terhadap kunci tepercaya yang independen.

[Mode pengumpulan](https://phishdestroy.github.io/TgWitness/id/guides/modes.html#scope)[Skenario](https://phishdestroy.github.io/TgWitness/id/guides/modes.html#scenarios)[Tingkat bukti](https://phishdestroy.github.io/TgWitness/id/guides/modes.html#levels)

Gambaran umum 3–5 menit · contoh fiktif · implementasi saat ini

1. **Telegram**

   Pembaruan yang terlihat di akun
2. **Pengumpul**

   Catatan yang tertaut, masing-masing ditandatangani
3. **Verifikator**

   Kunci tepercaya + batas yang dipertahankan

`h₁ → h₂ → h₃ · Ed25519`Integritas telah diverifikasi. Asal usul Telegram dan kebenaran suatu pesan tetap merupakan dua hal yang terpisah.

## Pilih ruang lingkup pengamatan

Tiga ruang lingkup dan pengaturan awal investigasi. Pengecualian dan jenis sumber yang diaktifkan tetap berlaku.

Default**Obrolan yang dipilih**

Catatan

Hanya sumber yang dipilih secara manual.

Obrolan baru

Tidak ditambahkan secara otomatis.

Pilih untuk

Kumpulan saluran atau grup yang diketahui. Belum ada kapasitas obrolan tetap yang ditetapkan.

**Yang tidak dilakukan** Aplikasi ini tidak mendeteksi obrolan lain atau mengisi riwayat sebelumnya.

Folder akun**Folder Telegram**

Catatan

Folder yang disertakan dan kategori, dikurangi pengecualian dan obrolan yang diarsipkan jika dikonfigurasi.

Obrolan baru

Pencocokan obrolan aktif; perubahan folder dalam waktu satu jam.

Pilih untuk

Seorang analis sudah mengelola folder kasus. Pastikan pengumpulan data dilakukan di akun khusus.

**Yang tidak dilakukan** Hal ini tidak berlaku untuk kondisi folder yang berubah-ubah muted/read kondisi folder tersebut.

Konfirmasi ruang lingkup**Akun lengkap**

Catatan

Obrolan yang terlihat oleh akun, termasuk percakapan pribadi dan bot, dalam jenis-jenis yang dipilih.

Obrolan baru

Ditambahkan saat pembaruan pertama tiba.

Pilih untuk

Akun pengamatan khusus, termasuk akun yang terlibat dalam suatu kasus.

**Yang tidak dilakukan** Aplikasi ini tidak bergabung ke obrolan secara otomatis atau melewati akses sumber.

Pengaturan awal seluruh akun**Mode investigasi**

Catatan

Semua jenis sumber, tindakan sendiri, profil sumber, dan 200 pesan terbaru yang terlihat dari sumber yang baru ditemukan.

Obrolan baru

Obrolan atau bot baru akan mendapatkan profil dan cuplikan riwayat.

Pilih untuk

Bergabunglah dengan tim atau berinteraksi dengan bot melalui panel. Tinjau dan simpan preset tersebut.

**Yang tidak dilakukan** TgWitness tidak mengambil snapshot setiap obrolan yang ada atau memantau callback yang ditekan di klien lain.

Kartu-kartu ini merupakan perbandingan lokal, bukan kontrol pengumpul data langsung. Kartu-kartu ini tidak mengubah akun.

**Yang tidak dilakukan** Tidak ada mode yang membaca obrolan rahasia, merekam saat proses dihentikan, bergabung dengan sumber secara otomatis, atau mengambil riwayat sebelumnya melebihi yang diminta snapshot/export.

[Baca detailnya](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/)

## Pengambilan melalui GitHub Actions (pratinjau)

Login Telegram baru, satu obrolan, arsip terenkripsi, dan bukti asal GitHub.

[Buka asisten pengambilan](https://phishdestroy.github.io/TgWitness/id/docs/capture/)

## Apa yang direkam

Hanya pengamatan yang telah dikirimkan atau diminta secara eksplisit yang dimasukkan ke dalam catatan. Asal usul yang tidak diketahui tetap tidak diketahui.

 Tangkapan tombol · ilustrasi lokalPesan baruPengeditanPenghapusanReaksiKeanggotaan

Panel ini menerapkan pengaturan ini per ruang kerja. Menonaktifkan salah satunya akan mempertahankan catatan yang ada; mengaktifkannya kembali tidak akan merekonstruksi peristiwa yang terlewat.

**Matriks peristiwa: materi yang disimpan dan hal-hal yang masih belum diketahui**

| Kategori | Tersimpan | Masih belum diketahui |
| --- | --- | --- |
| Pesan | Teks, ID, metadata pengirim, konteks balasan, dan amplop pembaruan asli. | Tidak ada tanda tangan Telegram yang dapat diverifikasi oleh pihak ketiga. |
| Edit | Setiap versi yang diamati, tanpa menimpa versi sebelumnya. | Pengeditan sementara mungkin terlewatkan; pengirim tidak selalu sama dengan editor. |
| Penghapusan | Pemberitahuan ditambah teks yang disimpan sebelumnya, jika tersedia. | Penghapus dan waktu tindakan yang tepat tidak disediakan. |
| Penghapusan tanpa cakupan | Pemberitahuan tingkat akun; rekan yang tidak dikenal tetap dinyatakan secara eksplisit. | Tidak ada tebakan obrolan. Korelasi menggunakan ID yang disimpan sebelumnya dalam lingkup akun jika memungkinkan. |
| Reaksi | Penghitung yang dikirimkan dan identitas terbaru yang terlihat. | Tidak semua reaktor terlihat; daftar lengkap yang tersedia memerlukan kueri terpisah. |
| Keanggotaan | Pesan layanan yang telah dikirimkan dan pembaruan peserta. | Peran dan jenis obrolan membatasi visibilitas; keheningan tidak menunjukkan ketidakhadiran. |
| Lampiran | Deskriptor versi asli, byte yang disimpan, SHA-256 dan hasil upaya. | File yang hilang mungkin tidak tersedia; versi yang lebih baru tidak menggantikannya. |
| Cuplikan riwayat | Pesan yang saat ini terlihat, ditandai sebagai pengamatan riwayat. | Pengeditan sebelumnya dan konten yang hilang tidak direkonstruksi. |
| Tindakan sendiri | Keluar messages/edits dan metadata keyboard balasan yang sesuai button_press metadata. | Callback yang ditekan di klien Telegram lain tidak terlihat. |
| Tombol bot | Metadata callback, URL, aplikasi web, dan permintaan disimpan bersama pesan. | URL dan phone/location permintaan adalah teks, tidak dibuka atau dijalankan secara otomatis. |

### Batas lampiran default

Foto

20 MiB

Video

100 MiB

Berkas

50 MiB

Animasi

20 MiB

Catatan video

50 MiB

Suara

20 MiB

Audio

50 MiB

Stiker

5 MiB

**Yang tidak dilakukan** Sebuah sakelar tidak menyunting metadata yang tertanam atau menonaktifkan catatan operasional. Penangkapan tidak mengidentifikasi pelaku yang tidak disediakan oleh Telegram.

[Baca detailnya](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/)

## Gunakan otorisasi yang Anda miliki

Setiap akun memiliki ruang kerja, jurnal, kunci penandatanganan, rute, dan antrian masing-masing.

### Nomor telepon + kode

Masukkan 2FA jika diaktifkan.

### QR kode

Lakukan pemindaian dari perangkat yang berwenang; 2FA mungkin masih diperlukan.

### Telethon .session

Impor berkas sesi akun tersebut.

### Pyrogram .session

Impor Pyrogram yang didukung.

### TData ZIP

Satu akun Desktop yang didukung; kode sandi lokal jika telah ditetapkan.

### StringSession teks

Tempelkan sebuah Telethon StringSession.

### .session + .json

Pilih sesi dan metadata pendamping yang sesuai.

### Kunci otentikasi HEX + DC ID

Impor otorisasi akun beserta pengenal pusat datanya.

**API pasangan**

Pasangan API pasangan Anda bersifat opsional. Tanpa pasangan tersebut, TgWitness sistem akan menggunakan kumpulan pasangan publik, termasuk pasangan dari Telegram Desktop resmi.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy masih dalam tahap percobaan; daftar publik bawaan MTProxy tersedia. Rute proxy yang gagal tidak akan beralih ke koneksi langsung.

Dua ruang kerja pada satu mesin bukanlah dua saksi yang independen.

**Yang tidak dilakukan** Impor tidak melewati otorisasi Telegram, 2FA atau format sesi yang tidak didukung. Akun-akun tersebut tetap berbagi proses aplikasi.

[Format akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/)

## Bertindak dari panel

Kirim atau balas, tekan tombol bot yang tersedia, simpan pratinjau tautan, lalu secara eksplisit bergabung ke obrolan atau jalankan bot dengan parameter start-nya.

`interaction.preview``interaction.requested``interaction.result`

Tanda terima pratinjau, permintaan, dan hasil ditandatangani. Sebelum tombol ditekan, server mengambil pesan tersebut kembali dan menolak perubahan yang dilakukan melalui keyboard. Teks dan URL callback yang dikembalikan tetap menjadi konteks yang tercatat.

**Yang tidak dilakukan** Tidak ada aplikasi web, pembayaran, phone/location berbagi, atau kueri sebaris. Menampilkan URL tidak akan membukanya.

[Baca detailnya](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/)

## Pemulihan dan kelangsungan

Kesenjangan ditampilkan, bukan disembunyikan.

### Lanjutkan dari posisi yang disimpan

Setelah restart, Telegram akan diminta untuk memperbarui pembaruan yang terlewat. Retensi terbatas dan perbedaan yang telah kedaluwarsa dapat meninggalkan celah.

### Periksa kembali pesan yang terlihat

Pengaturan default: sumber prioritas setiap 15 menit, yang lain setiap 6 jam. Hasilnya meliputi message.recovered dan message.missing_on_recheck.

### Baca coverage.json

Periode pengamatan, celah dengan alasan, dan ID yang tidak teramati menyertai ekspor yang ditandatangani. Catatan "hilang saat diperiksa ulang" bukanlah pemberitahuan penghapusan.

**Yang tidak dilakukan** Cuplikan riwayat yang diambil kemudian tidak menghapus gangguan layanan atau memulihkan setiap versi yang hilang. Penanda kursor yang disimpan bukanlah pengakuan tanpa kehilangan data atas penerimaan jurnal.

[Baca detailnya](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/)

## Tujuh tingkatan. Pertanyaan yang berbeda.

Setiap mekanisme menjawab pertanyaan yang terbatas. Konfigurasikan layanan eksternal secara terpisah dan pertahankan jangkar kepercayaannya di luar pengumpul.

1. ### Catat

   SHA-256 rantai + Ed25519 per peristiwa; yang pertama previous_hash adalah 64 angka nol.

   **Pemeriksaan pihak ketiga** Urutan dan tanda tangan di bawah kunci pengumpul yang disematkan.

   **Yang tidak dilakukan** Hal ini tidak membuktikan asal-usul atau kelengkapan Telegram.

   **Perintah verifikasi**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Kontainer

   manifest.json mencantumkan hash file; manifest.sig menandatanganinya. media.saved mengaitkan byte lampiran ke suatu peristiwa.

   **Pemeriksaan pihak ketiga** Berkas-berkas yang disediakan sesuai dengan manifest yang ditandatangani dan tanda terima media.

   **Yang tidak dilakukan** Ini tidak menandatangani CSV, HTML atau tangkapan layar.

   **Perintah verifikasi**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Batas yang dipertahankan

   Titik pemeriksaan saat startup, setiap 5 menit secara default, dan penghentian yang teratur. Simpan salinan di tempat lain.

   **Pemeriksaan pihak ketiga** Ekspor selanjutnya sesuai dengan panjang dan header yang disimpan sebelumnya; rollback dapat dideteksi.

   **Yang tidak dilakukan** Sistem ini tidak mendeteksi penggantian baik jurnal maupun semua titik pemeriksaan yang disimpan.

   **Perintah verifikasi**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Waktu eksternal

   Mode bukti mengirimkan titik pemeriksaan SHA-256 kepada RFC 3161 otoritas (FreeTSA, DigiCert) dan OpenTimestamps kalender.

   **Pemeriksaan pihak ketiga** Respons TSA yang terverifikasi mencatat tanggal byte-byte tersebut; sebuah OpenTimestamps membuatnya terikat pada Bitcoin.

   **Yang tidak dilakukan** Permintaan yang telah disiapkan atau tanda terima kalender yang tertunda tidak diperlakukan sebagai cap waktu yang telah dikonfirmasi.

   **Perintah verifikasi**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Saksi independen

   Pisahkan host, titik akhir baca-saja yang terbatas, tantangan baru, dan key/journal dan TGW1 posting saluran.

   **Pemeriksaan pihak ketiga** Heads yang diterima sebelumnya; status ok, key_changed, rollback, fork, tidak valid, dan no_response.

   **Yang tidak dilakukan** Hal ini tidak mengubah dua ruang kerja pada satu host pengumpul menjadi saksi yang independen.

   **Perintah verifikasi**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Replika di luar situs

   S3-salinan yang kompatibel yang dienkripsi dengan AES-256-GCM; Object Lock jika bucket mendukungnya.

   **Pemeriksaan pihak ketiga** Restore hanya mempublikasikan berkas setelah verifikasi jurnal, titik pemeriksaan, dan media yang disimpan berhasil.

   **Yang tidak dilakukan** Fitur ini tidak akan memulihkan data tanpa kunci yang diekspor atau mengasumsikan penyimpanan tanpa memeriksa respons penyimpanan.

   **Perintah verifikasi**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Jalankan provenance

   Tanda terima eksekusi yang ditandatangani: hash sumber, versi dependensi, dan konteks proses. Dilaporkan sendiri.

   **Pemeriksaan pihak ketiga** Apa yang dilaporkan oleh pengumpul tanda tangan mengenai eksekusinya sendiri.

   **Yang tidak dilakukan** Dokumen ini tidak menyediakan pembuktian proses independen atau mengecualikan kemungkinan terjadinya pelanggaran keamanan sebelum perekaman.

   **Perintah verifikasi**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Apa yang tidak dibuktikan oleh tingkat mana pun

Penyampaian setiap pembaruan Telegram; kebenaran teks; bahwa ID pengirim mengidentifikasi orang sungguhan; tidak adanya pelanggaran keamanan pengumpul sebelum perekaman; kelayakan sebagai bukti di pengadilan.

[Saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/)

Eksperimen SHA-256 eksperimen

### Coba ubah catatan 2

Catatan berikutnya mempertahankan tautan yang disimpan sebelumnya. Mengubah teks akan mengubah hash yang dihitung dari catatan ke-2.

Teks catatan 2

Catatan 1`h1`Dimulai dengan 64 angka nol

Catatan 2`h2`Termasuk yang disimpan h1

Catatan 3`h3`Termasuk yang disimpan h2

Contoh statis: h2 mencakup “Bertemu pukul 11:00”. Mengubah teks tersebut akan mengubah h2; catatan 3 masih merujuk pada yang tersimpan h2.

**Periksa ringkasan lengkap**

Hash catatan tersimpan 2

`SHA-256(e₂)`

Hash catatan 2 yang dihitung ulang

`SHA-256(e₂)`

Contoh ini menghitung hash, bukan tanda tangan. Verifikator yang sebenarnya memeriksa setiap tanda tangan dan tautan terhadap kunci tepercaya.

 [Baca detailnya](https://phishdestroy.github.io/TgWitness/id/docs/reference/how-it-works/)

## Pilih jalur melalui bukti

Situasi fiktif. Mulailah pengumpulan sebelum peristiwa yang relevan; pertahankan batas-batas dan celah-celah tersebut bersamaan dengan isinya.

### Sebuah saluran mengubah detail pembayaran

Mode → peristiwa

Obrolan yang dipilih → pesan, pengeditan, penghapusan.

Output

Versi postingan dan lampiran yang diamati berdasarkan hash.

Verifikasi

Tertanda ZIP + titik pemeriksaan yang disimpan + respons TSA yang terverifikasi.

**Yang tidak dilakukan** Ini tidak memulihkan data asli yang tidak pernah direkam.

### Pesan akan hilang setelah terjadi insiden

Mode → peristiwa

Folder atau seluruh akun → semua kategori peristiwa.

Output

Asli yang disimpan, pemberitahuan penghapusan, dan cakupan dengan celah.

Verifikasi

Ditandatangani ZIP + jurnal saksi independen.

**Yang tidak dilakukan** Hal ini tidak mengidentifikasi pihak yang menghapus dari pemberitahuan yang tidak mencantumkan pelaku.

### Selidiki bot toko

Mode → peristiwa

Pengaturan awal investigasi → tombol, pratinjau tautan, dan memulai bot secara eksplisit.

Output

Tanda terima interaksi yang ditandatangani, callback yang dikembalikan, dan profil yang disimpan.

Verifikasi

Tertanda ZIP; verifikasi setiap berkas terhadap ZIP.

**Yang tidak dilakukan** Aplikasi ini tidak membuka aplikasi web bot, melakukan pembayaran, atau merekam callback klien lain.

### Seorang peserta dapat mengganti nama di berbagai obrolan

Mode → peristiwa

Setiap ruang lingkup → metadata yang diamati sender/profile metadata.

Output

Riwayat nama/nama pengguna berdasarkan ID numerik, tautan “juga di”, dan petunjuk yang diekstraksi.

Verifikasi

Dokumen JSON telah diverifikasi terhadap yang ditandatangani ZIP.

**Yang tidak dilakukan** Hal ini tidak mengubah dompet, string mirip nomor telepon, atau nama pengguna menjadi identitas yang terverifikasi.

### Pengamatan jangka panjang dengan salinan di luar lokasi

Mode → peristiwa

Ruang lingkup apa pun → Mode bukti dan sebuah S3 replika dengan dukungan Object Lock.

Output

Salinan terenkripsi, titik pemeriksaan yang disimpan, dan respons cap waktu.

Verifikasi

Pulihkan menggunakan kunci yang diekspor, lalu verifikasi tanpa server asli.

**Yang tidak dilakukan** Ini tidak menggantikan saksi independen atau kunci dekripsi yang disimpan secara terpisah.

[Baca detailnya](https://phishdestroy.github.io/TgWitness/id/docs/reference/investigation/)

## Serahkan paket yang dapat diverifikasi

Sertakan dokumen asli yang telah ditandatangani, sidik jari kunci yang disimpan secara independen, titik pemeriksaan yang relevan, dan hasil verifikasi.

- Tertanda ZIP
- JSONL
- CSV
- HTML
- Titik pemeriksaan
- Tanda terima eksekusi
- Ekspor obrolan: chat.json / chat.html
- Dokumen JSON
- Dilindungi kata sandi AES-256 ZIP
- Ekspor terpisah untuk beberapa akun
- CLI Streaming: 5 GiB batas default

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Peroleh verifikator dari salinan tepercaya, bukan dari arsip yang sedang diperiksa.

**Yang tidak dilakukan** Mandiri CSV dan HTML bukanlah wadah yang ditandatangani. Kata sandi melindungi kerahasiaan transfer, bukan keasliannya. Ekspor ganda tidak menggabungkan jurnal akun.

[Baca detailnya](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/)

## Bandingkan artefak yang diserahkan

Artefak dasar tanpa penandatanganan tambahan, cap waktu, atau sistem saksi. Skrip dan pencatat log bervariasi sesuai implementasi; “sebagian” berarti terbatas pada materi yang terekam atau terlihat.

| Pendekatan | Pengeditan / penghapusan | Catat tanda tangan | Waktu eksternal | Saksi independen | Cakupan / celah | Verifikasi tanpa penulis |
| --- | --- | --- | --- | --- | --- | --- |
| Ekspor Telegram Desktop | Sebagian | Tidak | Tidak | Tidak | Tidak | Tidak |
| Telethon skrip snapshot | Sebagian | Tidak | Tidak | Tidak | Tidak | Tidak |
| Pencatat penghapusan: log teks | Sebagian | Tidak | Tidak | Tidak | Tidak | Tidak |
| Tangkapan layar / tangkapan web | Sebagian | Tidak | Tidak | Tidak | Tidak | Tidak |
| TgWitness dengan ekstra yang telah dikonfigurasi | Sebagian | Ya | Ya | Ya | Sebagian | Ya |

**Yang tidak dilakukan** Tabel ini tidak mengevaluasi setiap skrip atau produk pencatatan. Pemeriksaan waktu dan saksi yang bersifat opsional memerlukan layanan dan jangkar kepercayaan tersendiri; tidak ada yang menetapkan kebenaran sumber.

[Baca detailnya](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/)

## Pertahankan batasan-batasan tersebut bersama dengan bukti-buktinya

Verifikasi berguna jika ruang lingkupnya tetap eksplisit.

- Obrolan rahasia tidak tersedia.
- Tidak ada yang direkam saat proses dihentikan; pemulihan memiliki batasan.
- Catatan yang terverifikasi bukanlah bukti bahwa isinya benar.
- Seorang operator yang memiliki kunci dapat menandatangani konten apa pun. Saksi independen dan cap waktu membatasi penggantian di kemudian hari, bukan pencatatan awal yang tidak jujur.
- Gunakan akun khusus, bukan akun utama Anda.
- Telegram dapat membatasi akun berdasarkan volume permintaan.

**Yang tidak dilakukan** Tidak ada mode atau tingkat bukti yang menetapkan kelayakan hukum, pengiriman Telegram yang lengkap, atau identitas di dunia nyata.

[Panduan pengaturan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=id)[Akun khusus](https://phishdestroy.github.io/TgWitness/id/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/investigation/)
