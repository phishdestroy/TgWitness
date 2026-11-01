# Kanıt ve güven

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence-trust/

Dışa aktarımlar, videolar, web arşivleri ve imzalı kayıtların neyi kanıtlayabileceği ve toplama cihazının bunların güvenilirliğini nasıl etkilediği.

Bir dışa aktarım, ekran görüntüsü veya kayıt yararlı bir kanıt olabilir. Bunların güvenilirliği, nasıl toplandığına, korunduğuna ve doğrulandığına bağlıdır. **Geçerli bir hash veya imza, kaydedilen materyali doğrular; ancak toplama cihazının gerçek kaynak içeriğini aldığını bağımsız olarak kanıtlamaz.** Bu sınırlama TgWitness için de geçerlidir.

Bu kılavuz, teknik doğrulamayı hukuki değerlendirmeden ayırmaktadır. Ürün dokümantasyonu ve aşağıdaki hukuki hükümler 1 Kasım 2026 tarihinde gözden geçirilmiştir; Hunchly karşılaştırması, yayınlanmış dokümantasyonunu açıklamaktadır, yeni bir ürün denetimini değil.

## Güvenin yakalama sürecine dahil olduğu noktalar

Akış şeması · Telegram hesabı ve hizmeti → İstemci, tarayıcı ve işletim sistemi; İstemci, tarayıcı ve işletim sistemi → Dışa aktarma, video veya sayfa yakalama; Dışa aktarma, video veya sayfa yakalama → Hash değerleri ve toplayıcı imzaları; Hash değerleri ve toplayıcı imzaları → Bağımsız bir tarafça saklanan hash · Telegram hesabı vehizmeti · İstemci, tarayıcı veişletim sistemi · Dışa aktarma, videoveya sayfa yakalama · Hash değerleri vetoplayıcı imzaları · Bağımsız bir tarafçasaklanan hash

**Diyagramın metin olarak gösterimi**

1. Telegram hesabı ve hizmeti → İstemci, tarayıcı ve işletim sistemi
2. İstemci, tarayıcı ve işletim sistemi → Dışa aktarma, video veya sayfa yakalama
3. Dışa aktarma, video veya sayfa yakalama → Hash değerleri ve toplayıcı imzaları
4. Hash değerleri ve toplayıcı imzaları → Bağımsız bir tarafça saklanan hash

Buradaki tehdit modeli, bir saldırganın veya operatörün kanıtlar kaydedilmeden önce toplama ortamını değiştirebileceğini varsayar. Bu, koşullu bir analizdir; belirli bir cihazın veya ürünün ele geçirildiğine dair bir iddia değildir.

Resmi bir istemci ve şifreli bir bağlantı, normal kullanımın korunmasına yardımcı olur. Bunlar, çevredeki işletim sistemini, tarayıcıyı veya ekranı bağımsız olarak güvenilir hale getirmez. İçerik, şifre çözme işleminden sonra ancak yakalama işleminden önce değiştirilirse, dışa aktarıcı bunu doğru bir şekilde kaydedebilir ve imzalayan kişi bunu doğru bir şekilde imzalayabilir. Her iki işlem de bozuk bir hash algoritmasına veya sahte bir imzaya ihtiyaç duymaz.

Aynı cihazda çekilen bir video, aynı değiştirilmiş sunumu kaydedebilir. Ayrı bir kamera, ekranın ne gösterdiğini doğrulayabilir, ancak ekran tek başına Telegram'ın sağladıklarını doğrulamaz. Benzer şekilde, tek bir kontrollü ortamdan elde edilen eşleşen HTML, JSON, ekran görüntüleri ve tarayıcı günlükleri aynı hatayı paylaşabilir. Bunların birbiriyle uyuşması yararlı bir bağlamdır; ancak otomatik olarak bağımsız bir doğrulama değildir.

## Her bir kanıt türünün katkısı

