# Telegram · Keselamatan dan pengendalian data

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/

Model ancaman, model capaian, rahsia semasa rehat, pendedahan rangkaian, import sesi dan cara melaporkan kerentanan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Penyebaran dan pemulihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/)

![Penyebaran & pemulihan](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Halaman ini menerangkan akses, penyimpanan dan perlindungan rangkaian dalam ruang kerja tempatan atau pelayan. Untuk pengumpulan pada pelari GitHub atau dalam VM sulit Intel TDX, lihat [mod pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope), yang menambah semakan persekitaran pengumpulan. Sambungan akaun, pemberitahuan, cap masa, salinan luar tapak dan saksi mempunyai tetapan penghalaan mereka sendiri.

| Kawasan | Ringkasnya |
| --- | --- |
| Akses | Kunci pentadbir serta akses terhad ke akaun/perbualan, tujuh kebenaran dan sesi yang boleh ditarik balik; localhost secara lalai |
| Rahsia yang disimpan | Sesi, pasangan API, kunci penandatanganan dan tetapan proksi disulitkan dengan Fernet |
| Mesej dan media | Disimpan tanpa penyulitan: gunakan penyulitan cakera dan kebenaran yang ketat |
| Integriti | Rantaian hash SHA-256 dan tandatangan Ed25519 pada setiap rekod |
| Batas kepercayaan tempatan | Pentadbir hos mengawal ruang kerja dan kunci tandatanganannya; titik pemeriksaan bebas mengekalkan sempadan jurnal terdahulu |

Untuk laporan kerentanan, lihat [dasar keselamatan](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

**Pada halaman ini**

- [Model capaian](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#access-model)
- [Kandungan panel dan eksport](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#panel-content-and-exports)
- [Rahsia yang disimpan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#secrets-at-rest)
- [Proksi dan laluan rangkaian](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#proxies-and-network-routes)
- [Log masuk dan import sesi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#sign-in-and-session-imports)
- [Logs dan penghantaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#logs-and-transport)
- [Had integriti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#integrity-limits)
- [Jika anda mengesyaki terdapat masalah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#if-you-suspect-a-problem)

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

Kredensial API Telegram, kunci sesi dan kunci penandatanganan disulitkan dengan Fernet. Untuk mesej dan media tempatan, penyulitan disediakan oleh cakera atau volum hos; ruang kerja menyimpan fail biasa. Eksport boleh menggunakan ZIP AES-256 yang dilindungi kata laluan, dan salinan luar tapak menggunakan AES-256-GCM.

Kunci peti keselamatan secara lalai disimpan di direktori data terlindung. Gunakan fail kunci induk luaran di bawah untuk menyimpannya secara berasingan. Pada Unix, fail kunci peribadi baharu menggunakan mod 0600 dan direktori data baharu menggunakan 0700; pada Windows, tetapkan ACL direktori untuk akaun perkhidmatan dan pentadbir yang dibenarkan. Kebenaran direktori sedia ada dikekalkan.

### Kunci induk luaran

Untuk direktori data baharu, TGWITNESS_VAULT_KEY_FILE boleh membekalkan kunci induk rawak luaran. HKDF-SHA256 dan garam rawak berasingan menghasilkan kunci Fernet yang berbeza untuk setiap ruang kerja. vault.external.json mesti disimpan untuk pemulihan. Kunci induk yang hilang atau salah akan menyebabkan kegagalan dalam mod tertutup. Vault tempatan sedia ada tidak dipindahkan secara senyap. Panel memaparkan mod penyimpanan kunci yang dipilih. Penyulitan cakera melindungi fail mesej dan media tempatan dalam kedua-dua mod; lihat [sambungan dan perlindungan data](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) untuk butiran tetapan.

## Proksi dan laluan rangkaian

Konfigurasi proksi disulitkan dalam peti besi. Kata laluan dan rahsia MTProxy tidak dikembalikan oleh API atau ditulis ke dalam rekod bukti. Setiap ruang kerja memilih laluan Telegram dan [mod IP](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes) masing-masing.

**Sembunyikan alamat** menolak fallback Telegram langsung dan memerlukan proksi untuk permintaan HTTP luaran. Mod fallback yang dipilih secara eksplisit membenarkan akses Telegram langsung selepas kelewatannya; mod terowong/VPN membenarkan laluan langsung. Memilih mod terowong tidak memasang atau mengesahkan VPN. Tetapan ini tidak mengawal semua trafik mesin, pelayar, pengurus pakej atau penyelesaian DNS hos proksi tempatan.

MTProxy hanya membawa trafik Telegram. Permintaan luaran boleh menggunakan proksi SOCKS5/HTTP berasingan, laluan SOCKS5/HTTP ruang kerja, atau laluan terus yang dibenarkan; ia juga boleh dilumpuhkan. Saksi bebas mempunyai tetapan pengangkutan tersendiri. Pengesahan CONNECT SOCKS5/HTTP biasa tidak disulitkan oleh protokol proksi tersebut itu sendiri. Rahsia MTProxy TLS palsu masih tidak disokong.

## Log masuk dan import sesi

Fail .tgwitness-session yang diubah suai mengandungi rahsia kebenaran teks biasa sehingga dimuat dan disimpan dalam peti besi. CLI luar talian menerima skema Telethon yang telah disemak. Panel import juga menerima Pyrogram SQLite, TData ZIP akaun tunggal moden, dan input JSON yang didokumenkan. Ia disahkan, terhad kepada empat fail / 8 MiB, dan memproses muat naik dalam memori tanpa mengekstrak arkib atau menyimpan fail asal. Butiran pengesahan yang telah dinormalisasi hanya dikembalikan kepada pelayar yang disahkan yang membuat permintaan; ia disimpan dalam peti besi yang disulitkan selepas pengesahan Telegram berjaya. Lindungi fail asal dan fail yang telah ditukar, dan elakkan klien serentak menyalin kebenaran.

Pemprosesan TData mengesahkan checksum kontena, has rat pengekodan semula tempatan, dan panjang struktur. Kod laluan tempatan Desktop yang dibekalkan digunakan secara sementara dan tidak disimpan. Penganalisis terhad ini tidak menyatakan bahawa setiap versi Desktop adalah serasi. Imej QR dijana secara tempatan, mengandungi token log masuk Telegram yang singkat tempohnya, dan tidak pernah dihantar ke perkhidmatan paparan luaran. Kunci, pertukaran ruang kerja, log masuk baru, dan perubahan laluan membatalkan percubaan QR yang tertangguh. Memuat semula/menutup tab mungkin menyebabkan percubaan masih tertangguh sehingga tamat tempoh. Log masuk QR yang berjaya masih menguatkuasakan pengikatan akaun. Badan API biasa kekal terhad kepada 16 KiB; laluan import yang disahkan menerima sehingga 12 MiB JSON yang disulit, dengan menguatkuasakan had fail terdekod yang lebih kecil secara berasingan.

Kod log masuk dan kata laluan pengesahan dua langkah Telegram tidak disimpan. Status nombor telefon/kod-hash disimpan dalam memori semasa kebenaran. Sesi Telegram memberikan akses akaun; jangan sekali-kali memuat naik direktori data, sesi, token, kunci peti, atau kunci tandatangan peribadi ke GitHub.

## Logs dan penghantaran

Tindak balas pengesahan API lalai diganti supaya ia tidak memantulkan nilai kelayakan. Log akses aplikasi dilumpuhkan. Jangan tetapkan proksi terbalik untuk melogkan tajuk Autentikasi atau badan permintaan. HTTP membawa token dan rahsia log masuk dalam teks biasa: gunakan HTTPS atau terowong SSH setiap kali meninggalkan localhost.

## Had integriti

Semakan pengesahan tempatan memeriksa rekod tandatangan, rantaian hash, lampiran dan manifes eksport. Pentadbir memegang kunci penandatanganan tempatan dan boleh mencipta jurnal bertandatangan lain; titik pemeriksaan yang disimpan secara bebas mengesan penggantian awalan yang dilindunginya. Simpan cap jari kunci dan titik pemeriksaan bersama penerima atau saksi bebas.

Untuk pengesahan koleksi secara bebas, pilih [tangkapan GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) atau [penyebaran Intel TDX](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Pemverifikasinya memeriksa asal usul aliran kerja atau ukuran perkakasan selain integriti arkib. Cap masa pilihan dan salinan luar tapak yang disulitkan menyediakan titik rujukan masa dan salinan yang boleh dipulihkan; [format bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) menerangkan pemeriksaan untuk setiap mod.

## Jika anda mengesyaki terdapat masalah

Pelihara direktori data asal dan gunakan salinan berasingan untuk analisis. Laporkan versi terjejas, operasi dan langkah yang boleh diulang melalui [dasar keselamatan](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), sambil mengekalkan data akaun dan maklumat log masuk secara peribadi.
