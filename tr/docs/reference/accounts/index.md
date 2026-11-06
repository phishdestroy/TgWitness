# Telegram · Hesaplar ve oturum biçimleri

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/

Telefon, QR kodu veya kimlik anahtarıyla oturum açın, Telethon, Pyrogram veya Telegram Desktop oturumlarını içe aktarın ve birden fazla hesabı yönetin.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Başlangıç](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/)

![Başlangıç](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

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

Telegram API uygulaması oluşturmadan oturum açabilirsiniz. Hiçbir çift girilmediğinde, ithal edilmediğinde veya çalışma alanında önceden kaydedilmediğinde, TgWitness yerleşik 50 genel API çiftleri havuzundan (`tgwitness/api_pool.py`) bir çift seçer; yeni bir oturum açma işlemi için Telegram Desktop'ı tercih eder ve önceden kaydedilmiş çifti öncelikli olarak kullanır; kalan adaylar rastgele sıralanır. Telegram bir çifti reddederse (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), bir sonraki çift denenir; her oturum açma işlemi için en fazla sekiz çift denenir; reddedilen çiftler yeniden başlatılana kadar atlanır. Oturum açmada kullanılan çift, hesapla birlikte kaydedilir ve bu hesap için yeniden kullanılır. Bir **API ID** ve **API hash**, uygulamayı Telegram’a tanıtmaktadır; bunlar tek başlarına bir hesabı yetkilendirmemektedir.

Eksik bağlantı alanları, pakete dahil [opentele2 2.0.0 kataloglarından](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735) belirleyici bir cihaz/işletim sistemi çifti kullanır: Masaüstü `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834` ve Web `2496`. Android'in kaynak derleme kimliği `4` de, [Telegram Android'in BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java) bölümünde belirtildiği gibi Android kataloğunu kullanır. Web için varsayılan değer A'dır; içe aktarılan `K` uygulama sürümü son eki veya `macos` dil paketi seçildiğinde K seçilir ve `0.7.0` sürümü seçildiğinde Webogram seçilir. Bilinmeyen uygulama kimlikleri, Telethon'un ana varsayılan değerlerini korur. İçe aktarılan alanlar her zaman önceliklidir; buna eski bir uygulama sürümü ve boş bir dil paketi de dahildir. Katalog, API kimliğini/hash değerini asla değiştirmez. Sürüm anlık görüntüsü, oturum açma sırasında alınmaz, açıkça incelenir. Kaydedilmiş bir profil, güncellemelerden sonra da sabit kalır.

`account.getAuthorizations`, Telegram'ın kaydedilmiş yetkilendirme meta verilerini bildirir; bu, her yeni `initConnection`'in bir yankısı değildir. Bunu, fiilen gönderilen profille karşılaştırın. Mevcut bir yetkilendirmeyi bağlamak, ona eşlik eden API hash'ini doğrulamaz: `initConnection`, API kimliğini gönderirken, hash ise oturum açma isteklerinde kullanılır.

Yeni bir telefon veya QR yetkilendirmesinden sonra, TgWitness, yapılandırma, en yakın veri merkezi, çevrimiçi durum, diller (dil paketi boş değilse), uygulama güncellemeleri ve hizmet şartları güncellemelerini ister; istekler arasında 0.3–1.5 saniye bulunur. Durum güncellemesi, hesabı kısa bir süreliğine çevrimiçi olarak işaretler. Bu sıra, oturum açma işlemi tamamlandığında bir kez çalışır; içe aktarmalarda, yeniden bağlanmalarda veya yeniden başlatmalarda çalışmaz. Önce yetkilendirme kaydedilir; başarısız bir istek, yeniden deneme yapmadan veya oturum açma işlemini iptal etmeden sırayı durdurur. Sonuçlar, yanıt gövdeleri yerine hata adlarıyla birlikte `account.initialized` olarak kaydedilir. Bu sıra, hesap kısıtlamalarına karşı bir garanti değildir.

