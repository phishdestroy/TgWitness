# Apa yang telah diuji

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/

Ujian Telegram secara langsung, pemeriksaan automatik, pemeriksaan pelayar dan apa yang masih belum disahkan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bukti dan pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)

![Bukti & pengesahan](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Dikemas kini pada 6 November 2026.** Keputusan dipautkan kepada semakan, persekitaran dan beban kerja yang direkodkan untuk setiap pelaksanaan. [Keupayaan semasa](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) menerangkan aliran kerja yang tersedia; halaman ini merekodkan apa yang sebenarnya telah diperiksa.

[Graf prestasi](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Audit Bahasa Inggeris yang disahkan](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Pengukuran yang boleh dimuat turun](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Bukti terkini | Keputusan | Skop |
| --- | --- | --- |
| Audit pelepasan · 6 Nov | 1,461 ujian teras lulus; 37 platform diabaikan | Sumber `92e539af40d8`; penemuan terbuka dikekalkan |
| Eksport baharu · 6 Nov | 127.713 dan 141.781 rekod/s, kitaran lengkap | Dua akaun setiap pelayan; teks dan metadata melalui WARP |
| Arkib disimpan · 6 Nov | 48 arkib; 3,598,381 rekod disahkan | Arkib sedia ada disemak menentang kunci ruang kerja yang dipasang |
| Dipercayai Langsung · 5 Nov | Perekodan CPU yang dilindungi dan pemeriksaan WARP | Log masuk Desktop Rasmi dan eksport asli kekal tidak terhad |
| Phala / Intel TDX · 4 Nov | Semua pemeriksaan pengesah 16diluluskan pada larian kemudian | Penyebaran sejarah; tiada akaun Telegram pada CVM |

**Pada halaman ini**

- [Audit pelepasan dan eksport baharu · 6 November 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu dan WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Penyebaran Phala Cloud secara langsung · 4 November 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Inventori jurnal pelayan langsung · 1 November 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Semakan luar talian dan suntikan ralat terkini · 1 November 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Ujian Telegram langsung, akaun penuh · 29 Oktober 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Eksport yang dilindungi kata laluan dibuka dengan libarchive · 29 Oktober 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Ujian Telegram langsung · 27 hingga 29 Oktober 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Pengukuran kapasiti tempatan sintetik](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Carian teks penuh pada satu juta mesej · 5 November 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Kelayakan selebihnya](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#remaining-qualification)

## Audit pelepasan dan eksport baharu · 6 November 2026

Audit menggunakan v0.9.1 pada sumber `92e539af40d8368d198ff5e040f1d876f2c1310e`, keluaran `92e539af40d8-83e41104669e`. Semakan asap pakej terpasang lulus pada tiga pelayan. Laporan yang disahkan mengekalkan keadaan yang diperhatikan pada masa itu.

[![Perolehan dan kadar eksport lengkap untuk dua beban kerja baharu](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Beban kerja | Merekod | Pendapatan | Selesaikan kitaran | Kadar kitaran lengkap |
| --- | --- | --- | --- | --- |
| Pelayan A · dua akaun | 27,030 | 189.043s | 211.647s | 127.713 rekod/s |
| Pelayan B · dua akaun | 29,299 | 182.513s | 206.650s | 141.781 rekod/s |

Kedua-dua eksport bermula tanpa resume, mengecualikan lampiran dan avatar, dan berakhir dengan sifar rekod berganda atau yang digunakan semula. Kitaran lengkap merangkumi penyediaan, pengambilan, pemilihan, pembungkusan dan pengesahan arkib. Pelayan A juga menjalankan semakan baca sembang terlindung. Empat acara FloodWait pada A dan tiga pada B telah dihormati. Pengamatan ini tidak menetapkan jaminan kadar aliran umum.

| Semak | Keputusan | Kelayakan |
| --- | --- | --- |
| Inti pytest | 1,461 lulus | 37 platform melangkau |
| Pelayar / UX pelayar / bukti / laman | 102/66/15/9 lulus | Program-program ini bertindih dengan ujian lain; kiraan tidak bersifat penjumlahan |
| Pautan addon | 124 lulus | Tiga pemeriksaan Web Rasmi dihalang oleh Chromium sandbox yang diperlukan |
| Autorisasi API | 269 laluan; 538 permintaan berjaya | Kredensial hilang dan akses yang ditarik balik |
| Arkib yang disimpan | 48 daripada 48 disahkan | 3,598,381 rekod; kunci ruang kerja terpaku |
| Semakan baca armada langsung | 24 daripada 40 profil lulus | 16 laluan WARP gagal kelayakan; profil-profil tersebut tidak bersambung |

[Laporan yang disahkan](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) merekodkan semua penemuan terbuka, termasuk tiga kecacatan dalam snapshot sembang rahsia yang tidak diterbitkan yang tiada dalam binaan utama yang diaudit. [Kelayakan sejarah awam](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) yang terdahulu menggunakan revisi dan beban kerja yang berbeza; kadarnya tidak boleh digabungkan dengan perbandingan ini.

Sahkan laporan asal menggunakan [kunci dan pengesah yang dilampirkan](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Tandatanganannya melindungi laporan pengendali daripada pengubahsuaian. Ia bukan pengesahan bebas, bukti keaslian Telegram atau pensijilan GDPR.

## Trusted Live CPU Ubuntu dan WARP · 5 November 2026

Jalankan integrasi yang dikekalkan menggunakan tetamu Ubuntu 24.04.5 yang hanya menggunakan CPU (4 vCPU, 8 GiB) di bawah QEMU dalam hos RunPod CPU. Pengumpul menggunakan `14e642a5`; pengesahan menggunakan `02072461`. Pembetulan akhir disatukan dalam [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) sebagai `755f78f6`, yang pokoknya sepadan dengan kepala PR yang diuji. Ini bukan TEE.

- Satu Penghubung WARP sebenar melaporkan sihat; HTTPS proksi melaporkan WARP dan Gateway diaktifkan. Tiga probe melihat alamat egress yang sama, bukan jaminan IP tetap.
- Pemutusan sambungan WARP menyebabkan permintaan proksi gagal. HTTPS perkhidmatan gerbang langsung ditolak. Dalam ruang nama perekod, IPv4/IPv6 langsung, DNS luaran dan penyelesai UDP terbina dalam Docker dihalang.
- Token penyedia baca sahaja berbeza skop boleh membaca health/connections dan tidak dapat membaca token pendaftaran penyambung. Pengamatan penyedia yang ditandatangani termasuk sampel yang secara eksplisit tidak tersedia. Saksi dijalankan pada hos pengendali, jadi ini menunjukkan rakaman dan penyimpanan, bukan pemilikan pihak ketiga bebas.
- Desktop Rasmi telah mencapai skrin selamat datang tanpa pengesahan. Input papan kekunci yang dijaga ditolak semasa tangkapan. Tiga segmen paparan H.264 telah didekod dan lapisan jam mereka diperiksa. Arkib pra-penerbangan 18-peristiwa disahkan menentang kunci perekod yang dipasang dan mengekalkan titik pemeriksaan.
- Ujian tangkapan akhir lulus 114 kes pada Windows dan Linux CI, dengan Chromium/FFmpeg sebenar. Lima ujian sauh dan pemeriksaan nasihat kebergantungan lulus.

Permulaan awal 2 vCPU/4 GiB telah tamat masa di bawah beban pembinaan imej serentak dan dihentikan melalui pengawal; ia tidak dikira sebagai kejayaan. Log masuk akaun ujian manual, eksport sembang asli, perbandingan hibrid sebenar dan log keluar di pihak Telegram masih tertangguh. Tiada sesi Telethon yang dibekalkan diimport. Lampiran, OCR automatik, pengesahan drand BLS tempatan dan pengesahan Trusted Live TDX tidak layak.

## Penyebaran Langsung Phala Cloud · 4 November 2026

**Keputusan sejarah:** penyebaran kemudian lulus semua 16 pemeriksaan pengesah, termasuk Intel TDX dan terowong pantas. Masa mula semula bukti, penemuan alamat yang ditandatangani dan cap masa laporan diperiksa secara berasingan. Setiap CVM ujian dikeluarkan selepas ia dijalankan.

| Pemasangan | Nilai yang direkodkan |
| --- | --- |
| Penyedia | Phala Cloud · `tdx.small` · AS-BARAT-1 |
| Penyebaran | `--provider phala --quick-tunnel`; ruang kerja kosong pada mulanya |
| Pengumpul awal | `df7d860c` · v0.8.1 |
| Pengumpul dengan semua pembetulan | `53a0f7e9` |
| Tamu pengeluaran | `dstack-0.5.12`; Akses SSH dilumpuhkan |
| Perkhidmatan luaran | ntfy.sh, GitHub dan Intel PCS |
| Kos yang diperhatikan | Tujuh CVM, kira-kira 1.9sen AS bersama-sama; harga ujian sejarah |

Susunan di bawah memisahkan kegagalan awal, pembaikan dan pemeriksaan yang diselesaikan. Tiada akaun Telegram yang disambungkan ke CVM ini.

**Penyebaran 1–2 · perbezaan penyedia dan pemeriksaan regresi**

Dua penyebaran pertama menemui lima perbezaan daripada Phala Cloud yang disimulasi. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) kini dapat dihasilkan semula setiap satu, dan gagal tanpa pembetulannya:

| Pada Phala Cloud | Sebelum pembetulan | Betulkan |
| --- | --- | --- |
| `compose_file.name` diperlukan | HTTP 422, tiada apa-apa yang dicipta | Konfigurasi Docker Compose membawa nama CVM |
| Melainkan diberikan skrip kosong, Phala menambah skrip pra-pelancaran sendiri ke dalam app-compose yang diukur (v0.0.20: log masuk Docker, `docker compose pull`, kata laluan root, kunci SSH daripada `user_config`) | `tdx_compose` gagal: kod di luar konfigurasi Docker Compose yang diterbitkan | app-compose menetapkan `pre_launch_script` kepada `""`; Phala kemudiannya mengabaikannya |
| Tanpa `image`, Phala memilih `dstack-dev-0.5.12`, binaan pembangunan, dengan akses SSH diaktifkan | `server_state` gagal. Hanya rekod pengesahan perkakasan pada imej ini yang diluluskan; hanya rekod penyedia dan `tdx_os` yang menampilkannya | Penyebaran meminta binaan pengeluaran untuk keluaran semasa Phala, `dstack-0.5.12` |
| Dengan gateway dstack dimatikan, butiran CVM tidak pernah mendapat `instance_id` | Penempatan menunggu 30 minit dan gagal | ID instans dibaca daripada keadaan CVM |
| Memulakan semula, menghentikan dan memulakan semula adalah operasi CVM, bukan semakan aplikasi. | `provider_actions` tidak menyenaraikan permulaan semula | Operasi baca juga diambil kira |

**Penyebaran 3 · pengesahan, pemeriksaan akses dan bukti permulaan semula**

- CVM menjalankan `dstack-0.5.12` dengan akses SSH dimatikan. Pengumpul menyiarkan alamat yang ditandatangani kira-kira 1.5 minit selepas penciptaan. Deploy kemudian meneruskan `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, rekod pengesahan perkakasan v4, FMSPC `20a06f000000`, tidak dalam mod debug, tidak boleh dialih, menyokong data pengesahan kriptografi yang diperoleh daripada Intel), `tdx_compose_hash`, `tdx_compose` (byte demi byte) dan `tdx_identity` (kunci KMS).
- Panel di alamat trycloudflare.com menjawab 401 tanpa token atau dengan token yang salah, dan 200 dengan token panel.
- `verify` dengan `--source` ditetapkan ke arkib GitHub bagi komit dan cap jari dihantar secara berasingan: pelayan, `server_state`, tembok api (tiada gerbang, tiada hujung awam), log penyedia, kenyataan, cap jari, hash sumber, but dan lima pemeriksaan `tdx_*` lulus. Cloudflare dan `tdx_os` tidak tersedia, jadi hasilnya adalah TIDAK LENGKAP.
- Dua permulaan semula melalui API Phala: setiap kali CVM kembali dalam masa kurang dua minit dengan kunci pengumpul yang sama, alamat yang ditandatangani baharu, dan alamat lama menjawab 530. `verify` melaporkan but baharu dan kedua-dua permulaan semula sebagai TINJAUAN. Dengan `--evidence` ia mengesahkan tandatangan jurnal dan tiga permulaan, masing-masing dengan rekod pengesahan perkakasan Intel TDX tersendiri daripada CVM yang sama.
- `destroy` hanya membuang CVM itu. Ruang kerja kemudiannya kosong, dan alamat panel berhenti menjawab.
- Semakan harga wizard panel membaca `tdx.small` pada $0.058 sejam. Kunci yang salah menerima mesej biasa "tidak menerima kunci API".

**Pembetulan susulan · penemuan alamat yang ditandatangani dan pengukuran OS**

- Tanpa kunci alamat, `verify` mengikuti kiriman terbentuk baik terbaru mengenai topik alamat, yang dicetak dalam konfigurasi Docker Compose yang diterbitkan. Satu kiriman palsu menghantarnya ke hos yang tidak wujud, dan `statement` gagal: seorang pemalsu tidak dapat menyamar sebagai pengumpul, tetapi boleh menyekat pengesahan pihak ketiga, sehingga 12 jam dengan cop masa masa depan palsu. Pengumpul kini juga menyiarkan alamatnya yang ditandatangani dengan kunci sendiri, `verify` hanya menerima siaran sedemikian apabila pengumpul membuatnya, dan siaran disusun mengikut masa penerimaan ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) memutar semula kiriman palsu itu. Satu CVM hanya menjalankannya daripada commit yang mengandungkannya, jadi pengumpul pada larian ini belum menandatangani alamatnya lagi dan `verify` menyatakan demikian.
- `tdx_os` tidak dapat dijalankan tanpa `dstack-mr`, yang versi semasa mempunyai `measure-os` dan bukannya `measure --json` seperti yang dinyatakan dalam dokumentasi. Pemeriksa kini mengira MRTD dan RTMR0-2 sendiri daripada imej yang diterbitkan dan bentuk VM, termasuk jadual ACPI.

**Penyebaran 4 · semua 16 pemeriksaan, meterai laporan dan pengesahan semula**

- Deploy memuat turun `dstack-0.5.12` yang diterbitkan sekali, memadankannya dengan hash imej OS yang dilaporkan oleh CVM, dan `tdx_os` lulus: MRTD, RTMR0, RTMR1 dan RTMR2 sama dengan nilai yang dikira untuk QEMU 8.2.2, 1 vCPU dan 2 GiB. Pengiraan yang sama memberikan RTMR0 yang berbeza untuk tuntutan 4 GiB, 2 vCPU, QEMU 9.2.1 atau kad rangkaian kedua, dan gagal untuk kernel, firmware atau baris perintah yang diubah dan untuk imej pembangunan.
- `verify` lulus kesemua 16 pemeriksaan, termasuk penyambung terowong pantas, jadi hasilnya adalah LULUS. Ia menulis sijil HTML dan PDF, disegel secara digital dengan tandatangan dan cop masa dengan cop masa eIDAS bertauliah daripada unit cop masa kerajaan Belgium TSU 202301 (status diberikan dalam senarai dipercayai Belgium), cop masa FreeTSA dan tandatangan pengesah; `check-report` mengesahkan kesemuanya dan tandatangan PDF.
- Selepas but semula, `verify --evidence` mengesahkan dua permulaan, masing-masing disertai dengan pengesahan perkakasan yang dijana di dalam CVM dan masing-masing diboot daripada `dstack-0.5.12` yang diterbitkan; but semula dan but baru itu adalah REVIEW.
- `destroy` meninggalkan ruang kerja kosong.

**Penyebaran 5 · penemuan yang ditandatangani oleh pengumpul dan penolakan kiriman palsu**

Pengumpul dijalankan dari komit `53a0f7e9`, yang merangkumi pembetulan di atas.

- Pengumpul menyiarkan alamatnya yang ditandatangani dengan kuncinya sendiri, di sebelah kiriman HMAC pengendali. Dua kiriman palsu kemudian ditambah ke topik, satu dengan HMAC bernilai sifar dan satu lagi ditandatangani oleh kunci Ed25519 lain, kedua-duanya mendakwa masa pada tahun 2096. `verify` mengambil alamat yang ditandatangani oleh kunci pengumpul dan lulus semua 16 pemeriksaan; meterai itu sekali lagi memaparkan cop masa Belgium yang berkelayakan, cop masa FreeTSA dan tandatangan pengesah, dan `check-report` mengesahkannya.
- Selepas dihidupkan semula, pengumpul menyiarkan alamat baru yang disahkan: `verify` menemuinya serta-merta, **pengendali mencari alamat semasa** 27 saat kemudian daripada siaran HMAC, dan kedua-duanya mengabaikan siaran palsu itu. `verify --evidence` mengesahkan dua permulaan dibootstrap daripada `dstack-0.5.12`.
- Deploy mencetak apa yang Phala bilkan kepada CVM, termasuk cakera: $0.06078 sejam.

### Penyihir panel dan skop yang tinggal

Pembantu panel dijalankan pada Phala Cloud dua kali, sekali melalui API tugasnya dan sekali melalui pelayar dengan Chromium sebenar: pemeriksaan harga, penciptaan dengan komit di bawah **Advanced**, semua enam pemeriksaan pengesahan lulus, senarai pelayan memaparkan harga yang dikenakan (44.37 USD sebulan), **Cari alamat semasa**, muat turun konfigurasi Docker Compose yang diukur, dan pemadaman. Pelayar tidak menunjukkan sebarang ralat halaman. Setiap kali, ruang kerja kosong selepas itu.

Tidak termasuk: domain Cloudflare di Phala, akaun Telegram di CVM, dan imej `dstack-0.6.1`. Harga wizard sebelum penciptaan hanya merupakan harga pengkomputeran Phala, kerana API-nya hanya menyenaraikan harga disk untuk CVM sedia ada; senarai pelayan menunjukkan harga yang dikenakan selepas penciptaan. Semua harga dalam bahagian ini diperhatikan pada 4 November 2026.

## Inventori jurnal pelayan langsung · 1 November 2026

Pada kira-kira 19:15 UTC, pertanyaan SQLite berurutan hanya-baca `query_only` mengira kejadian dalam sepuluh pangkalan data ruang kerja pada pelayan yang sedang berjalan. Pengumpulan diteruskan semasa pertanyaan, jadi ini bukan snapshot atom merentas ruang kerja.

| Diperhatikan merentasi sepuluh pangkalan data ruang kerja | Mengira |
| --- | --- |
| Ruang kerja dengan sekurang-kurangnya satu acara `message.new` | 8 |
| Rekod jurnal, termasuk peristiwa operasi | 1,610,818 |
| Peristiwa `message.new` | 900,232 |
| Acara `message.edited` | 80,683 |
| Acara `message.deleted` | 400,536 |
| Acara `message.recovered` | 53,403 |
| Acara `message.snapshot` | 2,183 |
| Acara `media.saved` | 50,418 |
| Acara `media.failed` | 5,575 |
| Acara `coverage.gap` | 11 |
| Bait pangkalan data, kecuali fail WAL dan media | 7,909,003,264 |

Ini adalah **kiraan peristiwa**, bukan mesej unik, orang atau fail media. Mesej yang sama boleh muncul dalam lebih daripada satu ruang kerja, dan suntingan atau pemadaman boleh menghasilkan satu lagi peristiwa jurnal. `media.failed`mengira peristiwa kegagalan sejarah, bukan barisan media semasa. Permintaan tersebut **tidak** mengesahkan semula tandatangan dan keseluruhan rantaian hash bagi semua 1,610,818 rekod, mengukur penghantaran atau throughput, atau mengesahkan bahawa setiap peristiwa Telegram telah dirakam. Tiada kandungan mesej, ID akaun atau sembang, label ruang kerja, kelayakan atau fail peribadi diterbitkan di sini.

Pada semakan ini, pemantau awam yang dikonfigurasikan secara berasingan merangkumi tiga sumber: satu respons tangkapan adalah OK dan dua melaporkan `no_response`. Pemantau itu bukan ringkasan kesihatan sepuluh ruang kerja. `no_response` bermaksud pemerhati tidak dapat memperoleh respons pada pemeriksaan itu; ia tidak mengesahkan kehilangan mesej. Ujian 29 Oktober di bawah mempunyai tandatangan eksplisit dan pengesahan rantaian hash tersendiri.

## Semakan luar talian dan suntikan ralat terkini · 1 November 2026

Semakan ini menggunakan data rekaan dan fail tempatan; ia menambah bukti regresi untuk sumber semasa, bukan ukuran penghantaran Telegram langsung yang lain:

| Semak | Apa yang ia jalankan |
| --- | --- |
| [Arkib sumber](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Dua binaan dengan bait sumber yang sama tetapi masa fail yang diubah menghasilkan ZIP dan checksum yang sama. Bait arkib dan hash fail yang tepat sepadan; fail ujian peribadi tidak disertakan. Kegagalan menulis yang disimulasi mengekalkan arkib dan checksum sebelumnya utuh. |
| [Pemulihan eksport akaun](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Ralat cakera simulasi pada ahli ZIP kedua tidak menghasilkan sebarang ZIP yang diterbitkan atau separa. Resume mengekalkan setiap resit yang ditandatangani secara byte-identical, menghasilkan arkib yang boleh disahkan secara bebas menggunakan cap jari tandatangan yang dijangka, dan mengekalkan jurang liputan sintetik sebagai hasil separa. Penegasan skala melindungi daripada imbasan tugas dan resit berulang apabila sejarah berkembang. |
| [Pendedahan privasi yang diminimumkan](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Nama dan alias Unicode sintetik, metadata bersarang, penghantar tidak diketahui dan medan media telah diperiksa dalam ketiga-tiga mod identiti dan dengan pengecualian teks. Kegagalan had penutup tidak secara senyap melemahkan redaksi; eksport akaun yang ditandatangani asal kekal tidak berubah. |
| [Pemapar kod media Linux dan OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | [Semakan CI Docker Linux](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) pada commit `5a9e0814` berjaya menjana input Ogg/Opus, MP3, M4A, MP4 dengan video, WAV dan FLAC; kawalan tempoh palsu dan rujukan fail sekunder; serta 48 pemegang parser yang dimutasi (34 ditolak, 14 didekod dalam had). OCR Tesseract sebenar dijalankan dengan bait asal tidak berubah. Dekoder dan OCR dijalankan dalam kontena yang diasingkan rangkaian tanpa model Whisper. |

Semakan dijalankan dalam [permintaan tarik](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) dan aliran kerja [Semakan penuh](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml). Mereka menguji sempadan kegagalan ini, bukan setiap kemungkinan kegagalan penyimpanan atau sama ada pendedahan secara automatik selamat untuk diterbitkan. Semakan media tidak mengukur ketepatan pengecaman ucapan atau penghantaran Telegram. Semak setiap turunan sebelum dikongsi.

## Ujian Telegram langsung, akaun penuh · 29 Oktober 2026

Akaun yang sama terus dijalankan selepas ujian di bawah. Pada 29 Oktober jam 12:10 UTC skopnya telah ditukar kepada keseluruhan akaun (saluran, kumpulan, sembang peribadi dan bot); panel meminta pengesahan dan jurnal yang disahkan mencatatnya. Menjelang 17:59 UTC jurnal tersebut merekodkan:

| Direkodkan, 27 Oktober 21:36 hingga 29 Oktober 17:59 UTC | Mengira |
| --- | --- |
| Rekod jurnal | 9,968 |
| Mesej baru | 5,308 |
| daripada mereka selepas beralih ke akaun sepenuhnya | 3,878 |
| Pembuangan | 784 |
| daripadanya dipadam selepas TgWitness menyimpan mesej tersebut | 596 |
| Suntingan | 41 |
| Mesej ditambah oleh semakan semula | 2,273 |
| Mesej yang tidak dapat ditemui semula oleh semakan semula | 18 |
| Mesej disimpan melalui snapshot sejarah | 242 |
| Lampiran yang disimpan | 247 |
| Pengumpul bermula | 19 |
| Telegram FloodWait berehat | 26 |

- Semakan **Verify** pada panel mengesahkan tandatangan dan rantaian hash bagi semua 9,968 rekod.
- Mesej datang daripada 2 kumpulan atau saluran dan 3 sembang peribadi serta bot. Satu butang mesej telah ditekan daripada **Sembang**; permintaan dan jawapan Telegram terdapat dalam jurnal.
- Sembang baharu ditambah apabila pengumpul mengimbas semula akaun semasa permulaan semula. Penyimpanan mesej awal sembang baharu dimatikan (`history = 0`), jadi ia tidak diliputi di sini.

Tidak diliputi: reaksi, perubahan keahlian, profil orang, penghantaran mesej, penyertaan melalui jemputan, proksi, pemberitahuan, bot saksi dan beberapa akaun sekaligus. Fail awam hanya mengandungi bilangan.

## Eksport terlindung kata laluan dibuka dengan libarchive · 29 Oktober 2026

Satu arkib yang ditulis oleh kod penyulitan eksport (WinZip AES-256, format yang dibaca oleh 7-Zip dan WinRAR) dibuka dengan Windows `tar` (bsdtar 3.6.2, libarchive). Dengan kata laluan yang betul, fail yang diekstrak sepadan dengan SHA-256 asal; kata laluan yang salah ditolak dengan "Incorrect passphrase". 7-Zip dan WinRAR sendiri tidak dijalankan.

## Ujian Telegram langsung · 27 hingga 29 Oktober 2026

Satu akaun Telegram sebenar, yang log masuk melalui kolam pasangan API terbina dalam, merakam satu superkumpulan dari **27 Oktober 21:36 UTC hingga 29 Oktober 05:15 UTC**. Pengumpul dimulakan 12 kali dalam tempoh tersebut.

| Direkod | Mengira |
| --- | --- |
| Rekod jurnal, termasuk denyut nadi dan rekod perkhidmatan | 2,385 |
| Mesej baru | 1,291 |
| Pembuangan | 472 |
| daripada mereka dipadam selepas TgWitness menyimpan teks tersebut | 347 |
| Suntingan | 12 |
| Mesej yang terlepas semasa pemberhentian, ditambah semula oleh semakan semula | 12 |
| Lampiran yang disimpan | 17 |
| Lampiran tidak dimuat turun (pautan muat turun dimatikan, atau tiada fail untuk dimuat turun) | 14 |
| Telegram FloodWait berehat, 3 saat setiap satu, semasa semakan semula | 8 |

- Tandatangan dan rantaian hash bagi semua 2,385 rekod disahkan menentang kunci awam jurnal tersebut.
- Selepas dihidupkan semula, pengumpul akan meneruskan daripada keadaan kemas kini yang disimpan (`pts`) dan Telethon akan mengejar ketinggalan; semakan semula kemudian menambah mesej yang masih hilang.
- Pada setiap FloodWait, pengumpul menunggu masa yang diminta dan meneruskan.
- Akaun kekal log masuk, dan sesi yang sama disambung semula pada 29 Oktober.

Tidak dilindungi oleh ujian ini: beberapa akaun sekaligus, peranan pentadbir, proksi, gangguan yang melebihi beberapa jam dan [prosedur penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) sepenuhnya. Fail awam hanya mengandungi kiraan ini: tiada pengecam akaun atau sembang, mesej atau kelayakan.

## Pengukuran kapasiti tempatan sintetik

Perintah: `python tools/check_capacity.py --events 10000 --chats 100`

| Metrik | Perhatian |
| --- | --- |
| Input | 10,000 peristiwa mesej sintetik merentasi 100 sumber sintetik terpilih |
| Teks mesej | 400 aksara; tiada media atau rangkaian |
| Pengambilan | 53.273 saat; 187.7 peristiwa/saat |
| Kelewatan pengendali | p50 4.162 ms; p95 7.784 ms; maksimum 129.118 ms |
| Eksport ZIP | 19.868 saat dengan tracemalloc diaktifkan |
| Puncak penjejakan peruntukan eksport Python | 0.51 MiB; bukan proses RSS |
| Saiz ZIP | 4,610,962 bait |
| Pengesahan bebas | Semua 10,000 acara disahkan |

Ini mengukur laluan rakaman/pembuangan siri tempatan pada hos Windows ini. Ia tidak mengukur penghantaran MTProto, akaun serentak, pelambatan Telegram, media, beban kerja jangka panjang, atau bilangan sembang sebenar yang dijamin. Pengukuran ini dibuat sebelum wujudnya alat cap masa luar talian akhir, yang tidak mengubah laluan mesej yang diukur.

## Carian penuh teks pada sejuta mesej · 5 November 2026

Perintah: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Jurnal berasingan deterministik sebanyak 1,000,000 mesej sintetik dalam 200 sembang (bentuk kata Rusia, Ukraine, Inggeris, Cina, Jepun, pautan dan nama pengguna) telah diindeks dalam 71 saat; indeks mengambil 58 MiB selain jurnal 1.50 GiB. Carian padanan terbaik mengambil masa 9 hingga 190 ms (median), berbanding 2.4 hingga 3.2 saat untuk carian substring sebelumnya. Keputusan penuh, perkakasan dan had: [Carian teks penuh](https://phishdestroy.github.io/TgWitness/ms/docs/reference/search/#benchmark). `tools/test_fulltext.py` juga mengesahkan arkib berterasai yang dibuat sebelum carian penuh-teks (`tools/fixtures/evidence-before-fulltext.zip`) dengan pengesah semasa, dan arkib semasa dengan arkib tersebut sendiri `verify.py`.

## Kelayakan tambahan

Jurnal langsung yang disimpan mengesahkan pengumpulan sebenar, suntingan, notis pemadaman, lampiran, semakan semula dan pengendalian had kadar. Ia tidak menetapkan penghantaran menyeluruh atau matriks terkawal mengenai keterlihatan peranan, pelaku tindak balas, FloodWait berpanjangan, larangan akaun dan pemulihan gangguan rangkaian/proses. Penerbitan token QR kekal berasingan daripada pengesahan QR mudah alih yang telah diselesaikan.

Docker/Compose dan pemeriksaan pemasangan direkodkan dalam CI; penyebaran Phala sebenar dan pengesahan cap masa luaran diterangkan di atas. Ia tidak mewujudkan beban tinggi berterusan, matriks platform/peranan langsung lengkap, semakan keselamatan bebas, pengesahan arkib jangka panjang atau pensijilan forensik. Status MTProto yang disimpan dan catch-up telah dilaksanakan; replay langsung atomik tanpa kehilangan masih belum ditetapkan. Komit dan penunjuk terkini yang lebih baru dimasukkan secara atomik dan mengekalkan Tindakan Baru-baru Ini yang tersedia, tetapi liputannya yang sintetik berbeza daripada kelayakan langsung. Lihat [penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) untuk matriks kelayakan terkawal.

[Direktori audit awam](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) hanya mengandungi laporan yang ditandatangani dan pengukuran agregat. Resit operasi terperinci, rakaman mentah dan bahan akaun kekal peribadi. Tangkapan skrin aplikasi dalam `docs/assets/` menggunakan data demonstrasi rekaan.
