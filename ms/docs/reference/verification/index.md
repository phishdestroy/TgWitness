# Apa yang telah diuji

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/

Ujian Telegram secara langsung, pemeriksaan automatik, pemeriksaan pelayar dan apa yang masih belum disahkan.

Each result below applies to its recorded revision and environment. The [current capability matrix](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) separates implementation, published downloads and remaining qualification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Penyebaran Langsung Phala Cloud · 4 November 2026

`--provider phala --quick-tunnel` dijalankan terhadap **Phala Cloud** (`tdx.small`, rantau US-WEST-1) dengan kunci API Phala Cloud untuk ruang kerja kosong, ntfy.sh sebenar, GitHub dan Intel PCS. CVM memasang commit `df7d860c` (v0.8.1); deploy, verify dan destroy dijalankan dari baris perintah dengan pembetulan di bawah. Tujuh CVM menelan kos kira-kira 1.9 sen AS secara keseluruhannya.

Dua penyebaran pertama menemui lima perbezaan daripada Phala Cloud yang disimulasi. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) kini dapat dihasilkan semula setiap satu, dan gagal tanpa pembetulannya:

| Pada Phala Cloud | Sebelum pembetulan | Betulkan |
| --- | --- | --- |
| `compose_file.name` diperlukan | HTTP 422, tiada apa-apa yang dicipta | Konfigurasi Docker Compose membawa nama CVM |
| Melainkan diberikan skrip kosong, Phala menambah skrip pra-pelancaran sendiri ke dalam app-compose yang diukur (v0.0.20: log masuk Docker, `docker compose pull`, kata laluan root, kunci SSH daripada `user_config`) | `tdx_compose` gagal: kod di luar konfigurasi Docker Compose yang diterbitkan | app-compose menetapkan `pre_launch_script` kepada `""`; Phala kemudiannya mengabaikannya |
| Tanpa `image`, Phala memilih `dstack-dev-0.5.12`, binaan pembangunan, dengan akses SSH diaktifkan | `server_state` gagal. Hanya rekod pengesahan perkakasan pada imej ini yang diluluskan; hanya rekod penyedia dan `tdx_os` yang menampilkannya | Penyebaran meminta binaan pengeluaran untuk keluaran semasa Phala, `dstack-0.5.12` |
| Dengan gateway dstack dimatikan, butiran CVM tidak pernah mendapat `instance_id` | Penempatan menunggu 30 minit dan gagal | ID instans dibaca daripada keadaan CVM |
| Memulakan semula, menghentikan dan memulakan semula adalah operasi CVM, bukan semakan aplikasi. | `provider_actions` tidak menyenaraikan permulaan semula | Operasi baca juga diambil kira |

Penyebaran ketiga:

