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

## Kelayakan tambahan

Jurnal langsung yang disimpan mengesahkan pengumpulan sebenar, suntingan, notis pemadaman, lampiran, semakan semula dan pengendalian had kadar. Ia tidak menetapkan penghantaran menyeluruh atau matriks terkawal mengenai keterlihatan peranan, pelaku tindak balas, FloodWait berpanjangan, larangan akaun dan pemulihan gangguan rangkaian/proses. Penerbitan token QR kekal berasingan daripada pengesahan QR mudah alih yang telah diselesaikan.

Pembinaan/pelaksanaan Docker, pemasangan Linux/macOS, beban tinggi berterusan, semakan keselamatan bebas, tindak balas TSA bebas sebenar, pengesahan pembatalan/arkib sijil dan pensijilan forensik kekal di luar kelayakan yang direkodkan. Keadaan MTProto yang disimpan dan catch-up telah dilaksanakan; replay tahan lama atom masih belum ditetapkan. Pengumpulan log pentadbiran, senarai reaktor tambahan dan tinjauan pantas keutamaan kekal sebagai ciri berasingan. Lihat [penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) untuk matriks kelayakan terkawal.

Resit terperinci tempatan dan tangkapan skrin berada di bawah test-results/ (diabaikan oleh Git). Tangkapan skrin awam dalam docs/assets/ hanya mengandungi data demonstrasi rekaan.
