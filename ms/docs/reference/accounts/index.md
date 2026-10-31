# Akaun dan format sesi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/

Log masuk melalui telefon, kod QR atau kunci auth, import sesi Telethon, Pyrogram atau Telegram Desktop, dan jalankan beberapa akaun.

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

Anda boleh log masuk tanpa mencipta aplikasi API Telegram. Apabila tiada pasangan dimasukkan, diimport atau telah disimpan dalam ruang kerja, TgWitness akan memilih satu pasangan daripada kolam terbina dalam 50 pasangan API awam (`tgwitness/api_pool.py`) secara rawak. Jika Telegram menolak sepasang (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), sepasang seterusnya akan dicuba, sehingga lapan setiap log masuk; sepasang yang ditolak akan dilangkau sehingga dimulakan semula. Sepasang yang telah log masuk disimpan bersama akaun dan digunakan semula untuknya. **ID API** dan **hash API** mengenal pasti aplikasi kepada Telegram; ia tidak memberi kebenaran kepada mana-mana akaun dengan sendirinya.

Untuk menggunakan aplikasi anda sendiri sebaliknya (akaun yang mendaftarkannya adalah yang berisiko; lihat [Mengapa kolam API terbina dalam?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. Buka [my.telegram.org](https://my.telegram.org) dan log masuk dengan mana-mana nombor telefon yang anda miliki. Kod akan sampai dalam aplikasi Telegram, bukan melalui SMS.
2. Pilih **alat pembangunan API**.
3. Buat aplikasi: mana-mana tajuk dan nama ringkas (5–32 huruf), platform **Desktop**. URL dan keterangan boleh dibiarkan kosong.
4. Salin **ID aplikasi api_id** (sebuah nombor) dan **hash aplikasi api_hash** (32 aksara heksadesimal).

Di panel, buka **ID API + Hash** di bawah borang log masuk. Anda boleh menampal satu pasang `api_id:api_hash` ke dalam **ID API** dan kedua-dua medan akan diisi. Satu pasang boleh digunakan untuk semua akaun anda. Selepas log masuk berjaya, ia disimpan, disulitkan, dalam ruang kerja itu sahaja dan tidak pernah dihantar semula ke pelayar.

Tiga kelayakan berbeza terlibat:

| Rahsia | Membuka | Tempat ia berada |
| --- | --- | --- |
| Panel token | Panel web TgWitness | `panel-token.txt` dalam direktori data, atau `TGWITNESS_TOKEN` |
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

- Fail diubah **dalam memori** pada pelayan TgWitness anda. Muatan tidak disimpan, fail ZIP tidak diekstrak ke cakera dan tiada perkhidmatan luaran dihubungi.
- Sesi yang terhasil kemudian disemak dengan Telegram. Jika fail menyatakan ID pengguna, ia mesti sepadan dengan akaun yang dilaporkan oleh Telegram.
- Fail yang menerangkan akaun berbeza atau kelayakan API berbeza ditolak daripada memilih satu.
- **Kod laluan atau teks sesi** menempatkan medan kod laluan tempatan TData, satu kotak untuk menampal StringSession dan **fail Baca tanpa mendaftar masuk** (mengisi borang tanpa berhubung dengan Telegram).

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
- Medan lain seperti `phone`, `device`, `sdk`, `app_version`, `lang_pack` atau kata laluan `twoFA` yang disimpan **diabaikan**. Jika akaun mempunyai 2FA, TgWitness akan memintanya.
- JSON itu sendiri hanyalah metadata. Tanpa fail sesi, teruskan dengan log masuk telefon atau QR.

### Telegram Desktop (TData)

TData ialah folder `tdata` aplikasi Telegram Desktop (aplikasi rentas platform dari desktop.telegram.org).

| Sistem | Lokasi lalai `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram mudah alih: seterusnya `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Untuk mengimportnya:

> **Amaran sesi selari.** Mengimport TData menggunakan semula kunci kebenaran Telegram Desktop; ia tidak mencipta log masuk berasingan. Jangan gunakan kunci itu dalam Desktop dan TgWitness serentak. Telegram boleh membatalkan kebenaran dengan `AUTH_KEY_DUPLICATED`, menjadikan kedua-dua salinan tidak dapat digunakan sehingga log masuk baru.
>
>
>
> Tutup Desktop sepenuhnya, termasuk proses dulang sistemnya, dan biarkan salinan itu tertutup sementara TgWitness menggunakan sesi yang diimport. **Tutup, jangan log keluar atau batalkan sesi:** pembatalan juga membatalkan salinan yang diimport. Jika anda perlu kedua-dua klien berjalan, log masuk ke TgWitness melalui telefon atau QR untuk mencipta kebenaran tersendiri. Akaun khusus disyorkan, tetapi tidak menjadikan kunci klon selamat untuk digunakan serentak.
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
| `string_session` (`session_string`, `session`) | Telethon StringSession teks, bukan nama fail |
| `auth_key` (`auth_key_hex`) + `dc_id` | Lengkapkan Kunci Auth 512-karakter dan DC 1–5 |
| `user_id` (`id`) | Pilihan; disemak menentang Telegram sebelum kebenaran disimpan |

Jika kedua-dua nama samaran dan nama utama wujud, ia mesti sepadan. Contoh:

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

Gunakan **Akaun → Import akaun** untuk menambah beberapa akaun, memadankan fail mengikut nama asas dan melihat hasil setiap log masuk. Setiap akaun mendapat ruang kerja sendiri. Kumpulan boleh menyalin tetapan terpilih daripada templat tanpa menggabungkan sesi, kunci atau bukti. Lihat [panduan import dan kumpulan](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) dan [papan pemuka kumpulan MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Log keluar

**Akaun → Log keluar daripada Telegram** (dengan pemerhatian dihentikan) meminta Telegram menamatkan sesi, jadi ia juga akan hilang daripada **Tetapan → Peranti** akaun, dan memadam sesi daripada peti keselamatan ruang kerja. Jurnal, sumber, tetapan dan kunci tandatangan kekal, dan jurnal merekodkan log keluar tersebut. Ruang kerja masih milik akaunnya: hanya akaun itu sahaja yang boleh menyambung semula kepadanya. Jika Telegram tidak menjawab, sesi masih dipadamkan di sini dan panel akan memberitahu demikian; tamatkan sesi itu di Telegram di bawah **Tetapan → Peranti**.

## Menukar sesi Telethon ke luar talian

Panel mengimport fail `.session` secara langsung. Untuk penukaran luar talian kepada fail StringSession, jalankan dari folder projek:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Pengubah hanya membaca Telethon SQLite (sehingga 64 MiB), tidak pernah mengubah input, tidak membuat sebarang permintaan rangkaian dan enggan menimpa fail keluaran sedia ada.

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
| Sambungan proksi gagal | Semak laluan dan mod IP. MTProxy automatik mencuba entri lain yang berfungsi. Mod Sembunyikan IP menunggu; mod sandaran yang dipilih secara eksplisit boleh menyambung terus selepas kelewatan yang dikonfigurasikan. Lihat [mod penjejakan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes). |

Lihat juga: [sambungan dan keselamatan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) untuk proksi dan penyulitan, dan [bagaimana pengumpulan berfungsi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/) untuk apa yang dirakam selepas log masuk.
