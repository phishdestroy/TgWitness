# Mulai dalam hitungan menit

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/start/

Pertama, lihat contoh yang berfungsi. Kemudian, hubungkan akun Anda sendiri.

## Jelajahi situs ini tanpa perlu membuat akun

Unduh atau kloning proyek ini, instal **Python 3.11 atau versi yang lebih baru**, lalu jalankan demo. Peluncur akan membuat lingkungan lokal dan menginstal dependensi yang telah ditentukan.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

Browser akan membuka ruang kerja dengan pesan-pesan fiktif. Buka percakapan, bandingkan perubahan, dan periksa hasil ekspor. Mode demo tidak terhubung ke Telegram.

![Tampilan percakapan TgWitness dengan contoh pesan](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Contoh ruang kerja. Jurnal Anda sendiri dimulai secara terpisah.

## Mulailah ruang kerja Anda sendiri

Tutup proses demo, lalu gunakan peluncur biasa:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Buka alamat lokal yang ditampilkan oleh peluncur. Jika diminta, masukkan **token akses panel** dari berkas lokal yang disebutkan di terminal. Ini akan membuka akses ke TgWitness; proses ini terpisah dari proses masuk ke Telegram.

## Rekam pesan pertama Anda

1. [Hubungkan akun Telegram khusus.](https://phishdestroy.github.io/TgWitness/id/docs/accounts/)
2. Pilih grup atau saluran yang dapat diakses oleh akun tersebut, lalu mulailah pemantauan.
3. Kirim pesan baru ke grup uji coba yang Anda kendalikan dan pastikan pesan tersebut muncul di jurnal.

Untuk instalasi server, ikuti panduan "[Keep it running"](https://phishdestroy.github.io/TgWitness/id/docs/server/).
