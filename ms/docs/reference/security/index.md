# Keselamatan dan pengendalian data

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/

Model ancaman, model capaian, rahsia semasa rehat, pendedahan rangkaian, import sesi dan cara melaporkan kerentanan.

TgWitness dijalankan pada komputer atau pelayan anda sendiri. Sambungan akaun, penyelenggaraan senarai proksi awam dan perkhidmatan luaran pilihan mempunyai dasar penjejakan yang jelas. Pemberitahuan, cap masa, salinan luar tapak dan saksi dikonfigurasikan secara berasingan. Halaman ini menyenaraikan apa yang dilindungi, bagaimana, dan apa yang diserahkan kepada pengendali.

| Kawasan | Ringkasnya |
| --- | --- |
| Akses | Kunci pentadbir serta akses terhad ke akaun/perbualan, tujuh kebenaran dan sesi yang boleh ditarik balik; localhost secara lalai |
| Rahsia yang disimpan | Sesi, pasangan API, kunci penandatanganan dan tetapan proksi disulitkan dengan Fernet |
| Mesej dan media | Disimpan tanpa penyulitan: gunakan penyulitan cakera dan kebenaran yang ketat |
| Integriti | Rantaian hash SHA-256 dan tandatangan Ed25519 pada setiap rekod |
| Tidak dilindungi | Pentadbir mesin, token panel bocor, kelengkapan tangkapan |

