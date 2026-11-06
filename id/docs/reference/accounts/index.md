# Format akun dan sesi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/

Masuk menggunakan nomor telepon, kode QR, atau kunci otentikasi, impor sesi Telethon, Pyrogram, atau Telegram Desktop, dan kelola beberapa akun.

TgWitness masuk sebagai **akun pengguna Telegram** (bukan bot) melalui MTProto, menggunakan Telethon. Setiap akun berada di **ruang** kerja tersendiri (disebut *workspace* dalam API dan alat baris perintah) dengan sesi, sumber, jurnal, dan kunci penandatanganan tersendiri.

Berkas sesi, string sesi, dan Kunci Otentikasi merupakan **otorisasi akun**: siapa pun yang memilikinya dapat bertindak sebagai akun tersebut. Ketiganya tidak berisi riwayat pesan.

> [!PERINGATAN] **Jangan gunakan apa pun yang tidak boleh hilang.** Kami sangat menyarankan agar Anda tidak menghubungkan akun pribadi atau akun berharga lainnya, serta tidak membuat ID API / hash API pada akun yang Anda hargai. Ini bukan soal TgWitness belum teruji: Telegram membatasi dan memblokir akun secara permanen tanpa peringatan — untuk volume permintaan yang dianggapnya berlebihan, terlepas dari klien atau tujuannya, tanpa dokumentasi yang memadai. Banyak pemblokiran tidak dapat dibatalkan. Gunakan akun khusus. Kelancaran uji coba bergantung pada Telegram, bukan pada perangkat lunak, dan tidak menjamin apa pun untuk masa mendatang.

