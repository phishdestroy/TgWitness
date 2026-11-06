# Apa yang telah diuji

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/

Uji coba Telegram secara langsung, pemeriksaan otomatis, pemeriksaan browser, dan hal-hal yang masih belum terverifikasi.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bukti dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/)

![Bukti & verifikasi](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Diperbarui pada 6 November 2026.** Hasil terkait dengan revisi, lingkungan, dan beban kerja yang dicatat untuk setiap eksekusi. [Kemampuan saat ini](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) menjelaskan alur kerja yang tersedia; halaman ini mencatat apa yang sebenarnya telah diperiksa.

[Grafik kinerja](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Audit bahasa Inggris yang ditandatangani](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Pengukuran yang dapat diunduh](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Bukti terbaru | Hasil | Ruang Lingkup |
| --- | --- | --- |
| Audit rilis · 6 November | Uji inti 1,461 berhasil; uji platform 37 dilewati | Sumber `92e539af40d8`; temuan terbuka dipertahankan |
| Ekspor terbaru · 6 Nov | 127.713 dan 141.781 catatan per detik, siklus lengkap | Dua akun per server; teks dan metadata melalui WARP |
| Arsip yang disimpan · 6 Nov | Arsip 48; catatan 3,598,381 telah diverifikasi | Arsip yang ada telah diverifikasi menggunakan kunci ruang kerja yang disematkan |
| Trusted Live · 5 November | Perekaman CPU yang dilindungi dan pemeriksaan WARP | Proses masuk ke Desktop resmi dan ekspor asli tetap tidak memenuhi syarat |
| Phala / Intel TDX · 4 Nov | Semua pemeriksaan verifikator 16 telah lulus pada eksekusi selanjutnya | Penerapan historis; tidak ada akun Telegram di CVM |

**Di halaman ini**

- [Audit rilis dan ekspor terbaru · 6 November 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu dan WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Penerapan Phala Cloud secara langsung · 4 November 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Inventaris jurnal server langsung · 1 November 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Pemeriksaan offline dan injeksi kesalahan terbaru · 1 November 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Pengujian Telegram langsung, seluruh akun · 29 Oktober 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Ekspor yang dilindungi kata sandi dibuka dengan libarchive · 29 Oktober 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Uji coba Telegram langsung · 27 hingga 29 Oktober 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Pengukuran kapasitas lokal sintetis](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Pencarian teks lengkap pada satu juta pesan · 5 November 2026](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Kualifikasi yang tersisa](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#remaining-qualification)

## Audit rilis dan ekspor terbaru · 6 November 2026

Audit ini menggunakan v0.9.1 pada sumber `92e539af40d8368d198ff5e040f1d876f2c1310e`, rilis `92e539af40d8-83e41104669e`. Pemeriksaan awal paket yang terinstal berhasil di tiga server. Laporan yang ditandatangani mempertahankan kondisi yang diamati pada saat itu.

[![Tingkat akuisisi dan ekspor lengkap untuk dua beban kerja baru](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Beban kerja | Merekam | Akuisisi | Siklus lengkap | Tingkat siklus lengkap |
| --- | --- | --- | --- | --- |
| Server A · dua akun | 27,030 | 189.043 s | 211.647 s | 127.713 catatan/detik |
| Server B · dua akun | 29,299 | 182.513 s | 206.650 s | 141.781 catatan/detik |

Kedua ekspor dimulai tanpa melanjutkan proses sebelumnya, mengecualikan lampiran dan avatar, serta berakhir tanpa adanya catatan duplikat atau yang digunakan kembali. Siklus lengkap mencakup persiapan, akuisisi, seleksi, pengemasan, dan verifikasi arsip. Server A juga menjalankan pemeriksaan pembacaan obrolan terlindungi. Empat peristiwa FloodWait di A dan tiga di B dipatuhi. Pengamatan ini tidak menjamin throughput secara umum.

| Periksa | Hasil | Kualifikasi |
| --- | --- | --- |
| Inti pytest | 1,461 lulus | Platform 37 melewati |
| Browser / pengalaman pengguna browser / bukti / situs | 102 / 66 / 15 / 9 lulus | Program-program ini tumpang tindih dengan pengujian lain; jumlahnya tidak dapat dijumlahkan |
| Addon Capture | 124 lulus | Tiga pemeriksaan Web Resmi diblokir oleh sandbox Chromium yang diwajibkan |
| Otorisasi API | Rute 269; permintaan 538 berhasil | Kredensial yang hilang dan akses yang dicabut |
| Arsip yang disimpan | 48 dari 48 telah diverifikasi | Catatan 3,598,381; kunci ruang kerja yang disematkan |
| Pemeriksaan pembacaan armada secara langsung | Profil 24 dari 40 lulus | Rute WARP 16 gagal memenuhi syarat; profil-profil tersebut tidak terhubung |

Laporan [yang ditandatangani](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) mencatat semua temuan terbuka, termasuk tiga cacat dalam cuplikan obrolan rahasia yang belum dipublikasikan dan tidak terdapat dalam build utama yang diaudit. Kualifikasi [riwayat publik](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) sebelumnya menggunakan revisi dan beban kerja yang berbeda; tingkatnya tidak boleh digabungkan dengan perbandingan ini.

Verifikasi laporan asli menggunakan kunci [yang disematkan dan verifikator](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Tanda tangannya melindungi laporan operator dari perubahan. Ini bukanlah pengesahan independen, bukti kepenulisan Telegram, atau sertifikasi GDPR.

## Trusted Live CPU Ubuntu dan WARP · 5 November 2026

Proses integrasi yang dipertahankan menggunakan mesin tamu Ubuntu 24.04.5 yang hanya menggunakan CPU (4 vCPU, 8 GiB) di bawah QEMU di dalam host CPU RunPod. Pengumpul menggunakan `14e642a5`; verifikasi menggunakan `02072461`. Perbaikan akhir digabungkan dalam [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) sebagai `755f78f6`, yang pohonnya sesuai dengan kepala PR yang diuji. Ini bukan TEE.

- Sebuah WARP Connector asli dilaporkan dalam kondisi baik; HTTPS yang diproksi melaporkan bahwa WARP dan Gateway telah diaktifkan. Tiga probe mendeteksi alamat keluar yang sama, bukan jaminan alamat IP tetap.
- Memutuskan koneksi WARP menyebabkan permintaan yang diproksi gagal. HTTPS layanan gateway langsung ditolak. Di ruang nama perekam, IPv4/IPv6 langsung, DNS eksternal, dan penyelesai UDP tertanam Docker diblokir.
- Token penyedia yang hanya dapat dibaca dan memiliki cakupan tertentu dapat membaca status kesehatan/koneksi, tetapi tidak dapat membaca token pendaftaran konektor. Pengamatan penyedia yang ditandatangani mencakup sampel yang secara eksplisit tidak tersedia. Saksi berjalan di host operator, sehingga hal ini menunjukkan proses perekaman dan penyimpanan, bukan penyimpanan oleh pihak ketiga yang independen.
- Desktop Resmi mencapai layar sambutan tanpa otentikasi. Masukan keyboard yang dilindungi ditolak selama proses penangkapan. Tiga segmen tampilan H.264 telah diterjemahkan dan overlay jamnya telah diperiksa. Arsip pra-penerbangan peristiwa 18 telah diverifikasi berdasarkan kunci perekam yang disematkan dan titik pemeriksaan yang disimpan.
- Uji penangkapan akhir berhasil melewati kasus-kasus 114 di CI Windows dan Linux, dengan Chromium/FFmpeg yang sebenarnya. Lima uji jangkar dan pemeriksaan saran ketergantungan berhasil dilalui.

Proses awal 2 vCPU/4 GiB mengalami timeout saat beban pembuatan gambar bersamaan dan dihentikan oleh mekanisme pengaman; hal ini tidak dihitung sebagai keberhasilan. Masuk akun uji coba secara manual, ekspor obrolan asli, perbandingan hibrida nyata, dan keluar dari Telegram masih menunggu. Tidak ada sesi Telethon yang disediakan yang diimpor. Lampiran, OCR otomatis, verifikasi drand BLS lokal, dan pengesahan Trusted Live TDX tidak memenuhi syarat.

## Penerapan Phala Cloud langsung · 4 November 2026

**Hasil historis:** penerapan selanjutnya lulus semua pemeriksaan verifikator 16, termasuk Intel TDX dan quick tunnel. Bukti restart, penemuan alamat yang ditandatangani, dan cap waktu laporan diperiksa secara terpisah. Setiap CVM pengujian dihapus setelah dijalankan.

| Pengaturan | Nilai yang terekam |
| --- | --- |
| Penyedia | Phala Cloud · `tdx.small` · US-WEST-1 |
| Penerapan | `--provider phala --quick-tunnel`; ruang kerja awalnya kosong |
| Pengumpul awal | `df7d860c` · v0.8.1 |
| Collector dengan semua perbaikan | `53a0f7e9` |
| Tamu produksi | `dstack-0.5.12`; Akses SSH dinonaktifkan |
| Layanan eksternal | ntfy.sh, GitHub, dan Intel PCS |
| Biaya yang diamati | Tujuh CVM, total sekitar 1.9 sen AS; harga uji historis |

Urutan di bawah ini memisahkan kegagalan awal, perbaikan, dan pemeriksaan yang telah diselesaikan. Tidak ada akun Telegram yang terhubung ke CVM-CVM ini.

**Penerapan 1–2 · perbedaan penyedia dan pemeriksaan regresi**

Dua deployment pertama menemukan lima perbedaan dari Phala Cloud yang disimulasikan. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) kini mereproduksi masing-masing perbedaan tersebut, dan gagal tanpa perbaikan:

| Di Phala Cloud | Sebelum perbaikan | Perbaikan |
| --- | --- | --- |
| `compose_file.name` diperlukan | HTTP 422, tidak ada yang dibuat | Konfigurasi Docker Compose memuat nama CVM |
| Kecuali jika diberikan yang kosong, Phala menambahkan skrip pra-peluncuran miliknya sendiri ke app-compose yang diukur (v0.0.20: login Docker, `docker compose pull`, kata sandi root, kunci SSH dari `user_config`) | `tdx_compose` gagal: kode di luar konfigurasi Docker Compose yang dipublikasikan | App-compose menetapkan `pre_launch_script` menjadi `""`; Phala kemudian mengabaikannya |
| Tanpa `image`, Phala memilih `dstack-dev-0.5.12`, build pengembangan, dengan akses SSH diaktifkan | `server_state` gagal. Hanya catatan pengesahan perangkat keras yang lolos pada gambar ini; hanya catatan penyedia dan `tdx_os` yang menunjukkannya | Proses penyebaran meminta build produksi dari rilis Phala saat ini, `dstack-0.5.12` |
| Dengan gateway dstack dimatikan, detail CVM tidak pernah menerima kode kesalahan `instance_id` | Proses penyebaran menunggu selama 30 menit dan gagal | ID instans dibaca dari status CVM |
| Restart, penghentian, dan penyalaan adalah operasi CVM, bukan revisi aplikasi | `provider_actions` tidak mencantumkan restart | Operasi-operasi tersebut juga dibaca |

**Penerapan 3 · pengesahan, pemeriksaan akses, dan bukti restart**

- CVM menjalankan `dstack-0.5.12` dengan akses SSH dinonaktifkan. Pengumpul memposting alamat yang telah ditandatanganinya sekitar 1,5 menit setelah pembuatan. Proses penyebaran kemudian berhasil melewati `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, catatan pengesahan perangkat keras v4, FMSPC `20a06f000000`, tidak dalam mode debug, tidak dapat dimigrasikan, mendukung data verifikasi kriptografi yang diambil dari Intel), `tdx_compose_hash`, `tdx_compose` (byte per byte), dan `tdx_identity` (kunci KMS).
- Panel di alamat trycloudflare.com merespons dengan kode 401 tanpa token atau dengan token yang salah, dan 200 dengan token panel.
- `verify` dengan `--source` diatur ke arsip GitHub dari commit tersebut dan sidik jari yang diserahkan secara terpisah: server, `server_state`, firewall (tanpa gateway, tanpa titik akhir publik), log penyedia, laporan, sidik jari, hash sumber, boot, dan lima pemeriksaan `tdx_*` berhasil dilalui. Cloudflare dan `tdx_os` tidak tersedia, sehingga hasilnya adalah INCOMPLETE.
- Dua kali restart melalui API Phala: setiap kali CVM kembali aktif dalam waktu kurang dari dua menit dengan kunci pengumpul yang sama, alamat baru yang ditandatangani, dan alamat lama yang merespons 530. `verify` melaporkan boot baru dan kedua kali restart tersebut sebagai REVIEW. Dengan `--evidence`, sistem mengonfirmasi tanda tangan jurnal serta tiga kali proses booting, masing-masing dengan catatan pengesahan perangkat keras Intel TDX tersendiri dari CVM yang sama.
- `destroy` hanya menghapus CVM tersebut. Ruang kerja kemudian menjadi kosong, dan alamat panel berhenti menanggapi.
- Pemeriksaan harga pada panel wizard menunjukkan `tdx.small` sebesar $0,058 per jam. Kunci yang salah menghasilkan pesan sederhana "tidak menerima kunci API".

**Perbaikan lanjutan · penemuan alamat yang ditandatangani dan pengukuran sistem operasi**

- Tanpa kunci alamat, `verify` mengikuti posting terbaru yang terstruktur dengan baik mengenai topik alamat, yang tercantum dalam konfigurasi Docker Compose yang dipublikasikan. Satu posting palsu mengirimkannya ke host yang tidak ada, dan `statement` gagal: seorang pemalsu tidak dapat menyamar sebagai pengumpul, tetapi dapat menghalangi verifikasi pihak ketiga, hingga 12 jam dengan cap waktu masa depan yang dipalsukan. Kolektor kini juga memposting alamatnya yang ditandatangani dengan kuncinya sendiri; `verify` hanya menerima postingan semacam itu ketika kolektor yang membuatnya, dan postingan diurutkan berdasarkan waktu penerimaan ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) memutar ulang postingan yang dipalsukan. Sebuah CVM hanya menjalankan ini dari sebuah commit yang mengandungnya, sehingga pengumpul pada eksekusi ini belum menandatangani alamatnya dan `verify` menyatakan hal tersebut.
- `tdx_os` tidak dapat dijalankan tanpa `dstack-mr`, yang versi saat ini memiliki `measure-os`, bukan `measure --json` seperti yang disebutkan dalam dokumentasi. Verifikator kini menghitung MRTD dan RTMR0-2 sendiri dari gambar yang dipublikasikan dan bentuk VM, termasuk tabel ACPI.

**Penerapan 4 · semua pemeriksaan 16, segel laporan, dan verifikasi ulang**

- Deploy mengunduh `dstack-0.5.12` yang dipublikasikan sekali, mencocokkannya dengan hash gambar OS yang dilaporkan oleh CVM , dan `tdx_os` lulus: MRTD, RTMR0, RTMR1, dan RTMR2 sama dengan nilai yang dihitung untuk QEMU 8.2.2, 1 vCPU, dan 2 GiB. Perhitungan yang sama menghasilkan nilai RTMR0 yang berbeda untuk klaim 4 GiB, 2 vCPU, QEMU 9.2.1, atau kartu jaringan kedua, serta gagal untuk kernel, firmware, atau baris perintah yang diubah serta untuk citra pengembangan.
- `verify` lulus semua dari 16 pemeriksaan yang dilakukannya, termasuk konektor quick tunnel, sehingga hasilnya adalah LULUS. Sistem tersebut menulis sertifikat HTML dan PDF, yang disegel secara digital dengan tanda tangan dan cap waktu menggunakan cap waktu eIDAS yang memenuhi syarat dari unit cap waktu pemerintah Belgia TSU 202301 (status disetujui dalam daftar tepercaya Belgia), cap waktu FreeTSA, dan tanda tangan verifikator; `check-report` mengonfirmasi semuanya serta tanda tangan pada PDF tersebut.
- Setelah restart, `verify --evidence` mengonfirmasi dua kali proses booting, masing-masing disertai dengan pengesahan perangkat keras yang dihasilkan di dalam CVM dan masing-masing dibooting dari `dstack-0.5.12` yang telah dipublikasikan; proses restart dan booting baru tersebut berstatus REVIEW.
- `destroy` meninggalkan ruang kerja dalam keadaan kosong.

**Penerapan 5 · penemuan yang ditandatangani oleh pengumpul dan penolakan posting palsu**

Pengumpul dijalankan mulai dari commit `53a0f7e9`, yang mencakup perbaikan di atas.

- Pengumpul memposting alamatnya yang ditandatangani dengan kunci miliknya sendiri, di samping postingan HMAC milik operator. Dua postingan palsu kemudian ditambahkan ke topik tersebut, satu dengan HMAC bernilai nol dan satu lagi ditandatangani oleh kunci Ed25519 lain, keduanya mengklaim waktu pada tahun 2096. `verify` mengambil alamat yang ditandatangani oleh kunci pengumpul dan lulus semua 16 pemeriksaan; segel tersebut kembali memuat cap waktu Belgia yang terakreditasi, cap waktu FreeTSA, dan tanda tangan verifikator, dan `check-report` mengonfirmasi semuanya.
- Setelah restart, pengumpul memposting alamat baru yang ditandatangani: `verify` langsung menemukannya, **operator menemukan alamat saat ini,** 27 detik kemudian dari postingan HMAC, dan keduanya mengabaikan postingan palsu tersebut. `verify --evidence` mengonfirmasi dua kali booting dari `dstack-0.5.12`.
- Deploy mencantumkan biaya yang ditagihkan Phala kepada CVM, termasuk disk: $0,06078 per jam.

### Wizard panel dan cakupan yang tersisa

Wizard panel dijalankan di Phala Cloud dua kali, sekali melalui API tugasnya dan sekali melalui browser dengan Chromium asli: pemeriksaan harga, pembuatan dengan commit di bawah **Advanced**, keenam pemeriksaan sertifikasi lulus, daftar server menampilkan harga yang ditagih (44,37 USD per bulan), **Find alamat saat ini**, pengunduhan konfigurasi Docker Compose yang diukur, dan penghapusan. Browser tidak mendeteksi kesalahan halaman apa pun. Setiap kali, ruang kerja menjadi kosong setelahnya.

Tidak termasuk: domain Cloudflare di Phala, akun Telegram di CVM, dan gambar `dstack-0.6.1`. Harga wizard sebelum pembuatan hanya mencakup harga komputasi Phala, karena API-nya hanya mencantumkan harga disk untuk CVM yang sudah ada; daftar server menampilkan harga yang ditagihkan setelah pembuatan. Semua harga dalam bagian ini diamati pada tanggal 4 November 2026.

## Inventaris jurnal server langsung · 1 November 2026

Sekitar pukul 19:15 UTC, kueri SQLite `query_only` berurutan yang hanya dapat dibaca menghitung peristiwa dalam sepuluh basis data ruang kerja pada server yang sedang berjalan. Pengumpulan data berlanjut selama kueri berlangsung, sehingga ini bukanlah cuplikan data atomik yang mencakup seluruh ruang kerja.

| Teramati di sepuluh basis data ruang kerja | Jumlah |
| --- | --- |
| Ruang kerja dengan setidaknya satu peristiwa `message.new` | 8 |
| Catatan jurnal, termasuk peristiwa operasional | 1,610,818 |
| Peristiwa `message.new` | 900,232 |
| Peristiwa `message.edited` | 80,683 |
| Peristiwa `message.deleted` | 400,536 |
| Peristiwa `message.recovered` | 53,403 |
| Peristiwa `message.snapshot` | 2,183 |
| Peristiwa `media.saved` | 50,418 |
| Peristiwa `media.failed` | 5,575 |
| Peristiwa `coverage.gap` | 11 |
| Byte basis data, tidak termasuk berkas WAL dan media | 7,909,003,264 |

Ini adalah **jumlah peristiwa**, bukan pesan, orang, atau file media yang unik. Pesan yang sama dapat muncul di lebih dari satu ruang kerja, dan pengeditan atau penghapusan dapat menghasilkan peristiwa jurnal lainnya. `media.failed` menghitung peristiwa kegagalan historis, bukan antrian media saat ini. Kueri-kueri tersebut **tidak** memverifikasi ulang tanda tangan dan rantai hash lengkap dari seluruh 1,610,818 catatan, mengukur pengiriman atau throughput, atau memastikan bahwa setiap peristiwa Telegram terekam. Tidak ada isi pesan, ID akun atau obrolan, label ruang kerja, kredensial, atau berkas pribadi yang dipublikasikan di sini.

Pada tinjauan ini, monitor publik yang dikonfigurasi secara terpisah mencakup tiga sumber: satu respons penangkapan berstatus OK dan dua lainnya melaporkan `no_response`. Monitor tersebut bukan ringkasan kesehatan sepuluh ruang kerja. `no_response` berarti pengamat tidak dapat mendapatkan respons pada pemeriksaan tersebut; hal ini tidak menunjukkan adanya kehilangan pesan. Uji coba yang lebih kecil pada 29 Oktober di bawah ini memiliki tanda tangan eksplisit dan verifikasi rantai hash tersendiri.

## Pemeriksaan offline dan injeksi kesalahan terbaru · 1 November 2026

Pemeriksaan ini menggunakan data fiktif dan berkas lokal; pemeriksaan ini menambahkan bukti regresi untuk sumber saat ini, bukan pengukuran pengiriman Telegram langsung lainnya:

| Periksa | Apa yang telah diuji |
| --- | --- |
| [Arsip sumber](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Dua build dengan byte sumber yang identik namun waktu file yang berbeda menghasilkan ZIP dan checksum yang sama. Byte arsip dan hash file yang persis sama cocok; file pengujian pribadi tetap tidak termasuk. Kegagalan penulisan yang disimulasikan membuat arsip dan checksum sebelumnya tetap utuh. |
| [Pemulihan ekspor akun](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Kesalahan disk simulasi pada anggota ZIP kedua tidak menghasilkan ZIP yang dipublikasikan maupun ZIP parsial. Proses melanjutkan pemulihan mempertahankan setiap byte tanda terima yang ditandatangani secara identik, menghasilkan arsip yang dapat diverifikasi secara independen menggunakan sidik jari penandatanganan yang diharapkan, dan mempertahankan celah cakupan sintetis sebagai hasil parsial. Pernyataan skala mencegah pemindaian tugas dan tanda terima yang berulang seiring bertambahnya riwayat. |
| [Privasi dengan pengungkapan minimal](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Nama dan alias Unicode sintetis, metadata bersarang, pengirim yang tidak diketahui, serta bidang media telah diperiksa di ketiga mode identitas dan dengan penghilangan teks. Kegagalan batas penyamaran tidak secara diam-diam melemahkan proses penyuntingan; ekspor akun asli yang ditandatangani tetap tidak berubah. |
| [Pengkode media Linux dan OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | [Pemeriksaan CI Docker Linux](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) pada commit `5a9e0814` berhasil melewati uji dengan masukan Ogg/Opus, MP3, M4A, MP4 dengan video, WAV, dan FLAC; kontrol durasi palsu dan referensi berkas sekunder; serta 48 fixture parser yang dimutasi (34 ditolak, 14 berhasil didekode dalam batas). OCR Tesseract asli berjalan dengan byte asli tetap tidak berubah. Dekoder dan OCR berjalan dalam kontainer yang terisolasi dari jaringan tanpa model Whisper. |

Pemeriksaan ini dijalankan dalam alur kerja [(pull-request)](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) dan [(pemeriksaan lengkap)](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml). Pemeriksaan ini menguji batas-batas kegagalan ini, bukan setiap kemungkinan kegagalan penyimpanan atau apakah pengungkapan informasi tersebut secara otomatis aman untuk dipublikasikan. Pemeriksaan media tidak mengukur akurasi pengenalan suara atau pengiriman Telegram. Tinjau setiap turunan sebelum membagikannya.

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

## Pencarian teks lengkap pada satu juta pesan · 5 November 2026

Perintah: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Jurnal bertanda deterministik berisi 1.000.000 pesan sintetis dalam 200 obrolan (bentuk kata dalam bahasa Rusia, Ukraina, Inggris, Mandarin, Jepang, tautan, dan handle) diindeks dalam 71 detik; indeks tersebut memakan ruang 58 MiB di samping jurnal berukuran 1,50 GiB. Pencarian yang paling cocok memakan waktu 9 hingga 190 ms (median), dibandingkan dengan 2,4 hingga 3,2 detik untuk pencarian substring sebelumnya. Hasil lengkap, perangkat keras, dan batasan: [Pencarian teks lengkap](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#benchmark). `tools/test_fulltext.py` juga memverifikasi arsip yang ditandatangani yang dibuat sebelum pencarian teks lengkap (`tools/fixtures/evidence-before-fulltext.zip`) menggunakan verifikator saat ini, serta arsip saat ini dengan verifikator milik arsip tersebut sendiri `verify.py`.

## Kualifikasi lainnya

Jurnal langsung yang disimpan ini mencatat pengumpulan yang sebenarnya, pengeditan, pemberitahuan penghapusan, lampiran, pemeriksaan ulang, dan penanganan batasan laju. Jurnal ini tidak mencatat pengiriman yang lengkap atau matriks terkontrol mengenai visibilitas peran, pihak yang bereaksi, FloodWait yang berkepanjangan, pemblokiran akun, dan pemulihan gangguan jaringan/proses. Penerbitan token QR tetap terpisah dari konfirmasi QR seluler yang telah diselesaikan.

Pemeriksaan Docker/Compose dan instalasi dicatat dalam CI; penerapan Phala yang sebenarnya serta verifikasi cap waktu eksternal dijelaskan di atas. Hal-hal tersebut tidak menjamin beban tinggi yang berkelanjutan, matriks platform/peran langsung yang lengkap, tinjauan keamanan independen, validasi pengarsipan jangka panjang, atau sertifikasi forensik. Status MTProto yang disimpan dan proses penyesuaian telah diimplementasikan; pemutaran ulang langsung atomik tanpa kehilangan data masih belum terwujud. Backfill yang lebih baru melakukan commit pesan dan kursor secara atomik serta mempertahankan Tindakan Terkini yang tersedia, namun cakupan sintetisnya berbeda dari kualifikasi langsung. Lihat [(penerimaan langsung) dan](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) untuk matriks kualifikasi terkendali.

Direktori audit publik  hanya berisi laporan yang telah ditandatangani dan pengukuran agregat. Bukti operasional terperinci, tangkapan layar mentah, dan materi akun tetap bersifat pribadi. Tangkapan layar aplikasi di `docs/assets/` menggunakan data demonstrasi fiktif.
