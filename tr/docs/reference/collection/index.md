# Veri toplama süreci nasıl işliyor?

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/

Gözlem kapsamı, canlı güncellemeler, yeniden kontroller, ekler, kendi eylemler ve bir boşluğun ne anlama geldiği, kayıt bazında.

TgWitness, bağlı bir Telegram hesabının gözlemlediklerini kaydeder. Günlük, bu gözlemleri, sıralamalarını ve bunlarla birlikte sağlanan bağlamı korur. Eksik bir mesajdan veya hesabın bağlı olmasından yola çıkarak görülmemiş eylemler hakkında bir sonuca varmaz.

## Girişten günlüğe

Akış şeması · Bir kullanıcı hesabını yetkilendirin → Erişilebilir grupları ve kanalları seçin; Erişilebilir grupları ve kanalları seçin → Olay ve ek ayarlarını kaydet; Olay ve ek ayarlarını kaydet → Gözlemi başlat; Gözlemi başlat → Aktif müşteriden güncellemeleri alın; Aktif müşteriden güncellemeleri alın → Kaynak ve olay politikasını uygulayın; Kaynak ve olay politikasını uygulayın → İmzalı bir gözlem ekleyin; İmzalı bir gözlem ekleyin → Günlüğü inceleyin veya dışa aktarın; İmzalı bir gözlem ekleyin → Kuyrukta bekleyen ekleri işleme; Kuyrukta bekleyen ekleri işleme → İndirme sonucunu ekleyin · Bir kullanıcı hesabınıyetkilendirin · Erişilebilir gruplarıve kanalları seçin · Olay ve ek ayarlarınıkaydet · Gözlemi başlat · Aktif müşteridengüncellemeleri alın · Kaynak ve olaypolitikasını uygulayın · İmzalı bir gözlemekleyin · Günlüğü inceleyin veyadışa aktarın · Kuyrukta bekleyenekleri işleme · İndirme sonucunuekleyin

**Diyagramın metin olarak gösterimi**

1. Bir kullanıcı hesabını yetkilendirin → Erişilebilir grupları ve kanalları seçin
2. Erişilebilir grupları ve kanalları seçin → Olay ve ek ayarlarını kaydet
3. Olay ve ek ayarlarını kaydet → Gözlemi başlat
4. Gözlemi başlat → Aktif müşteriden güncellemeleri alın
5. Aktif müşteriden güncellemeleri alın → Kaynak ve olay politikasını uygulayın
6. Kaynak ve olay politikasını uygulayın → İmzalı bir gözlem ekleyin
7. İmzalı bir gözlem ekleyin → Günlüğü inceleyin veya dışa aktarın
8. İmzalı bir gözlem ekleyin → Kuyrukta bekleyen ekleri işleme
9. Kuyrukta bekleyen ekleri işleme → İndirme sonucunu ekleyin

Yetkilendirme, kaynağa erişim, çalışan bir toplayıcı ve tam teslimat farklı konulardır. Başarılı bir oturum açma işlemi, her gruba erişim hakkı vermez. Bağlantılı bir aktarım, ilgili her güncellemenin ulaştığını garanti etmez.

## Gözlem kapsamı: seçilen sohbetler, bir klasör veya hesabın tamamı

Kaynaklar → **Gözlem kapsamı,** bir çalışma alanının hangi sohbetleri kaydedeceğini belirler.

| Mod | Kayıtlar | Yeni sohbetler |
| --- | --- | --- |
| Seçili sohbetler (varsayılan) | Yalnızca elle eklediğiniz sohbetler | Asla otomatik olarak eklenmez |
| Telegram klasörü | Hesabın klasörlerinden birindeki sohbetler: isme göre dahil edilen sohbetler, ayrıca klasörün kategorileri (kişiler, kişiler dışındaki kişiler, gruplar, kanallar, botlar), hariç tutulan sohbetler ve klasörde belirtilmişse arşivlenmiş sohbetler | Eşleşen sohbetler aktif hale gelir gelmez eklenir; Telegram'da klasöre eklediğiniz sohbetler bir saat içinde alınır. |
| Hesabın tamamı | Hesabın gördüğü her sohbet | Her yeni sohbet, grup, özel sohbet veya bot, ilk güncellemesi geldiği anda eklenir. |

