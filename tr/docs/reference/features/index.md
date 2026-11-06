# Özellikler ve sınırlamalar

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/

TgWitness’in mevcut toplama modeli, çoklu hesap iş akışları, dışa aktarımlar ve operasyonel sınırları.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Proje referansı](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Proje referansı](https://phishdestroy.github.io/TgWitness/assets/chapter-project.svg)

TgWitness, bağlı hesapların erişebildiği Telegram sohbetlerini korur, gözlemlenen değişiklikleri kaydeder ve doğrulanabilir dışa aktarımlar hazırlar. Bu kılavuzda toplama modeli, mevcut iş akışları ve bunların sınırları açıklanmaktadır.

**Bu sayfada**

- [Bağımsız uygulama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#standalone-application)
- [Paylaşılan araştırmalar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#shared-investigations)
- [Arşivleme araçları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#archive-tools)
- [İsteğe bağlı ekler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#optional-extras)
- [Protokolü ve özel kaynaklar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#protocol-and-private-sources)
- [Birden fazla hesap](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#multiple-accounts)
- [Yakalama ve kaynak gösterme](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#capture-and-attribution)
- [Kapasite ve Telegram sınırları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#capacity-and-telegram-limits)
- [Güvenilirlik ve kurtarma](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#reliability-and-recovery)
- [Kanıt modeli](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#evidence-model)
- [Dışa aktarma, dağıtım ve devretme](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#export-deployment-and-handoff)
- [Kararlı sürüm kriterleri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/#stable-release-criteria)

## Bağımsız uygulama

TgWitness'in kendine ait kurulum süreci, veri dizini ve sürüm yaşam döngüsü vardır. Pakete dahil olan web arayüzü, kurulum ve inceleme işlemlerini yürütür; dışa aktarılan kayıtlar bağımsız olarak kullanılabilir.

Kullanıcı hesaplarını birbirine bağlar, her birinin görebileceği kaynakları seçer ve kaydedilmiş bir gözlem günlüğü elde eder. Panel, içeriği, kaydedilen değişiklikleri, gözlemin kaynağını ve bilinen eksiklikleri gösterir. Başka bir araştırmacı, dışa aktarılan materyali doğrulayabilir.

Panel, hesap yetkilendirmesini, kaynağa erişimi, toplayıcının faaliyetini ve kaydedilen kapsamı birbirinden ayırır. Mesaj sayısının az olduğu bir zaman aralığını veya bir bağlantı sorununu değerlendirirken bu durumları birlikte gözden geçirin.

## Ortak soruşturmalar

Bir yönetici, eylem bazında izinler, IP kısıtlamaları, son kullanma tarihi, oturum açma sınırları ve oturum kontrolü içeren, çalışma alanları ve bireysel sohbetlerle sınırlı [erişim jetonları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) verebilir. Salt okunur bir gözden geçiren, Telegram yetkilendirmesi veya ana panel anahtarı almadan bir vakayı inceleyebilir. Sohbetle sınırlı erişim, hesap genelindeki ayarlardan ve tam günlük dışa aktarımlarından ayrı tutulur.

Otomatik MTProxy, dört kamuya açık kaynaktan veya bir operatör kataloğundan çalışan Telegram rotalarını sürdürür. [IP modları,](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes) bir arıza durumunda başka bir proxy'nin beklenmesi gerekip gerekmediğini veya açıkça izin verilen doğrudan bir rotanın kullanılabileceğini belirler. Harici HTTP istekleri için ayrı bir rota ve devre dışı bırakma seçeneği mevcuttur.

## Arşivleme araçları

[Geçmiş verilerinin toplanması](https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/), [arşiv arama ve analizi](https://phishdestroy.github.io/TgWitness/tr/docs/reference/analysis/),[salt okunur MCP](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/), [yerel OCR/transkripsiyon](https://phishdestroy.github.io/TgWitness/tr/docs/reference/media-analysis/) ve[giden webhook'lar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/webhooks/) 0.7.1 adresinde yer almaktadır. Analitik raporlar ve tanınan metinler, yakalanan olaylardan ayrı tutulur.

[Case Board](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-board/), çalışma alanı içinde kaynağa bağlı yer imleri, alıntılar, notlar ve koleksiyonlar ekler. [Rapor oluşturucu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/), desteklenen HTML/PDF dışa aktarımları için materyali, bölümleri ve sekiz tasarımdan birini seçer.

## İsteğe bağlı ek özellikler

Günlük kurulum şu şekildedir: hesap → kaynaklar → gözlem. **Ekstra özellikler**, bir Telegram tanık botu ve GitHub yakalama önizlemesi içeren ayrı bir bölümdür. Her biri, ayarları göstermeden önce kullanılabilirliğini ve gereksinimlerini belirtir. Bir kart seçildiğinde talimatlar açılır; bu işlem, bir hizmete kaydolma veya hizmeti başlatma anlamına gelmez.

Bot kurulumu üç adımdan oluşur: salt okunur erişim oluşturma, yayın ayarlarını seçme ve witness sunucusunda başlatma. Ağ ve yayın seçenekleri, mevcut bağlantılar ve doğrulama komutları talep üzerine açıklanır. İndirilen yapılandırma, çalışır durumdaki bir Witness'tan farklıdır. Ekstra özellikler arasında geçiş yapıldığında taslak korunur; hesap değişiklikleri ve kilitleme işlemleri geçici jetonu ve formu siler. Yerleşik kılavuzda başlatma talimatları yer alır. [GitHub Actions,](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) fork'unuzdan sabitlenmiş bir toplayıcıyı başlatır, bir sohbeti yakalar ve iş akışı kaynağını içeren şifreli bir aktarım oluşturur.

## Protokol ve özel kaynaklar

**MTProto, Telegram'ın protokolüdür; Telethon ise TgWitness'in MTProto ile iletişim kurmak için kullandığı Python kütüphanesidir.** Bunlar alternatif bağlantı yöntemleri değildir. Toplama işlemi MTProto'yu kullanır; isteğe bağlı tanık ise Bot API aracılığıyla imzalı kontroller yayınlar.

Her çalışma alanı, kendi yetkili istemcisine ve hesap güncelleme akışına sahiptir. TgWitness, yapılandırılmış kaynaklardan gözlemleri seçer ve geçmiş anlık görüntüleri ile medya indirmeleri gibi işlevler için ayrı ve açık isteklerde bulunur.

Özel bir kaynağın herkese açık bir kullanıcı adına ihtiyacı yoktur. Telegram eş tipi ve sayısal kimlik numarası tanımlayıcılardır; unvanlar ve kullanıcı adları değişebilir. Erişim, mevcut üyelik ve izinlere bağlıdır. TgWitness, kaynaklara otomatik olarak katılmamakta veya katılım onayını atlamamaktadır. Başka bir hesaptan alınan erişim hash'i, evrensel bir erişim jetonu değildir.

Toplama modeli, katılım öncesindeki gizli geçmişi, katılımcı/yönetici rolleri, oturum iptali, kaldırma veya değiştirilen izinleri, gruptan süper gruba geçişi, konular/forumlar, bağlantılı tartışmalar, kanal kimlikleri ve erişilemeyen ekleri hesaba katmalıdır. Her kombinasyonun canlı ortamda test edildiği söylenemez.

Kaynak görünürlüğü, toplayıcı başlatıldığında kontrol edilir. Sınırlandırılmış diyalog sonucundan bir kaynağın eksik olması, **erişimin onaylanmadığı** anlamına gelir; kaynağın silindiği kanıtlanmış değildir. Tek bir erişilemeyen kaynak, diğer erişilebilir kaynakların gözlemlenmesini engellemez. Asla davet bağlantılarını veya gerçek oturumları herkese açık ortamlara koymayın.

## Birden fazla hesap

Panel, her biri aşağıdakilere sahip olan sınırsız sayıda **çalışma alanını** destekler:

- Yetkilendirme, şifreli depo ve bağlantı yolu.
- SQLite günlüğü ve Ed25519 imzalama kimliği.
- Seçilmiş kaynaklar, medya kuyruğu ve yakalama ayarları.
- Gözlem durumu, hatalar, kontrol noktaları ve dışa aktarımlar.

Görüntülenen çalışma alanının değiştirilmesi, başka bir toplayıcının çalışmasını durdurmaz. Çalışma alanları arasında hesap yetkilendirmesinin tekrarlanması reddedilir. Zaten bir Telegram hesabına bağlanmış bir günlük, başka bir hesaba yeniden atanamaz; ancak aynı hesabın yeniden bağlanmasına izin verilir. Bu, hesap kimliğini ve ilgili mesaj kimliği kapsamını korur.

Uygulama, sabit bir çalışma alanı sayısı belirlemez. Her çalışma alanı, bağlantı izleme, medya indirmeleri, yeniden kontroller ve yeni sohbet alımları için kendi toplayıcı görevlerini, paylaşılan bir Python süreci ve olay döngüsü içinde çalıştırır. İş hacmi, iş yüküne bağlıdır. Süreç yalıtımı için ayrı kurulumlar, bağlantı noktaları ve veri dizinleri kullanın.

Her hesaba erişebileceği kaynakları atayın. Farklı hesaplar aynı grubu gözlemleyebilir, ancak gözlemleri ayrı kalır ve kaynakları korunur. Bir operatör tarafından kontrol edilen makinedeki iki hesap, iki bağımsız tanık değildir. **Dışa aktarma işlemi** , ayrı ayrı imzalanmış çalışma alanı ZIP dosyalarını, bunların çalışma alanı kimliklerini, hash değerlerini ve imza anahtarı parmak izlerini içeren imzalı bir dosya listesiyle bir araya getirir. Her günlük kendi sınırlarını korur. Vaka notlarında veya analiz araçlarında, bu kaynak referanslarını koruyarak çalışma alanları arası birleşik bir zaman çizelgesi oluşturun.

## Kaydetme ve kaynak gösterme

Kaynaklar, yeni mesajlar, düzenlemeler, silme işlemleri, tepkiler ve üyelik için hesap başına anahtarlar sağlar. Ön ayarlar, tüm kategorileri veya mesajları/düzenlemeleri/silme işlemlerini korur. Politika, çalışma alanındaki seçili gruplar için geçerlidir, yeniden başlatma işleminden sonra da devam eder ve değişikliklerden önceki ve sonraki halleriyle imzalanır. Varsayılan ayarlar tüm kategorileri korur. Bir kategoriyi devre dışı bırakmak eski kayıtları silmez; tekrar etkinleştirmek ise kaçırılan olayları geri getirmez. Operasyonel kayıtlar, diğer grup hizmeti olayları ve açık geçmiş anlık görüntüleri ayrıdır. Yakalanan Telegram nesneleri, ayrı güncelleme ayarlarından bağımsız olarak gömülü meta verileri koruyabilir. Henüz grup bazında kategori geçersiz kılma seçeneği bulunmamaktadır.

| Materyal | Şu anda kaydediliyor | Sınır |
| --- | --- | --- |
| Mesaj | Metin, eş/mesaj kimlikleri, gönderen meta verileri, yanıtlar ve orijinal güncelleme zarfı | Toplayıcı tarafından imzalanmış, hesap tarafından görülebilen bir gözlem olarak korunur |
| Düzenle | Gözlemlenen yeni sürüm ve daha önce kaydedilmiş tüm sürümler | Hizmet kesintisi sırasında yapılan ara düzenlemeler kaybolabilir; gönderenin mutlaka düzenleyici olduğu söylenemez. |
| Silme | Bildirim ve varsa önceden yakalanan içerik | Genellikle silen kişi veya kesin eylem zamanı belirtilmez |
| Hesap düzeyinde silme bildirimi | Orijinal bildirim; çözülmüş kayıtlar, kaydedilmiş sohbeti ve korelasyon yöntemini içerir | Kapsamda tam olarak bir adet önceden kaydedilmiş özel sohbet veya normal grup eşleşmesi bulunmalıdır; diğer kimlikler “`deletion.unscoped`” olarak kalır. Kanal ve süper grup kimlikleri bu eşleştirme kapsamı dışında tutulur. |
| Tepki | Saçma sayıları ve görünür son kimlikler | Elde edilebilir tam reaktör listesi için ayrı sorgular gerekir; kanallar kimlikleri gizleyebilir |
| Üyelik | Hizmet mesajları ve katılımcılara gönderilen güncellemeler | Görünürlük, role ve sohbet türüne bağlıdır; eksik olaylar, yokluğu kanıtlamaz |
| Yönetici işlemleri | İlgili teslim edilen güncellemeler ve kanal/süper grup sohbeti dışa aktarımlarında bir yönetici günlüğü anlık görüntüsü | Dışa aktarma işlemi, dışa aktarma yetkisine sahip yönetici hesabı için mevcut olduğunda günlüğü okur; yönetici günlüğünün sürekli olarak taranması bu yolun dışındadır. |
| Ek | Orijinal sürüm tanımlayıcısı, indirilen bayt sayısı/SHA-256 ve deneme sonuçları | Silinen bir dosya geri kazanılamayabilir; en son sürüm bunun yerine geçmez |
| Tarihçe | O anda görünür olan mesajların açık bir anlık görüntüsü | Tüm düzenlemeleri veya silinen içeriği yeniden oluşturmaz |
| Toplayıcı süreci | Başlatma/durdurma, kalp atışı, hatalar, ayarlar, kapsam ve imzalı çalıştırma makbuzu | Yerel envanter; GitHub ve TDX, ['dan bağımsız ortam denetimleri ekledi](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) |

Arayüz, kaynak olayda belirtilen hesabı adlandırır ve gözlemlenen adları ve kullanıcı adlarını korur. Olayda fail belirtilmediğinde, rapor bu alanı boş bırakır.

## Kapasite ve Telegram sınırları

Garantili kaliteyle izlenebilecek sohbet sayısı konusunda evrensel bir rakam yoktur. Kapasite, saniye başına en yoğun olay sayısı, eklerin hacmi ve boyutları, ek RPC'ler, aktif hesaplar, disk gecikmesi/boş alan, ağ koşulları, Telegram sınırları, kabul edilebilir gecikme süresi ve kuyruk derinliğine bağlıdır.

Telegram, pasif iletim ile aktif kısa sorgulamayı birbirinden ayırır. Güncelleme belgelerinde, açık kanallar/süper gruplar için ek `updates.getChannelDifference` çağrıları açıklanmakta ve **aynı anda** en fazla **on kısa sorgulanan kaynağın** kullanılması önerilmektedir. Bu, seçilen grupların sayısının on ile sınırlı olduğu veya eksiksizlik garantisi olduğu anlamına gelmez.

| Mod | Amaç | Durum |
| --- | --- | --- |
| Standart gözlem | Seçilen kaynaklardan gelen güncellemeleri kaydetme | Uygulandı |
| Öncelikli yeniden kontroller | Yıldızlı kaynaklar kendi yapılandırılabilir aralıklarını kullanır ve her sınırlı yeniden kontrol aşamasında öncelik kazanır. | Geçmiş ve mesaj sorguları ile uygulanmıştır |

Öncelik yıldızı bu yeniden kontrolleri yönetir. Ek `updates.getChannelDifference` kısa sorgulama işlevi, ayrı bir kullanıcı modu olarak sunulmaz.

FloodWait'i göz ardı eden veya ek hesaplardan gelen kapasitenin doğrusal olduğunu varsayan keyfi yüksek frekanslı sorgulama, geçerli bir boyutlandırma modeli değildir. Varsayılan sınırlar şunlardır: listelenen ilk 1.000 diyalog, geçmiş anlık görüntüsü başına en fazla 500 mesaj, türüne göre toplanan her dosya için 1–2.000 MiB ve sıkıştırılmamış imzalı ZIP içeriği için 4 GiB’dir; bunların her biri **Parametreler** altından çalışma alanı başına değiştirilebilir. Dışa aktarmalarda sabit bir olay sayısı sınırı yoktur. Tarayıcı yedeği varsayılan olarak 128 MiB ile sınırlıdır; akış CLI’sinde yapılandırılabilir bir aktarım sınırı vardır ve varsayılan değer 5 GiB’dir.

## Güvenilirlik ve kurtarma

Uygulanan davranışlar arasında SQLite WAL/senkron işlemler; atomik mesaj ve medya işi yazma işlemleri; kalıcı işler ve yeniden deneme gecikmeleri; orijinal sürüm tanımlayıcıları; sınırlı yeniden denemeler; kalıcı medya FloodWait; metin olayının ağ bekleme süresi dışındaki medya indirmeleri; sonraki yazma işlemleri devam ederken kararlı önekli dışa aktarmalar; atomik ayarlar ve denetim kayıtları; başarısız yedek oturum açma sonrasında çalışma yetkisinin korunması; hasarlı ek çalışma alanının yalıtılması; açık yeniden bağlanma denemeleri; belirgin yetki kaybı raporlaması; ve monotonik saat kullanılarak gerçek zamanlı değişiklik algılama.

Hesap ve kanal pts/qts/seq değerleri kaydedilir ve yeniden başlatma sonrasında devam ettirilir; izlenen sohbetler periyodik olarak yeniden kontrol edilir; [kanıt formatına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#durable-collection-and-process-receipts-02) bakınız. Konumun periyodik olarak kaydedilmesi, günlüğün kabul edildiğine dair atomik ve kayıpsız bir onay değildir.

Her işlem başlangıcı, önceki başlığı ve çevrimdışı sınırını kaydeder. Mevcut geçmiş boşluk onarımı olarak değerlendirilmez. Telegram'ın veri saklama kapasitesi sınırlıdır; `differenceTooLong`, kaybolan tüm içeriği yeniden oluşturamaz. Kurtarılamayan boşluklar, daha sonraki bir geçmiş anlık görüntüsü başarılı olsa bile açıkça belirtilmelidir.

## Kanıt modeli

Her olay, bir sıra numarası, yerel UTC gözlem zamanı, varsa kaynak zamanı, türü, kaynağı, varsa aktör bilgisi, orijinal veri yükü, önceki hash değeri ve imzayı kaydeder. Mesaj gözlemleri ayrıca toplayıcı hesabı/çalıştırma bağlamını da saklar.

İmzalı işlem makbuzu, rastgele bir çalıştırma kimliği; TgWitness/Python/OS/bağımlılık sürümleri; kaynak dosya SHA-256 değerleri ve toplu parmak izi; başlangıç hesabı, kapsam ve ayarlar; UTC/monotonik okumalar; ve önceki günlük başlığını içerir. Ayar değişiklikleri, başlatma/durdurma işlemleri ve hatalar aynı günlüğe kaydedilir. Kontrol noktaları, başlangıçta, gözlem sırasında her beş dakikada bir (değiştirilebilir) ve düzgün bir şekilde durdurulduğunda saklanır. Saklanan bir yerel kontrol noktası, daha önceki bir günlük önekine geri dönüşü tespit edebilir.

| Çalışma Mekanizması | Neyi ortaya koyar? |
| --- | --- |
| Dosya SHA-256 | Baytlar, bilinen bir özetle eşleşiyor |
| Olay hash zinciri | Bilinen bir sınırla ilişkili olarak sıralama/bağlantı kaydı |
| Ed25519 | Belirli bir anahtarla imzalanmış |
| Bağımsız olarak tutulan kontrol noktası | Daha sonraki içerik, korunan sınırlarla uyumludur |
| Program dosyası boyutu | Ölçülen dosyalar hakkında toplayıcının kendi raporu |
| Geçerli bağımsız TSA yanıtı | Açık güven varsayımları altında TSA zamanına göre belirli baytların varlığı |

RFC 3161 istek hazırlığı ve OpenSSL yanıt doğrulaması uygulanmaktadır. Kanıt modu ayrıca kontrol noktası hash'lerini yapılandırılmış zaman damgası hizmetlerine gönderir. Bağımsız bir zaman referansı oluşturmak için yetkili kurumun yanıtını saklayın ve doğrulayın. [TIMESTAMP.md dosyasına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/) bakın.

Kontrol noktalarını bağımsız olarak saklayın, imzalama anahtarlarına erişimi kontrol edin, aktarım kayıtlarını tutun ve dışa aktarımları güvenilir yazılımlarla doğrulayın. [Doğrulama kapsamı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) , bu kontrollerinin birbirini nasıl tamamladığını ve hangi güven varsayımlarının geçerli olduğunu açıklar.

## Dışa aktarma, devreye alma ve devretme

İmzalı bir ZIP dosyası, orijinal JSONL, CSV, HTML dosyalarını, korunmuş ekleri, hash değerlerini, imzalı bir manifestoyu ve kullanışlı bir doğrulama aracını içerir. Tek bir çalışma alanını ve sabit bir tam günlük önekini kapsar. Panel arama filtreleri, kayıtları sessizce silmez. Gizli anahtarlar, token'lar ve Telegram oturumları hariç tutulur; orijinal gözlemler yine de kişisel bilgiler ve Telegram meta verileri içerebilir.

ZIP özetini, güvenilir parmak izini, kontrol noktasını, işlem makbuzunu ve devir kayıtlarını ayrı ayrı saklayın. Yalnızca incelenen ZIP dosyasında yer aldığı için yürütülebilir koda güvenmek yerine, güvenilir bir kurulumdan gelen bir doğrulayıcı kullanın.

Tarayıcı arayüzü, Node.js, CDN'ler veya harici yazı tipleri olmadan yerel olarak dağıtılır. Tek bir operatör jetonu kurulumu kontrol eder. Uzaktan erişim için HTTPS veya bir SSH tüneli gereklidir. Yerel Python ve konteyner tanımları sağlanır; [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) dizininde hizmet örnekleri bulunur; gerçekleştirilen platform kontrolleri ayrı olarak listelenir.

Varsayılan çalışma alanı veri kökünü kullanır; ek çalışma alanları ise `profiles/<id>/`'yi kullanır. Yedekleme için işlemin durdurulması ve eksiksiz veri/anahtar seti gereklidir. Kanıt ZIP dosyaları, uygulama yedeklemeleri değildir. Gizli veriler, yeni bir veri dizini için harici bir ana anahtar kullanabilir; günlük/medya şifreleme, operatörün diski/birimi tarafından sağlanır. [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/) ve [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/operations/) dosyalarına bakınız.

## Kararlı sürüm kriterleri

Kararlı sürüm yayınlanmadan önce şu açıklamayı ekleyin:

1. Üye/yönetici rolleri ve gizli/görünür geçmişi olan gerçek özel gruplar, süper gruplar, forumlar ve kanallar; bunlara giriş/2FA, iptal ve erişim kaybı da dahildir.
2. Bilinen eylemler karşısında yapılan kontrollü düzenlemeler, silme işlemleri, tepkiler, üyelik bilgileri ve medya içerikleri.
3. İşlem/sunucu çökmeleri, disk arızaları/disk dolması, süresi dolmuş dosya referansları, FloodWait, ağ bağlantısı kesilmesi, bozuk dosyalar ve veritabanı geri alma.
4. Ölçülen gecikme, kuyruklar, bellek ve disk ile sürekli çoklu hesap kullanımı; buna hem sessiz hem de gürültülü kaynaklar dahildir.
5. MTProto durum ilerlemesi ile günlük kaydı kabulü arasında bir kesinti.
6. Hedeflenen işletim sistemi/konteyner matrisinde sorunsuz kurulum ve doğrulanmış yedekleme geri yüklemesi.
7. Güvenlik, imzalar ve atıf/kanıt iddialarına ilişkin bağımsız inceleme.

Kapsamlı panel erişimi, [erişim ve izinler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) bölümünde açıklanmıştır. 0.6 sürümü, [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) dosyasında açıklanan sınırlı tek hesaplı TData ve hesap dosyası içe aktarmasını destekler. Yayınlamadan önce Telegram API şartlarını gözden geçirin. Araştırma referansları ve platform bulguları [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md) dosyasında yer almaktadır.
