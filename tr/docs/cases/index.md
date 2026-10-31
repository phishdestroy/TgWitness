# Tüm sohbetleri inceleyin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/cases/

Kanallar, gruplar, özel sohbetler ve botlar genelinde bir vakayı baştan sona ele alın: kanıtları toplayın, birbiriyle ilişkilendirin, yeniden yapılandırın ve teslim edin.

Bu adım adım kılavuz, kurgusal bir olayı baştan sona takip eder. Gerçek veri toplama, arama, kişi profili ve dışa aktarma özelliklerini kullanır. Vaka haritası bir dokümantasyon örneğidir; kendi sonuçlarınız ve vaka kaydınız uygulama dışında tutulur.

ÇÖZÜLMÜŞ VAKA / DEĞİŞTİRİLEN ÖDEME HEDEFİ

### Tek bir olay. Dört konuşma. Yeniden canlandırılması gereken bir iz.

Bir kanal duyurusu bir botu işaret ediyor. Bir operasyon grubu yeni bir ödeme bağlantısını tartışıyor. Özel bir takip mesajı bunu tekrarlıyor. Daha sonra duyuru düzenleniyor ve bir grup mesajı kayboluyor.

Her bir sürümü kim yayınladı?Bağlantı nerede göründü?Hangi dosya saklandı?Neler değişti ve ne zaman?

Geçmiş verilerin yüklenmesi, isteğe bağlı yapay zeka kaynak incelemesi, MCP, OCR ve giden webhook'lar hakkında bilgi için "[Arşivi Kullan](https://phishdestroy.github.io/TgWitness/tr/docs/archive/)" bölümüne bakın.

## 1. Hesabın tamamını kapsayacak şekilde kapsam oluşturun

