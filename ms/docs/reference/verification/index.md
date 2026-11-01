# Apa yang telah diuji

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/

Ujian Telegram secara langsung, pemeriksaan automatik, pemeriksaan pelayar dan apa yang masih belum disahkan.

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

Kemasukan lama di bawah menerangkan pelaksanaan mereka sendiri; kebanyakan daripadanya menggunakan klien ujian sintetik. Keputusan automatik terkini terdapat di bawah.

## Senarai MTProxy awam terbina dalam · 29 Oktober 2026

Ini adalah rekod ujian bersejarah bagi binaan pemilihan manual asal. Untuk mod kolam automatik dan IP semasa, lihat [tetapan sambungan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes). Bilangan dan ciri yang tidak disokong di bawah adalah milik revisi yang diuji itu.

Telah menambah snapshot awam terbungkus dan penyegaran HTTPS eksplisit daripada SoliSpirit/mtproto dan zakky8/mtproto-proxy-pro. Pada hos ini, pemuat turun aplikasi memuat turun kedua-dua suapan dengan jayanya pada 29 Oktober 2026 jam 12:58 UTC: **118 hujung unik yang serasi** selepas penapisan, penyahduplikasi dan had 64 entri bagi setiap sumber. Ini mengesahkan pemulihan senarai, bukan kebolehhubungan atau penghantaran mesej melalui hujung tersebut. Tiada akaun sebenar yang disambungkan ke proksi yang disenaraikan semasa kerja ini. [Panduan pengendali dan pengguna](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Respon sumber yang gagal/kosong/tidak serasi mengekalkan entri dan tarikh sebelumnya. Kemas kini tidak mengubah laluan yang dipilih. Alamat awam disahkan dan IP yang diselesaikan dipin semasa pemilihan; laluan operator/manual kekal berasingan. Probe sambungan kini tersedia di panel sebelum log masuk akaun. TLS ee palsu dan pemilihan proksi automatik tetap tidak disokong. Katalog operator sepenuhnya menimpa langganan.

- Suis lengkap: **366 lulus, 3 dilangkau**, 287.94 saat. Amaran kebergantungan sedia ada dan pelepasan platform kekal. Regresi senarai awam/lokalisasi terakhir: **36 lulus**, termasuk penolakan port proksi muat turun yang tidak sah; ini bertindih dengan suis penuh.
- Penerimaan pelayar diluluskan dalam Bahasa Inggeris/Rusia, cahaya/gelap pada 390/1440 piksel: pilihan terbina dalam, tiada muat turun luaran semasa membuka tetapan, kemas kini eksplisit, mengekalkan laluan dan cache semasa kegagalan, tinjauan pra-log masuk, pengasingan ruang kerja tindak balas lewat, butiran sumber dan susun atur/kontras. Tiada ralat JavaScript atau permintaan pelayar luaran.
- Liputan terjemahan statik akhir diluluskan untuk semua 13 lokalisasi; salinan baharu diterjemahkan ke dalam bahasa Rusia dengan pilihan bahasa Inggeris yang jelas di tempat lain. Panduan terbina dalam yang dikemas kini lulus pemeriksaan susun atur/kontras pada kedua-dua tema.
- Semakan kasar dan penerbitan lulus (259 fail awam, 1,354 pautan tempatan); dikemas kini YAML Susun dan CI diparsing. Docker dan CI jauh tidak dijalankan di sini.
- Geara yang dibina semula telah lulus pemasangan terasing, pemuatan senarai bundel dan pengesahan eksport berasingan tandatangan. Semua 69 sumber pakej sepadan dengan ruang kerja; hash sumber telah diperiksa.

Resit: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` dan `test-results/public-proxies-package.log`. Susunan pelayar/akaun/pengangkutan adalah sintetik; dua muat turun suapan di atas adalah permintaan HTTPS sebenar.

## Pembentangan tambahan pilihan · 29 Oktober 2026

Destinasi bot Proof sebelum ini kini dipanggil **Extras**: gambaran ringkas diikuti oleh halaman tetapan berasingan untuk pilihan yang dipilih. Borang saksi mempunyai tiga langkah, dengan pengurusan sambungan, pilihan rangkaian dan butiran penyebaran disembunyikan. GitHub secara eksplisit dirancang dan tidak mempunyai borang kelayakan. [Gambaran keseluruhan Rusia](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- 30 ujian fokus telah lulus untuk penempatan, penyediaan saksi dan pemeriksaan penerbitan.
- Ujian susun atur dan kontras teks latar belakang pepejal Chromium lulus dalam Bahasa Inggeris/Rusia, mod terang/gelap, pada 390/1440 piksel: fokus papan kekunci dan kekunci Enter, tiada sambungan tersirat apabila memilih tambahan, draf pengekalan, muat turun konfigurasi/token yang dipaku, pembersihan token pada kunci, dan pautan panduan tempatan yang berfungsi. Semakan susun atur dan kontras teks latar belakang pepejal telah lulus.
- Persetujuan pertukaran ruang kerja diluluskan, termasuk respons token tertunda yang tiba selepas pertukaran. Navigasi pantas menemui ekstras melalui bot, bukti dan terma GitHub; pemeriksaan 320/390/1440 piksel serta bahasa Rusia/RTL sedia ada juga lulus.
- Tiada ralat JavaScript atau permintaan pelayar luaran dikesan dalam larian penyediaan. Ini adalah pemeriksaan UI sintetik, bukan bukti penerbitan Telegram langsung atau bot baharu.
- Pemuatan bahasa akhir dan liputan kamus diluluskan untuk semua 13 lokalisasi, mengekalkan pilihan bahasa Inggeris eksplisit di luar bahasa Rusia. Panduan Proof yang diperluas juga lulus semakan susun atur/kontras pada 320/768/1440 piksel dalam kedua-dua tema.
- Roda yang dibina semula telah lulus pemasangan terasing dan pengesahan eksport berasingan tandatangan. Semua 67 sumber yang dibungkus sepadan dengan ruang kerja; arkib sumber mengandungi 253 fail awam. Pemeriksaan sumber/pautan lulus untuk 1,346 pautan dokumentasi tempatan.

Resit: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` dan `test-results/extras-artifacts.json`. Aset tangkapan skrin menggunakan ruang kerja sintetik.

## Audit penyediaan bot saksi dan proksi · 29 Oktober 2026

Pemasangan saksi (kini **Ekstra → Bot dalam saluran anda**) menyediakan saksi yang dikerahkan secara bebas: kunci pengumpul terpaku, muat turun token berlingkup, saluran sendiri, dasar penerbitan, laluan HTTP/SOCKS5 dan Bot API tersuai. Token bot kekal pada hos saksi. `--check-config` baharu mengesahkan konfigurasi dan fail tanpa membuka sambungan rangkaian atau mencipta kunci. Laluan fail JSON diselesaikan di sebelah konfigurasi. Semua varian saksi Compose kini meneruskan tetapan proksi HTTP dan Bot API.

Tetapan akaun menyokong katalog MTProxy awam yang diuruskan oleh pengendali, pratonton pautan proksi Telegram tersuai dan medan manual sedia ada. Tindak balas katalog mengecualikan rahsia; pemilihan menyimpan laluan dalam peti keselamatan ruang kerja. Katalog yang hilang atau tidak terbentuk membolehkan laluan manual terus digunakan. Tiada alamat proksi projek atau perkhidmatan saksi yang dihoskan dicipta atau diaktifkan secara lalai. Contoh Caddy hanya mendedahkan hujung utama yang terhad apabila saksi luaran perlu mencapai pengumpul yang panelnya kekal peribadi.

Pengesahan:

- Suis lengkap: **348 lulus, 3 dilangkau**, 195.81 saat. Sekatan Windows menjadi sebab pelarangan; dua amaran penyusutan kebergantungan sedia ada kekal.
- Jalankan regresi saksi/konfigurasi/pembebasan akhir: **11 lulus, 1 dilangkau**. Ini merangkumi keseluruhan suite. Ujian termasuk penyelesaian laluan, pra-penerbangan luar talian, menandatangani/menerbitkan melalui fixtures API Bot HTTP loopback sebenar, kegagalan penghantaran rakaman, pengesahan token saluran dan pengecualian rahsia proksi.
- Persetujuan tetapan Chromium diluluskan dalam Bahasa Inggeris/Rusia pada 390/1440 piksel: muat turun konfigurasi dan token yang dipaku, pembersihan token semasa kunci, pemilihan katalog, pratonton pautan tersuai diikuti dengan simpanan eksplisit, susun atur/kontras dan tiada ralat JavaScript atau permintaan pelayar luaran. Betulkan tajuk akaun Rusia yang sempit dan tetingkap log masuk yang melimpah.
- Ruff, pemeriksaan sumber/pautan dan pemarsian YAML untuk Compose/aliran kerja telah lulus.
- Geara yang dibina semula telah lulus pemeriksaan pemasangan terasing, panel/sumber statik dan pengesahan API, serta pengesahan bebas terhadap eksport sintetik 32 acara secara langsung dan penstriman.

Resit: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` dan `setup-package.log`. Semakan ini menggunakan akaun/proksi sintetik dan fixture Bot API tempatan. Ia tidak menuntut penerbitan bot sebenar, pelayan MTProxy awam yang berfungsi, pelaksanaan CI jauh atau penyebaran Docker. Sejarah pemerhatian Telegram sebenar yang dikekalkan di atas kekal sebagai bukti yang berasingan. [Arahan pemasangan](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Pembentangan dan semakan dokumentasi · 29 Oktober 2026

Halaman produk, skrin akses, README Bahasa Inggeris/Rusia dan imej pembentangan kini berkongsi satu gaya visual. Tangkapan skrin awam menggunakan data demo rekaan. Semakan ini juga telah membetulkan keterangan pengesahan langsung dan pemulihan yang lapuk di atas.

- Lokasi, tapak dan ujian penerbitan tertumpu: **33 lulus, 1 dilangkau**. Ujian yang dilangkau memerlukan penciptaan symlink yang tidak tersedia pada hos ini.
- Persetujuan umum panel Chromium telah diluluskan, termasuk semua katalog bahasa, susun atur RTL, tema cerah/gelap, kontras teks pepejal dan pertukaran ruang kerja. Semakan penciptaan profil kini menunggu respons HTTP sebenar sebelum memeriksa ruang kerja yang dipilih.
- Skrin akses Bahasa Inggeris/Rusia lulus pemeriksaan susun atur dan kontras pada kedua-dua tema pada 320, 390, 768, 850 dan 1440 piksel; butang hantar kekal dalam tetingkap pandangan awal.
- Penerimaan laman awam diluluskan pada 320, 390, 768, 1024 dan 1440 piksel, termasuk mesej kawalan sejarah, pembesaran tangkapan skrin/Escape/kembali tumpuan, tab papan kekunci, penolakan papan klip, subjalur projek, pergerakan dikurangkan dan jalan keluar tanpa JavaScript. Tiada permintaan aset yang gagal, permintaan luaran atau ralat JavaScript dikesan.
- Geara yang dibina semula lulus pemeriksaan pemasangan terasing: sumber panel dan locale pemuatan, akses API memerlukan pengesahan, dan eksport terus/disiarkan secara berasingan memverifikasi semua 32 peristiwa sintetik. Semakan kasar dan sumber terbuka/pautan lulus.

Resit tempatan: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log`, dan `design-package/install-receipt.json`. Suis backend penuh tidak dijalankan semula untuk perubahan pembentangan/dokumentasi ini; hasil sebelumnya kekal dalam audit pra-penerbitan.

## Versi 0.6.1

0.6.1 mengubah paparan panel, pelancar, pembungkusan dan dokumentasi; kod pengumpulan, penyimpanan, penandatanganan dan eksport kekal tidak berubah. Pada Windows 11 / Python 3.12.10 dengan runtime yang dipaku:

- Keseluruhan suite lulus **137 ujian** dengan **2 kali melangkau** dan amaran Starlette sedia ada. Ujian baharu merangkumi pengendalian Ctrl+C pelancar (pelayan mendapat 30 saat untuk pemberhentian yang teratur) dan kegagalan langkah persediaan yang boleh diambil tindakan.
- Chromium (shell tanpa kepala 156) lulus semua **45 senario umum** dan **35 skenario utama import akaun/QR/Auth**, termasuk pemeriksaan kontras teks pepejal, tiada tumpahan mendatar pada 320–1440 px dan medan log masuk pertama yang kelihatan pada 320/390 px. Tiada ralat JavaScript halaman atau permintaan luaran dikesan.
- `python start.py --setup-only` memasang semula pakej sebagai 0.6.1 dan `python start.py --check` melaporkan sedia. Pelayan `python -m tgwitness --demo` sebenar mengembalikan panel, helaian gaya, skrip, logo, panduan dan versi `/api/status` 0.6.1; `workspace.css` yang dialih keluar mengembalikan 404.
- `Start.cmd` menemui pemasangan Python di luar PATH. Apabila tiada Python tersedia ia menunjukkan tawaran pemasangan; menolak arahan manual yang dicetak dan keluar 1. Langkah muat turun dari python.org mendapatkan pemasang 3.12.10 dan lulus pemeriksaan Authenticode Python Software Foundation; pemasang itu sendiri tidak dijalankan pada hos ini.
- `start.sh` tanpa sebarang Python mencetak petunjuk pemasangan dan keluar 1. `scripts\Docker.cmd` dan `scripts/docker-start.sh` diuji terhadap fail boleh laji `docker` palsu: urutan panggilan yang betul, alamat panel dan keluaran token, dan tiada mesej kejayaan selepas kegagalan.
- `python tools/build_portable.py` membina pakej Windows bersaiz 18.8 MiB selepas mengesahkan checksum runtime terbina dalam yang dipinjamkan. Diekstrak ke laluan yang mengandungi ruang kosong dan dimulakan hanya dengan direktori `C:\Windows` pada PATH, Python terbunuhnya memproses `TgWitness-Check.cmd`, memaparkan demo (32 acara) dan ruang kerja langsung, dan Chromium memaparkan jurnal serta laci perincian tanpa ralat JavaScript. Data ditulis ke folder `data` dalam pakej tersebut.
- `python tools/build_preview.py` menghasilkan arkib sumber 110 fail. Uji kering `git add` menyenaraikan 110 fail yang sama tanpa fail sesi, kunci, pangkalan data, token, log atau eksport , tiada laluan mutlak tempatan dan tiada rentetan berbentuk rahsia.

Tidak dijalankan dalam larian pembungkusan 27 Oktober ini: pemasangan Python automatik itu sendiri, pemeriksaan Docker build/Compose, larian Linux/macOS atau latihan akaun langsung baharu. Bukti Telegram sebenar direkodkan di atas dan dalam pemeriksaan akaun awal di bawah. Definisi CI sahaja tidak membolehkan pelaksanaan platform.

## Versi 0.6.0

Suis penuh pin-runtime terkini pada Windows 11 / Python 3.12.10 lulus **135 ujian**, dengan **1 kali lompatan**, dalam masa 26.53 saat dan amaran Starlette sedia ada. Lompatan memerlukan kebenaran POSIX. Selepas menambah pemapar QR ke pemeriksaan kesiapsiagaan dan pengukuran proses, 8 pemeriksaan kesiapsiagaan/ruang kerja yang terjejas juga lulus.

Liputan baharu merangkumi skema Telethon 7/8, skema Pyrogram 2/3, JSON lengkap kunci dan JSON hanya metadata, fail akaun yang sepadan/bertentangan, kod laluan TData, pengubahsuaian checksum dan laluan tidak selamat, penukaran dalam memori luar talian/terpaut, semakan ID akaun dalam talian, kejayaan QR/2FA/tamat tempoh, pembatalan lapuk, dan pengasingan akaun. Fixtures TData menggunakan pelaksanaan AES-IGE berasingan untuk penyulitan.

Chromium telah lulus **45 senario umum** dan **35 senario import akaun/QR/Kunci Auth**, tanpa sebarang ralat JavaScript pada halaman atau permintaan luaran dikesan. Semakan pelayar baharu merangkumi semua empat format input sekaligus, TData yang dilindungi, metadata API, paparan QR, tamat tempoh/cubaan semula, 2FA, penolakan akaun salah, pembatalan kunci/ruang kerja, susun atur responsif, dan respons penukaran lewat selepas pemilihan fail yang lebih baharu.

Kedua-dua suite pelayar lulus semula selepas perubahan kemasukan akaun. Tetapan langsung membuka borang akaun; mod demo membuka jurnal contohnya. Halaman Akaun demo memaparkan arahan permulaan langsung dan menyembunyikan input kelayakan. Semakan fokus pada 320, 390, dan 1440 piksel mengesahkan bahawa medan nombor dan butang utama muat tanpa menatal dan medan API pada mulanya disembunyikan, serta kontras teks kekal boleh dibaca. Kawalan tangkapan dan pengesahan kekal terlindung selepas membuka bahagian boleh-tangani baharu mereka.

Aliran Kunci Auth langsung diuji dengan kelayakan sintetik melalui hujung import dan kebenaran sebenar. Semakan merangkumi kunci tidak lengkap, DC yang hilang, ID Pengguna tidak tepat, identiti akaun tidak sepadan, kelayakan API yang disimpan, kemajuan permintaan yang kelihatan, pembersihan rahsia, dan respons lewat selepas suntingan atau perubahan kaedah. Kesemua empat kaedah log masuk telah diperiksa pada 320, 390, dan 1440 piksel. Pemilih fail didahulukan sebelum panduan format, dan butang Sambung muat dalam tetingkap pandang awal 844 piksel dengan tetapan API dilipat. Tiada pengesahan Kunci Auth sebenar dicuba dalam ujian penerimaan UI ini.

Pembaharuan panel telah diperiksa semula dengan kedua-dua suite pelayar: tiada ralat JavaScript halaman atau permintaan luaran dikesan. Suite akaun kini merangkumi menampal satu pasangan ID/hash API, menolak pasangan yang tidak terbentuk dengan betul atau berbilang pasangan tanpa menggantikan medan, panduan hanya metadata, dan mengabaikan respons import lapuk selepas perubahan kaedah log masuk atau penyuntingan kelayakan secara manual. Enam pemeriksaan fokus tambahan diluluskan untuk panduan persediaan, permulaan/penghentian nyata, pemulihan carian kosong, dan susun atur sambungan akhir/panduan tempatan serta kontras teks yang jelas pada 320, 390, dan 1440 piksel. Kemas kini log masuk terus menambah satu operasi permintaan telefon/kod dan menggunakan semula pasangan API yang disimpan daripada ruang kerja semasa untuk log masuk telefon, QR, dan sesi. Suite Python penuh di atas merangkumi ujian ketahanan baru, penolakan kelayakan separa, dan pengasingan ruang kerja. Semakan pelayar merangkumi kemasukan telefon terus, penggunaan semula maklumat log masuk yang disimpan, penjejakan berasaskan metadata sahaja, kebenaran fail satu butang, dan penolakan akaun dwi. Borang panel-token dan telefon yang disederhanakan juga telah diperiksa tanpa menatal pada mulanya pada saiz 320, 390, dan 1440 piksel. Semakan keserasian mengesahkan borang telefon terus boleh menggunakan hujung konfigurasi/kod terdahulu semasa proses lama masih berjalan.

Satu akaun yang dibekalkan oleh pengguna telah diperiksa secara berasingan, di luar susunan ujian awam. Input Telethon, Pyrogram, dan TData menyelesaikannya kepada kebenaran yang sama; rakan JSON membekalkan kelayakan API. Keempat-empat fail dimuat melalui panel 0.6.0 dan Telegram mengesahkan ID akaun berangka yang dijangkakan. Fail sumber kekal tidak berubah. Tiada sumber dipilih dan pemerhatian kekal dimatikan. Ini menggambarkan satu contoh import/log masuk, bukan pengumpulan secara langsung, pemulihan, atau kapasiti.

Telegram juga mengeluarkan token QR sebenar, yang dibatalkan tanpa diimbas. Aliran pengesahan QR penuh dan 2FA telah diuji menggunakan klien sintetik; pengesahan mudah alih melalui aplikasi Telegram sebenar kekal sebagai langkah penerimaan berasingan. Tiada pengecam akaun sebenar, rahsia, atau tangkapan skrin disertakan dalam fail awam.

Kemas kini pelancar telah selesai; sumber, metadata terpasang, dan penanda kesiapsiagaan melaporkan 0.6.0, dengan qrcode 8.2 dan `pip check` yang lulus. Roda yang dipasang telah berkhidmat kepada panel dan panduan, menolak permintaan API tanpa pengesahan, dan secara bebas mengesahkan eksport sintetik 32-peristiwa secara langsung dan penstriman. Panduan luar talian yang dikemas kini telah diperiksa pada 320, 390, dan 1440 piksel. Tangkapan skrin awam kekal sintetik.

Pelepasan sumber mengandungi 107 fail yang dibenarkan. Pautan dokumentasi tempatan diselesaikan. Pelaksanaan Docker/Caddy, penerbitan CI/pakej jauh, runtime ARM64, pengumpulan berterusan, dan matriks penerimaan Telegram langsung penuh kekal tidak terhad di sini.

## Versi 0.5.1

Pada Windows 11 / Python 3.12.10, keseluruhan suite persekitaran projek lulus: **94 lulus, 2 dilangkau**, dalam 31.21 saat, dengan amaran Starlette sedia ada. Skip memerlukan kebenaran POSIX dan penciptaan symlink yang tidak tersedia pada hos ini. Fixture HTTP muat turun mencetak diagnostik rentetan permintaan; semua pernyataan lulus. Jalankan ini tidak mengesahkan ketiadaan isu pengangkutan hos.

Latihan liputan regresi baharu menolak StringSession, perubahan kod dan akaun 2FA, pencarian identiti yang dibatalkan, pembatalan log masuk yang tertangguh, dan kemas kini melalui penangani berdaftar pada klien aktif, ditolak, digantikan dan probe. Hanya pengumpul aktif menyumbang peristiwa; kelayakan yang disimpan dan sejarah yang ditandatangani kekal utuh. Semakan baharu lain merangkumi carian Unicode selepas membuka semula pangkalan data, penyertaan sempadan dasar pemantauan dalam Coverage, dan pengecualian pembungkusan sumber terbuka.

Projek sebenar `pythonw.exe` melancarkan panel sintetik terasing, memulangkan HTTP 200 dan mengekalkan diagnostik permulaan dalam `logs/server.log`. Log tersebut tidak mengandungi token panel yang dijana atau rekod capaian HTTP. Ujian hanya menamatkan proses sintetiknya sendiri. Tiada tugas Jadual Tugas (Task Scheduler) didaftarkan; logon/log keluar, tidur dan pemulihan perkhidmatan kekal sebagai kelayakan berasingan.

Penerimaan Chromium melepasi **45 senario**, tanpa ralat JavaScript halaman dan tiada permintaan luaran dikesan. Semakan baharu merangkumi tarikh dan masa garis masa 601/768/850 piksel, draf lampiran merentasi penyegaran status, suntingan baharu yang dibuat semasa menyimpan, keputusan pengesahan yang dipadamkan semasa menukar akaun, respons pengesahan lewat selepas berpindah dan kembali, serta sempadan pengesahan eksplisit apabila acara baharu tiba. Jarak ikon/teks carian juga telah diperbetulkan dan suite pelayar dijalankan semula.

Pelaksanaan pelayar menggunakan runtime yang dipinjamkan dalam `.venv` dan Playwright 1.62.0/Chromium sedia ada yang disediakan oleh sistem, disertakan selepas persekitaran projek pada laluan import. Pemasangan kebergantungan pembangunan pilihan dihentikan semasa muat turun Playwright yang perlahan; tiada versi alat pelayar baharu layak. `python start.py --setup-only` biasa melengkapkan peningkatan aplikasi. Sumber, metadata terpasang dan penanda pelancar melaporkan 0.5.1; `pip check` lulus. Semakan kesiapsiagaan lulus pada laluan baharu yang belum digunakan, mengekalkan amaran kunci peti simpanan tempatan yang dijangkakan.

Roda 0.5.1 dipasang secara berasingan dan diuji asap: semua aset panel/panduan dihantar, akses API tanpa pengesahan ditolak, dan kedua-dua ZIP bukti 32-peristiwa secara langsung dan penstriman lulus pengesahan bebas. Fail aplikasi dalam pakej yang dipasang dibandingkan dengan sumber. Arkib sumber awam menggunakan senarai izin jenis fail yang eksplisit dan menolak fail sumber yang dipautkan; bahan runtime yang diletakkan di dalam direktori sumber dikecualikan oleh ujian regresi.

Semasa pelaksanaan pembaikan kod, pemilihan sumber terbuka dan set calon Git mengandungi 86 fail, tanpa direktori data masa-lari disertakan. Imbasan untuk corak kunci peribadi, token GitHub, token bot Telegram dan StringSession yang boleh dikenali tidak menemui sebarang padanan. Ini adalah pemeriksaan corak terhad, bukan audit rahsia menyeluruh. Siasatan peraturan-abaikan merangkumi dua belas artifak akaun/data/eksport biasa. Aliran kerja/isu/Compose YAML dan skrip tugas Windows diparsing dengan jayanya. Pautan dokumentasi tempatan diselesaikan.

Kesemua tujuh penemuan daripada semakan 27 Oktober telah diambil tindakan. Pelaksanaan aliran kerja GitHub, runtime Linux/macOS/Docker, Telegram sebenar, interoperabiliti proksi luar/TSA dan kelayakan beban berterusan kekal di luar pelaksanaan tempatan ini. Tiada penerbitan repositori, pendaftaran perkhidmatan atau pengumpulan akaun sebenar dilakukan.

### Kemas kini dokumentasi Inggeris

Fail README, rujukan akaun/sesi, aliran kerja pengumpulan, dan panduan terbabit kini menerangkan input yang disokong, tingkah laku ruang kerja, dasar peristiwa, dan format eksport dalam Bahasa Inggeris. Tiga tangkapan skrin awam telah dikemas kini menggunakan data sintetik. Pada ketika itu, pilihan sumber terbuka mengandungi 88 fail, termasuk dua panduan baharu. Semua 131 pautan tempatan merentasi 23 dokumen Markdown berjaya diselesaikan.

Selepas pengeditan antara muka dan panduan, penerimaan Chromium sekali lagi lulus kesemua 45 senario, tanpa sebarang ralat JavaScript halaman atau permintaan luaran dikesan. Suis Python penuh tidak dijalankan semula untuk kemas kini dokumentasi dan pembentangan ini; keputusan 94-lulus di atas adalah milik larian pembaikan kod sebelumnya.

Gear yang dibina semula dipasang ke dalam sasaran terisolasi baharu. Panel dan aset panduan nya berfungsi dengan jayanya, akses API tanpa pengesahan ditolak, dan kedua-dua pembuangan data secara langsung dan penstriman lulus pengesahan bebas bagi 32 peristiwa sintetik.

### Kemas kini pemasangan dan penyebaran

Pemeriksaan pemasangan fokus, pembungkusan, dan kesiapsiagaan lulus **14 ujian**, dengan satu kali langkau untuk penciptaan symlink yang tidak tersedia. Pemeriksaan pembungkus asli merangkumi laluan dengan ruang, penghantaran hujah, mod penyediaan/demo, dan penyebaran keluaran bukan sifar. Semakan Git Bash menguji pembantu shell Docker dengan daemon simulasi, termasuk ketiadaan Docker, ketiadaan Compose, menunggu kesihatan yang gagal, dan permulaan port alternatif yang berjaya. Semakan simulasi ini tidak menentukan keserasian masa larian Docker.

Salinan sumber terbuka lengkap dipasang ke dalam direktori Windows baru yang laluannya mengandungi ruang. `scripts\Setup.cmd` mencipta persekitaran baharu dan memasang runtime yang dipin; `Start.cmd --check --json` melaporkan siap tanpa mencipta direktori data sasaran. `pip check` lulus. Roda yang dibina semula juga lulus pemeriksaan pakej terpasang, termasuk eksport 32-peristiwa secara langsung dan penstriman.

Sintaks shell dan lima fail aliran kerja/Compose YAML telah diparsing. Konfigurasi sumber dan imej Compose sepadan pada tetapan storan dan masa larian. Pada peringkat itu, semua 139 pautan tempatan merentasi 23 dokumen Markdown telah diselesaikan. Pilihan sumber terbuka mengandungi 99 fail.

Definisi CI kini menggunakan tetapan asli baharu pada Windows/Linux/macOS, kesihatan Compose/kawalan akses/ketahanan merentasi rekreasi kontena, dan konfigurasi Caddy. Aliran kerja keluaran mengehadkan penerbitan berdasarkan semakan tersebut dan menambah semakan asap ARM64 yang diemulasi. Docker tidak tersedia pada hos ini: pelaksanaan sebenar Compose/Caddy, penerbitan sijil, pelaksanaan ARM64, dan penerbitan aliran kerja/pakej jauh kekal tidak disokong secara tempatan. Kod aplikasi/UI tidak diubah oleh kemas kini ini; keputusan penuh Python dan pelayar sebelum ini tidak dijalankan semula.

## Versi 0.5.0

Keseluruhan suite runtime terpaku lulus: **81 lulus, 1 dilangkau**, dalam 22.00 saat, dengan amaran Starlette sedia ada. Semakan kebenaran POSIX dilangkau pada Windows. Pemproses baharu menguji penghantaran mesej, suntingan, pemadaman berbeza skop/tanpa skop, reaksi, kemas kini peserta dan mesej perkhidmatan keahlian melalui dasar yang berbeza. Kategori yang dilumpuhkan tidak menghasilkan sebarang pemerhatian langsung yang sepadan; diagnostik liputan dan snapshot eksplisit kekal tersedia. Ujian mengesahkan dasar yang disimpan, pemisahan ruang kerja, rekod audit sebelum/selepas yang disahkan, tingkah laku dasar yang tidak berubah, pengesahan ketat dan penglibatan dalam resit proses seterusnya.

Ujian kemasukan demo mengesahkan bahawa keupayaannya berbeza daripada token panel yang dikonfigurasikan, tidak dapat memberi kebenaran kepada ruang kerja langsung, tidak dapat menukar tetapan pengumpulan, dan tidak dikeluarkan atau diterima untuk permintaan jauh, yang disalurkan, rentas asal atau hos tidak sah. Membuka demo yang disimpan tanpa bendera demo yang nyata tidak mengaktifkan kemasukan automatik.

Ujian kelulusan Chromium lulus **39 senario**, termasuk kemasukan demo tempatan tanpa input token, pratetap pemantauan, peralihan daripada pemilihan sumber ke dasar, kebebasan setiap akaun dan pemeriksaan susun atur desktop/320/390 piksel serta kontras teks. Tiada ralat JavaScript halaman. Permintaan yang disuntik oleh AdGuard hos kekal dalam resit. Fail HTTP muat turun mencatat penetapan semula sambungan selepas klien menutup sambungannya; pernyataan masih lulus. Ini bukan keputusan perkhidmatan langsung.

Pelancar biasa telah menaik taraf persekitaran terasing ke 0.5.0; versi sumber dan terpasang sepadan dan pemeriksaan pip lulus. Semakan penyulitan peti rahsia sedia ada, penolakan kunci salah/hilang dan pengesahan tandatangan/pembongkaran media dalam suite penuh lulus. Tiada penyulitan aplikasi baharu bagi kandungan mesej atau lampiran didakwa.

Demonstrasi tempatan dihidupkan semula untuk menjadikan UI yang dikemas kini tersedia. Rekod sintetik sedia ada dikekalkan; menghentikan proses latar belakang demo lama mewujudkan sempadan luar talian pada permulaan seterusnya. Tiada sesi Telegram sebenar digunakan untuk pemeriksaan ini.

Panel localhost:8787 yang sedang berjalan memaparkan versi 0.5.0, akses demo automatik, lima kawalan pemantauan dan 33 peristiwa jurnal sintetik yang disimpan. Panel berasingan yang dipasang 0.5.0 menyediakan semua aset panel/panduan, menolak akses API tanpa pengesahan, dan menghasilkan fail ZIP terverifikasi berisikan 32 acara, sama ada secara langsung atau melalui pembantu muat turun penstriman. Versi pakej runtime kekal seperti yang direkodkan untuk 0.4.

## Versi 0.4.0

Suis penuh runtime yang dipin pin telah lulus: **78 lulus, 1 dilangkau**, dalam 19.77 saat. Semakan yang dilangkau memerlukan kebenaran POSIX; amaran penamatan sokongan Starlette TestClient asal masih wujud. Ujian baharu merangkumi muat turun beraliran/penghalaan ruang kerja, pengepala kebenaran, penolakan untuk menimpa, pengalihan, respons yang dipotong, had saiz yang diiklankan/sebenar, bacaan terhad, pembersihan, sistem fail tanpa pautan keras, kegagalan kesiapsiagaan dan mod pelancar yang tidak boleh memasang pakej. Ujian eksport mengesahkan fail sementara tempatan ruang kerja dan pembersihan anak yatim terpilih.

Penerimaan Chromium melepasi semua 36 senario yang disenaraikan tanpa sebarang ralat JavaScript pada halaman. Ia menguji log masuk telefon/kod/2FA tiruan, sesi yang ditukar, dua ruang kerja dan laluan/status berasingan, pemerhatian, tandatangan, checkpoint dan permintaan cap masa, serta:

- Susun atur desktop dan 320/390 piksel, tiada tumpahan mendatar, navigasi yang kelihatan, dan medan log masuk pertama dalam ruang tontonan awal 844 piksel.
- Kontras teks latar belakang pepejal pada ambang teks WCAG AA. Kawalan yang dilumpuhkan, ketelusan dan latar belakang imej/gradien dikecualikan; ini bukan audit WCAG penuh.
- Tindak balas eksport tempatan sebenar yang ditulis melalui pemilih fail OS tiruan/boleh ditulis, diikuti dengan pengesahan ZIP bebas; pembatalan tidak menghantar sebarang permintaan eksport.
- Kegagalan yang boleh ditulis membatalkan destinasi; sandaran 128 MiB menolak respons beriklan yang terlalu besar tanpa memperuntukkan muatan padanan.
- Panduan tempatan Bahasa Inggeris untuk desktop dan kedua-dua lebar sempit.

Dialog simpan OS dan penulisan pelayar berbilang gigabait sebenar tidak diautomasikan atau dijustifikasi. Ujian muat turun Python menggunakan ketulan terhad dan fixture loopback. Penerimaan penyebaran penuh dengan Telegram sebenar kekal berasingan.

Pemasang biasa menaik taraf `.venv` ke 0.4.0. Sumber dan metadata terpasang sepadan; `pip check` lulus. `python start.py --check --json` melaporkan sedia pada laluan sintetik baharu tanpa mencipta direktori data. Amaran penyimpanan kunci tempatan tetap wujud dengan betul: jurnal/media tidak disulitkan oleh aplikasi.

Gandar 0.4.0 telah dibina dan dipasang ke dalam direktori berasingan. Semua 23 fail aplikasi menepati sumber bait demi bait. Pakej yang dipasang menyediakan panel dan panduan/aset Bahasa Inggeris, menolak akses API tanpa pengesahan, dan mengeksport ZIP sintetik 32-peristiwa yang lulus pengesahan. Perintah muat turun penstrimanannya juga memuat turun ZIP yang disahkan secara bebas daripada aplikasi yang dipasang dan sedang berjalan.

Dokumentasi awam dan panduan tempatan adalah dalam Bahasa Inggeris; pautan dokumentasi tempatan diselesaikan. PowerShell menganalisis templat tugas Windows dan Python menganalisis plist macOS. Ini adalah semakan sintaks, bukan pelaksanaan perkhidmatan. Tiada tugas/perkhidmatan telah didaftarkan. Konfigurasi CI kini merangkumi semakan kesiapsiagaan tetapi CI jauh belum dijalankan di sini.

Jalankan semula pelayar versi 0.4 sekali lagi menyaksikan suntikan hos AdGuard dan pembersihan soket asyncio Windows OSError 10022. Pengesahan pelayar lulus; pemerhatian persekitaran ini dikekalkan dan bukannya dianggap sebagai tingkah laku aplikasi yang tetap. Cubaan awal sandbox OpenSSL/pelayar/pip gagal; larian kelayakan yang berjaya menggunakan pelaksanaan yang diluluskan di luar sandbox.

## Versi 0.3.1 menumpukan pembetulan kesiapsiagaan

Pemeriksaan pelancar, bukti/penyimpanan dan API yang terjejas telah lulus: **31 lulus, 1 dilangkau**, satu amaran Starlette hulu. Pemeriksaan yang dilangkau mengesahkan kebenaran direktori POSIX dan tidak dapat menetapkan kebenaran tersebut pada hos Windows ini. Ujian Python lama mensimulasikan sempadan versi/pengimportan; tiada penafsir Python 3.10 dipasang atau layak. Set ujian 0.3 yang sebelum ini lulus direkodkan di bawah; keseluruhan set ujian dan senario pelayar tidak dijalankan semula untuk perubahan terfokus ini.

Pelancar biasa menaik taraf persekitaran tempatan ke 0.3.1; metadata sumber dan terpasang sepadan, dan pemeriksaan pip lulus. Satu roda 0.3.1 yang dipasang secara berasingan menyediakan panel/aset, menolak akses API tanpa pengesahan dan menghasilkan eksport sintetik 32-peristiwa yang disahkan. YAML aliran kerja diparsing, tetapi pemeriksaan runtime kontena baharu tidak dijalankan: tiada runtime Docker/Podman/Linux tempatan yang boleh digunakan tersedia.

Lihat [penemuan kesiapsiagaan](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) untuk jurang kebolehgunaan, perkhidmatan langsung dan platform yang masih ada. Tampalan ini tidak menyertakan sistem pengendalian tambahan.

## Versi 0.3.0

Suit pin runtime penuh lulus: **61 ujian**, dengan satu amaran deprekasi Starlette TestClient dari hulu. Metadata runtime melaporkan TgWitness 0.3.0 dan python-socks 2.8.2; pemeriksaan pip lulus. Jalankan ujian penerimaan pelayar lulus tanpa sebarang ralat JavaScript pada halaman.

Gear 0.3.0 telah dibina dan dipasang ke dalam direktori pakej berasingan. Ia menyediakan panel dan aset, menolak permintaan API tanpa pengesahan, dan mengeksport jurnal sintetik 32-peristiwa yang lulus pengesahan bebas. Pautan dokumentasi tempatan diselesaikan. Selepas pembetulan normalisasi kunci kosong MTProxy, kesemua sembilan ujian sambungan/keselamatan dijalankan semula dengan jayanya.

Liputan baharu merangkumi:

- Nama pengguna/kata laluan SOCKS5 dan HTTP CONNECT melalui pelayan ujian loopback sebenar; proksi konfigurasi mati gagal daripada beralih semula ke destinasi.
- Pengesahan proksi, pemilihan penghantaran MTProxy, penolakan rahsia TLS palsu, keteguhan, pengasingan ruang kerja, penolakan perubahan semasa memerhati, dan pengecualian rahsia daripada status API dan acara yang ditandatangani.
- Konversi hanya-baca skema SQLite sintetik Telethon 7 dan 8; hash sumber tidak berubah; penolakan format lain, pandangan SQL, dan fail WAL yang belum diselesaikan.
- Kunci induk peti luaran: kunci ruang kerja terbitan berbeza, pembukaan semula berjaya, penolakan kunci salah/tiada, dan tiada migrasi tersirat bagi peti tempatan sedia ada.
- Tetapan proksi pelayar, pembersihan kelayakan, pendedahan perlindungan storan, halaman sambungan mudah alih, kebenaran fail sesi yang ditukar, laluan berasingan, dan semua senario pengumpulan/pembuangan yang telah dibincangkan sebelum ini dengan klien Telegram palsu.

Semasa pembangunan, ujian loopback menunggu tanpa had untuk penutupan rakan sebaya; satu lagi pelaksanaan memerhatikan tetapan semula sambungan Windows selepas jabat tangan. Peranti kini mengehadkan keseluruhan pertukaran dan menganggap EOF/tetapan semula selepas jabat tangan yang lengkap sebagai penutupan sambungan. Pengesahan jabat tangan/autentikasi kekal diperlukan. Ini tidak melayakkan penyedia proksi sebenar atau menunjukkan kecacatan pengangkutan Telegram yang tetap.

Pengamatan permintaan AdGuard hos yang diterangkan di bawah masih terpakai. Tiada akaun Telegram sebenar, di luar proksi SOCKS/HTTP, atau pelayan MTProxy langsung digunakan. MTProxy adalah eksperimental dan pilihan/pengesahan rahsia terpilihnya telah diperiksa, bukan interoperabiliti langsung. Perintah penukaran kunci luaran dan sesi baharu diuji hanya dengan rahsia sintetik. Linux/macOS/Docker kekal tidak disahkan di sini.

Pengukuran throughput 0.2 di bawah tidak diulang dan tidak boleh dibentangkan sebagai penanda aras berbilang akaun/proksi baharu untuk 0.3.

## Versi 0.2.0 asas

Diperiksa pada Windows dengan Python 3.12.10. Tiada akaun Telegram sebenar disambungkan.

| Semak | Keputusan |
| --- | --- |
| Suis Python | 52 lulus dalam persekitaran pembangunan dan 52 lulus dengan runtime yang dipasang; satu amaran deprekasi Starlette TestClient hulu dalam setiap larian |
| Sintaks JavaScript | Dihantar menggunakan Node.js |
| Penerimaan Chromium | Lulus; tiada ralat JavaScript pada halaman |
| Susun atur desktop/mudah alih | Disemak pada 1440 × 1060 dan 390 × 844; tiada tumpahan dokumen mendatar |
| Kandungan mesej berbentuk HTML | Dihasilkan sebagai teks; skrip yang disuntik tidak dijalankan |
| Aliran akaun contoh | Kredensial API → telefon → kod → 2FA → pilih kumpulan → mula → tangkapan → rehat → muat semula |
| Bukti dalam pelayar | Perbandingan suntingan, kandungan asal selepas pemadaman, penapis, muat turun ZIP, titik pemeriksaan, resit proses yang disahkan, muat turun permintaan RFC 3161 dan pengikatan titik pemeriksaan |
| Akaun pelbagai | Memisahkan jurnal, kunci, sumber dan status langsung; bertukar pelayar membiarkan pengumpul lain terus berjalan; ruang kerja dibuka semula selepas mula semula; penolakan duplikasi akaun dan penugasan semula akaun |
| Kegagalan kriptografi | Medan yang ditandatangani telah diubah, medan tanpa tandatangan ditambah, kunci salah, ahli arkib rosak, media diubah/hilang, pemotongan dikesan oleh checkpoint ditolak |
| Penyimpanan | Penambahan serentak disahkan; cubaan kemas kini/pembuangan ditolak; permulaan menolak jurnal yang telah diubah tanpa menambah dan melepaskan kuncinya |
| Ketahanan media | Penulisan mesej/tugas atomik; pemulihan semula; pengekalan penderia versi asal; penolakan penggantian barisan dan kerosakan fail sedia ada; FloodWait diteruskan; kegagalan sumber diasingkan |
| Streaming | Pendahuluan stabil dieksport sementara rekod baru ditambah; titik pemeriksaan yang disimpan mengesan jurnal yang dipotong; eksport tidak mematerialisasikan keseluruhan aliran peristiwa |
| RFC 3161 | OpenSSL 3.5.9 membaca permintaan yang dijana; respons CA/TSA sintetik yang dijana secara tempatan diterima; data diubah, nonce dan CA yang salah ditolak; persekitaran CA sekeliling tidak menafikan kepercayaan eksplisit |
| Pemasangan tempatan | start.py --setup-only telah menaik taraf .venv terasing ke 0.2.0; sumber dan metadata terpasang sepadan; pemeriksaan pip lulus |
| Roda | 0.2.0 dibina dan dipasang secara berasingan di bawah test-results; menyediakan panel/assets, menolak API yang tidak disahkan, mengeksport dan mengesahkan arkib sintetik 32 acara |

Ujian sumber menggunakan FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1, dan Playwright 1.62.0. Runtime yang dipinam menggunakan FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0, dan cryptography 50.0.2. deploy/constraints.txt merekod pin versi runtime; deploy/requirements.lock dan deploy/build.lock menambah SHA-256 bagi setiap fail pakej, dan Docker serta pelayan high-assurance hanya memasang daripadanya (pip --require-hashes). Tiada bukti keserasian pada setiap platform CI yang dikonfigurasi. CI jauh tidak berjalan.

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

## Pengamatan persekitaran

Sekatan sandbox Windows menghalang direktori sementara lalai pytest/pip dan subproses Playwright. Pytest menggunakan direktori sementara baru di dalam projek; proses pemasangan dan pelayar memerlukan pelaksanaan yang diluluskan di luar sandbox.

AdGuard pada mesin telah menyuntik permintaan ke local.adguard.org ke dalam pelayar. Resit pelayar mengekalkan permintaan tersebut. Jalankan ini **bukan** bukti tiada permintaan keluar dalam persekitaran pelayar yang tidak diubah suai; sumber aplikasi itu sendiri tidak mengandungi sebarang permintaan aset luaran/CDN/analitik. Tetapan AdGuard tidak diubah.

Jalankan terakhir pelayar juga mencatat OSError 10022 pembersihan soket asyncio Windows. Semua penegasan pelayar lulus dan tiada ralat JavaScript halaman berlaku. Punyanya tidak dapat dipastikan dan pelaksanaan ini tidak menunjukkan ketiadaan isu pengangkutan hos.

Probe HTTP pakej terpasang pertama yang menggunakan permintaan penutupan sambungan urllib mengalami penetapan semula sambungan, sama ada di dalam dan di luar sandbox dan dengan kedua-dua set kebergantungan. Probe terakhir menggunakan sambungan kekal HTTP/1.1 piawai melalui http.client dan lulus. Permintaan pelayar juga lulus. Asal tepat reset tersebut tidak dapat dipastikan; ia tidak dilabelkan sebagai kecacatan aplikasi yang telah diperbaiki.

## Kelayakan tambahan

Jurnal langsung yang disimpan mengesahkan pengumpulan sebenar, suntingan, notis pemadaman, lampiran, semakan semula dan pengendalian had kadar. Ia tidak menetapkan penghantaran menyeluruh atau matriks terkawal mengenai keterlihatan peranan, pelaku tindak balas, FloodWait berpanjangan, larangan akaun dan pemulihan gangguan rangkaian/proses. Penerbitan token QR kekal berasingan daripada pengesahan QR mudah alih yang telah diselesaikan.

Pembinaan/pelaksanaan Docker, pemasangan Linux/macOS, beban tinggi berterusan, semakan keselamatan bebas, tindak balas TSA bebas sebenar, pengesahan pembatalan/arkib sijil dan pensijilan forensik kekal di luar kelayakan yang direkodkan. Keadaan MTProto yang disimpan dan catch-up telah dilaksanakan; replay tahan lama atom masih belum ditetapkan. Pengumpulan log pentadbiran, senarai reaktor tambahan dan tinjauan pantas keutamaan kekal sebagai ciri berasingan. Lihat [penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) untuk matriks kelayakan terkawal.

Resit terperinci tempatan dan tangkapan skrin berada di bawah test-results/ (diabaikan oleh Git). Tangkapan skrin awam dalam docs/assets/ hanya mengandungi data demonstrasi rekaan.

## Laman web awam dan penyediaan penerbitan · 27 Oktober 2026

Pembinaan pembentangan berasingan `website/` dan Pages ditambah selepas pemeriksaan panel di atas. Tiada konfigurasi akaun langsung atau logik pengumpulan diubah.

- Set aplikasi sedia ada lulus: 138 lulus, 1 lompatan hanya POSIX, dan satu amaran penyahpenggunaan Starlette/httpx hulu. 11 ujian bina tapak yang ditambah lulus secara berasingan, termasuk penolakan output tidak dijangka dan penolakan input berkait.
- Kedua-dua skrip pelayar aplikasi diluluskan menggunakan project-venv Playwright dan Chromium headless shell 156. Tiada ralat JavaScript halaman atau permintaan luaran direkodkan. Semua senario akaun menggunakan pengangkutan palsu dan data rekaan.
- `tools/check_site.py` diluluskan pada lebar 320, 390, 768, 1024, dan 1440, dengan subjalur URL projek URL, tab papan kekunci, akses papan klip berjaya/ditolak, pergerakan dikurangkan, dan JavaScript dilumpuhkan. Tiada permintaan aset gagal atau permintaan luaran berlaku.
- `tools/build_site.py` menghasilkan 10 fail awam yang disenaraikan dibenarkan, kira-kira 460 KB jumlahnya. Skrinshot pelayar dan resit terdapat dalam `test-results/site/` yang diabaikan.
- Gandar dibina dengan jayanya selepas memasang build-only setuptools/wheel tools dalam persekitaran projek. Memasangnya ke dalam sasaran terasing dan menjalankan `tools/check_install.py`, ia lulus: aset statik, kawalan akses, eksport sintetik 32-peristiwa yang ditandatangani, dan muat turun penstriman yang disahkan secara bebas.
- `pip check` lulus. Imbasan corak pada calon awam terpilih oleh Git tidak menemui sebarang blok kunci peribadi yang boleh dikenali, token GitHub/bot/AWS, penugasan rahsia literal panjang, atau penanda konflik gabungan. Ini bukan bukti bahawa setiap format rahsia yang mungkin tiada. Pemeriksaan runtime-data/session/key diabaikan oleh Git.
- Pengesahan GitHub CLI tidak sah; tiada remote dikonfigurasikan dan tiada komit awal wujud. Tiada push, aliran kerja hos, penyebaran Pages, atau keluaran dilakukan. Docker dan kelayakan Telegram/platform secara langsung kekal di luar pemeriksaan ini.

Pada hos ini, kunci muat turun Playwright gagal pada sistem fail ruang kerja E:. Pemasangan Chromium di bawah `%LOCALAPPDATA%/tgwitness-playwright` dan penggunaan `PLAYWRIGHT_BROWSERS_PATH` yang sama untuk pemeriksaan berjaya. Ini adalah jalan penyelesaian persekitaran, bukan perubahan pada kebergantungan masa larian aplikasi.

## Dokumentasi interaktif dan metadata laman web · 29 Oktober 2026

Laman awam membina 12 halaman HTML Bahasa Inggeris: satu halaman utama, satu indeks panduan dan sepuluh panduan. Artifak mengandungi 28 fail pembentangan yang disenaraikan secara eksplisit, kira-kira 1.85 MB, dan tiada data pengumpul. Laman web awam adalah dalam Bahasa Inggeris; terjemahan aplikasi dan panduan repositori yang diterjemahkan adalah berasingan.

- Ujian tapak, penerbitan sumber dan sempadan keluaran: **18 lulus, 2 dilangkau**. Lompatan melibatkan penciptaan symlink pada sistem fail Windows ini. Ujian memeriksa metadata halaman unik, halaman awam hanya dalam Bahasa Inggeris, URL kanonik, semua entri peta tapak aset/pautan tempatan, navigasi berstruktur dan pengecualian fail peribadi.
- Kedua-dua `tools/check_site.py` dan `tools/check_docs_site.py` lulus di Chromium pada 320, 390, 768, 1024 dan 1440 piksel di bawah subjalur URL projek. Panduan ini memeriksa semua 11 halaman dokumentasi, carian dan navigasi papan kekunci, papan klip kejayaan/penolakan dan kandungan yang boleh dibaca tanpa JavaScript.
- Lima contoh interaktif telah diluluskan: main balik/langkah/sejukkan/reset mesej dengan pergerakan dikurangkan dan penggantungan luar skrin; rantaian hash asal/diubah/dibina semula/dipendekkan; keputusan penerimaan/pembatalan/cabang/tiada tindak balas saksi; dan senario penghantaran lengkap/terlambat/hilang; serta peta siasatan yang menghubungkan pemerhatian rentas-bual rekaan berdasarkan ID penghantar, destinasi dan has lampiran. Kawalan penyiasatan lulus semakan navigasi papan kekunci dan sandaran tanpa JavaScript. Hasil SHA-256 pelayar dibandingkan secara bebas dengan `hashlib` Python dan JSON kanonik. Contoh hash itu juga mengekalkan fallback yang boleh dibaca apabila Web Crypto tidak tersedia.
- Peratus penghantaran dan penanda carta dipadankan dengan jadual yang boleh diakses. Label paksi mudah alih diperbesarkan selepas semakan visual. Setiap contoh dilabelkan sebagai ilustratif atau sintetik, dan tiada kenalan contoh pelayar menghubungi Telegram.
- Tiada permintaan luaran, permintaan HTTP yang gagal atau ralat JavaScript direkodkan. Skrin tangkapan desktop/mudah alih dan resit diabaikan di bawah `test-results/site/` dan `test-results/docs-site/`. Indeks dokumentasi, contoh mesej/hash, susun atur saksi, carta penghantaran dan peta siasatan telah diperiksa pada saiz desktop/mudah alih.
- Pemindai penerbitan lulus untuk 282 fail sumber awam dan 1,426 pautan dokumentasi tempatan. Ruff lulus untuk alat dan ujian tapak Python yang diubah suai.
- `docs/HOW-IT-WORKS.md` menyediakan rakan GitHub Markdown dengan diagram dan formula Mermaid. `docs/INVESTIGATION.md` merangkumi skop keseluruhan akaun, pemerolehan sejarah perbualan secara individu, profil orang, rujukan merentas perbualan, garis masa dan penyerahan kes yang disahkan. Langkah-langkah dan hadnya telah diperiksa terhadap skop semasa, pengumpulan, draf, eksport, pengesah dan kod panel. Rendering GitHub yang dihoskan tidak diperiksa.

Ini adalah pemeriksaan laman web/dokumentasi tempatan. Ia tidak menambah kelayakan Telegram langsung, atau menyediakan penyebaran Halaman yang dihoskan, kejayaan CI jauh atau penyenaraian oleh enjin carian. Lihat [prosedur penerbitan](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) dan [nota metadata laman web](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
