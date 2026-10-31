# Apa yang telah diuji

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/

Uji coba Telegram secara langsung, pemeriksaan otomatis, pemeriksaan browser, dan hal-hal yang masih belum terverifikasi.

## Uji coba Telegram langsung, seluruh akun · 29 Oktober 2026

Akun yang sama tetap berjalan setelah pengujian di bawah ini. Pada 29 Oktober pukul 12:10 UTC, cakupannya diubah menjadi seluruh akun (saluran, grup, obrolan pribadi, dan bot); panel meminta konfirmasi dan jurnal yang ditandatangani mencatatnya. Pada pukul 17:59 UTC, jurnal tersebut berisi:

| Tercatat, 27 Oktober pukul 21:36 hingga 29 Oktober pukul 17:59 UTC | Jumlah |
| --- | --- |
| Catatan jurnal | 9,968 |
| Pesan baru | 5,308 |
| dari mereka setelah peralihan ke akun lengkap | 3,878 |
| Penghapusan | 784 |
| di antaranya dihapus setelah TgWitness menyimpan pesan tersebut | 596 |
| Pengeditan | 41 |
| Pesan yang ditambahkan melalui pemeriksaan ulang | 2,273 |
| Pesan-pesan yang tidak dapat lagi ditemukan saat dilakukan pemeriksaan ulang | 18 |
| Pesan yang disimpan melalui snapshot riwayat | 242 |
| Lampiran yang disimpan | 247 |
| Pengumpul dimulai | 19 |
| Telegram FloodWait ditangguhkan | 26 |

- Fitur **Verify** pada panel tersebut telah memverifikasi tanda tangan dan rantai hash dari seluruh 9.968 catatan.
- Pesan-pesan tersebut berasal dari 2 grup atau saluran serta 3 obrolan pribadi dan bot. Satu tombol pesan telah ditekan dari **Obrolan**; permintaan dan jawaban Telegram tercatat dalam jurnal.
- Obrolan baru ditambahkan saat pengumpul memindai ulang akun tersebut setelah restart. Penyimpanan pesan-pesan sebelumnya dari obrolan baru dinonaktifkan (`history = 0`), sehingga hal ini tidak dibahas di sini.

Tidak termasuk: reaksi, perubahan keanggotaan, profil pengguna, pengiriman pesan, bergabung melalui undangan, proxy, notifikasi, bot TgWitness, dan penggunaan beberapa akun sekaligus. Berkas publik hanya berisi jumlah.

## Ekspor yang dilindungi kata sandi dibuka dengan libarchive · 29 Oktober 2026

Sebuah arsip yang dibuat dengan kode enkripsi ekspor (WinZip AES-256, format yang dapat dibaca oleh 7-Zip dan WinRAR ) dibuka menggunakan Windows `tar` (bsdtar 3.6.2, libarchive). Dengan kata sandi yang benar, file yang diekstrak memiliki nilai SHA-256 yang sama dengan aslinya; kata sandi yang salah ditolak dengan pesan "Incorrect passphrase". 7-Zip dan WinRAR sendiri tidak dijalankan.

## Uji coba Telegram langsung · 27 hingga 29 Oktober 2026

Satu akun Telegram asli, yang masuk melalui kumpulan pasangan API bawaan, merekam satu supergrup mulai **tanggal 27 Oktober pukul 21:36 UTC hingga 29 Oktober pukul 05:15 UTC**. Pengumpul data tersebut dijalankan sebanyak 12 kali selama periode tersebut.

| Tercatat | Jumlah |
| --- | --- |
| Catatan jurnal, termasuk data detak dan catatan layanan | 2,385 |
| Pesan baru | 1,291 |
| Penghapusan | 472 |
| di antaranya dihapus setelah TgWitness menyimpan teks tersebut | 347 |
| Pengeditan | 12 |
| Pesan yang terlewat saat dihentikan, ditambahkan melalui pemeriksaan ulang | 12 |
| Lampiran yang disimpan | 17 |
| Lampiran tidak diunduh (pengunduhan dinonaktifkan, atau tidak ada berkas yang dapat diunduh) | 14 |
| Telegram FloodWait berhenti sejenak, masing-masing selama 3 detik, selama proses pemeriksaan ulang | 8 |

- Tanda tangan dan rantai hash dari seluruh 2.385 catatan tersebut diverifikasi menggunakan kunci publik jurnal tersebut.
- Setelah di-restart, pengumpul melanjutkan dari status pembaruan yang disimpan (`pts`) dan Telethon melakukan sinkronisasi; pemeriksaan ulang kemudian menambahkan pesan-pesan yang masih hilang.
- Pada setiap FloodWait, pengumpul menunggu selama waktu yang diminta dan kemudian melanjutkan.
- Akun tersebut tetap masuk, dan sesi yang sama terhubung kembali pada 29 Oktober.

Hal-hal yang tidak tercakup dalam pengujian ini: pengelolaan beberapa akun sekaligus, peran administrator, proxy, gangguan layanan yang berlangsung lebih dari beberapa jam, serta [prosedur penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) secara lengkap. Berkas publik hanya berisi data berikut: tidak ada pengenal akun atau obrolan, pesan, atau kredensial.

Entri-entri lama di bawah ini menjelaskan proses pengujian masing-masing; sebagian besar di antaranya menggunakan klien uji sintetis. Hasil otomatis terbaru terdapat di bawah ini.

## Daftar MTProxy publik bawaan · 29 Oktober 2026

Ini adalah catatan pengujian historis dari versi asli yang dipilih secara manual. Untuk mode pool otomatis dan IP saat ini, lihat [pengaturan koneksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes). Jumlah dan fitur yang tidak didukung di bawah ini merupakan bagian dari revisi yang diuji tersebut.

