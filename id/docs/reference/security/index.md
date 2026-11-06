# Keamanan dan penanganan data

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/security/

Model ancaman, model akses, data rahasia yang disimpan, paparan jaringan, impor sesi, dan cara melaporkan kerentanan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Penerapan dan pemulihan](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/)

![Penerapan & pemulihan](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Halaman ini menjelaskan akses, penyimpanan, dan perlindungan jaringan di ruang kerja lokal atau server. Untuk pengumpulan data di GitHub Runner atau di VM rahasia Intel TDX, lihat [mode verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#verification-scope), yang menambahkan pemeriksaan terhadap lingkungan pengumpulan data. Koneksi akun, pemberitahuan, cap waktu, salinan di luar lokasi, dan saksi memiliki pengaturan perutean tersendiri.

| Area | Singkatnya |
| --- | --- |
| Akses | Kunci administrator ditambah akses terbatas ke akun/obrolan, tujuh izin, dan sesi yang dapat dicabut; defaultnya menggunakan localhost |
| Rahasia yang tersimpan | Pengaturan sesi, pasangan API, kunci penandatanganan, dan proxy dienkripsi menggunakan Fernet |
| Pesan dan media | Disimpan tanpa enkripsi: gunakan enkripsi disk dan izin akses yang ketat |
| Integritas | Rantai hash SHA-256 dan tanda tangan Ed25519 pada setiap catatan |
| Batas kepercayaan lokal | Administrator host mengontrol ruang kerja dan kunci penandatanganannya; titik pemeriksaan independen menyimpan batas jurnal sebelumnya |

Untuk laporan kerentanan, lihat [kebijakan keamanan](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

**Di halaman ini**

- [Model akses](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/#access-model)
- [Isi panel dan ekspor](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/#panel-content-and-exports)
- [Rahasia dalam penyimpanan](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/#secrets-at-rest)
- [Proksi dan rute jaringan](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/#proxies-and-network-routes)
- [Masuk dan impor sesi](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/#sign-in-and-session-imports)
- [Log dan transportasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/#logs-and-transport)
- [Batas integritas](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/#integrity-limits)
- [Jika Anda mencurigai adanya masalah](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/#if-you-suspect-a-problem)

## Model akses

Token panel utama memberikan kendali penuh. Orang lain dapat memperoleh [akses terbatas](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/): ruang kerja dan obrolan yang dipilih, izin, masa berlaku, pembatasan IP, batas masuk, dan sesi yang dapat dicabut. Akses yang dibatasi pada obrolan tidak dapat melakukan operasi di seluruh ruang kerja meskipun izinnya telah dicentang. Ruang kerja berbagi proses dan tidak mengisolasi data dari administrator host.

Panel ini secara default mendengarkan di localhost. Proses masuk melalui browser menukar token akses dengan kredensial sesi; browser mengirimkannya sebagai token bearer. Token ini disimpan di sessionStorage, bukan di cookie otentikasi. Mengunci/keluar akan menghapus sesi browser. Menutup browser atau mengakhiri sesi tidak menghentikan proses pengumpulan data.

Token yang diterbitkan dan kredensial sesi disimpan sebagai hash di brankas terenkripsi. Pencabutan akan mengakhiri sesi yang terkait; perubahan izin akan memengaruhi permintaan berikutnya. File yang telah diunduh tidak dapat ditarik kembali. Administrator juga dapat membatasi sesi browser mereka sendiri, tetapi skrip yang menggunakan token panel utama secara langsung tetap memiliki akses penuh dan melewati batasan sesi browser tersebut.

Kegagalan otentikasi dibatasi berdasarkan alamat klien. Pembatasan IP menggunakan alamat yang terlihat oleh aplikasi; periksa perilaku reverse-proxy sebelum mengandalkannya. Kredensial Witness tetap terpisah sebagai kredensial titik pemeriksaan/kesehatan yang hanya dapat dibaca.

### Akses demo

`/api/demo-access` adalah bootstrap yang sengaja tidak diautentikasi untuk demo sintetis yang dimulai secara eksplisit dan terisolasi. Ini mengeluarkan kemampuan yang berlaku selama masa hidup proses, bukan token panel asli atau penggantian TGWITNESS_TOKEN. Penerbitan dan penggunaannya memerlukan peer loopback dan Host, tanpa header yang diteruskan, serta tanpa permintaan lintas asal. Ruang kerja tambahan atau sesi yang diotorisasi akan menonaktifkan jalur ini. Ruang kerja aktif tidak pernah menerbitkan kemampuan tersebut. Demo ini tidak dapat menghubungkan akun atau mengubah pengaturan pengumpulan data.

## Konten panel dan ekspor

Panel ini tidak menggunakan font eksternal, analitik, sumber daya CDN, atau media jarak jauh yang disematkan. Teks yang bersumber dari Telegram disisipkan sebagai teks, bukan HTML. Lampiran yang diunduh disajikan sebagai lampiran biner. Ekspor JSONL mempertahankan string asli; HTML melakukan escape terhadapnya; sel CSV yang berpotensi menjadi rumus diberi awalan tanda apostrof.

Ekspor tidak menyertakan rahasia otentikasi dan penandatanganan, tetapi secara sengaja berisi metadata sumber yang dikumpulkan, pengenal, dan kemungkinan konten pribadi atau sensitif. Hash akses Telegram dan referensi berkas dapat muncul dalam metadata sumber mentah.

## Rahasia yang tersimpan

Kredensial API Telegram, sesi, dan kunci penandatanganan dienkripsi menggunakan Fernet. Untuk pesan dan media lokal, enkripsi disediakan oleh disk atau volume host; ruang kerja menyimpan berkas biasa. Ekspor dapat menggunakan ZIP AES-256 yang dilindungi kata sandi, dan salinan di luar lokasi menggunakan AES-256-GCM.

Kunci brankas secara default berada di direktori data yang dilindungi. Gunakan berkas kunci utama eksternal di bawah ini untuk menyimpannya secara terpisah. Pada sistem Unix, berkas kunci pribadi baru menggunakan mode 0600 dan direktori data baru menggunakan mode 0700; pada Windows, atur ACL direktori untuk akun layanan dan administrator yang berwenang. Izin direktori yang sudah ada tetap dipertahankan.

### Kunci utama eksternal

Untuk direktori data baru, TGWITNESS_VAULT_KEY_FILE dapat menyediakan kunci utama acak eksternal. HKDF-SHA256 dan garam acak terpisah menghasilkan kunci Fernet yang berbeda untuk setiap ruang kerja. vault.external.json harus dipertahankan untuk pemulihan. Kunci utama yang hilang atau salah akan menyebabkan kegagalan. Brankas lokal yang sudah ada tidak akan dimigrasikan secara diam-diam. Panel menampilkan mode penyimpanan kunci yang dipilih. Enkripsi disk melindungi berkas pesan dan media lokal di kedua mode; lihat [koneksi dan perlindungan data](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) untuk detail pengaturan.

## Proksi dan rute jaringan

Konfigurasi proxy dienkripsi di dalam vault. Kata sandi dan rahasia MTProxy tidak dikembalikan oleh API atau ditulis ke dalam catatan bukti. Setiap ruang kerja memilih rute Telegram dan [mode IP](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes)-nya sendiri.

**Menyembunyikan alamat** akan menonaktifkan fallback Telegram langsung dan memerlukan proxy untuk permintaan HTTP eksternal. Mode fallback yang dipilih secara eksplisit memungkinkan akses langsung ke Telegram setelah penundaan; mode terowongan/VPN memungkinkan rute langsung. Memilih mode terowongan tidak menginstal atau memverifikasi VPN. Pengaturan ini tidak mengontrol seluruh lalu lintas mesin, peramban, pengelola paket, atau resolusi DNS host proxy lokal.

MTProxy hanya mengangkut lalu lintas Telegram. Permintaan eksternal dapat menggunakan proksi SOCKS5/HTTP terpisah, rute SOCKS5/HTTP ruang kerja, atau rute langsung yang diizinkan; permintaan tersebut juga dapat dinonaktifkan. Saksi independen memiliki pengaturan transportasi tersendiri. Otentikasi SOCKS5/HTTP CONNECT biasa tidak dienkripsi oleh protokol proxy tersebut sendiri. Rahasia TLS MTProxy palsu tetap tidak didukung.

## Masuk dan impor sesi

File .tgwitness-session yang telah dikonversi berisi rahasia otorisasi dalam bentuk teks biasa hingga dimuat dan disimpan di vault. CLI offline menerima skema Telethon yang telah ditinjau. Impor panel juga menerima Pyrogram SQLite, TData ZIP akun tunggal modern, dan masukan JSON yang terdokumentasi. Fitur ini diotentikasi, dibatasi hingga empat berkas / 8 MiB, dan memproses unggahan di memori tanpa mengekstrak arsip atau menyimpan berkas asli. Kredensial yang dinormalisasi hanya dikembalikan ke browser terotentikasi yang meminta; kredensial tersebut disimpan di brankas terenkripsi setelah otorisasi Telegram berhasil. Lindungi berkas asli dan berkas yang telah dikonversi, serta hindari klien bersamaan yang mengkloning otorisasi.

Pemrosesan data memverifikasi checksum kontainer, hash dekripsi lokal, dan panjang struktur. Kode sandi lokal Desktop yang diberikan digunakan sementara dan tidak disimpan. Parser terbatas ini tidak menjamin bahwa setiap versi Desktop kompatibel. Gambar QR dihasilkan secara lokal, berisi token login Telegram yang berumur pendek, dan tidak pernah dikirim ke layanan rendering eksternal. Penguncian, peralihan ruang kerja, login baru, dan perubahan rute akan membatalkan upaya QR yang tertunda. Memuat ulang/menutup tab dapat menyebabkan upaya tersebut tetap tertunda hingga masa berlakunya habis. Login QR yang berhasil tetap memberlakukan pengikatan akun. Isi API biasa tetap dibatasi hingga 16 KiB; rute impor terotentikasi menerima hingga 12 MiB JSON yang dikodekan, dengan menerapkan batas ukuran file terdekodasi yang lebih kecil secara terpisah.

Kode login dan kata sandi verifikasi dua langkah Telegram tidak disimpan secara permanen. Status nomor telepon/hash kode disimpan dalam memori selama proses otorisasi. Sesi Telegram memberikan akses ke akun; jangan pernah mengunggah direktori data, sesi, token, kunci vault, atau kunci penandatanganan pribadi ke GitHub.

## Log dan pengiriman

Respons validasi API default telah diganti agar tidak menampilkan nilai kredensial. Pencatatan akses aplikasi dinonaktifkan. Jangan konfigurasikan proxy terbalik untuk mencatat header Otorisasi atau isi permintaan. HTTP mengirimkan token dan rahasia login dalam teks biasa: gunakan HTTPS atau terowongan SSH setiap kali meninggalkan localhost.

## Batasan integritas

Pemeriksaan verifikasi lokal memeriksa tanda tangan rekaman, rantai hash, lampiran, dan manifes ekspor. Administrator memegang kunci penandatanganan lokal dan dapat membuat jurnal bertanda tangan lainnya; titik pemeriksaan yang disimpan secara independen mendeteksi penggantian awalan yang dicakupnya. Simpan sidik jari kunci dan titik pemeriksaan bersama penerima atau saksi independen.

Untuk pengumpulan yang diverifikasi secara independen, pilih [Penangkapan GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) atau [Penerapan Intel TDX](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Verifikator mereka memeriksa asal-usul alur kerja atau pengukuran perangkat keras selain integritas arsip. Cap waktu opsional dan salinan terenkripsi di luar lokasi menyediakan penanda waktu dan salinan yang dapat dipulihkan; format [bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#verification-scope) menjelaskan pemeriksaan untuk setiap mode.

## Jika Anda mencurigai adanya masalah

Pertahankan direktori data asli dan gunakan salinan terpisah untuk analisis. Laporkan versi yang terpengaruh, operasi, dan langkah-langkah yang dapat direproduksi melalui kebijakan keamanan , dengan menjaga kerahasiaan data akun dan kredensial.
