# Apa yang telah diuji

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/

Uji coba Telegram secara langsung, pemeriksaan otomatis, pemeriksaan browser, dan hal-hal yang masih belum terverifikasi.

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

## Kualifikasi lainnya

Jurnal langsung yang disimpan ini mencatat pengumpulan yang sebenarnya, pengeditan, pemberitahuan penghapusan, lampiran, pemeriksaan ulang, dan penanganan batasan laju. Jurnal ini tidak mencatat pengiriman yang lengkap atau matriks terkontrol mengenai visibilitas peran, pihak yang bereaksi, FloodWait yang berkepanjangan, pemblokiran akun, dan pemulihan gangguan jaringan/proses. Penerbitan token QR tetap terpisah dari konfirmasi QR seluler yang telah diselesaikan.

Pembuatan/pengoperasian Docker, instalasi di Linux/macOS, beban tinggi yang berkelanjutan, tinjauan keamanan independen, tanggapan TSA yang benar-benar independen, validasi pencabutan/pengarsipan sertifikat, dan sertifikasi forensik tetap berada di luar kualifikasi yang tercatat. Penyimpanan status MTProto dan fitur catch-up telah diimplementasikan; replay atomik yang tahan lama masih belum terwujud. Pengumpulan log admin, daftar reaktor tambahan, dan polling singkat prioritas tetap menjadi fitur terpisah. Lihat [penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) untuk matriks kualifikasi terkontrol.

Tangkapan layar dan bukti transaksi lokal yang terperinci terdapat di bawah folder test-results/ (diabaikan oleh Git). Tangkapan layar publik di folder docs/assets/ hanya berisi data demonstrasi fiktif.