Menambahkan snapshot publik yang dibundel dan penyegaran HTTPS eksplisit dari SoliSpirit/mtproto dan zakky8/mtproto-proxy-pro. Di host ini, pengunduh aplikasi berhasil mengambil kedua umpan pada tanggal 29 Oktober 2026 pukul 12:58 UTC: **118 titik akhir unik yang kompatibel** setelah penyaringan, penghapusan duplikat, dan batasan 64 entri per sumber. Hal ini memverifikasi pengambilan daftar, bukan konektivitas atau pengiriman pesan melalui titik akhir tersebut. Tidak ada akun nyata yang terhubung ke proxy yang terdaftar selama pekerjaan ini. [Panduan operator dan pengguna](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Respons sumber yang gagal/kosong/tidak kompatibel tetap mempertahankan entri dan tanggal sebelumnya. Pembaruan tidak mengubah rute yang dipilih. Alamat publik divalidasi dan IP yang diselesaikan disematkan saat dipilih; rute operator/manual tetap terpisah. Uji koneksi kini tersedia di panel sebelum masuk ke akun. TLS ee palsu dan pemilihan proxy otomatis masih tidak didukung. Katalog operator sepenuhnya menggantikan langganan.

- Rangkaian pengujian lengkap: **366 lulus, 3 dilewati**, 287,94 detik. Peringatan ketergantungan yang ada dan pengabaian platform tetap ada. Regresi daftar publik/lokalisasi akhir: **36 lulus**, termasuk penolakan port proxy unduhan yang tidak valid; ini tumpang tindih dengan rangkaian pengujian lengkap.
- Uji kompatibilitas browser lulus dalam bahasa Inggris/Rusia, mode terang/gelap pada resolusi 390/1440 piksel: pilihan terintegrasi, tanpa pengambilan data eksternal saat membuka pengaturan, penyegaran eksplisit, rute dan cache tetap terjaga selama kegagalan, pemeriksaan pra-login, isolasi ruang kerja saat respons terlambat, detail sumber, serta tata letak dan kontras. Tidak ada kesalahan JavaScript atau permintaan eksternal dari browser.
- Cakupan terjemahan statis akhir telah disetujui untuk semua 13 bahasa; teks baru telah diterjemahkan ke dalam bahasa Rusia dengan teks cadangan dalam bahasa Inggris yang ditampilkan secara eksplisit di bagian lain. Panduan bawaan yang diperbarui telah lulus pemeriksaan tata letak dan kontras pada kedua tema.
- Pemeriksaan awal dan publikasi telah lulus (259 berkas publik, 1.354 tautan lokal); diperbarui YAML Compose dan CI telah diparsing. Docker dan CI jarak jauh tidak dijalankan di sini.
- Roda yang dibangun ulang telah lulus uji instalasi terisolasi, pemuatan daftar bundel, dan verifikasi ekspor yang ditandatangani . Semua 69 sumber daya paket sesuai dengan ruang kerja; hash sumber telah diperiksa.

Bukti: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json`, dan `test-results/public-proxies-package.log`. Konfigurasi browser/akun/transportasi bersifat sintetis; dua unduhan feed di atas merupakan permintaan HTTPS yang sebenarnya.

## Presentasi fitur tambahan opsional · 29 Oktober 2026

Tujuan bot Proof sebelumnya kini menjadi **Extras**: ikhtisar singkat yang diikuti oleh halaman pengaturan terpisah untuk opsi yang dipilih. Formulir saksi memiliki tiga langkah, dengan pengelolaan koneksi, opsi jaringan, dan detail penerapan yang disembunyikan. GitHub secara eksplisit direncanakan dan tidak memiliki formulir kredensial. [Ikhtisar dalam bahasa Rusia](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- 30 tes terfokus telah dilalui untuk lokalisasi, pengaturan TgWitness, dan pemeriksaan publikasi.
- Pengujian penerimaan pengaturan Chromium lulus dalam bahasa Inggris/Rusia, mode terang/gelap, pada resolusi 390/1440 piksel: fokus keyboard dan tombol Enter, tidak ada koneksi tersembunyi saat memilih fitur tambahan, penyimpanan draf, unduhan konfigurasi/token yang disematkan, penghapusan token saat terkunci, dan tautan panduan lokal yang berfungsi. Pemeriksaan tata letak dan kontras teks dengan latar belakang solid telah lulus.
- Pengujian penerimaan peralihan ruang kerja telah lulus, termasuk respons token yang tertunda yang tiba setelah peralihan. Navigasi cepat memungkinkan pencarian fitur tambahan melalui istilah bot, bukti, dan GitHub; pengujian resolusi 320/390/1440 piksel serta dukungan bahasa Rusia dan RTL yang sudah ada juga lulus.
- Tidak ditemukan kesalahan JavaScript atau permintaan eksternal ke browser selama proses pengaturan. Ini adalah pemeriksaan antarmuka pengguna (UI) sintetis, bukan bukti publikasi Telegram atau bot yang baru dan aktif.
- Pemuatan bahasa akhir dan cakupan kamus telah lolos untuk semua 13 wilayah bahasa, dengan tetap mempertahankan bahasa Inggris sebagai cadangan eksplisit di luar bahasa Rusia. Panduan Proof yang diperluas juga telah lolos pemeriksaan tata letak/kontras pada resolusi 320/768/1440 piksel di kedua tema.
- Roda yang dibangun ulang telah lulus verifikasi instalasi terisolasi dan ekspor yang ditandatangani. Semua 67 sumber daya yang dikemas sesuai dengan ruang kerja; arsip sumber berisi 253 file publik. Pemeriksaan sumber/tautan berhasil untuk 1.346 tautan dokumentasi lokal.

Tanda terima: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log`, dan `test-results/extras-artifacts.json`. Aset tangkapan layar menggunakan ruang kerja sintetis.

## Audit pengaturan bot dan proxy Witness · 29 Oktober 2026

Pengaturan saksi (sekarang **Ekstra → Bot di saluran Anda**) menyiapkan saksi yang dihosting secara independen: kunci pengumpul yang disematkan , unduhan token berskala, saluran sendiri, kebijakan publikasi, rute HTTP/SOCKS5, dan API Bot khusus. Token bot tetap berada di host saksi. Kunci `--check-config` barunya memvalidasi konfigurasi dan berkas tanpa membuka koneksi jaringan atau membuat kunci. Jalur berkas JSON diresolusi di samping konfigurasi. Semua varian saksi Compose kini meneruskan pengaturan proxy HTTP dan Bot API.

Pengaturan akun mendukung katalog MTProxy publik yang dikelola operator, pratinjau tautan proxy Telegram kustom, dan bidang manual yang sudah ada. Respons katalog menghilangkan informasi rahasia; pemilihan menyimpan rute di brankas ruang kerja. Katalog yang hilang atau rusak membuat rute manual tetap tersedia. Tidak ada alamat proxy proyek atau layanan saksi yang dihosting yang diciptakan atau diaktifkan secara default. Contoh Caddy hanya mengekspos titik akhir head yang terbatas ketika saksi eksternal harus menjangkau pengumpul yang panelnya tetap bersifat pribadi.

Validasi:

- Rangkaian lengkap: **348 lulus, 3 dilewati**, 195,81 detik. Keterbatasan Windows menjadi penyebab dilewatinya beberapa tes; dua peringatan deprecation dependensi yang ada tetap ada.
- Pengujian regresi akhir untuk saksi/konfigurasi/rilis: **11 lulus, 1 dilewati**. Ini mencakup rangkaian pengujian lengkap. Pengujian meliputi resolusi jalur, pemeriksaan awal offline, penandatanganan/publikasi melalui fixture API Bot HTTP loopback yang sebenarnya, kegagalan pengiriman yang tercatat, verifikasi token saluran, dan pengecualian rahasia proxy.
- Pengujian penerimaan pengaturan Chromium lulus dalam bahasa Inggris/Rusia pada resolusi 390/1440 piksel: konfigurasi yang disematkan dan pengunduhan token, penghapusan token saat terkunci, pemilihan katalog, pratinjau tautan khusus diikuti dengan penyimpanan eksplisit, tata letak/kontras, serta tidak ada kesalahan JavaScript atau permintaan browser eksternal. Memperbaiki judul akun Rusia yang terlalu sempit dan tumpahan pada tab login.
- Ruff, pemeriksaan sumber/tautan, serta penguraian YAML Compose/alur kerja telah lulus.
- Roda yang dibangun ulang telah lulus pemeriksaan instalasi terisolasi, panel/sumber daya statis, dan otentikasi API, serta verifikasi independen terhadap ekspor sintetis 32 peristiwa, baik yang langsung maupun yang dialirkan.

Bukti: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log`, dan `setup-package.log`. Pemeriksaan ini menggunakan akun sintetis/proksi dan fixture Bot API lokal. Pemeriksaan ini tidak mengklaim adanya publikasi bot yang sebenarnya, server MTProxy publik yang berfungsi, eksekusi CI jarak jauh, atau penyebaran Docker. Riwayat pengamatan Telegram yang sebenarnya yang disimpan di atas tetap menjadi bukti terpisah. [Petunjuk pengaturan](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Tinjauan presentasi dan dokumentasi · 29 Oktober 2026

Halaman produk, layar akses, berkas README dalam bahasa Inggris/Rusia, dan gambar presentasi kini memiliki gaya visual yang seragam. Tangkapan layar publik menggunakan data demo fiktif. Revisi ini juga memperbaiki deskripsi validasi langsung dan pemulihan yang sudah usang di atas.

- Pengujian lokalisasi, situs, dan publikasi yang difokuskan: **33 lulus, 1 dilewati**. Pengujian yang dilewati memerlukan pembuatan symlink yang tidak tersedia di host ini.
- Penerimaan panel Chromium secara umum telah lolos, termasuk semua katalog bahasa, tata letak RTL, tema terang/gelap, kontras teks yang jelas, dan peralihan ruang kerja. Pemeriksaan pembuatan profil kini menunggu respons HTTP yang sebenarnya sebelum memeriksa ruang kerja yang dipilih.
- Layar akses bahasa Inggris/Rusia telah lulus pemeriksaan tata letak dan kontras pada kedua tema pada resolusi 320, 390, 768, 850, dan 1440 piksel; tombol kirim tetap berada di dalam viewport awal.
- Uji penerimaan situs publik berhasil pada resolusi 320, 390, 768, 1024, dan 1440 piksel, termasuk kontrol riwayat pesan, pembesaran tangkapan layar/tombol Escape/kembali ke fokus, tab keyboard, penolakan clipboard, subjalur proyek, gerakan yang dikurangi, dan fallback tanpa JavaScript. Tidak ada permintaan aset yang gagal, permintaan eksternal, atau kesalahan JavaScript yang terdeteksi.
- Roda yang dibangun ulang telah lulus pemeriksaan instalasi terisolasi: sumber daya panel dan lokal dimuat, akses API memerlukan otentikasi, dan ekspor langsung/aliran secara independen memverifikasi semua 32 peristiwa sintetis. Pemeriksaan Ruff dan sumber/tautan publik telah lulus.

Tanda terima lokal: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log`, dan `design-package/install-receipt.json`. Rangkaian backend lengkap tidak dijalankan ulang untuk perubahan presentasi/dokumentasi ini; hasil sebelumnya tetap ada dalam audit prapublikasi.

## Versi 0.6.1

Versi 0.6.1 mengubah tampilan panel, peluncur, pengemasan, dan dokumentasi; kode untuk pengumpulan, penyimpanan, penandatanganan, dan ekspor tetap tidak berubah. Pada Windows 11 / Python 3.12.10 dengan runtime yang disematkan:

- Paket lengkap ini lulus **137 tes** dengan **2 tes yang dilewati** dan peringatan Starlette yang sudah ada. Tes baru mencakup penanganan Ctrl+C pada peluncur (server diberi waktu 30 detik untuk berhenti secara teratur) serta kegagalan langkah pengaturan yang dapat ditindaklanjuti.
- Chromium (headless shell 156) lulus semua **45 skenario umum** dan **35 skenario impor akun/QR/Kunci Otentikasi**, termasuk pemeriksaan kontras teks solid, tidak ada luapan horizontal pada 320–1440 px, dan bidang login pertama yang terlihat pada 320/390 px. Tidak ditemukan kesalahan JavaScript pada halaman atau permintaan eksternal.
- `python start.py --setup-only` menginstal ulang paket tersebut sebagai versi 0.6.1 dan `python start.py --check` melaporkan bahwa semuanya siap. Server `python -m tgwitness --demo` yang asli mengembalikan panel, lembar gaya, skrip, logo, panduan, dan `/api/status` versi 0.6.1; `workspace.css` yang telah dihapus mengembalikan kode 404.
- `Start.cmd` menemukan instalasi Python di luar PATH. Karena tidak ada Python yang tersedia, sistem menampilkan tawaran instalasi; setelah menolak, sistem mencetak petunjuk manual dan keluar pada langkah 1. Langkah pengunduhan dari python.org berhasil mengunduh penginstal versi 3.12.10 dan lulus pemeriksaan Authenticode dari Python Software Foundation; penginstal itu sendiri tidak dijalankan di host ini.
- `start.sh`, tanpa menampilkan kode Python apa pun, mencetak petunjuk instalasi dan keluar. 1. `scripts\Docker.cmd` dan `scripts/docker-start.sh` diuji terhadap file eksekusi `docker` palsu: urutan panggilan yang benar, alamat panel, dan keluaran token, serta tidak ada pesan keberhasilan setelah kegagalan.
- `python tools/build_portable.py` membuat paket Windows berukuran 18,8 MiB setelah memverifikasi checksum embeddable-runtime yang disematkan. Diekstrak ke jalur yang mengandung spasi dan dijalankan hanya dengan direktori `C:\Windows` di PATH, Python tertanamnya berhasil melewati `TgWitness-Check.cmd`, menyajikan demo (32 peristiwa) dan ruang kerja langsung, serta Chromium menampilkan jurnal dan panel detail tanpa kesalahan JavaScript. Data ditulis ke folder `data` dalam paket tersebut.
- `python tools/build_preview.py` menghasilkan arsip sumber yang berisi 110 berkas. Uji coba `git add` mencantumkan 110 berkas yang sama tanpa berkas sesi, kunci, basis data, token, log, atau ekspor, tanpa jalur absolut lokal, dan tanpa string yang menyerupai rahasia.

Tidak dijalankan dalam proses pengemasan tanggal 27 Oktober ini: instalasi Python otomatis itu sendiri, pemeriksaan Docker build/Compose, eksekusi di Linux/macOS, atau latihan akun aktif baru. Bukti Telegram yang sebenarnya direkam di atas dan dalam pemeriksaan akun sebelumnya di bawah ini. Definisi CI saja tidak memenuhi syarat sebagai eksekusi platform.

## Versi 0.6.0

Suite runtime terpasang terbaru di Windows 11 / Python 3.12.10 lulus **135 tes**, dengan 1**tes yang dilewati**, dalam waktu 26,53 detik dan peringatan Starlette yang sudah ada. Pengesampingan tersebut memerlukan izin POSIX. Setelah menambahkan renderer QR ke pemeriksaan kesiapan dan pengukuran proses, 8 pemeriksaan kesiapan/ruang kerja yang terpengaruh juga berhasil dilalui.

Cakupan baru mencakup skema Telethon 7/8, skema Pyrogram 2/3, JSON lengkap dan JSON khusus metadata, file akun yang cocok/bertentangan, kode sandi TData, perubahan checksum dan jalur yang tidak aman, konversi dalam memori secara offline/terotentikasi, pemeriksaan ID akun daring, keberhasilan QR/2FA/kedaluwarsa, pembatalan yang kedaluwarsa, dan isolasi akun. Fixture TData menggunakan implementasi AES-IGE terpisah untuk enkripsi.

Chromium berhasil melewati **45 skenario umum** dan **35 skenario impor akun/QR/Kunci Otentikasi**, tanpa ditemukan kesalahan JavaScript pada halaman atau permintaan eksternal. Pemeriksaan browser baru mencakup keempat format input secara bersamaan, TData yang dilindungi, metadata API, rendering QR, kedaluwarsa/percobaan ulang, 2FA, penolakan akun yang salah, pembatalan kunci/ruang kerja, tata letak responsif, dan respons konversi terlambat setelah pemilihan file yang lebih baru.

Kedua rangkaian peramban kembali lulus setelah perubahan pada entri akun. Pengaturan langsung membuka formulir akun; mode demo membuka jurnal contohnya. Halaman Akun demo menampilkan petunjuk pengaktifan langsung dan menyembunyikan kolom input kredensial. Pemeriksaan terfokus pada resolusi 320, 390, dan 1440 piksel memastikan bidang angka dan tombol utama muat tanpa perlu menggulir, bidang API awalnya terlipat, dan kontras teks tetap terbaca. Kontrol perekaman dan verifikasi tetap tertutup setelah membuka bagian baru yang dapat diperluas.

Alur Auth Key langsung diuji dengan kredensial sintetis melalui titik akhir impor dan otorisasi yang sebenarnya. Pemeriksaan mencakup kunci yang tidak lengkap, DC yang hilang, ID Pengguna yang tidak akurat, identitas akun yang tidak cocok, kredensial API yang tersimpan, kemajuan permintaan yang terlihat, penghapusan rahasia, dan respons terlambat setelah pengeditan atau perubahan metode. Keempat metode masuk diperiksa pada resolusi 320, 390, dan 1440 piksel. Pemilih berkas muncul sebelum panduan format, dan tombol "Connect" sesuai dengan jendela tampilan awal 844 piksel dengan pengaturan API yang disembunyikan. Tidak ada upaya otorisasi Kunci Otentikasi yang sebenarnya dalam uji penerimaan antarmuka pengguna ini.

Penyegaran panel telah diperiksa kembali dengan kedua rangkaian browser: tidak ada kesalahan JavaScript halaman atau permintaan eksternal yang terdeteksi. Rangkaian akun kini mencakup penyisipan satu pasangan ID API/hash, penolakan pasangan yang tidak valid atau berlebih tanpa mengganti bidang, panduan khusus metadata, serta mengabaikan respons impor yang kedaluwarsa setelah perubahan metode masuk atau pengeditan kredensial manual. Enam pemeriksaan terfokus tambahan lulus untuk panduan pengaturan, perintah mulai/jeda yang eksplisit, pemulihan pencarian kosong, serta tata letak koneksi akhir/panduan lokal dan kontras teks yang jelas pada resolusi 320, 390, dan 1440 piksel. Pembaruan masuk langsung menambahkan satu operasi permintaan nomor telepon/kode dan menggunakan kembali pasangan API yang tersimpan di ruang kerja saat ini untuk masuk melalui telepon, QR, dan sesi. Rangkaian pengujian Python lengkap di atas mencakup pengujian persistensi baru, penolakan kredensial parsial, dan isolasi ruang kerja. Pemeriksaan browser mencakup entri nomor telepon langsung, penggunaan ulang kredensial yang disimpan, perutean berbasis metadata saja, otorisasi berkas satu tombol, dan penolakan akun duplikat. Formulir token panel dan nomor telepon yang disederhanakan juga telah diperiksa tanpa pengguliran awal pada resolusi 320, 390, dan 1440 piksel. Pemeriksaan kompatibilitas memastikan bahwa formulir nomor telepon langsung dapat menggunakan titik akhir konfigurasi/kode sebelumnya saat proses lama masih berjalan.

Satu akun yang disediakan pengguna diperiksa secara terpisah, di luar pengaturan pengujian publik. Input Telethon, Pyrogram, dan TData-nya mengarah ke otorisasi yang sama; berkas JSON yang menyertainya menyediakan kredensial API. Keempat berkas tersebut dimuat melalui panel 0.6.0 dan Telegram mengonfirmasi ID akun numerik yang diharapkan. Berkas sumber tetap tidak berubah. Tidak ada sumber yang dipilih dan pengamatan tetap dinonaktifkan. Hal ini memenuhi syarat sebagai satu contoh impor/login, bukan pengumpulan data langsung, pemulihan, atau kapasitas.

Telegram juga menerbitkan token QR asli, yang dibatalkan tanpa dipindai. Alur konfirmasi QR lengkap dan 2FA diuji menggunakan klien sintetis; konfirmasi seluler terhadap aplikasi Telegram asli tetap menjadi langkah penerimaan terpisah. Tidak ada pengenal akun asli, rahasia, atau tangkapan layar yang disertakan dalam berkas publik.

Peningkatan peluncur telah selesai; sumber, metadata yang terpasang, dan penanda kesiapan melaporkan versi 0.6.0, dengan kode QR 8.2 dan kode `pip check` yang lulus verifikasi. Roda yang terpasang melayani panel dan panduan, menolak permintaan API yang tidak terotentikasi, serta secara independen memverifikasi ekspor sintetis 32 peristiwa baik yang langsung maupun yang dialirkan. Panduan offline yang diperbarui telah diperiksa pada resolusi 320, 390, dan 1440 piksel. Tangkapan layar publik tetap bersifat sintetis.

Rilis sumber berisi 107 berkas yang termasuk dalam daftar putih. Tautan dokumentasi lokal dapat diakses. Eksekusi Docker/Caddy, publikasi CI/paket jarak jauh, runtime ARM64, pengumpulan berkelanjutan, serta matriks penerimaan Telegram langsung secara lengkap belum didukung di sini.

## Versi 0.5.1

Pada Windows 11 / Python 3.12.10, rangkaian lingkungan proyek lengkap berhasil dilalui: **94 lulus, 2 dilewati**, dalam 31,21 detik, dengan peringatan Starlette yang sudah ada. Proses yang dilewati memerlukan izin POSIX dan pembuatan tautan simbolis yang tidak tersedia di host ini. Fixture HTTP unduhan menampilkan diagnostik utas permintaan; semua asersi lulus. Pelaksanaan ini tidak menjamin tidak adanya masalah transportasi pada host.

Latihan cakupan regresi baru mencakup penolakan StringSession, perubahan kode dan akun 2FA, pencarian identitas yang dibatalkan, pembatalan login yang tertunda, serta pembaruan melalui penanganan terdaftar pada klien aktif, ditolak, digantikan, dan probe. Hanya pengumpul aktif yang menyumbangkan peristiwa; kredensial yang disimpan dan riwayat yang ditandatangani tetap utuh. Pemeriksaan baru lainnya mencakup pencarian Unicode setelah membuka kembali basis data, penyertakan batas kebijakan pemantauan dalam Cakupan, dan pengecualian pengemasan sumber terbuka.

Proyek sebenarnya, `pythonw.exe`, meluncurkan panel sintetis yang terisolasi, mengembalikan kode status HTTP 200, dan menyimpan diagnostik saat startup di `logs/server.log`. Log tersebut tidak berisi token panel yang dihasilkan atau catatan akses HTTP. Pengujian hanya menghentikan proses sintetisnya sendiri. Tidak ada tugas Task Scheduler yang terdaftar; proses masuk/keluar, mode tidur, dan pemulihan layanan tetap merupakan kualifikasi terpisah.

Pengujian penerimaan Chromium berhasil melewati **45 skenario**, tanpa kesalahan JavaScript pada halaman dan tidak terdeteksi adanya permintaan eksternal. Pemeriksaan baru mencakup tanggal dan waktu timeline 601/768/850 piksel, draf lampiran saat pembaruan status, pengeditan terbaru yang dilakukan saat menyimpan, hasil verifikasi yang dihapus saat berpindah akun, respons verifikasi terlambat setelah berpindah dan kembali, serta batas verifikasi eksplisit saat peristiwa baru tiba. Jarak ikon pencarian/teks juga telah diperbaiki dan rangkaian pengujian browser dijalankan kembali.

Eksekusi browser menggunakan runtime yang disematkan di `.venv` dan Playwright 1.62.0/Chromium yang disediakan sistem, ditambahkan setelah lingkungan proyek pada jalur impor. Pemasangan dependensi pengembangan opsional dihentikan selama proses unduhan Playwright yang lambat; tidak ada versi alat browser baru yang memenuhi syarat. Sebuah `python start.py --setup-only` normal menyelesaikan peningkatan aplikasi. Sumber, metadata yang terinstal, dan penanda peluncur melaporkan versi 0.5.1; `pip check` lulus. Pemeriksaan kesiapan lulus pada jalur baru yang belum pernah digunakan, dengan tetap menampilkan peringatan kunci brankas lokal yang diharapkan.

Paket 0.5.1 diinstal secara terpisah dan diuji secara singkat: semua aset panel/panduan telah disajikan, akses API tanpa otentikasi ditolak, dan ZIP bukti 32 peristiwa baik yang langsung maupun yang dialirkan telah lulus verifikasi independen. Berkas-berkas aplikasi dalam paket yang diinstal telah dibandingkan dengan kode sumbernya. Arsip kode sumber publik menggunakan daftar putih jenis berkas yang eksplisit dan menolak berkas sumber yang ditautkan; materi runtime yang ditempatkan di dalam direktori sumber dikecualikan dari pengujian regresi.

Selama proses perbaikan kode, pemilihan sumber terbuka dan kumpulan kandidat Git berisi 86 berkas, tanpa menyertakan direktori data runtime. Pemindaian terhadap pola kunci pribadi yang dapat dikenali, token GitHub, token bot Telegram, dan StringSession tidak menemukan kecocokan. Ini adalah pemeriksaan pola terbatas, bukan audit rahasia yang komprehensif. Pemeriksaan aturan abaikan mencakup dua belas artefak akun/data/ekspor yang umum. YAML Workflow/issue/Compose dan skrip tugas Windows berhasil diurai. Tautan dokumentasi lokal dapat diakses.

Ketujuh temuan dari tinjauan tanggal 27 Oktober telah ditangani. Eksekusi alur kerja GitHub, runtime Linux/macOS/Docker, Telegram asli, interoperabilitas dengan proxy eksternal/TSA, serta kualifikasi beban berkelanjutan tetap berada di luar cakupan pengujian lokal ini. Tidak ada publikasi repositori, pendaftaran layanan, atau pengumpulan akun asli yang dilakukan.

### Pembaruan dokumentasi bahasa Inggris

Berkas README, referensi akun/sesi, alur kerja pengumpulan data, dan panduan yang disertakan kini menjelaskan input yang didukung, perilaku ruang kerja, kebijakan peristiwa, dan format ekspor dalam bahasa Inggris. Tiga tangkapan layar publik telah diperbarui menggunakan data sintetis. Pada saat itu, koleksi sumber terbuka berisi 88 berkas, termasuk dua panduan baru. Semua 131 tautan lokal di 23 dokumen Markdown dapat diakses.

Setelah penyuntingan antarmuka dan panduan, uji penerimaan Chromium kembali lulus semua 45 skenario, tanpa ditemukan kesalahan JavaScript pada halaman atau permintaan eksternal. Rangkaian pengujian Python lengkap tidak dijalankan ulang untuk pembaruan dokumentasi dan presentasi ini; hasil 94 lulus di atas merupakan hasil dari proses perbaikan kode sebelumnya.

Roda yang telah dibangun ulang dipasang ke target terisolasi yang baru. Panel dan aset panduannya berfungsi dengan baik, akses API tanpa otentikasi ditolak, dan baik ekspor langsung maupun yang dialirkan lulus verifikasi independen terhadap 32 peristiwa sintetis.

### Pembaruan instalasi dan penerapan

Pemeriksaan penginstal, pengemasan, dan kesiapan yang difokuskan telah lulus **14 tes**, dengan satu pengabaian karena pembuatan tautan simbolik yang tidak tersedia. Pemeriksaan pembungkus asli mencakup jalur dengan spasi, penerusan argumen, mode pengaturan/demo, dan propagasi keluar bukan nol. Pemeriksaan Git Bash menguji helper shell Docker dengan daemon simulasi, termasuk Docker yang tidak ada, Compose yang tidak ada, kegagalan penantian kesehatan, dan pengaktifan port alternatif yang berhasil. Pemeriksaan simulasi ini tidak menjamin kompatibilitas runtime Docker.

Salinan sumber terbuka yang lengkap telah diinstal ke direktori Windows baru yang jalurnya mengandung spasi. `scripts\Setup.cmd` membuat lingkungan baru dan menginstal runtime yang disematkan; `Start.cmd --check --json` melaporkan siap tanpa membuat direktori data tujuannya. `pip check` lulus. Roda yang dibangun ulang juga lulus pemeriksaan paket terinstal, termasuk ekspor 32 peristiwa secara langsung dan melalui streaming.

Sintaks Shell dan lima berkas YAML alur kerja/Compose telah diurai. Konfigurasi Compose sumber dan gambar memiliki kesesuaian dalam pengaturan penyimpanan dan runtime. Pada tahap tersebut, seluruh 139 tautan lokal di 23 dokumen Markdown telah diselesaikan. Pilihan sumber publik berisi 99 berkas.

Definisi CI kini menerapkan konfigurasi asli terbaru pada Windows/Linux/macOS, pengaturan kesehatan/kontrol akses/persistensi Compose saat pembuatan ulang kontainer, serta konfigurasi Caddy. Alur kerja rilis mengharuskan publikasi lulus pemeriksaan tersebut dan menambahkan uji coba ARM64 yang diemulasi. Docker tidak tersedia di host ini: eksekusi Compose/Caddy yang sebenarnya, penerbitan sertifikat, eksekusi ARM64, serta alur kerja jarak jauh/publikasi paket masih belum terverifikasi secara lokal. Kode aplikasi/UI tidak berubah akibat pembaruan ini; hasil pengujian Python dan browser sebelumnya tidak dijalankan ulang.

## Versi 0.5.0

Seluruh rangkaian pengujian runtime yang disematkan berhasil dilalui: **81 lulus, 1 dilewati**, dalam waktu 22,00 detik, dengan peringatan Starlette yang sudah ada. Pemeriksaan izin POSIX dilewati pada Windows. Penguji handler baru mengirim pesan, pengeditan, penghapusan dalam lingkup/di luar lingkup, reaksi, pembaruan peserta, dan pesan layanan keanggotaan melalui berbagai kebijakan. Kategori yang dinonaktifkan tidak menghasilkan pengamatan langsung yang sesuai; diagnostik cakupan dan snapshot eksplisit tetap tersedia. Pengujian memverifikasi kebijakan yang dipertahankan, pemisahan ruang kerja, catatan audit sebelum/sesudah yang ditandatangani, perilaku kebijakan yang tidak berubah, validasi ketat, dan penyertakan dalam penerimaan proses berikutnya.

Uji masuk demo memastikan bahwa kemampuannya berbeda dari token panel yang dikonfigurasi, tidak dapat mengotorisasi ruang kerja aktif, tidak dapat mengubah pengaturan pengumpulan, dan tidak diterbitkan atau diterima untuk permintaan jarak jauh, diteruskan, lintas asal, atau Host yang tidak valid. Membuka demo yang tersimpan tanpa bendera demo eksplisit tidak mengaktifkan entri otomatis.

Uji penerimaan Chromium berhasil melewati **39 skenario**, termasuk akses demo lokal tanpa masukan token, pengaturan pemantauan, transisi dari pemilihan sumber ke kebijakan, kemandirian per akun, serta pemeriksaan tata letak desktop/320/390 piksel dan kontras teks. Tidak ada kesalahan JavaScript pada halaman. Permintaan yang disisipkan oleh AdGuard dari host tetap tercatat dalam log. Fixture HTTP unduhan mencatat reset koneksi setelah klien menutup koneksinya; asersi tetap lulus. Ini bukanlah hasil dari layanan langsung.

Peluncur standar telah memperbarui lingkungan terisolasi ke versi 0.5.0; versi sumber dan yang terinstal sudah sesuai, dan pemeriksaan pip berhasil. Enkripsi brankas rahasia yang ada, penolakan kunci yang salah/hilang, serta pemeriksaan integritas tanda tangan dan media berhasil dalam rangkaian pengujian lengkap. Tidak ada klaim enkripsi baru terhadap isi pesan atau lampiran oleh aplikasi.

Demo lokal dimulai ulang agar antarmuka pengguna (UI) yang diperbarui tersedia. Catatan sintetis yang ada tetap dipertahankan; menghentikan proses demo latar belakang yang lama akan menciptakan batas offline pada saat startup berikutnya. Tidak ada sesi Telegram yang sebenarnya yang digunakan untuk pemeriksaan ini.

Panel localhost:8787 yang sedang berjalan menampilkan versi 0.5.0, akses demo otomatis, lima kontrol pemantauan, dan 33 peristiwa jurnal sintetis yang disimpan. Wheel versi 0.5.0 yang diinstal secara terpisah menyajikan semua aset panel/panduan, menolak akses API yang tidak terotentikasi, dan menghasilkan ZIP berisi 32 peristiwa yang terverifikasi, baik secara langsung maupun melalui pembantu unduhan streaming. Versi paket runtime tetap dipertahankan sesuai yang tercatat untuk versi 0.4.

## Versi 0.4.0

Seluruh rangkaian pengujian runtime yang disematkan telah lulus: **78 lulus, 1 dilewati**, dalam waktu 19,77 detik. Pemeriksaan yang dilewati memerlukan izin POSIX; peringatan penghentian dukungan dari Starlette TestClient hulu tetap berlaku. Pengujian baru mencakup pengunduhan streaming/perutean ruang kerja, header otorisasi, penolakan untuk menimpa, pengalihan, respons terpotong, batas ukuran yang diiklankan/aktual, pembacaan terbatas, pembersihan, sistem berkas tanpa tautan keras, kegagalan kesiapan, dan mode peluncur yang tidak boleh menginstal paket. Uji ekspor memastikan keberadaan berkas sementara lokal di ruang kerja dan pembersihan berkas terlantar secara selektif.

Pengujian kompatibilitas Chromium berhasil melewati semua 36 skenario yang terdaftar tanpa kesalahan JavaScript pada halaman. Pengujian ini mencakup simulasi login melalui telepon/kode/2FA, sesi yang dikonversi, dua ruang kerja, serta rute/status terpisah, pengamatan, tanda tangan, titik pemeriksaan, dan permintaan cap waktu, ditambah:

- Tata letak desktop dan 320/390 piksel, tanpa tumpahan horizontal, navigasi yang terlihat, dan kolom login pertama berada dalam jendela tampilan awal seluas 844 piksel.
- Kontras teks pada latar belakang solid sesuai dengan ambang batas teks WCAG AA. Kontrol yang dinonaktifkan, opasitas, serta latar belakang gambar/gradien tidak termasuk; ini bukanlah audit WCAG yang lengkap.
- Respons ekspor lokal yang sebenarnya ditulis melalui pemilih/penulis berkas OS tiruan, diikuti dengan verifikasi ZIP independen; pembatalan tidak mengirimkan permintaan ekspor.
- Kegagalan penulisan akan membatalkan tujuan; fallback 128 MiB akan menolak respons yang diiklankan berukuran terlalu besar tanpa mengalokasikan muatan yang sesuai.
- Panduan lokal dalam bahasa Inggris untuk desktop dan kedua lebar layar sempit.

Dialog penyimpanan OS dan penulisan browser multi-gigabyte yang sebenarnya tidak diotomatisasi atau divalidasi. Uji unduhan Python menggunakan potongan data terbatas dan fixture loopback. Penerimaan penyebaran penuh dengan Telegram asli tetap terpisah.

Penginstal standar telah memperbarui `.venv` ke versi 0.4.0. Metadata sumber dan yang terinstal sesuai; `pip check` lulus. `python start.py --check --json` dilaporkan siap pada jalur sintetis baru tanpa membuat direktori data. Peringatan penyimpanan kunci lokalnya tetap muncul dengan benar: jurnal/media tidak dienkripsi oleh aplikasi.

Wheel versi 0.4.0 telah dibangun dan diinstal ke dalam direktori terpisah. Semua 23 berkas aplikasi cocok dengan sumber byte demi byte. Paket yang diinstal menampilkan panel dan panduan/aset berbahasa Inggris, menolak akses API yang tidak terotentikasi, dan mengekspor ZIP sintetis berisi 32 peristiwa yang lulus verifikasi. Perintah unduhan streaming-nya juga mengambil ZIP yang diverifikasi secara independen dari aplikasi yang sedang berjalan dan terinstal.

Dokumentasi publik dan panduan lokal tersedia dalam bahasa Inggris; tautan dokumentasi lokal dapat diakses. PowerShell mengurai templat tugas Windows dan Python mengurai berkas plist macOS. Ini adalah pemeriksaan sintaksis, bukan eksekusi layanan. Tidak ada tugas/layanan yang terdaftar. Konfigurasi CI kini mencakup pemeriksaan kesiapan, namun CI jarak jauh belum dijalankan di sini.

Pada eksekusi browser versi 0.4 yang dijalankan kembali, teramati injeksi AdGuard pada host dan OSError 10022 pada pembersihan soket asyncio Windows. Asersi browser lulus; pengamatan lingkungan ini dipertahankan alih-alih dianggap sebagai perilaku aplikasi yang tetap. Upaya awal sandbox OpenSSL/browser/pip gagal; uji coba yang berhasil menggunakan eksekusi yang disetujui di luar sandbox.

## Versi 0.3.1 berfokus pada perbaikan kesiapan

Pemeriksaan pada peluncur, bukti/penyimpanan, dan API yang terpengaruh berhasil: **31 lulus, 1 dilewati**, satu peringatan Starlette dari hulu. Pemeriksaan yang dilewati menguji izin direktori POSIX dan tidak dapat menetapkan izin tersebut pada host Windows ini. Pengujian Python versi lama mensimulasikan batas versi/impor; tidak ada interpreter Python 3.10 yang terinstal atau memenuhi syarat. Rangkaian pengujian 0.3 yang sebelumnya lulus dicatat di bawah ini; seluruh rangkaian pengujian dan skenario peramban tidak dijalankan ulang untuk perubahan-perubahan yang difokuskan ini.

Launcher standar telah memperbarui lingkungan lokal ke versi 0.3.1; metadata sumber dan yang terinstal sesuai, dan pemeriksaan pip berhasil. Wheel versi 0.3.1 yang diinstal secara terpisah melayani panel/aset, menolak akses API yang tidak terotentikasi, dan menghasilkan ekspor sintetis 32 peristiwa yang terverifikasi. YAML alur kerja berhasil diparsing, tetapi pemeriksaan runtime kontainer baru tidak dijalankan: tidak ada runtime Docker/Podman/Linux lokal yang dapat digunakan.

Lihat [temuan kesiapan](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) untuk kesenjangan yang tersisa terkait kegunaan, layanan langsung, dan platform. Patch ini tidak mendukung sistem operasi tambahan.

## Versi 0.3.0

Seluruh rangkaian pengujian runtime yang disematkan telah lulus: **61 tes**, dengan satu peringatan penghentian dukungan (deprecation) dari Starlette TestClient hulu. Metadata runtime melaporkan TgWitness 0.3.0 dan python-socks 2.8.2; pemeriksaan pip berhasil. Pengujian penerimaan browser berhasil tanpa kesalahan JavaScript pada halaman.

Wheel versi 0.3.0 telah dibangun dan diinstal ke dalam direktori paket terpisah. Wheel tersebut menyediakan panel dan aset, menolak permintaan API yang tidak terotentikasi, serta mengekspor jurnal sintetis berisi 32 peristiwa yang telah lulus verifikasi independen. Tautan dokumentasi lokal dapat diakses. Setelah koreksi normalisasi kunci mentah MTProxy, kesembilan uji koneksi/keamanan dijalankan ulang dengan sukses.

Liputan baru meliputi:

- Nama pengguna/kata sandi SOCKS5 dan HTTP CONNECT melalui server uji loopback yang sebenarnya; proksi yang konfigurasinya tidak aktif akan gagal daripada beralih ke tujuan.
- Validasi proxy, pemilihan transportasi MTProxy, penolakan rahasia TLS palsu, persistensi, isolasi ruang kerja, penolakan perubahan selama pemantauan, dan pengecualian rahasia dari status API dan peristiwa yang ditandatangani.
- Konversi read-only dari skema SQLite sintetis Telethon versi 7 dan 8; hash sumber tetap tidak berubah; penolakan terhadap format lain, tampilan SQL, dan file WAL yang belum diproses.
- Kunci utama brankas eksternal: kunci ruang kerja yang dihasilkan berbeda-beda, pembukaan ulang berhasil, penolakan jika kunci salah atau hilang, dan tidak ada migrasi implisit terhadap brankas lokal yang sudah ada.
- Pengaturan proxy browser, penghapusan kredensial, pengungkapan perlindungan penyimpanan, halaman koneksi seluler, otorisasi berkas sesi yang dikonversi, rute terpisah, serta semua skenario pengumpulan/ekspor yang telah dibahas sebelumnya menggunakan klien Telegram palsu.

Selama pengembangan, uji loopback menunggu tanpa batas waktu hingga peer dimatikan; pada uji coba lain, teramati reset koneksi Windows setelah proses handshake. Fixture kini membatasi seluruh pertukaran data dan menganggap EOF/reset setelah handshake selesai sebagai penutupan koneksi. Pemeriksaan handshake/otentikasi tetap diperlukan. Hal ini tidak mengindikasikan penyedia proxy yang sebenarnya atau menyiratkan adanya cacat tetap pada transportasi Telegram.

Pengamatan permintaan AdGuard yang dijelaskan di bawah ini masih berlaku. Tidak ada akun Telegram asli, proxy SOCKS/HTTP eksternal, atau server MTProxy yang aktif yang digunakan. MTProxy masih berada dalam tahap eksperimental dan opsi yang dipilih serta validasi rahasia telah diperiksa, bukan interoperabilitas langsung. Perintah konversi kunci eksternal dan sesi yang baru telah diuji hanya dengan rahasia sintetis. Linux/macOS/Docker masih belum memenuhi syarat di sini.

Pengukuran throughput versi 0.2 di bawah ini tidak diulang dan tidak boleh disajikan sebagai tolok ukur multi-akun/proksi baru untuk versi 0.3.

## Versi 0.2.0 dasar

Telah diuji pada Windows dengan Python 3.12.10. Tidak ada akun Telegram asli yang terhubung.

| Periksa | Hasil |
| --- | --- |
| Paket Python | 52 lulus di lingkungan pengembangan dan 52 lulus dengan runtime yang disematkan; satu peringatan penghentian dukungan Starlette TestClient dari hulu pada setiap eksekusi |
| Sintaks JavaScript | Dibuat menggunakan Node.js |
| Penerimaan Chromium | Lulus; tidak ada kesalahan JavaScript pada halaman |
| Tata letak desktop/seluler | Telah diperiksa pada resolusi 1440 × 1060 dan 390 × 844; tidak ada teks yang meluap secara horizontal |
| Isi pesan dalam format HTML | Ditampilkan sebagai teks; skrip yang disisipkan tidak dijalankan |
| Alur akun simulasi | Kredensial API → nomor telepon → kode → 2FA → pilih grup → mulai → ambil snapshot → jeda → muat ulang |
| Bukti di browser | Perbandingan suntingan, konten sebelumnya setelah penghapusan, filter, unduhan ZIP, titik pemeriksaan, tanda terima proses yang ditandatangani, unduhan permintaan RFC 3161, dan pengikatan titik pemeriksaan |
| Multi-akun | Jurnal, kunci, sumber, dan status real-time yang terpisah; berpindah browser tidak menghentikan pengumpul lainnya; ruang kerja terbuka kembali setelah restart; akun duplikat dan penugasan ulang akun ditolak |
| Kegagalan kriptografi | Bidang yang ditandatangani diubah, bidang yang tidak ditandatangani ditambahkan, kunci salah, anggota arsip rusak, media diubah/hilang, pemotongan yang terdeteksi oleh titik pemeriksaan ditolak |
| Penyimpanan | Penambahan data secara bersamaan memverifikasi; pemicu pembaruan/penghapusan ditolak; saat startup, sistem menolak jurnal yang telah diubah tanpa penambahan data dan melepaskan kuncinya |
| Ketahanan media | Penulisan pesan/tugas secara atomik; pemulihan setelah restart; deskriptor versi asli dipertahankan; penggantian antrian dan kerusakan berkas yang sudah ada ditolak; FloodWait dipertahankan; kegagalan sumber diisolasi |
| Streaming | Awalan yang stabil diekspor saat catatan baru ditambahkan; titik pemeriksaan yang disimpan mendeteksi jurnal yang terpotong; ekspor tidak merepresentasikan seluruh aliran peristiwa |
| RFC 3161 | OpenSSL 3.5.9 membaca permintaan yang dihasilkan; respons CA/TSA sintetis yang dihasilkan secara lokal diterima; data yang diubah, nonce, dan CA yang salah ditolak; lingkungan CA sekitar tidak menggantikan kepercayaan eksplisit |
| Pengaturan lokal | start.py --setup-only telah memperbarui .venv yang terisolasi ke versi 0.2.0; metadata sumber dan yang terinstal sesuai; pip check berhasil |
| Roda | Versi 0.2.0 telah dibangun dan diinstal secara terpisah di bawah direktori test-results; menyajikan panel/aset, menolak permintaan API yang tidak terotentikasi, mengekspor, dan memverifikasi arsip sintetis berisi 32 peristiwa |

Pengujian sumber menggunakan FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1, dan Playwright 1.62.0. Runtime yang ditetapkan menggunakan FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0, dan cryptography 50.0.2. deploy/constraints.txt mencatat versi runtime yang dikunci; deploy/requirements.lock dan deploy/build.lock menambahkan SHA-256 dari setiap berkas paket, dan Docker serta server dengan jaminan tinggi hanya menginstal dari berkas-berkas tersebut (pip --require-hashes). Keduanya juga bukan bukti kompatibilitas di setiap platform CI yang dikonfigurasi. CI jarak jauh belum dijalankan.

## Pengukuran kapasitas lokal sintetis

Perintah: `python tools/check_capacity.py --events 10000 --chats 100`

| Metrik | Teramati |
| --- | --- |
| Masukan | 10.000 peristiwa pesan sintetis dari 100 sumber sintetis yang dipilih |
| Teks pesan | 400 karakter; tanpa media atau jaringan |
| Pengambilan data | 53,273 detik; 187,7 peristiwa per detik |
| Latensi handler | p50 4,162 ms; p95 7,784 ms; maksimum 129,118 ms |
| Ekspor ZIP | 19,868 detik dengan tracemalloc diaktifkan |
| Alokasi ekspor Python yang dilacak pada puncaknya | 0,51 MiB; tidak memproses RSS |
| Ukuran ZIP | 4.610.962 byte |
| Verifikasi independen | Semua 10.000 peristiwa telah diverifikasi |

Pengukuran ini mencakup jalur perekaman/ekspor serial lokal pada host Windows ini. Pengukuran ini tidak mencakup pengiriman MTProto, akun bersamaan, pembatasan kecepatan Telegram, media, beban kerja jangka panjang, atau jumlah obrolan nyata yang dijamin. Pengukuran ini dilakukan sebelum alat cap waktu offline final, yang tidak mengubah jalur pesan yang diukur.

## Pengamatan lingkungan

Pembatasan sandbox Windows memblokir direktori sementara default pytest/pip serta subproses Playwright. Pytest menggunakan direktori sementara baru di dalam proyek; proses instalasi dan browser memerlukan eksekusi yang disetujui di luar sandbox.

AdGuard pada perangkat tersebut menyisipkan permintaan ke local.adguard.org ke dalam browser. Riwayat browser menyimpan permintaan-permintaan tersebut. Pengujian ini **bukanlah** bukti tidak adanya permintaan keluar dalam lingkungan browser yang tidak dimodifikasi; sumber aplikasi itu sendiri tidak mengandung permintaan aset eksternal/CDN/analitik. Pengaturan AdGuard tidak diubah.

Eksekusi browser terakhir juga mencatat OSError 10022 terkait pembersihan soket asyncio di Windows. Semua pengujian browser lulus dan tidak terjadi kesalahan JavaScript pada halaman. Penyebabnya belum teridentifikasi, dan eksekusi ini tidak menunjukkan tidak adanya masalah transportasi pada host.

Probe HTTP paket terinstal pertama yang menggunakan permintaan penutupan koneksi dari urllib mengalami reset koneksi, baik di dalam maupun di luar sandbox, serta dengan kedua set dependensi. Probe terakhir menggunakan koneksi persisten HTTP/1.1 standar melalui http.client dan berhasil. Permintaan browser juga berhasil. Asal mula pasti dari reset tersebut tidak dapat ditentukan; hal tersebut tidak dikategorikan sebagai cacat aplikasi yang tetap.

## Kualifikasi lainnya

Jurnal langsung yang disimpan ini mencatat pengumpulan yang sebenarnya, pengeditan, pemberitahuan penghapusan, lampiran, pemeriksaan ulang, dan penanganan batasan laju. Jurnal ini tidak mencatat pengiriman yang lengkap atau matriks terkontrol mengenai visibilitas peran, pihak yang bereaksi, FloodWait yang berkepanjangan, pemblokiran akun, dan pemulihan gangguan jaringan/proses. Penerbitan token QR tetap terpisah dari konfirmasi QR seluler yang telah diselesaikan.

Pembuatan/pengoperasian Docker, instalasi di Linux/macOS, beban tinggi yang berkelanjutan, tinjauan keamanan independen, tanggapan TSA yang benar-benar independen, validasi pencabutan/pengarsipan sertifikat, dan sertifikasi forensik tetap berada di luar kualifikasi yang tercatat. Penyimpanan status MTProto dan fitur catch-up telah diimplementasikan; replay atomik yang tahan lama masih belum terwujud. Pengumpulan log admin, daftar reaktor tambahan, dan polling singkat prioritas tetap menjadi fitur terpisah. Lihat [penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) untuk matriks kualifikasi terkontrol.

Tangkapan layar dan bukti transaksi lokal yang terperinci terdapat di bawah folder test-results/ (diabaikan oleh Git). Tangkapan layar publik di folder docs/assets/ hanya berisi data demonstrasi fiktif.

## Persiapan situs web publik dan publikasi · 27 Oktober 2026

Presentasi `website/` dan build Pages yang terpisah ditambahkan setelah pemeriksaan panel di atas. Tidak ada konfigurasi akun langsung atau logika pengumpulan data yang diubah.

- Rangkaian aplikasi yang ada lulus: 138 lulus, 1 dilewati (hanya POSIX), dan satu peringatan deprecation dari Starlette/httpx hulu. Sebanyak 11 uji pembangunan situs yang ditambahkan lulus secara independen, termasuk penolakan output tak terduga dan penolakan input tertaut.
- Kedua skrip browser aplikasi berhasil dijalankan menggunakan project-venv Playwright dan Chromium headless shell 156. Tidak ada kesalahan JavaScript pada halaman atau permintaan eksternal yang tercatat. Semua skenario akun menggunakan transportasi palsu dan data fiktif.
- `tools/check_site.py` lulus pada lebar 320, 390, 768, 1024, dan 1440, dengan subjalur URL proyek, tab keyboard, akses clipboard yang berhasil/ditolak, gerakan yang dikurangi, dan JavaScript yang dinonaktifkan. Tidak terjadi permintaan aset atau permintaan eksternal yang gagal.
- `tools/build_site.py` menghasilkan 10 berkas publik yang masuk daftar putih, dengan total sekitar 460 KB. Tangkapan layar browser dan tanda terima terdapat di `test-results/site/` yang diabaikan.
- Wheel berhasil dibuat setelah menginstal alat setuptools/wheel yang hanya untuk pembuatan di lingkungan proyek. Pemasangannya ke target terisolasi dan pengujian dengan perintah ``tools/check_install.py`` berhasil: aset statis, kontrol akses, ekspor sintetis berisi 32 peristiwa yang ditandatangani, serta unduhan streaming yang diverifikasi secara independen.
- `pip check` lulus. Pemindaian pola terhadap kandidat publik yang dipilih dari Git tidak menemukan blok kunci pribadi yang dapat dikenali, token GitHub/bot/AWS, penugasan rahasia literal panjang, atau penanda konflik penggabungan. Ini bukan bukti bahwa setiap format rahasia yang mungkin tidak ada. Pemeriksaan data runtime/sesi/kunci diabaikan oleh Git.
- Otentikasi GitHub CLI tidak valid; tidak ada remote yang dikonfigurasi dan tidak ada commit awal. Tidak ada push, alur kerja yang dihosting, penyebaran Pages, atau rilis yang dilakukan. Docker dan kualifikasi Telegram/platform langsung tetap berada di luar cakupan pemeriksaan ini.

Di host ini, penguncian unduhan Playwright gagal pada sistem berkas ruang kerja E:. Pemasangan Chromium di bawah `%LOCALAPPDATA%/tgwitness-playwright` dan penggunaan `PLAYWRIGHT_BROWSERS_PATH` yang sama untuk pemeriksaan berhasil. Ini merupakan solusi sementara pada lingkungan, bukan perubahan pada dependensi runtime aplikasi.

## Dokumentasi interaktif dan metadata situs web · 29 Oktober 2026

Situs publik ini terdiri dari 12 halaman HTML berbahasa Inggris: halaman beranda, indeks panduan, dan sepuluh panduan. Artefak ini berisi 28 berkas presentasi yang tercantum secara eksplisit, sekitar 1,85 MB, dan tidak ada data pengumpul. Situs web publik ini berbahasa Inggris; terjemahan aplikasi dan panduan repositori yang diterjemahkan disimpan secara terpisah.

- Pengujian situs, publikasi sumber, dan batas rilis: **18 lulus, 2 dilewati**. Pengabaian tersebut berkaitan dengan pembuatan symlink pada sistem berkas Windows ini. Pengujian memeriksa metadata halaman unik, halaman publik berbahasa Inggris saja, URL kanonik, semua entri peta situs, aset/tautan lokal, navigasi terstruktur, dan pengecualian berkas pribadi.
- Baik `tools/check_site.py` maupun `tools/check_docs_site.py` lulus pengujian di Chromium pada resolusi 320, 390, 768, 1024, dan 1440 piksel di bawah subjalur URL proyek. Pemeriksaan panduan ini mencakup seluruh 11 halaman dokumentasi, navigasi pencarian dan keyboard, keberhasilan/kegagalan clipboard, serta konten yang dapat dibaca tanpa JavaScript.
- Lima contoh interaktif telah lulus uji: pemutaran/langkah demi langkah/jeda/reset pesan dengan gerakan yang diperlambat dan penangguhan di luar layar; rantai hash asli/yang diubah/yang dibangun ulang/yang terpotong; keputusan penerimaan/pembatalan/pembelahan/tidak ada respons dari saksi; serta skenario pengiriman lengkap/tertunda/hilang; dan peta investigasi yang menghubungkan pengamatan lintas obrolan fiktif berdasarkan ID pengirim, tujuan, dan hash lampiran . Kontrol investigasi lulus pemeriksaan navigasi keyboard dan pemeriksaan fallback tanpa JavaScript . Hasil SHA-256 browser dibandingkan secara independen dengan `hashlib` Python dan JSON kanonik. Contoh hash tersebut juga mempertahankan fallback yang dapat dibaca saat Web Crypto tidak tersedia.
- Rasio penyampaian dan penanda grafik disesuaikan dengan tabel yang mudah diakses. Label sumbu versi seluler diperbesar setelah peninjauan visual. Setiap contoh diberi label sebagai ilustrasi atau sintetis, dan tidak ada contoh peramban yang menghubungi Telegram.
- Tidak ada permintaan eksternal, permintaan HTTP yang gagal, atau kesalahan JavaScript yang tercatat. Tangkapan layar desktop/seluler dan bukti transaksi diabaikan di `test-results/site/` dan `test-results/docs-site/`. Indeks dokumentasi, contoh pesan/hash, tata letak saksi, bagan pengiriman, dan peta investigasi telah diperiksa pada ukuran desktop/seluler.
- Pemindaian publikasi telah lulus untuk 282 berkas sumber publik dan 1.426 tautan dokumentasi lokal. Ruff telah lulus untuk alat dan pengujian situs Python yang dimodifikasi.
- `docs/HOW-IT-WORKS.md` menyediakan panduan Markdown GitHub yang dilengkapi dengan diagram dan rumus Mermaid . `docs/INVESTIGATION.md` mencakup cakupan seluruh akun, pengumpulan riwayat per obrolan, profil pengguna, referensi lintas obrolan, garis waktu , serta penyerahan kasus yang terverifikasi. Langkah-langkah dan batasannya telah diverifikasi berdasarkan ruang lingkup, pengumpulan data, berkas, ekspor, verifikator, dan kode panel saat ini. Rendering yang dihosting di GitHub belum diverifikasi.

Ini adalah pemeriksaan situs web/dokumentasi lokal. Pemeriksaan ini tidak menambahkan kualifikasi Telegram secara langsung atau menetapkan penerapan Pages yang dihosting, keberhasilan CI jarak jauh, atau pengindeksan mesin pencari. Lihat [prosedur penerbitan](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) dan [catatan metadata situs web](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
