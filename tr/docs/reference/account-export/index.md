# Telegram · Hesap dışa aktarma

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/account-export/

Bir hesabın şu anda okuyabileceği içeriği dışa aktarın: kapsam, devam ettirilebilir işler, imzalanmış bir arşiv ve küçültülmüş paylaşım kopyaları.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Kanıt ve doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)

![Kanıt ve doğrulama](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

Hesap dışa aktarımı hesabı yalnızca kendisi için ayırır. Başlatmadan veya sürdürmeden önce izlemeyi ya da diğer veri toplama görevini açıkça duraklatın; uygulama bunları otomatik olarak durdurmaz.

Kurulum yöneticisi olarak, **Buradan başla → Hesabımı dışa aktar seçeneğini** veya **Dışa Aktarmalar → Telegram hesabı → Hesap dışa aktarımını yapılandır seçeneğini** seçin. Gerekirse oturum açın, kapsamı gözden geçirin ve dışa aktarmayı açıkça başlatın. Sürekli gözlem gerekli değildir. "**Kaydedilen gözlemler**", mevcut günlüğün ayrı bir dışa aktarımdır; ZIP, günlük filtrelerinden bağımsız olarak tüm kaynakları içerir. Her çalışma alanının kendi işleri, imzalama kimliği ve depolama alanı vardır. Sınırsız normal dışa aktarma izni dahil olmak üzere verilen panel erişimi, bu hesap genelindeki yolları açamaz.

Gönderen ve metin filtreleri, **“Gönderen veya mesaj metnine göre filtrele”** seçeneğinin altında açılır. **“Hesap verileri ve bağlantı yöntemi” bölümü,** isteğe bağlı hesap kategorilerini ve “Takeout/normal oturum” seçeneğini içerir; özeti, kapalıyken bile etkin seçenekleri gösterir. Bu bölümler kapatıldığında ayarları korunur. Dışa aktarma ve rapor taslakları, görünüm değiştirilirken mevcut panel oturumunda kalır; tarayıcı yeniden yüklendiğinde kaydedilmez. Mevcut işlere her iki dışa aktarma seçeneğinden de erişilebilir.

Bu iş akışı, bağlı hesaba şu anda erişilebilen verileri dışa aktarır. Varsayılan olarak [Telegram Takeout](https://core.telegram.org/api/takeout) kullanılır; bu, erişilemeyen veya silinmiş Telegram verilerinin yedeği değildir. Gizli Sohbetler, erişilemeyen geçmiş ve önceki düzenlemeler kurtarılamaz. Telegram, Takeout işleminin başlamasından önce bir bekleme süresi uygulayabilir. Panel bu bekleme süresini gösterir; aktarım yöntemini sessizce değiştirmez. Açıkça belirtilen normal API seçeneği farklı bir kapsam sunar ve desteklenmeyen kategorileri kaydeder.

Takeout, Telegram Desktop tarafından da kullanılan resmi dışa aktarma API'sidir. TgWitness, kendi topladığı verilerden doğrudan Desktop ile uyumlu JSON dosyası oluşturabilir; başka birinin arşivini içe aktarmak gerekli değildir. Sohbet ve mesaj kimlikleri her iki aktarım yöntemiyle de erişilebilir. Genel bir sohbet veya iletme izni, daha hızlı bir dışa aktarım garantisi vermez veya Takeout’un onay gecikmesini ortadan kaldırmaz. Hız karşılaştırması yapmadan önce aynı kapsam ve medya ayarlarını ölçün.

20'a kadar açıkça seçilen sohbet kimlikleri için, normal API dışa aktarımı, hesabın tam diyalog envanterini dikkate almadan önce bu eşleri doğrudan çözümler. Bu sayede, okunabilir bir genel kanal, diyalog listesinde yer almıyor olsa bile, kanala katılmadan dışa aktarılabilir. Önbelleğe alınmamış eşler, normal envantere geri döner. Önbelleğe alınmamış eşler, normal envantere geri döner. Arşiv filtresi uygulanmaya devam eder: Telegram bir diyalog döndürmezse ve arşivlenmiş sohbetler hariç tutulursa, bilinmeyen arşiv durumu bir eksiklik olarak kaydedilir. Takeout, aralık bölmeli envanter prosedürünü korur. Her iki yol da sohbetlere katılmamakta veya yönlendirme izinlerini değiştirmemektedir. Masaüstü uyumlu JSON'da, Telegram'ın `left` olarak işaretlediği kanallar, `left_chats` altında görünür; buna, hesabın katılmadığı okunabilir genel kanallar da dahildir.

Hem `FLOOD_WAIT` hem de `FLOOD_PREMIUM_WAIT`, sunucu tarafından talep edilen sürenin tamamı boyunca duraklatma isteklerini askıya alır. Hesabın son tarihi, yeniden bağlanma ve yeniden başlatma işlemlerinde korunur; daha kısa bir sonraki bekleme süresi bunu kısaltamaz. Yeniden deneme sayısı sınırlıdır, iptal işlemi mühürlenmiş sayfaları korur ve API kimlik bilgileri, hız sınırını aşmak için değiştirilmez. Premium satın alımı yapılmaz.

## Nelerin toplanacağını seçin

| Ayarlar | Anlam |
| --- | --- |
| Amaç | Bu satın almanın neden gerekli olduğunu kaydedin. Buraya gereksiz isimler veya hassas vaka detayları eklemeyin. |
| Rapor dili | Okunabilir raporun etiketlerinin dilini seçin. Orijinal mesaj metni değişmez; çevrilmemiş şablon etiketlerinde İngilizce kullanılır. Dil, imzalanmış iş seçenekleriyle sabitlenir. |
| Sohbet türleri / sohbet kimlikleri | Seçilen tüm türler veya sadece listelenen sohbetler; Kaydedilen Mesajlar, özel sohbetlere aittir. Arşivlenmiş sohbetler ayrı olarak seçilebilir. |
| Tarihler | UTC. Panelin "Başlangıç" ve "Bitiş" takvim tarihleri her ikisi de dahil edilir. API, dahil `from_utc` ve hariç tutan `to_utc`kullanır; panel, "Through" tarihinden sonraki günün başlangıcını gönderir. Boş bir sınır, o tarafı kısıtlamaz. |
| Gönderen Kimlikleri | Yalnızca listelenen gönderenlerin mesajları; boş bir liste ise tüm gönderenleri içerir. |
| Metin şunları içerir: | Büyük/küçük harf duyarlı olmayan sabit ifadeler, OR ile eşleştirilir. Gönderen/tarih/kendi mesajı koşulları AND ile birleştirilir. |
| Kendi mesajlar | Yalnızca giden mesajları saklayın. |
| Medya türleri | Mesaj dosyalarının indirilmesini önlemek için ek kategorilerini seçin veya tümünü temizleyin. |
| Dosya / toplam medya sınırları | Dosya başına MiB ve indirilen toplam medya için GiB. Metinler, makbuzlar, okunabilir raporlar ve ZIP ek yükü için ek disk alanı gerekir. |
| Hesap kategorileri | Profil, kişiler, profil fotoğrafları, hikayeler, oturum meta verileri ve diğer Takeout verileri için ayrı denetimler mevcuttur. |

**Minimize koleksiyon** ön ayarı, dosyaları ve hesap meta verilerini devre dışı bırakır. Gönderen/içerik filtreleri, saklanan mesaj sayfaları ve medya indirmelerinden önce uygulanır. Telegram, bu filtreleri değerlendirmek için gerekli mesajları içeren API geçmiş sayfalarını hâlâ iletir: filtreleme, seçilmemiş mesajların işlem belleğine asla girmeyeceği garantisi değildir. Çalışma alanındaki diğer devam eden gözlemlerin kendi kapsamı ve saklama ayarları vardır.

Profil fotoğrafı geçmişi ve hikayeler varsayılan olarak seçili değildir. Vakanın yalnızca mesajlara ihtiyaç duyduğu durumlarda profil ve kişileri de devre dışı bırakın. Ekler veya meta veriler gereksizse, bunları toplama sırasında hariç tutmak, bu dışa aktarımda başka bir özel kopyanın saklanmasını önler.

Fotoğraf yükleri, meta verilerinde ve hash manifestolarında tanımlanan sabit görüntü varyantını kullanır; buna animasyonlu avatar varyantına sahip fotoğraflar da dahildir. Bu animasyon, seçilen sabit görüntünün yerine geçmez. Gözlemlenen boyuttan daha kısa veya daha uzun bir yük, başarısız bir ek olarak kaydedilir ve dosya referansının yenilenmesi sırasında değiştirilen temsil reddedilir. Bu hatalar, mesaj kayıtlarını korurken arşivi eksik bırakır. Bağımsız doğrulama, eski arşivler de dahil olmak üzere, imzalı uzunluğu gözlemlenen boyut veya temsil ile çelişen kaydedilmiş ekleri de reddeder.

## Özet, kapsam ve doğrulama

Her iş, kendi seçeneklerini ve hesap kimliğini sabitler. Envanter ve yakalanan sayfalar imzalanır; sayfa makbuzları, hash değerlerini, imleç konumlarını, zamanları, ek sonuçlarını ve bunlardan önceki makbuzları kaydeder. Yalnızca onaylanmış sayfalar ilerlemeyi sağlar. Yeniden başlatma/devam ettirme, devam etmeden önce bu kayıtları kontrol eder. Değiştirilmiş bir hesap, değiştirilmiş imzalı sayfa veya tutarsız makbuz zinciri reddedilir. Alım işlemi yarıda iken seçenekler düzenlenemez: başka bir kapsam için yeni bir iş başlatın.

"Pause" (Duraklat), çalışmakta olan hesap işlemini durdurur. Uygulamayı yeniden başlatmak, tamamlanmamış işlerin açıkça devam ettirilebilmesini sağlar. Süresi dolmuş bir Takeout oturumu, açıkça devam ettirilmeyi gerektirir; Telegram bölünmüş aralıklarının değiştirilmesi, yeni bir veri alımı gerektirebilir. "Resume" (Devam Et), önceki gözlemleri korur; bu nedenle uzun süren bir dışa aktarma işlemi tek bir atomik anlık görüntü değildir. Veri alımı sırasında diğer hesap değiştirme işlemleri ve çakışan dışa aktarma işlemleri engellenir. Bir çalışma alanını silmeden önce paketlemenin tamamlanmasını bekleyin.

Devam Et seçeneği, devam etmeden önce daha önce yakalanan içeriği doğrular. Yavaş depolama alanındaki büyük arşivler, yapılandırılmış **Parametreler → Panel eylem zaman aşımı** süresini (varsayılan olarak 120 saniye) aşabilir. Yeniden denemeden önce bu ayarı artırın; iptal veya depolama kesintisi, işi duraklatır; başarısız bütünlük kontrolleri ise bir açıklama ile birlikte işi başarısız olarak bırakır. Dosyalar kapatılabilmesi için doğrulama işleminin tamamlanması veya güvenli bir şekilde durdurulması gerekir. Sentetik kontrollerle, büyük hesaplara ilişkin herhangi bir iş hacmi iddiası doğrulanmamıştır.

Panel, tamamlanmış seçilmiş kapsamı kısmi arşivden ayırır ve eksiklikleri ile okunamayanları kaydeder. Kasıtlı olarak hariç tutulan dosyalar, okunamayan veya erişilemeyen dosyalardan farklıdır. Bütünlük doğrulaması başarılı olsa bile kapsama alanını inceleyin. Hiçbir yerel okuyucu, Telegram’ın var olan her mesajı geri gönderdiğini kanıtlayamaz.

Tamamlanan ZIP'ler, tekrarlı indirmeler ve HTTP aralık indirmeleri için kullanılabilir durumda kalır. Bir hesap arşivi, `manifest.json`, `manifest.sig`, imzalanmış `job.json`, `inventory.json`, `receipts/`, güvenilir `data/*.jsonl`, seçilmiş `media/`, okunabilir HTML ve bir doğrulayıcı içerir. Toplayıcı parmak izini bağımsız bir kanal üzerinden sabitleyin, ardından güvenilir bir kurulum kullanarak doğrulayın:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Genişletilmiş içeriği 4 GiB'yi aşan arşivler için, açıkça yeterli bir `--max-gib`. Panel, kimlik doğrulaması yapılmış ve tamamlanmış yerel arşivleri, beyan edilen genişletilmiş boyutları ve yayınlanan ZIP özetini kullanarak doğrular; harici CLI ise bağımsız boyut sınırını korur. Okunabilir HTML dosyasını açmadan önce doğrulama yapın. Arşivin birlikte gelen doğrulayıcısı kullanışlıdır, ancak bağımsız olarak edinilen bir doğrulayıcı, kanıtla birlikte sunulan yürütülebilir koda güvenmek zorunda kalmanızı önler.

Ed25519 imzası ve SHA-256 hash değerleri, toplayıcının ilgili baytları kayda aldıktan sonra yapılan değişiklikleri tespit eder. Bunlar, **değil** Telegram'ın bu mesajları imzaladığını, toplayıcı operatörünün dürüst olduğunu, hesabın geçmişinin eksiksiz olduğunu veya bir mahkemenin bu materyali kabul edeceğini kanıtlamaz. Yakalama zamanları, toplayıcının saatine göre belirlenir. Bağımsız zaman damgaları ve bağımsız elde etme kaynağı ayrı ayrı değerlendirilmelidir.

## Bir avukat veya başka bir alıcı için bir açıklama hazırlayın

Tamamlanmış bir dışa aktarım dosyasını indirdikten sonra, orijinal ZIP dosyasını saklayın ve `index.html` çıkartılmış bir kopyadan açın. Rapor, kapsamını, mevcut kapsama alanını ve sınırlarını açıklar. Kayıt referansları, arşiv referansını, belge yolunu ve kayıt numarasını birleştirir; böylece alıcı, HTML dosyasında veya çıktıda aynı girişi bulabilir. Uygulamalı bir örnek için, [kurgusal raporu aç](https://phishdestroy.github.io/TgWitness/demo/report/).

Tamamlanmış bir hesap dışa aktarımından "**Paylaşım kopyası hazırla**" seçeneğini seçin. Bu, ayrı bir imzalı türev oluşturur. Kaynak ZIP değişmeden kalır ve gizli kalır; alıcının tam içeriği almaya yetkisi olmadığı sürece, bunu küçültülmüş türevle birlikte göndermeyin. Rapor dilini ayrı olarak seçin. Dili veya herhangi bir seçim ayarını değiştirmek, oluşturma işleminden önce başka bir önizleme gerektirir.

1. Açıklama amacını girin ve tarihleri, gönderen kimliklerini ve metin kriterlerini seçin.
2. Kimlikleri korumayı, yalnızca listelenen katılımcıları göstermeyi veya herkesi takma adla göstermeyi seçin. Her iki takma ad modunda da sohbet kimlikleri/başlıkları ve mesaj kimlikleri değiştirilir. Takma adlar, tek bir paylaşım içinde sabittir ve bağımsız olarak hazırlanan paylaşımlar arasında değişir.
3. Mesaj metnini koruyun, tamamen atlayın veya maskelemek için tam adlar/ifadeler ekleyin. Özel modlarda araç, bilinen gizli gönderen adlarını ve alternatif kullanıcı adlarını, tam token gönderen kimliklerini, doğrudan sohbet adlarını, bağlantıları, e-posta adreslerini ve telefon numarası benzeri dizeleri de maskeler. Bilinen ad eşleştirme, `Straße`/`STRASSE`. Genel grup/kanal başlıkları mesaj metninden otomatik olarak kaldırılmaz. Bilinen kimlik maskeleme sınırı aşılırsa, kaynak dışa aktarımını daraltın veya metni atlayın; araç, sonraki isimleri sessizce atlamayı reddeder. Bunlar, genel bir anonimleştirme değil, elden gelenin en iyisi kurallardır.
4. Alıcının ihtiyaç duymadığı sürece dosyaları hariç tutun. Dahil edilen orijinaller piksel, ses, metin ve meta verilerini korur. Bu dosyalar, araç tarafından **değil** şekilde anonimleştirilir.
5. Sayımları, uyarıları ve dönüştürülmüş mesaj örneklerini önizleyin, ardından oluşturma işlemini açıkça onaylayın. Örnekler, her biri 12 mesaj ve 2.000 metin karakteriyle sınırlıdır. Bu bir örnektir, sonucun tam bir incelemesi değildir. Ayarları değiştirmek için başka bir önizleme gerekir. Bir önizleme 15 dakika sonra geçerliliğini yitirir ve o yönetici oturumuna ve tam olarak orijinal ZIP öğesine bağlıdır; oluşturulduktan sonra yeniden kullanılamaz. Yeni bir önizleme, aynı iş ve oturum için bir öncekini geçersiz kılar.
6. Ortaya çıkan sonucun tamamını inceleyin `index.html` ve `messages.jsonl` yerel olarak kontrol edin. Gereksiz bilgiler ortaya çıkarsa, daha sıkı hariç tutma koşulları içeren yeni bir paylaşım oluşturun. İmzalanmış ZIP öğesini yerinde düzenlemeyin.

### Seçim dışında bırakılan mesajlar

**Önizleme.** Bir ifşa, tam olmadığında tam görünmez. En az bir ifşa edilmiş mesaj içeren her sohbetin içinde, seçimin dışında kalan mesajlar işaretçi olarak görünür, `[withheld by selection — rule: sender]` (veya `text`, `period`). **Seçim dışında kalan mesajlar seçeneğini** belirleyin: arka arkaya gizlenen mesaj dizisi başına bir işaret (varsayılan) veya her mesaj için bir işaret. İşaretler yalnızca kuralı ve sayıyı gösterir; metin, gönderen, tarih veya dosyaları asla göstermez. Açıklanmış hiçbir şey içermeyen sohbetler tamamen dışarıda bırakılır, böylece paket bunların varlığını ortaya çıkarmaz.

Açıklanan yanıtlar, neye yanıt verdiklerini belirtir: bu kopyada yer alan bir mesaj, seçim nedeniyle gizlenen bir mesaj veya kaynak dışa aktarımında bulunmayan bir mesaj (dışa aktarımdan önce silinmiş veya hiç dışa aktarılmamış; dışa aktarımda hangisi olduğu anlaşılamaz). Açıklanan bir yanıtın yanıt verdiği, seçimden hariç tutulan bir mesaj her zaman kendine ait bir işaretçiye sahiptir; böylece yanıt, mesajın neden boş olduğunu açıklayan bir kayda işaret eder. Bu üç durum, kaynak dışa aktarımına ait olan silme işlemleri ve koleksiyon boşluklarından farklıdır.

Şu `messages.jsonl` (şu formatta `tgwitness-account-disclosure-v2`) her mesajda `state`: `disclosed`, veya `withheld` ile `rules` ve `count`. Açıklanan bir yanıtta `reply_to` hedef ile `id` ve `state` (`disclosed`, `withheld`, `not_in_source`). Manifest, ifşa edilen mesajları, sohbetleri, medya dosyalarını ve `withheld` mesajları sayar. `verify.py` içerik taşıyan bir işaretleyiciyi ve pakette bulunmayan bir kayda işaret eden bir yanıtı reddeder; sürüm 1 paketleri ise eskisi gibi doğrulanır.

Küçültülmüş format, yapılandırılmış hesap profillerini, kişileri, avatarları, oturumları, hikayeleri, ham Telegram nesnelerini, iletme başlıklarını, yanıt alıntılarını, kişi kartlarını ve konum meta verilerini hariç tutar. Orijinal JSONL dosyalarını, özel filtre ayarlarını, takma ad anahtarını ve kimlik haritasını içermez. Seçilen metin, açıkça saklanan kimlikler ve dahil edilen dosyalar, bu filtrelerde kullanılan aynı adları, kimlikleri veya ifadeleri içerebilir; bunların ayrı olarak incelenmesi gerekir. Özel politika ve takma ad anahtarı, iş için yerel kasada şifrelenmiş olarak saklanır; işin silinmesi, ilişkili özel ifşa kayıtlarını da temizler. Genel politika kayıtları, filtre değerleri yerine filtre sayılarını kaydeder. Belirtilen amaç, manifestoda ve HTML'de herkese açıktır: açık özel kriterler ve takma ad modlarında bilinen gizli kimlikler de burada maskelenir; bu, mesaj metninin çıkarılması durumlarını da içerir. Amacı gereksiz kişisel ayrıntılardan uzak tutun; bilinmeyen tanımlayıcı bağlamlar kalabilir.

Manifest dosyası, türetilmiş dosyaları, genel politikayı ve orijinal ZIP öğesinin hash değerini birbirine bağlar. Doğrulama işlemi, bütünlüğü teyit edebilir ve kaynak yerel olarak sağlanmışsa, kaynak bağlantısının eşleşip eşleşmediğini de belirleyebilir:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Kaynak bağlantısı, dönüştürme işleminin gerekli tüm öğeleri seçtiğini veya tanımlayıcı tüm ayrıntıları kaldırdığını tek başına kanıtlamaz. Orijinal düz metin, kanıt olarak eklenmemiştir. Bu yargıya varmak için yeni bir inceleme gereklidir.

## Paylaşım ve barındırılan yakalama

Alıcının ihtiyaç duyduğu mesajları ve dosyaları seçin, paylaşılacak kopyanın tamamını gözden geçirin ve kaynağı ayrı olarak saklayın. Alıcının tam olarak bu kopyayı tanımlayıp doğrulayabilmesi için teslim edilen ZIP dosyasının hash değerini kaydedin. Seçilen tanımlayıcılar takma adlandırma işlemiyle değiştirilir; dahil edilen metin ve orijinal dosyalar incelemenin bir parçası olarak kalır.

GitHub Actions, Takeout veya normal API aracılığıyla tam hesap ve seçili sohbet dışa aktarımlarının yanı sıra tek sohbetlik bir olay günlüğünü de destekler. [barındırılan yakalama kılavuzu](https://phishdestroy.github.io/TgWitness/docs/capture/), ayarların doğrulanmasını ve 120 dakikalık sınırı açıklamaktadır. Barındırılan yakalamadan türetilen bir paylaşım kopyasını doğrulamak için, kaynak hash değerini orijinal arşivle karşılaştırın ve [moduna özgü kontroller](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) ile arşivin doğruluğunu teyit edin.

[Kanıt formatı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) · [Vaka raporları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/)
