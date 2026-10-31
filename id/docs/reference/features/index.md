# Fitur dan batasan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/features/

Apa yang telah diimplementasikan oleh TgWitness saat ini, batasan apa saja yang diterapkan oleh platform Telegram, dan apa saja yang masih menjadi pekerjaan di masa depan.

Referensi desain: 26 Oktober 2026. Kasus penggunaan utamanya adalah grup dan saluran Telegram pribadi yang dapat diakses oleh akun-akun yang terhubung. Dokumen ini memisahkan perilaku yang telah diimplementasikan, batasan platform, dan pekerjaan di masa depan. Sebuah item arsitektur target bukanlah klaim bahwa fitur tersebut sudah ada.

## Aplikasi mandiri

TgWitness memiliki proses instalasi, direktori data, dan siklus rilisnya sendiri. Antarmuka web yang disertakan menangani pengaturan dan peninjauan; catatan yang diekspor dapat digunakan secara mandiri.

Operator menghubungkan akun-akun mereka, memilih sumber yang dapat dilihat oleh masing-masing, dan memperoleh jurnal pengamatan yang tersimpan. Panel tersebut menampilkan konten, perubahan yang tersimpan, asal-usul pengamatan, dan celah yang diketahui. Penyelidik lain dapat memverifikasi materi yang diekspor.

Ada empat kondisi penting yang perlu diperhatikan: otorisasi akun, akses ke sumber, pengumpul yang berfungsi, dan sejauh mana kelengkapan pengiriman telah dipastikan. Tidak ada satu pun dari tiga kondisi pertama yang secara otomatis membuktikan kondisi keempat. Grup yang tidak aktif belum tentu menandakan kegagalan pengumpul.

## Penyelidikan bersama

Seorang administrator dapat menerbitkan [token akses](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/) yang dibatasi pada ruang kerja dan obrolan individu, dengan tujuh izin, pembatasan IP, masa berlaku, batas masuk, dan kontrol sesi. Seorang peninjau dengan akses baca-saja dapat memeriksa suatu kasus tanpa perlu mendapatkan otorisasi Telegram atau kunci panel utama. Akses yang dibatasi pada obrolan tetap terpisah dari pengaturan tingkat akun dan ekspor jurnal lengkap.

MTProxy otomatis menjaga rute Telegram yang berfungsi dari empat sumber publik atau katalog operator. [Mode IP](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes) menentukan apakah kegagalan harus menunggu proxy lain atau dapat menggunakan rute langsung yang secara eksplisit diizinkan. Permintaan HTTP eksternal memiliki rute terpisah dan tombol nonaktif.

## Alat arsip

