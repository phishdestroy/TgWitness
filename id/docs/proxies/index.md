# Pilih proxy

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/proxies/

Pastikan akun tetap terhubung. Tentukan secara eksplisit kapan rute tersebut boleh menggunakan alamat server.

## Pilih mode IP terlebih dahulu

01**Sembunyikan IP**

Gunakan proxy. Jika tidak ada yang berfungsi, tunggu tanpa koneksi langsung ke Telegram.

02**Izinkan opsi cadangan**

Izinkan koneksi langsung setelah penundaan yang telah dikonfigurasi; kembali ke proxy yang berfungsi saat ada yang merespons.

03**Tunnel / VPN**

Izinkan rute langsung melalui jaringan host. Opsi ini tidak menginstal atau memverifikasi VPN.

Rute menentukan koneksi. Mode IP menentukan apakah koneksi langsung diizinkan.

## Biarkan kolam menjaga rute

1. Buka **Akun → Pengaturan → Pengaturan koneksi**.
2. Pilih mode IP dan **MTProxy Otomatis**, atau masukkan rute tetap.
3. Simpan dan jalankan **Uji Koneksi Telegram**. Fitur ini juga berfungsi sebelum masuk (sign-in).
4. Setelah memulai pengumpulan, pastikan bahwa pesan yang dikendalikan telah tercatat dalam jurnal.

Ruang kerja baru menggunakan MTProxy otomatis dengan fitur Hide IP. Pool ini menggabungkan empat sumber publik, memeriksa entri, mempertahankan rute yang berfungsi, dan mengganti proxy yang gagal. Unduhan yang gagal tetap menyimpan snapshot sebelumnya.

## Gunakan proxy Anda sendiri

Masukkan detail SOCKS5 atau HTTP CONNECT, tempelkan tautan proxy Telegram yang didukung, atau berikan katalog operator. Jeda pemantauan sebelum mengubah rute yang aktif. Kunci rahasia TLS MTProxy palsu yang dimulai dengan `ee` tetap tidak didukung.

**Pengaturan rotasi, berbagi, dan percobaan ulang**

Di bawah **Parameter → MTProxy Otomatis**, atur ambang batas kegagalan, waktu tunggu, rotasi terjadwal, dan jumlah akun per proxy. Batas berbagi sebesar satu akan membuat akun menunggu jika tidak ada akses eksklusif yang tersedia. Interval penyegaran daftar dan pemeriksaan mengikuti nilai-nilai di ruang kerja utama. Proxy terpisah tidak menjamin alamat IP keluar yang terpisah.

## Memisahkan Telegram dari permintaan eksternal

MTProxy hanya menangani lalu lintas Telegram. Cap waktu, pemberitahuan, salinan, dan pemeriksaan sumber menggunakan proxy SOCKS5/HTTP terpisah, rute SOCKS5/HTTP akun tersebut, atau Direct jika mode IP mengizinkannya. Permintaan eksternal tersebut dapat dinonaktifkan.

Konfigurasi eksplisit `TGWITNESS_PROXY_FEED_PROXY` menentukan rute pengunduh umpan. [Saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/witness/) ini mempertahankan pengaturannya sendiri. Kontrol ini tidak menginstal VPN sistem atau mengalihkan lalu lintas peramban.

Lihat [semua mode, pengaturan default, dan daftar sumber](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes), atau [tentukan siapa yang dapat mengubah rute akun](https://phishdestroy.github.io/TgWitness/id/docs/access/).