- CVM menjalankan `dstack-0.5.12` dengan akses SSH dimatikan. Pengumpul menyiarkan alamat yang ditandatangani kira-kira 1.5 minit selepas penciptaan. Deploy kemudian meneruskan `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, rekod pengesahan perkakasan v4, FMSPC `20a06f000000`, tidak dalam mod debug, tidak boleh dialih, menyokong data pengesahan kriptografi yang diperoleh daripada Intel), `tdx_compose_hash`, `tdx_compose` (byte demi byte) dan `tdx_identity` (kunci KMS).
- Panel di alamat trycloudflare.com menjawab 401 tanpa token atau dengan token yang salah, dan 200 dengan token panel.
- `verify` dengan `--source` ditetapkan ke arkib GitHub bagi komit dan cap jari dihantar secara berasingan: pelayan, `server_state`, tembok api (tiada gerbang, tiada hujung awam), log penyedia, kenyataan, cap jari, hash sumber, but dan lima pemeriksaan `tdx_*` lulus. Cloudflare dan `tdx_os` tidak tersedia, jadi hasilnya adalah TIDAK LENGKAP.
- Dua permulaan semula melalui API Phala: setiap kali CVM kembali dalam masa kurang dua minit dengan kunci pengumpul yang sama, alamat yang ditandatangani baharu, dan alamat lama menjawab 530. `verify` melaporkan but baharu dan kedua-dua permulaan semula sebagai TINJAUAN. Dengan `--evidence` ia mengesahkan tandatangan jurnal dan tiga permulaan, masing-masing dengan rekod pengesahan perkakasan Intel TDX tersendiri daripada CVM yang sama.
- `destroy` hanya membuang CVM itu. Ruang kerja kemudiannya kosong, dan alamat panel berhenti menjawab.
- Semakan harga wizard panel membaca `tdx.small` pada $0.058 sejam. Kunci yang salah menerima mesej biasa "tidak menerima kunci API".

Dua penemuan selanjutnya, yang diperbaiki kemudian:

- Tanpa kunci alamat, `verify` mengikuti kiriman terbentuk baik terbaru mengenai topik alamat, yang dicetak dalam konfigurasi Docker Compose yang diterbitkan. Satu kiriman palsu menghantarnya ke hos yang tidak wujud, dan `statement` gagal: seorang pemalsu tidak dapat menyamar sebagai pengumpul, tetapi boleh menyekat pengesahan pihak ketiga, sehingga 12 jam dengan cop masa masa depan palsu. Pengumpul kini juga menyiarkan alamatnya yang ditandatangani dengan kunci sendiri, `verify` hanya menerima siaran sedemikian apabila pengumpul membuatnya, dan siaran disusun mengikut masa penerimaan ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) memutar semula kiriman palsu itu. Satu CVM hanya menjalankannya daripada commit yang mengandungkannya, jadi pengumpul pada larian ini belum menandatangani alamatnya lagi dan `verify` menyatakan demikian.
- `tdx_os` tidak dapat dijalankan tanpa `dstack-mr`, yang versi semasa mempunyai `measure-os` dan bukannya `measure --json` seperti yang dinyatakan dalam dokumentasi. Pemeriksa kini mengira MRTD dan RTMR0-2 sendiri daripada imej yang diterbitkan dan bentuk VM, termasuk jadual ACPI.

Penyebaran keempat, dengan ini:

- Deploy memuat turun `dstack-0.5.12` yang diterbitkan sekali, memadankannya dengan hash imej OS yang dilaporkan oleh CVM, dan `tdx_os` lulus: MRTD, RTMR0, RTMR1 dan RTMR2 sama dengan nilai yang dikira untuk QEMU 8.2.2, 1 vCPU dan 2 GiB. Pengiraan yang sama memberikan RTMR0 yang berbeza untuk tuntutan 4 GiB, 2 vCPU, QEMU 9.2.1 atau kad rangkaian kedua, dan gagal untuk kernel, firmware atau baris perintah yang diubah dan untuk imej pembangunan.
- `verify` lulus kesemua 16 pemeriksaan, termasuk penyambung terowong pantas, jadi hasilnya adalah LULUS. Ia menulis sijil HTML dan PDF, disegel secara digital dengan tandatangan dan cop masa dengan cop masa eIDAS bertauliah daripada unit cop masa kerajaan Belgium TSU 202301 (status diberikan dalam senarai dipercayai Belgium), cop masa FreeTSA dan tandatangan pengesah; `check-report` mengesahkan kesemuanya dan tandatangan PDF.
- Selepas but semula, `verify --evidence` mengesahkan dua permulaan, masing-masing disertai dengan pengesahan perkakasan yang dijana di dalam CVM dan masing-masing diboot daripada `dstack-0.5.12` yang diterbitkan; but semula dan but baru itu adalah REVIEW.
- `destroy` meninggalkan ruang kerja kosong.

Penyebaran kelima menjalankan pengumpul daripada komit `53a0f7e9`, yang mempunyai semua perkara di atas:

- Pengumpul menyiarkan alamatnya yang ditandatangani dengan kuncinya sendiri, di sebelah kiriman HMAC pengendali. Dua kiriman palsu kemudian ditambah ke topik, satu dengan HMAC bernilai sifar dan satu lagi ditandatangani oleh kunci Ed25519 lain, kedua-duanya mendakwa masa pada tahun 2096. `verify` mengambil alamat yang ditandatangani oleh kunci pengumpul dan lulus semua 16 pemeriksaan; meterai itu sekali lagi memaparkan cop masa Belgium yang berkelayakan, cop masa FreeTSA dan tandatangan pengesah, dan `check-report` mengesahkannya.
- Selepas dihidupkan semula, pengumpul menyiarkan alamat baru yang disahkan: `verify` menemuinya serta-merta, **pengendali mencari alamat semasa** 27 saat kemudian daripada siaran HMAC, dan kedua-duanya mengabaikan siaran palsu itu. `verify --evidence` mengesahkan dua permulaan dibootstrap daripada `dstack-0.5.12`.
- Deploy mencetak apa yang Phala bilkan kepada CVM, termasuk cakera: $0.06078 sejam.

Pembantu panel dijalankan pada Phala Cloud dua kali, sekali melalui API tugasnya dan sekali melalui pelayar dengan Chromium sebenar: pemeriksaan harga, penciptaan dengan komit di bawah **Advanced**, semua enam pemeriksaan pengesahan lulus, senarai pelayan memaparkan harga yang dikenakan (44.37 USD sebulan), **Cari alamat semasa**, muat turun konfigurasi Docker Compose yang diukur, dan pemadaman. Pelayar tidak menunjukkan sebarang ralat halaman. Setiap kali, ruang kerja kosong selepas itu.

Tidak termasuk: domain Cloudflare di Phala, akaun Telegram di CVM, dan imej `dstack-0.6.1`. Harga wizard sebelum penciptaan adalah hanya harga komputasi Phala, kerana API-nya hanya menyenaraikan harga cakera untuk CVM yang sedia ada; senarai pelayan menunjukkan harga yang ditagih selepas penciptaan.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Mengira |
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

| Semak | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

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

| Metric | Perhatian |
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

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

Resit terperinci tempatan dan tangkapan skrin berada di bawah test-results/ (diabaikan oleh Git). Tangkapan skrin awam dalam docs/assets/ hanya mengandungi data demonstrasi rekaan.