- [Sekilas](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#at-a-glance)
- [Sebelum memulai: ID API dan hash API](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Nomor telepon](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#phone-number) · [Kode QR](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#qr-code) · [Kunci Otentikasi + ID DC](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#auth-key--dc-id)
- [Berkas akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#pyrogram-session) · [Pasangan sesi + JSON](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#telethon-stringsession) · [JSON Akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-json)
- [Identifikasi apa yang Anda miliki](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#identify-what-you-have) · [Format yang tidak didukung](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#unsupported-formats)
- [Beberapa akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#multiple-accounts) · [Menjaga keamanan berkas akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#keeping-account-files-safe) · [Pemecahan Masalah](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#troubleshooting)

## Sekilas

| Apa yang Anda miliki | Tab di **Tambahkan akun** | Anda juga akan memerlukan |
| --- | --- | --- |
| Nomor telepon dan akses ke kode login-nya | **Telepon** | Kata sandi 2FA jika diaktifkan |
| Telegram terbuka di perangkat lain | **Kode QR** | Kata sandi 2FA jika diaktifkan |
| Berkas `.session` (Telethon atau Pyrogram) | **Berkas** | Berkas JSON pelengkap opsional untuk pengaturan aplikasi |
| `.session` + `.json` dengan nama yang sama | **Berkas** (pilih keduanya) | Biasanya tidak ada yang lain |
| Folder `tdata` di Telegram Desktop | **Berkas** (dalam format ZIP) | Kode sandi lokal Desktop, jika ada yang ditetapkan |
| Sebuah Telethon StringSession (teks, `.txt`, `.tgwitness-session`) | **Berkas** | Tidak diperlukan pasangan API terpisah |
| `.json` dengan sesi atau Kunci Otentikasi | **Berkas** | Tidak diperlukan pasangan API terpisah |
| Kunci Otentikasi (512 karakter heksadesimal) dan nomor DC-nya | **Kunci otentikasi** | ID Pengguna (opsional) |

TgWitness mengenali berkas berdasarkan **isinya**, bukan namanya. Mengganti nama berkas tidak akan mengubah isinya.

## Sebelum memulai: ID API dan hash API

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

Untuk menggunakan aplikasi Anda sendiri sebagai gantinya (akun yang mendaftarkannya adalah yang berisiko; lihat [Mengapa menggunakan kumpulan API bawaan?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. Buka [my.telegram.org](https://my.telegram.org) dan masuk menggunakan nomor telepon apa pun yang Anda miliki. Kode verifikasi akan dikirimkan melalui aplikasi Telegram, bukan melalui SMS.
2. Pilih **alat pengembangan API**.
3. Buat aplikasi: judul dan nama pendek apa saja (5–32 huruf), platform **Desktop**. URL dan deskripsi dapat dikosongkan.
4. Salin **App api_id** (sebuah angka) dan **App api_hash** (32 karakter heksadesimal).

Di panel, buka bagian **API ID + Hash** di bawah formulir masuk. Anda dapat menempelkan satu pasangan `api_id:api_hash` ke kolom **API ID**, dan kedua kolom tersebut akan terisi otomatis. Satu pasangan dapat digunakan untuk semua akun Anda. Setelah login berhasil, data tersebut disimpan dalam bentuk terenkripsi, hanya di ruang kerja tersebut, dan tidak pernah dikirim kembali ke browser.

Terdapat tiga jenis kredensial yang terlibat:

| Rahasia | Buka | Lokasi |
| --- | --- | --- |
| Token panel | Panel web TgWitness | `panel-token.txt` di direktori data, atau `TGWITNESS_TOKEN` |
| ID API + hash | Tidak ada yang berdiri sendiri; mengidentifikasi aplikasi tersebut | Pasangan bawaan, pengaturan yang diimpor, atau aplikasi Anda sendiri di my.telegram.org |
| Otorisasi akun | Akun Telegram | Dibuat melalui login via telepon/QR atau dimasukkan sebagai sesi |

Jika Telegram harus diakses melalui proxy, atur terlebih dahulu di **Akun → Pengaturan → Pengaturan koneksi → Ubah rute koneksi**.

## Nomor telepon

1. Buka **Akun**, pilih tab **Telepon**, lalu masukkan nomor dalam format internasional, misalnya `+44 7700 900123`. Spasi dan tanda hubung akan dihapus secara otomatis.
2. Tekan **Lanjutkan**. Kolom API ID + Hash dapat dibiarkan kosong.
3. Masukkan kode yang dikirimkan oleh Telegram (biasanya ke aplikasi Telegram; pengiriman melalui SMS tidak dijamin).
4. Jika akun tersebut memiliki verifikasi dua langkah, masukkan kata sandi tersebut. Ini bukanlah token panel maupun kode sandi perangkat.
5. Periksa ID akun yang ditampilkan setelah masuk, lalu pilih sumber.

Kode login dan kata sandi 2FA tidak pernah disimpan ke disk.

## Kode QR

Gunakan ini jika akun sudah masuk (login) di ponsel atau komputer lain.

1. Tab **Kode QR** → **Tampilkan kode QR**. Kolom API ID + Hash dapat dibiarkan kosong.
2. Pada perangkat yang sudah masuk: **Pengaturan → Perangkat → Hubungkan Perangkat Desktop**, pindai kode dan konfirmasi.
3. Masukkan kata sandi 2FA di TgWitness jika Telegram memintanya.

Gambar QR dihasilkan secara lokal. Kode memiliki masa berlaku; tekan "**Buat kode QR lain"** untuk mencoba lagi. Mengunci panel, berpindah ruang kerja, atau memulai sesi login baru akan membatalkan kode yang sedang diproses.

## Kunci Otentikasi + ID DC

Kunci Otorisasi (Auth Key) adalah otorisasi mentah berukuran 256 byte yang mendasari setiap sesi Telegram, ditulis dalam bentuk **512 karakter heksadesimal**, bersama dengan nomor pusat data **DC 1–5**.

1. Tab **Kunci Otentikasi**. Tempelkan kunci secara lengkap; kunci yang dipersingkat yang mengandung `…` tidak akan berfungsi.
2. Pilih DC ID yang disertakan bersama kunci tersebut.
3. Masukkan **ID Pengguna** (opsional). TgWitness kemudian akan menolak terhubung jika Telegram melaporkan akun yang berbeda.
4. **Akun** Press **Connect**.

Kunci Otentikasi (512 karakter) bukanlah hash API (32 karakter). Kunci yang sama juga dapat diimpor sebagai JSON, lihat [JSON Akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-json).

## Berkas akun

Buka **Tambahkan akun → File** dan pilih hingga **empat file yang terkait dengan satu akun**, dengan total ukuran **8 MiB**, lalu tekan **Hubungkan akun**.

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- File dikonversi **di memori** pada server TgWitness Anda. Unggahan tidak disimpan, file ZIP tidak diekstrak ke disk, dan tidak ada layanan eksternal yang dihubungi.
- Sesi yang dihasilkan kemudian diverifikasi dengan Telegram. Jika sebuah berkas mencantumkan ID pengguna, ID tersebut harus sesuai dengan akun yang dilaporkan oleh Telegram.
- Berkas yang mendeskripsikan akun yang berbeda atau kredensial API yang berbeda akan ditolak daripada memilih salah satunya.
- **Kolom "Passcode" atau "session text"** berisi bidang "TData local passcode", sebuah kotak untuk menempelkan StringSession dan **membaca berkas tanpa perlu masuk** (mengisi formulir tanpa menghubungi Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Telethon `.session`

|  |  |
| --- | --- |
| Apa itu | Basis data SQLite yang dibuat oleh alat berbasis Telethon, misalnya `my_account.session` |
| Diakui oleh | Tabel `sessions` (bersama dengan `dc_id`, `server_address`, `port`, `auth_key`) dan `version` = 7 atau 8 |
| Persyaratan | Tepat satu baris sesi yang diotorisasi; basis data yang tertutup dan lengkap |

Tutup terlebih dahulu program yang membuat berkas tersebut. Jika terdapat `my_account.session-journal` atau `my_account.session-wal` di sampingnya, berarti basis data belum diselesaikan: buka dan tutup klien aslinya dengan benar. Menghapus berkas-berkas sidecar tersebut dapat meninggalkan salinan yang rusak.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Apa itu | Alat berbasis Pyrogram yang menggunakan basis data SQLite |
| Diakui oleh | Tabel `sessions` dengan `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 atau 3 |
| Persyaratan | Satu sesi **pengguna** yang berwenang di jaringan produksi. Sesi bot dan test-DC ditolak |

ID pengguna yang disimpan akan diverifikasi dengan Telegram saat login.

### Pasangan sesi + JSON

Akun sering kali didistribusikan dalam bentuk dua berkas dengan nama yang sama, misalnya `447700900123.session` dan `447700900123.json`. Pilih **keduanya** sekaligus.

- Dari JSON, TgWitness menggunakan `app_id`/`api_id` dan `app_hash`/`api_hash`, sehingga Anda biasanya tidak perlu memasukkan kredensial API.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData adalah folder `tdata` dari aplikasi Telegram Desktop (aplikasi lintas platform dari desktop.telegram.org).

| Sistem | Lokasi default `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portabel: di sebelah `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Untuk mengimpornya:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> Hal ini juga berlaku untuk berkas yang diimpor `.session` , teks StringSession, dan Auth Key HEX. Klien lain dengan otorisasi yang dibuat secara mandiri dapat tetap masuk. Lihat [dokumentasi AUTH_KEY_DUPLICATED dari Telegram](https://core.telegram.org/api/errors#406-not-acceptable).

1. Keluar sepenuhnya dari Telegram Desktop.
2. Buatlah berkas ZIP yang **hanya** berisi dua item berikut dari `tdata`:

   - `key_datas`
   - file berhuruf 16 yang berakhiran `s` di sebelahnya, biasanya `D877F783D5D3EF8Cs`

   Mengompres seluruh folder beserta cache medianya biasanya melebihi batas (512 entri, 32 MiB setelah diekstrak). 3. Pilih berkas ZIP di bagian "**Files**". Jika Telegram Desktop memiliki **kode sandi lokal**, masukkan kode tersebut di kolom **"Passcode" atau "session text"** terlebih dahulu. Ini bukanlah kata sandi 2FA.

Didukung: satu akun per arsip, penyimpanan modern `key_datas`/`key_data0`/`key_data1`, kode sandi lokal. Tidak didukung: folder dengan beberapa akun yang masuk, tata letak Desktop versi lama, file ZIP yang dilindungi kata sandi, dan aplikasi asli macOS terpisah "Telegram for macOS".

### Telethon StringSession

Satu baris teks, biasanya dimulai dengan `1` dan panjangnya sekitar 350 karakter. Unggah berkas tersebut sebagai berkas `.txt` atau `.tgwitness-session` (maksimal 4 KiB), atau tempelkan di bawah **kolom Kode Akses atau teks sesi**. Hanya string Telethon yang diterima; string Pyrogram dan TDLib menggunakan format yang berbeda.

### JSON Akun

Satu objek JSON, maksimal **64 KiB**, dalam berkas dengan ekstensi **`.json`**.

| Bidang (alias) | Arti |
| --- | --- |
| `api_id` (`app_id`) | ID Aplikasi, sebuah bilangan positif |
| `api_hash` (`app_hash`) | Hash aplikasi, 32 karakter heksadesimal |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Teks Telethon StringSession, bukan nama file |
| `auth_key` (`auth_key_hex`) + `dc_id` | Kunci Otentikasi (Auth Key) lengkap berpanjang 512 karakter dan DC 1–5 |
| `user_id` (`id`) | Opsional; diverifikasi dengan Telegram sebelum otorisasi disimpan |
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

Contoh pertama hanya mengisi kredensial API; masuk dengan nomor telepon atau QR, atau tambahkan berkas sesi. Daftar massal (array JSON akun) tidak diterima.

## Identifikasi apa yang Anda miliki

| Anda melihat | Ini adalah | Penggunaan |
| --- | --- | --- |
| `*.session`; saat dibuka di editor teks, bagian atasnya menampilkan `SQLite format 3` | Telethon atau Pyrogram SQLite | **Berkas** (terdeteksi secara otomatis) |
| Folder `tdata` yang berisi `key_datas` | Telegram Desktop TData | Kompres dua berkas menjadi ZIP, lalu **Berkas** |
| Satu baris teks yang dimulai dengan `1`, ~350 karakter | Telethon StringSession | **Berkas** |
| `*.json` dengan `app_id`/`app_hash` | Metadata pendamping | **Berkas**, beserta sesi-nya |
| `*.json` dengan `auth_key` atau `string_session` | JSON Akun | **Berkas** |
| 512 karakter `0-9a-f` | Kunci Otentikasi | **Kunci otentikasi** |
| 32 karakter `0-9a-f` | Hash API | **ID API + Hash** |
| `td.binlog` atau `db.sqlite` dari aplikasi TDLib | Penyimpanan TDLib | Tidak didukung |
| `123456789:AA…` | Token bot | Tidak didukung |

## Format yang tidak didukung

| Format | Alternatif |
| --- | --- |
| Penyimpanan TDLib (`td.binlog`) dan ekspor TDLib | Masuk menggunakan nomor telepon atau QR |
| **String** sesi Pyrogram | Gunakan berkas Pyrogram `.session`, atau ponsel/QR |
| TData dengan beberapa akun yang telah masuk | Keluar dari akun-akun lain di Telegram Desktop, atau gunakan berkas sesi masing-masing akun |
| Token bot | Tidak didukung: TgWitness beroperasi sebagai akun pengguna |
| Daftar CSV/JSON dari banyak akun | Impor file sesi yang didukung melalui **Akun → Impor akun**, atau masuk melalui telepon/QR di ruang kerja terpisah |
| Sesi Test-DC atau bot | Gunakan akun pengguna produksi |

## Beberapa akun

Tekan **+** di samping pemilih akun, atau buka **Akun → Pengaturan → Pengaturan koneksi → Ruang kerja**, masukkan label, dan masuk.

- Jumlah ruang kerja tidak terbatas, termasuk ruang kerja utama. Masing-masing memiliki sesi, rute proxy , sumber, kebijakan penangkapan, jurnal, kunci penandatanganan, titik pemeriksaan, dan ekspor tersendiri.
- Mengganti ruang kerja yang ditampilkan tidak akan menghentikan ruang kerja lainnya.
- Sebuah jurnal tetap terikat pada akun yang membuatnya. Masuk dengan akun yang berbeda memerlukan ruang kerja lain, dan satu akun tidak dapat ditugaskan ke dua ruang kerja.
- Token panel utama mengontrol semua ruang kerja. [Akses yang diberikan](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/) dapat membatasi orang lain hanya pada akun dan obrolan tertentu, dengan izin dan batas sesi yang terpisah.
- **Akun** mengganti nama ruang kerja dan menghapus ruang kerja yang ditambahkan, beserta sesi, jurnal, sumber, dan kunci penandatanganan. Ruang kerja utama tidak dapat dihapus dari panel.

### Impor massal dan grup akun

Gunakan **Akun → Impor akun** untuk menambahkan beberapa akun, pasangkan berkas berdasarkan nama dasar dan lihat hasil login masing-masing. Setiap akun memiliki ruang kerja tersendiri.

Sebuah grup menyatukan akun-akun yang terkait tanpa menggabungkan sesi, kunci, atau bukti mereka. **Buka grup** di **bagian Akun** untuk menuju ke halamannya di `/groups/<id>`:

- **Akun:** rute koneksi, pengamatan, dan pesan terakhir setiap anggota, dengan **Mulai Semua** dan **Jeda Semua**.
- **Perlu perhatian:** akun yang telah keluar, tidak tersedia, atau mengalami masalah koneksi, input, sumber, atau media; setiap nama mengarah ke kartunya masing-masing.
- **Obrolan di beberapa akun menampilkan:** sumber yang dibagikan, akun-akun yang mengamati obrolan tersebut, dan gangguan dalam periode pengamatan ruang kerja yang tersedia (hingga tujuh hari). **Ekspor dengan N akun** membagi ekspor saluran atau supergrup di antara akun-akun tersebut dan menandatangani satu arsip.
- **Ekspor grup:** satu ZIP dengan ekspor yang telah ditandatangani dari setiap akun di bawah `accounts/` dan `manifest.json` mencantumkan SHA-256 dan sidik jari kunci masing-masing, yang ditandatangani oleh ruang kerja utama di `manifest.signature.json`. Verifikasi setiap arsip akun secara terpisah dengan `python -m tgwitness.verify` dan sidik jari tepercaya akun tersebut.

Anggota berbagi pengaturan grup; sebuah akun dapat mempertahankan nilai-nilainya sendiri. Lihat [pengaturan bersama](https://phishdestroy.github.io/TgWitness/id/docs/reference/settings/#account-groups), [panduan impor dan grup](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) dan [dasbor kolam MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Keluar

**Akun → Keluar dari Telegram** (dengan pemantauan ditangguhkan) meminta Telegram untuk mengakhiri sesi, sehingga sesi tersebut juga menghilang dari **Pengaturan → Perangkat** akun, dan menghapus sesi tersebut dari brankas ruang kerja. Jurnal, sumber, pengaturan, dan kunci penandatanganan tetap ada, dan jurnal mencatat proses keluar tersebut. Ruang kerja tersebut masih milik akunnya: hanya akun tersebut yang dapat terhubung kembali ke sana. Jika Telegram tidak merespons, sesi tersebut tetap dihapus di sini dan panel akan menampilkannya; akhiri sesi tersebut di Telegram melalui **Pengaturan → Perangkat**.

## Menjaga keamanan berkas akun

- Perlakukan setiap `.session`, TData ZIP, StringSession, Auth Key, dan JSON akun seperti kata sandi. TgWitness menyimpan otorisasi yang diimpor di dalam brankas terenkripsinya; Anda dapat menghapus file aslinya setelahnya.
- Jangan menjalankan otorisasi yang sama di dua program sekaligus. Telegram dapat mencabutnya (`AUTH_KEY_DUPLICATED`), dan kedua salinan tersebut akan berhenti berfungsi.
- Sesi yang telah kedaluwarsa atau dicabut tidak dapat diaktifkan kembali melalui konversi. Silakan masuk kembali.

## Pemecahan Masalah

| Pesan atau gejala | Apa yang harus dilakukan |
| --- | --- |
| *Tidak dapat membaca sesi ini. Tutup klien aslinya…* | Berkas SQLite sedang terbuka atau belum selesai (sidecar `-journal`/`-wal`). Tutup program aslinya dengan benar, lalu salin kembali berkas tersebut. |
| *Skema SQLite Telethon yang didukung: 7 dan 8* / *Pyrogram … 2 dan 3* | File ini dibuat menggunakan versi pustaka yang sangat lama atau tidak dikenal. Silakan masuk menggunakan nomor telepon/QR. |
| *Hanya sesi pengguna produksi yang berwenang yang didukung* | Berkas Pyrogram tersebut milik bot atau jaringan uji coba. |
| *Arsip TData melebihi 512 entri atau 32 MiB* | Hanya berkas ZIP `key_datas` dan `D877F783D5D3EF8Cs`, bukan seluruh folder. |
| *Tidak dapat mendekripsi TData. Periksa kode sandi lokal Desktop* | Masukkan kode sandi lokal Telegram Desktop di kolom "**Passcode**" **atau "session text**". |
| *Impor satu akun TData pada satu waktu* | Telegram Desktop memiliki beberapa akun; lihat [Format yang Tidak Didukung](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#unsupported-formats). |
| *Berkas-berkas yang dipilih menjelaskan akun-akun yang berbeda atau kredensial API* | Pilih file dari satu akun saja. |
| *JSON tidak berisi kredensial API atau otorisasi yang didukung* | Periksa nama-nama bidang dalam [JSON Akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/#account-json). |
| *Hanya metadata API* | JSON ini tidak memiliki sesi. Tambahkan berkas `.session` atau gunakan nomor telepon/kode QR. |
| *Kunci Otorisasi HEX harus berisi seluruh 512 karakter heksadesimal* | Kunci tersebut terpotong atau mengandung `…`. |
| ID akun tidak sesuai dengan akun yang diimpor | ID pengguna pada berkas tersebut berbeda dengan yang dilaporkan oleh Telegram; berkas tersebut diperuntukkan bagi akun lain. |
| Akun ini sudah terdaftar di ruang kerja lain | Buka ruang kerja tersebut daripada menambahkan akun dua kali. |
| Tersambung, tetapi ada grup pribadi yang hilang dari daftar obrolan di **Sumber** | Periksa keanggotaan. Alat pemilih memeriksa 1.000 percakapan pertama; tingkatkan batasnya di bagian **Parameter**. |
| Koneksi proxy gagal | Periksa rute dan mode IP. Secara otomatis, MTProxy akan mencoba entri lain yang berfungsi. Sembunyikan penundaan alamat; Direct sebagai pilihan terakhir dapat terhubung langsung setelah penundaan yang telah dikonfigurasi. Lihat [mode perutean](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes). |

Lihat juga: [koneksi dan keamanan](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) untuk proxy dan enkripsi, serta [cara kerja pengumpulan](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/) data yang direkam setelah masuk.
