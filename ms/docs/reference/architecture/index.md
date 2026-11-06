# Arkitektur

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/architecture/

Komponen pengumpul, panel, jurnal, pekerja dan saksi, dan bagaimana data bergerak di antara mereka.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Development](https://phishdestroy.github.io/TgWitness/assets/chapter-develop.svg)

Satu proses Python menjadi hos panel FastAPI dan sebarang bilangan ruang kerja terasing, setiap satu dengan klien akaun pengguna Telethon. SQLite menyimpan jurnal peristiwa berasingan yang hanya menambah dan tetapan operasi yang boleh diubah. Sebuah peti besi yang disulitkan menyimpan kelayakan API, StringSession, dan kunci penandatanganan. Bahagian hadapan adalah HTML/CSS/JavaScript biasa yang dibundel: tiada pembinaan Node, CDN, atau muat turun bahagian hadapan semasa runtime diperlukan.

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| Modul | Tanggungjawab |
| --- | --- |
| collector.py | Autorisasi, pemilihan dialog, kemas kini, tangkapan skrin, barisan media, pemantauan sambungan |
| interactions.py / telegram_client.py | Tindakan panel yang jelas, resit yang disahkan, ID permintaan berterusan dan dasar percubaan semula callback/sertai tempatan tugas |
| message_content.py | Perbandingan mesej yang dapat diperhatikan, mengecualikan metadata capaian penghantaran |
| workers.py | Tunggu pekerja fail eksport sebelum pembersihan pembatalan |
| distributed_export.py / distributed_pages.py | Concurrent chat jobs, per-account reservations, signed checkpoints and cleanup after archive verification |
| distributed_takeout.py / export_timing.py | Resumable Takeout sessions and timings for each start or resume |
| store.py | Transaksi WAL, rantaian peristiwa teratur, penapis pertanyaan, tetapan operasi |
| fulltext.py | Indeks penuh terbitan (bentuk kata, BM25), diikat pada kepala jurnal yang ditandatangani; tidak pernah dieksport |
| security.py | Penciptaan fail peribadi, peti simpanan disulitkan, tandatangan Ed25519, kunci proses tunggal |
| evidence.py | Eksport jurnal lengkap, derivatif, titik pemeriksaan, pengesahan lampiran |
| verify.py | Pemverifikasi berdiri sendiri, baca sahaja (stdlib + kriptografi): arkib, liputan, jurnal saksi dan kiriman saluran, fail profil |
| app.py | API yang disahkan, kitar hayat, pengesahan permintaan, panel statik |
| profiles.py | Pengumpul akaun pelbagai, pengawal akses dikongsi, kitar hayat setiap ruang kerja |
| access.py | Kebenaran berperingkat, pemeriksaan kebenaran, sekatan IP, had sesi dan konsol pentadbir |
| proxy_catalog.py | Snepakta suapan awam, pemeriksaan pengangkutan, kolam proksi kongsi dan pemilihan berasaskan kesihatan |
| provenance.py | Pengukuran identiti, kod dan kebergantungan yang ditandatangani oleh proses akuisisi |
| network.py | Laluan per-workspace yang disahkan; status dan bukti yang disembunyikan; pilihan pengangkutan Telethon |
| sessions.py | Penukaran hanya-baca luar talian bagi skema SQLite Telethon yang telah disemak |
| account_import.py | Pengesanan dan penormalan dalam memori bagi fail akaun dan JSON yang disokong |
| tdata.py | Pembaca ZIP TData moden terhad, pengesahan checksum/penyahsulit, tiada ekstraksi |
| doctor.py | Semakan kesiapsiagaan tempatan tanpa pengumpulan, log masuk atau pemasangan pakej |
| download.py | Muat turun eksport penstriman yang disahkan dengan bacaan terhad dan tanpa ke atas menulis |
| monitoring.py | Dasar peristiwa setiap ruang kerja dan peraturan lampiran mengikut jenis yang disahkan, dikongsi oleh pengendali, status dan resit yang ditandatangani |
| scope.py | Skop pemerhatian (perbualan terpilih, folder Telegram, keseluruhan akaun), jenis sumber, pengecualian, peringkat semakan semula |
| dossier.py | Profil orang bagi setiap sembang dibina daripada rekod yang disimpan: fakta dengan rujukan rekod, SHA-256/pHash avatar, pengekstrakan sebutan |
| witness_api.py | Token saksi baca sahaja dan tajuk jurnal yang disahkan yang boleh mereka ambil |
| witness.py | Proses saksi bebas: kunci dan jurnal sendiri, pemeriksaan utama, kiriman saluran yang disahkan, eksport |
| alerts.py | Notifikasi Apprise dan senarai notifikasi panel |
| logging_config.py | Log konsol dan diagnostik pelayan berputar untuk pelancaran tanpa tetingkap |
| statik/ | Antaramuka responsif, pintu akses tempatan, penapis, butiran, eksport, tetapan akaun |
| demo.py | Jurnal sintetik dilabel dengan jelas, diasingkan daripada pengumpulan sebenar |

Pengendali pemerhatian didaftarkan sebelum sambungan. Pengumpulan langsung dikawal oleh identiti klien aktif, status pelaksanaan nyata, sumber yang diaktifkan atau skop pemerhatian (mod folder atau akaun penuh menambah sembang baru sebagai sumber pada kemas kini pertamanya), dan dasar acara. Klien yang ditolak dan digantikan tidak dapat menyumbang kemas kini langsung. Reaksi mentah dan kemas kini keahlian mengekalkan had keterlihatan. Kandungan mesej masuk dan tugas media tahan lama-nya disimpan bersama. Tugas mengekalkan penerang TL asal dan mengikat hash-nya kepada pemerhatian mesej yang disahkan. Semantik penghantar/penyunting/pembuang dipisahkan.

Setiap ruang kerja menerima satu akaun dan mempunyai direktori serta identiti tandatangan sendiri. Ruang kerja utama kekal di root untuk keserasian; ruang kerja tambahan terletak di profiles/<id>/. Satu token pemegang mengawal keseluruhan pemasangan; ruang kerja bukan penyewa kebenaran berasingan. Kunci proses melindungi direktori; kunci pangkalan data menyusun selingan peristiwa secara bersiri. Setiap tampalan melakukan komitmen secara serentak ke WAL SQLite dengan mod serentak PENUH. Pencetus kemas kini/pembuangan peristiwa menghalang suntingan aplikasi biasa; pentadbir sistem fail kekal di dalam sempadan kepercayaan.

API authorization is a bearer token. Login operations are serialized and time-bounded. Account uploads use a dedicated 12 MiB encoded-body limit and an 8 MiB decoded-file limit; normal API requests retain the 16 KiB limit. Conversion runs in a worker thread, keeps uploads in memory, and returns normalized input to the authenticated browser. QR login has a per-workspace candidate, short-lived identifier, waiter task, and explicit cancellation. Only accepted authorization becomes the active client. Telegram FloodWait is returned with a Retry-After value; credentials and raw RPC error messages are not exposed in API errors. Journal exports run outside the async event loop and are serialized per workspace. They stream a stable read snapshot alongside continuing WAL writes. Chat acquisition jobs can run concurrently on separate accounts; each account remains reserved until its job stops. A paused or failed job retains its checkpoints. Successful archive verification permits cleanup of its working files, leaving the ZIP, signed plan and status. Workspace collectors share the process/event loop.

Snapshot sejarah semasa dan kemas kini langsung boleh bertindih. Kedua-duanya adalah pemerhatian berasingan, dilabel mengikut sumber; duplikat tidak digabungkan secara senyap. Tiada inferens daripada ID yang hilang, teks yang dipadam tetapi dicipta, penyenaraian paksa ahli, atau penyertaan automatik dalam kumpulan dilaksanakan.

Untuk penjelasan yang ditujukan kepada pengendali, lihat [bagaimana pengumpulan berfungsi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/) dan [format akaun serta sesi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/).

Konfigurasi rangkaian disimpan dalam peti keselamatan yang disulitkan. Menggunakan laluan akan menutup klien lama dan membatalkan log masuk yang belum selesai; sambungan kemudian menggunakan laluan tersebut tanpa sebarang ralat balik langsung. Pemasangan kunci luaran baharu menghasilkan kunci Fernet setiap ruang kerja dengan HKDF-SHA256 daripada fail kunci induk dan garam rawak yang disimpan. Ini melindungi rahsia secara berasingan daripada direktori data, bukan kandungan jurnal/media dalam teks biasa.

Kemasukan demo tempatan menggunakan keupayaan proses yang dijana secara berasingan, dan tidak pernah menggunakan token panel yang dikonfigurasikan. Penerbitan dan penerimaan memerlukan mod demo secara eksplisit, root sintetik tanpa ruang kerja tambahan atau sesi yang dibenarkan, rakan sebantal/Host loopback, tiada penanda aras penghalaan proksi, dan tiada permintaan pelayar rentas asal. API langsung mengekalkan pengesahan pembawa dan menolak perubahan pengumpulan dalam mod demo.
