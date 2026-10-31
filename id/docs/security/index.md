# Jaga keamanannya

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/security/

Ketahui rute-rute untuk Telegram, daftar proxy publik, dan layanan eksternal opsional. Ketahui apa yang dibuka oleh setiap rahasia, apa yang dilindungi oleh fitur-fitur tersebut, dan apa yang menjadi tanggung jawab Anda.

**127.0.0.1**alamat panel secara default

**256-bit**token panel acak

**0**CDN, analitik, atau font jarak jauh

**Ed25519**tanda tangan pada setiap catatan

## Tempat semua data disimpan

Pengumpul data, panelnya, dan setiap catatan yang disimpan tetap berada di komputer atau server tempat Anda menjalankannya. Telegram adalah satu-satunya tujuan secara default; tujuan lainnya diatur melalui pengaturan terpisah.

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
| **Token panel** | `panel-token.txt` di direktori data; browser menyimpannya hanya untuk tab tersebut | Semua fitur di setiap ruang kerja: membaca dan mengekspor, mengubah cakupan, masuk ke akun | Hentikan TgWitness, hapus `panel-token.txt`, jalankan kembali: token baru telah dibuat |
| **Sesi Telegram** | Vault, terenkripsi (`credentials.enc`) | Akun Telegram itu sendiri | Akhiri sesi di Telegram melalui *Pengaturan → Perangkat* |
| **Kunci penandatanganan** | Vault, terenkripsi (`signing.enc`) | Catatan yang ditandatangani dan dapat diverifikasi menggunakan sidik jari Anda | Catatan pemeriksaan yang disimpan di tempat lain, beserta saksi dan cap waktu, menunjukkan apa yang ada sebelumnya |
| **Kunci brankas** | `vault.key` di samping data, atau kunci utama eksternal untuk direktori data baru | Menguraikan isi brankas | Anggaplah sesi dan kunci penandatanganan juga telah bocor |
| **Token Witness** | Di server TgWitness | Hanya baca: titik pemeriksaan yang ditandatangani dan status kesehatan | Hapus halaman tersebut di halaman Witness; buat yang baru |
| **Kunci teks di luar situs** | Vault; unduh sekali untuk pemulihan | Menguraikan salinan di luar situs | Siapa pun yang juga memiliki objek yang disimpan tersebut dapat mendekripsinya: anggap salinan tersebut sebagai data yang terekspos |

## Apa saja yang dilindungi oleh perlindungan ini

### Tercakup

- Catatan yang diubah, dihapus, atau diurutkan ulang dalam ekspor: rantai hash atau tanda tangan tidak lagi dapat diverifikasi.
- Jurnal yang dipangkas atau dibangun ulang setelah titik pemeriksaan disimpan di tempat lain: titik pemeriksaan yang disimpan tidak lagi cocok.
- Menebak token panel: 256 bit acak, dibandingkan dalam waktu konstan; setelah 15 kegagalan dalam satu menit, alamat tersebut ditolak.
- Konten obrolan yang bermuatan negatif: teks dimasukkan sebagai teks biasa, bukan sebagai HTML; lampiran diunduh sebagai berkas; panel tidak memuat apa pun dari situs lain.
- Direktori data yang disalin dengan kunci brankas eksternal: sesi dan kunci penandatanganan tetap terenkripsi tanpa kunci utama.

### Terserah Anda

- Token panel utama memiliki kendali penuh. Berikan akses terbatas kepada orang lain ke akun, obrolan, dan tindakan yang mereka butuhkan; jaga agar kunci utama tetap rahasia.
- Seorang administrator sistem dapat membaca seluruh isi jurnal, serta mengedit dan menandatanganinya kembali. Simpan sidik jari dan titik pemeriksaan pada sistem lain.
- Teks pesan dan media tidak dienkripsi oleh TgWitness. Gunakan enkripsi disk dan izin akses yang ketat.
- Penggunaan HTTP biasa di luar localhost akan menampilkan token di jaringan. Gunakan HTTPS atau terowongan SSH.
- Tanda tangan tersebut membuktikan bahwa apa yang direkam tidak diubah, bukan berarti setiap peristiwa di Telegram telah direkam.

[Bagikan akses ke suatu kasus](https://phishdestroy.github.io/TgWitness/id/docs/access/) dengan izin, batas waktu, dan batasan sesi. Token saksi tetap merupakan kredensial terpisah.

## Memperkuat instalasi

0 dari 8 selesai

1. **Gunakan akun Telegram khusus** — jangan pernah menggunakan akun utama Anda. Token panel dan sesi memberikan kendali penuh atas akun tersebut.
2. **Pertahankan panel pada alamat 127.0.0.1.** Akses secara jarak jauh hanya melalui HTTPS (konfigurasi Caddy yang disertakan) atau terowongan SSH.
3. **Enkripsi disk** yang menyimpan direktori data: teks pesan dan media disimpan persis seperti saat diterima.
4. **Batasi direktori data** hanya untuk akun layanan. Direktori baru akan memiliki mode 0700 di Unix; di Windows, atur izin folder tersebut.
5. **Simpan kunci utama brankas di lokasi lain** pada server: atur ``TGWITNESS_VAULT_KEY_FILE`` sebelum membuat direktori data.
6. **Simpan sidik jari kunci penandatanganan dan titik pemeriksaan** di sistem lain, lalu tambahkan saksi di host lain.
7. **Jangan pernah mengunggah** kunci `data/`, sesi, `panel-token.txt`, atau vault ke GitHub atau obrolan.
8. **Jangan mencatat** header `Authorization` atau isi permintaan di proxy terbalik.

**Apakah saya dapat mengubah token panel tanpa kehilangan data?**

Ya. Token tersebut hanya membuka panel. Hentikan TgWitness, hapus `panel-token.txt` dari direktori data, lalu jalankan kembali; jurnal, sesi, dan kunci tetap utuh. Jika `TGWITNESS_TOKEN` telah ditetapkan, nilai lingkungan akan digunakan sebagai pengganti berkas tersebut.

**Mengapa pesan tidak dienkripsi saat disimpan?**

Pengumpul data harus membaca file-file tersebut untuk melakukan pencarian, membandingkan versi, dan mengekspornya. Mengenkripsi file-file tersebut dengan kunci di mesin yang sama tidak akan banyak membantu jika ada pihak yang dapat mengakses mesin tersebut. Enkripsi disk melindungi disk yang dimatikan atau dicuri; izin akses yang ketat melindungi disk yang sedang berjalan.

## Laporkan kerentanan

Gunakan **menu Security → Laporkan Kerentanan** di repositori GitHub. Cantumkan versi, dampak, dan reproduksi sintetis minimal. Jangan pernah mengirimkan kredensial, direktori akun, atau arsip bukti asli. Jika pelaporan pribadi tidak tersedia, buka isu untuk meminta saluran pribadi tanpa detail eksploitasi.
