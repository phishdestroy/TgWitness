# Telegram · Penyimpanan dan pemulihan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/storage/

Pencadangan, pemindahan berkas lama ke cloud Anda, salinan di bawah Object Lock, dan pemulihan di perangkat baru.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Penerapan dan pemulihan](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/)

![Penerapan & pemulihan](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Panel ini membagi tiga tugas:

| Tugas | Fungsinya |
| --- | --- |
| Simpan salinan cadangan | Salin jurnal yang telah ditandatangani, titik pemeriksaan, berkas yang disimpan, dan ekspor yang sedang dalam antrian ke tujuan S3 yang telah dikonfigurasi. |
| Ruang lokal gratis | Salin lampiran lama yang dipilih ke S3 atau penyimpanan awan rclone, baca kembali secara utuh, verifikasi byte terenkripsi, lalu hapus salinan lokal yang telah diverifikasi. |
| Simpan salinan bukti | Konfigurasikan S3 Object Lock dan periksa status retensi yang dikembalikan. Layanan harus mengonfirmasi mode dan tanggal yang diminta. |

Pembebasan ruang penyimpanan tidak pernah menghapus atau menimpa jurnal yang telah ditandatangani. Setiap lampiran menyimpan SHA-256 aslinya dan tanda terima pemulihan. Kompresi gzip opsional dilakukan sebelum enkripsi terotentikasi. Nama file di cloud tidak mengandung nama Telegram, ID obrolan, atau nama lampiran asli. Satu lampiran dapat berukuran hingga 32 GiB.

Respons unggahan saja tidak berarti izin untuk menghapus file. TgWitness mengunduh objek terenkripsi secara lengkap dan memverifikasi ukurannya serta SHA-256, menyimpan tanda terima, lalu memeriksa byte lokal lagi segera sebelum penghapusan. Kegagalan unggahan, hasil pembacaan yang berbeda, atau transfer yang dibatalkan membuat file lokal tetap ada. Jika cadangan bukti yang diaktifkan belum menyalin file tersebut, penghapusan juga akan menunggunya.

**Di halaman ini**

- [Saat ruang penyimpanan hampir penuh](https://phishdestroy.github.io/TgWitness/id/docs/reference/storage/#when-the-disk-is-filling-up)
- [Hubungkan tujuan](https://phishdestroy.github.io/TgWitness/id/docs/reference/storage/#connect-a-destination)
- [Simpan berkas pemulihan](https://phishdestroy.github.io/TgWitness/id/docs/reference/storage/#keep-the-recovery-file)
- [Pemulihan setelah kehilangan instalasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/storage/#recover-after-losing-the-installation)
- [Bot operator dan pemberitahuan penyelesaian](https://phishdestroy.github.io/TgWitness/id/docs/reference/storage/#operator-bot-and-completion-notices)

## Saat disk mulai penuh

Unduhan lampiran dijeda ketika ruang kosong di bawah nilai **Parameter → Lampiran → ruang disk kosong** (default 1 GiB), dengan antrean tetap tersimpan. Pengamatan teks berlanjut. Ini tidak bergantung pada notifikasi: mematikannya tidak menonaktifkan cadangan unduhan atau perlindungan penyimpanan.

Untuk bertindak lebih awal, aktifkan **Jalankan otomatis**, pilih **Hapus file lokal untuk mengosongkan ruang**, dan aktifkan **Mulai pemindahan tambahan saat ruang disk rendah**. Secara default, aturan opsional dimulai di bawah 5120 MiB kosong dan memproses kelompok file hingga tersedia 10240 MiB. Kedua ambang dapat diatur. Tujuan, usia minimum file, batas kelompok, verifikasi dengan pembacaan balik lengkap, dan prasyarat cadangan bukti sama seperti proses manual. Aturan tidak mengaktifkan tujuan sendiri. Pemeriksaan berjalan setiap 30 detik; kesalahan atau tidak adanya kemajuan menunda percobaan berikutnya lima menit. Status dan waktu percobaan ulang bertahan setelah mulai ulang. Saat aturan tidak aktif, proses terjadwal tetap memakai interval normal.

Panel menampilkan ruang kosong, cadangan pengemasan, kesiapan aturan, dan file yang dilewati karena ruang sementara tidak cukup. Pengemasan dan pemulihan memeriksa kebutuhan ruang sementara maksimum sebelum dimulai serta ruang tersedia selama penulisan. Cadangan mengikuti pengaturan unduhan, minimal 64 MiB untuk operasi penyimpanan. Pemeriksaan ini bukan kuota sistem file; proses lain masih dapat memakai ruang di antara pemeriksaan.

Gzip memampatkan objek jarak jauh tanpa kehilangan data; tidak mengecilkan jurnal aktif atau membuat arsip lokal. JPEG, video, dan ZIP mungkin hampir tidak mengecil atau sedikit membesar. Dengan kompresi, pengemasan dapat sementara membutuhkan sekitar dua kali ukuran lampiran ditambah cadangan. Pilih ambang mulai cukup awal untuk file terbesar. File yang terlalu besar tetap disimpan dan dilaporkan; file kecil dan salinan jarak jauh yang sudah diverifikasi masih dapat membebaskan ruang. Salinan terverifikasi memungkinkan penghapusan file lokal tanpa file pengemasan baru. Pemulihan juga memerlukan ruang sementara dan dapat ditolak sampai ruang tersedia.

Jika tidak ada file yang memenuhi syarat untuk dipindahkan atau tujuan belum diatur, TgWitness tidak dapat membebaskan ruang otomatis. Pengelolaan penyimpanan tidak pernah memangkas atau menulis ulang jurnal bertanda tangan. Ruang tetap diperlukan untuk pengamatan teks baru.

## Hubungkan tujuan

Di **Ekstra → Penyimpanan & ruang disk → Kelola penyimpanan**, pilih tugas dan tujuan, simpan, lalu pilih **Uji unggah & unduh**. Uji ini mengunggah probe acak berukuran kecil dan membacanya kembali. Uji ini tidak menggunakan konten Telegram.

Untuk S3, gunakan titik akhir (endpoint), wilayah, dan bucket yang sebenarnya dari penyedia layanan. Wasabi, Backblaze, Cloudflare R2, dan layanan lain yang kompatibel menggunakan pengaturan S3 yang sama. API yang kompatibel saja tidak menjamin dukungan untuk Object Lock. Mode Governance mungkin memungkinkan administrator yang berwenang untuk melewati masa retensi; Mode Compliance memiliki batasan yang berbeda. Bacalah status Object Lock yang dikembalikan sebelum mengandalkan masa retensi.

Untuk tujuan rclone, buat satu remote menggunakan pengaturan penyedia rclone dan tempelkan bagian `[name]` ke dalam panel. Pembantu yang terpasang mendukung MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud, dan penyedia lain yang ditampilkan di pemilih. Kredensial disimpan di brankas terenkripsi ruang kerja ini. Pembaruan OAuth disimpan kembali ke dalam brankas. Kredensial tidak ditambahkan ke peristiwa jurnal atau disertakan dalam unduhan pemulihan.

Alat bantu ini diinstal di dalam ruang kerja, dengan versi yang disematkan dan SHA-256. Alat bantu ini tidak ditambahkan ke PATH sistem. Berkas konfigurasi dan berkas kerja merupakan berkas sementara di dalam ruang kerja tersebut. Koneksi jarak jauh berbasis perintah dan berkas lokal ditolak. Saat ini, rclone memerlukan rute **Direct** yang dipilih secara eksplisit untuk permintaan eksternal. Gunakan penyimpanan S3 asli untuk rute SOCKS5 atau HTTP ruang kerja; rclone tidak akan secara diam-diam melewati rute yang tidak tersedia.

## Simpan berkas pemulihan

Pilih **"Simpan berkas pemulihan"** setelah menyalin berkas dan simpan di tempat yang terpisah dari instalasi. Berkas tersebut berisi kunci dekripsi dan tanda terima objek yang telah ditandatangani, jadi perlakukanlah sebagai cadangan kunci pribadi. Simpan juga konfigurasi jarak jauh asli dan kredensial tujuan secara terpisah. Berkas pemulihan yang diambil sebelum penyalinan berikutnya tidak berisi tanda terima dari berkas tersebut.

Jejak jari kunci penandatanganan seharusnya sudah dicatat secara terpisah. Tanda tangan yang hanya diverifikasi berdasarkan kunci yang disertakan dalam berkas yang sama tidak dapat memastikan milik siapa berkas pemulihan tersebut.

Untuk memulihkan tanda terima penyimpanan yang hilang di ruang kerja yang sudah ada, buka **"Pulihkan berkas" dari berkas pemulihan yang telah disimpan**, lalu pilih berkas tersebut. Panel ini akan memeriksa tanda tangan dan memerlukan kunci penandatanganan ruang kerja yang sama. Sistem akan menolak mengganti kunci penyimpanan yang berbeda. Selanjutnya, pilih **"Pulihkan semua berkas**". Proses pemulihan akan menunda aturan penyimpanan otomatis sehingga proses terjadwal berikutnya tidak dapat langsung menghapus berkas yang telah dipulihkan kembali. Aktifkan kembali aturan tersebut setelah selesai menggunakan salinan lokal.

Pemulihan memverifikasi teks terenkripsi, mengautentikasi dekripsi, mendekompresi jika diperlukan, dan memeriksa teks biasa asli SHA-256 sebelum menempatkan file di `media/`. Objek jarak jauh yang rusak tidak akan pernah menggantikan file lokal. File lokal yang sudah ada dengan byte yang berbeda akan disimpan untuk ditinjau, bukan ditimpa.

## Pemulihan setelah kehilangan instalasi

Instal TgWitness di mesin lain. Gunakan berkas pemulihan pribadi, sidik jari yang direkam secara terpisah, serta kredensial tujuan asli:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

Untuk S3, `--credentials` menunjuk ke berkas JSON pribadi dengan `access_key` dan `secret_key`; berkas pemulihan yang ditandatangani menyediakan pengaturan tujuan. Perintah ini menggunakan koneksi eksternal langsung dan mengunduh helper yang disematkan ketika remote rclone membutuhkannya. Perintah ini menolak direktori keluaran yang sudah ada.

Byte asli yang dipulihkan ditulis ke `recovered-attachments/media/`, yang dinamai berdasarkan SHA-256 masing-masing. `recovery-log.jsonl` adalah catatan operasi pemulihan yang tidak ditandatangani. Perintah ini tidak membuat ulang jurnal yang hilang dan telah ditandatangani maupun kunci penandatanganannya. Simpan cadangan ruang kerja lengkap untuk hal-hal tersebut. File pemulihan penyimpanan bukanlah cadangan ruang kerja lengkap.

## Bot operator dan pemberitahuan penyelesaian

Bot Telegram ini milik operator. Buatlah melalui BotFather dan atur token, obrolan tujuan, serta ID pengguna Telegram yang secara eksplisit diizinkan di panel. Baik pengirim maupun obrolan harus cocok. Pesan yang diteruskan dan perintah dari bot lain akan diabaikan.

`/status` dan `/stats` tersedia dalam mode default yang hanya menampilkan status. Mode kontrol opsional menambahkan `/pause`, `/resume` dan `/copy`. `/copy` meminta tugas penyimpanan yang telah dikonfigurasi; hal ini tidak berarti bahwa unggahan jarak jauh telah selesai. Perintah tidak dapat menyediakan URL, file, atau program shell sembarangan.

Gunakan pengaturan notifikasi terpisah untuk peringatan dan penyelesaian tugas. Pemberitahuan penyelesaian membedakan ekspor akun yang tidak lengkap dari ekspor yang lengkap, serta menampilkan riwayat dan jumlah penyimpanan. Kutipan pesan tidak disertakan kecuali diaktifkan secara terpisah dalam pengaturan notifikasi. Pemilih layanan dihasilkan dari katalog Apprise yang sebenarnya terpasang, bukan dari kumpulan contoh penyedia yang tetap.
