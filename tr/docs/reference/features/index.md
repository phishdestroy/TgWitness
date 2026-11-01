# Özellikler ve sınırlamalar

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/

TgWitness'in şu anda uyguladığı özellikler, Telegram platformunun getirdiği kısıtlamalar ve gelecekte yapılması gereken çalışmalar.

Tasarım referansı: 26 Ekim 2026. Başlıca kullanım senaryosu, bağlı hesapların erişebildiği özel Telegram grupları ve kanallarıdır. Bu belge, uygulanmış davranışları, platform sınırlarını ve gelecekteki çalışmaları birbirinden ayırır. Bir hedef mimari öğesi, söz konusu özelliğin halihazırda mevcut olduğu iddiası değildir.

## Bağımsız uygulama

TgWitness'in kendine ait kurulum süreci, veri dizini ve sürüm yaşam döngüsü vardır. Pakete dahil olan web arayüzü, kurulum ve inceleme işlemlerini yürütür; dışa aktarılan kayıtlar bağımsız olarak kullanılabilir.

Kullanıcı hesaplarını birbirine bağlar, her birinin görebileceği kaynakları seçer ve kaydedilmiş bir gözlem günlüğü elde eder. Panel, içeriği, kaydedilen değişiklikleri, gözlemin kaynağını ve bilinen eksiklikleri gösterir. Başka bir araştırmacı, dışa aktarılan materyali doğrulayabilir.

Dört farklı durum önemlidir: hesap yetkilendirmesi, kaynağa erişim, çalışan bir toplayıcı ve iletimin eksiksizliğinin ne ölçüde tespit edildiği. İlk üçünün hiçbiri dördüncüyü otomatik olarak kanıtlamaz. Sessiz bir grup, mutlaka başarısız bir toplayıcı anlamına gelmez.

## Ortak soruşturmalar

Bir yönetici, yedi izin seviyesi, IP kısıtlamaları, son kullanma tarihi, oturum açma sınırları ve oturum kontrolü ile çalışma alanlarına ve bireysel sohbetlere özel [erişim jetonları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) verebilir. Salt okunur bir denetçi, Telegram yetkilendirmesi veya ana panel anahtarı almadan bir vakayı inceleyebilir. Sohbetle sınırlı erişim, hesap genelindeki ayarlardan ve tam günlük dışa aktarımlarından ayrı tutulur.

Otomatik MTProxy, dört kamuya açık kaynaktan veya bir operatör kataloğundan çalışan Telegram rotalarını sürdürür. [IP modları,](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes) bir arıza durumunda başka bir proxy'nin beklenmesi gerekip gerekmediğini veya açıkça izin verilen doğrudan bir rotanın kullanılabileceğini belirler. Harici HTTP istekleri için ayrı bir rota ve devre dışı bırakma seçeneği mevcuttur.

## Arşivleme araçları

