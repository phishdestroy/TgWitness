# Hesap dışa aktarma

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/account-export/

Bir hesabın şu anda okuyabileceği içeriği dışa aktarın: kapsam, devam ettirilebilir işler, imzalanmış bir arşiv ve küçültülmüş paylaşım kopyaları.

Kurulum yöneticisi olarak, **Buradan başla → Hesabımı dışa aktar seçeneğini** veya **Dışa Aktarmalar → Telegram hesabı → Hesap dışa aktarımını yapılandır seçeneğini** seçin. Gerekirse oturum açın, kapsamı gözden geçirin ve dışa aktarmayı açıkça başlatın. Sürekli gözlem gerekli değildir. "**Kaydedilen gözlemler**", mevcut günlüğün ayrı bir dışa aktarımdır; ZIP, günlük filtrelerinden bağımsız olarak tüm kaynakları içerir. Her çalışma alanının kendi işleri, imzalama kimliği ve depolama alanı vardır. Sınırsız normal dışa aktarma izni dahil olmak üzere verilen panel erişimi, bu hesap genelindeki yolları açamaz.

Gönderen ve metin filtreleri, **“Gönderen veya mesaj metnine göre filtrele”** seçeneğinin altında açılır. **“Hesap verileri ve bağlantı yöntemi” bölümü,** isteğe bağlı hesap kategorilerini ve “Takeout/normal oturum” seçeneğini içerir; özeti, kapalıyken bile etkin seçenekleri gösterir. Bu bölümler kapatıldığında ayarları korunur. Dışa aktarma ve rapor taslakları, görünüm değiştirilirken mevcut panel oturumunda kalır; tarayıcı yeniden yüklendiğinde kaydedilmez. Mevcut işlere her iki dışa aktarma seçeneğinden de erişilebilir.

Bu iş akışı, bağlı hesaba şu anda erişilebilen verileri dışa aktarır. Varsayılan olarak [Telegram Takeout](https://core.telegram.org/api/takeout) kullanılır; bu, erişilemeyen veya silinmiş Telegram verilerinin yedeği değildir. Gizli Sohbetler, erişilemeyen geçmiş ve önceki düzenlemeler kurtarılamaz. Telegram, Takeout işleminin başlamasından önce bir bekleme süresi uygulayabilir. Panel bu bekleme süresini gösterir; aktarım yöntemini sessizce değiştirmez. Açıkça belirtilen normal API seçeneği farklı bir kapsam sunar ve desteklenmeyen kategorileri kaydeder.

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

Küçültülmüş format, yapılandırılmış hesap profillerini, kişileri, avatarları, oturumları, hikayeleri, ham Telegram nesnelerini, iletme başlıklarını, yanıt alıntılarını, kişi kartlarını ve konum meta verilerini hariç tutar. Orijinal JSONL dosyalarını, özel filtre ayarlarını, takma ad anahtarını ve kimlik haritasını içermez. Seçilen metin, açıkça saklanan kimlikler ve dahil edilen dosyalar, bu filtrelerde kullanılan aynı adları, kimlikleri veya ifadeleri içerebilir; bunların ayrı olarak incelenmesi gerekir. Özel politika ve takma ad anahtarı, iş için yerel kasada şifrelenmiş olarak saklanır; işin silinmesi, ilişkili özel ifşa kayıtlarını da temizler. Genel politika kayıtları, filtre değerleri yerine filtre sayılarını kaydeder. Belirtilen amaç, manifestoda ve HTML'de herkese açıktır: açık özel kriterler ve takma ad modlarında bilinen gizli kimlikler de burada maskelenir; bu, mesaj metninin çıkarılması durumlarını da içerir. Amacı gereksiz kişisel ayrıntılardan uzak tutun; bilinmeyen tanımlayıcı bağlamlar kalabilir.

Manifest dosyası, türetilmiş dosyaları, genel politikayı ve orijinal ZIP öğesinin hash değerini birbirine bağlar. Doğrulama işlemi, bütünlüğü teyit edebilir ve kaynak yerel olarak sağlanmışsa, kaynak bağlantısının eşleşip eşleşmediğini de belirleyebilir:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Kaynak bağlantısı, dönüştürme işleminin gerekli tüm öğeleri seçtiğini veya tanımlayıcı tüm ayrıntıları kaldırdığını tek başına kanıtlamaz. Orijinal düz metin, kanıt olarak eklenmemiştir. Bu yargıya varmak için yeni bir inceleme gereklidir.

## Veri koruma ve barındırılan Capture önizlemesi

Bu kontroller, amaç sınırlaması ve veri asgari tutma ilkelerini destekler; ancak otomatik bir yasal uyum kontrolü değildir. [GDPR’nin 5. ve 25. maddeleri,](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) bu ilkeleri ve tasarım/varsayılan olarak koruma ilkelerini ele alır. Yasal dayanak, gereklilik, uygun olduğu durumlarda özel kategori koşulları, saklama süresi, güvenlik ve alıcı erişimi konularında hâlâ duruma uygun bir karar alınması gerekir. Yalnızca dava amacı, her türlü bilgi paylaşımını yasal hale getirmez. Takma adla anonimleştirilmiş veriler genellikle kişisel veri olarak kalır; [EDPB’nin açıklamasına](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en) bakınız.

Serbest metinler, tarihler, nadir olaylar ve olguların birleşimleri, isimler kaldırıldıktan sonra bile kişilerin kimliğini ortaya çıkarabilir. Mesaj içeriğinin gereksiz olduğu durumlarda metnin çıkarılmasını tercih edin; gerekli olduğu durumlarda ise tam türevini inceleyin. Kaynağı ve veri kasasını koruyun, saklama ve paylaşma koşullarını sorumlu kişiyle kararlaştırın ve tam olarak hangi ZIP öğesinin teslim edildiğini kaydedin.

Bu özellik yerel panelde çalışır. Ayrı olarak yayınlanan [barındırılan Yakalama önizlemesi](https://phishdestroy.github.io/TgWitness/docs/capture/), sabitlenmiş tek kullanımlık bir çalıştırıcı ve kendi doğrulama politikasını kullanır. Yerel toplayıcı imzaları, söz konusu çalıştırıcının kaynağını devralmaz. Buradaki bir değişiklik, onaylanmış bir uzak iş akışını veya güven sabitlemelerini güncellemez; barındırılan tam hesap yakalama işlemi, ayrı olarak incelenmiş ve yayınlanmış bir toplayıcı/iş akışı çifti ile canlı çalıştırıcı onayı gerektirir. Yerel sentetik testler, barındırılan bir dağıtım veya gerçek Telegram hesabı edinimi iddiasında bulunmaz.

[Kanıt formatı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) · [Vaka raporları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/)
