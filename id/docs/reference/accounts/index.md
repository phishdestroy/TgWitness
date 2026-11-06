# Format akun dan sesi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/

Masuk menggunakan nomor telepon, kode QR, atau kunci otentikasi, impor sesi Telethon, Pyrogram, atau Telegram Desktop, dan kelola beberapa akun.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Memulai](https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/)

![Memulai](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness masuk sebagai **akun pengguna Telegram** (bukan bot) melalui MTProto, menggunakan Telethon. Setiap akun berada di **ruang** kerja tersendiri (disebut *workspace* dalam API dan alat baris perintah) dengan sesi, sumber, jurnal, dan kunci penandatanganan tersendiri.

Berkas sesi, string sesi, dan Kunci Otentikasi merupakan **otorisasi akun**: siapa pun yang memilikinya dapat bertindak sebagai akun tersebut. Ketiganya tidak berisi riwayat pesan.

> [!PERINGATAN] **Jangan gunakan apa pun yang tidak boleh hilang.** Kami sangat menyarankan agar Anda tidak menghubungkan akun pribadi atau akun berharga lainnya, serta tidak membuat ID API / hash API pada akun yang Anda hargai. Ini bukan soal TgWitness belum teruji: Telegram membatasi dan memblokir akun secara permanen tanpa peringatan — untuk volume permintaan yang dianggapnya berlebihan, terlepas dari klien atau tujuannya, tanpa dokumentasi yang memadai. Banyak pemblokiran tidak dapat dibatalkan. Gunakan akun khusus. Kelancaran uji coba bergantung pada Telegram, bukan pada perangkat lunak, dan tidak menjamin apa pun untuk masa mendatang.

- [Sekilas](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#at-a-glance)
- [Sebelum memulai: ID API dan hash API](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Nomor telepon](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#phone-number) · [Kode QR](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#qr-code) · [Kunci Otentikasi + ID DC](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#auth-key--dc-id)
- [Berkas akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#pyrogram-session) · [Pasangan sesi + JSON](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#telethon-stringsession) · [JSON Akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-json)
- [Identifikasi apa yang Anda miliki](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#identify-what-you-have) · [Format yang tidak didukung](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#unsupported-formats)
- [Beberapa akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#multiple-accounts) · [Menjaga keamanan berkas akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#keeping-account-files-safe) · [Pemecahan Masalah](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#troubleshooting)

## Sekilas

| Apa yang Anda miliki | Tab di **Tambahkan akun** | Anda juga akan memerlukan |
| --- | --- | --- |
| Nomor telepon dan akses ke kode login-nya | **Telepon** | Kata sandi 2FA jika diaktifkan |
| Telegram terbuka di perangkat lain | **Kode QR** | Kata sandi 2FA jika diaktifkan |
| Berkas `.session` (Telethon atau Pyrogram) | **Berkas** | Berkas JSON pelengkap opsional untuk pengaturan aplikasi |
| `.session` + `.json` dengan nama yang sama | **Berkas** (pilih keduanya) | Biasanya tidak ada yang lain |
| Folder `tdata` di Telegram Desktop | **Berkas** (dalam format ZIP) | Kode sandi lokal Desktop, jika ada yang ditetapkan |
| Sebuah Telethon StringSession (teks, `.txt`, `.tgwitness-session`) | **Berkas** | Tidak diperlukan pasangan API terpisah |
| `.json` dengan sesi atau Kunci Otentikasi | **Berkas** | Tidak diperlukan pasangan API terpisah |
| Kunci Otentikasi (512 karakter heksadesimal) dan nomor DC-nya | **Kunci otentikasi** | ID Pengguna (opsional) |

TgWitness mengenali berkas berdasarkan **isinya**, bukan namanya. Mengganti nama berkas tidak akan mengubah isinya.

## Sebelum memulai: ID API dan hash API

Anda dapat masuk tanpa membuat aplikasi API Telegram. Jika tidak ada pasangan yang dimasukkan, diimpor, atau sudah disimpan di ruang kerja, TgWitness memilih pasangan dari kumpulan bawaan pasangan API publik 50 (`tgwitness/api_pool.py`), dengan memprioritaskan Telegram Desktop untuk login baru dan mempertahankan pasangan yang sudah disimpan terlebih dahulu; kandidat yang tersisa diacak. Jika Telegram menolak sebuah pasangan (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), pasangan berikutnya akan dicoba, hingga delapan kali per proses masuk; pasangan yang ditolak dilewati hingga aplikasi di-restart. Pasangan yang digunakan untuk masuk disimpan bersama akun dan digunakan kembali untuk akun tersebut. Sebuah **API ID** dan **API hash** mengidentifikasi aplikasi kepada Telegram; keduanya tidak mengotorisasi akun secara mandiri.

Bidang koneksi yang hilang menggunakan pasangan perangkat/OS yang deterministik dari katalog [opentele2 2.0.0 yang disertakan](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, dan Web `2496`. ID build sumber Android `4` juga menggunakan katalog Android, sebagaimana diidentifikasi dalam [BuildVars Telegram Android](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web secara default menggunakan A; sufiks versi aplikasi yang diimpor `K` atau paket bahasa `macos` memilih K, dan versi `0.7.0` memilih Webogram. ID aplikasi yang tidak dikenal mempertahankan pengaturan default host Telethon. Bidang yang diimpor selalu diutamakan, termasuk versi aplikasi yang lebih lama dan paket bahasa yang kosong. Katalog tidak pernah mengubah ID/hash API. Cuplikan versinya ditinjau secara eksplisit, bukan diambil saat login. Profil yang disimpan tetap stabil setelah pembaruan.

`account.getAuthorizations` melaporkan metadata otorisasi Telegram yang tersimpan; ini bukanlah duplikat dari setiap `initConnection` baru. Bandingkan dengan profil yang sebenarnya dikirim. Menghubungkan otorisasi yang sudah ada tidak memvalidasi hash API yang menyertainya: `initConnection` mengirimkan ID API, sedangkan hash digunakan oleh permintaan login.

Setelah otorisasi ponsel baru atau QR, TgWitness meminta konfigurasi, DC terdekat, status online, bahasa (jika paket bahasa tidak kosong), pembaruan aplikasi, dan pembaruan syarat layanan, dengan jeda 0.3–1.5 detik antar permintaan. Pembaruan status menandai akun sebagai online untuk sementara. Urutan ini dijalankan sekali saat proses masuk selesai, bukan saat impor, koneksi ulang, atau restart. Otorisasi disimpan terlebih dahulu; permintaan yang gagal akan menghentikan urutan tanpa mencoba ulang atau membatalkan proses masuk. Hasilnya dicatat sebagai `account.initialized`, dengan nama kesalahan alih-alih isi respons. Urutan ini bukan jaminan terhadap pembatasan akun.

Untuk `tdesktop` , jika `tz_offset` tidak ada, maka digunakan offset UTC lokal server, dibulatkan ke 900 detik menggunakan algoritma [opentele2](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; lisensi di `tgwitness/client_profiles.LICENSE` ). Nilai ini diperbarui pada setiap koneksi sehingga perubahan waktu musim panas tercermin. `tz_offset` yang diimpor memiliki prioritas di setiap platform dan dipertahankan persis seperti aslinya, termasuk nilai nol. Entri `initConnection.params` lainnya tetap dipertahankan. Formulir masuk HTTP menerima zona waktu numerik yang dikembalikan oleh impor berkas; nilai boolean, pecahan, dan offset di luar rentang yang didukung akan ditolak.

Rute langsung, SOCKS5, dan HTTP CONNECT menggunakan `ConnectionTcpObfuscated` (MTProto yang disingkat dan dikaburkan) dari Telethon. HTTPS CONNECT mempertahankan TLS ke proxy dan menggunakan transportasi yang disamarkan yang sama di dalam terowongan. MTProxy mempertahankan transportasi perantara acak dan penanganan rahasia yang diwajibkan. Pergantian rute menerapkan pilihan yang sama. Pengaburan mengubah pembingkaian paket; hal ini tidak menyembunyikan akun atau metadata kliennya dari Telegram atau menyiratkan kekebalan terhadap pembatasan.

Setelah menghubungkan klien yang berwenang, TgWitness memeriksa konfigurasi, DC terdekat, otorisasi saat ini, baseline lapisan yang telah ditinjau, bahasa, pembaruan aplikasi, dan pembaruan syarat layanan. Diagnostik ini dijalankan sekali per instance klien, sebelum pengumpulan data, dan ditampilkan di bawah detail koneksi beserta waktunya. `account.connection_checked`merekam hasil tanpa hash sesi, alamat IP, token, atau hash API. Mereka tidak pernah menerima persyaratan atau menginstal pembaruan. Kegagalan permintaan atau FloodWait menghentikan permintaan berikutnya; hasil yang hilang tetap tidak diketahui. Pemeriksaan lokal masih dapat melaporkan hasilnya sementara pemeriksaan jaringan dilewati.

Diagnostik FloodWait menyimpan metode TL yang gagal, pembungkus Takeout/range apa pun, penundaan yang diminta server, dan batas waktu efektif di `telegram.backoff`. Rincian koneksi menampilkan metode dan batas waktu saat permintaan ditangguhkan. Diagnostik ini mencakup penghitung panggilan klien per metode sejak klien tersebut dibuat; penghitung ini menghitung resolusi peer bersarang secara terpisah, tetapi tidak menghitung paket atau upaya percobaan ulang internal Telethon. Penghitung saat ini juga tersedia sebagai `collector.rpc_activity` di API status. Tidak ada argumen permintaan, nama pengguna, hash akses, atau teks pengecualian yang disertakan. Diagnostik terakhir dan batas waktu penuh tetap ada setelah restart. Penundaan sebelumnya tanpa catatan metode tidak dapat diatribusikan secara retrospektif. Lihat batas ekspor  untuk tinjauan sumber dan perbedaan antara penemuan dan perolehan riwayat.

`official_app=True` atau `False` adalah bendera otorisasi saat ini dari Telegram. Tidak ada satu pun nilai tersebut yang menentukan apakah akun tersebut dibatasi, tepercaya, atau sedang dalam pengamatan. Snapshot mode bukti `account.devices` yang ada tetap mencatat riwayat semua perangkat yang masuk; diagnostik koneksi hanya menyimpan deskripsi perangkat saat ini.

Sebelum koneksi, pemeriksaan penasihat membandingkan platform API, paket bahasa, format perangkat/OS dan versi aplikasi, pengaturan wilayah sistem seluler, serta lapisan skema aktual Telethon dengan dasar katalog yang telah ditinjau. Peringatan muncul di log server dan metadata status akun; peringatan tersebut tidak pernah menggantikan nilai yang diimpor atau mengubah lapisan skema. Lapisan yang berbeda merupakan sinyal tinjauan kompatibilitas, bukan bukti adanya akun yang rusak atau dibatasi. Pemeriksaan ini dan `official_app` tidak menjamin bahwa Telegram menganggap akun tersebut aman dari pembatasan. Status akun yang terputus menggunakan profil yang tersimpan alih-alih menghasilkan deskripsi perangkat lain.

Untuk menggunakan aplikasi Anda sendiri sebagai gantinya (akun yang mendaftarkannya adalah yang berisiko; lihat [Mengapa menggunakan kumpulan API bawaan?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. Buka [my.telegram.org](https://my.telegram.org) dan masuk menggunakan nomor telepon apa pun yang Anda miliki. Kode verifikasi akan dikirimkan melalui aplikasi Telegram, bukan melalui SMS.
2. Pilih **alat pengembangan API**.
3. Buat aplikasi: judul dan nama pendek apa saja (5–32 huruf), platform **Desktop**. URL dan deskripsi dapat dikosongkan.
4. Salin **App api_id** (sebuah angka) dan **App api_hash** (32 karakter heksadesimal).

Di panel, buka bagian **API ID + Hash** di bawah formulir masuk. Anda dapat menempelkan satu pasangan `api_id:api_hash` ke kolom **API ID**, dan kedua kolom tersebut akan terisi otomatis. Satu pasangan dapat digunakan untuk semua akun Anda. Setelah login berhasil, data tersebut disimpan dalam bentuk terenkripsi, hanya di ruang kerja tersebut, dan tidak pernah dikirim kembali ke browser.

Terdapat tiga jenis kredensial yang terlibat:

| Rahasia | Buka | Lokasi |
| --- | --- | --- |
| Token panel | Panel web TgWitness | `panel-token.txt` di direktori data, atau `TGWITNESS_TOKEN` |
| ID API + hash | Tidak ada yang berdiri sendiri; mengidentifikasi aplikasi tersebut | Pasangan bawaan, pengaturan yang diimpor, atau aplikasi Anda sendiri di my.telegram.org |
| Otorisasi akun | Akun Telegram | Dibuat melalui login via telepon/QR atau dimasukkan sebagai sesi |

Jika Telegram harus diakses melalui proxy, atur terlebih dahulu di **Akun → Pengaturan → Pengaturan koneksi → Ubah rute koneksi**.

## Nomor telepon

1. Buka **Akun**, pilih tab **Telepon**, lalu masukkan nomor dalam format internasional, misalnya `+44 7700 900123`. Spasi dan tanda hubung akan dihapus secara otomatis.
2. Tekan **Lanjutkan**. Kolom API ID + Hash dapat dibiarkan kosong.
3. Masukkan kode yang dikirimkan oleh Telegram (biasanya ke aplikasi Telegram; pengiriman melalui SMS tidak dijamin).
4. Jika akun tersebut memiliki verifikasi dua langkah, masukkan kata sandi tersebut. Ini bukanlah token panel maupun kode sandi perangkat.
5. Periksa ID akun yang ditampilkan setelah masuk, lalu pilih sumber.

Kode login dan kata sandi 2FA tidak pernah disimpan ke disk.

## Kode QR

Gunakan ini jika akun sudah masuk (login) di ponsel atau komputer lain.

1. Tab **Kode QR** → **Tampilkan kode QR**. Kolom API ID + Hash dapat dibiarkan kosong.
2. Pada perangkat yang sudah masuk: **Pengaturan → Perangkat → Hubungkan Perangkat Desktop**, pindai kode dan konfirmasi.
3. Masukkan kata sandi 2FA di TgWitness jika Telegram memintanya.

Gambar QR dihasilkan secara lokal. Kode memiliki masa berlaku; tekan "**Buat kode QR lain"** untuk mencoba lagi. Mengunci panel, berpindah ruang kerja, atau memulai sesi login baru akan membatalkan kode yang sedang diproses.

## Kunci Otentikasi + ID DC

Kunci Otorisasi (Auth Key) adalah otorisasi mentah berukuran 256 byte yang mendasari setiap sesi Telegram, ditulis dalam bentuk **512 karakter heksadesimal**, bersama dengan nomor pusat data **DC 1–5**.

1. Tab **Kunci Otentikasi**. Tempelkan kunci secara lengkap; kunci yang dipersingkat yang mengandung `…` tidak akan berfungsi.
2. Pilih DC ID yang disertakan bersama kunci tersebut.
3. Masukkan **ID Pengguna** (opsional). TgWitness kemudian akan menolak terhubung jika Telegram melaporkan akun yang berbeda.
4. **Akun** Press **Connect**.

Kunci Otentikasi (512 karakter) bukanlah hash API (32 karakter). Kunci yang sama juga dapat diimpor sebagai JSON, lihat [JSON Akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-json).

## Berkas akun

Buka **Tambahkan akun → File** dan pilih hingga **empat file yang terkait dengan satu akun**, dengan total ukuran **8 MiB**, lalu tekan **Hubungkan akun**.

Formulir **Files**, **Auth key**, dan formulir impor massal menampilkan peringatan sesi paralel sebelum terhubung. Secara default, otorisasi yang diimpor akan digunakan kembali. Biarkan klien asli tetap tertutup selama kuncinya digunakan di sini. **Files** dan **Auth key** juga menawarkan **Buat otorisasi independen**, yang dijelaskan di bawah ini. Impor massal masih menggunakan mode langsung. Masuk melalui telepon dan QR interaktif membuat otorisasi terpisah. Judul peringatan tetap terlihat di formulir impor; penjelasan lengkapnya terbuka secara otomatis saat file atau string kunci/sesi disediakan. Peringatan ini dapat ditutup setelah dibaca, sehingga pemilih file dan kontrol koneksi tetap dapat digunakan di ponsel.

- File dikonversi **di memori** pada server TgWitness Anda. Unggahan tidak disimpan, file ZIP tidak diekstrak ke disk, dan tidak ada layanan eksternal yang dihubungi.
- Sesi yang dihasilkan kemudian diverifikasi dengan Telegram. Jika sebuah berkas mencantumkan ID pengguna, ID tersebut harus sesuai dengan akun yang dilaporkan oleh Telegram.
- Berkas yang mendeskripsikan akun yang berbeda atau kredensial API yang berbeda akan ditolak daripada memilih salah satunya.
- **Kolom "Passcode" atau "session text"** berisi bidang "TData local passcode", sebuah kotak untuk menempelkan StringSession dan **membaca berkas tanpa perlu masuk** (mengisi formulir tanpa menghubungi Telegram).

### Buat otorisasi independen

Pilih **Buat otorisasi independen** sebelum menghubungkan berkas yang diimpor atau Kunci Otorisasi. TgWitness menghubungkan donor yang diimpor sebentar, menggunakannya untuk menyetujui token login QR klien baru, dan memutuskan koneksi donor segera setelah persetujuan. Klien baru memiliki kunci otorisasi sendiri dan profil Desktop yang dipilih secara terpisah. Kredensial API dan profil perangkat yang disediakan oleh donor hanya digunakan untuk koneksi donor. Tidak ada otorisasi yang ada yang dicabut atau dibatalkan.

**Pastikan klien asli pemberi tetap tertutup sepenuhnya selama langkah ini.** Koneksi awal masih menggunakan kunci yang disalin, sehingga mode ini tidak dapat menghilangkan risiko penggunaan paralel awal tersebut. Setelah otorisasi baru terhubung, pemilik dapat membuka kembali klien asli dan menggunakan keduanya secara independen. Login interaktif **kode QR** memungkinkan klien asli menyetujui login tanpa menyalin atau menghubungkan kuncinya di sini.

Jika Telegram meminta 2FA, mode ini menggunakan `twoFA` dari JSON yang dipilih jika tersedia, atau meminta kata sandi. Kata sandi yang diimpor dan ditolak akan kembali ke formulir kata sandi. Kata sandi tidak disimpan. Kunci kandidat disimpan dalam bentuk terenkripsi di `independent_login.enc`, termasuk perubahan selama migrasi pusat data. Setelah terjadi gangguan, pilih donor yang sama dan opsi ini untuk melanjutkan kunci kandidat yang tersimpan. Ruang kerja tetap dicadangkan untuk akun tersebut; kegagalan penyelesaian tidak akan menghapus ruang kerja baru tersebut. Simpan direktori datanya dan kunci brankasnya. Kredensial akhir dan catatan jurnal `account.authorized` mencakup metode impor, format input, dan ID API donor, tanpa kunci atau kata sandi donor.

Pada 5 November 2026, sebuah akun khusus lulus pemeriksaan langsung dengan donatur Telethon, Pyrogram, dan TData: penyelesaian 2FA, kunci otorisasi baru yang berbeda, akses bersamaan oleh donatur dan klien baru, serta membaca saluran publik. Kasus Telethon juga melanjutkan kandidat yang disimpan setelah terjadi gangguan pada langkah kata sandi. Setiap otorisasi baru menyelesaikan enam permintaan inisialisasi pasca-login, dan jurnalnya yang ditandatangani terverifikasi. Sesi asli tetap dapat digunakan dalam keempat format yang disediakan.

Basis data kesalahan [RPC Telegram](https://core.telegram.org/api/errors.json) mengaitkan `FRESH_CHANGE_ADMINS_FORBIDDEN` dengan pergantian admin, `FRESH_CHANGE_PHONE_FORBIDDEN` dengan perubahan nomor telepon, dan `FRESH_RESET_AUTHORISATION_FORBIDDEN` dengan pencabutan sesi lain, perubahan masa berlakunya, atau pendaftaran kunci akses. `SESSION_TOO_FRESH_*` dan `PASSWORD_TOO_FRESH_*` berkaitan dengan pengalihan kepemilikan serta penarikan pendapatan atau hadiah. Ini bukanlah operasi pengumpulan; login baru tidak berarti larangan pembacaan selama 24 jam secara menyeluruh. Ekspor dapat secara terpisah mengembalikan `TAKEOUT_INIT_DELAY_*`. TgWitness mempertahankan jeda yang diminta server dan tidak mencoba kembali penerimaan token secara otomatis atau mencabut sesi untuk mengatasi pembatasan.

### Telethon `.session`

|  |  |
| --- | --- |
| Apa itu | Basis data SQLite yang dibuat oleh alat berbasis Telethon, misalnya `my_account.session` |
| Diakui oleh | Tabel `sessions` (bersama dengan `dc_id`, `server_address`, `port`, `auth_key`) dan `version` = 7 atau 8 |
| Persyaratan | Tepat satu baris sesi yang diotorisasi; basis data yang tertutup dan lengkap |

Tutup terlebih dahulu program yang membuat berkas tersebut. Jika terdapat `my_account.session-journal` atau `my_account.session-wal` di sampingnya, berarti basis data belum diselesaikan: buka dan tutup klien aslinya dengan benar. Menghapus berkas-berkas sidecar tersebut dapat meninggalkan salinan yang rusak.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Apa itu | Alat berbasis Pyrogram yang menggunakan basis data SQLite |
| Diakui oleh | Tabel `sessions` dengan `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 atau 3 |
| Persyaratan | Satu sesi **pengguna** yang berwenang di jaringan produksi. Sesi bot dan test-DC ditolak |

ID pengguna yang disimpan akan diverifikasi dengan Telegram saat login.

### Pasangan sesi + JSON

Akun sering kali didistribusikan dalam bentuk dua berkas dengan nama yang sama, misalnya `447700900123.session` dan `447700900123.json`. Pilih **keduanya** sekaligus.

- Dari JSON, TgWitness menggunakan `app_id`/`api_id` dan `app_hash`/`api_hash`, sehingga Anda biasanya tidak perlu memasukkan kredensial API.
- Profil koneksi menggunakan `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack`, dan `tz_offset` opsional (detik dari UTC, -43200 hingga 50400). Bidang yang diisi memiliki prioritas lebih tinggi daripada nilai default yang dihasilkan dan bahasa panel/browser . Alias yang bertentangan akan ditolak. Profil yang telah diselesaikan disimpan dalam kredensial ruang kerja terenkripsi dan digunakan kembali setelah restart, termasuk versi aplikasinya.
- `phone`, pengaturan proxy, dan token perangkat di**abaikan**. `twoFA` bersifat hanya baca ketika **Buat otorisasi independen** dipilih; impor langsung mengabaikannya.
- JSON tanpa bidang otorisasi yang didukung hanyalah metadata. Tambahkan berkas sesi atau lanjutkan dengan login melalui telepon atau QR. JSON yang berisi sesi yang didukung atau Kunci Otorisasi dapat melakukan otorisasi secara mandiri; lihat [Account JSON](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData adalah folder `tdata` dari aplikasi Telegram Desktop (aplikasi lintas platform dari desktop.telegram.org).

| Sistem | Lokasi default `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portabel: di sebelah `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Untuk mengimpornya:

> **Peringatan sesi paralel.** Impor TData langsung menggunakan kembali kunci otorisasi Telegram Desktop. Jangan gunakan kunci tersebut di Desktop dan TgWitness secara bersamaan. Telegram dapat membatalkan otorisasi tersebut dengan `AUTH_KEY_DUPLICATED`, sehingga kedua salinan menjadi tidak dapat digunakan hingga login baru dilakukan.
>
>
>
> Tutup Desktop sepenuhnya, termasuk proses tray-nya, dan biarkan salinan tersebut tetap tertutup saat TgWitness menggunakan sesi yang diimpor. **Tutup, jangan logout atau mencabut sesi:** pencabutan juga akan membatalkan salinan yang diimpor. Jika Anda memerlukan kedua klien berjalan, pilih **Buat otorisasi independen** dan biarkan Desktop tetap tertutup hingga login baru berhasil, atau masuk ke TgWitness melalui telepon atau QR. Akun khusus disarankan, tetapi tidak menjamin keamanan kunci kloning untuk digunakan secara paralel.
>
>
>
> Hal ini juga berlaku untuk berkas yang diimpor `.session` , teks StringSession, dan Auth Key HEX. Klien lain dengan otorisasi yang dibuat secara mandiri dapat tetap masuk. Lihat [dokumentasi AUTH_KEY_DUPLICATED dari Telegram](https://core.telegram.org/api/errors#406-not-acceptable).

1. Keluar sepenuhnya dari Telegram Desktop.
2. Buatlah berkas ZIP yang **hanya** berisi dua item berikut dari `tdata`:

   - `key_datas`
   - file berhuruf 16 yang berakhiran `s` di sebelahnya, biasanya `D877F783D5D3EF8Cs`

   Mengompres seluruh folder beserta cache medianya biasanya melebihi batas (512 entri, 32 MiB setelah diekstrak). 3. Pilih berkas ZIP di bagian "**Files**". Jika Telegram Desktop memiliki **kode sandi lokal**, masukkan kode tersebut di kolom **"Passcode" atau "session text"** terlebih dahulu. Ini bukanlah kata sandi 2FA.

Didukung: satu akun per arsip, penyimpanan modern `key_datas`/`key_data0`/`key_data1`, kode sandi lokal. Tidak didukung: folder dengan beberapa akun yang masuk, tata letak Desktop versi lama, file ZIP yang dilindungi kata sandi, dan aplikasi asli macOS terpisah "Telegram for macOS".

### Telethon StringSession

Satu baris teks, biasanya dimulai dengan `1` dan panjangnya sekitar 350 karakter. Unggah berkas tersebut sebagai berkas `.txt` atau `.tgwitness-session` (maksimal 4 KiB), atau tempelkan di bawah **kolom Kode Akses atau teks sesi**. Hanya string Telethon yang diterima; string Pyrogram dan TDLib menggunakan format yang berbeda.

### JSON Akun

Satu objek JSON, maksimal **64 KiB**, dalam berkas dengan ekstensi **`.json`**.

| Bidang (alias) | Arti |
| --- | --- |
| `api_id` (`app_id`) | ID Aplikasi, sebuah bilangan positif |
| `api_hash` (`app_hash`) | Hash aplikasi, 32 karakter heksadesimal |
| `string_session` (`session_string`, `session_str`; `session` versi lama) | Teks Telethon StringSession, bukan nama file |
| `auth_key` (`auth_key_hex`) + `dc_id` | Kunci Otentikasi (Auth Key) lengkap berpanjang 512 karakter dan DC 1–5 |
| `user_id` (`id`) | Opsional; diverifikasi dengan Telegram sebelum otorisasi disimpan |
| `device_model` (`device`) | Deskripsi perangkat koneksi |
| `system_version` (`sdk`) | Versi OS koneksi |
| `app_version` | Versi aplikasi yang dikirim ke Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Bahasa klien, bahasa sistem, dan paket bahasa klien; nilai kosong untuk `lang_pack` diperbolehkan |
| `tz_offset` | Offset UTC opsional dalam detik, dikirim dalam `initConnection.params`; bilangan bulat atau string bilangan desimal |

Jika alias dan nama utama sama-sama ada, keduanya harus sesuai. Bidang sesi Telethon yang eksplisit memiliki prioritas lebih tinggi daripada blob `session` generik dalam format lain. Jika keduanya berisi sesi Telethon yang dapat dikenali, keduanya harus menggambarkan otorisasi yang sama. Tanpa bidang eksplisit, `session` harus berupa StringSession Telethon yang valid. Contoh:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

Contoh pertama hanya mengisi kredensial API; masuk dengan nomor telepon atau QR, atau tambahkan berkas sesi. Daftar massal (array JSON akun) tidak diterima.

## Identifikasi apa yang Anda miliki

| Anda melihat | Ini adalah | Penggunaan |
| --- | --- | --- |
| `*.session`; saat dibuka di editor teks, bagian atasnya menampilkan `SQLite format 3` | Telethon atau Pyrogram SQLite | **Berkas** (terdeteksi secara otomatis) |
| Folder `tdata` yang berisi `key_datas` | Telegram Desktop TData | Kompres dua berkas menjadi ZIP, lalu **Berkas** |
| Satu baris teks yang dimulai dengan `1`, ~350 karakter | Telethon StringSession | **Berkas** |
| `*.json` dengan `app_id`/`app_hash` | Metadata pendamping | **Berkas**, beserta sesi-nya |
| `*.json` dengan `auth_key` atau `string_session` | JSON Akun | **Berkas** |
| 512 karakter `0-9a-f` | Kunci Otentikasi | **Kunci otentikasi** |
| 32 karakter `0-9a-f` | Hash API | **ID API + Hash** |
| `td.binlog` atau `db.sqlite` dari aplikasi TDLib | Penyimpanan TDLib | Tidak didukung |
| `123456789:AA…` | Token bot | Tidak didukung |

## Format yang tidak didukung

| Format | Alternatif |
| --- | --- |
| Penyimpanan TDLib (`td.binlog`) dan ekspor TDLib | Masuk menggunakan nomor telepon atau QR |
| **String** sesi Pyrogram | Gunakan berkas Pyrogram `.session`, atau ponsel/QR |
| TData dengan beberapa akun yang telah masuk | Keluar dari akun-akun lain di Telegram Desktop, atau gunakan berkas sesi masing-masing akun |
| Token bot | Tidak didukung: TgWitness beroperasi sebagai akun pengguna |
| Daftar CSV/JSON dari banyak akun | Impor file sesi yang didukung melalui **Akun → Impor akun**, atau masuk melalui telepon/QR di ruang kerja terpisah |
| Sesi Test-DC atau bot | Gunakan akun pengguna produksi |

## Beberapa akun

Tekan **+** di samping pemilih akun, atau buka **Akun → Pengaturan → Pengaturan koneksi → Ruang kerja**, masukkan label, dan masuk.

- Jumlah ruang kerja tidak terbatas, termasuk ruang kerja utama. Masing-masing memiliki sesi, rute proxy , sumber, kebijakan penangkapan, jurnal, kunci penandatanganan, titik pemeriksaan, dan ekspor tersendiri.
- Mengganti ruang kerja yang ditampilkan tidak akan menghentikan ruang kerja lainnya.
- Sebuah jurnal tetap terikat pada akun yang membuatnya. Masuk dengan akun yang berbeda memerlukan ruang kerja lain, dan satu akun tidak dapat ditugaskan ke dua ruang kerja.
- Token panel utama mengontrol semua ruang kerja. [Akses yang diberikan](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/) dapat membatasi orang lain hanya pada akun dan obrolan tertentu, dengan izin dan batas sesi yang terpisah.
- **Akun** mengganti nama ruang kerja dan menghapus ruang kerja yang ditambahkan, beserta sesi, jurnal, sumber, dan kunci penandatanganan. Ruang kerja utama tidak dapat dihapus dari panel.

### Impor massal dan grup akun

Gunakan **Akun → Impor akun** untuk menambahkan beberapa akun, pasangkan berkas berdasarkan nama dasar dan lihat hasil login masing-masing. Setiap akun memiliki ruang kerja tersendiri.

Sebuah grup menyatukan akun-akun yang terkait tanpa menggabungkan sesi, kunci, atau bukti mereka. **Buka grup** di **bagian Akun** untuk menuju ke halamannya di `/groups/<id>`:

- **Akun:** rute koneksi, pengamatan, dan pesan terakhir setiap anggota, dengan **Mulai Semua** dan **Jeda Semua**.
- **Perlu perhatian:** akun yang telah keluar, tidak tersedia, atau mengalami masalah koneksi, input, sumber, atau media; setiap nama mengarah ke kartunya masing-masing.
- **Obrolan di beberapa akun menampilkan:** sumber yang dibagikan, akun-akun yang mengamati obrolan tersebut, dan gangguan dalam periode pengamatan ruang kerja yang tersedia (hingga tujuh hari). **Ekspor dengan N akun** membagi ekspor saluran atau supergrup di antara akun-akun tersebut dan menandatangani satu arsip.
- **Ekspor grup:** satu ZIP dengan ekspor yang telah ditandatangani dari setiap akun di bawah `accounts/` dan `manifest.json` mencantumkan SHA-256 dan sidik jari kunci masing-masing, yang ditandatangani oleh ruang kerja utama di `manifest.signature.json`. Verifikasi setiap arsip akun secara terpisah dengan `python -m tgwitness.verify` dan sidik jari tepercaya akun tersebut.

Anggota berbagi pengaturan grup; sebuah akun dapat mempertahankan nilai-nilainya sendiri. Lihat [pengaturan bersama](https://phishdestroy.github.io/TgWitness/id/docs/reference/settings/#account-groups), [panduan impor dan grup](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) dan [dasbor kolam MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Keluar

**Akun → Keluar dari Telegram** (dengan pemantauan ditangguhkan) meminta Telegram untuk mengakhiri sesi, sehingga sesi tersebut juga menghilang dari **Pengaturan → Perangkat** akun, dan menghapus sesi tersebut dari brankas ruang kerja. Jurnal, sumber, pengaturan, dan kunci penandatanganan tetap ada, dan jurnal mencatat proses keluar tersebut. Ruang kerja tersebut masih milik akunnya: hanya akun tersebut yang dapat terhubung kembali ke sana. Jika Telegram tidak merespons, sesi tersebut tetap dihapus di sini dan panel akan menampilkannya; akhiri sesi tersebut di Telegram melalui **Pengaturan → Perangkat**.

## Menjaga keamanan berkas akun

- Perlakukan setiap `.session`, TData ZIP, StringSession, Auth Key, dan JSON akun seperti kata sandi. TgWitness menyimpan otorisasi yang diimpor di dalam brankas terenkripsinya; Anda dapat menghapus file aslinya setelahnya.
- Jangan menjalankan otorisasi yang sama di dua program sekaligus. Telegram dapat mencabutnya (`AUTH_KEY_DUPLICATED`), dan kedua salinan tersebut akan berhenti berfungsi.
- Sesi yang telah kedaluwarsa atau dicabut tidak dapat diaktifkan kembali melalui konversi. Silakan masuk kembali.

## Pemecahan Masalah

| Pesan atau gejala | Apa yang harus dilakukan |
| --- | --- |
| *Tidak dapat membaca sesi ini. Tutup klien aslinya…* | Berkas SQLite sedang terbuka atau belum selesai (sidecar `-journal`/`-wal`). Tutup program aslinya dengan benar, lalu salin kembali berkas tersebut. |
| *Skema SQLite Telethon yang didukung: 7 dan 8* / *Pyrogram … 2 dan 3* | File ini dibuat menggunakan versi pustaka yang sangat lama atau tidak dikenal. Silakan masuk menggunakan nomor telepon/QR. |
| *Hanya sesi pengguna produksi yang berwenang yang didukung* | Berkas Pyrogram tersebut milik bot atau jaringan uji coba. |
| *Arsip TData melebihi 512 entri atau 32 MiB* | Hanya berkas ZIP `key_datas` dan `D877F783D5D3EF8Cs`, bukan seluruh folder. |
| *Tidak dapat mendekripsi TData. Periksa kode sandi lokal Desktop* | Masukkan kode sandi lokal Telegram Desktop di kolom "**Passcode**" **atau "session text**". |
| *Impor satu akun TData pada satu waktu* | Telegram Desktop memiliki beberapa akun; lihat [Format yang Tidak Didukung](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#unsupported-formats). |
| *Berkas-berkas yang dipilih menjelaskan akun-akun yang berbeda atau kredensial API* | Pilih file dari satu akun saja. |
| *JSON tidak berisi kredensial API atau otorisasi yang didukung* | Periksa nama-nama bidang dalam [JSON Akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-json). |
| *Hanya metadata API* | JSON ini tidak memiliki sesi. Tambahkan berkas `.session` atau gunakan nomor telepon/kode QR. |
| *Kunci Otorisasi HEX harus berisi seluruh 512 karakter heksadesimal* | Kunci tersebut terpotong atau mengandung `…`. |
| ID akun tidak sesuai dengan akun yang diimpor | ID pengguna pada berkas tersebut berbeda dengan yang dilaporkan oleh Telegram; berkas tersebut diperuntukkan bagi akun lain. |
| Akun ini sudah terdaftar di ruang kerja lain | Buka ruang kerja tersebut daripada menambahkan akun dua kali. |
| Tersambung, tetapi ada grup pribadi yang hilang dari daftar obrolan di **Sumber** | Periksa keanggotaan. Alat pemilih memeriksa 1.000 percakapan pertama; tingkatkan batasnya di bagian **Parameter**. |
| Koneksi proxy gagal | Periksa rute dan mode IP. Secara otomatis, MTProxy akan mencoba entri lain yang berfungsi. Sembunyikan penundaan alamat; Direct sebagai pilihan terakhir dapat terhubung langsung setelah penundaan yang telah dikonfigurasi. Lihat [mode perutean](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes). |

Lihat juga: [koneksi dan keamanan](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) untuk proxy dan enkripsi, serta [cara kerja pengumpulan](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/) data yang direkam setelah masuk.
