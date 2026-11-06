# Telegram · Koneksi, proxy, dan perlindungan data

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/

Otentikasi, kumpulan proxy otomatis, mode IP, kebijakan cadangan, permintaan eksternal, dan penyimpanan rahasia.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Penerapan dan pemulihan](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/)

![Penerapan & pemulihan](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Dokumen ini menjelaskan perilaku TgWitness 0.8.0 dan batasannya. Otentikasi, akses sumber, konektivitas jaringan, dan kelengkapan penangkapan merupakan kondisi yang terpisah. Untuk langkah-langkah masuk, format berkas, dan pengelolaan beberapa akun, mulailah dengan [bagian akun dan format sesi](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/). Untuk kebijakan peristiwa dan perilaku saat dimulai ulang, lihat [cara kerja pengumpulan data](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/).

## Panduan pengaturan koneksi

Di **Koneksi**, administrator dapat memilih **Akun ini**, **Kelompok akun** atau **Semua akun**, lalu pilih rute. **Tinjau Pilihan** menampilkan daftar akun yang terpengaruh. **Siapkan dan Periksa** menguji rute yang diusulkan tanpa mengubah rute yang telah disimpan. **Terapkan Koneksi yang Telah Diperiksa** memeriksa kembali, menjeda pemantauan jika diperlukan, menyimpan rute, dan melanjutkan pemantauan yang sudah berjalan. Pengumpulan data tidak pernah dimulai di akun yang sebelumnya tidak aktif. Unduhan riwayat tetap dijeda dan dapat dilanjutkan secara terpisah. Jeda ekspor yang aktif sebelum beralih.

Perubahan grup secara default mempertahankan akun dengan rute masing-masing. Hapus opsi tersebut hanya jika pratinjau mencantumkan perubahan yang Anda inginkan. Aplikasi melaporkan hasil setiap akun; ini bukan transaksi "semua atau tidak sama sekali" yang mencakup seluruh basis data. Peralihan yang gagal akan mengembalikan pengaturan sebelumnya pada akun tersebut. Kegagalan dalam melanjutkan akan ditampilkan secara eksplisit. Pratinjau kedaluwarsa setelah sepuluh menit dan perubahan pada pengaturan koneksi atau keanggotaan grup memerlukan pemeriksaan ulang.

| Rute | Apa yang dikelola oleh TgWitness |
| --- | --- |
| Langsung | Koneksi dari host; VPN host eksternal tidak terdeteksi atau tidak diberlakukan. |
| VPN | Satu profil WireGuard dengan tunnel penuh per akun, dijalankan oleh proses SOCKS5 di ruang pengguna lokal. Tidak ada antarmuka host atau driver yang diinstal. |
| Proksi saya | Kredensial SOCKS5, HTTP CONNECT, atau MTProxy. Sebuah URL dapat diisi pada kolom SOCKS5/HTTP. Memilih beberapa akun akan membagikan proxy yang dimasukkan ini. |
| MTProto Publik | Pool yang ada menetapkan rute Telegram. Permintaan eksternal dinonaktifkan hingga proxy terpisah yang sesuai dikonfigurasi di pengaturan lanjutan. |
| WARP | Terowongan lokal terpisah untuk setiap akun yang dipilih, dengan pendaftaran WARP dan profil WireGuard yang disimpan di brankas akun tersebut. |

Pemeriksaan rute saat ini menggunakan transportasi Telegram baru yang belum diautentikasi, bukan sesi akun. Untuk rute yang mendukung HTTP, pemeriksaan ini juga meminta jejak HTTPS Cloudflare melalui rute tersebut dan menampilkan IP keluar yang dilaporkan, negara, status WARP, serta waktu pemeriksaan. Latensi yang diukur adalah waktu penyiapan koneksi Telegram, bukan ping ICMP. Persiapan WARP akan gagal kecuali jejak melaporkan WARP aktif. Pemeriksaan ini memastikan konektivitas, bukan keaslian atau kelengkapan pesan yang ditangkap. Proses lokal yang sedang berjalan saja tidak menjamin keberhasilan pemeriksaan titik keluar.

### WARP dan WireGuard yang portabel

Ini adalah integrasi WARP tidak resmi **** menggunakan [wgcf 2.3.1](https://github.com/ViRb3/wgcf/releases/tag/v2.3.1) dan [wireproxy 1.1.3](https://github.com/windtf/wireproxy/releases/tag/v1.1.3). Administrator secara eksplisit menyetujui pengaturan sebelum unduhan pertama atau pendaftaran WARP. Koneksi pengaturan tersebut terhubung langsung ke GitHub dan Cloudflare serta mengungkapkan alamat IP mesin. Lalu lintas akun biasa tetap menggunakan rute yang ada hingga aplikasi. Cloudflare memilih alamat keluar dan negara; terowongan terpisah dapat berbagi alamat keluar yang sama. Pemilihan negara, rotasi IP berkala, dan kill switch VPN untuk seluruh host tidak disediakan oleh fitur ini.

Unduhan helper yang didukung: Linux dan macOS x86-64/ARM64, serta Windows x86-64. Artefak diperiksa berdasarkan hash SHA-256 yang disertakan dalam sumber yang telah ditinjau, dan file eksekusi yang disimpan dalam cache diperiksa kembali sebelum dijalankan. Tidak ada program bantu yang ditambahkan ke PATH, diinstal sebagai layanan sistem, atau diberi pendengar publik. Semua berkas berada di bawah direktori `portable-routes/` ruang kerja dan entri brankas terenkripsi. Pendengar loopback SOCKS5 memerlukan kredensial yang dihasilkan secara independen.

Profil pribadi dan kredensial akun WARP dienkripsi menggunakan brankas ruang kerja yang ada. Saat berjalan, helper memerlukan konfigurasi teks biasa yang hanya dapat diakses pemilik; konfigurasi ini dihapus saat penghentian normal. Kerusakan host dapat meninggalkan berkas ini di folder data khusus pemilik. Hal ini tidak mengenkripsi disk atau melindungi dari administratornya. Pengawas akan menutup terowongan jika pipa induk panel menghilang. Terowongan yang gagal tidak pernah mengaktifkan fallback langsung. Restart panel akan memulihkan terowongan yang dipilih; upaya awal yang gagal akan dicoba ulang dengan penundaan terbatas. **Hentikan terowongan** juga menghentikan sementara pemantauan dan mempertahankan status terhenti. **Mulai terowongan** memulai terowongan; lanjutkan pemantauan secara terpisah saat sudah siap.

Profil WireGuard yang diunggah harus berisi satu Antarmuka dan satu Peer, rute IPv4 dan IPv6 lengkap, serta tidak boleh ada hook, include, substitusi lingkungan, atau listener tambahan. Alamat titik akhir publik diselesaikan dan ditetapkan sebelum startup. Gunakan VPN eksternal atau gerbang SOCKS5 untuk OpenVPN/IPsec dan titik akhir pribadi.

## Metode otentikasi

**API ID dan API hash mengidentifikasi sebuah aplikasi; keduanya tidak menggantikan proses login akun.** Keduanya bersifat opsional di TgWitness. Urutan prioritas: pasangan yang dimasukkan melalui formulir, kemudian pasangan dari berkas JSON akun yang diimpor, lalu pasangan yang disimpan di ruang kerja, kemudian kumpulan bawaan berisi 50 pasangan publik, dicoba dalam urutan acak dengan rotasi otomatis saat Telegram menolak salah satunya. Hanya pasangan Telegram Desktop (2040) yang dikirim bersama deskripsi klien Telegram Desktop yang sesuai. Pasangan Anda sendiri dari Alat Pengembangan API di [my.telegram.org](https://my.telegram.org) dapat digunakan dengan semua akun Anda; setiap akun tetap memiliki otorisasi tersendiri.

| Metode | Persyaratan | Dukungan TgWitness |
| --- | --- | --- |
| Nomor telepon, kode, 2FA (opsional) | Akses akun; pasangan API opsional | Panel masuk |
| Kunci Otentikasi HEX + ID DC | Kunci lengkap 512 karakter dan DC 1–5 | Tab **Kunci Otorisasi** Langsung; ID Pengguna opsional diperiksa sebelum otorisasi disimpan |
| Telethon StringSession | String sesi yang valid | Panel masuk |
| Telethon SQLite `.session` | Teks yang tertutup dan konsisten | Impor skema langsung melalui panel 7/8; CLI offline opsional |
| Pyrogram SQLite `.session` | Sesi pengguna produksi telah ditutup | Impor skema langsung melalui panel 2/3 |
| Telegram Desktop TData ZIP | Satu akun modern; kode sandi lokal jika dilindungi | Konversi dalam memori dengan pemeriksaan checksum dan dekripsi |
| JSON Akun | Bidang API/sesi/kunci yang didukung | Metadata saja sudah cukup untuk mengisi kredensial API; namun, login menggunakan sesi/kunci atau nomor telepon/QR code tetap diperlukan |
| Masuk dengan QR | Konfirmasi dari aplikasi Telegram yang resmi | Pembuatan QR lokal, masa berlaku/percobaan ulang, 2FA opsional |
| TDLib / Pyrogram StringSession | Format khusus perpustakaan lainnya | Tidak didukung |
| Token bot | Sebuah bot dengan model akses/pembaruan tersendiri | Tidak digunakan oleh pengumpul ini |

Telegram memilih pengiriman kode; pengiriman melalui SMS tidak dijamin. Hash API tidak dapat memperbaiki sesi yang dicabut atau menggantikan kata sandi 2FA yang terlupa. TgWitness tidak menyimpan kode login atau kata sandi 2FA Telegram ke disk.

Untuk sumber pribadi, akun tersebut harus sudah memiliki akses. Nama pengguna grup tidak diperlukan. Penggunaan proxy atau impor sesi tidak memberikan hak keanggotaan maupun hak administrator. Keanggotaan saat ini tidak menjamin akses ke riwayat sebelum bergabung.

## Impor berkas sesi Telethon

Telethon SQLite, Pyrogram SQLite, dan Telegram Desktop TData menggunakan format yang berbeda. Panel ini mendeteksi dan mengonversi struktur yang didukung; mengganti nama file bukanlah proses konversi. Pilih satu sesi dan file JSON yang menyertainya di bawah **"Files**", lalu tekan **"Connect account"**. Maksimal empat file yang cocok dan total 8 MiB diterima. Lihat [batasan format](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/) untuk detail TData/JSON. Tidak ada pemulihan kode sandi. Masuk melalui telepon/2FA atau QR akan membuat otorisasi terpisah.

Jalur baris perintah opsional khusus Telethon tetap tersedia:

1. Hentikan klien yang menggunakan sesi asli dan buat salinan yang konsisten. Konverter akan menolak berkas dengan WAL/jurnal yang belum selesai. Tutup klien asli dengan benar, bukan dengan menghapus berkas-berkas tersebut untuk menghindari pemeriksaan.
2. Dari lingkungan TgWitness, jalankan:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. Di bawah **Tambahkan akun → File**, unggah hasilnya atau tempelkan stringnya, lalu lanjutkan.
2. Periksa ID akun numerik yang ditampilkan, pilih sumber, dan mulailah pemantauan.

**File yang dikonversi merupakan rahasia akses akun yang tidak terenkripsi.** Simpanlah di tempat penyimpanan yang terlindungi dan jangan pernah mengunggahnya atau mengirimkannya ke layanan konversi pihak ketiga. TgWitness menyimpan sesi otorisasi di brankas terenkripsinya. Menyalin sesi tidak akan menciptakan otorisasi terpisah: jangan jalankan klien secara bersamaan dengan kunci otorisasi yang dikloning dan mengasumsikan pengiriman pembaruan yang independen.

Konversi mentransfer otorisasi, bukan pesan asli, cache entitas, atau kursor pembaruan yang tahan lama. Konversi ini tidak memastikan pemulihan pembaruan saat proses dimulai ulang.

## MTProto, Telethon, dan proxy

MTProto adalah protokol Telegram. Telethon adalah pustaka klien Python yang digunakan oleh TgWitness. MTProxy adalah proxy transportasi Telegram; SOCKS5 dan HTTP CONNECT menyediakan terowongan umum. Tidak ada yang menggantikan otentikasi akun.

Simpan rute untuk setiap ruang kerja di **Akun → Pengaturan → Pengaturan koneksi → Ubah rute koneksi** sebelum masuk. Ruang kerja baru secara default menggunakan mode **Otomatis MTProxy · daftar publik** dengan **opsi Sembunyikan alamat**. Ruang kerja yang sudah ada yang secara eksplisit menggunakan mode Langsung tetap mempertahankan mode yang mengizinkannya.

## Mode IP

Rute menentukan koneksi. Mode IP, yaitu pengaturan **perlindungan IP** di bagian Akun pada panel, menentukan kapan alamat server dapat terungkap. Kontrol ini tidak menginstal VPN atau mengalihkan seluruh lalu lintas perangkat.

| Mode | Telegram | Permintaan eksternal |
| --- | --- | --- |
| Sembunyikan alamat (`hide`) | Gunakan proxy; tunggu jika tidak ada yang berfungsi. Tidak ada opsi cadangan langsung. | Memerlukan SOCKS5/HTTP; menolak permintaan tanpa proxy yang sesuai. |
| Gunakan Direct sebagai pilihan terakhir (`fallback`) | MTProxy otomatis mungkin menggunakan Direct setelah penundaan yang dikonfigurasi, kemudian kembali ke proxy yang berfungsi. | Disarankan menggunakan proxy eksternal yang telah dikonfigurasi atau rute SOCKS5/HTTP akun; jika tidak, opsi Direct diperbolehkan. |
| Server yang berada di balik terowongan atau VPN (`tunnel`) | Rute langsung dan pengalihan otomatis ke pool cadangan diperbolehkan. | Akses langsung diperbolehkan jika tidak ada proxy yang dikonfigurasi. |

Mode terowongan atau VPN mengasumsikan Anda mengelola jaringan tersebut secara terpisah. Tanpa terowongan yang berfungsi, tujuan dapat melihat alamat server itu sendiri. Pilih mode sesuai dengan jaringan Anda yang sebenarnya, bukan berdasarkan nama opsi tersebut.

### Pilih jalur

| Rute | Pengaturan | Batasan |
| --- | --- | --- |
| MTProxy Otomatis | Daftar bawaan atau katalog operator | Menjaga rute Telegram yang berfungsi; fallback langsung bergantung pada mode IP |
| Langsung | Mode terowongan atau VPN | Telethon menggunakan rute jaringan tuan rumah |
| SOCKS5 | Host, port, nama pengguna/kata sandi (opsional) | python-socks, DNS tujuan jarak jauh diaktifkan |
| HTTP CONNECT | Host, port, nama pengguna/kata sandi (opsional) | HTTP CONNECT biasa; TLS ke proxy itu sendiri belum diimplementasikan |
| MTProxy | Host, port, rahasia | Transportasi Telethon eksperimental; 32 digit heksadesimal atau `dd` + 32 digit heksadesimal |

Rahasia TLS palsu `ee` ditolak. Normalisasi Telethon 1.45 dapat menghilangkan awalan dan domain, tetapi hal itu tidak mengimplementasikan TLS palsu. Tempelkan `tg://proxy?server=…&port=…&secret=…` atau `https://t.me/proxy?server=…&port=…&secret=…` dan pilih **"Isi bidang dari tautan**". Ini akan memvalidasi dan mengisi kolom tanpa terhubung atau menyimpan; tinjau dan simpan rute secara terpisah. Kolom manual tetap tersedia. Lihat [tautan proxy Telegram](https://core.telegram.org/api/links#proxy-links).

### Proksi publik yang disediakan oleh instalasi Anda

Daftar bawaan ini menggabungkan empat sumber: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) dan [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Snapshot yang disertakan berisi data titik akhir, atribusi sumber, dan tanggal unduhan. Kehadiran penyedia dalam daftar ini bukanlah bukti bahwa proxy tersebut berfungsi atau menyalurkan setiap pembaruan Telegram.

**MTProxy otomatis** memeriksa konektivitas transportasi Telegram, mempertahankan proxy yang berfungsi dan beralih ke proxy lain saat terjadi kegagalan. Ruang kerja lebih memilih proxy yang berbeda jika tersedia cukup entri yang berfungsi; alamat keluar yang unik tidak dijamin. Proksi yang gagal akan beristirahat sebelum upaya berikutnya. Jika tidak ada yang berfungsi, mode IP menentukan apakah pengumpulan harus ditunda atau dapat menggunakan koneksi langsung. Mengganti proksi tidak mengubah akun atau menghapus jurnalnya. Pilihan dan perubahan rute dicatat dalam jurnal yang ditandatangani.

Selama rute otomatis aktif, daftar diperbarui setiap jam dan pemeriksaan pengiriman dijalankan setiap sepuluh menit secara default. Interval-interval ini dapat dikonfigurasi. Permintaan **pembaruan daftar publik** memicu pembaruan; hanya melihat daftar saja tidak mengubah rute manual yang telah disimpan.

**Lalu lintas Telegram dan permintaan HTTPS menggunakan rute yang berbeda.** Unduhan daftar menggunakan koneksi HTTPS terpisah dan rute permintaan eksternal yang disediakan. ``TGWITNESS_PROXY_FEED_PROXY`` secara eksplisit mengganti rute tersebut dengan proxy HTTP/SOCKS5; kedua varian pengumpul Compose meneruskannya. Kolam latar belakang mengikuti ruang kerja utama. Tidak ada sesi Telegram, kredensial API, token panel, atau token bot yang dikirim ke penyedia umpan. Nama penyedia, tanggal snapshot, dan rute unduhan tercantum di bagian **“Dari mana daftar ini berasal**”.

Sebuah MTProxy hanya mengangkut lalu lintas Telegram. Operasi HTTP ruang kerja seperti cap waktu, pemberitahuan, salinan di luar situs, dan pemeriksaan sumber menggunakan proxy SOCKS5/HTTP terpisah saat dikonfigurasi, kemudian rute SOCKS5/HTTP akun tersebut. Tanpa keduanya, "Sembunyikan alamat" akan menolak permintaan; mode lainnya mengizinkan "Langsung". Permintaan eksternal dapat dinonaktifkan. Proxy unduhan umpan yang dikonfigurasi secara eksplisit tetap menjadi pengaturan operator terpisah. Layanan saksi independen mempertahankan rutenya sendiri.

Untuk layanan pribadi yang dikelola operator, pengaturan lingkungan server yang ada `TGWITNESS_ALLOW_PRIVATE_DESTINATIONS=1` mengizinkan tujuan pribadi dan mempertahankan resolusi nama host di sisi proxy. Pengaturan ini tidak dapat diaktifkan dari panel. Mode khusus publik menolak tujuan `.onion` sebelum melakukan kueri ke resolver publik; layanan onion Tor memerlukan pengaturan tujuan pribadi yang eksplisit dan proxy yang sesuai. Perilaku DNS ini berlaku untuk operasi HTTP eksternal, bukan transportasi Telegram. Cloudflare mendokumentasikan [titik akhir DNS JSON](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/).

****Parameter kolam otomatis****

Di bawah **Parameter → MTProxy Otomatis**, konfigurasikan ambang batas kegagalan, waktu tunggu, rotasi terjadwal, berbagi proxy, dan penundaan fallback yang diizinkan.

| Kontrol | Default |
| --- | --- |
| Terputus sebelum penggantian | 3 dalam 10 menit |
| Proksi yang dicoba per upaya koneksi | 3 |
| Istirahat pertama / maksimum setelah kegagalan | 10 menit / 6 jam |
| Rotasi yang direncanakan | Dinonaktifkan; aktifkan jika terjadi kegagalan |
| Akun per proxy | 0: utamakan entri terpisah, gabungkan jika diperlukan. Atur 1 untuk menunggu entri eksklusif. |
| Penundaan sebelum fallback langsung diizinkan | 10 menit; Menyembunyikan alamat masih ditolak secara langsung |
| Pemeriksaan penyegaran / pengiriman data | Notulen 60/10; nilai ruang kerja utama berlaku untuk kumpulan bersama |

Penggunaan proxy yang berbeda tidak menjamin alamat keluar yang berbeda. Pengaturan ini tidak menggantikan batasan Telegram atau membuktikan anonimitas.

Untuk mengganti daftar publik dengan katalog operator Anda sendiri, konfigurasikan pengaturan penggantian di bawah ini. Pengaturan ini menonaktifkan langganan eksternal sepenuhnya, termasuk ketika array `proxies`-nya kosong.

Salin [katalog kosong](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) ke `proxy-config/proxies.json` dan tambahkan titik akhir publik yang telah Anda terapkan:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Nilai-nilai contoh harus diganti. Maksimal 32 entri berbeda dapat diterima. Daftar yang terotentikasi mengembalikan label/host/port tanpa rahasia bersama; memilih salah satunya akan menyimpan kredensialnya ke dalam brankas ruang kerja. Ketersediaan belum diuji hingga dilakukan uji transportasi secara eksplisit. Katalog yang tidak valid memungkinkan konfigurasi manual.

Peluncuran lokal: atur `TGWITNESS_PROXY_CATALOG` ke jalur JSON lokal. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

Overlay dipasang sebagai `proxy-config` read-only; berkas harus dapat dibaca oleh UID kontainer 10001. Direktori tersebut dikecualikan dari Git, konteks build Docker, dan arsip sumber. Katalog ini mengonfigurasi akun-akun pengumpul; [bot saksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/) menggunakan rute HTTP/SOCKS5-nya sendiri, bukan MTProxy.

Pengalihan langsung diatur oleh mode IP di atas. Jeda pengamatan sebelum mengubah rute. Penyimpanan akan memutuskan koneksi klien lama dan membatalkan proses login yang belum selesai; klien baru akan menggunakan rute yang disimpan. Pengikatan jurnal/sesi akun tetap berlaku. Pengaturan akan menggantikan rute sebelumnya: masukkan kembali kredensial proxy saat mengeditnya.

Kredensial dienkripsi menggunakan `network.enc`. API tidak mengembalikan nama pengguna, kata sandi, atau rahasia. Catatan yang ditandatangani berisi jenis rute dan apakah kredensial terdapat di dalamnya, tanpa menyertakan titik akhir dan rahasia. Operator dapat melihat titik akhir di panel. Bidang rahasia akan dihapus setelah menyimpan, mengunci, atau beralih antar ruang kerja.

**Uji koneksi Telegram**, juga tersedia sebelum masuk, membuka dan menutup koneksi Telegram sementara yang tidak sah melalui rute tersebut. Fitur ini tidak menghubungi situs web pemeriksaan IP. Keberhasilan uji ini menunjukkan terjalinnya konektivitas transportasi, bukan akses ke grup, pengiriman yang lengkap, atau anonimitas.

Proksi ini berlaku untuk koneksi klien Telegram, termasuk unduhan media dari server distribusi (DC) Telegram. Alat-alat seperti browser, pip, SSH, dan TSA yang dijalankan secara manual memiliki rute terpisah. Nama host proksi dapat diresolusi secara lokal. `rdns` memengaruhi nama host tujuan; Telegram sering kali menyediakan alamat IP numerik dari server distribusi (DC).

SOCKS5 dan HTTP CONNECT biasa tidak mengenkripsi kredensial proxy atau terowongan klien-ke-proxy itu sendiri. MTProto secara terpisah melindungi lalu lintas Telegram. Gunakan saluran aman yang sesuai ke proxy pada jaringan yang tidak tepercaya. Grup pribadi adalah obrolan cloud; MTProto tidak mengubahnya menjadi Obrolan Rahasia yang dienkripsi ujung-ke-ujung.

## Enkripsi dan tanda tangan

| Lapisan | Telah diterapkan | Tanggung jawab operator |
| --- | --- | --- |
| Lalu lintas Telegram | Telethon MTProto | Kepercayaan, rute, dan ketersediaan platform |
| Panel web | Token pembawa, pengaturan default loopback, batas permintaan | HTTPS atau terowongan SSH untuk akses jarak jauh |
| Rahasia | Fernet untuk kredensial API, sesi, kredensial proxy, dan kunci pribadi penandatanganan | Lindungi kunci dekripsi dan host yang sedang berjalan |
| Kunci brankas | Kunci lokal, atau kunci utama eksternal untuk instalasi baru | Penyimpanan terpisah yang dilindungi dan cadangan kunci |
| Pesan dan lampiran | Penyimpanan aplikasi dalam bentuk teks biasa | Disk/volume terenkripsi |
| ZIP/JSONL/CSV/HTML | Pemeriksaan integritas, tanpa enkripsi konten | Lindungi salinan yang diekspor dan transfer |
| Asal-usul dan waktu | Jurnal yang ditandatangani, tanda terima proses, alat RFC 3161 | Kunci tepercaya, titik pemeriksaan independen/TSA, dan prosedur penyimpanan |

**Perlindungan penyimpanan** di Akun menampilkan status-status ini. Token panel adalah kunci akses, bukan kata sandi enkripsi. Token ini memberikan akses administrator; [token yang diterbitkan](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/) dapat dibatasi cakupannya ke akun dan obrolan. Ruang kerja berbagi proses host dan bukan penyewa yang terisolasi.

BitLocker, LUKS, FileVault, atau volume terenkripsi yang dikelola dapat melindungi penyimpanan sesuai dengan model ancaman masing-masing. Seorang administrator pada mesin yang sedang berjalan dan tidak terkunci masih dapat membaca data. Sertakan SQLite WAL/SHM, media, ekspor sementara, swap, cadangan, dan unduhan browser dalam perencanaan penyimpanan. Volume Docker tidak otomatis terenkripsi hanya karena statusnya sebagai volume. TgWitness tidak mengimplementasikan SQLCipher atau enkripsi objek.

## Kunci utama eksternal

Untuk instalasi **baru**, letakkan kunci utama di luar direktori data. Hal ini tidak secara otomatis memigrasikan brankas kunci lokal yang sudah ada. Siapkan direktori kunci yang hanya dapat diakses oleh identitas layanan, lalu jalankan:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, menggunakan lingkungan proyek yang telah diinstal:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

Di Docker, pasang berkas tersebut sebagai read-only di luar `/data`, misalnya di `/run/secrets/tgwitness-master.key`, dan atur variabel lingkungan ke jalur tersebut. UID layanan harus memiliki izin baca terhadap berkas tersebut. Sampaikan jalurnya, bukan byte kunci, melalui berkas lingkungan/konfigurasi.

Setiap ruang kerja menerima salt publik acak dan kunci Fernet-nya sendiri yang diturunkan melalui HKDF-SHA256. `vault.external.json` menyimpan metadata derivasi, bukan kunci utama. Kunci yang hilang atau salah akan menyebabkan kegagalan saat memulai tanpa menggantinya secara diam-diam. Simpan baik metadata salt maupun kunci utama untuk pemulihan.

Semua ruang kerja berasal dari kunci utama yang sama; jika kunci tersebut bocor, hal itu akan memengaruhi seluruh instalasi. Proses yang sedang berjalan dapat mendekripsi rahasia. Ini bukanlah HSM atau KDF kata sandi. Kata sandi buatan manusia yang sembarangan tidak diterima sebagai pengganti kunci acak.

Simpan kunci yang ada untuk instalasi yang sudah ada hingga migrasi yang disengaja dilaksanakan dan diverifikasi. Menghapus `vault.key` atau mengganti kunci utama dapat menghancurkan akses ke sesi/kunci penandatanganan. Simpan cadangan terenkripsi dan kunci secara terpisah, serta uji pemulihan di instance yang terisolasi.
