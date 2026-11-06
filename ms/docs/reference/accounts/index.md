# Telegram · Akaun dan format sesi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/

Log masuk melalui telefon, kod QR atau kunci auth, import sesi Telethon, Pyrogram atau Telegram Desktop, dan jalankan beberapa akaun.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Permulaan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/quickstart/)

![Memulakan](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness log masuk sebagai **akaun pengguna Telegram** (bukan bot) melalui MTProto, menggunakan Telethon. Setiap akaun wujud dalam **ruang** kerja sendiri (dipanggil *workspace* dalam API dan alat baris perintah) dengan sesi, sumber, jurnal dan kunci tandatangan masing-masing.

Fail sesi, rentetan sesi dan Kunci Auth adalah **kebenaran akaun**: sesiapa yang memegangnya boleh bertindak sebagai akaun tersebut. Ia tidak mengandungi sejarah mesej.

> [!AMARAN] **Jangan gunakan apa-apa yang anda tidak mampu kehilangannya.** Kami sangat menasihatkan agar tidak menyambungkan akaun peribadi atau akaun yang berharga, dan agar tidak mencipta ID API / hash API pada akaun yang anda hargai. Ini bukan mengenai TgWitness yang belum diuji: Telegram mengehadkan dan mengharamkan akaun secara tidak menentu — untuk jumlah permintaan yang dianggap berlebihan, tanpa mengira klien atau tujuannya, tanpa dokumentasi yang mencukupi. Banyak pengharaman adalah tidak dapat dipulihkan. Gunakan akaun khusus. Kelancaran pelaksanaan ujian bergantung pada Telegram, bukan pada perisian, dan tidak menjamin apa-apa untuk masa hadapan.

- [Sekilas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#at-a-glance)
- [Sebelum anda bermula: ID API dan hash API](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Nombor telefon](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#phone-number) · [Kod QR](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#qr-code) · [Kunci Auth + ID DC](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#auth-key--dc-id)
- [Fail akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#pyrogram-session) · [Pasangan sesi + JSON](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#telethon-stringsession) · [JSON Akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#account-json)
- [Kenal pasti apa yang anda ada](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#identify-what-you-have) · [Format yang tidak disokong](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#unsupported-formats)
- [Beberapa akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#multiple-accounts) · [Menjaga keselamatan fail akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#keeping-account-files-safe) · [Pemecahan masalah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#troubleshooting)

## Sekilas

| Apa yang anda ada | Tab dalam **Tambah Akaun** | Anda juga akan memerlukan |
| --- | --- | --- |
| Nombor telefon dan akses kepada kod log masuknya | **Telefon** | Kata laluan 2FA jika diaktifkan |
| Telegram dibuka pada peranti lain | **Kod QR** | Kata laluan 2FA jika diaktifkan |
| Fail `.session` (Telethon atau Pyrogram) | **Fail** | JSON pilihan untuk tetapan aplikasi |
| `.session` + `.json` dengan nama yang sama | **Fail** (pilih kedua-duanya) | Biasanya tiada apa-apa lagi |
| Folder `tdata` Telegram Desktop | **Fail** (sebagai ZIP) | Kod laluan tempatan Desktop jika ditetapkan |
| Sesi Rangkaian Telethon (teks, `.txt`, `.tgwitness-session`) | **Fail** | Tiada pasangan API berasingan diperlukan |
| `.json` dengan sesi atau Kunci Auth | **Fail** | Tiada pasangan API berasingan diperlukan |
| Kunci Auth (512 aksara heksadesimal) dan nombor DC-nya | **KunciAuth** | ID Pengguna Pilihan |

TgWitness mengenali fail berdasarkan **kandungannya**, bukan namanya. Menama semula fail tidak pernah mengubahnya.

## Sebelum anda bermula: ID API dan hash API

Anda boleh log masuk tanpa mencipta aplikasi API Telegram. Apabila tiada pasangan dimasukkan, diimport atau sudah disimpan dalam ruang kerja, TgWitness memilih sepasang daripada kolam terbina dalamnya 50 pasangan API awam (`tgwitness/api_pool.py`), memprioritkan Telegram Desktop untuk log masuk baharu dan mengekalkan pasangan yang disimpan terlebih dahulu; calon-calon selebihnya dikocok. Jika Telegram menolak sepasang (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), yang seterusnya akan dicuba, sehingga lapan setiap log masuk; pasangan yang ditolak akan dilangkau sehingga dimulakan semula. Pasangan yang telah log masuk disimpan bersama akaun dan digunakan semula untuknya. Satu **ID API** dan **Hash API** mengenal pasti aplikasi kepada Telegram; mereka tidak memberi kebenaran akaun dengan sendirinya.

Medan sambungan yang hilang menggunakan pasangan peranti/OS deterministik daripada [katalog opentele2 2.0.0](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735) yang disertakan: Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, dan Web `2496`. ID binaan sumber Android `4` juga menggunakan katalog Android, seperti yang dikenal pasti dalam [BuildVars Telegram Android](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web secara lalai adalah A; sufix versi aplikasi `K` yang diimport atau pek bahasa `macos` memilih K, dan versi `0.7.0` memilih Webogram. ID aplikasi yang tidak diketahui mengekalkan lalai hos Telethon. Medan yang diimport sentiasa diutamakan, termasuk versi aplikasi yang lebih lama dan pek bahasa yang kosong. Katalog tidak pernah menukar ID/hash API. Snapshot versinya disemak secara eksplisit, bukan dimuat semasa log masuk. Profil yang disimpan kekal stabil selepas kemas kini.

`account.getAuthorizations` melaporkan metadata kebenaran yang disimpan oleh Telegram; ia bukan salinan bagi setiap `initConnection` yang baharu. Bandingkannya dengan profil yang sebenarnya dihantar. Menghubungkan kebenaran sedia ada tidak mengesahkan hash API penemanannya: `initConnection` menghantar ID API, manakala hash digunakan oleh permintaan log masuk.

Selepas pengesahan telefon baru atau QR, TgWitness meminta konfigurasi, DC terdekat, status dalam talian, bahasa (apabila pek bahasa tidak kosong), kemas kini aplikasi dan kemas kini terma perkhidmatan, dengan selang 0.3–1.5 saat antara permintaan. Mengemas kini status secara ringkas menandakan akaun sebagai dalam talian. Urutan ini dijalankan sekali selepas log masuk selesai, bukan semasa import, sambungan semula atau permulaan semula. Kebenaran diberikan terlebih dahulu; permintaan yang gagal menhentikan urutan tanpa mencuba semula atau membatalkan log masuk. Keputusan direkod sebagai `account.initialized`, dengan nama ralat dan bukannya badan respons. Urutan ini bukan jaminan terhadap sekatan akaun.

Untuk `tdesktop` , `tz_offset` yang hilang menggunakan selisih UTC tempatan pelayan, dibundarkan ke 900 saat menggunakan [algoritma opentele2](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; lesen dalam `tgwitness/client_profiles.LICENSE` ). Ia dikemas kini pada setiap pautan supaya perubahan penjimatan waktu diambang. `tz_offset` yang diimport diutamakan pada setiap platform dan dikekalkan dengan tepat, termasuk sifar. Kemasukan `initConnection.params` lain dikekalkan. Borang log masuk HTTP menerima zon waktu numerik yang dikembalikan oleh import fail; boolean, pecahan dan selisih di luar julat yang disokong ditolak.

Rute Direct, SOCKS5 dan HTTP CONNECT menggunakan `ConnectionTcpObfuscated` Telethon (MTProto ringkas yang di-obfuskasi). HTTPS CONNECT mengekalkan TLS ke proksi dan menggunakan pengangkutan yang di-obfuskasi yang sama di dalam terowong. MTProxy mengekalkan pengangkutan perantara rawak yang diperlukan dan pengendalian rahsia. Peralihan rute menerapkan pilihan yang sama. Pengaburan mengubah bingkai paket; ia tidak menyembunyikan akaun atau metadata kliennya daripada Telegram atau menunjukkan kebebasan daripada sekatan.

Selepas menyambungkan klien yang dibenarkan, TgWitness memeriksa konfigurasi, DC terdekat, kebenaran semasa, garis dasar lapisan yang disemak, bahasa, kemas kini aplikasi dan kemas kini terma perkhidmatan. Diagnostik ini dijalankan sekali bagi setiap instans klien, sebelum pengumpulan, dan dipaparkan di bawah butiran sambungan beserta waktunya. `account.connection_checked` merekodkan keputusan tanpa hash sesi, IP, token atau hash API. Ia tidak pernah menerima terma atau memasang kemas kini. Kegagalan permintaan atau FloodWait menghentikan permintaan seterusnya; keputusan yang hilang kekal tidak diketahui. Semakan tempatan masih boleh melaporkan keputusan mereka manakala semakan rangkaian diabaikan.

Diagnostik FloodWait mengekalkan kaedah TL yang gagal, sebarang pembalut Takeout/range, menunggu yang diminta oleh pelayan dan tarikh akhir berkesan dalam `telegram.backoff`. Butiran sambungan memaparkan kaedah dan tarikh akhir semasa permintaan ditangguhkan. Diagnostik ini termasuk pengira panggilan klien bagi setiap kaedah sejak klien itu dicipta; ia mengira penyelesaian rakan sebaya bersarang secara berasingan, tetapi tidak mengira paket atau percubaan cuba semula dalaman Telethon. Pengira semasa juga tersedia sebagai `collector.rpc_activity` dalam API status. Tiada hujah permintaan, nama pengguna, hashes akses atau teks pengecualian disertakan. Diagnostik terakhir dan tarikh akhir penuh akan kekal selepas permulaan semula. Tempoh menunggu terdahulu tanpa rekod kaedah tidak dapat dikaitkan semula. Lihat [had eksport](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) untuk semakan sumber dan perbezaan antara penemuan dan pemerolehan sejarah.

`official_app=True` atau `False` ialah penanda kebenaran semasa Telegram. Tiada satu pun nilai tersebut menentukan sama ada akaun itu terhad, dipercayai atau sedang diperhatikan. Snapshot sedia ada mod bukti `account.devices` kekal sebagai sejarah semua peranti yang log masuk; diagnostik sambungan hanya mengekalkan penerangan peranti semasa.

Sebelum sambungan, pemeriksaan penasihat membandingkan platform API, pek bahasa, format peranti/OS dan versi aplikasi, lokel sistem mudah alih, dan lapisan skema sebenar Telethon dengan garis dasar katalog yang disemak. Amaran muncul dalam log pelayan dan metadata status akaun; ia tidak pernah menggantikan nilai yang diimport atau mengubah lapisan skema. Lapisan yang berbeza adalah isyarat semakan keserasian, bukan bukti akaun yang rosak atau terhad. Semakan ini dan `official_app` tidak mengesahkan bahawa Telegram menganggap akaun tersebut selamat daripada sekatan. Status akaun terputus menggunakan profil yang disimpan dan bukannya menjana penerangan peranti lain.

Untuk menggunakan aplikasi anda sendiri sebaliknya (akaun yang mendaftarkannya adalah yang berisiko; lihat [Mengapa kolam API terbina dalam?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. Buka [my.telegram.org](https://my.telegram.org) dan log masuk dengan mana-mana nombor telefon yang anda miliki. Kod akan sampai dalam aplikasi Telegram, bukan melalui SMS.
2. Pilih **alat pembangunan API**.
3. Buat aplikasi: mana-mana tajuk dan nama ringkas (5–32 huruf), platform **Desktop**. URL dan keterangan boleh dibiarkan kosong.
4. Salin **ID aplikasi api_id** (sebuah nombor) dan **hash aplikasi api_hash** (32 aksara heksadesimal).

Di panel, buka **ID API + Hash** di bawah borang log masuk. Anda boleh menampal satu pasang `api_id:api_hash` ke dalam **ID API** dan kedua-dua medan akan diisi. Satu pasang boleh digunakan untuk semua akaun anda. Selepas log masuk berjaya, ia disimpan, disulitkan, dalam ruang kerja itu sahaja dan tidak pernah dihantar semula ke pelayar.

Tiga kelayakan berbeza terlibat:

| Rahsia | Membuka | Tempat ia berada |
| --- | --- | --- |
| Token panel | Panel web TgWitness | `panel-token.txt` dalam direktori data, atau `TGWITNESS_TOKEN` |
| ID API + hash | Tiada apa-apa sendirian; mengenal pasti aplikasi | Pasangan terbina dalam, tetapan import, atau aplikasi anda sendiri di my.telegram.org |
| Pengesahan akaun | Akaun Telegram | Dicipta melalui log masuk telefon/QR atau dibawa masuk sebagai sesi |

Jika Telegram perlu diakses melalui proksi, tetapkan ia terlebih dahulu di **Akaun → Tetapan → Tetapan sambungan → Ubah laluan sambungan**.

## Nombor telefon

1. Buka **Akaun**, tab **Telefon**, dan masukkan nombor dalam format antarabangsa, contohnya `+44 7700 900123`. Ruang dan garisan dialih keluar secara automatik.
2. Tekan **Teruskan**. ID API + Hash boleh dibiarkan kosong.
3. Masukkan kod yang dihantar oleh Telegram (biasanya ke aplikasi Telegram; SMS tidak dijamin).
4. Jika akaun mempunyai pengesahan dua langkah, masukkan kata laluan itu. Ia bukan token panel dan bukan kod akses peranti.
5. Semak ID akaun yang dipaparkan selepas log masuk, kemudian pilih sumber.

Kod log masuk dan kata laluan 2FA tidak pernah ditulis ke cakera.

## Kod QR

Gunakan ini apabila akaun sudah log masuk pada telefon atau komputer lain.

1. Tab **Kod QR** → **Tunjukkan Kod QR**. ID API + Hash boleh dibiarkan kosong.
2. Pada peranti yang telah log masuk: **Tetapan → Peranti → Pautkan Peranti Desktop**, imbas kod dan sahkan.
3. Masukkan kata laluan 2FA dalam TgWitness jika Telegram memintanya.

Imej QR dijana secara tempatan. Kod akan tamat tempoh; tekan **'Jana Kod QR lain'** untuk mencuba semula. Mengunci panel, menukar ruang kerja atau memulakan log masuk lain akan membatalkan kod yang sedang menunggu.

## Kunci Auth + ID DC

Kunci Auth ialah kebenaran mentah 256 bait di sebalik setiap sesi Telegram, ditulis sebagai **512 aksara heksadesimal**, bersama nombor pusat data **DC 1–5**.

1. Tab **Auth kunci**. Tampal keseluruhan kunci; kunci yang dipendekkan yang mengandungi `…` tidak akan berfungsi.
2. Pilih ID DC yang disediakan bersama kunci.
3. Secara pilihan, masukkan **ID Pengguna**. TgWitness kemudiannya menolak sambungan jika Telegram melaporkan akaun yang berbeza.
4. Tekan **akaun Connect**.

Kunci Auth (512 aksara) bukan hash API (32 aksara). Kunci yang sama juga boleh diimport sebagai JSON, lihat [JSON Akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#account-json).

## Fail akaun

Buka **Tambah akaun → Fail** dan pilih sehingga **empat fail milik satu akaun**, jumlahnya **8 MiB**, kemudian tekan **Sambungkan akaun**.

Borang **Fail**, **Kunci Auth** dan import pukal memaparkan amaran sesi selari sebelum menyambung. Secara lalai, kebenaran yang diimport akan digunakan semula. Biarkan klien asal tertutup selagi kuncinya digunakan di sini. **Fail** dan **Kunci Auth** juga menawarkan pilihan untuk **Mewujudkan kebenaran bebas**, seperti yang diterangkan di bawah. Import pukal masih menggunakan mod langsung. Log masuk telefon dan QR interaktif mewujudkan kebenaran berasingan. Heading amaran kekal kelihatan dalam borang import; penjelasan penuh akan dibuka secara automatik apabila fail atau rentetan kunci/sesi disediakan. Ia boleh dilipat selepas dibaca, supaya pemilih fail dan kawalan sambungan kekal boleh digunakan pada telefon.

- Fail diubah **dalam memori** pada pelayan TgWitness anda. Muatan tidak disimpan, fail ZIP tidak diekstrak ke cakera dan tiada perkhidmatan luaran dihubungi.
- Sesi yang terhasil kemudian disemak dengan Telegram. Jika fail menyatakan ID pengguna, ia mesti sepadan dengan akaun yang dilaporkan oleh Telegram.
- Fail yang menerangkan akaun berbeza atau kelayakan API berbeza ditolak daripada memilih satu.
- **Kod laluan atau teks sesi** menempatkan medan kod laluan tempatan TData, satu kotak untuk menampal StringSession dan **fail Baca tanpa mendaftar masuk** (mengisi borang tanpa berhubung dengan Telegram).

### Buat kebenaran bebas

Pilih **'Buat kebenaran bebas** sebelum menyambungkan fail yang diimport atau Kunci Auth'. TgWitness menyambungkan penderma yang diimport seketika, menggunakannya untuk meluluskan token log masuk QR klien baru, dan memutuskan sambungan penderma itu serta-merta selepas kelulusan. Klien baru mempunyai kunci kebenaran sendiri dan profil Desktop yang dipilih secara berasingan. Butiran API dan profil peranti yang disediakan oleh penderma hanya digunakan untuk sambungan penderma tersebut. Tiada kebenaran sedia ada yang akan dilog keluar atau dibatalkan.

**Biarkan klien asal penderma kekal ditutup sepenuhnya semasa langkah ini.** Sambungan awal masih menggunakan kuncinya yang disalin, jadi mod ini tidak dapat menghapuskan risiko penggunaan serentak awal tersebut. Setelah kebenaran baharu disambungkan, pemilik boleh membuka semula klien asal dan menggunakan kedua-duanya secara berasingan. Log masuk **kod QR** interaktif membolehkan klien asal meluluskan log masuk tanpa menyalin atau menyambungkan kuncinya di sini.

Jika Telegram meminta 2FA, mod ini menggunakan `twoFA` daripada JSON yang dipilih apabila tersedia, atau meminta kata laluan. Kata laluan yang diimport dan ditolak akan kembali ke borang kata laluan. Kata laluan tidak disimpan. Kunci calon disimpan secara disulitkan dalam `independent_login.enc`, termasuk perubahan semasa migrasi pusat data. Selepas gangguan, pilih penderma yang sama dan pilihan ini untuk menyambung semula calon yang disimpan. Ruang kerja kekal diperuntukkan untuk akaun tersebut; kegagalan penyempurnaan tidak memadam ruang kerja baru. Kekalkan direktori datanya dan kunci peti besi. Butiran pengesahan akhir dan rekod jurnal `account.authorized` merangkumi kaedah import, format input dan ID API penderma, tanpa kunci atau kata laluan penderma.

Pada 5 November 2026, sebuah akaun khusus lulus pemeriksaan langsung dengan penderma Telethon, Pyrogram dan TData: penyempurnaan 2FA, kunci kebenaran baharu yang berasingan, capaian serentak oleh penderma dan klien baharu, dan membaca saluran awam. Kes Telethon juga memulihkan calon yang disimpan selepas gangguan pada langkah kata laluan. Setiap kebenaran baharu melengkapkan enam permintaan inisialisasi pasca-log masuk, dan jurnal yang disahkannya disemak. Sesi asal kekal boleh digunakan dalam semua empat format yang disediakan.

[Pangkalan data ralat RPC](https://core.telegram.org/api/errors.json) Telegram mengaitkan `FRESH_CHANGE_ADMINS_FORBIDDEN` dengan pertukaran pentadbir, `FRESH_CHANGE_PHONE_FORBIDDEN` dengan pertukaran nombor telefon, dan `FRESH_RESET_AUTHORISATION_FORBIDDEN` dengan membatalkan sesi lain, mengubah jangka hayat mereka atau mendaftarkan kunci laluan. `SESSION_TOO_FRESH_*` dan `PASSWORD_TOO_FRESH_*` berkaitan pemindahan pemilikan dan pengeluaran hasil atau hadiah. Ini bukan operasi kutipan; log masuk baru tidak bermakna larangan membaca menyeluruh selama 24 jam. Eksport boleh memulangkan `TAKEOUT_INIT_DELAY_*` secara berasingan. TgWitness mengekalkan jeda yang diminta oleh pelayan dan tidak mencuba semula penerimaan token secara automatik atau membatalkan sesi untuk mengatasi sekatan.

### Telethon `.session`

|  |  |
| --- | --- |
| Apa itu | Pangkalan data SQLite yang dicipta oleh alat berasaskan Telethon, contohnya `my_account.session` |
| Diiktiraf oleh | Jadual `sessions` (dengan `dc_id`, `server_address`, `port`, `auth_key`) dan `version` = 7 atau 8 |
| Keperluan | Satu baris sesi bertauliah tepat; pangkalan data tertutup dan lengkap |

Tutup program yang mencipta fail itu terlebih dahulu. Jika `my_account.session-journal` atau `my_account.session-wal` wujud di sebelahnya, pangkalan data belum dimuktamadkan: buka dan tutup klien asal dengan sempurna. Memadam fail sidecar tersebut boleh meninggalkan salinan yang rosak.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Apa itu | Pangkalan data SQLite yang dihasilkan oleh alat berasaskan Pyrogram |
| Diiktiraf oleh | Jadual `sessions` dengan `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 atau 3 |
| Keperluan | Satu sesi **pengguna** bertauliah pada rangkaian pengeluaran. Sesi bot dan test-DC ditolak |

ID pengguna yang disimpan disemak menentang Telegram semasa log masuk.

### Pasangan sesi + JSON

Akaun sering diedarkan sebagai dua fail dengan nama yang sama, contohnya `447700900123.session` dan `447700900123.json`. Pilih **kedua-duanya** sekaligus.

- Daripada JSON, TgWitness menggunakan `app_id`/`api_id` dan `app_hash`/`api_hash`, jadi anda biasanya tidak perlu menaip kelayakan API.
- Profil sambungan menggunakan `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` dan `tz_offset` pilihan (saat dari UTC, -43200 hingga 50400). Medan yang dibekalkan diutamakan berbanding lalai yang dijana dan bahasa panel/pelayar. Alias yang bertembung ditolak. Profil yang diselesaikan disimpan dalam kredensial ruang kerja yang disulitkan dan digunakan semula selepas but semula, termasuk versi aplnya.
- `phone`, tetapan proksi dan token peranti **diabaikan**. `twoFA` hanya boleh dibaca apabila **Buat kebenaran bebas** dipilih; import terus mengabaikannya.
- JSON tanpa medan kebenaran yang disokong hanyalah metadata. Tambah fail sesi atau teruskan dengan log masuk telefon atau QR. JSON yang mengandungi sesi yang disokong atau Kunci Auth boleh memberi kebenaran sendiri; lihat [JSON Akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData ialah folder `tdata` aplikasi Telegram Desktop (aplikasi rentas platform dari desktop.telegram.org).

| Sistem | Lokasi lalai `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram mudah alih: seterusnya `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Untuk mengimportnya:

> **Amaran sesi selari.** Import TData terus menggunakan kunci kebenaran Telegram Desktop. Jangan gunakan kunci itu dalam Desktop dan TgWitness serentak. Telegram boleh membatalkan kebenaran dengan `AUTH_KEY_DUPLICATED`, menjadikan kedua-dua salinan tidak dapat digunakan sehingga log masuk semula.
>
>
>
> Tutup Desktop sepenuhnya, termasuk proses dulanginya, dan biarkan salinan itu tertutup semasa TgWitness menggunakan sesi yang diimport. **Tutup, jangan log keluar atau batalkan sesi:** pencabutan juga membatalkan salinan yang diimport. Jika anda perlu kedua-dua klien berjalan, pilih **Buat kebenaran bebas** dan biarkan Desktop tertutup sehingga log masuk baru berjaya, atau log masuk ke TgWitness melalui telefon atau QR. Akaun khusus disyorkan, tetapi tidak menjadikan kunci klon selamat untuk digunakan secara serentak.
>
>
>
> Ini juga terpakai kepada fail `.session` yang diimport, teks StringSession dan HEX Auth Key. Klien lain dengan kebenaran yang dicipta secara bebas boleh kekal log masuk. Rujuk [dokumentasi AUTH_KEY_DUPLICATED Telegram](https://core.telegram.org/api/errors#406-not-acceptable).

1. Batalkan sepenuhnya Telegram Desktop.
2. Buat fail ZIP yang mengandungi **hanya** kedua-dua item ini daripada `tdata`:

   - `key_datas`
   - pengakhiran fail 16 aksara yang berakhir dengan `s` di sebelahnya, biasanya `D877F783D5D3EF8Cs`

   Memampatkan keseluruhan folder dengan cache medianya biasanya melebihi had (512 entri, 32 MiB selepas dipadamkan). 3. Pilih fail ZIP dalam **Fail**. Jika Telegram Desktop mempunyai **kod akses tempatan**, masukkan kod tersebut di bawah **Kod Akses atau teks sesi** terlebih dahulu. Ini bukan kata laluan 2FA.

Disokong: satu akaun setiap arkib, storan moden `key_datas`/`key_data0`/`key_data1`, kod akses tempatan. Tidak disokong: folder dengan beberapa akaun yang log masuk, susun atur Desktop lama, fail ZIP yang dilindungi kata laluan, dan aplikasi asli macOS berasingan "Telegram for macOS".

### Telethon StringSession

Satu baris teks, biasanya bermula dengan `1` dan berketinggian kira-kira 350 aksara. Muatkan ia sebagai fail `.txt` atau `.tgwitness-session` (maksimum 4 KiB), atau tampal di bawah **Passcode atau teks sesi**. Hanya rentetan Telethon diterima; rentetan Pyrogram dan TDLib menggunakan format berbeza.

### JSON Akaun

Satu objek JSON, maksimum **64 KiB**, dalam fail yang berakhir dengan **`.json`**.

| Medan (nama samaran) | Maksud |
| --- | --- |
| `api_id` (`app_id`) | ID Aplikasi, satu nombor positif |
| `api_hash` (`app_hash`) | Hash aplikasi, 32 aksara heksadesimal |
| `string_session` (`session_string`, `session_str`; `session` lama) | Telethon StringSession teks, bukan nama fail |
| `auth_key` (`auth_key_hex`) + `dc_id` | Lengkapkan Kunci Auth 512-karakter dan DC 1–5 |
| `user_id` (`id`) | Pilihan; disemak menentang Telegram sebelum kebenaran disimpan |
| `device_model` (`device`) | Deskripsi peranti sambungan |
| `system_version` (`sdk`) | Versi OS Sambungan |
| `app_version` | Versi aplikasi dihantar ke Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Bahasa klien, bahasa sistem dan pek bahasa klien; pek `lang_pack` kosong dibenarkan |
| `tz_offset` | Peralihan UTC pilihan dalam saat, dihantar dalam `initConnection.params`; rentetan integer atau integer perpuluhan |

Jika kedua-dua nama samaran dan nama utama wujud, ia mesti sepadan. Medan sesi Telethon eksplisit diutamakan berbanding blok `session` generik dalam format lain. Jika kedua-duanya mengandungi sesi Telethon yang boleh dikenali, ia mesti menerangkan kebenaran yang sama. Tanpa medan eksplisit, `session` mesti merupakan StringSession Telethon yang sah. Contoh:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

Contoh pertama hanya mengisi kelayakan API; log masuk melalui telefon atau QR, atau tambahkan fail sesi. Senarai pukal (susunan JSON akaun) tidak diterima.

## Kenal pasti apa yang anda ada

| Anda lihat | Ia | Gunakan |
| --- | --- | --- |
| `*.session`; membukanya dalam penyunting teks memaparkan `SQLite format 3` di bahagian atas | Telethon atau Pyrogram SQLite | **Fail** (dikesan secara automatik) |
| Satu folder `tdata` yang mengandungi `key_datas` | Telegram Desktop TData | ZIP dua fail, kemudian **Fail** |
| Satu baris teks bermula dengan `1`, kira-kira 350 aksara | Telethon StringSession | **Fail** |
| `*.json` dengan `app_id`/`app_hash` | Metadata rakan | **Fail-fail**, bersama sesi |
| `*.json` dengan `auth_key` atau `string_session` | JSON Akaun | **Fail** |
| 512 aksara `0-9a-f` | Kunci Auth | **KunciAuth** |
| 32 aksara `0-9a-f` | Hash API | **ID API + Hash** |
| `td.binlog` atau `db.sqlite` daripada aplikasi TDLib | Simpanan TDLib | Tidak disokong |
| `123456789:AA…` | Token bot | Tidak disokong |

## Format yang tidak disokong

| Format | Alternatif |
| --- | --- |
| Penyimpanan TDLib (`td.binlog`) dan eksport TDLib | Log masuk melalui telefon atau QR |
| **Rentetan** sesi Pyrogram | Gunakan fail Pyrogram `.session`, atau telefon/QR |
| TData dengan beberapa akaun yang log masuk | Log keluar akaun lain dalam Telegram Desktop, atau gunakan fail sesi setiap akaun |
| Token bot | Tidak disokong: TgWitness memerhati sebagai akaun pengguna |
| Senarai CSV/JSON bagi banyak akaun | Import fail sesi yang disokong melalui **Akaun → Import akaun**, atau log masuk menggunakan telefon/QR dalam ruang kerja yang berasingan |
| Sesi Test-DC atau bot | Gunakan akaun pengguna produksi |

## Beberapa akaun

Tekan **+** di sebelah pemilih akaun, atau buka **Akaun → Tetapan → Tetapan sambungan → Workspaces**, masukkan label dan log masuk.

- Sebarang bilangan ruang kerja, termasuk ruang utama. Setiap satu mempunyai sesi, laluan proksi, sumber, dasar tangkapan, jurnal, kunci tandatangan, titik pemeriksaan dan eksport masing-masing.
- Menukar ruang kerja yang dipaparkan tidak menangguhkan ruang kerja yang lain.
- Jurnal kekal terikat kepada akaun yang menciptanya. Log masuk sebagai akaun lain memerlukan ruang kerja lain, dan satu akaun tidak boleh ditugaskan kepada dua ruang kerja.
- Token panel utama mengawal semua ruang kerja. [Akses yang dikeluarkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/) boleh mengehadkan orang lain kepada akaun dan sembang terpilih, dengan kebenaran berasingan dan had sesi.
- **Akaun** menamakan semula ruang kerja dan memadam ruang kerja yang ditambah, termasuk sesi, jurnal, sumber dan kunci tandatangan. Ruang kerja utama tidak boleh dipadam dari panel.

### Import pukal dan kumpulan akaun

Gunakan **Akaun → Import akaun** untuk menambah beberapa akaun, padankan fail mengikut nama asas dan lihat setiap keputusan log masuk. Setiap akaun mendapat ruang kerja sendiri.

Kumpulan mengekalkan akaun berkaitan bersama tanpa menggabungkan sesi, kunci atau bukti mereka. **Membuka kumpulan** pada **Akaun** membawa ke halaman kumpulan itu di `/groups/<id>`:

- **Akaun:** laluan sambungan setiap ahli, pemerhatian dan mesej terakhir, dengan Mulakan**semua** dan **Jeda semua**.
- **Perlu perhatian:** akaun yang telah log keluar, tidak tersedia atau mempunyai masalah sambungan, kemasukan, sumber atau media; setiap nama membawa ke kadnya.
- **Perbualan beberapa akaun lihat:** sumber yang dikongsi, akaun yang memerhatikannya dan gangguan dalam tempoh pemerhatian ruang kerja tersedia (sehingga tujuh hari). **Eksport dengan N akaun** membahagikan eksport saluran atau superkumpulan di antara mereka dan menandatangani satu arkib.
- **Eksport kumpulan:** satu ZIP dengan eksport bermassa tandatangan setiap akaun di bawah `accounts/` dan `manifest.json` menyenaraikan SHA-256 dan cap jari kunci mereka, disahkan oleh ruang kerja utama dalam `manifest.signature.json`. Sahkan setiap arkib akaun secara berasingan dengan `python -m tgwitness.verify` dan cap jari yang dipercayai bagi akaun tersebut.

Ahli berkongsi tetapan kumpulan; akaun boleh mengekalkan nilai tersendiri. Lihat [tetapan yang dikongsi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/settings/#account-groups), [panduan import dan kumpulan](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) dan [papan pemuka kolam MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Log keluar

**Akaun → Log keluar daripada Telegram** (dengan pemerhatian dihentikan) meminta Telegram menamatkan sesi, jadi ia juga akan hilang daripada **Tetapan → Peranti** akaun, dan memadam sesi daripada peti keselamatan ruang kerja. Jurnal, sumber, tetapan dan kunci tandatangan kekal, dan jurnal merekodkan log keluar tersebut. Ruang kerja masih milik akaunnya: hanya akaun itu sahaja yang boleh menyambung semula kepadanya. Jika Telegram tidak menjawab, sesi masih dipadamkan di sini dan panel akan memberitahu demikian; tamatkan sesi itu di Telegram di bawah **Tetapan → Peranti**.

## Menjaga keselamatan fail akaun

- Layan setiap `.session`, TData ZIP, StringSession, Auth Key dan JSON akaun seperti kata laluan. TgWitness menyimpan kebenaran yang diimport dalam peti keselamatan yang disulitkan; anda boleh memadam fail asal selepas itu.
- Jangan jalankan kebenaran yang sama dalam dua program sekaligus. Telegram mungkin membatalkan kebenaran tersebut (`AUTH_KEY_DUPLICATED`), dan kedua-dua salinan akan berhenti berfungsi.
- Sesi yang telah tamat tempoh atau dibatalkan tidak boleh dihidupkan semula melalui penukaran. Log masuk semula.

## Pemecahan masalah

| Mesej atau simptom | Apa yang perlu dilakukan |
| --- | --- |
| *Tidak dapat membaca sesi ini. Tutup klien asalnya…* | Fail SQLite dibuka atau belum selesai (sidecar `-journal`/`-wal`). Tutup program asal dengan kemas dan salin semula fail tersebut. |
| *Skema Telethon SQLite yang disokong: 7 dan 8* / *Pyrogram … 2 dan 3* | Satu versi perpustakaan yang sangat lama atau tidak diketahui telah mencipta fail tersebut. Log masuk melalui telefon/QR sebaliknya. |
| *Hanya sesi pengguna produksi yang dibenarkan disokong* | Fail Pyrogram ini milik bot atau rangkaian ujian. |
| *Arkib TData melebihi 512 entri atau 32 MiB* | ZIP hanya `key_datas` dan `D877F783D5D3EF8Cs`, bukan keseluruhan folder. |
| *Tidak dapat menyahsulit TData. Semak kod laluan tempatan Desktop.* | Masukkan kod laluan tempatan Telegram Desktop di bawah **Passcode atau teks sesi**. |
| *Import satu akaun TData pada satu masa* | Telegram Desktop mempunyai beberapa akaun; lihat [format yang tidak disokong](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#unsupported-formats). |
| *Fail terpilih menerangkan akaun berbeza atau kelayakan API* | Pilih fail daripada satu akaun sahaja. |
| *JSON tidak mengandungi kelayakan API atau kebenaran yang disokong* | Semak nama medan dalam [JSON Akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#account-json). |
| *Hanya metadata API* | JSON tidak mempunyai sesi. Tambahkan fail `.session` atau gunakan telefon/QR. |
| *Kunci Auth HEX mesti mengandungi semua 512 aksara heksadesimal* | Kunci dipotong atau mengandungi `…`. |
| ID akaun tidak sepadan dengan akaun yang diimport | ID pengguna fail itu berbeza daripada yang dilaporkan oleh Telegram; fail itu adalah untuk akaun lain. |
| Akaun ini sudah dimiliki oleh ruang kerja lain | Buka ruang kerja itu bukannya menambah akaun itu dua kali. |
| Disambungkan, tetapi satu kumpulan peribadi hilang daripada senarai sembang dalam **Sumber** | Semak keahlian. Pemilih memeriksa 1,000 dialog pertama; naikkan had di bawah **Parameter**. |
| Sambungan proksi gagal | Periksa laluan dan mod IP. MTProxy automatik mencuba entri lain yang berfungsi. Tunggu menyembunyikan alamat; Direct sebagai pilihan terakhir boleh menyambung terus selepas kelewatan yang ditetapkan. Lihat [mod penjejakan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes). |

Lihat juga: [sambungan dan keselamatan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) untuk proksi dan penyulitan, dan [bagaimana pengumpulan berfungsi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/) untuk apa yang dirakam selepas log masuk.
