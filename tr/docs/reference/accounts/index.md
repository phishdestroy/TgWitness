# Hesaplar ve oturum biçimleri

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/

Telefon, QR kodu veya kimlik anahtarıyla oturum açın, Telethon, Pyrogram veya Telegram Desktop oturumlarını içe aktarın ve birden fazla hesabı yönetin.

TgWitness, Telethon kullanarak MTProto üzerinden bir **Telegram kullanıcı hesabı** (bot değil) olarak oturum açar. Her hesap, kendi oturumu, kaynakları, günlüğü ve imzalama anahtarı ile birlikte kendi **çalışma** alanında (API ve komut satırı araçlarında "*çalışma alanı*" olarak adlandırılır) bulunur.

Oturum dosyaları, oturum dizeleri ve Oturum Açma Anahtarları **hesap yetkilendirmeleridir**: bunlardan birine sahip olan kişi, o hesap adına hareket edebilir. Bunlar mesaj geçmişini içermez.

> [!UYARI] **Kaybetmeyi göze alamayacağınız hiçbir şeyi kullanmayın.** Kişisel veya başka şekilde değerli hesapları bağlamamanızı ve değer verdiğiniz bir hesap üzerinde API kimliği / API hash'i oluşturmamanızı şiddetle tavsiye ederiz. Bu, TgWitness’in test edilmemiş olmasıyla ilgili değildir: Telegram, hesapları öngörülemez bir şekilde kısıtlar ve kalıcı olarak yasaklar — istem hacminin, istemci veya amaç ne olursa olsun, aşırı olduğunu düşündüğü durumlarda, yeterli bir dokümantasyon olmaksızın. Birçok yasaklama geri alınamaz. Yalnızca bu amaç için ayrılmış hesaplar kullanın. Testlerin sorunsuz geçmesi, yazılıma değil Telegram’a bağlıdır ve ileride herhangi bir garanti vermez.

