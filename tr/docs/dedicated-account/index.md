# Ayrı bir hesap kullanın. Asla ana hesabınızı kullanmayın.

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/dedicated-account/

Hesabınızı bağlamadan önce lütfen okuyun

Ana hesabınızı kullanmamanız yönündeki tavsiyemiz şaka değildir. Bu bir gerçektir.

Ana hesap

- Kendi uygulama hash'inizle, hesapların %99'u oturumdan çıkarılır
- Sadece düşük güven derecesi nedeniyle hesapların yasaklanması sıkça görülmektedir
- Ana hesabınızı kullanmak gerçekten aptalca bir fikirdir

Genel API kimliği/API hash çiftleri üzerinde bir ek hesap

- Bu API ID/API hash çiftleri aracılığıyla bir milyondan fazla hesap kaydedilmiştir
- Bu API ID/API hash çiftleri 5 yılı aşkın süredir kullanılmaktadır
- Hiç kimse bu API çiftleri aracılığıyla verilerinizin hiçbirini göremez

01

## Neden ana hesabınızı kullanmamalısınız?

Bu bilgiler doğrudur. Bu sorunların tuzaklarının tam olarak nerede olduğunu biliyoruz.

1. ### Kendi uygulama hash'inizle, hesapların %99'u oturumdan çıkarılır

   Erişiminiz olmayan bir hesapla my.telegram.org adresine giriş yapıp bir uygulama hash'i elde ettikten sonra, bu uygulama hash'i üzerinden herhangi bir istek gönderirseniz, hesabın oturumu kapatılma olasılığı %99'dur. Bunu kontrol edebilirsiniz.
2. ### Sadece düşük güven derecesi nedeniyle hesapların yasaklanması sıkça görülmektedir

   Hesaplar, sırf Telegram onlara güvenmediği için yasaklanıyor ve bu tür yasaklamalar sık sık yaşanıyor. Bunu da kontrol edebilirsiniz. Kendi hesabınızı kullanmak gerçekten aptalca bir fikir.
