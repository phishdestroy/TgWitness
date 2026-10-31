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

Telegram API uygulaması oluşturmadan oturum açabilirsiniz. Hiçbir çift girilmediğinde, ithal edilmediğinde veya çalışma alanında önceden kaydedilmediğinde, TgWitness yerleşik havuzundaki 50 adet genel API çiftinden (`tgwitness/api_pool.py`) rastgele bir çift seçer. Telegram bir çifti reddederse (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), bir sonraki çift denenir; her oturum açma işlemi için en fazla sekiz çift denenir; reddedilen çiftler yeniden başlatılana kadar atlanır. Oturum açmada kullanılan çift, hesapla birlikte kaydedilir ve o hesap için yeniden kullanılır. Bir **API kimliği** ve **API hash'i**, uygulamayı Telegram'a tanımlar; bunlar tek başlarına bir hesabı yetkilendirmez.

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

- Dosyalar, TgWitness sunucunuzun **belleğinde** dönüştürülür. Yüklenen dosyalar depolanmaz, ZIP dosyaları diske açılmaz ve hiçbir harici hizmetle bağlantı kurulmaz.
- Elde edilen oturum daha sonra Telegram ile karşılaştırılır. Bir dosyada bir kullanıcı kimliği belirtiliyorsa, bu kimlik, Telegram'ın bildirdiği hesapla eşleşmelidir.
- Farklı hesapları veya farklı API kimlik bilgilerini açıklayan dosyalar reddedilir; tek bir tanesini seçmek yerine.
- **Şifre veya oturum metni**, TData yerel şifre alanını içerir; bu alan, **oturum açmadan** StringSession ve **Read**dosyalarını yapıştırmak için bir kutudur (Telegram ile iletişime geçmeden formu doldurur).

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
- `phone`, `device`, `sdk`, `app_version`, `lang_pack` gibi diğer alanlar veya kayıtlı bir `twoFA` şifresi **göz ardı** edilir. Hesapta 2FA varsa, TgWitness bunu ister.
- Tek başına bir JSON dosyası yalnızca meta veridir. Oturum dosyası yoksa, telefon veya QR koduyla oturum açmaya devam edin.

### Telegram Masaüstü (TData)

TData, Telegram Desktop uygulamasının (desktop.telegram.org adresinden indirilebilen platformlar arası uygulama) `tdata` klasörüdür.

| Sistem | Varsayılan `tdata` konumu |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (taşınabilir Telegram: `Telegram.exe`'nin yanında) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

İçe aktarmak için:

> **Paralel oturum uyarısı.** TData'yı içe aktarmak, Telegram Desktop'un yetkilendirme anahtarını yeniden kullanır; bağımsız bir oturum açma oluşturmaz. Bu anahtarı Desktop ve TgWitness'te aynı anda kullanmayın. Telegram, `AUTH_KEY_DUPLICATED` ile yetkilendirmeyi geçersiz kılabilir ve yeni bir oturum açılana kadar her iki kopyayı da kullanılamaz hale getirebilir.
>
>
>
> Desktop'u, sistem tepsisindeki işlemi de dahil olmak üzere tamamen kapatın ve TgWitness içe aktarılan oturumu kullanırken bu kopyayı kapalı tutun. **Çıkın, oturumu kapatmayın veya oturumu iptal etmeyin:** iptal etme işlemi, içe aktarılan kopyayı da geçersiz kılar. Her iki istemcinin de çalışması gerekiyorsa, telefon veya QR koduyla TgWitness'e giriş yaparak kendi yetkilendirme bilgilerinizi oluşturun. Ayrı bir hesap kullanılması önerilir, ancak bu, klonlanmış anahtarların paralel olarak güvenli bir şekilde kullanılmasını sağlamaz.
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
| `string_session` (`session_string`, `session`) | Telethon StringSession metni, dosya adı değil |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512 karakterlik tam Otorizasyon Anahtarı ve DC 1–5 |
| `user_id` (`id`) | İsteğe bağlı; yetkilendirme kaydedilmeden önce Telegram ile karşılaştırılarak kontrol edilir |

Hem takma ad hem de asıl ad mevcutsa, bunlar birbiriyle uyumlu olmalıdır. Örnekler:

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
| Çok sayıda hesabın CSV/JSON listeleri | Hesap başına bir çalışma alanı ekleyin |
| Test-DC veya bot oturumları | Üretim kullanıcı hesabı kullanın |

## Birden fazla hesap

Hesap seçicinin yanındaki **+** tuşuna basın veya **Hesap → Ayarlar → Bağlantı ayarları → Çalışma alanları'nı** açın, bir etiket girin ve oturum açın.

- Ana çalışma alanı dahil olmak üzere sınırsız sayıda çalışma alanı. Her birinin kendine ait oturumu, proxy yolu, kaynakları, yakalama politikası, günlüğü, imzalama anahtarı, kontrol noktaları ve dışa aktarımları vardır.
- Görüntülenen çalışma alanını değiştirmek, diğerlerini duraklatmaz.
- Bir günlük, onu oluşturan hesaba bağlı kalır. Farklı bir hesapla oturum açmak için başka bir çalışma alanı gerekir ve bir hesap iki çalışma alanına atanamaz.
- Ana panel jetonu tüm çalışma alanlarını kontrol eder. [Verilen erişim izni](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/), ayrı izinler ve oturum sınırlamalarıyla diğer kişilerin erişimini belirli hesaplar ve sohbetlerle sınırlayabilir.
- **Hesaplar,** bir çalışma alanının adını değiştirir ve eklenen bir çalışma alanını, oturumu, günlüğü, kaynakları ve imzalama anahtarıyla birlikte siler. Ana çalışma alanı panelden silinemez.

## Çıkış

**Hesap → Telegram'dan çıkış yap** (gözlem duraklatılmış halde), Telegram'dan oturumu sonlandırmasını ister; böylece oturum, hesabın **Ayarlar → Cihazlar** bölümünden de kaybolur ve çalışma alanı kasasından kaldırılır. Günlük, kaynaklar, ayarlar ve imzalama anahtarı kalır ve günlük, çıkış işlemini kaydeder. Çalışma alanı hâlâ ilgili hesaba aittir: yalnızca o hesap tekrar bağlanabilir. Telegram yanıt vermezse, oturum yine de buradan kaldırılır ve panelde bu durum belirtilir; Telegram’da **Ayarlar → Cihazlar** altından oturumu sonlandırın.

## Bir Telethon oturumunu çevrimdışı ortama dönüştürün

Panel, `.session` dosyalarını doğrudan içe aktarır. Çevrimdışı olarak bir StringSession dosyasına dönüştürmek için proje klasöründen şu komutu çalıştırın:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Dönüştürücü yalnızca Telethon SQLite dosyalarını okur (en fazla 64 MiB), girdiyi asla değiştirmez, ağ isteği göndermez ve mevcut bir çıktı dosyasının üzerine yazmayı reddeder.

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
| Proxy bağlantısı başarısız | Yol ve IP modunu kontrol edin. Otomatik MTProxy, çalışan başka bir girişi dener. IP gizleme modu bekler; açıkça seçilen yedek mod, yapılandırılan gecikme süresinden sonra doğrudan bağlanabilir. [Yönlendirme modlarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes) bakın. |

Ayrıca bakınız: proxy'ler ve şifreleme için [bağlantı ve güvenlik](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/), ve oturum açıldıktan sonra yakalanan verilerin [nasıl toplandığı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/).
