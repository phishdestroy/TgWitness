# Bagikan sebuah kasus

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/access/

Bagikan kasus yang dibutuhkan seseorang. Tetap kendalikan sisanya.

01**Pilih bukti**

Seluruh ruang kerja atau obrolan tertentu.

02**Pilih tindakan**

Lihat, ekspor, atau hanya operasi yang mereka perlukan.

03**Tentukan batasannya**

Token pribadi dengan masa berlaku, batas sesi, dan aturan IP jika Anda mau.

Cakupan pengumpulan menentukan apa yang direkam. Cakupan akses menentukan apa yang dapat dilihat dan dilakukan oleh seseorang.

## Berikan akses kepada seseorang

1. Sebagai admin, buka **Akses**.
2. Beri nama, pilih ruang kerja dan obrolan.
3. Peninjau cukup dengan **Lihat**. Tambahkan **Ekspor** untuk unduhan.
4. Tentukan batasan, lalu tekan **Buat akses**.
5. Salin token (hanya ditampilkan sekali) dan kirim secara pribadi bersama alamat panel.
6. Periksa dulu apa yang akan mereka lihat di sesi browser terpisah.

## Mulailah dengan tugas yang perlu mereka lakukan

| Orang | Akses | Hasil |
| --- | --- | --- |
| Peninjau | Obrolan terpilih; hanya dapat dilihat | Membaca obrolan, tidak bisa mengubah apa pun. |
| Analis | Obrolan terpilih; lihat dan ekspor | Membaca dan mengunduh yang dibutuhkan kasus. |
| Operator | Ruang kerja yang dipilih secara keseluruhan; sumber dan koleksi | Memutuskan apa yang diamati, memulai dan menghentikan kolektor. |

Ini hanya contoh, bukan peran tetap. Akses yang terbatas pada obrolan tidak pernah mendapat pengaturan akun atau ekspor jurnal lengkap. Akses semua ruang kerja mencakup akun yang ditambahkan kemudian.

## Anda dapat mengubah pikiran Anda kapan saja

Ubah akses kapan saja, berlaku sejak permintaan berikutnya. Akhiri satu sesi atau cabut semuanya. Berkas yang sudah diunduh tidak bisa ditarik. Pengumpulan tetap berjalan.

**Batas sesi dan IP**

Batasi sesi paralel dan login, tetapkan tanggal akhir, izinkan IP atau subnet, atau kunci ke IP login pertama. Masa berlaku dihitung dari ketidakaktifan; panel yang terbuka dihitung aktif. Di balik proxy, periksa IP klien mana yang dilihat aplikasi.

**Kunci utama dan log aktivitas**

Token utama tetap di tangan admin. Akses yang diterbitkan tidak bisa mengelola akses orang lain atau membuka konsol admin. Perubahan akses dan sesi ditandatangani ke jurnal, tanpa token. Admin server tetap bisa melihat semuanya.

Ketujuh izin dan aturan sesi: [referensi akses](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/).