| Materyal | Yararlı katkı | Kalan sorular |
| --- | --- | --- |
| Telegram Masaüstü dışa aktarma | Okunabilir veya makine tarafından okunabilir sohbetler ve seçilmiş medya | İstemci ve dışa aktarma dosyalarını kim kontrol etti ve nelere erişim vardı ya da neler hariç tutuldu? |
| Ekran görüntüsü veya ekran kaydı | Görünür bağlam, işlem dizisi ve sunum | Sunum, kaynağı ve kayıt dışında neler olduğunu aslına sadık bir şekilde yansıtıyor mu? |
| MHTML dahil yerel web arşivi | Sonraki inceleme için sayfa içeriği ve ilgili kaynaklar | Tarayıcı, arşivleyiciye ne sağladı ve bu tarayıcıyı kim kontrol ediyordu? |
| Toplayıcı tarafından imzalanmış arşiv | İmzalı baytlarda yapılan değişiklikler, güvenilir bir anahtara göre tespit edilebilir ve referans korunabilir | İmzalamadan önce imza anahtarını ve girdiyi kim kontrol etti? |
| Bağımsız olarak saklanan kontrol noktası veya doğrulanmış zaman damgası | Sonraki bir gönderimle karşılaştırma amacıyla saklanan bir hash veya kontrol noktası | Hangi baytlar ve sınırlar kapsanmaktadır ve bağımsız taraf aslında neyi tasdik etmektedir? |

Telegram, Masaüstü dışa aktarımını çevrimdışı bir HTML/JSON kopyası olarak ve Takeout API'sini seçilen hesap verilerini almak için bir yol olarak belgelemektedir. Bu açıklamalar, alıcının doğrulayabileceği, dışa aktarılan nihai arşiv üzerinde bir Telegram imzası sağlamaz. Sonuçlarımız, belgelenen bu dışa aktarım mekanizmalarıyla sınırlıdır; bu, Telegram kanıtlarının hukuki değeri olmadığı iddiası değildir.[Telegram Masaüstü dışa aktarımı](https://telegram.org/blog/export-and-more),[Takeout API](https://core.telegram.org/api/takeout).

Aynı ayrım, arka plan istekleri, önbellek girdileri ve ağ günlükleri için de geçerlidir. Bunlar tutarsızlıkları ortaya çıkarabilir ve bir toplama işleminin doğrulanmasına yardımcı olabilir. Bunların karmaşıklığı tek başına, bunları kimin ürettiğini belirlemez. Bağımsız olarak işletilen bir arşiv veya ayrı olarak elde edilen hizmet kaydı, kendi toplama ve saklama sınırlamalarına tabi olmak üzere, karşılaştırma için farklı bir kaynak sunar.

## Hunchly aynı sınırı gösterir

