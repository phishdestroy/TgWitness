# Telegram · Muat riwayat sumber

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/history/

Muat pesan-pesan sebelumnya dari sumber yang diaktifkan, jeda dan lanjutkan, serta verifikasi laporan kemajuan yang telah ditandatangani.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Koleksi](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Koleksi](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

Di **Sumber**, tinjau obrolan yang diaktifkan, jeda pengamatan, pilih ekspor API Standar atau Takeout, lalu pilih **Muat riwayat lengkap**. Proses ini memperbarui daftar sumber tersebut dan membaca pesan-pesan lama yang tersedia ke dalam Obrolan dan jurnal pengamatan yang ditandatangani. Media menggunakan pengaturan lampiran yang ada dan antrian unduhan yang tahan lama. Ini terpisah dari ekspor JSON/HTML yang ditandatangani per obrolan.

Untuk pengumpulan di seluruh akun, pilih **Seluruh akun**, mulai pengamatan untuk memuat daftar sumbernya, dan tinjau daftar tersebut sebelum memulai riwayat. Batas daftar dialog masih berlaku (1,000 secara default, dapat disesuaikan di Parameter). Pelaksanaan yang berhasil tidak menjamin bahwa setiap dialog akun telah terdaftar. Obrolan yang ditemukan atau diaktifkan kemudian memerlukan pelaksanaan ulang. Jeda pengamatan sebelum memulai riwayat; satu proses pengambilan hanya dapat mengelola satu akun pada satu waktu.

Pilih satu hingga lima pekerja lampiran dan tentukan apakah akan mempertahankan Tindakan Terbaru yang tersedia serta membandingkan versi yang disimpan sebelumnya. Pengambilan data mungkin memerlukan persetujuan di Telegram dan waktu tunggu yang ditentukan server. Opsi-opsi ini tetap berlaku saat dilanjutkan. Lihat [perilaku Backfill dan kontrak bukti](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) untuk detail pengiriman, percobaan ulang, dan kepercayaan.

## Jeda, mulai ulang, dan hasil parsial

- **Jeda riwayat** menghentikan pembacaan. **Lanjutkan riwayat** melanjutkan dari pesan terakhir yang telah disimpan di setiap sumber; memulai ulang aplikasi juga akan membuat proses tetap dalam keadaan dijeda hingga dilanjutkan kembali. Untuk melanjutkan, diperlukan akun Telegram yang sama yang tidak aktif.
- Pengamatan pesan, pemrosesan lampiran, dan pencatatan posisi kursor dilakukan dalam satu transaksi. Proses yang dilanjutkan tidak akan mengulangi pengamatan yang telah dicatat sebelumnya. Penangkapan langsung atau proses terpisah yang dimulai secara eksplisit dapat mengamati pesan yang sama secara independen.
- Setiap sumber (setiap rentang Telegram yang dipisahkan di Takeout) menetapkan ID pesan tertinggi pada pembacaan pertamanya. Pesan-pesan yang lebih baru termasuk dalam pengamatan langsung, bukan pada halaman historis yang tersisa dari sumber tersebut.
- Sumber yang tidak dapat diakses dan sumber yang dinonaktifkan selama proses pengumpulan tetap terlihat sebagai gagal atau dilewati. Sumber lainnya tetap berlanjut; hasil keseluruhan tidak lengkap.
- Penundaan FloodWait menghormati pengaturan backoff akun yang disimpan. Kegagalan sementara akan dicoba ulang hingga lima kali; kehabisan kuota dan ruang disk rendah akan menghentikan sementara proses dengan kursor tetap utuh.
- **Akhiri proses riwayat ini** mempertahankan pengamatan yang telah disimpan. Perintah ini tidak menghapusnya atau membatalkan tugas lampiran API standar. Mengakhiri Takeout menandai file Takeout yang tersisa sebagai terlewati; menjeda membuatnya tetap dapat dilanjutkan. Proses baru membaca kembali sumber yang diaktifkan.

Penyelesaian riwayat hanya menggambarkan pembacaan riwayat. Lampiran mungkin tetap dalam status tertunda, gagal, atau dikecualikan oleh kebijakan yang dikonfigurasi. Periksa tanda terima media di jurnal dan antrian lampiran; hanya tanda terima yang telah selesai dengan byte yang terpelihara yang dianggap sebagai lampiran yang tersimpan. Operasi riwayat merupakan permintaan snapshot eksplisit dan terpisah dari opsi yang memilih kategori peristiwa langsung di masa mendatang.

## Transfer dan verifikasi

Simpan **laporan kemajuan** yang **telah ditandatangani**, lalu gunakan **"Ekspor Bukti"** untuk mengunduh jurnal dan lampiran yang disimpan. Ekspor bukti di kemudian hari mungkin mencakup catatan tambahan; laporan tersebut mengikat penghitungnya ke awalan jurnal pada saat dibuat. Jalankan verifikator dari salinan tepercaya versi ini:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Simpan sidik jari kunci penandatanganan yang diharapkan secara terpisah. Verifikator memeriksa tanda tangan laporan, arsip bukti, titik pemeriksaan laporan, rencana sumber, akun, dan jumlah pesan yang tersimpan/tidak tersedia. Proses baru juga mengaitkan kemajuan sumber dan opsi ke peristiwa kursor yang ditandatangani. Tanpa `--evidence`, alat ini hanya memeriksa laporan yang ditandatangani dan konsistensi internalnya. Bidang kemajuan lama dan ringkasan lampiran tetap menjadi pernyataan pengumpul yang ditandatangani. Verifikator bukti memeriksa byte media yang diarsipkan.

Baik penandatanganan maupun penyelesaian riwayat yang tersedia tidak membuktikan asal-usul Telegram, snapshot atomik, atau kelengkapan historis. Pesan dapat berubah saat dibaca; pesan yang dihapus serta pengeditan sementara di luar Tindakan Terbaru yang tersedia, dan Obrolan Rahasia, tidak dapat dipulihkan. Seorang operator yang mengendalikan kunci penandatanganan dapat memalsukan jurnal sebelum adanya komitmen eksternal. Gunakan titik pemeriksaan yang disimpan secara terpisah atau saksi independen untuk sifat-sifat deteksi gangguan yang terdokumentasi.

Kursor akuisisi menunjukkan status ruang kerja lokal. Memulihkan berkas ZIP bukti saja tidak akan memulihkan tugas akuisisi yang tertunda atau sesi Telegram. Simpan cadangan ruang kerja jika Anda perlu melanjutkan tugas asli.