`main` saat ini menambahkan [fitur perolehan riwayat](https://phishdestroy.github.io/TgWitness/id/docs/reference/history/), [pencarian dan analisis arsip](https://phishdestroy.github.io/TgWitness/id/docs/reference/analysis/), [MCP read-only](https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/), [OCR/transkripsi lokal](https://phishdestroy.github.io/TgWitness/id/docs/reference/media-analysis/), dan [webhook keluar](https://phishdestroy.github.io/TgWitness/id/docs/reference/webhooks/). Ini adalah fitur-fitur yang tersedia di repositori sumber, ditambahkan setelah pratinjau portabel versi 0.7.0. Laporan analitis dan teks yang dikenali tetap terpisah dari peristiwa yang direkam.

## Fitur tambahan opsional

Pengaturan harian adalah akun → sumber → pengamatan. **Fitur tambahan** merupakan tujuan terpisah yang mencakup bot saksi Telegram dan pratinjau tangkapan layar GitHub. Masing-masing mencantumkan ketersediaan dan persyaratannya sebelum menampilkan pengaturan. Memilih kartu akan membuka petunjuk; hal ini tidak mendaftarkan atau memulai layanan.

Pengaturan bot terdiri dari tiga langkah: buat akses baca-saja, pilih pengaturan publikasi, dan jalankan di host witness. Opsi jaringan dan publikasi, koneksi yang ada, serta perintah verifikasi diungkapkan sesuai permintaan. Konfigurasi yang diunduh berbeda dari saksi yang sedang berjalan. Mengganti opsi tambahan akan mempertahankan draf; perubahan akun dan penguncian akan menghapus token sementara dan formulir. Panduan bawaan mencakup petunjuk peluncuran. [GitHub Actions menangkap](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) peluncuran pengumpul yang disematkan dari fork Anda, menangkap satu obrolan, dan menghasilkan serah terima terenkripsi dengan riwayat alur kerja.

## Protokol dan sumber-sumber rahasia

**MTProto adalah protokol Telegram; Telethon adalah pustaka Python yang digunakan TgWitness untuk berkomunikasi menggunakan MTProto.** Keduanya bukanlah metode koneksi alternatif. Proses pengumpulan data menggunakan MTProto; saksi opsional menerbitkan pemeriksaan yang ditandatangani melalui Bot API.

Setiap ruang kerja memiliki klien yang berwenang dan aliran pembaruan akunnya sendiri. TgWitness memilih pengamatan dari sumber-sumber yang telah dikonfigurasi dan mengajukan permintaan terpisah secara eksplisit untuk fungsi-fungsi seperti penangkapan riwayat dan pengunduhan media.

Sumber pribadi tidak memerlukan nama pengguna publik. Jenis rekan Telegram dan ID numerik adalah pengidentifikasi; judul dan nama pengguna dapat berubah. Akses bergantung pada keanggotaan dan izin yang ada. TgWitness tidak secara otomatis bergabung dengan sumber atau melewati persetujuan bergabung. Hash akses dari akun lain bukanlah token akses universal.

Model pengumpulan data harus memperhitungkan riwayat tersembunyi sebelum bergabung, peran peserta/admin, pencabutan sesi, penghapusan atau perubahan izin, migrasi dari grup ke supergrup, topik/forum, diskusi yang tertaut, identitas saluran, dan lampiran yang tidak tersedia. Tidak semua kombinasi telah diuji secara langsung.

Visibilitas sumber diperiksa saat pengumpul dimulai. Jika ada sumber yang hilang dari hasil dialog yang dibatasi, hal itu berarti **akses belum dikonfirmasi**, bukan penghapusan yang terbukti. Satu sumber yang tidak tersedia tidak menghalangi pengamatan terhadap sumber lain yang dapat diakses. Jangan pernah menempatkan tautan undangan atau sesi asli di fixture publik.

## Beberapa akun

Panel ini mendukung sejumlah **ruang kerja**, masing-masing dengan:

- Otorisasi, brankas terenkripsi, dan rute koneksi.
- Jurnal SQLite dan identitas penandatanganan Ed25519.
- Sumber terpilih, antrian media, dan pengaturan penangkapan.
- Status pemantauan, kesalahan, titik pemeriksaan, dan ekspor.

Mengganti ruang kerja yang ditampilkan tidak akan menghentikan pengumpul lainnya. Otorisasi akun ganda di seluruh ruang kerja akan ditolak. Jurnal yang sudah terikat pada satu akun Telegram tidak dapat dialihkan ke akun lain; namun, menghubungkan kembali akun yang sama diperbolehkan. Hal ini menjaga identitas akun dan cakupan ID pesan yang relevan.

Tidak ada batasan jumlah tetap dan tidak ada jaminan throughput yang terukur. Ruang kerja berbagi proses Python dan event loop. Pekerja akun terpisah masih menjadi pekerjaan di masa mendatang. Untuk isolasi proses saat ini, gunakan instalasi, port, dan direktori data yang terpisah.

Tetapkan sumber-sumber yang dapat diakses oleh setiap akun. Akun yang berbeda mungkin mengamati grup yang sama, tetapi pengamatan mereka tetap terpisah dan mempertahankan asal-usulnya. Dua akun pada satu mesin yang dikendalikan oleh operator bukanlah dua saksi independen. Ekspor dilakukan per ruang kerja; paket kasus gabungan atau garis waktu Telegram global belum diimplementasikan.

## Perekaman dan atribusi

Sumber menyediakan pengaturan per akun untuk pesan baru, pengeditan, penghapusan, reaksi, dan keanggotaan. Pengaturan default menyimpan semua kategori atau pesan/pengeditan/penghapusan. Kebijakan ini berlaku untuk grup yang dipilih di ruang kerja, tetap berlaku setelah restart, dan ditandatangani dengan perubahan sebelum/sesudah. Pengaturan default menyimpan semua kategori. Menonaktifkan suatu kategori tidak menghapus catatan lama; mengaktifkannya kembali tidak memulihkan peristiwa yang terlewat. Catatan operasional, peristiwa layanan grup lainnya, dan cuplikan riwayat eksplisit bersifat terpisah. Objek Telegram yang ditangkap mungkin tetap menyimpan metadata yang tertanam terlepas dari pengaturan pembaruan terpisah. Belum ada penggantian kategori per grup.

| Materi | Tercatat saat ini | Batasan |
| --- | --- | --- |
| Pesan | Teks, ID rekan/pesan, metadata pengirim, balasan, dan amplop pembaruan asli | Tidak ada tanda tangan Telegram yang dapat diverifikasi secara publik untuk pesan tersebut |
| Edit | Versi terbaru yang terdeteksi dan semua versi yang telah disimpan sebelumnya | Pengeditan yang dilakukan selama masa downtime dapat hilang; pengirim tidak selalu sama dengan pengedit |
| Penghapusan | Pemberitahuan dan konten yang telah direkam sebelumnya, jika ada | Biasanya tidak ada informasi mengenai siapa yang menghapus atau waktu tindakan yang tepat |
| Penghapusan yang tidak tercakup | Pemberitahuan asli di tingkat akun tanpa menebak rekan | Korelasi yang ketat dengan ID yang disimpan sebelumnya dalam lingkup akun merupakan pekerjaan yang akan datang |
| Reaksi | Jumlah hitungan yang ditampilkan dan identitas terbaru yang terlihat | Daftar reaktor yang lengkap memerlukan kueri terpisah; saluran mungkin menyembunyikan identitas |
| Keanggotaan | Pesan layanan dan pembaruan yang dikirimkan kepada peserta | Visibilitas bergantung pada peran dan jenis obrolan; peristiwa yang tidak tercatat tidak berarti tidak terjadi |
| Tindakan admin | Hanya pembaruan yang relevan yang disampaikan | Pencarian terpisah pada log admin belum diimplementasikan |
| Lampiran | Deskripsi versi asli, jumlah byte yang diunduh/SHA-256, dan hasil upaya | File yang hilang mungkin tidak dapat dipulihkan; versi terbaru tidak akan menggantikannya |
| Sejarah | Cuplikan eksplisit dari pesan-pesan yang saat ini terlihat | Tidak merekonstruksi semua pengeditan atau konten yang dihapus |
| Proses pengumpulan | Mulai/berhenti, detak jantung, kesalahan, pengaturan, cakupan, dan penerimaan program | Laporan mandiri, bukan pengesahan proses independen |

Sebuah tindakan hanya dikaitkan dengan seseorang jika sumber benar-benar menyebutkan pelaku tersebut. Jika tidak, antarmuka akan melaporkan bahwa atribusi tersebut tidak tersedia. Nama pengguna dan nama adalah atribut yang diamati, bukan bukti identitas di dunia nyata.

## Kapasitas dan batasan Telegram

Tidak ada jumlah obrolan universal yang dapat dipantau dengan kualitas terjamin. Kapasitas bergantung pada jumlah peristiwa puncak per detik, volume dan ukuran lampiran, RPC tambahan, akun aktif, latensi disk/ruang kosong, kondisi jaringan, batasan Telegram, kelambatan yang dapat diterima, dan kedalaman antrian.

Telegram membedakan pengiriman pasif dari polling singkat aktif. Dokumentasi pembaruannya menjelaskan panggilan `updates.getChannelDifference` tambahan untuk saluran terbuka dan supergrup, serta merekomendasikan maksimal **sepuluh sumber yang dipolling secara singkat secara bersamaan**. Ini bukanlah batasan sepuluh grup yang dipilih atau jaminan kelengkapan.

| Mode | Tujuan | Status |
| --- | --- | --- |
| Pengamatan standar | Mencatat pembaruan yang dikirimkan dari sumber-sumber terpilih | Telah diterapkan |
| Pengamatan prioritas | Pemeriksaan perbedaan tambahan untuk kumpulan sumber yang terbatas | Belum diimplementasikan sebagai mode pengguna |

Polling frekuensi tinggi yang sewenang-wenang, mengabaikan FloodWait, atau mengasumsikan kapasitas linier dari akun tambahan bukanlah model penentuan ukuran yang valid. Batas default adalah 1.000 percakapan pertama yang terdaftar, hingga 500 pesan per cuplikan riwayat, 1–2.000 MiB per berkas yang dikumpulkan berdasarkan jenisnya, dan 4 GiB konten ZIP yang ditandatangani dan tidak terkompresi; masing-masing dapat diubah per ruang kerja di bawah **Parameter**. Ekspor tidak memiliki batasan jumlah peristiwa yang tetap. Fallback browser dibatasi hingga 128 MiB secara default; CLI streaming memiliki batas transfer yang dapat dikonfigurasi, 5 GiB secara default.

`tools/check_capacity.py` mengukur pengambilan dan ekspor data sintetis lokal. Hasilnya bukanlah pengukuran pengiriman Telegram atau jumlah obrolan nyata yang dijamin. Lihat [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/) untuk versi yang diukur dan beban kerja.

## Keandalan dan pemulihan

Perilaku yang diimplementasikan meliputi WAL SQLite/transaksi sinkron; penulisan pesan dan tugas media secara atomik; tugas yang persisten dan penundaan percobaan ulang; deskriptor versi asli; upaya ulang terbatas; FloodWait media yang disimpan; unduhan media di luar penantian jaringan peristiwa teks; ekspor awalan stabil sementara penulisan selanjutnya berlanjut; pengaturan atomik dan catatan audit; pelestarian otorisasi yang berfungsi setelah kegagalan login pengganti; isolasi ruang kerja tambahan yang rusak; upaya koneksi ulang eksplisit; pelaporan kehilangan otorisasi yang terpisah; serta deteksi perubahan waktu jam dinding menggunakan jam monotonik.

Posisi (pts/qts/seq) akun dan saluran disimpan dan dilanjutkan setelah restart, dan obrolan yang dipantau diverifikasi ulang secara berkala; lihat [format bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#durable-collection-and-process-receipts-02). Penyimpanan posisi secara berkala bukanlah konfirmasi penerimaan jurnal yang bersifat atomik dan tanpa kehilangan data.

Setiap awal proses mencatat posisi awal (head) sebelumnya dan batas offline. Riwayat saat ini tidak dianggap sebagai perbaikan celah. Kapasitas penyimpanan perbedaan Telegram terbatas; `differenceTooLong` tidak dapat merekonstruksi seluruh konten yang hilang. Celah yang tidak dapat dipulihkan harus tetap dinyatakan secara eksplisit meskipun snapshot riwayat berikutnya berhasil.

## Model bukti

Setiap peristiwa mencatat urutan, waktu pengamatan UTC lokal, waktu sumber (jika tersedia), jenis, sumber, pelaku (jika tersedia), muatan asli, hash sebelumnya, dan tanda tangan. Pengamatan pesan juga menyimpan informasi akun pengumpul dan konteks eksekusi.

Tanda terima proses yang ditandatangani berisi ID eksekusi acak; versi dependensi TgWitness/Python/OS; nilai SHA-256 berkas sumber dan sidik jari agregat; akun awal, ruang lingkup, dan pengaturan; pembacaan UTC/monotonik; serta bagian awal jurnal sebelumnya. Perubahan pengaturan, mulai/berhenti, dan kesalahan dicatat dalam jurnal yang sama. Titik pemeriksaan disimpan saat startup, setiap lima menit selama pemantauan (dapat diubah), dan saat penghentian teratur. Titik pemeriksaan lokal yang disimpan dapat mendeteksi rollback ke awalan jurnal yang lebih awal.

| Mekanisme | Apa yang ditetapkan |
| --- | --- |
| SHA-256 berkas | Byte-byte tersebut cocok dengan ringkasan yang diketahui |
| Rantai hash peristiwa | Mencatat urutan/hubungan relatif terhadap batas yang diketahui |
| Ed25519 | Tanda tangan menggunakan kunci tertentu |
| Titik pemeriksaan yang disimpan secara independen | Materi selanjutnya sesuai dengan batasan yang dipertahankan |
| Pengukuran berkas program | Laporan mandiri pengumpul mengenai berkas yang diukur |
| Tanggapan TSA independen yang valid | Keberadaan byte tertentu pada waktu TSA berdasarkan asumsi kepercayaan eksplisit |

Persiapan permintaan RFC 3161 dan verifikasi respons OpenSSL telah diimplementasikan. Pengiriman otomatis belum diimplementasikan. Permintaan atau tanda tangan lokal yang memuat waktu mesin bukanlah cap waktu independen. Lihat [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/).

Seorang operator yang mengendalikan pengumpul data dan kunci penandatanganan dapat memalsukan pengamatan baru yang telah ditandatangani. Tanda tangan tersebut tidak membuktikan asal usul Telegram, kebenaran, atau kelayakan hukum otomatis. Pengamanan yang lebih ketat memerlukan titik pemeriksaan independen/penyimpanan waktu, kontrol akses kunci, catatan transfer, dan verifikasi dari perangkat lunak tepercaya.

## Ekspor, penerapan, dan serah terima

Sebuah berkas ZIP yang ditandatangani berisi JSONL, CSV, HTML asli, lampiran yang disimpan, hash, manifest yang ditandatangani, dan alat verifikasi praktis. Berkas ini mencakup satu ruang kerja dan awalan jurnal lengkap yang tetap. Filter pencarian panel tidak menghapus catatan secara diam-diam. Kunci rahasia, token, dan sesi Telegram tidak disertakan; pengamatan asli mungkin masih berisi informasi pribadi dan metadata Telegram.

Simpan ringkasan ZIP, sidik jari tepercaya, titik pemeriksaan, tanda terima proses, dan catatan serah terima secara terpisah. Gunakan verifikator dari instalasi tepercaya, daripada hanya mempercayai kode yang dapat dieksekusi semata-mata karena muncul dalam ZIP yang diperiksa.

Antarmuka browser disertakan secara lokal tanpa Node.js, CDN, atau font eksternal. Satu token operator mengontrol instalasi. Akses jarak jauh memerlukan HTTPS atau terowongan SSH. Definisi Python asli dan kontainer disertakan, dengan contoh layanan di bawah [folder deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); pemeriksaan platform yang dijalankan tercantum secara terpisah.

Ruang kerja default menggunakan direktori data root; ruang kerja tambahan menggunakan `profiles/<id>/`. Pencadangan memerlukan proses yang dihentikan dan kumpulan data/kunci yang lengkap. Berkas ZIP bukti bukanlah cadangan aplikasi. Rahasia dapat menggunakan kunci utama eksternal untuk direktori data baru; enkripsi jurnal/media disediakan oleh disk/volume operator. Lihat [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) dan [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/operations/).

## Kriteria rilis stabil

Sebelum rilis stabil, jelaskan:

1. Grup pribadi, supergrup, forum, dan saluran yang sebenarnya dengan peran anggota/admin serta riwayat yang tersembunyi/terlihat, termasuk login/2FA, pencabutan, dan kehilangan akses.
2. Pengeditan, penghapusan, reaksi, keanggotaan, dan media yang dikendalikan terhadap tindakan yang diketahui.
3. Kegagalan proses/host, kegagalan disk/disk penuh, referensi berkas yang kedaluwarsa, FloodWait, kehilangan koneksi jaringan, berkas yang rusak, dan rollback basis data.
4. Penggunaan multi-akun secara berkelanjutan dengan latensi terukur, antrian, memori, dan ruang disk, termasuk sumber yang tenang dan berisik secara bersamaan.
5. Terjadinya gangguan antara kemajuan status MTProto dan penerimaan jurnal.
6. Instalasi bersih pada matriks sistem operasi/kontainer yang dituju serta pemulihan cadangan yang terverifikasi.
7. Tinjauan independen mengenai keamanan, tanda tangan, serta klaim atribusi dan bukti.

Polling log admin, daftar reaktor tambahan, polling prioritas, pekerja terpisah, serta enkripsi di seluruh aplikasi masih menjadi pekerjaan yang akan datang. Akses panel yang dibatasi dijelaskan dalam [bagian akses dan izin](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/). Versi 0.6 mendukung TData akun tunggal yang dibatasi dan impor berkas akun yang dijelaskan dalam [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/). Tinjau ketentuan API Telegram sebelum publikasi. Referensi penelitian dan temuan platform terdapat di [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