3. ### Kopyalanan oturum anahtarları iptal edilebilir

   İçe aktarılan bir TData/oturum anahtarını Telegram Desktop ve TgWitness'te aynı anda çalıştırmak, `AUTH_KEY_DUPLICATED` hatasını tetikleyebilir. Telegram bu yetkilendirmeyi geçersiz kılar, bu nedenle her iki kopya için de yeni bir oturum açma işlemi gerekir. Özel bir hesap bunu engellemez.

   Orijinal istemciden tamamen çıkın ve içe aktarılan oturumu kullanırken istemciyi kapalı tutun. Paralel kullanım için, telefon veya QR ile TgWitness'e giriş yaparak ayrı bir yetkilendirme oluşturun; ayrı olarak yetkilendirilmiş diğer istemciler oturumda kalabilir.

   [Oturum içe aktarma uyarısını okuyun](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr#session-warning)

Telegram belgeleri

- [Oturum kapatma hataları: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Kendi uygulama hash'inizi oluşturma: api_id'yi alma](https://core.telegram.org/api/obtaining_api_id)

02

## TgWitness neden halka açık uygulama hash'i ve uygulama kimliği çiftleri aracılığıyla çalışır?

İşte bu nedenle TgWitness'i halka açık uygulama hash/uygulama kimliği çiftleri üzerine kurduk. Mantığımıza göre, bu çiftler kullanıldığında yasaklanma olasılığı daha düşüktür: bu çiftler aracılığıyla bir milyondan fazla Telegram hesabı kaydedilmiştir ve birçok farklı program bu çiftler üzerinden çalışmaktadır. Mantığımıza göre, bu, kişisel bir uygulama hash'iyle doğrudan çalışmaktan daha iyidir: bu çiftlerin 5 yıldan fazla bir süredir aktif olduğu kesindir.

### Kendi yeni API kimliği/API hash çiftiniz

my.telegram.org adresinde ilgili hesaptan oluşturulmuştur.

- Bu hesapların yaklaşık %99'u oturumdan çıkarılır
- Tek bir yeni uygulama, tek bir hesap

### Havuzdaki genel API kimliği/API hash çiftleri

Birçok programın kullandığı aynı API ID/API hash çiftleri.

- Bir milyondan fazla kayıtlı hesap
- Birçok farklı program
- Bu API çiftleri 5 yılı aşkın süredir sorunsuz bir şekilde çalışmaktadır.

### Neden kimse bu API çiftleri aracılığıyla verilerinizi göremez?

- #### API çifti bir anahtar değil, bir isimdir

  Telegram, bir program bağlandığında ve oturum açma kodu talep ettiğinde API kimliğini ve API hash değerini ister. Bunlar uygulamayı tanımlar ve hiçbir hesaba erişim izni vermez; Telethon'un belgelerinde, bir çiftin herhangi bir telefon numarasıyla çalıştığı belirtilmektedir.
- #### Oturum anahtarınız asla sunucunuzdan dışarı çıkmaz

  Giriş yapıldığında, TgWitness ve Telegram arasında bir Diffie–Hellman değişimi yoluyla bir yetkilendirme anahtarı oluşturulur; anahtarın kendisi hiçbir zaman gönderilmez. Telegram belgelerine göre: yetkilendirme işleminden sonra anahtar kullanıcıyla ilişkilendirilir ve bu anahtarla yapılan her çağrı o kullanıcı adına gerçekleştirilir. Aynı anahtar çiftine sahip diğer programların kendi anahtarları vardır ve sizin anahtarınızı kullanamazlar.
- #### Trafik, sizin anahtarınızla şifrelenir

  Her istek ve yanıt, API hash'i ile değil, oturumun yetkilendirme anahtarıyla şifrelenir. API hash'ini bilmek hiçbir şeyin şifresini çözmez.
- #### API kimliği/API hash çifti sahibi hiçbir şey görmez

  Telegram'da hesapları, oturumları veya mesajları API kimliğine göre listeleyen bir yöntem bulunmamaktadır. Bir çiftin sahibi, my.telegram.org adresinde yalnızca kendi uygulama ayarlarını görebilir.
- #### Hangi uygulama olduğu yalnızca sizin hesabınız tarafından görülebilir

  Kendi hesabınızın Ayarlar → Cihazlar bölümünde, her oturumun uygulama adı ve API kimliği, cihaz, IP adresi ve tarihleri listelenir. Bu listeye başka hiç kimse erişemez.

Telegram belgeleri

- [Kullanıcı yetkilendirme: anahtar, kullanıcıya bağlanır](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [MTProto yetkilendirme anahtarının oluşturulması](https://core.telegram.org/mtproto/auth_key)
- [MTProto şifreleme](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Bir Telegram yetkilendirme (oturum) girdisi neleri içerir?](https://core.telegram.org/constructor/authorization)
- [api_id'nin alınması](https://core.telegram.org/api/obtaining_api_id)
- [Telegram uygulamalarının açık kaynak kodu](https://telegram.org/apps#source-code)

Kütüphaneler ve tartışma başlıkları

- [Telethon: Telegram'da oturum açma](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: Resmi uygulamaların API kimlik bilgileri](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: api_hash gizli tutulmalı mı?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Diğer programlardaki aynı API ID/API hash çiftleri 7

Resmi Telegram uygulamalarının API ID/API hash çiftleri halka açıktır ve birçok bağımsız programa ve kütüphaneye entegre edilmiştir:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Hesap kaydı amacıyla yayınlanan, resmi Telegram uygulamalarının API ID/API hash çiftlerini listeleyen bir forum gönderisi

03

## Ek hesap oluşturma yöntemleri

Bir Telegram hesabı için, giriş kodunu alacak bir telefon numarası gereklidir. Hesabın ne kadar süreyle aktif kalması gerektiğine göre seçim yapın.

- En iyi seçim

  ### Ön ödemeli SIM veya eSIM

  ********

  Ne kadar sürer?

  Bakiyenizi dolu tuttuğunuz sürece

  Unutmayın

  En güvenilir yöntem: Telegram, gerçek cep telefonu numaralarını en iyi şekilde kabul eder. Operatörün geri aldığı bir numara başka birine verilir.
- ### Sanal telefon numaraları sunan bir uygulama

  ********

  Ne kadar sürer?

  Uygulama telefon numarasını sakladığı sürece

  Unutmayın

  Telegram, sanal numarayı reddedebilir, kodu göndermeyebilir veya yeni hesabı hemen kısıtlayabilir; bazı uygulamalar kullanılmayan numaraları geri alır.
- ### Telefon numarası kiralama

  ********

  Ne kadar sürer?

  Kiralama süresi için

  Unutmayın

  Süre dolduğunda, sıra bir sonraki müşteriye geçer.
- ### Tek seferlik etkinleştirme

  ********

  Ne kadar sürer?

  Yalnızca bir oturum açma kodu

  Unutmayın

  Numara, genellikle önceki sahiplerinin geçmiş bilgileriyle birlikte anında havuza geri döner. Her şeyden önce bulut şifresini ayarlayın.

Numarayı daha sonra elinde bulunduran kişi, bir giriş kodu talep edebilir. Bir bulut şifresi (iki aşamalı doğrulama), bu kişinin oturum açmasını engeller; bu şifre olmadan hesap, numaranın bir sonraki sahibine geçer.

Telegram belgeleri

- [Spam SSS: sanal numaralar ve önceki sahipler](https://telegram.org/faq_spam)
- [İki aşamalı doğrulama](https://core.telegram.org/api/srp)

### Kiralanan +888 numaraları (Fragment)

Bazı pazar yerleri ve hizmetler, Fragment üzerinden Telegram’ın resmi +888 numaralarının geçici olarak kiralanmasını sunmaktadır.

Yaklaşık ücret: Günlük 20 ABD doları.

- Telegram Web veya Telegram Desktop üzerinden doğrudan bir hesap açabilirsiniz.
- Belirtilen numaradaki hesapları silebilir ve yenilerini oluşturabilirsiniz.
- Bu hesaplar genellikle daha az dolandırıcılık önleme kontrolüne tabi tutulur, ancak dokunulmazlık veya özel ayrıcalıklar sağlamazlar.

Bu numara size ait değildir. Kiralama süresi sona erdiğinde, sahibi numarayı geri alabilir. Hemen bir bulut şifresi belirleyin ve bu hesabı uzun vadeli bir hesap olarak değerlendirmeyin.

+888 numarasının sahibi olmak veya kontrolünüz altındaki bir ön ödemeli SIM kart kullanmak daha güvenilirdir.

### Pazar yerlerinden hazır hesaplar

Bazı pazar yerleri (örneğin G2G veya Z2U), yeni, eski veya oturum dosyaları içeren hazır Telegram hesapları satmaktadır.

- [G2G: Telegram hesap listeleri](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Telegram hesap listeleri](https://www.z2u.com/telegram/accounts-5-15140)

ASLA ANA HESABINIZI KULLANMAYIN! Bu şekilde oluşturulan özel bir hesap, ana Telegram hesabınızı TgWitness'e eklemekten yine de daha güvenlidir.

#### Satın almadan önce uyarılar

- Bu, Telegram'ın Hizmet Şartları'nı ihlal eder.
- Birçok hesap toplu olarak kaydedilmiştir (otomatik kayıt) veya geçmişi bilinmemektedir.
- Bazı satıcıların hala kurtarma erişimi olabilir.
- Bu tür pazarlardan açılan hesaplar genellikle daha sonra yasaklanır veya kısıtlanır.
- Hırsızlık yazılımlarını, kimlik avı araçlarını veya açıkça çalınmış hesapları açıkça satan pazar yerlerinden uzak durun.
- Kimlik avı araçları, bilgi hırsızlığı yazılımları, çalınmış oturumlar veya hesapları açıkça satan platformlardan bir hesap satın almak — "otomatik kayıt" olarak tanıtılanlar dahil — sadece Telegram'ın Hizmet Şartlarını değil, aynı zamanda çoğu ülkenin yasalarını da ihlal eder. Bu durum, daha sonra kanıtlarınızın geçersiz sayılmasına neden olabilir. Seçiminizi dikkatli yapın.

#### Bu seçeneği kullanırsanız

1. Hesabı tek kullanımlık olarak değerlendirin.
2. Diğer tüm oturumları sonlandırın, bir bulut şifresi belirleyin ve kurtarma yöntemlerini derhal değiştirin.
3. Farklı sağlayıcılardan 2–3 hesap veya kendiniz kaydettiğiniz hesapları kullanın.

**Premium, silme ve yedi günlük gecikme**

Hesapta Premium varsa, telefon numarasına erişimi olan bir kişi hesabı hemen silemez. Bir bildirim alırsınız ve silinmeden önce yedi gün süreniz vardır.

Bu önemlidir çünkü araştırmanız hesaba bağlıdır: yerine geçecek bir hesap hazırlamak için zamanınız var.

**Yeni hesaplar ve API kimlik bilgileri**

SMS hizmetinden aldığınız bir numarayı kullanarak kendiniz kaydettiğiniz yeni bir hesaptan kendi api_id/api_hash'ınızı elde edip kullanırsanız, ilk API isteğinde veya oturum yetkilendirmede hesap oturumu kapatılacaktır. Bir araştırma planlarken bunu göz önünde bulundurun.

04

## Hesap oluşturma

Telefon numarası almaktan ilk kaydedilen sohbete kadar.

1. ### Bir telefon numarası alın

   Hesabın uzun süre aktif kalması gerektiğinde ön ödemeli SIM veya eSIM; kısa süreli bir iş için kiralık SIM veya tek seferlik aktivasyon. Hizmetler aşağıda listelenmiştir.
2. ### Ana hesabınızdan ayrı olarak kaydolun

   Ana hesabınızın yanında değil, ayrı bir cihazda, emülatörde veya telefon profilinde resmi Telegram uygulamasına kaydolun.
3. ### Hesabı bir bulut şifresiyle koruyun

   Hemen, başka hiçbir yerde kullanılmayan bir bulut şifresi ve kurtarma e-postası belirleyin.
4. ### Hesabın gizlilik ayarlarını kısıtlayın

   Telefon numarası: **Hiç kimse**, numaramdan beni bul; **Kişilerim**, en son görülme tarihi, profil fotoğrafları ve biyografi: **Hiç kimse** veya **Kişilerim**; kişi senkronizasyonunu kapat.
5. ### Hesabın kendi kendini imha etmesini önleyin

   Hesap kendini imha süresini en uzun süreye ayarlayın; böylece TgWitness'in durdurulması durumunda hesabınızı kaybetmezsiniz.
6. ### Hesaba tarafsız bir profil verin

   Diğer hesaplarınıza ait isim, fotoğraf, kullanıcı adı veya biyografi bilgileri ve kişisel kişiler listesi bulunmaz.
7. ### Yeni hesabın ısınmasına izin verin

   İlk başta, günde sadece birkaç sohbete katılın. Acele eden yeni hesaplar ilk olarak kısıtlanır.
8. ### Botlarla hiçbir şeyi paylaşmayın

   Bir bot için asla “Telefon numarasını paylaş” veya “Konumunu paylaş” seçeneğine basmayın. Bağlantıları ve Mini Uygulamaları, o cihazda bir VPN veya proxy üzerinden açın.
9. ### Hesabı TgWitness'e bağlayın

   Kendi çalışma alanınızda, **Hesap → QR kodu** seçeneğine tıklayın, ardından **Kaynaklar → Soruşturma modu** seçeneğine basın. Uygulama, sizin eylemlerinizi gerçekleştirdiğiniz yerdir; TgWitness ise kayıt tutan sistemdir.

Telegram belgeleri

- [İki aşamalı doğrulama](https://core.telegram.org/api/srp)
- [Gizlilik ayarları](https://core.telegram.org/api/privacy)
- [Hesap, etkin değilse kendini imha eder](https://core.telegram.org/method/account.setAccountTTL)

05

## Telefon numarası hizmetleri

Bunlar, başlangıç için seçeneklerdir. Ülkeler, fiyatlar ve Telegram'ın belirli bir numarayı kabul edip etmediği sık sık değişir, bu nedenle ödeme yapmadan önce kontrol edin.

### Ön ödemeli SIM ve eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Ön ödemeli

  PayGo planı, çok ucuz
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Ön ödemeli
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Ön ödemeli
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Ön ödemeli
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Sanal telefon numaralarına sahip uygulamalar 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Yalnızca ABD; kayıt için bir ABD telefon numarası gereklidir
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Kullanmazsanız numara geri alınır
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Diğer ülkeler
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - Ücretli hizmet

  Deneme süresi mevcuttur
- [Hushedhushed.com](https://hushed.com)

  - Birçok ülke
  - Ücretli hizmet

  Düşük fiyat
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  Bir uygulamadaki Avrupa cep telefonu numaraları
- [Sonetelsonetel.com](https://sonetel.com)

  - Birçok ülke
  - Ücretsiz bir numara
- [Zadarmazadarma.com](https://zadarma.com)

  - Birçok ülke

  Sanal telefon numaraları

### Telefon numarası kiralama ve tek seferlik aktivasyonlar 12

Bir telefon numarası kiralamak, o numaranın haftalarca veya aylarca size ait kalmasını sağlar. Tek seferlik aktivasyon, tek bir oturum açma kodu verir: kayıt olduktan hemen sonra bulut şifrenizi ayarlayın.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Numara kiralama
  - Tek seferlik aktivasyonlar
- [SMSPVAsmspva.com](https://smspva.com)

  - Numara kiralama
  - Tek seferlik aktivasyonlar
- [5SIM5sim.net](https://5sim.net)

  - Numara kiralama
  - Tek seferlik aktivasyonlar
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Numara kiralama
  - Tek seferlik etkinleştirme
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Numara kiralama
  - Tek seferlik aktivasyonlar
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Numara kiralama
  - Tek seferlik aktivasyonlar
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Numara kiralama
  - Tek seferlik aktivasyonlar
- [365SMS365sms.org](https://365sms.org)

  - Numara kiralama
  - Tek seferlik aktivasyonlar
- [SIMSMSsimsms.org](https://simsms.org)

  - Numara kiralama
  - Tek seferlik aktivasyonlar
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Tek seferlik etkinleştirme
- [SMS-MANsms-man.com](https://sms-man.com)

  - Tek seferlik etkinleştirme
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Tek seferlik etkinleştirme
