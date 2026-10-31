# Soruşturma modu

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/investigation/

Kapsam belirlemeden doğrulanmış vaka dosyasına kadar, kanallar, gruplar, özel sohbetler ve botlar genelinde tüm hesaplara yönelik soruşturmalar.

Bir vakayı, ilk toplamadan alıntılanan zaman çizelgesine ve doğrulanabilir devir teslimine kadar kanallar, gruplar, özel sohbetler ve botlar üzerinden takip edin. Etkileşimli web sitesi sürümü `/docs/cases/` adresinde bulunur; [önizleme talimatları](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Örnek vaka: Dört farklı sohbet boyunca bir hedef adresin değişmesi

Bir duyuru bir botu işaret ediyor. Bir operasyon grubu yeni bir ödeme hedefini tartışıyor, botun klavyesi bunu gösteriyor ve özel bir takip mesajında bu bilgi tekrarlanıyor. Ardından duyuru düzenleniyor ve bir grup mesajı kayboluyor.

Sorular şunlardır: Değişiklikten önce ve sonra neler gözlemlendi, her bir öğeyi hangi Telegram hesapları paylaştı, hedef nerede göründü, hangi ek baytları korundu ve hangi aralıklar bilinmiyor?

Bu örnekteki tüm isimler, kimlik numaraları, zamanlar ve günlük referansları kurgusaldır. İş akışı mevcut özellikleri kullanır; vaka haritası bir örnektir, uygulama tarafından otomatik olarak oluşturulan bir grafik değildir.

Akış şeması · Kanallar → Çalışma alanı günlüğü; Gruplar → Çalışma alanı günlüğü; Özel sohbetler → Çalışma alanı günlüğü; Botlar → Çalışma alanı günlüğü; Çalışma alanı günlüğü → Tüm kaynaklarda arama yap; Çalışma alanı günlüğü → Kayıt referansları içeren kişi profilleri; Çalışma alanı günlüğü → Kaydedilen sürümler ve ek alım belgeleri; Tüm kaynaklarda arama yap → Analist zaman çizelgesi ve kaynak kaydı; Kayıt referansları içeren kişi profilleri → Analist zaman çizelgesi ve kaynak kaydı; Kaydedilen sürümler ve ek alım belgeleri → Analist zaman çizelgesi ve kaynak kaydı; Çalışma alanı günlüğü → İmzalı kanıt ZIP dosyası; Analist zaman çizelgesi ve kaynak kaydı → Ayrı ayrı doğrulanmış kanıtlarla vaka devri; İmzalı kanıt ZIP dosyası → Ayrı ayrı doğrulanmış kanıtlarla vaka devri · Kanallar · Gruplar · Özel sohbetler · Botlar · Çalışma alanı günlüğü · Tüm kaynaklarda arama yap · Kayıt referansları içerenkişi profilleri · Kaydedilen sürümler ve ekalım belgeleri · İmzalı kanıt ZIP dosyası · Analist zaman çizelgesi vekaynak kaydı · Ayrı ayrı doğrulanmışkanıtlarla vaka devri

**Diyagramın metin olarak gösterimi**

1. Kanallar → Çalışma alanı günlüğü
2. Gruplar → Çalışma alanı günlüğü
3. Özel sohbetler → Çalışma alanı günlüğü
4. Botlar → Çalışma alanı günlüğü
5. Çalışma alanı günlüğü → Tüm kaynaklarda arama yap
6. Çalışma alanı günlüğü → Kayıt referansları içeren kişi profilleri
7. Çalışma alanı günlüğü → Kaydedilen sürümler ve ek alım belgeleri
8. Tüm kaynaklarda arama yap → Analist zaman çizelgesi ve kaynak kaydı
9. Kayıt referansları içeren kişi profilleri → Analist zaman çizelgesi ve kaynak kaydı
10. Kaydedilen sürümler ve ek alım belgeleri → Analist zaman çizelgesi ve kaynak kaydı
11. Çalışma alanı günlüğü → İmzalı kanıt ZIP dosyası
12. Analist zaman çizelgesi ve kaynak kaydı → Ayrı ayrı doğrulanmış kanıtlarla vaka devri
13. İmzalı kanıt ZIP dosyası → Ayrı ayrı doğrulanmış kanıtlarla vaka devri

## 1. Vakayı tanımlayın ve olayın tüm ayrıntılarını toplayın

1. Toplama hesabını kendi çalışma alanına bağlayın. Harici vaka notlarında, vaka referansını, hesap kimliğini, çalışma alanını, gözlem başlangıç tarihini ve güvenilir imza anahtarı parmak izini kaydedin.
2. Açık **Kaynaklar → Gözlem kapsamı → Soruşturma modu**. Ön ayar, **Tüm hesap**, kanallar/gruplar/özel sohbetler/botlar, kendi eylemler, kaynak profilleri ve yeni keşfedilen kaynaklara ait en son 200 görünür mesajı seçer. İnceledikten sonra **Kapsamı Kaydet**düğmesine basın ve kapsam onayını tamamlayın.
3. **Sohbetleri yükleyin** ve kaynakları hesabın sohbet listesiyle karşılaştırın. Hariç tutulanları kontrol edin. **Parametreler → Hesabın listesinden okunan sohbet sayısı** varsayılan olarak 1.000'dir ve en fazla 20.000'e kadar izin verilir. Liste sınırını aşan kaynaklar, aktif hale geldiklerinde eklenir. Gerçekte sayılanları kaydedin.
4. **Kayıt ayar**larında, "**Görünür tüm etkinlikler"** seçeneğini seçin ve izleme ayarlarını kaydedin. Ek türlerini/sınırlarını ve boş disk alanını kontrol edin.
5. Gözlemi başlatın. Kontrollü bir yeni mesaj, düzenleme ve silme işlemini doğrulayın, ardından test referanslarını ve olası hataları kaydedin.

"Tüm hesap" kapsamı, kaydedilen ayarlar dahilinde hesapta görülebilen etkinlikleri kaydeder. Gizli sohbetlere erişmez veya bağlantılı her gruba otomatik olarak katılmamaktadır. Ayrıca mevcut tüm sohbetleri geriye dönük olarak doldurmaz. [Toplama kapsamına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account) bakınız.

## 2. Her kaynağı listeleyin ve tarihsel bağlamı belirleyin

Her sohbet için bir satır içeren bir kaynak kaydı tutun:

| Alan | Kaydet |
| --- | --- |
| Kimlik | Çalışma alanı, hesap kimliği, sayısal sohbet kimliği, başlık ve tür |
| Görünürlük | Üyelik/rol, erişim onaylanmış veya onaylanmamış, hariç tutulanlar |
| Canlı yakalama | Başlangıç zamanı, seçilen olay türleri ve sonraki politika değişiklikleri |
| Günlük geçmişi | İstenen/tamamlanan anlık görüntü, sınır, zaman ve kayıt referansları |
| Tam geçmiş | Sohbet başına imzalı dışa aktarım dosya adı, sınır ve tamamlanma/başarısızlık durumu |
| Ekler | Tamamlanmış medya makbuzları, hash değerleri, boyutlar ve atlanan/başarısız sonuçlar |
| Kapsam | Kesintiler, eksik veri alımı, FloodWait, erişilemeyen mesajlar ve diğer eksiklikler |

Her kaynak için uygun veri toplama yöntemini kullanın:

- **Kaynaklar**'da **tam geçmişi yükle** (şu anki `main`), etkinleştirilmiş kaynaklardan mevcut geçmiş mesajları çalışma alanı günlüğüne yükler. Duraklatma/devam ettirme ve imzalı ilerleme raporunu destekler. [Geçmiş elde etme bölümüne](https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/) bakın.
- **Geçmiş anlık görüntüsü,** son zamanlarda görünür olan mesajları gözlem günlüğüne kaydeder. Varsayılan maksimum değer 500'dür; **Parametreler → En büyük geçmiş anlık görüntüsü** seçeneği ile bu değer 10.000'e yükseltilebilir. Bunlar, yeniden oluşturulmuş düzenlemeler değil, güncel geçmiş gözlemleridir.
- **Sohbetin tamamını dışa aktar → Sohbetin tamamını dışa aktar** veya **Sohbetler → Sohbeti dışa aktar** seçeneği, bir sohbetin o anda görünür olan geçmişini ayrı bir imzalı `chat.json` / `chat.html` paketine aktarır. Davanın kaynakları için bu işlemi tekrarlayın ve her sonucu saklayın.
- **Yeni bir sohbet veya bot ortaya çıktığında,** profilini ve en fazla 1.000 adet son mesajı kaydedebilir; Soruşturma modunda ise 200 mesaj seçilir. Mod etkinleştirildiğinde, mevcut sohbetler bu verileri geriye dönük olarak almaz.
- **Görünür eklerin indirilmesi**, yapılandırılan ilke kapsamında baytları korur. SHA-256 ve bayt sayısını içeren, tamamlanmış bir `media.saved` makbuzu gereklidir. Kuyrukta bekleyen bir iş, küçük resim veya dosya adı, korunan ek olarak kabul edilmez.

Sohbetin tam olarak dışa aktarılması, günlüğe veya kişi profillerine tüm mesajları eklemez. TgWitness içinde analiz etmeniz gereken geçmiş için **"Tüm geçmişi yükle"** veya sınırlı günlük anlık görüntülerini kullanın. Geçmiş işlemini başlatmadan önce etkinleştirilmiş kaynak listesini gözden geçirin. Her iki yöntem de Telegram'ın artık geri getirmediği içerikleri kurtarmaz.

## 3. Gelişen vakayı ve kasıtlı etkileşimleri kaydetmek

Aktif vaka sohbetlerini öncelikli kaynaklar olarak işaretleyin. Yeniden kontrol aralıklarını, devam eden takip işlemlerini ve medya çıktılarını gözden geçirin. Hesabı kullanırken toplayıcının gözlem yapmasını sağlayın. **Sohbetler → Profil → Profili şimdi kaydet** seçeneğini kullanarak açıklamalar ve bot komutları gibi kaynak meta verilerini koruyun. Bu, kaydedilmiş mesajlardan türetilen kişi profillerinden ayrıdır.

Davanın bir kaynağı takip etmeyi veya bir botla etkileşime geçmeyi içerdiği durumlarda:

1. **Telegram bağlantısını aç → Önizlemeyi kaydet**, verilen bağlantıyı ve bir işlemden önce görüntülenen önizlemeyi kaydeder.
2. **Join / open ve observe komutları**, join/open işlemini gerçekleştirir ve belirtildiğinde botun start parametresini gönderir. Onay bekleyen bir katılma isteği, beklemede olarak kaydedilir.
3. Panel tarafından gönderilen metin yanıtları ve desteklenen düğme tıklamaları, `interaction.requested` ve `interaction.result` değerlerini korur. Geri arama makbuzları, geri gönderilen açılır pencere metnini, uyarı durumunu ve URL'yi koruyabilir.

Bunlar gerçek hesap eylemleridir. Başka bir Telegram uygulamasındaki geri arama tuşlamaları, toplayıcı tarafından görülemez; ancak bunlardan kaynaklanan mesajlar veya düzenlemeler görülebilir. Mini istemci, web uygulaması, ödeme, telefon veya konum iş akışlarını yürütmez. Kesin davranış için [panel etkileşimlerine](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/#act-from-the-panel) bakın.

## 4. Sohbetler arasındaki gözlemleri birbiriyle ilişkilendirin

"**Günlük**" bölümünde "**Tüm kaynaklar**" seçeneğini seçin ve kaydedilmiş içeriği arayın. Eşleşen kayıtları açın ve çalışma alanını, sohbeti, mesaj kimliğini, sıra numarasını ve kayıt hash değerini not edin.

İlgili bir sohbette, **Kişiler → Profilleri aç seçeneğine gidin** ve bir kişiyi inceleyin:

- Zaman içinde gözlemlenen isimler/kullanıcı adları ve sayısal Telegram kimliği.
- Kaynak kayıt referanslarıyla birlikte yanıt ilişkileri.
- **Ayrıca…** bu çalışma alanı günlüğünde, söz konusu kullanıcı kimliğinin yazdığı diğer sohbetlerde de.
- Etkinlikler, düzenlemeler/silme işlemleri ve bahsedilen cüzdanlar, telefonlar, kullanıcı adları ve bağlantılar.
- Kaydedilmiş avatar meta verileri ve benzer önbelleğe alınmış avatarlar, ayrı kaynak bilgileriyle birlikte.

Bir bulguda türetilmiş bir profili kullanmadan önce, alıntılanan kayıtları açın. Profiller, grubun her üyesini değil, kaydedilmiş mesajları olan kişileri kapsar. **Parametreler → Her bir olaya göre alıntılanan kayıtlar**, referans listesini sınırlar; altta yatan etkinlik sayısını sınırlamaz. Bahsetmeler ve avatar benzerliği ipucu niteliğindedir; sahiplik veya kimliği kanıtlamaz.

Örnekte:

| Bağlantı | Kayıtlar | Desteklenen gözlem |
| --- | --- | --- |
| Aynı gönderen hesabı | Grup #146 ve özel takip #205 | Her ikisi de Telegram gönderen kimliği 71001'i sağlar |
| Aynı hedef | #146, bot klavyesi #173, kanal düzenleme #188, özel mesaj #205 | Hepsinde `pay.example.invalid/new` bulunur; sahiplik/kontrol durumu belirlenmemiştir |
| Aynı kaydedilmiş dosya | #151 ve #209 numaralı medya makbuzları tamamlandı | Korunan baytlar için tam SHA-256 değerleri birbiriyle uyumludur |
| Kanal kaynağı | #101 ve #188 | Göndereni belirtilmedikçe, bir kanal gönderisini 71001 numaralı kullanıcıya atfetmeyin. |

Eklerin hash değerlerini ve bunlara ilişkin mesaj referanslarını karşılaştırın. Aynı dosyalar, bir dosyanın yaratıcısını, ileten kişiyi veya ortak bir operatörü kanıtlamaz. Aynı isimler ve benzer avatarlar tek başına iki Telegram kimliğini tek bir kişiye bağlamaz.

## 5. Sohbetler arası zaman çizelgesini oluşturun

**Sohbetler'de** kaydedilen sürümleri ve bunların **Günlük kaydı #…** bağlantılarını kullanın. **Günlük**'te, **Tüm kaynakları Düzenlemeler**, **Silme işlemleri** ve **Kapsam** ile birleştirin. Varsa hem `source_at`'yi hem de `observed_at`'yi koruyun.

| Örnek gözlem süresi | Referans | Gözlem |
| --- | --- | --- |
| 09:00 | Kanal #101 | Orijinal hedef yakalandı |
| 09:12 | Grup #146; medya #151 | Yeni hedef yayınlandı; dosya indirme işlemi tamamlandı |
| 09:16 | Bot #173 | Klavye, yeni hedefe yönlendirir |
| 09:20 | Kanal #188 | Duyuru düzenlendi; her iki kaydedilmiş sürüm de korunuyor |
| 09:24 | Özel #205; medya #209 | Aynı gönderen kimliği alıcıda da tekrarlanır; aynı dosya baytları korunur |
| 09:28 | Grup #231 | Silme bildirimi alındı; silen kişi ve kesin silme zamanı bilinmiyor |

Bu örnek referanslar arasında başka kayıtlar da yer alabilir. Sıra numaraları gözlemleri sıralar; geçmiş anlık görüntüleri daha eski kaynak tarihlerine sahip olabilir ve canlı olaylardan daha geç ulaşabilir. Anlık görüntüleri, kurtarılan mesajları, silme bildirimlerini ve yeniden kontrol edildiğinde eksik bulunan sonuçları birbirinden ayırın. Kapsam boşluklarını bilinmeyen aralıklar olarak işaretleyin. Daha sonra elde edilen geçmiş verileri, geriye dönük olarak kesintisiz gözlem sağladığını göstermez.

## 6. Kaynaklarını kaybetmeden hesap bakış açılarını ekleyin

Her bir hesap için ayrı bir çalışma alanı kullanın ve envanterini tekrarlayın. Her karşılaştırmada hesap kimliğini, rolü, imza anahtarı parmak izini ve kaynak referanslarını saklayın. Mesaj numaraları, sohbetler/hesaplar arasında geçerli genel tanımlayıcılar değildir.

Çalışma alanları arası korelasyon, harici vaka notlarında veya analiz araçlarında gerçekleştirilir. TgWitness'te şu anda çalışma alanları arası genel arama, birleştirilmiş zaman çizelgesi, soruşturma grafiği veya birleştirilmiş vaka arşivi bulunmamaktadır. **Bir** kanalın/süper grubun çoklu hesap olarak dışa aktarılması, hesap günlüklerinin birleştirilmesi değil, ayrı bir işlemdir.

Daha uzun süreli çalışmalar için, [bağımsız bir tanık](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/) aracılığıyla sınırları koruyun. Kontrollü teslimat kontrollerini kullanarak her hesabın yakalama yolunu ve görünürlüğünü doğrulayın.

## 7. Vaka devrini düzenleyin ve doğrulayın

Bunları, bir analist tarafından derlenen vaka dizininde bir arada tutun:

| Materyal | Amaç |
| --- | --- |
| Vaka notları ve kaynak kaydı | Soru, veri toplama politikası, erişim/rol, bulgular, alternatif açıklamalar ve eksiklikler |
| Zaman çizelgesi | Her bir giriş için hem zaman bilgisi hem de çalışma alanı/sohbet/mesaj/sıraya ilişkin referanslar |
| Çalışma alanı başına imzalı kanıt ZIP dosyası | Kaydedilen günlüğün tamamı, içerik listesi ve dahil edilen korunmuş medya dosyaları; panel filtreleri, günlüğün dışa aktarılmasını kısıtlamaz |
| Ayrı ayrı imzalanmış kişi profil dosyaları | Elde edilen referanslar, ilgili çalışma alanındaki kanıtlarla karşılaştırılarak kontrol edildi |
| İmzalı tam sohbet dışa aktarımları | Gözlem günlüğünden ayrı olarak, o anda görünür olan geçmişin toplanması |
| Güvenilir parmak izleri ve önceki kontrol noktaları | Ana kimlik ve saklanan günlük sınırları |
| Yapılandırılmışsa, tanık verileri | Ayrı günlük, imzalı gönderiler ve tanık parmak izi |
| Doğrulama sonuçları ve teslim edilen dosyaların hash değerleri | Neler kontrol edildi, hangi baytlar aktarıldı ve kime aktarıldı? |

Güvenilir bir kurulumdan, dosya adları ve her çalışma alanının gerçek parmak izi ile birlikte:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Gerçek doğrulama sonuçları ve orijinal kanıtlar korunur. Üst düzey vaka dizini, kaynak kaydı ve analistlerin sonuçları harici olarak tutulur; her bir TgWitness kanıtının kendine özgü bir imzası ve doğrulama prosedürü vardır.

## Soruşturmaya uyarlama

| Örnek | Trace | Sun |
| --- | --- | --- |
| Bot destekli sipariş/ödeme anlaşmazlığı | Giriş duyurusu → kaydedilmiş bağlantı önizlemesi → bot başlatma parametresi → mesaj ve klavye sürümleri → panel geri arama makbuzları → özel/grup takibi | Gözlemlenen teklif/yanıt zaman çizelgesi ve doğrulanmış kaynaklar; tek başına bir ödeme bağlantısı, ödeme yapıldığını kanıtlamaz |
| Bir olayın ardından silinen mesajlar | Etkilenen tüm sohbetler → kaydedilen orijinaller/düzenlemeler → silme veya yeniden kontrol edildiğinde eksiklik sonuçları → korunan medya → kapsam ve diğer hesap perspektifleri | Korunmuş sürümler ve açıkça belirtilmiş bilinmeyen aralıklar; uydurma silme failleri yok |
| Bir katılımcı, farklı sohbetlerde farklı isimler kullanıyor | Sayısal gönderen kimliği → isim/kullanıcı adı geçmişi → yanıtlar → gözlemlenen diğer sohbetler → alıntılanan hedefler/dosyalar | Alıntılanan bir Telegram hesabı etkinlik zaman çizelgesi; gerçek dünyadaki kimlik ve ilişki hipotezleri ayrı tutulmuştur |

[Koleksiyon referansı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/) · [Kişi profili doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#people-profiles) · [Kanıt devri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#investigation-handoff) · [Doğrulama tamamlandı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/)
