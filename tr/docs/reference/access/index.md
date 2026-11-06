# Erişim ve izinler

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/

Hesaplara ve sohbetlere kısıtlı erişim izni verin, izinleri seçin, oturumları ve IP adreslerini sınırlayın ve erişimi iptal edin.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Başlangıç](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/)

![Başlangıç](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

Bir gözden geçiren kişiye bir sohbet erişimi, bir analiste bir vakayı dışa aktarma izni veya bir operatöre seçilen hesaplar üzerinde kontrol hakkı verin. Her kişi kendi jetonuna sahip olur. Ana panel jetonu ise yöneticiye aittir.

[Hesap kurulumu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) · [Bağlantı yolları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/) · [Güvenlik modeli](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/)

## İki kapsam, iki farklı görev

**Toplama kapsamı**, bir hesabın neleri kaydedeceğini belirler: seçilen sohbetler, bir Telegram klasörü veya hesabın tamamı. **Erişim kapsamı ise,** kaydedilen bu hesap ve sohbetlerden hangilerinin başka bir kişi tarafından görülebileceğini ve kullanılabileceğini belirler. Erişim izni vermek, bir Telegram sohbetine katılmak, toplama işlemini başlatmak veya Telegram hesabı izinleri vermek anlamına gelmez.

Bir erişim izni, seçilen çalışma alanlarını, bunların içindeki seçilen sohbetleri, tüm çalışma alanlarını veya bir [hesap](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#bulk-import-and-account-groups)grubundaki tüm hesapları açabilir. **Tüm çalışma alanları, daha sonra eklenenler de dahil olmak üzere**, gelecekteki hesapları da kapsar. Bir grup erişimi de o gruba daha sonra eklenen hesapları kapsar. Bir vakanın yalnızca belirli çalışma alanlarıyla sınırlı kalması gerektiğinde, bu çalışma alanlarını açıkça seçin.

## Birine erişim izni verin

1. Ana yönetici olarak oturum açın ve "**Erişim" bölümünü** açın.
2. "**Birine erişim izni ver**" bölümüne, günlüğünde tanıyabileceğiniz bir isim girin.
3. Çalışma alanlarını ve gerektiğinde bireysel sohbetleri seçin.
4. Bu kişinin yapabileceklerini seçin. "**Görüntüle" seçeneği** her zaman dahil edilir.
5. Gerektiği şekilde geçerlilik süresini, oturum açma/oturum sınırlarını ve izin verilen adresleri ayarlayın.
6. **"Erişim Oluştur" düğmesine** basın. Jetonu hemen kopyalayın: bu jeton yalnızca bir kez görüntülenir.
7. Panel adresini ve jetonu özel olarak gönderin. Alıcı, bu jetonu normal oturum açma sayfasına girer; ana panel jetonunuza veya bir Telegram oturumuna ihtiyacı yoktur.

Verilen jetonu içeren paneli ayrı bir tarayıcı oturumunda açın ve teslim etmeden önce görünür sohbetleri ve izin verilen işlemleri kontrol edin.

## İzinleri seçin

Yalnızca metin içeren halka açık bir tanıtım için, sıradan inceleme erişimi yerine **Halka Açık Tanıtım'ı** kullanın. Bu özellik, açıkça seçilmiş halka açık kanalları, saklanan düzenlemeleri ve silme işlemlerini ve imzalanmış istatistikleri gösterir; yazar alanları gizlenir ve dosyalar API sınırında kapatılır. [Bir tanıtım oluşturun ve doğrulayın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/showcase/).

| İzin | Neleri sağlar? |
| --- | --- |
| `view` | İzin verilen sohbetleri, yakalanan mesajları, profilleri, dosyaları ve filtrelenmiş günlük kayıtlarını okuyun. Her zaman dahildir. |
| `export` | İzin verilen sohbet geçmişini ve dosyaları dışa aktarın. Tüm çalışma alanına ait kanıtların dışa aktarılması için çalışma alanının tamamına erişim gerekir. |
| `sources` | Kaynakları, anlık görüntüleri ve profil yakalamayı yönetin. Sohbet sınırlı erişim yalnızca izin verilen sohbetlerde işlem yapabilir; hesap genelinde kaynak keşfi ve kapsam ayarları kapalı kalır. |
| `collect` | Bir toplayıcıyı başlatın veya durdurun. Toplama işlemi hesabı etkilediği için tüm çalışma alanına erişim gerektirir. |
| `interact` | Erişim kapsamı dahilinde desteklenen Telegram etkileşimlerini gerçekleştirin. Sohbetle sınırlı erişimde, hesap genelinde bağlantı önizlemeleri kullanılamaz. |
| `settings` | Toplama ayarlarını, zaman damgalarını, bildirimleri, site dışı kopyaları ve parametreleri değiştirin. Tüm çalışma alanına erişim gerektirir. |
| `account` | Telegram'da oturum açın veya kapatın ve bağlantı yollarını yönetin. Tüm çalışma alanına erişim gerektirir. |
| `board.read` | Vaka Panosu notlarını yalnızca izin verilen çalışma alanı ve sohbetler içinde okuyun. |
| `board.write` | Yer imleri, vurgulamalar, kesitler, yorumlar ve açma/inceleme durumları ekleyin. Ayrıca `board.read`'e de ihtiyaç duyar. |
| `board.manage` | Koleksiyonları, nihai ekip durumlarını ve diğer katılımcıların kartlarını yönetin. Ayrıca yönetim kurulunda okuma/yazma yetkisi gereklidir. |

İzinler ve kapsam birlikte kontrol edilir. Bir izni işaretlemek, diğer sohbetleri açmaz veya sohbetle sınırlı erişim durumunda çalışma alanı genelinde bir işlemi etkinleştirmez. Paralel bir dışa aktarım için, erişim seçilen her hesapta dışa aktarılan sohbeti kapsamalıdır. Verilen bir erişim, yeni erişimler oluşturamaz, başkalarının oturumlarını yönetemez veya yönetici konsolunu açamaz.

### Üç faydalı kurulum

| Kişi | Kapsam | İzinler |
| --- | --- | --- |
| İnceleme Yapan Kişi | Bir vakanın kaydedilmiş sohbetleri | `view` |
| Devir teslim hazırlığı yapan analist | Araştırılacak ve dışa aktarılacak sohbetler | `view`, `export`; yalnızca Telegram üzerinden hareket etmeleri gerekiyorsa `interact`'yi ekleyin |
| Toplama operatörü | Seçilmiş tüm çalışma alanları | `view`, `sources`, `collect`; `settings` veya `account`'yi yalnızca gerektiğinde ekleyin |

Access formunun başlangıç ön ayarları arasında Case Board da bulunur: Gözden Geçirici okuyabilir, Analist okuyabilir ve yazabilir, Operatör ise yönetebilir. Ön ayarlar düzenlenebilir durumda kalır ve mevcut izinler otomatik olarak genişletilmez. Devralınan sohbet kapsamları ve dışa aktarma gizliliği için [Case Board'a](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-board/) bakın.

## Sınırlar ve oturumlar

| Ayarlar | Nasıl çalışır? |
| --- | --- |
| Paralel oturumlar | Eşzamanlı oturum sayısını 1–100 ile sınırlayın. Sınıra ulaşıldığında, bir sonraki oturum açma girişimini reddedin veya en eski oturumu sonlandırın. |
| Girişlere izin verilir | Oturum başlatmak için jetonun başarılı kullanım sayısını sınırlayın. Son izin verilen oturum açma hakkı kullanılmış olsa bile mevcut oturumlar sona ermez. |
| Geçerlilik süresi | Erişim için kesin bir son kullanma tarihi vardır. Süresi dolmuş erişim, oturum açamaz veya istek göndermeye devam edemez. |
| Etkinlik olmayan dakikalar | Oturum hareketsizlik zaman aşımı süresi, 5 dakikadan 30 güne kadar. Başarılı istekler bu süreyi uzatır; açık bir panel, yoklama yaparak kendini aktif tutabilir. |
| İzin verilen adresler | Belirli IP adreslerini veya CIDR alt ağlarını kabul edin. İlk oturum açma bağlaması etkinleştirilmedikçe, herhangi bir adrese izin vermek için bu alanı boş bırakın. |
| İlk oturum açışa bağla | İlk başarılı oturum açma işlemi, o erişim için izin verilen adresi sabitler. |

IP, uygulama tarafından görülen istemci adresidir. Ters proxy veya tünel arkasında iseniz, IP kurallarına güvenmeden önce **Açık oturumlar** bölümünde gösterilen adresi kontrol edin: aksi takdirde, birkaç kullanıcı proxy adresini paylaşıyormuş gibi görünebilir.

## Erişimi değiştirme veya geri çekme

**"Verilen erişim**" altındaki bir girişi düzenleyerek kapsamını, izinlerini veya sınırlarını değiştirebilirsiniz. Kapsam ve izin değişiklikleri, halihazırda açık olan oturumlardan gelen istekler de dahil olmak üzere sonraki isteklerde kontrol edilir. Bir erişimin iptal edilmesi, ilgili oturumları sonlandırır ve verilen jetonu kullanılamaz hale getirir. **Açık oturumlar özelliği** ayrıca, yöneticinin tüm erişimi iptal etmeden tek bir oturumu sonlandırmasına olanak tanır.

Kaydedilen dışa aktarım kopyaları, oluşturucusunu, çalışma alanını, sohbet kapsamını ve gerekli izinleri korur. Erişim izni verilen bir kullanıcı, yalnızca bu izinler geçerli olduğu sürece kendi kopyalarını listeleyebilir veya indirebilir; Case Board içeren kopyalar için ayrıca `board.read` izni gereklidir. Yönetici tüm kopyaları alabilir. Bu meta verileri ve grup paketlerini içermeyen eski kopyalar yalnızca yönetici tarafından erişilebilir. İndirme biletleri ve hazırlanmış dosya yanıtları, dosya hazırlandıktan sonra, baytları gönderilmeden önce erişimi yeniden kontrol eder.

İptal işlemi, birinin daha önce indirdiği dosyaları geri getiremez. Oturumu kapatmak, paneli kilitlemek veya oturumu sonlandırmak, çalışmakta olan toplayıcıyı durdurmaz.

## Yöneticinin görebileceği bilgiler

İnceleme uzmanları ve analistler, proxy uç noktaları, havuz tanılama bilgileri, sunucu yolları veya ham bağlantı hataları içermeyen veri toplama ilerleme raporlarını alırlar. Bağlantı tanılama işlemleri, tüm çalışma alanı üzerinde `account` izni gerektirir. Bildirim okuma, site dışı kopyalama ve parametre ayarları için `settings` izni gereklidir.

Tarayıcıdaki tam User-Agent dizeleri erişim oturumlarında saklanmaz. Bir yükseltme işlemi de bunları değiştirilebilir oturum önbelleğinden siler. Panel işlem günlüğü, IP adreslerini, URL kimlik bilgilerini ve etiketli gizli bilgileri maskeler. Yerel hizmet günlükleri ve daha önce imzalanmış günlük kayıtları yeniden yazılmaz. Erişim kuralları ve imzalanmış oturum açma kayıtları hâlâ istemci adresini kullanır.

### Ana anahtarı değiştirin

**Access → Sınırlarım →** yönetici anahtarını yeniden oluştur seçeneğini kullanın veya panel çalışırken yönetilen bir kurulumdan `tgwitness token rotate` komutunu çalıştırın. Meslektaş jetonlarıyla açılan oturumlar da dahil olmak üzere tüm mevcut tarayıcı oturumları sona erer. İsteği gönderen tarayıcı yeni bir oturum alır; yeni yönetici anahtarını gizlemeden önce kaydedin. Verilen meslektaş jetonları, ayrı olarak iptal edilene kadar geçerliliğini korur. `TGWITNESS_TOKEN` komutunu kullanan bir kurulumda, söz konusu ortam ayarının değiştirilmesi ve sistemin yeniden başlatılması gerekir.

### İstek ve proxy sınırları

API, her istemci IP'si başına dakikada en fazla 600 istek kabul eder. Bir dakika içinde on adet reddedilen kimlik doğrulama, bir saniyeden beş dakikaya kadar uzayan üstel bir bekleme süresini başlatır. Bekleme süresi dolduktan sonra yapılan başarısız bir deneme, bu süreyi uzatır; başarısız deneme yapılmayan on dakika sonunda süre artışı sıfırlanır. Reddedilme durumlarında HTTP 429 ve `Retry-After` kodları döndürülür. Sınırlar bellekte tutulur ve tek bir panel işlemi içindeki çalışma alanları arasında paylaşılır; yeniden başlatma işlemi bu sınırları sıfırlar. Canlı akışlar, taşıyıcı belirteci başına dört ile sınırlıdır ve panel işlemi için bu sınır 32’dir. Bir akışın açılması da API istek kotasından düşer.

İstek gövdeleri için 60 saniyelik bir alım süresi sınırı vardır (MCP için 8 saniye). Her uygulama, tamamlanmamış gövdeleri 32 istek ve 64 MiB ayrılmış yol kotası ile sınırlar. Boyutu aşan gövdeler 413 hatası, zaman aşımına uğrayan gövdeler 408 hatası ve gövde kapasitesinin tükenmesi durumunda `Retry-After` ile birlikte 503 hatası döndürür.

Gerçek TCP eşi `TGWITNESS_TRUSTED_PROXIES`'ye (virgülle ayrılmış IP'ler veya CIDR'ler) ait olmadığı sürece, iletilen IP başlıkları yok sayılır. `TGWITNESS_PROXY_HEADER`'yi `x-forwarded-for` veya `cf-connecting-ip` olarak ayarlayın. XFF, en yakın proxy'den ilk güvenilmeyen eşe doğru izlenir. Yanlış biçimlendirilmiş veya yinelenen güvenilir adres meta verileri reddedilir; bu nedenle izin listesindeki bir proxy adresini devralamaz. Yönetilen hızlı tünel yerel Cloudflare konektörüne güvenir; kendi etki alanı kurulumunda ise yerel Caddy'ye güvenilir. Doğrudan dağıtımlar varsayılan olarak hiçbir proxy’ye güvenmez. Uvicorn’u kendiniz başlatıyorsanız, bu sınırın gerçek eşi alabilmesi için proxy başlığı işleme özelliğini devre dışı bırakın.

`TGWITNESS_PANEL_ALLOWED_IPS`, yönetici dahil tüm panel erişimini listelenen IP'ler veya CIDR'lerle sınırlar. Yükleyicinin yönlendirme kimliği sorgusu herkese açık kalır ve hiçbir hesap verisi döndürmez. İzin listesini etkinleştirmeden önce gerekli yerel yönetim yolunu ekleyin. Yönetilen bir kurulumun **START-HERE** kılavuzu, hizmet yapılandırması ve kurtarma talimatlarını içerir.

Bir API `ws` sorgu seçicisi, istek yolundaki çalışma alanını tanımlamalıdır; bilinmeyen, uyuşmayan ve yinelenen seçiciler 404 hatasıyla reddedilir.

Panel komut dosyaları ve stilleri, SHA-384 bütünlük meta verilerini içerir. Bir içe aktarma haritası ayrıca, içe aktarma haritası bütünlüğünü destekleyen tarayıcılarda yerel olarak içe aktarılan JS modüllerini de kapsar. Dinamik olarak oluşturulan dil yanıtı ayrıdır. Bu kontroller, teslim edilen sayfaya göre varlık değiştirilmesini tespit eder; hem sayfayı hem de hash değerlerini değiştirebilen güvenliği ihlal edilmiş bir sunucuya güven sağlamazlar.

**Bu başlangıçtan itibaren tutulan günlük,** işlem günlüklerini her çalışma alanından gelen günlük etkinlikleriyle birleştirir: oturum açma işlemleri, reddedilmeler, rota değişiklikleri ve operatör eylemleri. Bu, her mesajın kalıcı bir kopyası değil, mevcut işlem için bellek içi bir konsoldur. Sık tekrarlanan mesaj olayları, konsolu doldurmak yerine günlükte kalır.

Erişim izni verme, değiştirme ve iptal etme ile oturum başlatma veya sonlandırma işlemleri de imzalı `access.*` günlük kayıtları oluşturur. Jetonlar bu kayıtlara dahil edilmez. Verilen jetonlar ve oturum kimlik bilgileri, şifrelenmiş kasada hash değerleri olarak saklanır.

****Ana yönetici ve güven sınırı****

Ana panel jetonu kısıtlamaya tabi değildir. Bu jetonla yapılan tarayıcı oturum açma işlemleri, yöneticinin yapılandırdığı oturum sınırlarına tabi oturumlar oluşturur. Ana jetonu doğrudan gönderen komut dosyaları tam erişim hakkını korur ve tarayıcı oturumları olarak sayılmaz.

Bu, tek bir kurulumda uygulama düzeyinde erişim denetimidir. Tüm çalışma alanları sunucu sürecini paylaşır; bu, ana bilgisayar yöneticisinden izolasyon anlamına gelmez. Ana jetonu, Telegram oturumlarını, imzalama anahtarlarını ve veri dizinini gizli tutun. Bir tanık jetonu, panel erişim jetonu değil, ayrı bir kontrol noktası/sağlık kimlik bilgisidir.
