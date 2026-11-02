# Kelola sekelompok akun

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/groups/

Kelola beberapa akun pengumpul secara bersamaan sambil tetap menjaga agar catatan dan identitas penandatangan setiap akun tetap terpisah.

Grup akun menggabungkan status koneksi, kontrol pemantauan, pengaturan bersama, dan ekspor ke dalam satu tampilan kerja. Fitur ini berguna ketika beberapa akun menangani penyelidikan yang sama atau memerlukan pengaturan operasional yang konsisten.

## Buka ikhtisar grup

Di bagian **Akun**, buka grup tersebut. Setiap akun menampilkan status pemantauannya, rute koneksi, latensi rute terbaru yang terukur saat pemeriksaan terkini berhasil, dan pesan terakhir yang disimpan. Tautan **“Perlu Perhatian”** mengarah ke akun-akun yang memerlukan tindakan; **tombol “Perbaiki”** membuka ruang kerja dan kontrol yang relevan.

**Fitur "Start all"** dan **"Pause all"** berlaku pada akun yang memenuhi syarat setelah konfirmasi. **Pengaturan grup** membagikan pengaturan yang dipilih; akun dengan nilai tersendiri akan mempertahankan nilai tersebut hingga Anda memilih untuk menggantinya.

### Tinjau perubahan rute di seluruh grup

Contoh sintetis · pemeriksaan dan hasil ilustratif

1. **Pilih.** Pilih grup dan tinjau akun mana saja yang akan berubah.
2. **Persiapkan.** Pertahankan jalur akun tersebut jika memang harus tetap terpisah.
3. **Periksa.** Uji koneksi yang diusulkan dan periksa hasil pengukuran.
4. **Terapkan.** Periksa kembali sebelum menyimpan dan tinjau hasilnya untuk setiap akun.

#### Tim kasus

Pengumpul saluran · Pengumpul grup · Akun referensi

3 ruang kerja terpisah

#### Pilihan yang telah ditinjau

2 akun mengikuti rute yang diusulkan.

Akun referensi memiliki jalurnya sendiri.

#### Pemeriksaan persiapan

Pengumpul saluran: Waktu transmisi Telegram 84 ms

Pengumpul grup: Waktu transmisi Telegram 91 ms

Angka-angka ini adalah angka fiktif yang digunakan sebagai contoh.

#### Hasil aplikasi

Pengumpul saluran: rute disimpan, pengamatan dilanjutkan.

Pengumpul grup: pemeriksaan ulang gagal, pengaturan sebelumnya dipulihkan.

Akun referensi: rute asli dipertahankan.

## Ubah alur dengan menambahkan langkah peninjauan

1. Pilih "**Ubah rute grup**", lalu pilih jenis koneksi dan pengaturannya.
2. Pilih **opsi "Review"**. Tinjau akun-akun yang tercantum beserta pengaturan rute khusus masing-masing.
3. Pilih **"Prepare" dan "Check"**. Proses "Check" menggunakan saluran Telegram yang baru; rute HTTP yang didukung juga melaporkan pemeriksaan keluar HTTPS-nya.
4. Pilih "**Apply checked connection"** dan periksa hasil setiap akun. Pengamatan yang sebelumnya berjalan akan dilanjutkan jika aplikasi berhasil; akun yang tidak aktif tetap tidak aktif.

Latency menggambarkan pengukuran waktu penyiapan koneksi Telegram. Pemeriksaan exit-IP menggambarkan rute tersebut pada waktu pemeriksaan yang tercatat. Otorisasi akun dan kesehatan pemantauan memiliki indikator masing-masing; perubahan grup dapat menghasilkan hasil yang berbeda-beda per akun.

## Gunakan akses tumpang tindih

**Obrolan yang dapat dilihat oleh beberapa akun** menampilkan sumber yang dibagikan dan cakupan pengamatan ruang kerja yang tersedia. Saluran dan supergrup yang memenuhi syarat dapat menggunakan **opsi “Ekspor dengan … akun”** untuk membagi proses pengambilan riwayat satu obrolan. Obrolan pribadi dan grup biasa tetap berada di akun awal karena nomor pesan mereka termasuk dalam riwayat akun tersebut.

## Ekspor grup sebagai paket

**Grup ekspor** membuat satu berkas ZIP yang berisi ekspor bertanda tangan dari setiap akun serta daftar bertanda tangan dari berkas-berkas tersebut. Identitas dan sidik jari ruang kerja asli tetap tersedia untuk verifikasi. Bangun narasi lintas akun menggunakan referensi tersebut; satu garis waktu gabungan tetap disusun secara terpisah.

Lanjutkan dengan [desain laporan](https://phishdestroy.github.io/TgWitness/id/docs/reports/), [Case Board di dalam ruang kerja](https://phishdestroy.github.io/TgWitness/id/docs/case-board/), atau [verifikasi ekspor](https://phishdestroy.github.io/TgWitness/id/docs/exports/).