- **Kaynak türleri** (kanallar, gruplar, özel sohbetler, botlar), klasör ve tüm hesap modlarını daraltır. Seçilen sohbetler, özel sohbetler ve botlar dahil olmak üzere herhangi bir türde olabilir.
- **Hariç tutulan sohbetler** hiçbir modda kaydedilmez. Klasör ve tüm hesap modlarında, bir kaynağa "*Hariç Tut"* veya "*Kaldır"* işlemi uygulandığında bu listeye eklenir, böylece kapsam onu tekrar eklemez. Sohbeti manuel olarak yeniden seçmek (Kaynaklar'da veya Sohbetler'den), onu listeden çıkarır. Liste en fazla 5.000 sohbeti barındırır; bu sayıyı aşarsa, *Kaldır işlemi* reddedilir ve bunun yerine sohbet duraklatılabilir.
- **Kendi eylemleri** (varsayılan olarak açıktır): bu hesabın gönderdiği mesajlar, yaptığı düzenlemeler ve yanıt klavyesi düğmesine basışları. Kapalıyken, giden mesajlar ve düzenlemeler atlanır.
- Bir klasöre veya tüm hesaba geçiş yapıldığında onay istenir: bu modlar özel sohbetleri ve üçüncü şahısların mesajlarını kaydeder ve yalnızca bu amaca ayrılmış bir hesapta kullanılmalıdır. Onay ve her kapsam değişikliği, `scope.changed` kayıtlarıyla imzalanır.
- Kapsam tarafından eklenen sohbetler, *"auto"* olarak işaretlenmiş kaynaklar olarak görünür ve `scope.applied` (başlangıçta ve saat başı) veya `source.discovered` (gözlem sırasında yeni bir sohbet) olarak kaydedilir. Seçilen sohbetlere geri dönülmesi, otomatik olarak eklenen tüm kaynakları duraklatır.

Bu modların yapamadıkları şeyler:

- **Gizli sohbetler,** iki cihaz arasında uçtan uca şifrelenir ve hiçbir şekilde, hiçbir modda TgWitness'e ulaşmaz.
- **TgWitness çalışmadığı sürece hiçbir şey kaydedilmez.** Yeniden başlatıldıktan sonra, Telegram’dan kaçırılan güncellemeleri ister ve sohbetleri yeniden kontrol eder, ancak uzun süreli kesintilerden sonra Telegram tüm verileri geri göndermez. Raporlar ve `verify.py`, bu tür dönemleri boşluklar olarak gösterir (bkz. [kapsama alanı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Başlangıçta yalnızca ilk 1.000 diyalog listelenir (sınır, **Parametreler** bölümünde belirtilmiştir); daha eski sohbetler, bir sonraki aktif hale geldiklerinde eklenir. Eklenen bir sohbetin daha önceki geçmişi alınmaz — ihtiyaç duyduğunuzda bir geçmiş anlık görüntüsü alın veya sohbeti tamamen dışa aktarın.
- Sürekli değişen klasör koşulları (sessize alınmış, okunmuş) uygulanmaz: bu tür sohbetler gözlem altında kalır.
- Başka bir uygulamada basılan **satır içi (geri arama) bot düğmeleri**, ikinci bir oturumda görünmez; botun yanıtı veya düzenlemesi kaydedilir. Yanıt klavyesi tuşlarına basıldığında, bunlar giden mesajlar olarak gelir ve `button_press` etiketiyle işaretlenir.
- Sohbet sayısı arttıkça istek sayısı da artar. Telegram, aşırı olarak değerlendirdiği hacimlerde hesaplara kısıtlama uygular; bu da özel hesaplar kullanmanın bir nedeni daha.

## Kapsam ve olay seçimi

Her çalışma alanının kendine ait kaynakları vardır. TgWitness gruplara katılmaz, davetleri kabul etmez veya her üyeyi otomatik olarak listelemez. Kaynaklar, hesap tarafından zaten erişilebilir durumda olmalıdır. Başlangıçta, toplayıcı seçilen kaynakları hesabın görünür sohbetleriyle karşılaştırır; **Parametreler → Hesaptan okunan sohbetler listesinde** aksi belirtilmedikçe ilk 1.000 sohbet incelenir. Yok olan bir kaynak, **erişim onaylanmamış olarak** işaretlenir; sizi kaldırdığı varsayılmaz.

| Ayarlar | Toplar | Devre dışı bırakıldığında etkisi |
| --- | --- | --- |
| Yeni mesajlar | Normal olarak gönderilen mesajlar | Daha sonra yapılan düzenlemeler/silme işlemleri için, karşılaştırma yapılabilecek daha önceki bir metin kaydı bulunmayabilir. |
| Düzenlemeler | Düzenlenmiş mesaj sürümleri sunulur | Ara aşamadaki değişiklikler daha sonra yeniden oluşturulmaz. |
| Silme işlemleri | Kapsamlı silme bildirimleri ve kapsam dışı hesap düzeyinde bildirimler | Silme bildirimleri günlüğe eklenmez. |
| Tepkiler | Anlık tepki görüntüleri sunuldu | Ayrı tepki güncellemeleri eklenmez. |
| Üyelik | Üyelik hizmeti mesajları ve katılımcılara yönelik güncellemeler iletildi | Bu üyelik gözlemleri eklenmemiştir. |

Ayarlar, çalışma alanındaki tüm seçili kaynaklar için geçerlidir. Değişiklikleri uygulamak için formu kaydedin; değişiklikler, imzalı "önce" ve "sonra" değerleriyle kaydedilir. Bir kategoriyi devre dışı bırakmak, önceki kayıtları silmez. Kategoriyi yeniden etkinleştirmek, kaçırılan güncellemeleri geriye dönük olarak doldurmaz.

Operasyonel kayıtlar ve diğer grup hizmeti olayları bu ayar değişikliklerinden bağımsız olarak kalır. Üyelik hizmeti mesajları, üyelik etkinleştirildiğinde, normal yeni mesaj yakalama devre dışı olsa bile mesaj kayıtları oluşturabilir. Yakalanan Telegram nesneleri gömülü meta verileri korur; bir ayar değişikliği, bir sansür kuralı değildir.

**Özel sohbetlerdeki ve normal gruplardaki silme işlemleri**, sohbet bilgisi olmadan mesaj kimlikleri olarak gelir. Bu sohbetler, hesap genelinde tek bir mesaj kimlik dizisini paylaşır; bu nedenle, o kimliğe sahip bir mesaj daha önce kaydedilmişse, ilgili sohbet bilinir: silme işlemi o sohbette kaydedilir ve nasıl yapıldığı `chat_resolution` ile açıklanır. Hiç kaydedilmemiş kimlik numaraları, kaynağı açıkça bilinmeyen, **kapsamı belirlenmemiş**bir **silme** işlemi olarak kalır; toplayıcı tahminde bulunmaz. Telegram, bir mesajı kimin sildiğini asla belirtmez; silinen mesaj bu hesap tarafından gönderilmişse, kayıtta (`deleted_message_was_outgoing`) silen kişinin adı belirtilmeden bu durum belirtilir.

## Kendi eylemleri

İzlenen hesap tarafından gönderilen mesajlar `outgoing` olarak etiketlenir. Giden bir mesajın düzenlenmesi durumunda, özel sohbetlerde ve gruplarda yalnızca yazarın mesajı düzenleyebileceği, kanal gönderilerinin ise diğer yöneticiler tarafından düzenlenebileceği belirtilir. Giden bir mesaj, o sohbetteki en son kaydedilmiş yanıt klavyesindeki bir düğmenin metnini tekrar ettiğinde, klavyenin kaydına bir bağlantı içeren `button_press` etiketini taşır.

Kendi eylemlerin hariç tutulması, arka plan yeniden kontrolleri ve otomatik yeni sohbet geçmişi için de geçerlidir. Atlanan giden mesajlar, yeniden kontrol konumunu ilerletir; böylece daha sonra gelen mesajları engelleyemezler. Açıkça belirtilen panel eylemleri ve manuel olarak talep edilen geçmiş anlık görüntüleri kaydedilmeye devam eder.

## Soruşturma modu: ekiplere katılma ve botlarla iletişim kurma

**Kaynaklar → Gözlem kapsamı → Soruşturma modu**, takım sohbetlerine katılan, botları başlatan ve bunlara mesaj yazan özel bir hesap için kapsamı hazırlar: hesabın tamamı, her kaynak türü, kendi eylemleri ve görünen her sohbet veya bot için profil ve en son 200 görünür mesaj. Formu gözden geçirip **Kapsamı Kaydet** düğmesine basın; tüm hesaba geçiş için her zamanki gibi onay istenir.

- **Düğmeler.** Bir mesajın altındaki düğmeler o mesajla birlikte tutulur ve **Sohbetler'**de gösterilir: bağlantılar, web uygulamaları, oturum açma bağlantıları, kopyalanacak metinler, geri arama verileri, satır içi sorgular, telefon numarası veya konum talepleri. Bağlantılar metin olarak gösterilir ve panel tarafından asla açılmaz. Bir bot yalnızca düğmeleri değiştirdiğinde (yeni bir ödeme bağlantısı gibi), bu hem canlı güncellemeler hem de yeniden kontroller açısından mesajın yeni bir sürümüdür.
- **Yeni sohbetler ve botlar.** Klasör ve tüm hesap modlarında, **yeni bir sohbet veya bot ortaya çıktığında**, ortaya çıkar çıkmaz kaydedilir:

  - `source.profile` kaydı olarak profili: bot açıklaması ve komutları, bir kullanıcı, grup veya kanalın hakkında metni, üyeler, Telegram tarafından sağlandığında bağlantılı sohbet ve davet bağlantısı ;
  - `new_chat` olarak işaretlenmiş bir geçmiş anlık görüntüsü olarak en son görünür mesajları (en fazla 1.000): az önce katıldığınız bir grup sohbetinin önceki mesajları veya gözlem, sohbeti fark etmeden önce bir botun söyledikleri. Canlı olarak zaten kaydedilmiş mesajlar tekrarlanmaz.

  Mod etkinleştirildiğinde listede zaten bulunan sohbetler, anlık görüntü alınmadan eklenir. Bir FloodWait bu işlemi duraklatır ve daha sonra devam ettirir; hatalar kaydedilir ve sohbetin canlı kaydı devam eder. - **İsteğe bağlı profiller. Sohbetler → Profil → Profili Kaydet seçeneği artık** herhangi bir kaynağın mevcut profilini kaydediyor; en yeni profil mesajların üzerinde gösterilir. - **Görünmez.** Başka bir Telegram uygulamasında basılan satır içi (geri arama) düğmeleri, bir botun bu tür bir basışa yanıt verdiği açılır pencere veya bağlantı ve başka bir uygulamada kullanılan davet bağlantıları TgWitness'e ulaşmaz. Botun daha sonra gönderdiği veya düzenlediği içerikler kaydedilir.

### Panelden hareket edin

**Sohbetler** artık, seçilen çalışma alanının Telegram hesabını kullanan bir mini istemci içerir:

- Düz metin bir mesaj yazın veya kaydedilmiş bir mesajın altındaki **"Yanıtla" seçeneğini** seçin. Geri gönderilen mesaj, kapsam giden güncellemeleri hariç tutsa bile kaydedilir.
- Mevcut bir geri arama veya metin düğmesinin altındaki **Bas düğmesine** basın. Sunucu, mesajı tekrar alır ve klavye girişi kaydedilen sürümden farklıysa işlemi reddeder. Geri arama makbuzları, Telegram'ın açılır pencere metnini, uyarı bayrağını ve URL'yi korur; yanıt ayrıca sohbetin altında da gösterilir. URL'ler seçilebilir metin olarak kalır ve otomatik olarak açılmaz.
- **Telegram bağlantısını** genişletin, `@username`, halka açık bir `https://t.me/name` bağlantısı, `https://t.me/+invite` / `joinchat/invite` veya `?start=parameter` içeren bir bot bağlantısı girin ve " **Önizlemeyi Kaydet**"e basın. Katılmadan önce orijinal bağlantı ve Telegram önizlemesi imzalanır. **Katıl / aç ve gözlemle** seçeneği, gruba/kanala katılır veya kullanıcıyı/botu açar, sohbeti etkin bir kaynak olarak ekler ve başlangıç parametresini de içeren `/start` kodunu bir bota gönderir. Yönetici onayı bekleyen bir katılma isteği, üyelik olarak değil, beklemede olan bir istek olarak kaydedilir.

Gelen yanıtları anlık olarak yakalamak için **"Gözlemi Başlat"** seçeneğini etkinleştirin. Gözlem duraklatıldığında panel eylemleri çalışmaya devam eder, ancak bu durumda yalnızca doğrudan yanıtların kaydedileceği garanti edilir. Gözlem çalışırken, yeni eklenen kaynaklar yapılandırılmış profil/geçmiş alımını kullanır. Bir kaynak duraklatıldığında, gönderim yapmadan veya düğmelerine basmadan önce "**Kaynaklar"** bölümünden bu kaynağı etkinleştirin.

`interaction.preview`, `interaction.requested` ve `interaction.result`, kanıt dışa aktarımlarına dahil edilen sıradan imzalı günlük olaylarıdır. İstekler, hesabı, mesajı/düğmeyi veya önizleme kaydını ve gözlemin çalışıp çalışmadığını belirtir. Makbuzlar, başarı, red, onay bekliyor ve bilinmeyen sonuç durumlarını ayırt eder. Kesintiye uğrayan bir istek Telegram'a ulaşmış olabilir: yeni bir eyleme başlamadan önce sohbeti kontrol edin. Bir istek kimliğini yeniden kullanmak, yeniden başlatma sonrası da dahil olmak üzere, eylemi tekrarlamadan kaydedilmiş makbuzu getirir. Panel, mevcut sayfa oturumu sırasında aynı eylem için belirsiz bir yanıt alındığında kimliği saklar. Ayrıca, başarılı bir eylemden sonra görünümün yenilenmesi başarısız olduğunda da bu kimliği saklar: makbuz görünür kalır ve tekrar tıklandığında geri getirilir. Geri arama ve katılma RPC’leri için tek bir uygulama denemesi vardır; yeniden denenebilir okumalar, yapılandırılmış yeniden deneme politikasını korur. Sohbetler arasında anında geçiş yapıldığında taslak ve yanıt hedefi silinir ve yeni sohbet yüklenene kadar gönderim devre dışı bırakılır.

Bu mini istemci, metin ve geri arama düğmelerini yönetir. Web uygulamaları, oturum açma/telefon/konum istekleri, ödemeler, satır içi sorgular ve ekler için hâlâ bir Telegram istemcisi gereklidir; kaydedilen düğme meta verileri görünür kalır. Yeni denetimlerde İngilizce metin kullanılır.

## Seviyeleri yeniden kontrol edin

Yeniden kontrol işlemi, Telegram'dan kaçırılan mesajları, düzenlemeleri ve artık döndürülmeyen mesajları tekrar ister. Yıldız işaretli kaynaklar **öncelikli** kaynaklardır ve varsayılan olarak her 15 dakikada bir yeniden kontrol edilir; diğer tüm kaynaklar ise her 6 saatte bir kontrol edilir. Seçilen sohbetler öncelikli kaynaklar olarak başlar; bir klasör veya tüm hesap tarafından eklenen sohbetler ise normal kaynaklar olarak değerlendirilir. Her turda en fazla 30 kaynak yeniden kontrol edilir ve geri kalanı bir sonraki dakikayı bekler; yeniden bağlanmanın ardından öncelikli kaynaklar ilk sırada yer alır. Her iki aralık da Kaynaklar → Kayıt ayarları → Yeniden Kontrol altında ayarlanır (0, bir kademenin devre dışı bırakılması anlamına gelir) ve `recheck.changed` olarak kaydedilir.

Kaçırılan mesajlar, önceki taramanın durduğu yerden itibaren, tarama başına en fazla **Parametreler → yeniden kontrol başına yeni mesaj sayısı** (varsayılan olarak 1.000) kadar alınır. Uzun bir duraklamadan sonra, yeniden kontrol işlemi bu nedenle tüm boşluğu doldurur; bu boşluktan daha yeni olan canlı mesajlar önce kaydedilmiş olsa bile. Hala geride kalan bir sohbet, kademeli aralığını beklemek yerine bir sonraki dakikada yeniden kontrol edilir; işlem tamamlanana kadar `recheck.completed`, `continues_after` olarak gösterilir.

Karşılaştırmalar arasında mesaj metni, varlıklar, klavye girişleri (silme işlemleri dahil) ve ek içeriği/kimliği yer alır. Yalnızca dosya erişim hash'lerinin veya dosya referanslarının değiştirilmesi bir düzenleme oluşturmaz; Telegram'ın kendi kendine doldurduğu unsurlar da düzenleme sayılmaz: bir bağlantı önizlemesinin yüklenmesi, hikaye görüntülemeleri, bu hesap tarafından kilidi açılan ücretli medya içerikleri, bir faturanın makbuzu. Sohbetler'de kaydedilen her sürüm, medya meta verileri de dahil olmak üzere tam günlük kaydına bağlanır.

## Mesaj geçmişi ve kaynak gösterimi

Toplayıcının önce “10:00’da toplantı” ifadesini gözlemlediğini, daha sonra “11:00’da toplantı” ifadesini gördüğünü ve ardından bir silme bildirimi aldığını varsayalım. Bu durumda üç farklı gözlem eklenir. Orijinal metin kalır, düzenleme ayrı bir sürüm olarak kaydedilir ve bildirimde bir silme işleminin gözlemlendiği belirtilir.

Toplama işlemi ilk sürümün ortadan kalkmasından sonra başlamışsa, o metne erişilemez. İşlem çevrimdışıyken birkaç düzenleme yapılmışsa, yalnızca daha sonra gözlemlenen sürümler kaydedilebilir. Silme bildirimi, hiç yakalanmamış içeriği geri getiremez.

Mesajı gönderen kişi otomatik olarak düzenleyen kişi değildir. Telegram genellikle mesajı silen kişinin kimliğini veya tam silme zamanını belirtmez. Kimliği bilinmeyen kişiler bilinmeyen olarak kalır. Tepki anlık görüntüleri ve katılımcı güncellemeleri, yalnızca Telegram'ın hesaba gösterdiği sayı ve kimlikleri içerir.

Sıra numaraları gözlem sırasını ifade eder. Toplayıcının UTC zaman damgası, yerel saatine aittir; Telegram kaynak zaman damgası, sağlandığında ayrı olarak saklanır. Her ikisi de bağımsız ve güvenilir bir zaman damgası değildir.

## Geçmiş anlık görüntüleri

Bir anlık görüntü, etkinleştirilmiş bir kaynaktan en son görünen mesajları ister; istek başına en fazla 500 adede kadar. Sonuçlar, geçmiş gözlemleri olarak etiketlenir. Bunlar, canlı yakalama ile çakışabilir ve tekrarlanan gözlemler ayrı kayıtlar olarak saklanır.

Anlık görüntüler ek dosya politikasına uyar, ancak canlı olay anahtarlamalarından ayrı tutulur. Silinen mesajları veya kaçırılan ara sürümleri yeniden oluşturmazlar. Duraklatılmış durumdayken bir anlık görüntü talep edebilirsiniz; kuyruğa alınan ek dosyalar, gözlem başlayana ve indirme işleyicisi çalışana kadar bekler.

## Eklerin işlenmesi

Ek indirme özelliği varsayılan olarak etkindir ve 1 GiB'den az boş disk alanı kaldığında duraklatılır. Toplayıcı, mesaj gözlemleme ve indirme işini birlikte gerçekleştirir. İş, orijinal medya tanımlayıcısını ve boyut politikasını korur; böylece daha sonra düzenlenmiş bir ek, fark edilmeden değiştirilmez.

İndirmeler, mesaj yakalandıktan sonra gerçekleştirilir. Tamamlanan bir indirme işlemi, SHA-256 değeri ve bayt sayısını içeren bir `media.saved` kaydı oluşturur. Atlanan, başarısız olan, yeniden denenen ve kesintiye uğrayan işlemlerin ayrı sonuçları vardır. Kuyruğa alınan bir iş, dosyanın korunduğunun kanıtı değildir. Tamamlanan dosya, gözlemlenen orijinal ek tanımlayıcısındaki bayt sayısıyla da eşleşmelidir. Kısa veya beklenmedik şekilde uzun bir yanıt, korunmuş medya olarak kaydedilmez.

Sınırlar **türlere göre** belirlenmiştir: fotoğraflar, videolar, GIF'ler ve animasyonlar, yuvarlak video mesajları, sesli mesajlar, müzik ve ses dosyaları, çıkartmalar ve dosyalar. Her tür ayrı ayrı devre dışı bırakılabilir ve 1 ile 2.000 MiB arasında kendi boyut sınırına sahiptir; yeni çalışma alanları fotoğraflar için 20 MiB, videolar için 100 MiB, dosyalar, ses ve yuvarlak videolar için 50 MiB, sesli mesajlar ve GIF'ler için 20 MiB ve çıkartmalar için 5 MiB ile başlar. Yeni çalışma alanlarında GIF’ler ve çıkartmalar etkinleştirilene kadar devre dışıdır. Tür bazında sınırlar belirlenmeden önce kayıtlı ilkeler bulunan çalışma alanlarında tüm türler etkin kalır ve her tür için tek bir sınır korunur. *Maksimum dosya boyutu*, tüm türler için aynı anda belirlenir. Devre dışı bırakılan bir tür, `media.skipped` kaydı oluşturur; boyutu bilinmeyen veya sınırı aşan dosyalar indirilmez. Büyük dosyalar, boyutlarına ve 256 KiB/s temel hıza göre ek indirme süresine sahip olur. İşler, yeniden başlatma işleminden sonra da devam eder, ancak süresi dolmuş referanslar, erişim kaybı veya silinmiş dosyalar yine de kurtarmayı engelleyebilir. Bekleyen işler, kendileriyle birlikte kaydedilen sınırı korur; bu nedenle, artırılan sınır yalnızca yeni dosyalara uygulanır. Bir türü devre dışı bırakmak veya sınırını düşürmek, hariç tutulan bekleyen dosyaları da atlar; her bir dosya için `media.skipped` kaydı oluşturulur; indirmeleri devre dışı bırakmak, tekrar etkinleştirilene kadar kuyruğu duraklatır.

## Duraklatma, kilitleme, bağlantıyı kesme ve yeniden başlatma

| Eylem veya durum | Etki |
| --- | --- |
| Çalışma alanını değiştir | Panel görünümünü değiştirir; diğer toplayıcılar durumlarını korur. |
| Paneli kilitleyin veya sekmeyi kapatın | Sunucu ve gözlem işlemi çalışır durumda kalır. |
| Gözlemi duraklat | Toplayıcıyı durdurur ve kuyrukta bekleyen ek işlemlerini korur. |
| Bir kaynağı devre dışı bırak | Gelecekteki kapsamlı yakalamayı durdurur; devre dışı bırakıldığı süre boyunca bunun için kuyruğa alınmış medya işleri beklemeye alınır. |
| Bir kaynağı kaldır | Kaynak olarak dikkate alınmaz ve kullanıcı profilleri silinir; önceden kaydedilmiş veriler yalnızca ekleme yapılabilen günlüğünde kalır. Hala beklemede olan ekler, başarısız (`source_removed`) olarak kaydedilir. Klasör ve tüm hesap modlarında da hariç tutulur. |
| Bağlantı yolunu değiştirin | Bir süre bekleme gerektirir, eski istemcileri kapatır ve tamamlanmamış oturum açma işlemlerini iptal eder. |
| Python sürecini durdurun | Tüm çalışma alanlarını durdurur; çevrimdışı olduğu sürece herhangi bir gözlem yapılmaz. |
| Aktif gözlemden sonra yeniden başlat | Kaydedilen oturumu kullanarak kaydedilen kapsamı devam ettirmeye çalışır. Manuel olarak duraklatma işlemi bu niyeti iptal eder. |

Toplayıcı, algılanan bağlantı kesintilerini, yeniden denemeleri, hataları, başlatma/durdurma işlemlerini ve kalp atışlarını kaydeder. Kısa süreli kesintiler, periyodik bağlantı kontrolleri sırasında gözden kaçabilir. Yeniden başlatmanın ardından, kaçırılan güncellemeler kaydedilen güncelleme konumundan talep edilir ve izlenen sohbetler periyodik olarak yeniden kontrol edilir; [kanıt formatına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#durable-collection-and-process-receipts-02) bakınız. Anlık görüntü bağlam sağlar; bir boşluğun giderildiğini kanıtlamaz.

## Hesap izolasyonu ve doğrulama

Her çalışma alanının kendine ait bir günlüğü, yetkilendirme sistemi, imzalama anahtarı, politikası ve kuyruğu vardır. Yalnızca aktif istemcisi canlı gözlemler ekleyebilir. Reddedilen, beklemede olan, yerine yenisi gelen ve bağlantı testi yapan istemciler, günlüğüne canlı güncellemeler yazamaz. Farklı hesaplar aynı grubu gözlemleyebilir, ancak günlükleri ayrı kalır.

Her olay, önceki hash değerini ve bir Ed25519 imzasını içerir. Dışa aktarımlar, sabit bir sıra numarası aracılığıyla tüm çalışma alanı günlüğünü kapsar. Panel filtreleri, dışa aktarımı filtrelemez; hazırlık aşamasındayken toplama işlemi sınırların ötesinde devam edebilir.

**Doğrulama günlüğü,** görüntülenen sınır aracılığıyla olay zincirini ve imzaları kontrol eder. Çalışma alanı değiştiğinde sonuç silinir ve panel, kontrolün ardından eklenen yeni kayıtları tanımlar. ZIP dışa aktarma işlemi, toplanan medya dosyalarını da doğrular.

Geçerli bir imza, Telegram'ın kaynağı veya içeriğin doğruluğu değil, güvenilir anahtara göre bütünlüğü teyit eder. Parmak izlerini ve kontrol noktalarını bağımsız olarak saklayın. Güven ve teslimat gereklilikleri için [kanıt model](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)ine, [günlük işlemlere](https://phishdestroy.github.io/TgWitness/tr/docs/reference/operations/) ve [canlı kabul prosedürüne](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) bakın.