[Geçmiş verilerinin toplanması](https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/), [arşiv arama ve analizi](https://phishdestroy.github.io/TgWitness/tr/docs/reference/analysis/),[salt okunur MCP](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/), [yerel OCR/transkripsiyon](https://phishdestroy.github.io/TgWitness/tr/docs/reference/media-analysis/) ve[giden webhook'lar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/webhooks/) 0.7.1 adresinde yer almaktadır. Analitik raporlar ve tanınan metinler, yakalanan olaylardan ayrı tutulur.

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

Sabit bir sayı veya ölçülmüş iş hacmi garantisi yoktur. Çalışma alanları, bir Python süreci ve olay döngüsünü paylaşır. Ayrı hesap işleyicileri, gelecekte gerçekleştirilecek bir çalışmadır. Mevcut süreç yalıtımı için ayrı kurulumlar, bağlantı noktaları ve veri dizinleri kullanın.

Her hesaba erişebileceği kaynakları atayın. Farklı hesaplar aynı grubu gözlemleyebilir, ancak gözlemleri ayrı kalır ve kaynakları korunur. Tek bir operatör tarafından kontrol edilen makinede bulunan iki hesap, iki bağımsız tanık sayılmaz. Dışa aktarımlar çalışma alanı bazında yapılır; birleştirilmiş vaka paketi veya genel Telegram zaman çizelgesi özelliği uygulanmamaktadır.

## Kaydetme ve kaynak gösterme

Kaynaklar, yeni mesajlar, düzenlemeler, silme işlemleri, tepkiler ve üyelik için hesap başına anahtarlar sağlar. Ön ayarlar, tüm kategorileri veya mesajları/düzenlemeleri/silme işlemlerini korur. Politika, çalışma alanındaki seçili gruplar için geçerlidir, yeniden başlatma işleminden sonra da devam eder ve değişikliklerden önceki ve sonraki halleriyle imzalanır. Varsayılan ayarlar tüm kategorileri korur. Bir kategoriyi devre dışı bırakmak eski kayıtları silmez; tekrar etkinleştirmek ise kaçırılan olayları geri getirmez. Operasyonel kayıtlar, diğer grup hizmeti olayları ve açık geçmiş anlık görüntüleri ayrıdır. Yakalanan Telegram nesneleri, ayrı güncelleme ayarlarından bağımsız olarak gömülü meta verileri koruyabilir. Henüz grup bazında kategori geçersiz kılma seçeneği bulunmamaktadır.

| Materyal | Şu anda kaydediliyor | Sınır |
| --- | --- | --- |
| Mesaj | Metin, eş/mesaj kimlikleri, gönderen meta verileri, yanıtlar ve orijinal güncelleme zarfı | Mesaj için kamuya açık olarak doğrulanabilir bir Telegram imzası yok |
| Düzenle | Gözlemlenen yeni sürüm ve daha önce kaydedilmiş tüm sürümler | Hizmet kesintisi sırasında yapılan ara düzenlemeler kaybolabilir; gönderenin mutlaka düzenleyici olduğu söylenemez. |
| Silme | Bildirim ve varsa önceden yakalanan içerik | Genellikle silen kişi veya kesin eylem zamanı belirtilmez |
| Kapsam dışı silme | Karşı tarafı tahmin etmeden, orijinal hesap düzeyinde bildirim | Daha önce kaydedilmiş hesap kapsamındaki kimlik numaralarıyla sıkı bir korelasyon sağlanması, gelecekte ele alınacak bir konudur. |
| Tepki | Saçma sayıları ve görünür son kimlikler | Elde edilebilir tam reaktör listesi için ayrı sorgular gerekir; kanallar kimlikleri gizleyebilir |
| Üyelik | Hizmet mesajları ve katılımcılara gönderilen güncellemeler | Görünürlük, role ve sohbet türüne bağlıdır; eksik olaylar, yokluğu kanıtlamaz |
| Yönetici işlemleri | Yalnızca ilgili güncellemeler sunulur | Ayrı bir yönetici günlüğü sorgulama özelliği uygulanmamıştır |
| Ek | Orijinal sürüm tanımlayıcısı, indirilen bayt sayısı/SHA-256 ve deneme sonuçları | Silinen bir dosya geri kazanılamayabilir; en son sürüm bunun yerine geçmez |
| Tarihçe | O anda görünür olan mesajların açık bir anlık görüntüsü | Tüm düzenlemeleri veya silinen içeriği yeniden oluşturmaz |
| Toplayıcı süreci | Başlatma/durdurma, durum kontrolü, hatalar, ayarlar, kapsam ve program alımı | Kendi beyanına dayalı, bağımsız bir süreç doğrulaması değildir |

Bir eylem, yalnızca kaynak o kişiyi gerçekten belirtmişse o kişiye atfedilir. Aksi takdirde arayüz, atıf eksikliğini bildirir. Kullanıcı adları ve isimler, gözlemlenen özelliklerdir; gerçek dünyadaki kimliğin kanıtı değildir.

## Kapasite ve Telegram sınırları

Garantili kaliteyle izlenebilecek sohbet sayısı konusunda evrensel bir rakam yoktur. Kapasite, saniye başına en yoğun olay sayısı, eklerin hacmi ve boyutları, ek RPC'ler, aktif hesaplar, disk gecikmesi/boş alan, ağ koşulları, Telegram sınırları, kabul edilebilir gecikme süresi ve kuyruk derinliğine bağlıdır.

Telegram, pasif iletim ile aktif kısa sorgulamayı birbirinden ayırır. Güncelleme belgelerinde, açık kanallar/süper gruplar için ek `updates.getChannelDifference` çağrıları açıklanmakta ve **aynı anda** en fazla **on kısa sorgulanan kaynağın** kullanılması önerilmektedir. Bu, seçilen grupların sayısının on ile sınırlı olduğu veya eksiksizlik garantisi olduğu anlamına gelmez.

| Mod | Amaç | Durum |
| --- | --- | --- |
| Standart gözlem | Seçilen kaynaklardan gelen güncellemeleri kaydetme | Uygulandı |
| Öncelikli gözlem | Sınırlı bir kaynak kümesi için ek farklılık kontrolleri | Kullanıcı modu olarak uygulanmamıştır |

FloodWait'i göz ardı eden veya ek hesaplardan gelen kapasitenin doğrusal olduğunu varsayan keyfi yüksek frekanslı sorgulama, geçerli bir boyutlandırma modeli değildir. Varsayılan sınırlar şunlardır: listelenen ilk 1.000 diyalog, geçmiş anlık görüntüsü başına en fazla 500 mesaj, türüne göre toplanan her dosya için 1–2.000 MiB ve sıkıştırılmamış imzalı ZIP içeriği için 4 GiB’dir; bunların her biri **Parametreler** altından çalışma alanı başına değiştirilebilir. Dışa aktarmalarda sabit bir olay sayısı sınırı yoktur. Tarayıcı yedeği varsayılan olarak 128 MiB ile sınırlıdır; akış CLI’sinde yapılandırılabilir bir aktarım sınırı vardır ve varsayılan değer 5 GiB’dir.

`tools/check_capacity.py`, yerel sentetik veri alımı ve dışa aktarımını ölçer. Sonuçları, Telegram teslimat ölçümleri veya garantili gerçek sohbet sayısı değildir. Ölçülen sürüm ve iş yükü için [VERIFICATION.md dosyas](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/)ına bakınız.

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

RFC 3161 istek hazırlığı ve OpenSSL yanıt doğrulaması uygulanmaktadır. Otomatik gönderim ise uygulanmamaktadır. Makinenin saatini içeren bir istek veya yerel imza, bağımsız bir zaman damgası değildir. [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/) dosyasına bakınız.

Toplayıcıyı ve imzalama anahtarını kontrol eden bir operatör, yeni imzalı gözlemler uydurabilir. İmzalar, Telegram'ın kaynağını, doğruluğunu veya otomatik yasal kabul edilebilirliğini kanıtlamaz. Daha güçlü bir saklama süreci için bağımsız kontrol noktaları/zamanlı depolama, anahtar erişim kontrolleri, aktarım kayıtları ve güvenilir yazılımlar tarafından doğrulama gereklidir.

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

Yönetici günlüğü sorgulama, ek reaktör listeleri, öncelikli sorgulama, ayrı işleyiciler ve uygulama genelinde şifreleme, gelecekte gerçekleştirilecek işler arasında yer almaktadır. Kapsamlı panel erişimi, [erişim ve izinler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) bölümünde açıklanmaktadır. 0.6 sürümü, [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) dosyasında açıklanan sınırlı tek hesaplı TData ve hesap dosyası içe aktarmayı desteklemektedir. Yayınlamadan önce Telegram API şartlarını gözden geçirin. Araştırma referansları ve platform bulguları [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md) dosyasında yer almaktadır.
