# Telegram · Kelola sekelompok akun

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/groups/

Jalankan beberapa akun bersama, masing-masing tetap dengan catatan dan kuncinya sendiri.

Grup menyatukan status koneksi, mulai/jeda, pengaturan bersama, dan ekspor di satu layar. Praktis saat beberapa akun menangani kasus yang sama.

## Buka ikhtisar grup

Buka grupnya di **Akun**. Setiap akun menampilkan status, rute, latensi, dan pesan tersimpan terakhir. **Perlu perhatian** mencantumkan yang bermasalah, **Perbaiki** membawa Anda langsung ke sana.

**Mulai semua** / **Jeda semua** bertanya dulu sebelum bertindak. **Pengaturan grup** dibagikan, tetapi nilai milik akun tetap ada sampai Anda menggantinya.

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

1. **Ubah rute grup**, pilih jenis dan pengaturannya.
2. **Tinjau pilihan**: akun mana yang berubah dan mana yang punya rute sendiri.
3. **Siapkan dan periksa** menguji koneksi Telegram baru, dan jika memungkinkan juga IP keluar.
4. **Terapkan koneksi yang diperiksa** dan lihat setiap hasilnya. Akun yang berjalan melanjutkan, yang diam tetap diam.

Latensi adalah waktu menyiapkan koneksi Telegram; IP keluar adalah yang ditampilkan rute saat diperiksa. Hasilnya bisa berbeda per akun.

## Gunakan akses tumpang tindih

**Obrolan yang dilihat beberapa akun** mencantumkan sumber bersama dan cakupannya. Kanal dan supergrup bisa diekspor beberapa akun sekaligus lewat **Ekspor dengan … akun**. Obrolan pribadi dan grup biasa tidak bisa; nomor pesannya berlaku per akun.

## Ekspor grup sebagai paket

**Ekspor grup** memberi satu ZIP berisi ekspor bertanda tangan setiap akun dan daftar bertanda tangannya. Masing-masing mempertahankan sidik jarinya untuk verifikasi. Lini masa gabungan tetap Anda susun sendiri.

Berikutnya: [laporan](https://phishdestroy.github.io/TgWitness/id/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/id/docs/case-board/), [memverifikasi ekspor](https://phishdestroy.github.io/TgWitness/id/docs/exports/).
