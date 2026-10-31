# Format akun dan sesi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/

Masuk menggunakan nomor telepon, kode QR, atau kunci otentikasi, impor sesi Telethon, Pyrogram, atau Telegram Desktop, dan kelola beberapa akun.

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

Anda dapat masuk tanpa perlu membuat aplikasi API Telegram. Jika tidak ada pasangan yang dimasukkan, diimpor, atau sudah disimpan di ruang kerja, TgWitness akan memilih pasangan dari kumpulan bawaan yang terdiri dari 50 pasangan API publik (`tgwitness/api_pool.py`) secara acak. Jika Telegram menolak sebuah pasangan (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), pasangan berikutnya akan dicoba, hingga delapan kali per proses masuk; pasangan yang ditolak akan dilewati hingga aplikasi dimulai ulang. Pasangan yang digunakan untuk masuk akan disimpan bersama akun dan digunakan kembali untuk akun tersebut. **ID API** dan **hash API** mengidentifikasi aplikasi kepada Telegram; keduanya tidak memberikan otorisasi akun secara mandiri.

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

- File dikonversi **di memori** pada server TgWitness Anda. Unggahan tidak disimpan, file ZIP tidak diekstrak ke disk, dan tidak ada layanan eksternal yang dihubungi.
- Sesi yang dihasilkan kemudian diverifikasi dengan Telegram. Jika sebuah berkas mencantumkan ID pengguna, ID tersebut harus sesuai dengan akun yang dilaporkan oleh Telegram.
- Berkas yang mendeskripsikan akun yang berbeda atau kredensial API yang berbeda akan ditolak daripada memilih salah satunya.
- **Kolom "Passcode" atau "session text"** berisi bidang "TData local passcode", sebuah kotak untuk menempelkan StringSession dan **membaca berkas tanpa perlu masuk** (mengisi formulir tanpa menghubungi Telegram).

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
- Kolom lain seperti `phone`, `device`, `sdk`, `app_version`, `lang_pack`, atau kata sandi `twoFA` yang tersimpan akan **diabaikan**. Jika akun tersebut memiliki 2FA, TgWitness akan memintanya.
- Sebuah berkas JSON itu sendiri hanyalah metadata. Tanpa berkas sesi, lanjutkan dengan login melalui ponsel atau QR.

### Telegram Desktop (TData)

TData adalah folder `tdata` dari aplikasi Telegram Desktop (aplikasi lintas platform dari desktop.telegram.org).

| Sistem | Lokasi default `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portabel: di sebelah `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Untuk mengimpornya:

> **Peringatan sesi paralel.** Mengimpor TData akan menggunakan kembali kunci otorisasi Telegram Desktop; hal ini tidak membuat login yang independen. Jangan gunakan kunci tersebut di Desktop dan TgWitness secara bersamaan. Telegram dapat membatalkan otorisasi dengan `AUTH_KEY_DUPLICATED`, sehingga kedua salinan tersebut tidak dapat digunakan hingga login baru.
>
>
>
> Tutup Desktop sepenuhnya, termasuk prosesnya di baki sistem, dan biarkan salinan tersebut tetap tertutup selama TgWitness menggunakan sesi yang diimpor. **Keluar, jangan logout atau mencabut sesi:** pencabutan juga akan membatalkan salinan yang diimpor. Jika Anda memerlukan kedua klien untuk tetap berjalan, masuk ke TgWitness melalui ponsel atau QR untuk membuat otorisasi tersendiri. Disarankan untuk menggunakan akun khusus, tetapi hal ini tidak menjamin keamanan penggunaan kunci kloning secara paralel.
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
| `string_session` (`session_string`, `session`) | Teks Telethon StringSession, bukan nama file |
| `auth_key` (`auth_key_hex`) + `dc_id` | Kunci Otentikasi (Auth Key) lengkap berpanjang 512 karakter dan DC 1–5 |
| `user_id` (`id`) | Opsional; diverifikasi dengan Telegram sebelum otorisasi disimpan |

Jika alias dan nama utama keduanya ada, keduanya harus sama. Contoh:

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
| Daftar CSV/JSON dari banyak akun | Tambahkan satu ruang kerja per akun |
| Sesi Test-DC atau bot | Gunakan akun pengguna produksi |

## Beberapa akun

Tekan **+** di samping pemilih akun, atau buka **Akun → Pengaturan → Pengaturan koneksi → Ruang kerja**, masukkan label, dan masuk.

- Jumlah ruang kerja tidak terbatas, termasuk ruang kerja utama. Masing-masing memiliki sesi, rute proxy , sumber, kebijakan penangkapan, jurnal, kunci penandatanganan, titik pemeriksaan, dan ekspor tersendiri.
- Mengganti ruang kerja yang ditampilkan tidak akan menghentikan ruang kerja lainnya.
- Sebuah jurnal tetap terikat pada akun yang membuatnya. Masuk dengan akun yang berbeda memerlukan ruang kerja lain, dan satu akun tidak dapat ditugaskan ke dua ruang kerja.
- Token panel utama mengontrol semua ruang kerja. [Akses yang diberikan](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/) dapat membatasi orang lain hanya pada akun dan obrolan tertentu, dengan izin dan batas sesi yang terpisah.
- **Akun** mengganti nama ruang kerja dan menghapus ruang kerja yang ditambahkan, beserta sesi, jurnal, sumber, dan kunci penandatanganan. Ruang kerja utama tidak dapat dihapus dari panel.

## Keluar

**Akun → Keluar dari Telegram** (dengan pemantauan ditangguhkan) meminta Telegram untuk mengakhiri sesi, sehingga sesi tersebut juga menghilang dari **Pengaturan → Perangkat** akun, dan menghapus sesi tersebut dari brankas ruang kerja. Jurnal, sumber, pengaturan, dan kunci penandatanganan tetap ada, dan jurnal mencatat proses keluar tersebut. Ruang kerja tersebut masih milik akunnya: hanya akun tersebut yang dapat terhubung kembali ke sana. Jika Telegram tidak merespons, sesi tersebut tetap dihapus di sini dan panel akan menampilkannya; akhiri sesi tersebut di Telegram melalui **Pengaturan → Perangkat**.

## Mengonversi sesi Telethon secara offline

Panel ini mengimpor berkas `.session` secara langsung. Untuk konversi offline ke berkas StringSession, jalankan perintah berikut dari folder proyek:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Konverter ini hanya membaca file Telethon SQLite (hingga 64 MiB), tidak pernah mengubah data masukan, tidak melakukan permintaan jaringan, dan menolak untuk menimpa berkas keluaran yang sudah ada.

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
| Koneksi proxy gagal | Periksa mode rute dan IP. MTProxy otomatis akan mencoba entri lain yang berfungsi. Mode Sembunyikan IP akan menunggu; mode cadangan yang dipilih secara eksplisit dapat terhubung langsung setelah penundaan yang dikonfigurasi. Lihat [mode perutean](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes). |

Lihat juga: [koneksi dan keamanan](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) untuk proxy dan enkripsi, serta [cara kerja pengumpulan](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/) data yang direkam setelah masuk.