- [Bir bakışta](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#at-a-glance)
- [Başlamadan önce: API kimliği ve API hash değeri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Telefon numarası](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#phone-number) · [QR kodu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#qr-code) · [Oturum Açma Anahtarı + DC Kimliği](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#auth-key--dc-id)
- [Hesap dosyaları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#pyrogram-session) · [Oturum + JSON çifti](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#telethon-stringsession) · [Hesap JSON'u](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#account-json)
- [Elinizde ne olduğunu belirleyin](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#identify-what-you-have) · [Desteklenmeyen formatlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#unsupported-formats)
- [Birden fazla hesap](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#multiple-accounts) · [Hesap dosyalarını güvende tutma](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#keeping-account-files-safe) · [Sorun Giderme](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#troubleshooting)

## Bir bakışta

| Elinizde olanlar | **Hesap Ekle** sekmesi | Ayrıca şunlara da ihtiyacınız olacak: |
| --- | --- | --- |
| Telefon numarası ve giriş kodlarına erişim | **Telefon** | Etkinleştirilmişse 2FA şifresi |
| Telegram başka bir cihazda açık | **QR kodu** | Etkinleştirilmişse 2FA şifresi |
| Bir `.session` dosyası (Telethon veya Pyrogram) | **Dosyalar** | Uygulama ayarları için isteğe bağlı eşlik eden JSON dosyası |
| `.session` + `.json` (aynı isimde) | **Dosyalar** (her ikisini de seçin) | Genellikle başka bir şey yoktur |
| Telegram Desktop'taki `tdata` klasörü | **Dosyalar** (ZIP olarak) | Varsa, masaüstü için ayarlanmış yerel şifre |
| Bir Telethon StringSession (metin, `.txt`, `.tgwitness-session`) | **Dosyalar** | Ayrı bir API çifti gerekmez |
| Bir oturum veya Oturum Açma Anahtarı (Auth Key) içeren bir `.json` | **Dosyalar** | Ayrı bir API çifti gerekmez |
| Bir Oturum Açma Anahtarı (512 onaltılık karakter) ve buna ait DC numarası | **Oturum açma anahtarı** | İsteğe bağlı Kullanıcı Kimliği |

TgWitness, dosyaları adlarına göre değil, **içerik**lerine göre tanır. Bir dosyanın adının değiştirilmesi asla dosyanın dönüştürülmesine yol açmaz.

## Başlamadan önce: API kimliği ve API hash değeri

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

Bunun yerine kendi uygulamanızı kullanmak isterseniz (uygulamayı kaydeden hesap risk altındadır; bkz. [Neden yerleşik bir API havuzu?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. [my.telegram.org adresini](https://my.telegram.org) açın ve sahip olduğunuz herhangi bir telefon numarasıyla giriş yapın. Kod, SMS yoluyla değil, Telegram uygulamasına gelir.
2. **API geliştirme araçlarını** seçin.
3. Bir uygulama oluşturun: herhangi bir başlık ve kısa ad (5–32 harf), platform: **Masaüstü**. URL ve açıklama alanları boş bırakılabilir.
4. **App api_id** (bir sayı) ve **App api_hash** (32 onaltılık karakter) değerlerini kopyalayın.

Panelde, oturum açma formunun altında açık **API Kimliği + Hash** bulunur. **API Kimliği** alanına tek bir `api_id:api_hash` çifti yapıştırdığınızda her iki alan da doldurulur. Tek bir çift, tüm hesaplarınız için kullanılabilir. Başarılı bir oturum açma işleminden sonra bu bilgi, şifrelenmiş olarak yalnızca o çalışma alanında saklanır ve asla tarayıcıya geri gönderilmez.

Burada üç farklı kimlik bilgisi söz konusudur:

| Gizli | Açılır | Bulunduğu yer |
| --- | --- | --- |
| Panel jetonu | TgWitness web paneli | Veri dizinindeki `panel-token.txt` veya `TGWITNESS_TOKEN` |
| API Kimliği + hash | Tek başına bir anlam ifade etmez; uygulamayı tanımlar | Yerleşik çift, içe aktarılan ayarlar veya my.telegram.org adresindeki kendi uygulamanız |
| Hesap yetkilendirme | Telegram hesabı | Telefon/QR koduyla oturum açma yoluyla oluşturulur veya oturum olarak eklenir |

Telegram'a bir proxy üzerinden erişilmesi gerekiyorsa, önce **Hesap → Ayarlar → Bağlantı ayarları → Bağlantı yolunu değiştir** seçeneğinden ayarlayın.

## Telefon numarası

1. **Hesap** Aç seçeneğine tıklayın, **Telefon** sekmesine gidin ve numarayı uluslararası formatta girin, örneğin `+44 7700 900123`. Boşluklar ve tireler otomatik olarak kaldırılır.
2. **"Devam"** düğmesine basın. API Kimliği + Hash alanları boş bırakılabilir.
3. Telegram'ın gönderdiği kodu girin (genellikle Telegram uygulamasına gönderilir; SMS ile gönderilmesi garanti edilmez).
4. Hesapta iki aşamalı doğrulama varsa, o şifreyi girin. Bu, panel jetonu veya cihaz şifresi değildir.
5. Giriş yaptıktan sonra gösterilen hesap kimliğini kontrol edin, ardından kaynakları seçin.

Giriş kodları ve 2FA şifresi hiçbir zaman diske kaydedilmez.

## QR kodu

Hesap bir telefonda veya başka bir bilgisayarda zaten oturum açmışsa bunu kullanın.

1. **QR kodu** sekmesi → **QR kodunu göster**. API Kimliği + Hash alanları boş bırakılabilir.
2. Oturum açılmış cihazda: **Ayarlar → Cihazlar → Masaüstü Cihazını Bağla seçeneğine gidin**, kodu tarayın ve onaylayın.
3. Telegram talep ederse, TgWitness'e 2FA şifresini girin.

QR kodu görüntüsü yerel olarak oluşturulur. Kodların geçerlilik süresi dolabilir; yeniden denemek için "**Başka bir QR kodu oluştur"** düğmesine basın. Paneli kilitlemek, çalışma alanını değiştirmek veya başka bir oturum açma işlemi başlatmak, beklemede olan kodu iptal eder.

## Oturum Açma Anahtarı + DC Kimliği

Bir Oturum Açma Anahtarı (Auth Key), her Telegram oturumunun arkasında yatan 256 baytlık ham yetkilendirme verisidir ve **512 onaltılık karakter**den oluşur; buna veri merkezi numarası **DC 1–5** de eklenir.

1. **"Auth**" **sekmesi**. Anahtarın tamamını yapıştırın; `…` içeren kısaltılmış bir anahtar çalışmaz.
2. Anahtarla birlikte sağlanan DC kimliğini seçin.
3. İsteğe bağlı olarak **Kullanıcı Kim**liğini girin. Telegram farklı bir hesap bildirdiğinde TgWitness bağlantı kurmayı reddeder.
4. Press **Connect hesabı**.

Bir Oturum Açma Anahtarı (512 karakter), bir API hash'i (32 karakter) değildir. Aynı anahtar ayrıca JSON olarak da içe aktarılabilir; bkz. [Hesap JSON'u](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#account-json).

## Hesap dosyaları

**"Hesap Ekle" → "Dosyalar"** seçeneğini açın ve **bir hesaba ait**, toplamda **8 MiB**'ye kadar **dört dosyayı** seçin, ardından "**Hesabı Bağla"** düğmesine basın.

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Dosyalar, TgWitness sunucunuzun **belleğinde** dönüştürülür. Yüklenen dosyalar depolanmaz, ZIP dosyaları diske açılmaz ve hiçbir harici hizmetle bağlantı kurulmaz.
- Elde edilen oturum daha sonra Telegram ile karşılaştırılır. Bir dosyada bir kullanıcı kimliği belirtiliyorsa, bu kimlik, Telegram'ın bildirdiği hesapla eşleşmelidir.
- Farklı hesapları veya farklı API kimlik bilgilerini açıklayan dosyalar reddedilir; tek bir tanesini seçmek yerine.
- **Şifre veya oturum metni**, TData yerel şifre alanını içerir; bu alan, **oturum açmadan** StringSession ve **Read**dosyalarını yapıştırmak için bir kutudur (Telegram ile iletişime geçmeden formu doldurur).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Telethon `.session`

|  |  |
| --- | --- |
| Nedir? | Telethon tabanlı araçların oluşturduğu SQLite veritabanı; örneğin `my_account.session` |
| Tarafından tanınan | `sessions` tabloları (`dc_id`, `server_address`, `port`, `auth_key` ile birlikte) ve `version` = 7 veya 8 |
| Gereksinimler | Tam olarak bir adet yetkili oturum satırı; kapalı, eksiksiz bir veritabanı |

Öncelikle dosyayı oluşturan programı kapatın. Yanında `my_account.session-journal` veya `my_account.session-wal` dosyası varsa, veritabanı henüz tamamlanmamıştır: orijinal istemciyi açın ve düzgün bir şekilde kapatın. Bu yan dosyaları silmek, bozuk bir kopya bırakabilir.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Nedir? | Pyrogram tabanlı araçların oluşturduğu SQLite veritabanı |
| Tarafından tanınan | `sessions` tablosu; `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 veya 3 |
| Gereksinimler | Üretim ağında tek bir yetkili **kullanıcı** oturumu. Bot ve test-DC oturumları reddedilir. |

Oturum açma sırasında saklanan kullanıcı kimliği, Telegram ile karşılaştırılarak doğrulanır.

### Oturum + JSON çifti

Hesaplar genellikle aynı ada sahip iki dosya olarak dağıtılır; örneğin, `447700900123.session` ve `447700900123.json`. **Her ikisini de** aynı anda seçin.

- JSON'dan TgWitness, `app_id`/`api_id` ve `app_hash`/`api_hash` kullanır, bu nedenle genellikle API kimlik bilgilerini girmeniz gerekmez.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#account-json).

### Telegram Masaüstü (TData)

TData, Telegram Desktop uygulamasının (desktop.telegram.org adresinden indirilebilen platformlar arası uygulama) `tdata` klasörüdür.

| Sistem | Varsayılan `tdata` konumu |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (taşınabilir Telegram: `Telegram.exe`'nin yanında) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

İçe aktarmak için:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> Bu, içe aktarılan `.session` dosyalar, StringSession metni ve Auth Key HEX için de geçerlidir. Kendi bağımsız yetkilendirmelerine sahip diğer istemciler oturumda kalmaya devam edebilir. [Telegram’ın AUTH_KEY_DUPLICATED belgelerine](https://core.telegram.org/api/errors#406-not-acceptable) bakın.

1. Telegram Desktop'tan tamamen çıkın.
2. `tdata`'den **yalnızca** bu iki öğeyi içeren bir ZIP dosyası oluşturun:

   - `key_datas`
   - Yanında `s` ile biten 16 karakterlik dosya, genellikle `D877F783D5D3EF8Cs`

   Medya önbelleği ile birlikte tüm klasörü ZIP dosyasına sıkıştırmak genellikle sınırları aşar (512 giriş, sıkıştırılmamış haliyle 32 MiB). 3. **Dosyalar** bölümünden ZIP dosyasını seçin. Telegram Desktop'ta **yerel** bir **şifre** varsa, bunu önce **Şifre veya oturum metni** alanına girin. Bu, 2FA şifresi değildir.

Desteklenenler: arşiv başına tek hesap, modern `key_datas`/`key_data0`/`key_data1` depolama, yerel şifre. Desteklenmeyenler: birden fazla oturum açılmış hesabın bulunduğu klasörler, eski Masaüstü düzenleri, şifre korumalı ZIP dosyaları ve ayrı bir yerel macOS uygulaması olan "Telegram for macOS".

### Telethon StringSession

Genellikle `1` ile başlayan ve yaklaşık 350 karakter uzunluğunda tek satırlık bir metin. Bunu `.txt` veya `.tgwitness-session` dosyası olarak yükleyin (en fazla 4 KiB) ya da **Şifre veya oturum metni** alanına yapıştırın. Yalnızca Telethon dizeleri kabul edilir; Pyrogram ve TDLib dizeleri farklı biçimler kullanır.

### Hesap JSON'u

**`.json`** ile biten bir dosyada, en fazla **64 KiB** boyutunda tek bir JSON nesnesi.

| Alan (takma adlar) | Anlam |
| --- | --- |
| `api_id` (`app_id`) | Uygulama Kimliği, pozitif bir sayı |
| `api_hash` (`app_hash`) | Uygulama hash değeri, 32 onaltılık karakter |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Telethon StringSession metni, dosya adı değil |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512 karakterlik tam Otorizasyon Anahtarı ve DC 1–5 |
| `user_id` (`id`) | İsteğe bağlı; yetkilendirme kaydedilmeden önce Telegram ile karşılaştırılarak kontrol edilir |
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

İlk örnekte yalnızca API kimlik bilgileri girilir; telefon veya QR koduyla oturum açın ya da bir oturum dosyası ekleyin. Toplu listeler (hesapların bulunduğu bir JSON dizisi) kabul edilmez.

## Elinizde ne olduğunu belirleyin

| Görüyorsunuz | Bu, | Kullanım |
| --- | --- | --- |
| `*.session`; bir metin düzenleyicide açıldığında en üstte `SQLite format 3` yazısı görünür | Telethon veya Pyrogram SQLite | **Dosyalar** (otomatik olarak algılanır) |
| `key_datas` içeren bir `tdata` klasörü | Telegram Masaüstü TData | İki dosyayı ZIP'leyin, ardından **Dosyalar** |
| `1` ile başlayan tek satırlık metin, yaklaşık 350 karakter | Telethon StringSession | **Dosyalar** |
| `*.json` ile `app_id`/`app_hash` | İlişkili meta veriler | **Dosyalar**, oturum bilgileriyle birlikte |
| `*.json` ile `auth_key` veya `string_session` | Hesap JSON'u | **Dosyalar** |
| 512 karakter `0-9a-f` | Oturum Açma Anahtarı | **Oturum açma anahtarı** |
| 32 karakter `0-9a-f` | API hash | **API Kimliği + Hash** |
| Bir TDLib uygulamasından `td.binlog` veya `db.sqlite` | TDLib depolama | Desteklenmiyor |
| `123456789:AA…` | Bot jetonu | Desteklenmiyor |

## Desteklenmeyen formatlar

| Biçim | Alternatif |
| --- | --- |
| TDLib depolama (`td.binlog`) ve TDLib dışa aktarımları | Telefon veya QR koduyla giriş yapın |
| Pyrogram oturum **dizeleri** | Pyrogram `.session` dosyasını veya telefon/QR kodunu kullanın |
| Birkaç oturum açılmış hesap içeren TData | Telegram Desktop'taki diğer hesaplardan çıkış yapın veya her hesabın kendi oturum dosyasını kullanın |
| Bot jetonları | Desteklenmez: TgWitness, bir kullanıcı hesabı olarak gözlem yapar |
| Çok sayıda hesabın CSV/JSON listeleri | Desteklenen oturum dosyalarını **Hesaplar → Hesapları içe aktar** üzerinden içe aktarın veya ayrı çalışma alanlarında telefon/QR ile giriş yapın |
| Test-DC veya bot oturumları | Üretim kullanıcı hesabı kullanın |

## Birden fazla hesap

Hesap seçicinin yanındaki **+** tuşuna basın veya **Hesap → Ayarlar → Bağlantı ayarları → Çalışma alanları'nı** açın, bir etiket girin ve oturum açın.

- Ana çalışma alanı dahil olmak üzere sınırsız sayıda çalışma alanı. Her birinin kendine ait oturumu, proxy yolu, kaynakları, yakalama politikası, günlüğü, imzalama anahtarı, kontrol noktaları ve dışa aktarımları vardır.
- Görüntülenen çalışma alanını değiştirmek, diğerlerini duraklatmaz.
- Bir günlük, onu oluşturan hesaba bağlı kalır. Farklı bir hesapla oturum açmak için başka bir çalışma alanı gerekir ve bir hesap iki çalışma alanına atanamaz.
- Ana panel jetonu tüm çalışma alanlarını kontrol eder. [Verilen erişim izni](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/), ayrı izinler ve oturum sınırlamalarıyla diğer kişilerin erişimini belirli hesaplar ve sohbetlerle sınırlayabilir.
- **Hesaplar,** bir çalışma alanının adını değiştirir ve eklenen bir çalışma alanını, oturumu, günlüğü, kaynakları ve imzalama anahtarıyla birlikte siler. Ana çalışma alanı panelden silinemez.

### Toplu içe aktarma ve hesap grupları

**Hesaplar → Hesapları içe aktar** seçeneğini kullanarak birden fazla hesap ekleyin, dosyaları temel ada göre eşleştirin ve her oturum açma sonucunu görüntüleyin. Her hesap kendi çalışma alanına sahip olur.

Bir grup, oturumlarını, anahtarlarını veya kanıtlarını birleştirmeden ilgili hesapları bir arada tutar. **Hesaplar** altındaki **grubu açtığınızda**, grubun sayfasına yönlendirilirsiniz: `/groups/<id>`:

- **Hesaplar:** her üyenin bağlantı yolu, gözlemleri ve son mesajı; "**Tümünü** başlat" ve "**Tümünü duraklat"** seçenekleri ile.
- **Dikkat gerekiyor:** oturumu kapatılmış, erişilemeyen veya bağlantı, giriş, kaynak ya da medya sorunu olan hesaplar; her bir isim kendi kartına yönlendirir.
- **Birden fazla hesabın görüldüğü sohbetler:** paylaşılan kaynaklar, bunları gözlemleyen hesaplar ve kullanılabilir çalışma alanı gözlem süresindeki kesintiler (en fazla yedi gün). **N hesapla dışa aktarma,** bir kanal veya süper grubun dışa aktarımını bu hesaplar arasında böler ve tek bir arşivi imzalar.
- **Grubu dışa aktar:** her hesabın imzalanmış dışa aktarımının bulunduğu bir ZIP `accounts/` ve `manifest.json` SHA-256 ve anahtar parmak izlerini listeleyen, ana çalışma alanı tarafından `manifest.signature.json`. Her hesap arşivini, `python -m tgwitness.verify` ve o hesabın güvenilir parmak izi ile ayrı ayrı doğrulayın.

Üyeler grubun ayarlarını paylaşır; bir hesap kendi değerlerini koruyabilir. [Paylaşılan ayarlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/settings/#account-groups), [içe aktarma ve gruplar kılavuzuna](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) ve [MTProxy havuz panosuna](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources) bakın.

## Çıkış

**Hesap → Telegram'dan çıkış yap** (gözlem duraklatılmış halde), Telegram'dan oturumu sonlandırmasını ister; böylece oturum, hesabın **Ayarlar → Cihazlar** bölümünden de kaybolur ve çalışma alanı kasasından kaldırılır. Günlük, kaynaklar, ayarlar ve imzalama anahtarı kalır ve günlük, çıkış işlemini kaydeder. Çalışma alanı hâlâ ilgili hesaba aittir: yalnızca o hesap tekrar bağlanabilir. Telegram yanıt vermezse, oturum yine de buradan kaldırılır ve panelde bu durum belirtilir; Telegram’da **Ayarlar → Cihazlar** altından oturumu sonlandırın.

## Hesap dosyalarını güvende tutma

- Her bir `.session`, TData ZIP, StringSession, Auth Key ve hesap JSON dosyasını bir şifre gibi ele alın. TgWitness, içe aktarılan yetkilendirme bilgilerini şifreli kasasında saklar; daha sonra orijinal dosyaları silebilirsiniz.
- Aynı yetkilendirmeyi aynı anda iki programda çalıştırmayın. Telegram bu yetkilendirmeyi iptal edebilir (`AUTH_KEY_DUPLICATED`) ve her iki kopya da çalışmaz hale gelir.
- Süresi dolmuş veya iptal edilmiş bir oturum, dönüştürme yoluyla yeniden etkinleştirilemez. Lütfen tekrar oturum açın.

## Sorun Giderme

| Mesaj veya belirti | Ne yapılmalı |
| --- | --- |
| *Bu oturumu okuyamıyor. Orijinal istemcisini kapatın…* | SQLite dosyası açık veya tamamlanmamış durumda (`-journal`/`-wal` sidecar). Orijinal programı düzgün bir şekilde kapatın ve dosyayı yeniden kopyalayın. |
| *Desteklenen Telethon SQLite şemaları: 7 ve 8* / *Pyrogram … 2 ve 3* | Dosya, çok eski veya bilinmeyen bir kütüphane sürümüyle oluşturulmuştur. Bunun yerine telefon/QR koduyla giriş yapın. |
| *Yalnızca yetkili üretim kullanıcı oturumları desteklenmektedir* | Pyrogram dosyası bir bota veya test ağına aittir. |
| *TData arşivi 512 girdiyi veya 32 MiB'yi aşıyor* | Sadece `key_datas` ve `D877F783D5D3EF8Cs` ZIP dosyalarını ekleyin, klasörün tamamını değil. |
| *TData'nın şifresi çözülemiyor. Masaüstü yerel şifresini kontrol edin* | **"Şifre" veya "oturum metni"** alanına Telegram Desktop yerel şifrenizi girin. |
| *Her seferinde tek bir TData hesabı içe aktarın* | Telegram Desktop'ta birkaç hesap vardı; bkz. [Desteklenmeyen biçimler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#unsupported-formats). |
| *Seçilen dosyalar, farklı hesapları veya API kimlik bilgilerini açıklamaktadır* | Yalnızca bir hesaba ait dosyaları seçin. |
| *JSON dosyasında desteklenen API kimlik bilgileri veya yetkilendirme bulunmamaktadır* | [Hesap](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#account-json)JSON'undaki alan adlarını kontrol edin. |
| *Yalnızca API meta verileri* | JSON'da oturum bilgisi yoktur. `.session` dosyasını ekleyin veya telefon/QR kodunu kullanın. |
| *Auth Key HEX, 512 onaltılık karakterin tamamını içermelidir* | Anahtar kesik veya "`…`" ifadesini içeriyor. |
| Hesap kimliği, içe aktarılan hesapla eşleşmiyor | Dosyanın kullanıcı kimliği, Telegram'ın bildirdiğinden farklıdır; dosya başka bir hesaba aittir. |
| Hesap zaten başka bir çalışma alanına ait | Hesabı iki kez eklemek yerine o çalışma alanını açın. |
| Bağlantı kurulmuş, ancak "**Kaynaklar"** bölümündeki sohbet listesinde bir özel grup eksik. | Üyeliği kontrol edin. Seçici, ilk 1.000 diyaloğu inceler; **Parametreler** altından sınırı artırın. |
| Proxy bağlantısı başarısız | Yol ve IP modunu kontrol edin. Otomatik MTProxy, çalışan başka bir girişi dener. Adres gizleme bekler; son çare olarak Direct, yapılandırılan gecikmeden sonra doğrudan bağlanabilir. [Yönlendirme modlarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes) bakın. |

Ayrıca bakınız: proxy'ler ve şifreleme için [bağlantı ve güvenlik](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/), ve oturum açıldıktan sonra yakalanan verilerin [nasıl toplandığı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/).
