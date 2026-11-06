# Telegram · Pengaturan awal dan konfigurasi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/settings/

Wizard pengaturan, tujuan, tingkat antarmuka, rute koneksi, dan pengaturan yang dibagikan oleh sebuah grup akun.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Memulai](https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/)

![Memulai](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/) · [Koneksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) · [Akses](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/)

Ruang kerja baru terbuka `/first-run`: bahasa dan waktu, tingkat antarmuka, tujuan, koneksi, Telegram, dan obrolan. Setiap jawaban disimpan di server segera setelah berubah, sehingga memuat ulang halaman akan melanjutkan langkah yang sama. Layar terakhir mencantumkan jawaban-jawaban tersebut dan memungkinkan Anda kembali ke jawaban mana pun.

Bahasa, zona waktu IANA, tema, dan tingkat disimpan per operator dan per ruang kerja. Pengaturan defaultnya adalah bahasa browser, zona waktu perangkat, tema sistem, dan antarmuka sederhana. Mengubah bahasa tidak akan memengaruhi sesi panel. Waktu dalam jurnal yang ditandatangani tidak akan pernah berubah.

`/settings` mengedit catatan yang sama seperti yang dilakukan oleh wizard. Pencarian mencakup bidang utama, parameter, dan formulir tambahan; bidang tersembunyi dapat dibuka tanpa mengubah tingkat akses. Tingkat akses hanya mengubah apa yang ditampilkan: server memeriksa izin secara otomatis. Pengaturan koleksi dan koneksi pertama menjadi tanggung jawab administrator ruang kerja.

| Tingkat | Bidang | Sidebar |
| --- | --- | --- |
| Sederhana | Hanya hal-hal yang penting | Beranda, Obrolan, Perubahan, Arsip, Pengaturan |
| Standar | Pengaturan umum beserta penjelasannya | Menambahkan Case Board, Akun, dan Akses |
| Ahli | Semua bidang, batasan, dan detail teknis | Menambahkan Sumber, Ekstra, Tanya Arsip, Parameter, Akun, Log Sistem, dan Integrasi |

[Panduan panel](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/) ini menjelaskan setiap bagian.

## Tujuan

| Tujuan | Koleksi | Berkas | Layanan eksternal | Alamat server |
| --- | --- | --- | --- | --- |
| Salinan arsip | Mati; **Mulai** menjalankan ekspor | Foto berukuran hingga 20 MB | Mati | Otomatis |
| Ikuti obrolan | Berkelanjutan | Foto dan video berdurasi hingga 60 detik / 20 MB | Cap waktu dan pemberitahuan masalah | Otomatis |
| Bukti | Berkelanjutan | Semua berkas berukuran hingga 1 GB | Cap waktu, drand, notifikasi | Tidak, sembunyikan |

Salinan di luar platform, bot saksi, dan pemeriksaan kode direkomendasikan sebagai bukti. Alamat penyimpanan dan pemberitahuan memerlukan tujuan terlebih dahulu. Fitur yang terhubung ke layanan eksternal meminta izin untuk mengirim permintaan di luar Telegram; menonaktifkan fitur tersebut juga akan menonaktifkan cap waktu, pemberitahuan, dan salinan di luar platform secara bersamaan.

Mengubah target akan menampilkan perbedaannya terlebih dahulu, dan perubahan manual dapat dipertahankan. Bidang yang berbeda dari target akan ditandai **sebagai “Diubah oleh Anda”** dan dapat dikembalikan. Revisi pengaturan mencegah perbedaan yang telah ditinjau diterapkan di atas perubahan yang dibuat di tab lain.

## Koneksi

**Automatic** mencoba server publik MTProxy terlebih dahulu, kemudian WARP, lalu koneksi langsung, yang terakhir hanya jika alamat server dapat ditampilkan. Automatic dan WARP dapat menginstal komponen yang telah diverifikasi hash-nya dan mendaftarkan server ke Cloudflare. WARP menggunakan manajer wgcf/wireproxy yang sudah ada dan port SOCKS5 lokal; tabel perutean sistem tidak diubah. Ketika layanan eksternal diperlukan, Automatic lebih memilih WARP daripada MTProxy.

