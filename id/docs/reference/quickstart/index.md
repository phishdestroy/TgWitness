# Panduan cepat

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/

Semua cara untuk menginstal dan menjalankan TgWitness: paket Windows, Python, Docker, dan demo sintetis, beserta pemeriksaan awal.

**Bahasa Inggris** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ukraina](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Bahasa Turki](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Bahasa Vietnam](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Bahasa Mandarin (Sederhana)](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness adalah aplikasi mandiri untuk memantau grup dan saluran Telegram yang dapat diakses oleh akun Anda. Aplikasi ini berjalan secara lokal dengan direktori data tersendiri.

**Pertama kali berkunjung?** [Jelajahi demo](https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/#explore-the-interface) sebelum menghubungkan akun. [Pilih panduan](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) untuk proxy, saksi, ekspor, atau pengaturan server.

## Instal dan mulai

[Pengambilan melalui GitHub Actions (pratinjau)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Pilih salah satu metode. Unduhan portabel akan tersedia setelah rilis build diterbitkan:

| Host | Tidak ada yang diinstal | Dari sumber: Python 3.11+ | Docker: Engine/Desktop dengan Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | Ekstrak `TgWitness-<version>-windows-amd64-portable.zip` dari GitHub Releases, klik dua kali `TgWitness.cmd` | Klik dua kali `Start.cmd` | Klik dua kali `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Untuk metode kode sumber, [unduh dan ekstrak `main` saat ini](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) atau kloning repositori:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

`Start.cmd` menawarkan untuk menginstal Python 3.12 bagi pengguna Windows Anda jika tidak ditemukan Python yang sesuai (winget, atau penginstal python.org bertanda tangan). `start.sh` mencetak perintah instalasi yang tepat untuk distribusi Linux atau macOS Anda jika Python belum ada. Peluncuran kode sumber pertama akan membuat `.venv` dan menginstal dependensi secara otomatis.

Docker membangun aplikasi dan menjalankannya di latar belakang; Python di host tidak diperlukan. `scripts\Docker.cmd` dan `scripts/docker-start.sh` menampilkan alamat panel dan token saat kontainer dalam kondisi baik. Perintah Docker yang setara di setiap host yang didukung adalah:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Buka **http://127.0.0.1:8787**. Gunakan token yang dicetak oleh Docker helper atau perintah Docker kedua, atau baca **berkas data/live/panel-token.txt** untuk instalasi portabel atau dari sumber. Lanjutkan ke bagian "**Connect Telegram"** di bawah ini. Instalasi native dan Docker menggunakan penyimpanan terpisah; menjalankan Docker tidak akan mengimpor jurnal native yang sudah ada.

Untuk server, [proses penerapan](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/) mencakup HTTPS otomatis, restart, publikasi gambar, pembaruan, dan pencadangan.

## Jelajahi antarmuka

1. Jalankan **TgWitness-Demo.cmd** dalam paket portabel, **scripts\Demo.cmd** di folder sumber Windows, atau `sh start.sh --demo` di Linux/macOS. Peluncuran dari folder sumber akan terlebih dahulu membuat `.venv` dan menginstal dependensi.
2. Buka **http://127.0.0.1:8787**.
3. Demo lokal akan membuka jurnal contoh secara otomatis. Tidak diperlukan salinan token untuk akses lokal langsung.

Pesan demo bersifat fiktif. Mode demo tidak dapat terhubung ke akun Telegram yang sebenarnya.

## Hubungkan Telegram

> [!PERINGATAN] **Jangan gunakan apa pun yang tidak boleh hilang.** Kami sangat menyarankan agar Anda tidak menghubungkan akun pribadi atau berharga, serta tidak membuat ID API / hash pada akun yang Anda hargai. Telegram memblokir akun secara tidak terduga dan seringkali permanen, terlepas dari klien yang digunakan. Kelancaran uji coba bergantung pada Telegram, bukan pada TgWitness, dan tidak menjamin apa pun untuk masa mendatang.

1. Jika demo bawaan sedang berjalan, hentikan dan jalankan **Start.cmd** atau `sh start.sh`. Jika tidak, biarkan instalasi langsung yang telah dijalankan di atas tetap berjalan.
2. Gunakan token panel sesuai metode instalasi Anda untuk membuka panel.
3. Jika Anda memerlukan proxy, simpan di bawah **Akun → Pengaturan → Pengaturan koneksi → Ubah rute koneksi**.
4. Di bagian **Akun**, masukkan nomor telepon Anda dan tekan **Lanjutkan**, pilih **Kode QR → Tampilkan Kode QR**, atau pilih berkas dan tekan **Hubungkan Akun**. **ID API + Hash** bersifat opsional: ruang kerja akan menggunakan pasangan yang disimpan atau diimpor, atau pasangan yang berfungsi dari kumpulan bawaan. Untuk menggunakan aplikasi Anda sendiri, tempelkan satu pasangan `API ID:API Hash` ke kolom ID API. Untuk kunci otorisasi lengkap, pilih **Kunci otorisasi**, tempelkan seluruh 512 karakter heksadesimal , dan pilih ID DC yang disediakan. ID Pengguna bersifat opsional dan akan dicentang jika dimasukkan.
5. Selesaikan metode masuk yang Anda pilih: telepon/kode/2FA, konfirmasi dari aplikasi Telegram yang sudah masuk untuk QR, atau impor sesi otorisasi yang didukung.
6. Periksa ID akun yang ditampilkan. **Sumber** Terbuka: obrolan Anda dimuat secara otomatis; tambahkan grup Anda.
7. Di bawah **Pilih perubahan mana yang akan disimpan**, pilih kategori peristiwa atau preset **Pesan, pengeditan**, **& penghapusan**, lalu simpan pengaturan pemantauan.
8. Pilih pengaturan lampiran secara terpisah, lalu tekan **Mulai pemantauan**.

Kredensial API mengidentifikasi aplikasi Anda; kredensial tersebut tidak secara otomatis memberikan otorisasi atas akun. Grup pribadi tidak memerlukan nama pengguna publik, tetapi akun Anda harus memiliki akses.

Untuk akun yang sudah ada, lihat [akun dan format sesi](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/): panel menerima Telethon StringSession, SQLite Telethon/Pyrogram, ZIP TData akun tunggal, dan JSON akun yang didukung. Pilih sesi beserta JSON pendampingnya sekaligus, lalu tekan **Hubungkan akun**. Login QR juga tersedia dengan pengaturan API opsional yang sama. TDLib, sesi bot, dan inventaris akun CSV/JSON tidak didukung.

Untuk beberapa akun, gunakan **Akun → Impor akun** dan pilih file sesi yang didukung. File JSON pendamping dipasangkan berdasarkan nama dasar (basename); setiap akun yang diimpor mendapatkan ruang kerjanya sendiri. Lihat [impor massal dan grup akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#bulk-import-and-account-groups).

Untuk menambahkan akun lain, tekan **+** di samping pemilih akun atau buka **Akun → Pengaturan → Pengaturan koneksi → Ruang kerja**, atau gunakan **Akun**. Ruang kerja memiliki sesi, jurnal, kunci, sumber, dan antrian yang terpisah. Mengganti tampilan tidak akan menghentikan pengumpul lainnya. Akun Telegram yang sama tidak dapat ditugaskan ke dua ruang kerja dalam instalasi ini. Tidak ada batasan jumlah ruang kerja; semuanya berbagi satu proses, sehingga kapasitasnya bergantung pada mesin.

Token panel langsung melindungi akses ke otorisasi Telegram dan materi yang disimpan Anda; token ini terpisah dari kredensial API Telegram. Hanya demo lokal yang secara eksplisit dijalankan dan diakses secara langsung yang mendapatkan akses otomatis. Demo jarak jauh/proksi tetap menggunakan `data/demo/panel-token.txt`.

## Tinjau dan ekspor

- **Jurnal:** cari dan saring pengamatan berdasarkan sumber dan jenis peristiwa.
- Pilih suatu peristiwa untuk memeriksa catatan aslinya, atribusi, dan versi yang disimpan.
- Rincian pengeditan menampilkan konten sebelum dan sesudah yang tersedia. Rincian penghapusan menampilkan konten terakhir yang terekam, jika ada; pelaku yang tidak dikenal tetap tidak diketahui.
- **Format ekspor:** ZIP yang ditandatangani, JSONL, CSV, dan HTML offline.
- **Ekspor obrolan lengkap** (Sumber → Ekspor obrolan lengkap): unduh seluruh riwayat yang terlihat dari satu obrolan sebagai bundel yang ditandatangani dengan `chat.json` (gaya ekspor Telegram) dan `chat.html` yang dapat dibaca. Obrolan pribadi berfungsi jika akun tersebut merupakan anggota. Ini adalah cuplikan saat ini, bukan rekonstruksi dari pesan yang dihapus atau sebelumnya diedit. Verifikasi salinan tersebut dengan `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Simpan titik pemeriksaan:** jaga agar batas jurnal yang ditandatangani tetap berada di luar pengumpul.
- **Unduh tanda terima eksekusi yang ditandatangani:** simpan catatan program/versi pengumpul.
- **Siapkan permintaan cap waktu:** siapkan permintaan offline kepada otoritas cap waktu; ikuti panduan di [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/) untuk memperoleh dan memverifikasi respons.
- **Verifikasi jurnal:** periksa tanda tangan peristiwa dan tautan rantai. Ekspor ZIP juga memeriksa media.

Browser yang didukung dapat menyimpan ekspor berukuran besar langsung ke file yang dipilih. Browser lain hanya dapat menyimpan dalam buffer maksimal 128 MiB. Selama server berjalan, CLI streaming mendukung unduhan berukuran lebih besar tanpa perlu menyimpan seluruh respons dalam buffer:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Untuk ruang kerja lain, tambahkan `--profile ID` menggunakan **Ekspor → ID Ruang Kerja**. Untuk server jarak jauh, tambahkan `--url https://your-server`. Batas transfer default adalah 5 GiB; `--max-mib` mengubahnya. Konten ZIP yang ditandatangani memiliki batas verifikasi terkompresi terpisah sebesar 4 GiB secara default (**Parameters** menaikkannya; verifikasi arsip semacam itu dengan `verify.py --max-gib N`). Verifikasi arsip menggunakan salinan verifier yang tepercaya dan sidik jari kunci/titik pemeriksaan yang disimpan secara independen.

## Periksa proses instalasi

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` memeriksa dependensi lokal, dukungan penandatanganan, penyimpanan, konfigurasi kunci, dan alamat pendengar. Alat ini tidak menginstal apa pun atau terhubung ke Telegram. Port yang sedang digunakan mungkin menandakan adanya instance lain yang sedang berjalan. Gunakan `--port` yang berbeda atau hentikan instance tersebut terlebih dahulu.

Launcher diinstal ke `.venv`. Perintah tambahan `python -m tgwitness...` harus menggunakan `.venv\Scripts\python.exe` di Windows atau `.venv/bin/python` di Linux/macOS, kecuali jika lingkungan tersebut sudah diaktifkan.

## Sesi, perlindungan, dan pengoperasian

Berkas Telethon SQLite `.session` yang tertutup dan konsisten dapat dikonversi secara lokal menggunakan `python -m tgwitness.sessions account.session --out account.tgwitness-session`, kemudian dimuat ke dalam Akun. Impor berkas langsung dan login melalui QR juga tersedia. Lihat [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) untuk format login, SOCKS5, HTTP CONNECT, MTProxy, dan kunci utama eksternal.

**Menjeda pengamatan** akan menghentikan pengumpulan data. **Mengunci** hanya menutup akses browser. Menutup tab tidak menghentikan proses pengumpul data. Menghentikan proses akan menghentikan pengumpulan data; cuplikan riwayat tidak dapat merekonstruksi semua pengeditan atau penghapusan yang terlewatkan. Lihat [cara kerja pengumpulan data](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/) terkait kebijakan peristiwa, antrian lampiran, isolasi akun, dan perilaku saat dimulai ulang.

Sesi dan rahasia dienkripsi. Isi pesan, media, dan ekspor memerlukan disk atau volume terenkripsi. Tanda tangan memastikan integritas relatif terhadap kunci tepercaya; tanda tangan tersebut tidak memastikan asal pesan dari Telegram atau mencegah pemalsuan oleh operator yang mengontrol pengumpul data dan kuncinya.

Baca [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/operations/) untuk pencadangan/pemulihan, [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/) untuk hosting, dan [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) untuk contoh layanan. Panel yang telah diinstal juga menyertakan panduan pengaturan offline di `/guide.html`.

Verifikasi aktual dan batasan yang masih ada dicatat dalam [berkas VERIFICATION.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/) dan [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
