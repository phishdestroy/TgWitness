# Apa yang telah diuji

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/

Uji coba Telegram secara langsung, pemeriksaan otomatis, pemeriksaan browser, dan hal-hal yang masih belum terverifikasi.

Each result below applies to its recorded revision and environment. The [current capability matrix](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) separates implementation, published downloads and remaining qualification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Penerapan Phala Cloud langsung · 4 November 2026

`--provider phala --quick-tunnel` dijalankan pada **Phala Cloud** yang sebenarnya (`tdx.small`, wilayah US-WEST-1) dengan kunci API Phala Cloud dari ruang kerja kosong, ntfy.sh asli, GitHub, dan Intel PCS. CVM menginstal commit `df7d860c` (v0.8.1); proses deploy, verify, dan destroy dijalankan dari baris perintah dengan perbaikan di bawah ini. Tujuh CVM menghabiskan biaya sekitar 1,9 sen AS secara total.

Dua deployment pertama menemukan lima perbedaan dari Phala Cloud yang disimulasikan. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) kini mereproduksi masing-masing perbedaan tersebut, dan gagal tanpa perbaikan:

| Di Phala Cloud | Sebelum perbaikan | Perbaikan |
| --- | --- | --- |
| `compose_file.name` diperlukan | HTTP 422, tidak ada yang dibuat | Konfigurasi Docker Compose memuat nama CVM |
| Kecuali jika diberikan yang kosong, Phala menambahkan skrip pra-peluncuran miliknya sendiri ke app-compose yang diukur (v0.0.20: login Docker, `docker compose pull`, kata sandi root, kunci SSH dari `user_config`) | `tdx_compose` gagal: kode di luar konfigurasi Docker Compose yang dipublikasikan | App-compose menetapkan `pre_launch_script` menjadi `""`; Phala kemudian mengabaikannya |
| Tanpa `image`, Phala memilih `dstack-dev-0.5.12`, build pengembangan, dengan akses SSH diaktifkan | `server_state` gagal. Hanya catatan pengesahan perangkat keras yang lolos pada gambar ini; hanya catatan penyedia dan `tdx_os` yang menunjukkannya | Proses penyebaran meminta build produksi dari rilis Phala saat ini, `dstack-0.5.12` |
| Dengan gateway dstack dimatikan, detail CVM tidak pernah menerima kode kesalahan `instance_id` | Proses penyebaran menunggu selama 30 menit dan gagal | ID instans dibaca dari status CVM |
| Restart, penghentian, dan penyalaan adalah operasi CVM, bukan revisi aplikasi | `provider_actions` tidak mencantumkan restart | Operasi-operasi tersebut juga dibaca |

Penerapan ketiga:

