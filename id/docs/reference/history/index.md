# Muat riwayat sumber

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/history/

Muat pesan-pesan sebelumnya dari sumber yang diaktifkan, jeda dan lanjutkan, serta verifikasi laporan kemajuan yang telah ditandatangani.

**Versi utama saat ini:** tersedia dari sumber; tidak termasuk dalam pratinjau portabel 0.7.0.

Di bagian **Sumber**, tinjau obrolan yang diaktifkan, mulai pengamatan, lalu pilih **Muat riwayat lengkap**. Proses ini mengunci daftar sumber tersebut dan membaca pesan-pesan lama yang tersedia ke dalam Obrolan dan jurnal pengamatan yang ditandatangani. Media menggunakan pengaturan lampiran yang ada dan antrian unduhan yang tahan lama. Ini terpisah dari ekspor JSON/HTML yang ditandatangani per obrolan.

Untuk pengumpulan di seluruh akun, pilih **"Seluruh akun**", mulai pemantauan untuk memuat daftar sumbernya, dan tinjau daftar tersebut sebelum memulai riwayat. Batas daftar dialog masih berlaku (1.000 secara default, dapat disesuaikan di Parameter). Proses yang berhasil tidak menjamin bahwa setiap percakapan akun telah terdaftar. Percakapan yang ditemukan atau diaktifkan kemudian memerlukan proses pengumpulan ulang.

## Jeda, mulai ulang, dan hasil parsial

- **Riwayat jeda** menghentikan pembacaan. **Riwayat lanjut** melanjutkan dari pesan terakhir yang disimpan di setiap sumber; memulai ulang aplikasi juga akan membuat proses berjalan tetap dalam keadaan jeda hingga dilanjutkan kembali. Mulailah pengamatan terlebih dahulu. Untuk melanjutkan, diperlukan akun Telegram yang sama.
- Pengamatan pesan, pemrosesan lampiran, dan pencatatan posisi kursor dilakukan dalam satu transaksi. Proses yang dilanjutkan tidak akan mengulangi pengamatan yang telah dicatat sebelumnya. Penangkapan langsung atau proses terpisah yang dimulai secara eksplisit dapat mengamati pesan yang sama secara independen.
- Setiap sumber menetapkan ID pesan tertinggi pada pembacaan pertamanya. Pesan-pesan yang lebih baru termasuk dalam pengamatan langsung, bukan dalam halaman riwayat yang tersisa dari sumber tersebut.
- Sumber yang tidak dapat diakses dan sumber yang dinonaktifkan selama proses pengumpulan tetap terlihat sebagai gagal atau dilewati. Sumber lainnya tetap berlanjut; hasil keseluruhan tidak lengkap.
- Penundaan FloodWait menghormati pengaturan backoff akun yang telah disimpan. Timeout transmisi dan ruang disk yang rendah akan menghentikan sementara proses dengan kursor tetap utuh. Lanjutkan setelah penyebabnya teratasi.
- **Mengakhiri proses riwayat ini** akan mempertahankan pengamatan yang telah disimpan. Tindakan ini tidak menghapus pengamatan tersebut atau membatalkan unduhan lampiran yang sudah ada dalam antrian. Proses baru akan membaca kembali sumber-sumber yang diaktifkan.

Penyelesaian riwayat hanya menggambarkan pembacaan riwayat. Lampiran mungkin tetap dalam status tertunda, gagal, atau dikecualikan oleh kebijakan yang dikonfigurasi. Periksa tanda terima media di jurnal dan antrian lampiran; hanya tanda terima yang telah selesai dengan byte yang terpelihara yang dianggap sebagai lampiran yang tersimpan. Operasi riwayat merupakan permintaan snapshot eksplisit dan terpisah dari opsi yang memilih kategori peristiwa langsung di masa mendatang.

## Transfer dan verifikasi

Simpan **laporan kemajuan** yang **telah ditandatangani**, lalu gunakan **"Ekspor Bukti"** untuk mengunduh jurnal dan lampiran yang disimpan. Ekspor bukti di kemudian hari mungkin mencakup catatan tambahan; laporan tersebut mengikat penghitungnya ke awalan jurnal pada saat dibuat. Jalankan verifikator dari salinan tepercaya versi ini:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Simpan sidik jari kunci penandatanganan yang diharapkan secara terpisah. Verifikator memeriksa tanda tangan laporan, arsip bukti, titik pemeriksaan laporan, rencana sumber, akun, serta jumlah pesan yang tersimpan/tidak tersedia. Tanpa `--evidence`, verifikator hanya memeriksa laporan yang ditandatangani dan konsistensi internalnya. Fase kemajuan, judul, penunjuk, dan ringkasan lampiran merupakan pernyataan pengumpul yang ditandatangani, bukan direkonstruksi secara independen oleh pemeriksa laporan ini. Verifikator bukti tetap memeriksa byte media yang diarsipkan.

Baik penandatanganan maupun penyelesaian riwayat yang tersedia tidak membuktikan asal-usul Telegram, cuplikan instan, atau kelengkapan historis. Pesan dapat berubah saat dibaca; pesan yang dihapus, pengeditan sementara yang tidak terlihat, dan Obrolan Rahasia tidak dapat dipulihkan. Seorang operator yang mengendalikan kunci penandatanganan dapat memalsukan jurnal sebelum adanya komitmen dari pihak luar. Gunakan titik pemeriksaan yang disimpan secara terpisah atau saksi independen untuk memastikan sifat deteksi gangguan yang terdokumentasi.

Kursor akuisisi menunjukkan status ruang kerja lokal. Memulihkan berkas ZIP bukti saja tidak akan memulihkan tugas akuisisi yang tertunda atau sesi Telegram. Simpan cadangan ruang kerja jika Anda perlu melanjutkan tugas asli.