Proksi Anda sendiri menerima `tg://proxy`, `socks5://`, `http://` dan `https://`. Sertifikat proksi HTTPS diperiksa sebelum kredensial dikirim ke proksi tersebut.

Pemeriksaan koneksi berlaku selama lima menit dan terikat pada rute, kebijakan, dan jawaban wizard; mengubah salah satu dari ketiganya memerlukan pemeriksaan baru. Opsi **“Lanjutkan tanpa pemeriksaan”** tersedia dan tidak menggantikan proses masuk ke Telegram. Rute yang dipilih akan diperiksa ulang di latar belakang, dan fitur “Otomatis” akan menjalankan rantai prosesnya kembali setelah koneksi terputus. Jika tidak ada proxy publik yang merespons, hitungan akan berubah menjadi merah disertai tindakan WARP dan pemeriksaan ulang.

## Grup akun

Akun-akun dalam sebuah grup berbagi pengaturannya. Buka **Akun → Grup dan pengaturan bersama → Pengaturan bersama**, atau **Pengaturan grup** di halaman Pengaturan akun.

Grup ini berbagi tujuan, berkas yang disimpan, cap waktu, drand, pemberitahuan masalah, salinan di luar situs, permintaan di luar Telegram, mode IP, apa yang akan direkam, jadwal pemeriksaan ulang, aturan pemberitahuan, pengaturan laporan, parameter, dan rute koneksi. Tujuan pemberitahuan, kredensial proxy, dan proses masuk tetap per akun, begitu pula pengaktifan dan penundaan pengumpulan data.

- Setiap anggota mengikuti grup tersebut. Pengaturan menandai nilai 🔗 **Dari grup** atau ✏️ **Nilai sendiri**; **Kembali ke nilai grup** akan mengembalikannya ke nilai semula.
- Sebuah perubahan mencantumkan akun-akun yang terpengaruh (**Berlaku untuk 2 dari 3 akun**) dan meminta konfirmasi per akun sebelum mengganti nilai aslinya. Akun yang tidak dicentang akan mempertahankan nilainya.
- Parameter yang tidak dibagikan oleh grup akan tetap berstatus **“Tidak dibagikan”: setiap akun mempertahankan nilainya sendiri** hingga Anda menekan **“Bagikan nilai ini**”.
- **Menyalin pengaturan dari satu akun** akan menjadikan nilai-nilai dari akun yang dipilih sebagai pengaturan grup.
- Akun yang dipindahkan ke dalam grup akan ditanya**, “Apakah ingin menggunakan nilai-nilai grup ini?”** Jika tidak, akun tersebut akan tetap menggunakan nilai-nilainya sendiri, yang ditandai dengan ✏️. Akun yang ditambahkan kemudian akan mulai menggunakan nilai-nilai grup tersebut.
- Sebuah akun pengamat mempertahankan mode IP-nya hingga dihentikan sementara.

Setiap perubahan dicatat dalam jurnal yang ditandatangani di ruang kerja utama dan di setiap anggota yang terlibat. Menghapus sebuah grup tidak akan menghapus akun-akun di dalamnya beserta nilai-nilai terkini mereka.

Halaman grup `/groups/<id>` menampilkan anggota, hal-hal yang perlu diperhatikan, dan obrolan yang dapat dilihat oleh beberapa akun. Lihat [grup akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#bulk-import-and-account-groups).

## Ruang kerja yang ada

Ruang kerja yang sudah memiliki sesi atau pengaturan yang telah diselesaikan sebelumnya tidak akan menampilkan wizard. Nilainya tidak diganti oleh tujuan saat halaman dimuat. Menyembunyikan bidang tidak akan menonaktifkan fitur tersebut atau menghapus nilainya.

Perkiraan ukuran dan waktu mencakup hingga tiga obrolan yang dipilih dan hingga 20 pesan dari masing-masing obrolan. Ini hanyalah perkiraan: perkiraan ini tidak memprediksi batasan Telegram, kecepatan server tertentu, atau file-file dalam setiap obrolan.
