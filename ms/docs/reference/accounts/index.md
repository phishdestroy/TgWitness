# Akaun dan format sesi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/

Log masuk melalui telefon, kod QR atau kunci auth, import sesi Telethon, Pyrogram atau Telegram Desktop, dan jalankan beberapa akaun.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/ms/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

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

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`), preferring Telegram Desktop for a fresh login and retaining a saved pair first; remaining candidates are shuffled. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

Missing connection fields use a deterministic device/OS pair from the bundled [opentele2 2.0.0 catalogs](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, and Web `2496`. Android's source-build ID `4` also uses the Android catalog, as identified in [Telegram Android's BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web defaults to A; an imported `K` app-version suffix or `macos` language pack selects K, and version `0.7.0` selects Webogram. Unknown application IDs keep Telethon's host defaults. Imported fields always win, including an older app version and an empty language pack. The catalog never changes the API ID/hash. Its version snapshot is reviewed explicitly, not fetched during login. A saved profile stays stable after updates.

`account.getAuthorizations` reports Telegram's saved authorization metadata; it is not an echo of each new `initConnection`. Compare it with the actual sent profile. Connecting an existing authorization does not validate its companion API hash: `initConnection` sends the API ID, while the hash is used by login requests.

After a new phone or QR authorization, TgWitness requests config, nearest DC, online status, languages (when the language pack is nonempty), app updates and terms-of-service updates, with 0.3–1.5 seconds between requests. Updating status briefly marks the account online. This sequence runs once at login completion, not on imports, reconnects or restarts. The authorization is saved first; a failed request stops the sequence without retrying or discarding the login. Results are recorded as `account.initialized`, with error names rather than response bodies. The sequence is not a guarantee against account restrictions.

For `tdesktop`, a missing `tz_offset` uses the server's local UTC offset, rounded to 900 seconds using the [opentele2 algorithm](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; license in `tgwitness/client_profiles.LICENSE`). It is refreshed on each connection so daylight-saving changes are reflected. An imported `tz_offset` takes precedence on every platform and is kept exactly, including zero. Other `initConnection.params` entries are retained. The HTTP sign-in form accepts the numeric timezone returned by file import; booleans, fractions and offsets outside the supported range are rejected.

Direct, SOCKS5 and HTTP CONNECT routes use Telethon's `ConnectionTcpObfuscated` (obfuscated abridged MTProto). HTTPS CONNECT retains TLS to the proxy and uses the same obfuscated transport inside the tunnel. MTProxy retains its required randomized intermediate transport and secret handling. Route switches apply the same choices. Obfuscation changes packet framing; it does not hide the account or its client metadata from Telegram or imply immunity to restrictions.

After connecting an authorized client, TgWitness checks config, nearest DC, the current authorization, the reviewed layer baseline, languages, app updates and terms-of-service updates. These diagnostics run once per client instance, before collection, and are shown under the connection details with their time. `account.connection_checked` records the result without session hashes, IPs, tokens or API hashes. They never accept terms or install updates. A request failure or FloodWait stops subsequent requests; a missing result stays unknown. Local checks can still report their results while network checks are skipped.

FloodWait diagnostics retain the failed TL method, any Takeout/range wrappers, the server-requested wait and the effective deadline in `telegram.backoff`. Connection details show the method and deadline while requests are paused. The diagnostic includes per-method client-call counters since that client was created; they count nested peer resolution separately, but do not count packets or Telethon's internal retry attempts. Current counters are also available as `collector.rpc_activity` in the status API. No request arguments, usernames, access hashes or exception text are included. The last diagnostic and full deadline survive restart. Earlier waits without a method record cannot be attributed retrospectively. See [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) for the source review and the distinction between discovery and history acquisition.

`official_app=True` or `False` is Telegram's current-authorization flag. Neither value establishes whether the account is restricted, trusted or under observation. The existing evidence-mode `account.devices` snapshots remain the history of all signed-in devices; connection diagnostics retain only the current device description.

Before connection, advisory checks compare the API platform, language pack, device/OS and app-version formats, mobile system locale, and Telethon's actual schema layer against the reviewed catalog baseline. Warnings appear in the server log and account status metadata; they never replace imported values or change the schema layer. A different layer is a compatibility review signal, not proof of a broken or restricted account. These checks and `official_app` do not certify that Telegram considers the account safe from restrictions. Disconnected account status uses the saved profile instead of generating another device description.

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

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Fail diubah **dalam memori** pada pelayan TgWitness anda. Muatan tidak disimpan, fail ZIP tidak diekstrak ke cakera dan tiada perkhidmatan luaran dihubungi.
- Sesi yang terhasil kemudian disemak dengan Telegram. Jika fail menyatakan ID pengguna, ia mesti sepadan dengan akaun yang dilaporkan oleh Telegram.
- Fail yang menerangkan akaun berbeza atau kelayakan API berbeza ditolak daripada memilih satu.
- **Kod laluan atau teks sesi** menempatkan medan kod laluan tempatan TData, satu kotak untuk menampal StringSession dan **fail Baca tanpa mendaftar masuk** (mengisi borang tanpa berhubung dengan Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

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
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData ialah folder `tdata` aplikasi Telegram Desktop (aplikasi rentas platform dari desktop.telegram.org).

| Sistem | Lokasi lalai `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram mudah alih: seterusnya `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Untuk mengimportnya:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
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
| `string_session` (`session_string`, `session_str`; legacy `session`) | Telethon StringSession teks, bukan nama fail |
| `auth_key` (`auth_key_hex`) + `dc_id` | Lengkapkan Kunci Auth 512-karakter dan DC 1–5 |
| `user_id` (`id`) | Pilihan; disemak menentang Telegram sebelum kebenaran disimpan |
| `device_model` (`device`) | Connection device description |
| `system_version` (`sdk`) | Connection OS version |
| `app_version` | Application version sent to Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client language, system language and client language pack; an empty `lang_pack` is allowed |
| `tz_offset` | Optional UTC offset in seconds, sent in `initConnection.params`; integer or decimal integer string |

If both an alias and the main name are present, they must agree. Explicit Telethon session fields take priority over a generic `session` blob in another format. If both contain recognizable Telethon sessions, they must describe the same authorization. Without an explicit field, `session` must be a valid Telethon StringSession. Examples:

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
