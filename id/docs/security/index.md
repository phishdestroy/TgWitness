# Jaga keamanannya

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/security/

Apa yang keluar dari mesin Anda, apa yang dibuka setiap rahasia, dan apa yang dilindungi versus apa yang menjadi tanggung jawab Anda.

**127.0.0.1**alamat panel secara default

**256-bit**token panel acak

**0**CDN, analitik, atau font jarak jauh

**Ed25519**tanda tangan pada setiap catatan

## Tempat semua data disimpan

Kolektor, panel, dan setiap catatan tetap di mesin Anda. Secara bawaan hanya Telegram yang dihubungi; selebihnya sakelar terpisah.

06 / APA YANG DITINGGALKAN MESINProses instalasi Anda

KOMPUTER ATAU SERVER ANDA

**Panel**127.0.0.1:8787 · token bearer

**Pengumpul**satu klien Telegram per ruang kerja

DIREKTORI DATA

**Jurnal**SQLite · berantai hash · ditandatangani

**Media**file yang diberi nama berdasarkan SHA-256

**Vault**Fernet · sesi, pasangan API, kunci penandatanganan, proxy

- **Telegram**Selalu · melalui rute Anda

  Koneksi MTProto akun ini: langsung, SOCKS5, HTTP, atau MTProxy. Mode Sembunyikan IP menunggu proxy yang berfungsi. Pengalihan ke koneksi langsung memerlukan mode yang secara eksplisit mengizinkannya.
- **Teks di luar situs**Opsional · dinonaktifkan secara default

  Jurnal, berkas, dan titik pemeriksaan dienkripsi dengan AES-GCM sebelum diunggah ke penyimpanan yang kompatibel dengan S3. Kunci tetap berada di tangan Anda; lampiran diberi nama berdasarkan hash yang dienkripsi dengan kunci, bukan hash isinya.
- **Pemberitahuan**Opsional · dinonaktifkan secara default

  Masalah dan jumlah perubahan disertai judul obrolan. Kutipan pesan hanya dikirim jika Anda mengaktifkannya.
- **Otoritas cap waktu**Opsional · dinonaktifkan secara default

  Hanya nilai SHA-256 dari titik pemeriksaan yang ditandatangani dan nilai nonce acak. Tidak ada pesan, tidak ada nama obrolan.
- **Witness**Opsional · dinonaktifkan secara default

  Mengekstrak titik pemeriksaan yang ditandatangani dan penghitung penangkapan menggunakan token baca-saja. Alat ini tidak dapat membaca percakapan atau mengubah pengaturan.

Pengaturan default: hanya koneksi Telegram yang keluar dari mesin ini.

Tujuan penyimpanan opsional dikonfigurasi per ruang kerja. Teks pesan dan media disimpan tanpa enkripsi di direktori data: lindungi dengan enkripsi disk dan izin file.

## Apa yang terungkap dari setiap rahasia

| Rahasia | Di mana disimpan | Apa yang dapat diakses | Jika bocor |
| --- | --- | --- | --- |
| **Token panel** | `panel-token.txt` di direktori data; browser menyimpannya per tab | Semua hal di setiap ruang kerja | Hentikan TgWitness, hapus `panel-token.txt`, jalankan lagi: Anda mendapat yang baru |
| **Sesi Telegram** | Vault, terenkripsi (`credentials.enc`) | Akun Telegram itu sendiri | Akhiri sesi di Telegram melalui *Pengaturan → Perangkat* |
| **Kunci penandatanganan** | Vault, terenkripsi (`signing.enc`) | Menandatangani catatan dengan sidik jari Anda | Checkpoint di tempat lain, saksi, dan cap waktu tetap menunjukkan apa yang ada sebelumnya |
| **Kunci brankas** | `vault.key` di samping data, atau kunci induk eksternal | Brankas | Anggap sesi dan kunci tanda tangan juga bocor |
| **Token Witness** | Di server TgWitness | Baca-saja: checkpoint dan status | Hapus di halaman saksi, buat yang baru |
| **Kunci teks di luar situs** | Vault; unduh sekali untuk pemulihan | Salinan luar | Siapa pun yang juga memegang bucket bisa mendekripsinya: anggap salinannya terbuka |

