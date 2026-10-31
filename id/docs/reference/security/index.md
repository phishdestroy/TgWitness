# Keamanan dan penanganan data

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/security/

Model ancaman, model akses, data rahasia yang disimpan, paparan jaringan, impor sesi, dan cara melaporkan kerentanan.

TgWitness berjalan di komputer atau server Anda sendiri. Koneksi akun, pemeliharaan daftar proxy publik, dan layanan eksternal opsional memiliki kebijakan perutean yang eksplisit. Pemberitahuan, cap waktu, salinan di luar lokasi, dan saksi dikonfigurasi secara terpisah. Halaman ini mencantumkan apa saja yang dilindungi, bagaimana caranya, dan apa saja yang menjadi tanggung jawab operator.

| Area | Singkatnya |
| --- | --- |
| Akses | Kunci administrator ditambah akses terbatas ke akun/obrolan, tujuh izin, dan sesi yang dapat dicabut; defaultnya menggunakan localhost |
| Rahasia yang tersimpan | Pengaturan sesi, pasangan API, kunci penandatanganan, dan proxy dienkripsi menggunakan Fernet |
| Pesan dan media | Disimpan tanpa enkripsi: gunakan enkripsi disk dan izin akses yang ketat |
| Integritas | Rantai hash SHA-256 dan tanda tangan Ed25519 pada setiap catatan |
| Tidak tercakup | Seorang administrator sistem, token panel yang bocor, kelengkapan pencatatan |

