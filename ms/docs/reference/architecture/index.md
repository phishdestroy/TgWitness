# Arkitektur

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/architecture/

Komponen pengumpul, panel, jurnal, pekerja dan saksi, dan bagaimana data bergerak di antara mereka.

Satu proses Python menjadi hos panel FastAPI dan sebarang bilangan ruang kerja terasing, setiap satu dengan klien akaun pengguna Telethon. SQLite menyimpan jurnal peristiwa berasingan yang hanya menambah dan tetapan operasi yang boleh diubah. Sebuah peti besi yang disulitkan menyimpan kelayakan API, StringSession, dan kunci penandatanganan. Bahagian hadapan adalah HTML/CSS/JavaScript biasa yang dibundel: tiada pembinaan Node, CDN, atau muat turun bahagian hadapan semasa runtime diperlukan.

| Modul | Tanggungjawab |
| --- | --- |
| collector.py | Autorisasi, pemilihan dialog, kemas kini, tangkapan skrin, barisan media, pemantauan sambungan |
| interactions.py / telegram_client.py | Tindakan panel yang jelas, resit yang disahkan, ID permintaan berterusan dan dasar percubaan semula callback/sertai tempatan tugas |
| message_content.py | Perbandingan mesej yang dapat diperhatikan, mengecualikan metadata capaian penghantaran |
| workers.py | Tunggu pekerja fail eksport sebelum pembersihan pembatalan |
| store.py | Transaksi WAL, rantaian peristiwa teratur, penapis pertanyaan, tetapan operasi |
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

Autorisasi API adalah token pembawa. Operasi log masuk disusun secara bersiri dan terhad mengikut masa. Pemunggahan akaun menggunakan had khusus 12 MiB untuk badan yang disulitkan dan had 8 MiB untuk fail yang terdekod; permintaan API biasa mengekalkan had 16 KiB. Penukaran dijalankan dalam benang pekerja (worker thread), menyimpan muat naik dalam memori, dan memulangkan input yang dinormalisasi kepada pelayar yang disahkan. Log masuk QR mempunyai calon bagi setiap ruang kerja, pengecam jangka pendek, tugas penanti, dan pembatalan eksplisit. Hanya kebenaran yang diterima akan menjadi klien aktif. Telegram FloodWait dikembalikan dengan nilai Retry-After; kelayakan dan mesej ralat RPC mentah tidak didedahkan dalam ralat API. Eksport dijalankan di luar gelung peristiwa asenkron dan disusun mengikut ruang kerja. Ia menyalurkan snapshot bacaan yang stabil, dan boleh wujud bersama dengan penulisan WAL yang berterusan. Pengumpul ruang kerja berkongsi gelung proses/peristiwa.

Snapshot sejarah semasa dan kemas kini langsung boleh bertindih. Kedua-duanya adalah pemerhatian berasingan, dilabel mengikut sumber; duplikat tidak digabungkan secara senyap. Tiada inferens daripada ID yang hilang, teks yang dipadam tetapi dicipta, penyenaraian paksa ahli, atau penyertaan automatik dalam kumpulan dilaksanakan.

Untuk penjelasan yang ditujukan kepada pengendali, lihat [bagaimana pengumpulan berfungsi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/) dan [format akaun serta sesi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/).

Konfigurasi rangkaian disimpan dalam peti keselamatan yang disulitkan. Menggunakan laluan akan menutup klien lama dan membatalkan log masuk yang belum selesai; sambungan kemudian menggunakan laluan tersebut tanpa sebarang ralat balik langsung. Pemasangan kunci luaran baharu menghasilkan kunci Fernet setiap ruang kerja dengan HKDF-SHA256 daripada fail kunci induk dan garam rawak yang disimpan. Ini melindungi rahsia secara berasingan daripada direktori data, bukan kandungan jurnal/media dalam teks biasa.

Kemasukan demo tempatan menggunakan keupayaan proses yang dijana secara berasingan, dan tidak pernah menggunakan token panel yang dikonfigurasikan. Penerbitan dan penerimaan memerlukan mod demo secara eksplisit, root sintetik tanpa ruang kerja tambahan atau sesi yang dibenarkan, rakan sebantal/Host loopback, tiada penanda aras penghalaan proksi, dan tiada permintaan pelayar rentas asal. API langsung mengekalkan pengesahan pembawa dan menolak perubahan pengumpulan dalam mod demo.