## Apa saja yang dilindungi oleh perlindungan ini

### Tercakup

- Catatan yang diubah, dihapus, atau diurutkan ulang: rantai hash atau tanda tangan rusak.
- Jurnal yang dipotong atau dibangun ulang setelah Anda menyimpan checkpoint di tempat lain: checkpoint tidak cocok lagi.
- Menebak token: 256 bit acak, perbandingan waktu konstan; 15 kegagalan per menit dan alamatnya diblokir.
- Konten obrolan yang berbahaya: teks tetap teks, tidak pernah HTML; lampiran diunduh sebagai berkas; panel tidak memuat apa pun dari situs lain.
- Direktori data yang dicuri dengan kunci brankas eksternal: sesi dan kunci tetap terenkripsi.

### Terserah Anda

- Token utama bisa melakukan apa saja. Beri orang lain akses terbatas dan simpan token utama untuk diri sendiri.
- Siapa pun yang menjadi admin mesin bisa membaca semuanya dan menandatangani ulang jurnal. Simpan sidik jari dan checkpoint di tempat lain.
- TgWitness tidak mengenkripsi pesan dan media. Enkripsi disknya, batasi izinnya.
- HTTP biasa di luar localhost membocorkan token. Gunakan HTTPS atau tunnel SSH.
- Tanda tangan tidak memberi tahu apa yang terlewat. Periksa cakupan dan uji pengiriman di akun dan sumber Anda sendiri.

[Bagikan akses ke sebuah kasus](https://phishdestroy.github.io/TgWitness/id/docs/access/) dengan izin, masa berlaku, dan batas sesi.

## Memperkuat instalasi

0 dari 8 selesai

1. **Gunakan akun Telegram khusus**, jangan pernah akun utama.
2. **Biarkan panel di 127.0.0.1.** Akses jarak jauh hanya lewat HTTPS (Caddy bawaan) atau tunnel SSH.
3. **Enkripsi disk** tempat direktori data; pesan dan media disimpan apa adanya.
4. **Batasi direktori data** untuk akun layanan (0700 di Unix, izin folder di Windows).
5. **Simpan kunci brankas di tempat lain** di server: atur `TGWITNESS_VAULT_KEY_FILE` sebelum start pertama.
6. **Simpan sidik jari dan checkpoint** di sistem lain, jalankan saksi di host lain.
7. **Jangan pernah mengunggah** kunci `data/`, sesi, `panel-token.txt`, atau vault ke GitHub atau obrolan.
8. **Jangan mencatat** header `Authorization` atau isi permintaan di proxy terbalik.

**Apakah saya dapat mengubah token panel tanpa kehilangan data?**

Ya, token hanya membuka panel. Hentikan TgWitness, hapus `panel-token.txt`, jalankan lagi. Jurnal, sesi, dan kunci tetap ada. Jika `TGWITNESS_TOKEN` diatur, nilai itu yang dipakai, bukan berkasnya.

**Mengapa pesan tidak dienkripsi saat disimpan?**

Kolektor harus membacanya untuk mencari, membandingkan, dan mengekspor. Kunci di mesin yang sama tidak akan menghentikan orang yang memang bisa membaca mesin itu. Enkripsi disk melindungi disk yang dicuri, izin melindungi sistem yang sedang berjalan.

## Laporkan kerentanan

**Security → Report a vulnerability** di GitHub. Versi, dampak, dan contoh minimal dengan data fiktif. Jangan pernah mengirim kredensial, folder akun, atau bukti asli. Jika pelaporan privat nonaktif, buka issue untuk meminta saluran privat, tanpa detail exploit.
