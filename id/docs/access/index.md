# Bagikan sebuah kasus

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/access/

Bagikan kasus yang dibutuhkan seseorang. Tetap kendalikan sisanya.

01**Pilih bukti**

Pilih seluruh ruang kerja akun atau obrolan yang direkam secara individual.

02**Pilih tindakan**

Izinkan akses untuk melihat, mengekspor, atau izin operasional spesifik yang dibutuhkan oleh pengguna.

03**Tentukan batasannya**

Terbitkan token pribadi dengan masa berlaku, batasan sesi, dan pembatasan IP opsional.

Cakupan pengumpulan menentukan apa yang direkam. Cakupan akses menentukan apa yang dapat dilihat dan dilakukan oleh seseorang.

## Berikan akses kepada seseorang

1. Masuk sebagai administrator dan buka **Access**.
2. Sebutkan akses dan pilih ruang kerja serta obrolan.
3. Sertakan opsi "**Lihat"** untuk peninjau. Tambahkan opsi "**Ekspor"** jika mereka perlu mengunduh catatan.
4. Tentukan batasan, lalu tekan **Buat akses**.
5. Salin token yang ditampilkan sekali saja. Kirimkan secara pribadi bersama alamat panel.
6. Periksa tampilan yang diizinkan dalam sesi browser terpisah sebelum menyerahkannya.

## Mulailah dengan tugas yang perlu mereka lakukan

| Orang | Akses | Hasil |
| --- | --- | --- |
| Peninjau | Obrolan terpilih; hanya dapat dilihat | Baca percakapan yang terekam tanpa mengubah data yang dikumpulkan. |
| Analis | Obrolan terpilih; lihat dan ekspor | Tinjau dan unduh catatan yang diperlukan untuk kasus ini. |
| Operator | Ruang kerja yang dipilih secara keseluruhan; sumber dan koleksi | Kelola apa yang diamati dan mulai atau hentikan pengumpul data. |

Ini adalah konfigurasi yang Anda pilih, bukan peran yang tetap. Pengaturan tingkat akun dan ekspor jurnal lengkap tetap tidak dapat diakses melalui obrolan, bahkan ketika izin lain diaktifkan. Akses ke seluruh ruang kerja mencakup akun-akun di masa mendatang.

## Anda dapat mengubah pikiran Anda kapan saja

Edit akses untuk mengubah apa yang dapat dilakukan oleh permintaan berikutnya. Akhiri satu sesi atau cabut seluruh akses untuk mengakhiri semua sesinya. File yang sudah diunduh tidak dapat ditarik kembali. Mengakhiri sesi panel tidak menghentikan pengumpulan data.

**Batas sesi dan IP**

Batasi sesi paralel dan jumlah login yang berhasil, tetapkan tanggal berakhir mutlak, izinkan alamat IP atau subnet tertentu, atau batasi akses hanya pada alamat IP yang digunakan saat pertama kali login. Masa berlaku sesi dihitung berdasarkan ketidakaktifan; panel yang terbuka akan dihitung sebagai aktivitas. Periksa alamat klien yang ditampilkan oleh aplikasi saat dijalankan melalui proxy atau terowongan.

**Kunci utama dan log aktivitas**

Administrator menyimpan token panel utama. Akses yang diberikan tidak dapat mengelola akses orang lain atau membuka konsol administrator. Konsol menampilkan aktivitas proses saat ini di seluruh ruang kerja; catatan akses yang ditandatangani menyimpan peristiwa pemberian izin dan sesi tanpa token. Ruang kerja berbagi proses host dan tidak mengisolasi data dari administrator server.

Gunakan [referensi izin lengkap](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/) untuk ketujuh izin, aturan sesi, dan batasan administrator.
