# Telegram · Akses dan izin

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/access/

Tentukan cakupan akses ke akun dan obrolan, pilih izin, batasi sesi dan alamat IP, serta cabut akses.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Memulai](https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/)

![Memulai](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

Berikan akses kepada peninjau ke satu obrolan, izin kepada analis untuk mengekspor suatu kasus, atau kontrol kepada operator atas akun-akun yang dipilih. Setiap orang mendapatkan tokennya masing-masing. Token panel utama tetap berada di tangan administrator.

[Pengaturan akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/) · [Rute koneksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) · [Model keamanan](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/)

## Dua cakupan, dua tugas yang berbeda

**Cakupan pengumpulan** menentukan apa yang direkam oleh suatu akun: obrolan terpilih, folder Telegram, atau seluruh akun. **Cakupan akses** menentukan akun dan obrolan mana saja dari yang telah direkam tersebut yang dapat dilihat dan digunakan oleh orang lain. Memberikan akses tidak berarti bergabung ke obrolan Telegram, memulai pengumpulan, atau memberikan izin akun Telegram.

Sebuah akses dapat membuka ruang kerja yang dipilih, obrolan tertentu di dalamnya, semua ruang kerja, atau setiap akun dalam sebuah [grup akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#bulk-import-and-account-groups). **Semua ruang kerja, termasuk yang ditambahkan kemudian**, juga mencakup akun-akun di masa mendatang. Akses grup juga mencakup akun-akun yang ditambahkan ke grup tersebut di kemudian hari. Pilih ruang kerja secara eksplisit jika kasus harus dibatasi hanya pada ruang kerja tersebut.

## Berikan akses kepada seseorang

1. Masuk sebagai administrator utama dan buka **Akses**.
2. Di bawah bagian "**Berikan akses kepada seseorang**", masukkan nama yang akan Anda kenali dalam log.
3. Pilih ruang kerja dan, jika diperlukan, obrolan individu.
4. Pilih tindakan yang mungkin dilakukan oleh orang ini. Opsi "**Lihat"** selalu disertakan.
5. Tentukan masa berlaku, batas masuk/sesi, dan alamat yang diizinkan sesuai kebutuhan.
6. Tekan **"Buat Akses**". Salin token sekarang: token ini hanya ditampilkan sekali.
7. Kirim alamat panel dan token secara pribadi. Penerima memasukkan token tersebut di halaman masuk biasa; mereka tidak memerlukan token panel utama Anda atau sesi Telegram.

Buka panel yang berisi token yang diterbitkan dalam sesi browser terpisah dan periksa obrolan yang terlihat serta tindakan yang diizinkan sebelum menyerahkannya.

## Pilih izin

Untuk demonstrasi publik berbasis teks saja, gunakan **"Public showcase"** alih-alih akses peninjau biasa. Fitur ini menampilkan saluran publik yang dipilih secara eksplisit, riwayat suntingan dan penghapusan yang disimpan, serta statistik yang ditandatangani, dengan kolom penulis disamarkan dan berkas ditutup pada batas API. [Buat dan verifikasi showcase](https://phishdestroy.github.io/TgWitness/id/docs/reference/showcase/).

| Izin | Fitur yang ditawarkan |
| --- | --- |
| `view` | Baca obrolan yang diizinkan, pesan yang direkam, profil, berkas, dan catatan jurnal yang telah difilter. Selalu disertakan. |
| `export` | Ekspor riwayat obrolan dan berkas yang diizinkan. Ekspor bukti seluruh ruang kerja memerlukan akses ke seluruh ruang kerja. |
| `sources` | Kelola sumber, snapshot, dan penangkapan profil. Akses terbatas pada obrolan hanya dapat diterapkan pada obrolan yang diizinkan; penemuan sumber dan pengaturan cakupan di seluruh akun tetap dinonaktifkan. |
| `collect` | Memulai atau menghentikan pengumpul data. Membutuhkan akses ke seluruh ruang kerja karena pengumpulan data memengaruhi akun. |
| `interact` | Lakukan interaksi Telegram yang didukung dalam lingkup akses. Akses terbatas pada obrolan tidak dapat menggunakan pratinjau tautan di seluruh akun. |
| `settings` | Ubah pengaturan pengumpulan data, cap waktu, pemberitahuan, salinan di luar situs, dan parameter. Membutuhkan akses ke seluruh ruang kerja. |
| `account` | Masuk atau keluar dari Telegram dan kelola rute koneksi. Membutuhkan akses ke seluruh ruang kerja. |
| `board.read` | Baca catatan Papan Kasus hanya di dalam ruang kerja dan obrolan yang diizinkan. |
| `board.write` | Tambahkan penanda, sorotan, potongan, komentar, serta status terbuka/tinjau. Juga memerlukan ``board.read``. |
| `board.manage` | Kelola koleksi, status akhir tim, dan kartu peserta lainnya. Juga memerlukan akses baca/tulis ke papan. |

Izin dan cakupan diperiksa secara bersamaan. Mencentang suatu izin tidak akan membuka obrolan lain atau membuka operasi di seluruh ruang kerja untuk akses yang terbatas pada obrolan tertentu. Untuk ekspor paralel, akses harus mencakup obrolan yang diekspor di setiap akun yang dipilih. Akses yang diterbitkan tidak dapat membuat akses baru, mengelola sesi orang lain, atau membuka konsol administrator.

### Tiga pengaturan yang berguna

| Orang | Ruang Lingkup | Izin |
| --- | --- | --- |
| Peninjau | Percakapan yang direkam dari satu kasus | `view` |
| Analis yang sedang mempersiapkan serah terima | Percakapan yang akan diselidiki dan diekspor | `view`, `export`; tambahkan `interact` hanya jika mereka harus bertindak melalui Telegram |
| Operator pengumpulan data | Ruang kerja yang dipilih secara keseluruhan | `view`, `sources`, `collect`; tambahkan `settings` atau `account` hanya jika diperlukan |

Pengaturan awal formulir Akses juga mencakup Papan Kasus: Peninjau dapat membaca, Analis dapat membaca dan menulis, serta Operator dapat mengelolanya. Pengaturan awal tetap dapat diedit, dan izin yang ada tidak secara otomatis diperluas. Lihat [Papan Kasus](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-board/) untuk cakupan obrolan yang diwarisi dan privasi ekspor.

## Batasan dan sesi

| Pengaturan | Cara kerjanya |
| --- | --- |
| Sesi paralel | Batasi sesi simultan menjadi 1–100. Saat mencapai batas tersebut, tolak upaya masuk berikutnya atau akhiri sesi yang paling lama. |
| Masuk diperbolehkan | Batasi penggunaan token yang berhasil untuk memulai sesi. Sesi yang sudah ada tidak akan berakhir hanya karena batas masuk terakhir yang diizinkan telah digunakan. |
| Berlaku hingga | Akses ini memiliki batas waktu kedaluwarsa yang mutlak. Akses yang telah kedaluwarsa tidak dapat masuk atau terus melakukan permintaan. |
| Menit tanpa aktivitas | Batas waktu ketidakaktifan sesi, mulai dari 5 menit hingga 30 hari. Permintaan yang berhasil akan memperpanjangnya; panel yang terbuka dapat mempertahankan status aktifnya dengan melakukan polling. |
| Alamat yang diizinkan | Terima alamat IP tertentu atau subnet CIDR. Biarkan kosong untuk mengizinkan alamat apa pun kecuali jika pengikatan saat masuk pertama kali diaktifkan. |
| Terikat pada sesi masuk pertama | Pendaftaran pertama yang berhasil akan menetapkan alamat yang diizinkan untuk akses tersebut. |

IP adalah alamat klien yang terlihat oleh aplikasi. Jika berada di balik proxy terbalik atau terowongan, periksa alamat yang ditampilkan di "**Sesi Terbuka"** sebelum mengandalkan aturan IP: jika tidak, beberapa pengguna mungkin tampak berbagi alamat proxy tersebut.

## Mengubah atau mencabut akses

Edit entri di bawah "**Akses yang Diberikan"** untuk mengubah cakupan, izin, atau batasannya. Perubahan cakupan dan izin akan diperiksa pada permintaan berikutnya, termasuk permintaan dari sesi yang sudah terbuka. Mencabut akses akan mengakhiri sesi-sesi tersebut dan membuat token yang diterbitkan tidak dapat digunakan lagi. **Sesi yang terbuka** juga memungkinkan administrator mengakhiri sesi individu tanpa mencabut seluruh akses.

Salinan ekspor yang disimpan tetap mempertahankan informasi pembuat, ruang kerja, cakupan obrolan, dan izin yang diperlukan. Akses yang diberikan hanya dapat menampilkan daftar atau mengunduh salinannya sendiri selama izin tersebut masih berlaku; salinan yang berisi Case Board juga memerlukan izin ``board.read``. Administrator dapat mengambil semua salinan. Salinan lama tanpa metadata ini dan bundel grup hanya dapat diakses oleh administrator. Unduh tiket dan respons berkas yang telah disiapkan akan memeriksa ulang akses setelah berkas disiapkan, sebelum mengirimkan byte-bytenya.

Pencabutan tidak dapat menarik kembali berkas yang telah diunduh oleh seseorang. Keluar dari akun, mengunci panel, atau mengakhiri sesi tidak akan menghentikan pengumpul yang sedang berjalan.

## Apa yang dapat dilihat oleh administrator

Peninjau dan analis menerima laporan kemajuan pengumpulan data tanpa titik akhir proxy, diagnostik pool, jalur server, atau kesalahan koneksi mentah. Diagnostik koneksi memerlukan izin `account` untuk seluruh ruang kerja. Membaca notifikasi, salinan di luar lokasi, dan pengaturan parameter memerlukan izin `settings`.

String User-Agent lengkap dari browser tidak disimpan dalam sesi akses. Pembaruan juga menghapusnya dari cache sesi yang dapat diubah. Log proses panel menyembunyikan literal IP, kredensial URL, dan rahasia berlabel. Log layanan lokal dan catatan jurnal yang telah ditandatangani sebelumnya tidak ditulis ulang. Aturan akses dan catatan masuk yang ditandatangani masih menggunakan alamat klien.

### Ganti kunci utama

Gunakan **Akses → Batas saya → Terbitkan ulang kunci administrator**, atau jalankan `tgwitness token rotate` dari instalasi yang dikelola saat panel sedang berjalan. Semua sesi browser yang ada akan berakhir, termasuk sesi yang dibuka dengan token rekan kerja. Browser yang meminta akan menerima sesi baru; simpan kunci administrator baru sebelum menyembunyikannya. Token rekan kerja yang telah diterbitkan tetap berlaku hingga dicabut secara terpisah. Instalasi yang menggunakan `TGWITNESS_TOKEN` harus mengubah pengaturan lingkungan tersebut dan melakukan restart.

### Batas permintaan dan proxy

API ini mengizinkan hingga 600 permintaan per menit per alamat IP klien. Sepuluh penolakan otentikasi dalam satu menit akan memicu masa tunggu eksponensial, mulai dari satu detik hingga lima menit. Upaya yang gagal setelah masa tunggu berakhir akan memperpanjangnya; sepuluh menit tanpa upaya yang gagal akan mereset eskalasi. Penolakan mengembalikan kode HTTP 429 dan `Retry-After`. Batasan disimpan dalam memori, dibagikan di seluruh ruang kerja dalam satu proses panel; restart akan menghapusnya. Streaming langsung dibatasi hingga empat per token pembawa dan 32 untuk proses panel. Membuka streaming juga menghabiskan kuota permintaan API.

Badan permintaan memiliki batas waktu penerimaan 60 detik (8 detik untuk MCP). Setiap aplikasi membatasi badan permintaan yang belum selesai hingga 32 permintaan dan 64 MiB kuota rute yang dialokasikan. Badan permintaan yang melebihi batas ukuran akan mengembalikan kode status 413, badan permintaan yang habis waktu akan mengembalikan 408, dan kapasitas badan permintaan yang habis akan mengembalikan 503 dengan atribut ``Retry-After``.

Header IP yang diteruskan diabaikan kecuali jika rekan TCP yang sebenarnya termasuk dalam `TGWITNESS_TRUSTED_PROXIES` (IP yang dipisahkan dengan koma atau CIDR). Atur `TGWITNESS_PROXY_HEADER` menjadi `x-forwarded-for` atau `cf-connecting-ip`. XFF dilacak dari proxy terdekat menuju rekan pertama yang tidak tepercaya. Metadata alamat tepercaya yang salah format atau duplikat akan ditolak, sehingga tidak dapat mewarisi alamat proxy yang ada dalam daftar putih . Terowongan cepat yang dikelola mempercayai konektor cloudflared lokal; pengaturan domain sendiri mempercayai Caddy lokal. Penerapan langsung secara default tidak mempercayai proxy apa pun. Jika Anda menjalankan Uvicorn sendiri, nonaktifkan pemrosesan header proxy-nya agar batas ini menerima peer yang sebenarnya.

`TGWITNESS_PANEL_ALLOWED_IPS` membatasi semua akses panel, termasuk administrator, hanya ke alamat IP atau CIDR yang terdaftar. Probe identitas perutean penginstal tetap publik dan tidak mengembalikan data akun apa pun. Sertakan rute administratif lokal yang diperlukan sebelum mengaktifkan daftar izinkan. Panduan **START-HERE** untuk instalasi terkelola mencakup konfigurasi layanan dan petunjuk pemulihan.

Pemilih kueri API `ws` harus mengidentifikasi ruang kerja dalam jalur permintaan; pemilih yang tidak dikenal, tidak cocok, dan duplikat akan ditolak dengan kode status 404.

Skrip dan gaya panel membawa metadata integritas SHA-384. Peta impor juga mencakup modul JS yang diimpor secara lokal di peramban yang mendukung integritas peta impor. Respons bahasa yang dihasilkan secara dinamis bersifat terpisah. Pemeriksaan ini mendeteksi penggantian aset relatif terhadap halaman yang dikirimkan; pemeriksaan ini tidak menetapkan kepercayaan pada server yang disusupi yang dapat mengganti baik halaman maupun hash-nya.

**Log sejak awal ini** menggabungkan log proses dengan aktivitas jurnal dari setiap ruang kerja: masuk, penolakan, perubahan rute, dan tindakan operator. Ini adalah konsol dalam memori untuk proses saat ini, bukan salinan permanen dari setiap pesan. Peristiwa pesan yang sering terjadi tetap tersimpan dalam jurnal daripada memenuhi konsol.

Penerbitan, perubahan, dan pencabutan akses, serta memulai atau mengakhiri sesi, juga menghasilkan catatan jurnal `access.*` yang ditandatangani. Token tidak termasuk dalam catatan tersebut. Token yang diterbitkan dan kredensial sesi disimpan sebagai hash di brankas terenkripsi.

****Administrator utama dan batas kepercayaan****

Token panel utama tetap tidak dibatasi. Masuk ke browser menggunakan token tersebut akan membuat sesi yang tunduk pada batas sesi yang dikonfigurasi oleh administrator. Skrip yang mengirimkan token utama secara langsung tetap memiliki akses penuh dan tidak dihitung sebagai sesi browser.

Ini adalah kontrol akses tingkat aplikasi dalam satu instalasi. Semua ruang kerja berbagi proses server; ini bukanlah isolasi dari administrator host. Jaga kerahasiaan token utama, sesi Telegram, kunci penandatanganan, dan direktori data. Token saksi adalah kredensial titik pemeriksaan/kesehatan yang terpisah, bukan token akses panel.