- CVM menjalankan `dstack-0.5.12` dengan akses SSH dinonaktifkan. Pengumpul memposting alamat yang telah ditandatanganinya sekitar 1,5 menit setelah pembuatan. Proses penyebaran kemudian berhasil melewati `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, catatan pengesahan perangkat keras v4, FMSPC `20a06f000000`, tidak dalam mode debug, tidak dapat dimigrasikan, mendukung data verifikasi kriptografi yang diambil dari Intel), `tdx_compose_hash`, `tdx_compose` (byte per byte), dan `tdx_identity` (kunci KMS).
- Panel di alamat trycloudflare.com merespons dengan kode 401 tanpa token atau dengan token yang salah, dan 200 dengan token panel.
- `verify` dengan `--source` diatur ke arsip GitHub dari commit tersebut dan sidik jari yang diserahkan secara terpisah: server, `server_state`, firewall (tanpa gateway, tanpa titik akhir publik), log penyedia, laporan, sidik jari, hash sumber, boot, dan lima pemeriksaan `tdx_*` berhasil dilalui. Cloudflare dan `tdx_os` tidak tersedia, sehingga hasilnya adalah INCOMPLETE.
- Dua kali restart melalui API Phala: setiap kali CVM kembali aktif dalam waktu kurang dari dua menit dengan kunci pengumpul yang sama, alamat baru yang ditandatangani, dan alamat lama yang merespons 530. `verify` melaporkan boot baru dan kedua kali restart tersebut sebagai REVIEW. Dengan `--evidence`, sistem mengonfirmasi tanda tangan jurnal serta tiga kali proses booting, masing-masing dengan catatan pengesahan perangkat keras Intel TDX tersendiri dari CVM yang sama.
- `destroy` hanya menghapus CVM tersebut. Ruang kerja kemudian menjadi kosong, dan alamat panel berhenti menanggapi.
- Pemeriksaan harga pada panel wizard menunjukkan `tdx.small` sebesar $0,058 per jam. Kunci yang salah menghasilkan pesan sederhana "tidak menerima kunci API".

Dua temuan tambahan, yang telah diperbaiki setelahnya:

- Tanpa kunci alamat, `verify` mengikuti posting terbaru yang terstruktur dengan baik mengenai topik alamat, yang tercantum dalam konfigurasi Docker Compose yang dipublikasikan. Satu posting palsu mengirimkannya ke host yang tidak ada, dan `statement` gagal: seorang pemalsu tidak dapat menyamar sebagai pengumpul, tetapi dapat menghalangi verifikasi pihak ketiga, hingga 12 jam dengan cap waktu masa depan yang dipalsukan. Kolektor kini juga memposting alamatnya yang ditandatangani dengan kuncinya sendiri; `verify` hanya menerima postingan semacam itu ketika kolektor yang membuatnya, dan postingan diurutkan berdasarkan waktu penerimaan ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) memutar ulang postingan yang dipalsukan. Sebuah CVM hanya menjalankan ini dari sebuah commit yang mengandungnya, sehingga pengumpul pada eksekusi ini belum menandatangani alamatnya dan `verify` menyatakan hal tersebut.
- `tdx_os` tidak dapat dijalankan tanpa `dstack-mr`, yang versi saat ini memiliki `measure-os`, bukan `measure --json` seperti yang disebutkan dalam dokumentasi. Verifikator kini menghitung MRTD dan RTMR0-2 sendiri dari gambar yang dipublikasikan dan bentuk VM, termasuk tabel ACPI.

Penerapan keempat, dengan hal-hal berikut:

- Deploy mengunduh `dstack-0.5.12` yang dipublikasikan sekali, mencocokkannya dengan hash gambar OS yang dilaporkan oleh CVM , dan `tdx_os` lulus: MRTD, RTMR0, RTMR1, dan RTMR2 sama dengan nilai yang dihitung untuk QEMU 8.2.2, 1 vCPU, dan 2 GiB. Perhitungan yang sama menghasilkan nilai RTMR0 yang berbeda untuk klaim 4 GiB, 2 vCPU, QEMU 9.2.1, atau kartu jaringan kedua, serta gagal untuk kernel, firmware, atau baris perintah yang diubah serta untuk citra pengembangan.
- `verify` lulus semua dari 16 pemeriksaan yang dilakukannya, termasuk konektor quick tunnel, sehingga hasilnya adalah LULUS. Sistem tersebut menulis sertifikat HTML dan PDF, yang disegel secara digital dengan tanda tangan dan cap waktu menggunakan cap waktu eIDAS yang memenuhi syarat dari unit cap waktu pemerintah Belgia TSU 202301 (status disetujui dalam daftar tepercaya Belgia), cap waktu FreeTSA, dan tanda tangan verifikator; `check-report` mengonfirmasi semuanya serta tanda tangan pada PDF tersebut.
- Setelah restart, `verify --evidence` mengonfirmasi dua kali proses booting, masing-masing disertai dengan pengesahan perangkat keras yang dihasilkan di dalam CVM dan masing-masing dibooting dari `dstack-0.5.12` yang telah dipublikasikan; proses restart dan booting baru tersebut berstatus REVIEW.
- `destroy` meninggalkan ruang kerja dalam keadaan kosong.

Penerapan kelima menjalankan pengumpul dari commit `53a0f7e9`, yang mencakup semua hal di atas:

- Pengumpul memposting alamatnya yang ditandatangani dengan kunci miliknya sendiri, di samping postingan HMAC milik operator. Dua postingan palsu kemudian ditambahkan ke topik tersebut, satu dengan HMAC bernilai nol dan satu lagi ditandatangani oleh kunci Ed25519 lain, keduanya mengklaim waktu pada tahun 2096. `verify` mengambil alamat yang ditandatangani oleh kunci pengumpul dan lulus semua 16 pemeriksaan; segel tersebut kembali memuat cap waktu Belgia yang terakreditasi, cap waktu FreeTSA, dan tanda tangan verifikator, dan `check-report` mengonfirmasi semuanya.
- Setelah restart, pengumpul memposting alamat baru yang ditandatangani: `verify` langsung menemukannya, **operator menemukan alamat saat ini,** 27 detik kemudian dari postingan HMAC, dan keduanya mengabaikan postingan palsu tersebut. `verify --evidence` mengonfirmasi dua kali booting dari `dstack-0.5.12`.
- Deploy mencantumkan biaya yang ditagihkan Phala kepada CVM, termasuk disk: $0,06078 per jam.

Wizard panel dijalankan di Phala Cloud dua kali, sekali melalui API tugasnya dan sekali melalui browser dengan Chromium asli: pemeriksaan harga, pembuatan dengan commit di bawah **Advanced**, keenam pemeriksaan sertifikasi lulus, daftar server menampilkan harga yang ditagih (44,37 USD per bulan), **Find alamat saat ini**, pengunduhan konfigurasi Docker Compose yang diukur, dan penghapusan. Browser tidak mendeteksi kesalahan halaman apa pun. Setiap kali, ruang kerja menjadi kosong setelahnya.

Tidak termasuk: domain Cloudflare di Phala, akun Telegram di CVM, dan gambar `dstack-0.6.1` . Harga yang ditampilkan oleh wizard sebelum pembuatan hanya mencakup biaya komputasi Phala, karena API-nya hanya mencantumkan biaya disk untuk CVM yang sudah ada; daftar server menampilkan harga yang ditagihkan setelah pembuatan.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Jumlah |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Periksa | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

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

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

Tangkapan layar dan bukti transaksi lokal yang terperinci terdapat di bawah folder test-results/ (diabaikan oleh Git). Tangkapan layar publik di folder docs/assets/ hanya berisi data demonstrasi fiktif.