1. [Toplama hesabını kendi çalışma alanına bağlayın](https://phishdestroy.github.io/TgWitness/tr/docs/accounts/). Vaka referansını, hesap kimliğini, çalışma alanı adını ve imza anahtarı parmak izini vaka notlarınıza kaydedin.
2. Açık **Kaynaklar → Gözlem kapsamı → Soruşturma modu**. **Tüm hesabı**, dört kaynak türünün tamamını ve **Kendi eylemlerini** inceleyin. Bu ön ayar, yeni bir kaynağın profilini ve **görünür durumdaki** en son **200 mesajını** kaydetmenizi sağlar. **Kapsamı kaydet seçeneğine** basın ve kapsam onayını tamamlayın.
3. **"Sohbetleri Yükle"** düğmesine basın. Kaynakları hesabın sohbet listesiyle karşılaştırın ve hariç tutulanları inceleyin. **"Parametreler" → "Hesabın listesinden okunan sohbetler**" altında, gerekirse başlangıç liste sınırını ayarlayın: varsayılan değer 1.000 sohbettir ve 20.000'e kadar yapılandırılabilir. Sınırı aşan sohbetler, aktif hale geldiklerinde tespit edilir.
4. **Kayıt**ayarlarında, "**Görünür tüm etkinlikler"** seçeneğini seçin ve kaydedin. Ek türlerini, boyut sınırlarını ve boş disk alanını gözden geçirin. Kuruluma güvenmeden önce gözlemi başlatın ve kontrollü bir mesajı, düzenlemeyi ve silme işlemini doğrulayın.

KanallarGruplarÖzel sohbetlerBotlar

TEK HESAP / TEK İMZA ANAHTARI**Seçilen tüm hesapta görülebilen etkinlikler → tek bir günlük**

Mesajlar · düzenlemeler · silme bildirimleri · görünür tepkiler · üyelik etkinlikleri · kendi eylemleri

“Tüm hesap”, bu hesabın erişebileceği sohbetleri, yapılandırılmış kaynak türleri ve hariç tutulanlar dahil olmak üzere kapsar. Gizli sohbetler kullanılamaz. Güncellemeler geldikçe yeni diyaloglar eklenir; bu modun etkinleştirilmesi, mevcut her sohbetin eski geçmişinin tamamını otomatik olarak indirmez.

## 2. Geçmişi elde etme ve dosyaları koruma

Soruşturmanın tamamı için bir kaynak kaydı oluşturun. Her sohbete, sayısal kimliği, başlığı, hesabı, erişim/rolü, canlı başlangıç tarihi, geçmiş verilerinin elde edilme tarihi, medya sonuçları ve bilinen eksiklikleri içeren bir satır ayırın. İlgili sonucu kontrol ettikten sonra kaynağı "elde edildi" olarak işaretleyin.

| İhtiyaç | Paneldeki eylem | Neler sunar? |
| --- | --- | --- |
| Etkinleştirilmiş sohbetlerdeki geçmiş | Kaynaklar → Tüm geçmişi yükle | Güncel ana özellik: mevcut geçmiş mesajlar çalışma alanı günlüğüne aktarılır; bu süreçte duraklatma/devam ettirme seçenekleri ve imzalı bir ilerleme raporu sunulur. [Geçmiş kılavuzu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/). |
| Günlükteki mevcut sohbet içeriği | Kaynaklar → Kayıt ayarları → Geçmiş anlık görüntüsü | Görünür durumdaki son mesajlar, imzalı gözlemler olarak gösterilir. Varsayılan maksimum sayı 500'dür; **Parametreler → En büyük geçmiş anlık görüntüsü seçeneği ile** bu sayı 10.000'e kadar artırılabilir. |
| Bir sohbetin şu anda görünür olan tam geçmişi | Sohbeti tamamen dışa aktar → Sohbeti tamamen dışa aktar veya Sohbetler → Sohbeti dışa aktar | `chat.json` ve `chat.html` içeren ayrı bir imzalı paket. Kaynak başına tekrarlayın; tamamlanma/başarısızlık sonuçlarını saklayın. |
| Yeni bir sohbet ortaya çıktığında geçerli olan bağlam | Gözlem kapsamı → Yeni bir sohbet veya bot ortaya çıktığında | Bir kaynak profili ve en fazla 1.000 adet son görünür mesaj; Soruşturma modunda 200 adet seçilir. Mevcut sohbetler bu verileri geriye dönük olarak almaz. |
| Ek boyutu | Görünür ekleri indir + tür başına sınırlar | `media.saved` değerini, SHA-256 değerini ve bayt sayısını kontrol edin. Kuyrukta bekleyen, atlanan veya başarısız olan bir indirme, korunmuş bir dosya sayılmaz. |

Sohbetin tam olarak dışa aktarılması ayrı bir anlık görüntüdür; tüm geçmişi günlüğe veya kişi profillerine aktarmaz. TgWitness içinde arama yapmanız gereken geçmiş veriler için, etkinleştirilmiş kaynaklar genelinde "**Tüm geçmişi yükle**" seçeneğini veya sınırlı günlük anlık görüntülerini kullanın. İşlemi başlatmadan önce kaynak listesini gözden geçirin.

İncelenen vakada, duyuru kanalını, operasyon grubunu, botla yapılan sohbeti ve özel takip mesajlarını elde edin. Fatura eklerinin baytlarını ve hash değerlerini koruyun. Bugün mevcut olan geçmiş veriler, yakalanmadan önce silinmiş bir mesajı veya Telegram'ın artık geri getirmediği ara düzenlemeleri yeniden oluşturamaz.

## 3. Gelişen konuşmayı ve kendi eylemlerinizi takip edin

Vaka geliştikçe gözlemi sürdürün. Aktif vaka sohbetlerini öncelikli kaynaklar olarak işaretleyin; öncelik ve diğer kaynaklardan yeniden kontrol ayarlarını **Kayıt ayarları → Yeniden Kontrol** bölümünden yapılandırın. Çalışma ilerledikçe `recheck.completed`, devam eden güncelleme, FloodWait ve medya sonuçlarını gözden geçirin.

Mevcut kaynak açıklamalarını, bot komutlarını ve Telegram'ın döndürdüğü diğer meta verileri korumak için **Sohbetler → Profil → Profili şimdi kaydet seçeneğini** kullanın. Bu kaynak profili, günlük mesajlarından oluşturulan kişi profillerinden ayrıdır.

**Vaka kapsamında bir botu takip etme veya daveti kabul etme**

1. **Sohbetler → Telegram bağlantısını aç** seçeneğinde, önce önizlemeyi kaydedin. Orijinal bağlantı ve görüntülenen önizleme, imzalı kayıtlar haline gelir.
2. Soruşturma gerektiriyorsa, **Join / open**komutu kaynağa katılır veya açar ve sağlanan başlangıç parametresiyle bir botu başlatır. Beklemede olan bir katılım isteği, kayıtta beklemede kalır.
3. Belgelemeniz gereken bir eylem için, panelin metin yanıtını veya desteklenen **"Düğmeye Bas"** kontrolünü kullanın. Günlük, geri gönderilen geri arama metni veya URL dahil olmak üzere `interaction.requested` ve `interaction.result` bilgilerini saklar.

Bu denetimler gerçek Telegram eylemlerini gerçekleştirir. Farklı bir Telegram uygulamasında basılan bir geri arama düğmesi, toplayıcı tarafından görülemez; ancak botun ardından gelen mesajı veya düzenlemesi görülebilir. Web uygulamaları, ödemeler ve telefon/konum talepleri mini istemcinin kapsamı dışındadır.

## 4. Sohbetlerdeki kişileri, bağlantıları ve dosyaları takip edin

1. **Günlüğü** açın, kaynak filtresini "**Tüm kaynaklar**" olarak bırakın ve belirgin bir ifade, etki alanı, kullanıcı adı veya kaydedilmiş bir tanımlayıcıyı arayın. Eşleşen her kaydı açın ve sohbetini, mesaj kimliğini ve günlük sıra numarasını kaydedin.
2. İlgili bir sohbeti incelemek için **Sohbetler → Kişiler → Profilleri aç seçeneğini** açın, ardından bir kişi seçin. İsim/kullanıcı adı geçmişini, yanıt ilişkilerini, etkinliği, **Ayrıca… bölümündeki** diğer gözlemlenen sohbetleri ve çıkarılan bağlantıları, cüzdanları veya telefon numaralarını inceleyin. Alıntılanan kayıt defteri kayıtlarını açın.
3. Aynı sayısal Telegram kullanıcı kimliğini bu çalışma alanındaki diğer sohbetlerde de takip edin. Eşleşen bir isim, cüzdan bahsi veya benzer bir avatarı, kontrol edilmesi gereken bir ipucu olarak değerlendirin. Bahsedilen bir adres, sahipliği kanıtlamaz; benzer bir avatar da aynı kişi olduğunu kanıtlamaz.
4. Kayıtlar arasında saklanan eklerin SHA-256 değerlerini karşılaştırın. Eşleşen hash değerleri, kaydedilen dosyaların bayt düzeyinde özdeşliğini destekler. Bunları kimin paylaştığına dair bir sonuca varmadan önce, ilgili mesaj ve gönderen kayıtlarını inceleyin.

VAKA HARİTASI / KAYNAKLARI İZLEKurgusal vaka · gerçek zamanlı bir grafik değildir

KANAL / DUYURU**Orijinal → düzenlenmiş hedef**

Kayıtlar #101, #188 Mesaj #84 · göndereni belirtilmemiş

GRUP / OPERASYONLAR**Kullanıcı 71001 yeni bağlantıyı paylaşıyor**

Kayıt #146 · mesaj #309 Kaydedilen dosya makbuzu #151

BOT / SİPARİŞ SOHBETİ**Bir düğme bu hedefe yönlendirir**

Kayıt #173 · mesaj #12 Geri Dön düğmesinin meta verileri

ÖZEL / TAKİP**71001 numaralı kullanıcı hedefi tekrarlar**

Kayıt #205 · mesaj #922 Kaydedilen dosya makbuzu #209

Dört sohbet, farklı gözlemler sunmaktadır. Her bağlantı için kaynak kayıtlarını takip edin; göndereni belirtilmemiş kanal gönderisini 71001 numaralı kullanıcıya atamayın.

Sayısal kimlikler ve kayıt referansları bu adım adım kılavuz için uydurulmuştur. Bu şema, bir analistin arama, profiller ve kayıt incelemeyi kullanarak gerçekleştirdiği iş akışını açıklamaktadır; uygulama, genel bir soruşturma grafiği oluşturmaz.

| Bağlantı | Destekleyici gözlem | Korunacak sonuç |
| --- | --- | --- |
| Aynı Telegram hesabı | #146 numaralı grupta ve #205 numaralı özel sohbette 71001 numaralı kullanıcı | Her iki sohbette de aynı gönderen kimliği paylaşılmıştır. Gerçek kimlik ise ayrı bir konudur. |
| Tekrarlanan hedef | `pay.example.invalid/new`, #146; düğme meta verileri, #173; düzenlenmiş gönderiler, #188 ve #205 | Aynı hedef, gözlemlenen dört bağlamda da karşımıza çıkmaktadır. Bu durum tek başına, hedefin kim tarafından kontrol edildiğini ortaya koymaz. |
| Aynı dosya baytları | Tamamlanmış medya makbuzları #151 ve #209'daki SHA-256 değerleri birbiriyle eşleşiyor | Korunan iki ek, bayt düzeyinde aynıdır. Dosya adları veya küçük resimler tek başına bunu kanıtlamaz. |

Kişi profilleri, o sohbette kaydedilmiş mesajları olan yazarları kapsar ve bunları *aynı çalışma alanı*günlüğündeki diğer sohbetlerle ilişkilendirir. Bunlar eksiksiz bir üye dizini değildir. Avatar hash değerleri ayrı bir yerel önbellekten alınır; profil alıntılarının sınırı, **Parametreler → Her bir olaya ilişkin alıntılanan kayıtlar** altında yapılandırılabilir.

## 5. Sırayı yeniden oluşturun ve eksiklikleri işaretleyin

**"Sohbetler"** bölümünde, kaydedilmiş sürümleri ve bunların "**Günlük kaydı #…"** bağlantılarını inceleyin. **"Günlük"** bölümünde, **"Tüm kaynaklar**" ile **"Düzenlemeler**", **"Silme İşlemleri**" ve **"Kapsam"** seçeneklerini kullanın. Sağlanan Telegram tarihi ile toplayıcının gözlem zamanını kullanarak bir vaka zaman çizelgesi oluşturun.

1. 09:00 · #101**Kanal gönderisi yakalandı**

   Orijinal hedef korunmuştur.
2. 09:12 · #146 / #151**Grup farklı bir bağlantı paylaşıyor**

   71001 numaralı kullanıcı bunu yayınlar; ek dosyanın indirilmesi tamamlanır.
3. 09:16 · #173**Bot aynı hedefi gösteriyor**

   Kaydedilen klavye meta verileri bağlantıyı içerir.
4. 09:20 · #188**Kanal duyurularındaki değişiklikler**

   Hem orijinal hem de düzenlenmiş gözlemler korunur.
5. 09:24 · #205 / #209**Özel takip mesajında bu ifade tekrarlanır**

   Kaydedilen ek, #151 ile aynı tam SHA-256 değerine sahiptir.
6. 09:28 · #231**Grup silme bildirimi geldi**

   Daha önceki gözlem hâlâ geçerlidir; ne silen kişi ne de kesin silme zamanı belirtilmiştir.

Açıklayıcı gözlem zamanları ve referanslar. Bu girişler arasında başka günlük kayıtları da yer almaktadır.

Günlük sıralaması, mesajların alındığı sırayı yansıtır; bu, Telegram'daki orijinal eylemlerin sırasıyla aynı olması gerekmez. Daha yeni bir canlı mesajdan sonra, daha eski bir geçmiş anlık görüntüsü gelebilir. Canlı gözlemleri, anlık görüntüleri, kurtarılan mesajları, silme bildirimlerini ve “yeniden kontrol edildiğinde eksik” olanları birbirinden ayrı tutun. Kapsamda bir boşluk olduğu her yerde açıkça “bilinmeyen aralık” ibaresini ekleyin; daha sonraki bir anlık görüntü bu boşluğu ortadan kaldırmaz.

## 6. Uygulamayı diğer toplama hesaplarına genişletin

Her bir ayrı hesap için bir çalışma alanı ekleyin ve kapsam ile geçmiş envanterini tekrarlayın. Her biri için üyelik/rol ve imza anahtarı parmak izini kaydedin. Tanımlayıcıları çalışma alanı ve sohbet bazında nitelendirin: aynı mesaj numarası, hesaplar arası genel bir tanımlayıcı değildir.

Vaka notlarınızda veya analiz araçlarınızda ilgili gözlemleri karşılaştırın; her satır için hesap ve günlük referansını koruyun. TgWitness şu anda çalışma alanları arasında tek bir genel arama, birleştirilmiş zaman çizelgesi, kişi grafiği veya vaka arşivi sunmamaktadır. Bir kanalın veya süper grubun çoklu hesaplı tam dışa aktarımı ayrı bir özelliktir; bu, tüm hesap günlüklerinin birleştirilmesi değildir.

Daha uzun süreli çalışmalar sırasında, önceki sınırları korumak için [bağımsız bir tanık](https://phishdestroy.github.io/TgWitness/tr/docs/witness/) ekleyin. Hesapların yakalama yollarını ve görünürlüğünü doğrulamak için kontrollü teslim pilotunu kullanın.

## 7. Eksiksiz ve doğrulanabilir bir vaka dosyası sunun

Her çalışma alanından imzalı bir günlük ZIP dosyasını dışa aktarın. Bu dosya, panel arama filtrelerinden bağımsız olarak kaydedilen günlüğün tamamını içerir. İlgili kişi profillerini ayrı olarak dışa aktarın, her bir sohbet geçmişi paketini tam olarak koruyun ve eksiksiz ek kanıtlarını muhafaza edin.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Güvenilir parmak izlerini ayrı bir kanal üzerinden saklayın. Güvenilir bir kurulumdan, her bir kanıt parçasını kendi çalışma alanı kimliğiyle karşılaştırarak doğrulayın:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Gerçek doğrulama sonuçlarını kontrol edin, orijinalleri koruyun ve kapsam raporunu, veri toplama hatalarını ve aktarım kayıtlarını bulgularınızla birlikte saklayın. Üst düzey vaka klasörü ve analistlerin sonuçları harici olarak derlenir; her bir TgWitness verisi kendi imzasını taşır.

## Diğer soruşturmalarda da aynı yöntemi kullanın

**Bot kaynaklı bir sipariş veya ödeme anlaşmazlığı**

**Soru:** Bot ne vaat etmişti, hangi düğme hedefi sunulmuştu ve sonrasında ne değişti?

**İzleme:** kanal girişi gönderisi → kaydedilmiş bot bağlantısı önizlemesi → bot başlatma parametresi → mesajlar ve klavye sürümleri → panel tarafından gönderilen herhangi bir geri arama onayı → grup/özel takip. Her bir hedefi kaynak kaydıyla eşleştirin; profil açıklamalarını ve tamamlanmış medya öğelerini koruyun.

**Sunulacaklar:** gözlemlenen teklif ve yanıtların zaman çizelgesi, kaynak referansları ve doğrulanmış dışa aktarımlar. Görüntülenen bir ödeme bağlantısı, ödemenin gerçekleştiğine dair bir kanıt değildir.

**Sohbetler arası bir olayın ardından silinen mesajlar**

**Soru:** İlgili mesajlar kaybolmadan önce neler gözlemlenmişti?

**İzleme:** etkilenen tüm sohbetler → orijinal mesajlar → iletilen düzenlemeler → silme bildirimleri veya daha sonra yeniden kontrol edildiğinde eksik olduğu tespit edilen sonuçlar → saklanan ekler → olayla ilgili haberler. Bağımsız hesap gözlemlerini, belirtilen görünürlük düzeyleriyle karşılaştırın.

**Sunulacak içerik:** Korunmuş sürümlerin bir dizisi ve açıkça belirtilmiş bilinmeyen aralıklar. Geçmişte bulunmayan bir mesajı, belirli bir kişinin onu sildiğine dair kanıt olarak sunmayın.

**Bir katılımcı, birkaç sohbet arasında isimlerini değiştiriyor**

**Soru:** İsim değişikliğine rağmen hangi gözlemlenen etkinlik aynı Telegram hesabına aittir?

**İzleme:** sayısal gönderen kimliği → kaydedilmiş ad/kullanıcı adı geçmişi → yanıtlar → çalışma alanındaki diğer sohbetler → bahsedilen hedefler ve kaydedilmiş dosyalar. İddia edilen her bağlantı için kaynak kayıtlarını kontrol edin; benzer hesapları ayrı tutun.

**Sunulacaklar:** kaynak gösterilmiş hesap etkinlik zaman çizelgesi ve ilişkiler hakkında ayrı ayrı hipotezler. İsim benzerliği ve avatar pHash'i, kimlik kanıtı değil, ipucu niteliğindedir.