Untuk laporan kerentanan, lihat [kebijakan keamanan](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

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

Kredensial API Telegram, StringSession, dan kunci pribadi Ed25519 dienkripsi menggunakan Fernet. Secara default, kuncinya disimpan di direktori data terlindungi yang sama. Hal ini mengurangi risiko paparan teks biasa yang tidak disengaja; namun, ini bukan perlindungan terhadap penyerang yang dapat membaca seluruh direktori. Isi pesan dan media **tidak dienkripsi** oleh TgWitness. Gunakan enkripsi disk dan izin sistem operasi yang ketat. Berkas kunci pribadi Unix dibuat dengan mode 0600; direktori data yang baru dibuat menggunakan mode 0700. Izin direktori yang sudah ada tidak diubah. Windows mewarisi ACL direktori: batasi aksesnya hanya untuk akun layanan dan administrator yang berwenang.

### Kunci utama eksternal

Untuk direktori data baru, TGWITNESS_VAULT_KEY_FILE dapat menyediakan kunci utama acak eksternal. HKDF-SHA256 dan garam acak terpisah menghasilkan kunci Fernet yang berbeda untuk setiap ruang kerja. Berkas vault.external.json harus disimpan untuk pemulihan. Kunci utama yang hilang atau salah akan menyebabkan proses gagal. Brankas lokal yang sudah ada tidak akan dipindahkan secara otomatis. Proses yang sedang berjalan dapat mengakses kunci; ini bukan isolasi HSM. Panel melaporkan mode yang dipilih dan secara eksplisit menyatakan bahwa penyimpanan pesan/media tidak dienkripsi oleh aplikasi. Lihat [koneksi, proxy, dan perlindungan data](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) untuk model ancaman lengkap.

## Proksi dan rute jaringan

Konfigurasi proxy dienkripsi di dalam vault. Kata sandi dan rahasia MTProxy tidak dikembalikan oleh API atau ditulis ke dalam catatan bukti. Setiap ruang kerja memilih rute Telegram dan [mode IP](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes)-nya sendiri.

Mode "Hide IP" menolak fallback Telegram langsung dan memerlukan proxy untuk permintaan HTTP eksternal. Mode fallback yang dipilih secara eksplisit mengizinkan akses langsung ke Telegram setelah penundaan; mode terowongan/VPN mengizinkan rute langsung. Memilih mode terowongan tidak akan menginstal atau memverifikasi VPN. Pengaturan ini tidak mengontrol seluruh lalu lintas mesin, peramban, pengelola paket, atau resolusi DNS host proxy lokal.

MTProxy hanya mengangkut lalu lintas Telegram. Permintaan eksternal dapat menggunakan proksi SOCKS5/HTTP terpisah, rute SOCKS5/HTTP ruang kerja, atau rute langsung yang diizinkan; permintaan tersebut juga dapat dinonaktifkan. Saksi independen memiliki pengaturan transportasi tersendiri. Otentikasi SOCKS5/HTTP CONNECT biasa tidak dienkripsi oleh protokol proxy tersebut sendiri. Rahasia TLS MTProxy palsu tetap tidak didukung.

## Masuk dan impor sesi

File .tgwitness-session yang telah dikonversi berisi rahasia otorisasi dalam bentuk teks biasa hingga dimuat dan disimpan di vault. CLI offline menerima skema Telethon yang telah ditinjau. Impor panel juga menerima Pyrogram SQLite, TData ZIP akun tunggal modern, dan masukan JSON yang terdokumentasi. Fitur ini diotentikasi, dibatasi hingga empat berkas / 8 MiB, dan memproses unggahan di memori tanpa mengekstrak arsip atau menyimpan berkas asli. Kredensial yang dinormalisasi hanya dikembalikan ke browser terotentikasi yang meminta; kredensial tersebut disimpan di brankas terenkripsi setelah otorisasi Telegram berhasil. Lindungi berkas asli dan berkas yang telah dikonversi, serta hindari klien bersamaan yang mengkloning otorisasi.

Pemrosesan data memverifikasi checksum kontainer, hash dekripsi lokal, dan panjang struktur. Kode sandi lokal Desktop yang diberikan digunakan sementara dan tidak disimpan. Parser terbatas ini tidak menjamin bahwa setiap versi Desktop kompatibel. Gambar QR dihasilkan secara lokal, berisi token login Telegram yang berumur pendek, dan tidak pernah dikirim ke layanan rendering eksternal. Penguncian, peralihan ruang kerja, login baru, dan perubahan rute akan membatalkan upaya QR yang tertunda. Memuat ulang/menutup tab dapat menyebabkan upaya tersebut tetap tertunda hingga masa berlakunya habis. Login QR yang berhasil tetap memberlakukan pengikatan akun. Isi API biasa tetap dibatasi hingga 16 KiB; rute impor terotentikasi menerima hingga 12 MiB JSON yang dikodekan, dengan menerapkan batas ukuran file terdekodasi yang lebih kecil secara terpisah.

Kode login dan kata sandi verifikasi dua langkah Telegram tidak disimpan secara permanen. Status nomor telepon/hash kode disimpan dalam memori selama proses otorisasi. Sesi Telegram memberikan akses ke akun; jangan pernah mengunggah direktori data, sesi, token, kunci vault, atau kunci penandatanganan pribadi ke GitHub.

## Log dan pengiriman

Respons validasi API default telah diganti agar tidak menampilkan nilai kredensial. Pencatatan akses aplikasi dinonaktifkan. Jangan konfigurasikan proxy terbalik untuk mencatat header Otorisasi atau isi permintaan. HTTP mengirimkan token dan rahasia login dalam teks biasa: gunakan HTTPS atau terowongan SSH setiap kali meninggalkan localhost.

## Batasan integritas

Rantai hash, pemicu basis data, dan tanda tangan mendeteksi modifikasi tertentu; namun, hal tersebut tidak mencegah administrator lokal untuk menulis ulang dan menandatangani ulang jurnal tersebut. Simpan titik pemeriksaan yang ditandatangani dan sidik jari kunci publik pada sistem terpisah. Mode bukti dan salinan di luar lokasi (keduanya dinonaktifkan secara default) mengirimkan hash titik pemeriksaan ke layanan cap waktu dan salinan terenkripsi ke penyimpanan yang kompatibel dengan S3; lihat [format bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/). Log transparansi, penandatanganan yang didukung HSM, dan sertifikasi rantai penguasaan formal belum diimplementasikan.

## Jika Anda mencurigai adanya masalah

Pertahankan direktori data asli dan gunakan salinan terpisah untuk analisis. Jangan menyertakan data Telegram pribadi atau kredensial dalam masalah publik. Tidak ada sertifikasi keamanan independen yang diklaim.