`tdesktop` için, eksik bir `tz_offset` değeri, sunucunun yerel UTC ofsetini kullanır ve bu değer, [opentele2 algoritması](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; lisans `tgwitness/client_profiles.LICENSE` 'te) kullanılarak 900 saniyeye yuvarlanır. Her bağlantıda yenilenir, böylece yaz saati değişiklikleri yansıtılır. İçe aktarılan `tz_offset` , her platformda önceliklidir ve sıfır dahil olmak üzere aynen korunur. Diğer `initConnection.params` girişleri korunur. HTTP oturum açma formu, dosya içe aktarma işlemiyle döndürülen sayısal saat dilimini kabul eder; desteklenen aralığın dışındaki boole değerleri, kesirler ve ofsetler reddedilir.

Doğrudan, SOCKS5 ve HTTP CONNECT rotaları Telethon'un `ConnectionTcpObfuscated` 'sini (gizlenmiş kısaltılmış MTProto) kullanır. HTTPS CONNECT, proxy'ye giden TLS bağlantısını korur ve tünel içinde aynı gizlenmiş aktarım yöntemini kullanır. MTProxy, gerekli olan rastgele ara aktarım ve gizli bilgi işleme özelliklerini korur. Rota geçişlerinde de aynı seçenekler uygulanır. Gizleme işlemi paket çerçevelemesini değiştirir; ancak hesabı veya istemci meta verilerini Telegram'dan gizlemez ya da kısıtlamalara karşı dokunulmazlık sağladığını ima etmez.

Yetkili bir istemci bağlandıktan sonra, TgWitness; yapılandırmayı, en yakın veri merkezini, mevcut yetkilendirmeyi, gözden geçirilmiş katman temel değerini, dilleri, uygulama güncellemelerini ve hizmet şartları güncellemelerini kontrol eder. Bu tanılama işlemleri, her istemci örneği için bir kez, veri toplanmadan önce çalıştırılır ve bağlantı ayrıntıları altında zaman bilgileriyle birlikte gösterilir. `account.connection_checked`, sonucu oturum hash'leri, IP'ler, belirteçler veya API hash'leri olmadan kaydeder. Asla şartları kabul etmez veya güncellemeleri yüklemez. Bir istek hatası veya FloodWait, sonraki istekleri durdurur; eksik bir sonuç bilinmeyen olarak kalır. Ağ kontrolleri atlanırken yerel kontroller sonuçlarını yine de bildirebilir.

FloodWait tanılama bilgileri, başarısız olan TL yöntemini, varsa Takeout/aralık sarmalayıcılarını, sunucu tarafından talep edilen bekleme süresini ve `telegram.backoff`'daki etkin son tarihi saklar. Bağlantı ayrıntıları, istekler duraklatılmışken yöntemi ve son tarihi gösterir. Teşhis, söz konusu istemcinin oluşturulduğu andan itibaren yöntem başına istemci çağrı sayaçlarını içerir; bu sayaçlar, iç içe geçmiş eş çözümlemelerini ayrı olarak sayar, ancak paketleri veya Telethon’un dahili yeniden deneme girişimlerini saymaz. Mevcut sayaçlar, durum API’sinde `collector.rpc_activity` olarak da mevcuttur. İstek argümanları, kullanıcı adları, erişim hash'leri veya istisna metinleri dahil edilmez. Son tanılama ve tam son tarih yeniden başlatma işleminden sonra da korunur. Yöntem kaydı olmayan önceki beklemeler geriye dönük olarak atfedilemez. Kaynak incelemesi ve keşif ile geçmiş edinimi arasındaki ayrım için bkz. [dışa aktarma sınırları](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md).

`official_app=True` veya `False`, Telegram'ın mevcut yetkilendirme bayrağıdır. Her iki değer de hesabın kısıtlı, güvenilir veya gözlem altında olup olmadığını belirlemez. Mevcut kanıt modu `account.devices` anlık görüntüleri, tüm oturum açılmış cihazların geçmişini içerir; bağlantı tanılama ise yalnızca mevcut cihazın açıklamasını saklar.

Bağlantı kurulmadan önce, danışma kontrolleri API platformunu, dil paketini, cihaz/işletim sistemi ve uygulama sürümü formatlarını, mobil sistem yerel ayarlarını ve Telethon'un gerçek şema katmanını, incelenen katalog temel değerleriyle karşılaştırır. Uyarılar sunucu günlüğünde ve hesap durumu meta verilerinde görünür; bunlar hiçbir zaman içe aktarılan değerlerin yerini almaz veya şema katmanını değiştirmez. Farklı bir katman, bir uyumluluk inceleme sinyalidir; hesabın bozuk veya kısıtlanmış olduğunun kanıtı değildir. Bu kontroller ve `official_app`, Telegram’ın hesabı kısıtlamalardan muaf gördüğünü garanti etmez. Bağlantısı kesilmiş hesap durumu, başka bir cihaz açıklaması oluşturmak yerine kaydedilmiş profili kullanır.

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

**Dosyalar**, **Otorizasyon anahtarı** ve toplu içe aktarma formları, bağlanmadan önce paralel oturum uyarısını gösterir. Varsayılan olarak içe aktarılan yetkilendirmeler yeniden kullanılır. Anahtarı burada kullanılırken orijinal istemciyi kapalı tutun. **Dosyalar** ve **Otorizasyon anahtarı** ayrıca aşağıda açıklanan **Bağımsız bir yetkilendirme oluştur** seçeneğini sunar. Toplu içe aktarma hâlâ doğrudan modu kullanır. Telefon ve etkileşimli QR girişi, ayrı yetkilendirmeler oluşturur. İçe aktarma formunda uyarı başlığı görünür kalır; dosyalar veya bir anahtar/oturum dizesi sağlandığında tam açıklaması otomatik olarak açılır. Okunduktan sonra daraltılabilir, böylece dosya seçici ve bağlantı kontrolleri telefonda kullanılabilir durumda kalır.

- Dosyalar, TgWitness sunucunuzun **belleğinde** dönüştürülür. Yüklenen dosyalar depolanmaz, ZIP dosyaları diske açılmaz ve hiçbir harici hizmetle bağlantı kurulmaz.
- Elde edilen oturum daha sonra Telegram ile karşılaştırılır. Bir dosyada bir kullanıcı kimliği belirtiliyorsa, bu kimlik, Telegram'ın bildirdiği hesapla eşleşmelidir.
- Farklı hesapları veya farklı API kimlik bilgilerini açıklayan dosyalar reddedilir; tek bir tanesini seçmek yerine.
- **Şifre veya oturum metni**, TData yerel şifre alanını içerir; bu alan, **oturum açmadan** StringSession ve **Read**dosyalarını yapıştırmak için bir kutudur (Telegram ile iletişime geçmeden formu doldurur).

### Bağımsız bir yetkilendirme oluşturun

**'u seçin. İçe aktarılan dosyaları veya bir Oturum Açma Anahtarı'nı bağlamadan önce bağımsız bir yetkilendirme** oluşturun. TgWitness, içe aktarılan donörü kısa süreliğine bağlar, bunu yeni istemcinin QR oturum açma belirtecini onaylamak için kullanır ve onaydan hemen sonra donörün bağlantısını keser. Yeni istemcinin kendi yetkilendirme anahtarı ve ayrı olarak seçilmiş bir Masaüstü profili vardır. Bağışçının sağladığı API kimlik bilgileri ve cihaz profili yalnızca bağışçı bağlantısı için kullanılır. Mevcut hiçbir yetkilendirme oturumu kapatılmaz veya iptal edilmez.

**Bu adım sırasında bağışçının orijinal istemcisini tamamen kapalı tutun.** İlk bağlantı hâlâ kopyalanmış anahtarı kullanır, bu nedenle bu mod, o ilk paralel kullanım riskini ortadan kaldıramaz. Yeni yetkilendirme bağlandıktan sonra, sahibi orijinal istemciyi yeniden açabilir ve her ikisini de bağımsız olarak kullanabilir. Etkileşimli **QR kodu** ile oturum açma, orijinal istemcinin anahtarını buraya kopyalamadan veya bağlamadan oturum açmayı onaylamasına olanak tanır.

Telegram 2FA talep ederse, bu mod mevcut olduğunda seçilen JSON'dan `twoFA`'i kullanır, aksi takdirde şifre sorar. Reddedilen bir içe aktarılan şifre, şifre formuna geri döner. Şifreler kaydedilmez. Aday anahtar, veri merkezi geçişi sırasındaki değişiklikler de dahil olmak üzere şifrelenmiş olarak `independent_login.enc`'de kaydedilir. Bir kesintiden sonra, kaydedilen adayı devam ettirmek için aynı bağışçıyı ve bu seçeneği seçin. Çalışma alanı o hesap için ayrılmış olarak kalır; işlemin başarısızlıkla sonuçlanması yeni çalışma alanını silmez. Veri dizinini ve kasa anahtarını saklayın. Nihai kimlik bilgileri ve `account.authorized` günlük kaydı, bağışçı anahtarı veya şifre hariç olmak üzere içe aktarma yöntemini, giriş formatlarını ve bağışçı API kimliğini içerir.

5 Kasım 2026 tarihinde, özel bir hesap Telethon, Pyrogram ve TData bağışçılarıyla canlı kontrolleri geçti: 2 faktörlü kimlik doğrulama (2FA) tamamlanması, farklı yeni yetkilendirme anahtarları, bağışçı ve yeni istemci tarafından eşzamanlı erişim ve halka açık bir kanalın okunması. Telethon örneğinde ayrıca şifre adımında yaşanan bir kesintinin ardından kaydedilmiş bir aday yeniden başlatıldı. Her yeni yetkilendirme, oturum açma sonrası altı başlatma isteğini tamamladı ve imzalı günlüğü doğrulandı. Orijinal oturum, sağlanan dört formatın hepsinde kullanılabilir durumda kaldı.

Telegram'ın [RPC hata veritabanı](https://core.telegram.org/api/errors.json), `FRESH_CHANGE_ADMINS_FORBIDDEN`'yi yönetici değişikliğiyle, `FRESH_CHANGE_PHONE_FORBIDDEN`'ü telefon numarası değişikliğiyle ve `FRESH_RESET_AUTHORISATION_FORBIDDEN`'ü diğer oturumların iptal edilmesi, ömürlerinin değiştirilmesi veya bir geçiş anahtarının kaydedilmesiyle ilişkilendirir. `SESSION_TOO_FRESH_*` ve `PASSWORD_TOO_FRESH_*`, sahiplik devri ve gelir veya hediye çekme işlemleriyle ilgilidir. Bunlar toplama işlemleri değildir; yeni bir oturum açma, genel bir 24 saatlik okuma yasağı anlamına gelmez. Dışa aktarma, `TAKEOUT_INIT_DELAY_*`'yi ayrı olarak döndürebilir. TgWitness, sunucu tarafından talep edilen duraklamaları korur ve kısıtlamaları aşmak için belirteç kabulünü otomatik olarak yeniden denemez veya oturumları iptal etmez.

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
- Bağlantı profili `device_model` (`device` takma adı), `system_version` (`sdk` takma adı), `app_version`, `lang_code`, `system_lang_code` (`system_lang_pack` takma adı), `lang_pack` ve isteğe bağlı `tz_offset`'u (UTC'ye göre saniye, -43200 ile 50400 arası) kullanır. Girilen alanlar, oluşturulan varsayılan değerlere ve panel/tarayıcı diline göre önceliklidir. Çakışan takma adlar reddedilir. Çözümlenen profil, şifrelenmiş çalışma alanı kimlik bilgilerine kaydedilir ve uygulama sürümü de dahil olmak üzere yeniden başlatma sonrasında yeniden kullanılır.
- `phone`, proxy ayarları ve cihaz belirteçleri **yoksayılır**. `twoFA`, yalnızca **Bağımsız yetkilendirme oluştur** seçeneği seçildiğinde okunur; doğrudan içe aktarma sırasında yoksayılır.
- Desteklenen bir yetkilendirme alanı içermeyen bir JSON dosyası yalnızca meta veridir. Oturum dosyasını ekleyin veya telefon ya da QR koduyla oturum açmaya devam edin. Desteklenen bir oturum veya Auth Key içeren bir JSON dosyası tek başına yetkilendirme yapabilir; bkz. [Account JSON](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#account-json).

### Telegram Masaüstü (TData)

TData, Telegram Desktop uygulamasının (desktop.telegram.org adresinden indirilebilen platformlar arası uygulama) `tdata` klasörüdür.

| Sistem | Varsayılan `tdata` konumu |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (taşınabilir Telegram: `Telegram.exe`'nin yanında) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

İçe aktarmak için:

> **Paralel oturum uyarısı.** Doğrudan TData içe aktarımı, Telegram Desktop'ın yetkilendirme anahtarını yeniden kullanır. Bu anahtarı Desktop ve TgWitness'da aynı anda kullanmayın. Telegram, `AUTH_KEY_DUPLICATED` ile yetkilendirmeyi geçersiz kılabilir ve bu durumda yeni bir oturum açılana kadar her iki kopya da kullanılamaz hale gelir.
>
>
>
> Desktop'u, sistem tepsisindeki işlemi de dahil olmak üzere tamamen kapatın ve TgWitness içe aktarılan oturumu kullanırken bu kopyayı kapalı tutun. **Kapatın, oturumu kapatmayın veya iptal etmeyin:** iptal işlemi, içe aktarılan kopyayı da geçersiz kılar. Her iki istemcinin de çalışması gerekiyorsa, **Bağımsız yetkilendirme oluştur'u seçin** ve yeni oturum açma işlemi başarılı olana kadar Desktop'ı kapalı tutun ya da telefon veya QR ile TgWitness'e giriş yapın. Özel bir hesap kullanılması önerilir, ancak bu, klonlanmış anahtarların paralel olarak güvenli bir şekilde kullanılmasını sağlamaz.
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
| `string_session` (`session_string`, `session_str`; eski `session`) | Telethon StringSession metni, dosya adı değil |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512 karakterlik tam Otorizasyon Anahtarı ve DC 1–5 |
| `user_id` (`id`) | İsteğe bağlı; yetkilendirme kaydedilmeden önce Telegram ile karşılaştırılarak kontrol edilir |
| `device_model` (`device`) | Bağlantı cihazı açıklaması |
| `system_version` (`sdk`) | Bağlantı işletim sistemi sürümü |
| `app_version` | Telegram'a gönderilen uygulama sürümü |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | İstemci dili, sistem dili ve istemci dil paketi; boş bir `lang_pack` değerine izin verilir |
| `tz_offset` | `initConnection.params`'da gönderilen, saniye cinsinden isteğe bağlı UTC zaman farkı; tamsayı veya ondalık tamsayı dizesi |

Hem takma ad hem de ana ad mevcutsa, bunlar birbiriyle uyumlu olmalıdır. Açık Telethon oturum alanları, başka bir formattaki genel `session` blobuna göre önceliklidir. Eğer her ikisi de tanınabilir Telethon oturumları içeriyorsa, aynı yetkilendirmeyi tanımlamalıdır. Açık bir alan yoksa, `session` geçerli bir Telethon StringSession olmalıdır. Örnekler:

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
