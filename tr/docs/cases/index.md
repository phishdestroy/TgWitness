# Tüm sohbetleri inceleyin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/cases/

Kanallar, gruplar, özel sohbetler ve botlar boyunca koca bir dava: topla, noktaları birleştir, zaman çizelgesini yeniden kur, teslim et.

Baştan sona uydurma bir olay. Toplama, arama ve kişi profilleri kayıtları bulur, [Case Board](https://phishdestroy.github.io/TgWitness/tr/docs/case-board/) düzenler, [Report studio](https://phishdestroy.github.io/TgWitness/tr/docs/reports/) sunar.

ÇÖZÜLMÜŞ VAKA / DEĞİŞTİRİLEN ÖDEME HEDEFİ

### Tek bir olay. Dört konuşma. Yeniden canlandırılması gereken bir iz.

Bir kanal gönderisi bir bota yönlendirir. Bir grup yeni bir ödeme bağlantısından söz eder ve bot onu gösterir. Gönderi düzenlenir, özel bir sohbet bağlantıyı tekrarlar, bir grup mesajı kaybolur.

Her bir sürümü kim yayınladı?Bağlantı nerede göründü?Hangi dosya saklandı?Neler değişti ve ne zaman?

Geçmiş yükleme, yapay zekâ, MCP, OCR ve webhook'lar: [Arşivle çalışmak](https://phishdestroy.github.io/TgWitness/tr/docs/archive/).

## 1. Hesabın tamamını kapsayacak şekilde kapsam oluşturun

Tüm hesap kapsamı yalnızca ayrı bir hesapta. Ana hesap seçili sohbetler ya da bir klasörle sınırlı kalır.

1. [Hesabı bağlayın](https://phishdestroy.github.io/TgWitness/tr/docs/accounts/), kendi çalışma alanında. Dava referansını, hesap kimliğini, çalışma alanını ve anahtar parmak izini not edin.
2. **Kaynaklar → Gözlem kapsamı → Soruşturma kipi**: **Tüm hesap**, dört kaynak türünün hepsi, **Kendi eylemleri**. Her yeni sohbetin profili ve son **200 görünür mesajı** kaydedilir. **Kapsamı kaydet** ve onaylayın.
3. **Sohbetleri yükle** ve hesabın sohbet listesiyle karşılaştırın. Sınır 1.000 sohbettir (**Parametreler → Hesap listesinden okunan sohbetler** ile 20.000'e kadar); ötesindekiler etkinleştiklerinde görünür.
4. **Kayıt ayarları** → **Tüm görünür etkinlik**, ek sınırlarını ve disk alanını kontrol edin. Başlatın, sonra bir mesaj, bir düzenleme ve bir silmeyle test edin.

KanallarGruplarÖzel sohbetlerBotlar

TEK HESAP / TEK İMZA ANAHTARI**Seçilen tüm hesapta görülebilen etkinlikler → tek bir günlük**

Mesajlar · düzenlemeler · silme bildirimleri · görünür tepkiler · üyelik etkinlikleri · kendi eylemleri

"Tüm hesap", istisnalar dışında bu hesabın açabildiği her sohbettir. Gizli sohbetler yok. Yeni sohbetler ortaya çıktıkça eklenir; eski geçmiş kendiliğinden indirilmez.

## 2. Geçmişi elde etme ve dosyaları koruma

Bir Case Board koleksiyonu oluşturun ve önemli olanları işaretleyin. Bir kaynak kaydı tutun: sohbet kimliği, başlık, hesap, rol, canlı yakalamanın başlangıcı, geçmiş sonucu, medya sonucu, boşluklar.

| İhtiyaç | Paneldeki eylem | Neler sunar? |
| --- | --- | --- |
| Etkinleştirilmiş sohbetlerdeki geçmiş | Kaynaklar → Tüm geçmişi yükle | Erişilebilir geçmiş mesajlar, duraklatma/devam ettirme ve imzalı bir ilerleme raporu ile birlikte çalışma alanı günlüğüne girer. [Geçmiş kılavuzu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/). |
| Günlükteki mevcut sohbet içeriği | Kaynaklar → Kayıt ayarları → Geçmiş anlık görüntüsü | Son mesajlar imzalı kayıtlar olarak. Varsayılan 500, **Parametreler → En büyük geçmiş anlık görüntüsü** ile 10.000'e kadar. |
| Bir sohbetin şu anda görünür olan tam geçmişi | Sohbeti tamamen dışa aktar → Sohbeti tamamen dışa aktar veya Sohbetler → Sohbeti dışa aktar | `chat.json` ve `chat.html` içeren ayrı bir imzalı paket, sohbet başına bir tane. |
| Yeni bir sohbet ortaya çıktığında geçerli olan bağlam | Gözlem kapsamı → Yeni bir sohbet veya bot ortaya çıktığında | Profili ve en fazla 1.000 son mesajı (soruşturma kipinde 200). Mevcut sohbetlere uygulanmaz. |
| Ek boyutu | Görünür ekleri indir + tür başına sınırlar | SHA-256 ve boyutla birlikte `media.saved` arayın. Kuyrukta, atlandı ya da başarısız demek kaydedilmedi demektir. |

Bir sohbet dışa aktarımı günlüğe ya da kişi profillerine girmez. TgWitness içinde eski geçmişte aramak için **Tüm geçmişi yükle**'yi ya da anlık görüntüleri kullanın.

Burada: kanal, grup, bot sohbeti ve özel sohbet, artı fatura dosyası ve karması. Yakalamadan önce silinen geri gelmez.

## 3. Gelişen konuşmayı ve kendi eylemlerinizi takip edin

Çalışmaya devam etsin. Sıcak sohbetleri yıldızla öncelikli yapın, yeniden kontrolleri **Kayıt ayarları → Yeniden kontrol**'de ayarlayın ve `recheck.completed`, FloodWait ve medya sonuçlarını izleyin.

**Sohbetler → Profil → Profili şimdi kaydet**, sohbet açıklamasını, bot komutlarını ve diğer üst verileri kaydeder.

**Vaka kapsamında bir botu takip etme veya daveti kabul etme**

1. **Sohbetler → Telegram bağlantısı aç**, önce önizlemeyi kaydedin. Bağlantı ve önizleme imzalı kayıt olur.
2. Gerekirse **Katıl / aç ve gözle** sohbete katılır ya da botu başlangıç parametresiyle başlatır.
3. Bir eylemi belgelemek için panelden yanıtlayın ya da **Düğmeye bas**'ı kullanın. Botun yanıtıyla birlikte `interaction.requested` ve `interaction.result` alırsınız.

Bunlar gerçek eylemlerdir. Başka bir uygulamada basılan düğmeler görünmez, yalnızca botun yanıtı görünür. Web uygulaması, ödeme ya da telefon/konum yok.

## 4. Sohbetlerdeki kişileri, bağlantıları ve dosyaları takip edin

1. **Günlük**, **Tüm kaynaklar**, bir ifade, alan adı ya da kullanıcı adı arayın. Sonuçları açın ve **Panoya** gönderin.
2. **Sohbetler → Kişiler → Profilleri aç**, bir kişi seçin: ad geçmişi, yanıtlar, etkinlik, **Ayrıca şurada…**, bağlantılar, cüzdanlar, telefonlar. Alıntılanan kayıtları açın.
3. Aynı sayısal kullanıcı kimliğini diğer sohbetlerde izleyin. Eşleşen bir ad, cüzdan ya da avatar ipucudur, kanıt değil.
4. Dosya karmalarını karşılaştırın. Aynı SHA-256 = aynı baytlar. Onları kimin paylaştığı ayrı bir soru.

VAKA HARİTASI / KAYNAKLARI İZLEKurgusal vaka · gerçek zamanlı bir grafik değildir

KANAL / DUYURU**Orijinal → düzenlenmiş hedef**

Kayıtlar #101, #188 Mesaj #84 · göndereni belirtilmemiş

GRUP / OPERASYONLAR**Kullanıcı 71001 yeni bağlantıyı paylaşıyor**

Kayıt #146 · mesaj #309 Kaydedilen dosya makbuzu #151

BOT / SİPARİŞ SOHBETİ**Bir düğme bu hedefe yönlendirir**

Kayıt #173 · mesaj #12 Geri Dön düğmesinin meta verileri

ÖZEL / TAKİP**71001 numaralı kullanıcı hedefi tekrarlar**

Kayıt #205 · mesaj #922 Kaydedilen dosya makbuzu #209

Dört sohbet, farklı gözlemler sunmaktadır. Her bağlantı için kaynak kayıtlarını takip edin; kanal gönderisinin atfedilmiş bir göndereni yoktur.

Sayısal kimlikler ve kayıt referansları bu adım adım kılavuz için uydurulmuştur. Bu açıklayıcı harita, arama sonuçlarını, profilleri ve incelenen kayıtları nasıl birbirine bağlayacağınızı gösterir; Case Board, ilgili kartları ve kaynak referanslarını saklar.

| Bağlantı | Destekleyici gözlem | Korunacak sonuç |
| --- | --- | --- |
| Aynı Telegram hesabı | #146 numaralı grupta ve #205 numaralı özel sohbette 71001 numaralı kullanıcı | İki sohbette de aynı gönderen kimliği. Gerçek hayatta kim olduğu başka bir soru. |
| Tekrarlanan hedef | `pay.example.invalid/new`, #146; düğme meta verileri, #173; düzenlenmiş gönderiler, #188 ve #205 | Aynı bağlantı dört yerde. Onu kimin kontrol ettiği için başka kaynaklar gerekir. |
| Aynı dosya baytları | Tamamlanmış medya makbuzları #151 ve #209'daki SHA-256 değerleri birbiriyle eşleşiyor | İki dosya bayt bayt aynı. |

Profiller yalnızca *bu çalışma alanında* bir şey yazmış kişileri kapsar, üye listesi değildir. Olgu başına alıntı: **Parametreler → Olgu başına alıntılanan kayıt**.

## 5. Sırayı yeniden oluşturun ve eksiklikleri işaretleyin

**Sohbetler**'de sürümler, sonra **Günlük**'te **Tüm kaynaklar** + **Düzenlemeler**, **Silmeler**, **Kapsam**. Zaman çizelgesine iki zamanı da koyun: Telegram tarihi ve gözlem anı.

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

Günlük sırası varış sırasıdır, olayların sırası olmak zorunda değildir. Canlı kayıtları, anlık görüntüleri, kurtarılan mesajları, silmeleri ve "yeniden kontrolde bulunamadı"yı ayrı tutun ve her boşluğu bilinmeyen olarak işaretleyin.

## 6. Uygulamayı diğer toplama hesaplarına genişletin

Hesap başına bir çalışma alanı, aynı adımlar. Her birinin rolünü ve parmak izini not edin. Mesaj numaraları hesaba özgüdür, bu yüzden çalışma alanını ve sohbeti her zaman belirtin.

Bir [hesap grubu](https://phishdestroy.github.io/TgWitness/tr/docs/groups/) durumu gösterir, ayarları paylaşır ve herkesi birlikte dışa aktarır; her biri kendi günlüğü ve anahtarıyla. Hesaplar arası zaman çizelgesini notlarınızda kurarsınız.

Uzun bir dava mı? Bir [bağımsız tanık](https://phishdestroy.github.io/TgWitness/tr/docs/witness/) ekleyin ve her hesabın gerçekte neyi yakaladığını test edin.

## 7. Doğrulanabilir bir vaka paketi sunun

Her çalışma alanından imzalı bir ZIP (her zaman tüm günlük, süzgeçler fark etmez), artı kişi profilleri, sohbet dışa aktarımları ve dosyalar.

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

Parmak izlerini ayrı gönderin. Her şeyi kendi çalışma alanına karşı doğrulayın:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Doğrulayıcı çıktısını, orijinalleri, kapsamı ve teslim kaydını bulgularınızla birlikte saklayın. Hepsini Report studio'da yazın. Alıcıya daha azı gerekiyorsa [küçültülmüş bir teslim](https://phishdestroy.github.io/TgWitness/tr/docs/handover/) hazırlayın.