Untuk laporan kerentanan, lihat [dasar keselamatan](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Model akses

Token panel utama memberikan kawalan penuh. Orang lain boleh menerima [akses terhad](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/) mereka sendiri: ruang kerja dan sembang terpilih, kebenaran, tamat tempoh, sekatan IP, had log masuk dan sesi yang boleh ditarik balik. Akses terhad sembang tidak dapat menjalankan operasi seluruh ruang kerja walaupun kebenaran mereka telah dicentang. Ruang kerja berkongsi satu proses dan tidak mengasingkan data daripada pentadbir hos.

Panel mendengar pada localhost secara lalai. Log masuk pelayar menukar token akses untuk kelayakan sesi; pelayar menghantarnya sebagai token pembawa. Ia disimpan dalam sessionStorage dan bukannya kuki pengesahan. Kunci/keluar log membersihkan sesi pelayar. Menutup pelayar atau menamatkan sesi tidak menghentikan pengumpulan.

Token yang dikeluarkan dan kelayakan sesi disimpan sebagai hash dalam peti besi yang disulitkan. Pencabutan menamatkan sesi yang berkaitan; perubahan kebenaran menjejaskan permintaan seterusnya. Fail yang dimuat turun tidak dapat ditarik balik. Pentadbir juga boleh mengehadkan sesi pelayar mereka sendiri, tetapi skrip yang menggunakan token panel utama secara langsung mengekalkan akses penuh dan memintas had sesi pelayar tersebut.

Pengesahan gagal dihadkan kadar mengikut alamat klien. Sekatan IP menggunakan alamat yang dilihat oleh aplikasi; semak tingkah laku proksi songsang sebelum bergantung padanya. Kredensial Witness kekal berasingan sebagai kredensial titik pemeriksaan/kesihatan baca sahaja.

### Akses demo

`/api/demo-access` adalah bootstrap yang sengaja tidak diautentikasi untuk demo sintetik yang dimulakan secara eksplisit dan terasing. Ia mengeluarkan keupayaan tempoh-proses yang berasingan, tidak pernah token panel sebenar atau penimpaan TGWITNESS_TOKEN. Penerbitan dan penggunaan memerlukan rakan sebaya loopback dan Host, tiada pengepala yang diteruskan, dan tiada permintaan rentas asal. Ruang kerja tambahan atau sesi yang dibenarkan menyahaktifkan laluan ini. Ruang kerja langsung tidak pernah mengeluarkan keupayaan ini. Demo ini tidak boleh menghubungkan akaun atau menukar tetapan pengumpulan.

## Kandungan panel dan eksport

Panel ini tidak menggunakan fon luaran, analitik, sumber CDN, atau media jauh yang disemat. Teks yang diperoleh daripada Telegram disisipkan sebagai teks, bukan HTML. Lampiran yang dimuat turun dihidangkan sebagai lampiran binari. Eksport JSONL mengekalkan rentetan asal; HTML melarikan mereka; sel CSV yang boleh menjadi formula diberi awalan tanda petik.

Eksport mengecualikan rahsia pengesahan dan penandatanganan, tetapi sengaja mengandungi metadata sumber yang dikumpul, pengecam, dan mungkin kandungan peribadi atau sensitif. Hash akses Telegram dan rujukan fail boleh muncul dalam metadata sumber mentah.

## Rahsia yang disimpan

Kredensial API Telegram, StringSession, dan kunci peribadi Ed25519 disulit menggunakan Fernet. Secara lalai, kuncinya disimpan dalam direktori data terlindung yang sama. Ini mengurangkan pendedahan teks biasa secara tidak sengaja; ia bukan perlindungan terhadap penyerang yang boleh membaca keseluruhan direktori. Kandungan mesej dan media **tidak disulitkan** oleh TgWitness. Gunakan penyulitan cakera dan kebenaran OS yang terhad. Fail kunci peribadi Unix dicipta dengan mod 0600; direktori data yang baru dibuat menggunakan mod 0700. Kebenaran direktori sedia ada tidak diubah. Windows mewarisi ACL direktori: hadkan ia kepada akaun perkhidmatan dan pentadbir yang dibenarkan.

### Kunci induk luaran

Untuk direktori data baru, TGWITNESS_VAULT_KEY_FILE boleh membekalkan kunci induk rawak luaran. HKDF-SHA256 dan garam rawak berasingan menghasilkan kunci Fernet yang berbeza untuk setiap ruang kerja. vault.external.json mesti disimpan untuk pemulihan. Kunci induk yang hilang atau salah akan menyebabkan kegagalan tertutup. Peti simpanan tempatan sedia ada tidak dipindahkan secara senyap. Proses yang sedang berjalan boleh mengakses kunci; ini bukan pengasingan HSM. Panel melaporkan mod yang dipilih dan menyatakan dengan jelas bahawa storan mesej/media tidak disulitkan oleh aplikasi. Lihat [sambungan, proksi dan perlindungan data](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) untuk model ancaman penuh.

## Proksi dan laluan rangkaian

Konfigurasi proksi disulitkan dalam peti besi. Kata laluan dan rahsia MTProxy tidak dikembalikan oleh API atau ditulis ke dalam rekod bukti. Setiap ruang kerja memilih laluan Telegram dan [mod IP](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes) masing-masing.

Mod Sembunyikan IP menolak fallback Telegram langsung dan memerlukan proksi untuk permintaan HTTP luaran. Mod fallback yang dipilih secara eksplisit membenarkan akses Telegram langsung selepas kelewatannya; mod terowong/VPN membenarkan laluan langsung. Memilih mod terowong tidak memasang atau mengesahkan VPN. Tetapan ini tidak mengawal semua trafik mesin, pelayar, pengurus pakej atau penyelesaian DNS hos proksi tempatan.

MTProxy hanya membawa trafik Telegram. Permintaan luaran boleh menggunakan proksi SOCKS5/HTTP berasingan, laluan SOCKS5/HTTP ruang kerja, atau laluan terus yang dibenarkan; ia juga boleh dilumpuhkan. Saksi bebas mempunyai tetapan pengangkutan tersendiri. Pengesahan CONNECT SOCKS5/HTTP biasa tidak disulitkan oleh protokol proksi tersebut itu sendiri. Rahsia MTProxy TLS palsu masih tidak disokong.

## Log masuk dan import sesi

Fail .tgwitness-session yang diubah suai mengandungi rahsia kebenaran teks biasa sehingga dimuat dan disimpan dalam peti besi. CLI luar talian menerima skema Telethon yang telah disemak. Panel import juga menerima Pyrogram SQLite, TData ZIP akaun tunggal moden, dan input JSON yang didokumenkan. Ia disahkan, terhad kepada empat fail / 8 MiB, dan memproses muat naik dalam memori tanpa mengekstrak arkib atau menyimpan fail asal. Butiran pengesahan yang telah dinormalisasi hanya dikembalikan kepada pelayar yang disahkan yang membuat permintaan; ia disimpan dalam peti besi yang disulitkan selepas pengesahan Telegram berjaya. Lindungi fail asal dan fail yang telah ditukar, dan elakkan klien serentak menyalin kebenaran.

Pemprosesan TData mengesahkan checksum kontena, has rat pengekodan semula tempatan, dan panjang struktur. Kod laluan tempatan Desktop yang dibekalkan digunakan secara sementara dan tidak disimpan. Penganalisis terhad ini tidak menyatakan bahawa setiap versi Desktop adalah serasi. Imej QR dijana secara tempatan, mengandungi token log masuk Telegram yang singkat tempohnya, dan tidak pernah dihantar ke perkhidmatan paparan luaran. Kunci, pertukaran ruang kerja, log masuk baru, dan perubahan laluan membatalkan percubaan QR yang tertangguh. Memuat semula/menutup tab mungkin menyebabkan percubaan masih tertangguh sehingga tamat tempoh. Log masuk QR yang berjaya masih menguatkuasakan pengikatan akaun. Badan API biasa kekal terhad kepada 16 KiB; laluan import yang disahkan menerima sehingga 12 MiB JSON yang disulit, dengan menguatkuasakan had fail terdekod yang lebih kecil secara berasingan.

Kod log masuk dan kata laluan pengesahan dua langkah Telegram tidak disimpan. Status nombor telefon/kod-hash disimpan dalam memori semasa kebenaran. Sesi Telegram memberikan akses akaun; jangan sekali-kali memuat naik direktori data, sesi, token, kunci peti, atau kunci tandatangan peribadi ke GitHub.

## Logs dan penghantaran

Tindak balas pengesahan API lalai diganti supaya ia tidak memantulkan nilai kelayakan. Log akses aplikasi dilumpuhkan. Jangan tetapkan proksi terbalik untuk melogkan tajuk Autentikasi atau badan permintaan. HTTP membawa token dan rahsia log masuk dalam teks biasa: gunakan HTTPS atau terowong SSH setiap kali meninggalkan localhost.

## Had integriti

Rantaian hash, pencetus pangkalan data, dan tandatangan mengesan pengubahsuaian tertentu; ia tidak menghalang pentadbir tempatan daripada menulis semula dan menandatangani semula jurnal. Simpan titik pemeriksaan bertandatangan dan cap jari kunci awam pada sistem berasingan. Mod bukti dan salinan luar tapak (kedua-duanya dimatikan secara lalai) menghantar hash titik pemeriksaan kepada perkhidmatan cop masa dan salinan yang disulitkan ke storan serasi S3; lihat [format bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/). Log ketelusan, penandatanganan disokong HSM dan pensijilan rantaian pemilikan formal tidak dilaksanakan.

## Jika anda mengesyaki terdapat masalah

Pelihara direktori data asal dan gunakan salinan berasingan untuk analisis. Jangan sertakan data Telegram peribadi atau maklumat log masuk dalam isu awam. Tiada pensijilan keselamatan bebas dituntut.
