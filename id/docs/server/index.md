# Jaga agar tetap berjalan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/server/

Pastikan pengumpul tetap tersedia dan datanya tetap utuh meskipun sistem di-restart.

## Pilih metode peluncuran

Untuk instalasi lokal, gunakan [peluncur](https://phishdestroy.github.io/TgWitness/id/docs/start/) dan contoh layanan yang terdapat di [folder `deploy/`.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Untuk Docker, instal Docker dengan Compose dan jalankan dari direktori proyek:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Panel default mendengarkan pada alamat loopback host, port 8787. Buka panel tersebut secara lokal atau melalui terowongan SSH. Gunakan token dari perintah kedua untuk membuka kunci panel.

## Pertahankan seluruh direktori data

Instalasi lokal menggunakan `data/live`. Docker menggunakan volume `tgwitness-data` yang persisten. Simpan jurnal, sesi akun, kunci, dan status operasional secara bersamaan. Ekspor yang ditandatangani merupakan bukti yang berguna, tetapi bukan cadangan instalasi lengkap.

1. Hentikan pengumpulan data sebelum membuat cadangan yang konsisten.
2. Salin seluruh direktori data pribadi ke penyimpanan yang terlindungi di luar host.
3. Uji pemulihan pada instalasi terisolasi sebelum mengandalkan cadangan tersebut.

## Periksa kembali setelah restart

Pastikan ruang kerja dan kunci yang diharapkan, koneksi Telegram, sumber yang dipilih, serta penangkapan pesan baru. Status MTProto yang disimpan dan fitur penyesuaian membantu memulihkan pembaruan yang masih disimpan oleh Telegram. Alat ini tidak dapat merekonstruksi setiap pembaruan yang telah kedaluwarsa atau pengeditan yang dihapus sebelum penangkapan.

Kondisi kontainer yang baik berarti server web merespons. Gunakan pesan terkontrol dan pemeriksaan saksi untuk mengevaluasi pengumpulan data dan publikasi eksternal.

## Hanya publikasikan apa yang Anda maksudkan

Referensi penerapan mencakup contoh HTTPS, perintah volume persisten, pembaruan, dan langkah-langkah pemulihan. Perintah Docker disediakan untuk penerapan; [catatan validasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/) saat ini mengidentifikasi lingkungan yang benar-benar telah diuji.
