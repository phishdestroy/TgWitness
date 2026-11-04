# Pilih proxy

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/proxies/

Jaga akun tetap online dan putuskan sendiri apakah ia boleh menampilkan IP server Anda.

## Pilih mode IP terlebih dahulu

01**Sembunyikan alamat**

Hanya proxy. Jika tidak ada yang berfungsi, ia menunggu.

02**Langsung sebagai pilihan terakhir**

Langsung terhubung setelah jeda, lalu kembali ke proxy begitu ada yang berfungsi.

03**Server yang berada di balik terowongan atau VPN**

Koneksi langsung boleh. Mode ini tidak menyiapkan atau memeriksa VPN untuk Anda.

Rute menentukan koneksi. Mode IP menentukan apakah koneksi langsung diizinkan.

## Biarkan kolam menjaga rute

1. **Akun → Pengaturan → Pengaturan koneksi**.
2. Pilih mode IP dan **MTProxy otomatis**, atau rute tetap.
3. Simpan, lalu **Uji koneksi Telegram** (juga berfungsi sebelum masuk).
4. Mulai pengumpulan dan kirim pesan uji ke diri sendiri.

Ruang kerja baru dimulai dengan MTProxy otomatis dan **Sembunyikan alamat**. Pool memakai empat daftar publik, menguji server, mempertahankan yang baik, dan mengganti yang mati.

## Gunakan proxy Anda sendiri

SOCKS5, HTTP CONNECT, tautan proxy Telegram, atau katalog operator. Jeda pengamatan sebelum mengganti. Rahasia Fake TLS (`ee`…) tidak berfungsi.

**Pengaturan rotasi, berbagi, dan percobaan ulang**

**Parameter → MTProxy otomatis**: ambang kegagalan, jeda, rotasi, akun per proxy. Batas 1 berarti akun menunggu alih-alih berbagi. Proxy berbeda tetap bisa berbagi IP keluar yang sama.

## Memisahkan Telegram dari permintaan eksternal

MTProxy hanya membawa Telegram. Cap waktu, notifikasi, salinan, dan pemeriksaan kode lewat proxy SOCKS5/HTTP terpisah, rute SOCKS5/HTTP akun, atau langsung jika mode mengizinkan. Atau matikan saja.

`TGWITNESS_PROXY_FEED_PROXY` menetapkan rute untuk mengunduh daftar. [Saksi](https://phishdestroy.github.io/TgWitness/id/docs/witness/) punya pengaturannya sendiri. Semua ini tidak menyentuh browser atau jaringan sistem Anda.

Lainnya: [mode dan nilai bawaan](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes), [siapa yang boleh mengubah rute](https://phishdestroy.github.io/TgWitness/id/docs/access/).
