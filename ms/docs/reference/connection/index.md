# Sambungan, proksi dan perlindungan data

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/

Pengesahan, kolam proksi automatik, mod IP, dasar sandaran, permintaan luaran dan penyimpanan rahsia.

Dokumen ini menerangkan tingkah laku TgWitness 0.7.1 dan hadnya. Pengesahan, akses sumber, sambungan rangkaian dan kelengkapan tangkapan adalah keadaan yang berasingan. Untuk langkah log masuk, format fail, dan akaun berbilang, mulakan dengan [akaun dan format sesi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/). Untuk dasar peristiwa dan tingkah laku permulaan semula, lihat [bagaimana pengumpulan berfungsi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/).

## Kaedah pengesahan

**ID API dan hash API mengenal pasti aplikasi; ia tidak menggantikan log masuk akaun.** Ia adalah pilihan dalam TgWitness. Keutamaan: sepasang yang dimasukkan dalam borang, kemudian satu daripada JSON akaun yang diimport, kemudian sepasang yang disimpan dalam ruang kerja, kemudian kolam terbina dalam sebanyak 50 pasangan Telegram Desktop (2040) dihantar dengan keterangan klien Telegram Desktop yang sepadan. Pasangan anda sendiri daripada Alat Pembangunan API di [my.telegram.org](https://my.telegram.org) boleh digunakan dengan semua akaun anda; setiap akaun masih mempunyai kebenaran tersendiri.

| Kaedah | Keperluan | TgWitness sokongan |
| --- | --- | --- |
| Telefon, kod, 2FA pilihan | Akses akaun; pasangan API pilihan | Log masuk panel |
| Kunci Auth HEX + ID DC | Kunci penuh 512-karakter dan DC 1–5 | Tab **Kunci Auth** Langsung; ID Pengguna pilihan disemak sebelum kebenaran disimpan |
| Telethon StringSession | Rentetan sesi yang sah | Log masuk panel |
| Telethon SQLite `.session` | Salinan tertutup dan konsisten | Import panel langsung skema 7/8; CLI luar talian pilihan |
| Pyrogram SQLite `.session` | Sesi pengguna pengeluaran ditutup | Import panel langsung skema 2/3 |
| Telegram Desktop TData ZIP | Satu akaun moden; kod laluan tempatan jika dilindungi | Penukaran dalam memori dengan pemeriksaan checksum/penyahsulit |
| JSON Akaun | Medan API/sesi/kunci yang disokong | Metadata sahaja mengisi kelayakan API; log masuk sesi/kunci atau telefon/QR masih diperlukan |
| Log masuk QR | Pengesahan daripada aplikasi Telegram yang dibenarkan | Penghasilan QR tempatan, tamat tempoh/cubaan semula, 2FA pilihan |
| TDLib / Pyrogram StringSession | Format khusus perpustakaan lain | Tidak disokong |
| Token bot | Sebuah bot dengan model akses/kemas kini tersendiri | Tidak digunakan oleh pengumpul ini |

Telegram memilih penghantaran kod; SMS tidak dijamin. Hah API tidak dapat membaiki sesi yang ditarik balik atau menggantikan kata laluan 2FA yang terlupa. TgWitness tidak menyimpan kod log masuk atau kata laluan 2FA Telegram ke cakera.

Untuk sumber peribadi, akaun mesti sudah mempunyai akses. Nama pengguna kumpulan tidak diperlukan. Import proksi atau sesi tidak memberikan hak keahlian atau pentadbir. Keahlian semasa tidak menjamin akses kepada sejarah sebelum menyertai.

## Import fail sesi Telethon

Telethon SQLite, Pyrogram SQLite, dan TData Telegram Desktop menggunakan format yang berbeza. Panel mengesan dan menukar struktur yang disokong; menamakan semula fail bukanlah penukaran. Pilih satu sesi dan JSON pengiringnya di bawah **Fail**, kemudian tekan **Sambungkan akaun**. Sehingga empat fail yang sepadan dan jumlah 8 MiB diterima. Lihat [had format](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/) untuk butiran TData/JSON. Tiada pemulihan kod laluan. Log masuk Telefon/2FA atau QR mewujudkan kebenaran berasingan.

Laluan baris perintah pilihan hanya untuk Telethon kekal tersedia:

1. Hentikan klien yang menggunakan sesi asal dan buat salinan yang konsisten. Konverter menolak fail dengan WAL/jurnal yang belum selesai. Tutup klien asal dengan betul dan bukannya memadam fail tersebut untuk memintas pemeriksaan.
2. Dari persekitaran TgWitness, jalankan:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. Di bawah **Tambah akaun → Fail**, muat naik hasil atau tampal rentetannya, dan teruskan.
2. Semak ID akaun numerik yang dipaparkan, pilih sumber dan mulakan pemerhatian.

Pengubah membuka SQLite hanya-baca, tidak melakukan peningkatan skema atau permintaan rangkaian, dan tidak mencetak sesi. Ia memeriksa versi skema, jenis jadual, satu baris sesi, IP/port/DC dan panjang kunci. Input CLI terhad kepada 64 MiB; teks StringSession terhad kepada 4 KiB. Panel penukaran memuat naik fail ke pelayan TgWitness yang disahkan, memprosesnya dalam memori, dan memulangkan kelayakan yang dinormalisasi ke pelayar tersebut tanpa menyimpan fail asal yang dimuat naik. Gunakan HTTPS untuk pelayan jauh.

**Fail yang ditukar adalah rahsia akses akaun yang tidak disulitkan.** Simpannya dalam simpanan terlindung dan jangan sekali-kali komit atau hantar ke perkhidmatan penukaran pihak ketiga. TgWitness menyimpan sesi yang dibenarkan dalam peti besi yang disulitkannya. Menyalin sesi tidak mencipta kebenaran berasingan: jangan jalankan klien serentak dengan kunci kebenaran klon dan menganggap penghantaran kemas kini secara berasingan.

Pemindahan penukaran memindahkan kebenaran, bukan mesej asal, cache entiti atau penuding kemas kini tahan lama. Ia tidak membaiki pemulihan kemas kini merentasi permulaan semula proses.

## MTProto, Telethon dan proksi

MTProto ialah protokol Telegram. Telethon ialah pustaka klien Python yang digunakan oleh TgWitness. MTProxy ialah proksi pengangkutan Telegram; SOCKS5 dan HTTP CONNECT menyediakan terowong umum. Tiada satu pun menggantikan pengesahan akaun.

Simpan laluan untuk setiap ruang kerja di **Akaun → Tetapan → Tetapan sambungan → Ubah laluan sambungan** sebelum log masuk. Ruang kerja baru secara lalai menggunakan **Automatic MTProxy · senarai awam** dengan kelakuan Sembunyikan IP. Ruang kerja sedia ada yang secara eksplisit menggunakan Direct mengekalkan mod yang membenarkannya.

## Mod IP

Rute memilih sambungan. Mod IP menentukan bila alamat pelayan mungkin terdedah. Kawalan ini tidak memasang VPN atau mengalihkan semua trafik mesin.

| Mod | Telegram | Permintaan luaran |
| --- | --- | --- |
| Sembunyikan IP (`hide`) | Gunakan proksi; tunggu jika tiada yang berfungsi. Tiada pelan sandaran langsung. | Perlukan SOCKS5/HTTP; menolak permintaan tanpa proksi yang sesuai. |
| Benarkan sandaran (`fallback`) | MTProxy automatik mungkin menggunakan Direct selepas kelewatan yang ditetapkan, kemudian kembali ke proksi yang berfungsi. | Utamakan proksi luaran yang dikonfigurasikan atau laluan SOCKS5/HTTP akaun; jika tidak, Direct dibenarkan. |
| Terowong / VPN (`tunnel`) | Laluan terus dan pelan B imbangan automatik segera dibenarkan. | Direct dibenarkan apabila tiada proksi yang sesuai dikonfigurasikan. |

Mod terowong/VPN menganggap anda mengurus rangkaian tersebut secara berasingan. Tanpa terowong yang berfungsi, destinasi boleh melihat alamat pelayan itu sendiri. Pilih mod mengikut rangkaian sebenar anda, bukan nama pilihan.

### Pilih laluan

| Rute | Tetapan | Batas |
| --- | --- | --- |
| MTProxy automatik | Senarai terbina dalam atau katalog pengendali | Menjaga laluan Telegram yang berfungsi; sandaran langsung bergantung pada mod IP |
| Langsung | Mod Terowong/VPN | Telethon menggunakan laluan rangkaian hos |
| SOCKS5 | Host, port, nama pengguna/kata laluan pilihan | python-socks, DNS destinasi jauh diaktifkan |
| HTTP CONNECT | Host, port, nama pengguna/kata laluan pilihan | HTTP CONNECT biasa; TLS ke proksi itu sendiri tidak dilaksanakan |
| MTProxy | Host, port, rahsia | Pengangkutan Telethon Eksperimental; 32 digit heksadesimal atau `dd` + 32 digit heksadesimal |

Rahsia Fake TLS `ee` ditolak. Normalisasi Telethon 1.45 boleh menyingkirkan awalan dan domain, tetapi ia tidak melaksanakan Fake TLS. Tampal `tg://proxy?server=…&port=…&secret=…` atau `https://t.me/proxy?server=…&port=…&secret=…` dan pilih **Isi medan daripada pautan**. Ini mengesahkan dan mengisi medan tanpa menyambung atau menyimpan; semak dan simpan laluan secara berasingan. Medan manual kekal tersedia. Lihat [pautan proksi Telegram](https://core.telegram.org/api/links#proxy-links).

### Proksi awam yang disediakan oleh pemasangan anda

Senarai terbina dalam menggabungkan empat sumber: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) dan [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Snapshot yang disertakan mengandungi fakta hujung, atribusi sumber dan tarikh muat turun. Penyenaraian penyedia bukan bukti bahawa proksi berfungsi atau menyampaikan setiap kemas kini Telegram.

**Semakan MTProxy automatik** memeriksa kebolehhubungan penghantaran Telegram, mengekalkan proksi yang berfungsi dan beralih ke proksi lain apabila ia gagal. Ruang kerja memilih proksi berbeza apabila terdapat cukup entri berfungsi; alamat keluar unik tidak dijamin. Proksi yang gagal berehat sebelum cubaan lain. Jika tiada yang berfungsi, mod IP menentukan sama ada pengumpulan perlu menunggu atau boleh menggunakan sambungan terus. Menukar proksi tidak menukar akaun atau memadam jurnalnya. Pilihan dan perubahan laluan direkodkan dalam jurnal yang disahkan.

Semasa laluan automatik diaktifkan, senarai dikemas kini setiap jam dan pemeriksaan pengangkutan dijalankan setiap sepuluh minit secara lalai. Jeda ini boleh diubah suai. **Mengemas kini senarai awam** memerlukan penyegaran; melihat senarai sahaja tidak mengubah laluan manual yang disimpan.

Setiap respons suapan dihadkan kepada 1 MiB dengan had masa permintaan lapan saat dan tarikh akhir muat turun keseluruhan 20 saat; penalaan semula ditolak. Sehingga 64 entri serasi bagi setiap sumber disimpan dan diasingkan. Pemarser menerima rahsia heksadesimal dan base64url yang disokong serta suapan JSON. `ee` TLS palsu, pautan tidak sah, literal IP peribadi/tertahan dan nama hos tempatan diabaikan. Nama hos diselesaikan dan diperiksa sebelum digunakan, dan IP yang dipilih dikunci untuk sambungan tersebut. Pengambilan semula automatik menyelesaikan nama hos sekali lagi; terapkan semula kemasukan manual untuk menyelesaikannya sekali lagi.

Tindak balas suapan yang gagal, kosong atau tidak serasi mengekalkan tangkapan sumber sebelumnya. Kemas kini bersifat atom, disusun secara bersiri dan terhad kepada satu percubaan setiap minit bagi setiap ruang kerja. Siasatan penghantaran yang berjaya mewujudkan sambungan, bukananonimiti atau kelengkapan tangkapan.

**Lalu lintas Telegram dan permintaan HTTPS menggunakan laluan yang berbeza.** Muat turun senarai menggunakan sambungan HTTPS berasingan dan laluan permintaan luaran yang disediakan. `TGWITNESS_PROXY_FEED_PROXY` secara eksplisit menimpa laluan itu dengan proksi HTTP/SOCKS5; kedua-dua varian Compose pengumpul meneruskannya. Kolam latar belakang mengikuti ruang kerja utama. Tiada sesi Telegram, kelayakan API, token panel atau token bot dihantar kepada penyedia feed. Nama penyedia, tarikh snapshot dan laluan muat turun muncul di bawah Bahagian **'Where the list comes from**'.

MTProxy hanya membawa trafik Telegram. Operasi Workspace HTTP seperti cap masa, pemberitahuan, salinan luar tapak dan semakan sumber menggunakan proksi SOCKS5/HTTP berasingan apabila dikonfigurasikan, kemudian laluan SOCKS5/HTTP akaun. Tanpa salah satu daripadanya, Hide IP menolak permintaan; mod lain membenarkan Direct. Permintaan luaran boleh dilumpuhkan. Proksi muat turun suapan yang dikonfigurasikan secara eksplisit kekal sebagai keutamaan pengendali berasingan. Perkhidmatan saksi bebas mengekalkan laluan tersendiri.

****Parameter kolam automatik**** Di bawah **Parameter → MTProxy Automatik**, konfigurasi ambang kegagalan, masa rehat, putaran yang dirancang, perkongsian proksi dan kelewatan fallback yang dibenarkan. | Kawalan | Lalai | | --- | --- | | Putus sambungan sebelum penggantian | 3 dalam 10 minit | | Proksi yang dicuba bagi setiap percubaan sambungan | 3 | | Rehat pertama / maksimum selepas kegagalan | 10 minit / 6 jam | | Putaran yang dirancang | Dilumpuhkan; aktifkan semasa kegagalan | | Akaun setiap proksi | 0: utamakan kemasukan berasingan, kongsi apabila perlu. Tetapkan 1 untuk menunggu kemasukan eksklusif. | | Kelewatan sebelum fallback Langsung yang dibenarkan | 10 minit; Sembunyikan IP masih menolak Langsung | | Semakan semula suapan / pengesahan penghantaran | 60 / 10 minit; nilai ruang kerja utama terpakai pada kolam kongsi | Proksi yang berbeza tidak menjamin alamat keluar yang berbeza. Tetapan ini tidak membatalkan had Telegram atau membuktikan kerahsiaan.

Untuk menggantikan senarai awam dengan katalog pengendali anda sendiri, konfigurasi penggantian di bawah. Ia menyahaktifkan langganan luaran sepenuhnya, termasuk apabila tatasusunan `proxies`-nya kosong.

Salin [katalog kosong](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) ke `proxy-config/proxies.json` dan tambahkan titik akhir awam yang anda sediakan:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Nilai contoh mesti diganti. Sehingga 32 entri berbeza diterima. Penyenaraian terautentikasi memaparkan label/hos/port tanpa rahsia kongsi; memilih satu menyimpan kelayakannya ke dalam peti besi ruang kerja. Ketersediaannya masih belum diuji sehingga ujian pengangkutan eksplisit. Katalog yang tersusun salah membolehkan konfigurasi manual.

Pelancaran asli: tetapkan `TGWITNESS_PROXY_CATALOG` ke laluan JSON tempatan. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

Lapisan atas memasang `proxy-config` sebagai baca sahaja; fail mesti boleh dibaca oleh UID kontena 10001. Direktori itu dikecualikan daripada Git, konteks pembinaan Docker dan arkib sumber. Katalog ini mengkonfigurasi akaun pengumpul; [bot saksi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/) menggunakan laluan HTTP/SOCKS5 sendiri, bukan MTProxy.

Fallback langsung dikawal oleh mod IP di atas. Hentikan pemerhatian sebelum menukar laluan. Penyimpanan memutuskan sambungan klien lama dan membatalkan log masuk yang belum selesai; klien baru menggunakan laluan yang disimpan. Pengikatan jurnal/sesi akaun kekal. Tetapan menggantikan laluan sebelumnya: masukkan semula kelayakan proksi apabila menyuntingnya.

Kredensial disulitkan dalam `network.enc`. API tidak memulangkan nama pengguna, kata laluan atau rahsia. Rekod yang ditandatangani mengandungi jenis laluan dan sama ada kredensial wujud, tanpa memasukkan titik akhir dan rahsia. Pengendali boleh melihat titik akhir di panel. Medan rahsia dipadam selepas menyimpan, mengunci atau menukar ruang kerja.

**Uji sambungan Telegram**, juga tersedia sebelum log masuk, membuka dan menutup sambungan Telegram sementara tanpa kebenaran melalui laluan. Ia tidak menghubungi laman web semakan IP. Kejayaan mengesahkan sambungan pengangkutan, bukan akses kumpulan, penghantaran lengkap atauanonimiti.

Proksi terpakai pada sambungan klien Telegram, termasuk muat turun media DC Telegram. Pelayar, pip, SSH dan alat TSA yang dipanggil secara manual mempunyai laluan berasingan. Nama hos proksi boleh diselesaikan secara tempatan. `rdns` menjejaskan nama hos destinasi; Telegram sering menyediakan IP DC berangka.

SOCKS5 dan HTTP CONNECT biasa tidak menyulitkan kelayakan proksi atau terowong klien-ke-proksi itu sendiri. MTProto melindungi trafik Telegram secara berasingan. Gunakan saluran selamat yang sesuai ke proksi pada rangkaian yang tidak dipercayai. Kumpulan Peribadi adalah sembang awan; MTProto tidak mengubahnya menjadi Sembang Rahsia yang disulitkan hujung-ke-hujung.

## Sulitan dan tandatangan

| Lapisan | Dipelaksanaan | Tanggungjawab pengendali |
| --- | --- | --- |
| Lalu lintas Telegram | Telethon MTProto | Kepercayaan platform, laluan dan ketersediaan |
| Panel web | Token pemegang, lalai gelung balik, had permintaan | Tunel HTTPS atau SSH untuk capaian jauh |
| Rahsia | Fernet untuk kelayakan API, sesi, kelayakan proksi dan kunci peribadi penandatangan | Lindungi kunci penyahsulitan dan hos yang sedang berjalan |
| Kunci peti | Kunci tempatan, atau kunci induk luaran untuk pemasangan baharu | Pisahkan storan terlindung dan sandaran kunci |
| Mesej dan lampiran | Penyimpanan aplikasi teks biasa | Cakera/jumlah yang disulitkan |
| ZIP/JSONL/CSV/HTML | Semakan integriti, tiada penyulitan kandungan | Melindungi salinan dan pemindahan yang dieksport |
| Asal usul dan masa | Jurnal berasingan, resit proses, alat RFC 3161 | Kunci dipercayai, titik pemeriksaan bebas/TSA dan prosedur pemeliharaan |

**Perlindungan storan** dalam Akaun memaparkan keadaan ini. Token panel adalah rahsia capaian, bukan kata laluan penyulitan. Ia memberi akses pentadbir; [token yang dikeluarkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/) boleh dihadkan kepada akaun dan sembang. Ruang kerja berkongsi proses hos dan bukan penyewa terasing.

Demonstrasi sintetik yang dimulakan secara eksplisit dan terasing boleh dibuka secara automatik melalui sambungan loopback langsung. Ini menggunakan keupayaan jangka hayat proses yang berasingan; ia tidak mendedahkan token panel yang dikonfigurasikan mahupun memberi akses kepada ruang kerja sebenar. Permintaan jauh, melalui proksi atau merentas asal tidak dapat memperoleh/menggunakan keupayaan kemasukan automatik ini. Kemudahan ini tidak menghapuskan sempadan pengesahan untuk data akaun sebenar.

BitLocker, LUKS, FileVault atau volum yang disulitkan yang diuruskan boleh melindungi storan di bawah model ancaman masing-masing. Pentadbir mesin yang sedang berjalan dan tidak dikunci masih boleh membaca data. Sertakan SQLite WAL/SHM, media, eksport sementara, swap, sandaran dan muat turun pelayar dalam perancangan storan. Isipadu Docker tidak disulitkan semata-mata kerana ia adalah isipadu. TgWitness tidak melaksanakan SQLCipher atau penyulitan objek.

## Kunci induk luaran

Untuk pemasangan **baharu**, letakkan kunci induk di luar direktori data. Ini tidak secara automatik memindahkan peti kunci tempatan sedia ada. Sediakan direktori kunci yang hanya boleh diakses oleh identiti perkhidmatan, kemudian jalankan:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, menggunakan persekitaran projek yang dipasang:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

Dalam Docker, pasang fail secara baca sahaja di luar `/data`, contohnya di `/run/secrets/tgwitness-master.key`, dan tetapkan pembolehubah persekitaran kepada laluan tersebut. UID perkhidmatan mesti dapat membacanya. Sampaikan laluan, bukan bait kunci, melalui fail persekitaran/konfigurasi.

Setiap ruang kerja menerima garam awam rawak dan kunci Fernet sendiri yang diperoleh melalui HKDF-SHA256. `vault.external.json` menyimpan metadata derivasi, bukan kunci utama. Kunci yang hilang/salah akan menyebabkan permulaan gagal tanpa menggantikannya secara senyap. Simpan kedua-dua metadata garam dan kunci utama untuk pemulihan.

Semua ruang kerja berpunca daripada kunci induk yang sama; komprominya menjejaskan keseluruhan pemasangan. Proses yang sedang berjalan boleh menyahsulitkan rahsia. Ini bukan HSM atau KDF kata laluan. Kata laluan sewenang-wenangnya tidak diterima sebagai ganti kunci rawak.

Simpan kunci sedia ada untuk pemasangan sedia ada sehingga migrasi yang disengajakan dilaksanakan dan disahkan. Memadam `vault.key` atau menggantikan kunci induk boleh memusnahkan akses kepada sesi/kunci penandatanganan. Simpan sandaran yang disulitkan dan kunci secara berasingan dan uji pemulihan dalam contoh terasing.

## Sumber dan skop pengesahan

Disemak pada 26 Oktober 2026:

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0: SQLiteSession, StringSession, String`Connection._proxy_connect`, String `TcpMTProxy.normalize_secret` dan kaedah muat turun.

Ujian tempatan merangkumi tetapan loopback SOCKS5/HTTP CONNECT, sesi SQLite sintetik, pengasingan laluan, pengecualian rahsia dan penolakan kunci hilang. Ia tidak menetapkan interoperabiliti sebenar Telegram/proksi atau tingkah laku MTProxy secara langsung. Lihat [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/) dan [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