Hunchly belgelerinde, MHTML yakalamaları, fotoğraflar ve eklerin SHA-256 karma hesaplaması ve bağımsız karma doğrulaması açıklanmaktadır. Ayrıca, değiştirilmiş bir dosyanın yeni hesaplanmış bir karma değeri eşliğinde bu karşılaştırmayı neden geçebileceği açıklanmakta ve ek kontroller olarak imzalar ve kaynak doğrulaması gösterilmektedir.[Hunchly: içerik, fotoğraf ve eklerin karma hesaplaması](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

Yayınlanan *Kanıt Kılavuzu’nun* 17 Ekim 2018 tarihli 1.0 revizyonu, MHTML yakalamaları için yerel olarak oluşturulan GPG anahtarlarını ve imzaları açıklamaktadır. Kılavuz, değiştirilmiş materyali yeniden imzalamak için yerel özel anahtara erişimi açıkça belirtmektedir. Bu, belgelenmiş bir güven sınırlamasıdır; açıklanmamış güncel bir güvenlik açığının kanıtı değildir. Kılavuzda ayrıca MHTML yakalamasının Chrome tarafından gerçekleştirildiği belirtilmektedir. Hunchly’yi sadece araştırmacının itibarına dayanan bir sistem olarak tanımlamak, bu teknik kontrolleri göz ardı etmek anlamına gelir.[Hunchly Kanıt Kılavuzu, bölüm 2–4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

Belirli bir ürünle toplanan materyalin bir davada kabul edilip edilmediği, ilgili karar ve koşullara bağlıdır. Burada, mahkemelerin Hunchly veya TgWitness’i ne sıklıkla kabul ettiği veya her iki ürünün de genel bir mahkeme onayı olup olmadığı konusunda herhangi bir iddiada bulunmuyoruz.

## TgWitness'in sağladığı ek özellikler ve korumanın sınırları

TgWitness, gözlemleri imzalı, bağlantılı bir günlüğe kaydeder ve alıcının doğrulayabileceği dışa aktarımlar sağlar. Saklanan kontrol noktaları, zaman damgaları ve ayrı bir tanık, gözden geçirenlere toplayıcının mevcut dosyalarının ötesinde referanslar sunar. Bunlar, daha önce kaydedilmiş kayıtlardaki değişiklikleri ortaya çıkarmaya yardımcı olur. Kapsam kayıtları ve açık toplama sonuçları, nelerin yakalandığını ve nelerin yakalanmadığını açıklamaya yardımcı olur.[Kanıt biçimi ve devri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/), [toplama kapsamı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/).

Olası bir ikame işleminin zamanlaması önemlidir:

1. **İmzaladıktan sonra, imza anahtarına erişim olmadan:** imzalanmış bir kaydı veya manifestoya bağlı bir dosyayı değiştirmek, güvenilir bir doğrulayıcı ve anahtarla yapılan doğrulamayı başarısız kılar.
2. **Toplayıcı anahtarıyla, bağımsız bir kontrol noktası saklandıktan sonra:** bir değiştirme günlüğü geçerli yeni imzalar içerebilir, ancak değiştirilmiş bir önek, daha önceki kontrol noktasıyla karşılaştırıldığında başarısız olur. Yalnızca aynı kontrol altındaki cihazda tutulan bir kontrol noktası, günlükle birlikte değiştirilebilir. Saklanan sınırın ötesindeki kayıtlar için ayrı bir kapsam gereklidir.
3. **Bir gözlemi kapsayan kontrol noktası bağımsız olarak saklanmadan önce:**yanlış girdiler, daha önceki bir kontrol noktasından sonra eklenen yeni kayıtlar da dahil olmak üzere başarıyla imzalanabilir ve sabitlenebilir. Ortaya çıkan kontrol noktası veya zaman damgası hala bu yanlış kayıtları kapsar; bunların doğruluğunu kanıtlamaz.

Bir TgWitness tanığı, toplayıcının imzalı kontrol noktalarını alır; altta yatan Telegram sohbetini bağımsız olarak okumaz. Anahtarı ve saklanan kayıtları ayrı ayrı güvenilir olmalıdır. Gönderilen günlüğün tamamının tanıklanması gerektiğinde,[son dışa aktarma sınırını gerektiren devretme prosedürünü](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/#require-a-witnessed-export-boundary) kullanın. Sıradan bir bütünlük denetimi, tanıklanmamış bir son kısmı yine de rapor edebilir.

Doğrulanmış bir RFC 3161 yanıtı, bir kontrol noktasının yetkili kurumun belirttiği zamanda mevcut olduğunu destekleyebilir. Ancak bu, bir Telegram mesajının ne zaman gönderildiğini veya içeriğinin doğru olup olmadığını kanıtlamaz. Hazırlanmış bir istek veya eklenmiş bir yanıt dosyası tek başına yeterli değildir. `tgwitness.verify` ile bir dışa aktarmayı doğrularken, ekli TSA imzalarını kontrol etmek için `--tsa-ca` aracılığıyla açıkça güvenilir bir CA gereklidir. OpenTimestamps makbuzları için bağımsız `ots verify` gereklidir; gerektiğinde kanıt yükseltmeleri yapılmalıdır. [Zaman damgası prosedürü](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

[GitHub Actions yakalamasında](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), geçici olarak barındırılan bir çalıştırıcı mesajları toplar. Doğrulama, arşivi onaylanmış bir iş akışına bağlar. Bu mod, hala GitHub’a, onaylanmış yazılıma ve bağımlılıklara, yardımcı programa/tarayıcıya ve tünele güvenir. Bu, gizli bir donanım, bir Telegram imzası veya hiç kimsenin ana bilgisayara erişmediğine dair bir kanıt değildir. Yerel olarak imzalanmış bir çalıştırma makbuzu da, donanım doğrulaması değil, kendi kendini bildiren bir ölçümdür.

## Yasal geçerlilik temele bağlıdır

Dört sorunun birbirinden ayrı tutulması gerekir: öğenin iddia edildiği gibi olup olmadığı, gönderilen baytların saklanan kayıtla eşleşip eşleşmediği, içeriğin iddia edilen gerçekleri destekleyip desteklemediği ve geçerli kuralların kullanımına izin verip vermediği. Kriptografik bir kontrol, bu temelin yalnızca bir kısmını ele alır.

ABD federal yargılama süreçlerinde, Kural 901, bilgili tanık ifadeleri ve bir süreç veya sistemle ilgili kanıtlar dahil olmak üzere, kanıtların doğrulanmasına yönelik yöntemler sunar. 902(13) ve 902(14) numaralı kurallar, usul gereklilikleri ile birlikte belirli elektronik kayıtlar ve kopyalar için tasdik yolları sunar. Komite notları, doğrulamayı kulaktan dolma bilgi, alaka düzeyi ve atıf gibi konulardan ayırır. Bir yazılım imzası tek başına, burada açıklanan yetkili kişinin tasdiki değildir.[Federal Delil Kuralı 901](https://www.law.cornell.edu/rules/fre/rule_901),[Federal Delil Kuralı 902](https://www.law.cornell.edu/rules/fre/rule_902).

Kanada Delil Yasası'nın geçerli olduğu durumlarda, 31.1. madde elektronik belgelerin doğrulanmasını ele alır. 31.2. madde, en iyi delil kuralını sistem bütünlüğü veya geçerli bir varsayımla ilişkilendirir; 31.3. madde ise bütünlük varsayımı için koşulları belirtir. Bunlar, tanımlanmış delil koşullarıdır; herhangi bir lisanslı araştırmacının veya ticari ürünün hatasız olduğuna dair genel bir varsayım değildir. [Kanada Delil Kanunu, 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Bu örnekler, başka bir yargı alanında veya belirli bir davada kabul edilebilirliği kesinleştirmez. Teknik kontroller, bir iddiayı destekleyen veya sorgulayan materyallere tutarlı bir şekilde uygulanmalıdır. Bu kılavuz, savcılık delillerinin genel olarak savunma delillerinden daha kolay kabul edilebilir olduğu iddiasında bulunmaz.

## Başka bir kişinin değerlendirebileceği bir kayıt hazırlayın

- Hesabı, toplama cihazını, operatörü, yazılım sürümünü, erişim haklarını, seçilen kapsamı ve toplama süresini açıklayın. Başarılı bir imza kontrolünü cihazın temiz olduğu anlamına gelen bir test olarak değerlendirmek yerine, kesintileri ve olası güvenlik ihlallerini kaydedin.
- Orijinal paketleri koruyun ve aktarımları, karma değerleri ve zaman kaynağını kaydedin. Anahtar parmak izini ve kontrol noktalarını ayrı bir güvenilir kanal aracılığıyla saklayın. Bir raporda açıklamadan önce gerçek tanık veya zaman damgası kapsamını doğrulayın.
- İddia ile uyumlu bağımsız doğrulama kaynakları arayın: başka bir katılımcının kayıtları, bağımsız bir yakalama veya yasal yollarla elde edilmiş hizmet kayıtları. Bunların bağımsızlığını ve sınırlamalarını açıklayın; kopyalar arasındaki uyum tek başına yeterli değildir.
- İlgili bağlamı koruyun. Atlanan dosyaları, erişilemeyen geçmişi ve sansürlenmiş kısımları belirtin. Gerektiğinde [ayrıbir özet açıklama](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)hazırlayın ve bunu tam orijinal metin olarak sunmadan yapılan değişiklikleri açıklayın.
- Alıcıya doğrulama talimatlarını ve bu kontroller için gerekli materyalleri verin. Gözlemleri, teknik bulguları ve analistin sonuçlarını birbirinden ayırt edilebilir şekilde tutun.

Belirli bir devir için arşiv hash'ini, güvenilir anahtarı, doğrulama sonucunu ve harici olarak kapsanan kesin sınırı belirtin. Kaynağın özgünlüğünü, hesap atıfını, eksiksizliğini ve hukuki sonuçları ayrı ayrı açıklayın. Bu, bir sonraki inceleyiciye incelenmesi gereken belirli iddialar sunar.
