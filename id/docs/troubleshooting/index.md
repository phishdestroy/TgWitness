# Temukan apa yang salah

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/troubleshooting/

Mulailah dari gejalanya. Periksa satu lapisan demi satu.

## Panel meminta token

Gunakan token panel dari berkas lokal yang ditampilkan oleh peluncur. Untuk Docker, jalankan perintah ``docker compose exec tgwitness cat /data/panel-token.txt``. Kode login Telegram, token BotFather, dan token saksi baca-saja memiliki fungsi yang berbeda-beda.

## Telegram tidak terhubung

Buka pengaturan koneksi dan jalankan pemeriksaan koneksi. Jika menggunakan proxy publik, coba entri lain dan simpan rute secara eksplisit. Periksa jenis proxy dan format rahasia yang didukung. Memperbarui daftar publik tidak akan mengubah rute akun.

## Terhubung, tetapi tidak ada pesan baru

1. Pastikan observasi berjalan di ruang kerja yang benar.
2. Pastikan sumber telah dipilih dan terlihat oleh akun tersebut.
3. Kirim pesan baru yang unik ke dalam grup yang dikendalikan, lalu cari teks persis seperti itu.
4. Periksa jurnal operasional untuk mengetahui adanya gangguan, keterlambatan pekerjaan, atau kesalahan Telegram.

Cuplikan historis dan peristiwa pesan baru adalah dua hal yang berbeda. Sumber yang tidak aktif dapat dihubungkan tanpa menghasilkan pesan baru. Gunakan uji pengiriman terkontrol jika kelengkapan data menjadi hal yang penting.

## FloodWait atau jeda setelah restart

FloodWait berarti Telegram memerlukan jeda. Tunggu selama periode yang ditentukan dan tinjau beban kerja pengumpulan data; koneksi ulang yang berulang tidak akan menghapus batasan tersebut. Status pembaruan yang disimpan membantu mengejar ketertinggalan setelah restart, namun pembaruan yang kedaluwarsa dan beberapa jendela gangguan tetap menjadi batasan. Catat selisih waktu tersebut daripada menganggap jurnal tersebut sudah lengkap.

## Bot ini telah dikonfigurasi tetapi tidak memposting apa pun

Pastikan proses TgWitness benar-benar berjalan, bot dapat memposting di saluran, dan TgWitness dapat terhubung ke kolektor serta Bot API. Periksa jurnalnya untuk mengetahui adanya publikasi yang gagal. Polling kolektor yang berhasil saja tidak menjamin adanya postingan di saluran.

## Di mana integrasi token GitHub?

**Sedang direncanakan.** Bagian "Extras" menjelaskan alur kerja verifikasi fork dan build yang diusulkan. Saat ini belum ada formulir token GitHub atau verifikasi otomatis yang memastikan bahwa instalasi yang berjalan sesuai dengan repositori. Lihat [status fitur saat ini](https://phishdestroy.github.io/TgWitness/id/docs/reference/features/).

Saat melaporkan masalah, sertakan versi, sistem operasi, langkah-langkah, dan pesan kesalahan yang telah disunting. Jangan sertakan sesi, token, pesan pribadi, dan direktori data dalam laporan masalah publik.
