# Rapor yapılandırması ve doğrulama

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/

Rapor filtreleri, sekiz tasarım, içerik ön ayarları, kaydedilmiş değişiklik geçmişleri ve imzalı dışa aktarımlara dahil edilen değerlendirme.

Seçilen gözlemleri, vakanın okunabilir bir özetine dönüştürün: vakanın sorusu, kapsamı, kaydedilen değişiklikler, grafikler, bulgular ve kaynak referansları. Her rapor, alıcıya teslim edilen materyali kontrol etme ve toplama kapsamını inceleme imkanı sunar.

"**Güven Temeli ve Sınırlamalar**" bölümü günlük, devir teslimi, sohbet, hesap ve paylaşım raporlarında yer alır. Günlük ve devir teslimi PDF'leri, imzalanmış `report.json` dosyasıyla aynı değerlendirmeyi kullanır. ZIP manifestoları, imzalanmış manifestoda `case_assessment` bilgisini taşır. Bu değerlendirme, dışa aktarılan materyalle birlikte aktarılır. Orijinal gözlemler mevcut imzalarını korur.

## Belge formatları ve okuma sırası

### Rapor stüdyosu

**Dışa Aktar → Yapılandır ve önizle** seçeneklerini açın. **Veri → Tasarım ve içerik → Önizleme** adımlarını izleyin:

1. Tüm çalışma alanını kullanın veya sohbetleri, yazarları, UTC gözlem tarihlerini ve olay türlerini seçin. Sohbetleri ve yazarları aramak için kataloğu yükleyin veya Telegram kimliklerini girin. Yazar filtreleri, kaydedilen gönderen kimlikleriyle eşleşir; göndereni belirtilmemiş bir silme bildirimi, yazar filtresiyle eşleşmez.
2. Bir sayfa tasarımı seçin, ardından grafikleri, katılımcı etiketlerini, transkripti ve yazılı bulgularınızı seçin. Tasarım değiştirildiğinde bu seçimler korunur.
3. Önizlemeyi oluşturun. Önizleme, gerçek sayıları, etkinlikleri, katılımcıları, örnek kayıtları, kaydedilen değişiklikleri ve eksik mesaj numarası aralıklarını gösterir. Bir seçimin değiştirilmesi önizlemenin güncelliğini yitirmesine neden olur. HTML, imzalı PDF, imzalı JSON veya delil ZIP dosyasını indirmeden önce kaydedin.

Veri önizlemesi, ilk bir örnek değil, tam ve kararlı günlük önekini sayar. Yalnızca görüntülenen örnek satırlar ve uzun listeler sınırlandırılmıştır; atlanan sayıların toplamı gösterilir. Daha sonraki bir dışa aktarım işlemi yeni bir kararlı anlık görüntü alır, bu nedenle devam eden toplama işlemi rakamları artırabilir. Kapsam, sayı ve kaynak kimliği imzalı raporda yer alır. Formu açmak veya önizlemek, formun kaydedilmesine yol açmaz.

**Alıcının kopyasını seçin.** Grafikler ve transkript, seçilen kayıtları kullanır. Bütünlük, saklama ve kapsam, kaynak günlüğünün tamamını tanımlar. Kanıt ZIP dosyası orijinal kayıtları ve ekleri içerir. Alıcının yalnızca seçilmiş, izin verilen verileri alması gerektiğinde, [en az miktarda veri içeren bir devir işlemi](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#handover-extract) kullanın.

### Düzenlemeleri, silme işlemlerini ve eksik kimlik numaralarını okuyun

Bir düzenleme, kaydedilmiş **"Önce"** ve **"Sonra"** metinlerini gösterir ve değiştirilen kelimeleri vurgular. Bir silme işlemi, bildirimden önce kaydedilen son sürümü gösterir. Daha önceki içerik yakalanmamışsa, raporda bu durum belirtilir. Yalnızca düzenlemeleri veya silme işlemlerini seçtiğinizde, önceki sürümler, filtrelerin dışında açıkça etiketlenmiş bağlam olarak kullanılabilir durumda kalır. Bu geçmişlere konuyla ilgisiz mesajlar eklenmez.

**Gözlemlenmemiş mesaj kimlikleri**, seçilen sohbetlerdeki bilinen numaralar ile tarihten türetilen kimlik aralığı arasındaki boşluklardır. Bir numarayı gözlemlenmemiş olarak ilan etmeden önce bilinen her kaynak kayıt kontrol edilir: başka bir yazarın, olay türünün veya tarihin filtrelenerek çıkarılması yanlış bir boşluk yaratamaz. Bitişik kaydedilmiş mesajlar bağlam olarak etiketlenir. Eksik bir sayı, bir mesajın var olduğunu veya silindiğini kanıtlamaz; silme bildirimleri ve başarısız yeniden kontroller ayrı olay türleri olarak kalır.

### Bir tasarım seçin

Günlük ve tekli sohbet HTML raporları ile imzalı PDF raporları için sekiz farklı sayfa tasarımı mevcuttur. Bu tasarımlar aynı kayıtları ve hesaplamaları kullanır, ancak kapakları, tipografisi, bölüm başlıkları, tabloları ve satır aralıkları farklıdır.

| Tasarım | Okuma stili |
| --- | --- |
| Klasik | Koyu renkli kapaklı ve numaralandırılmış bölümleri olan geleneksel bir dosya. |
| Editörlük | Çerçeveli serif başlık sayfası, geniş kenar boşlukları ve dar bölüm başlığı çubuğu. |
| Özet | Lacivert sırtlı, kısa başlıklar ve sıkı dizilmiş tablolar içeren kompakt bir kapak. |
| Analitik | Anket tarzında bir kapak, modüler grafik tabloları ve sabit aralıklı şekiller. |
| Teknik | Çizgili kayıt defteri, numaralı referans çubuğu ve kesin karşılaştırma tabloları. |
| Genel Bakış | Panoramik bir kapak, bol boşluk ve göze çarpan özet şekiller. |
| Okuma serisi | Bulgular, kapsam, değişiklikler ve gözlem günlüğü için bir bölüm menüsü ve gruplandırılmış bölümler. |
| Defter ve marj | Geniş kenar boşluklu numaralı bölümler, kesin çizelge tabloları ve ayrı bir mesaj transkripti. |

Tasarım, çalışma alanı başına kaydedilir ve imzalı dışa aktarma manifestosuna kaydedilir. HTML çevrimdışı çalışır, açık ve koyu temaları destekler ve dar ekranlara ve sağdan sola yazılan dillere uyum sağlar. Yerel PDF'ler paketlenmiş yazı tiplerini kullanır; Editorial tasarımı, paketlenmiş SIL Açık Yazı Tipi Lisansı kapsamında Noto Serif'i içerir. Okuma serisi ve Ledger & margin özellikleri, hesap özetleri, hesap sohbetleri ve kopya paylaşımları için de geçerlidir.

Çince, Japonca ve Korece PDF'ler için ayrıca sunucuda uygun bir yazı tipine ihtiyaç vardır; örneğin, sistem genelinde yüklü olan veya `TGWITNESS_FONT_DIR` dizinine yerleştirilmiş Noto Sans CJK gibi. Bu yazı tipi mevcut değilse, ZIP dosyası HTML ve JSON raporlarını korur.

Bu iki tasarım, JavaScript olmadan okunabilir bir günlük içerir. Büyük dışa aktarımlar için bu görünüm, 8 MiB'lik bir giriş bütçesi dahilinde en fazla 500 tam kayıt içerir; rapor, sınırı belirtir ve tam görüntüleyici ile kaynak kayıtlarına bağlantı sağlar. Hesap dizini ve ilişki dizini, tüm katılımcıları değil, aynı okuma örneğini açıklar. Tam günlük grafikleri, ayrı olarak belirtilen kapsamlarını korur.

### İçeriği seçin

| İçindekiler ön ayarı | Varsayılan olarak dahil edilmiştir |
| --- | --- |
| Dava dosyası | Etkinlik, gözlem zamanları, katılımcılar, sohbetler ve kayıt transkripti. |
| Özet | Katılımcı sıralamaları veya konuşma metni içermeyen bir etkinlik özeti. |
| Etkinlik incelemesi | Etkinlikler, gözlem zamanları, katılımcılar, sohbetler ve içerikleri, kaynak referansları ve kesin rakamlarla birlikte. |
| Özel rapor | Grafikler, transkriptler ve önizlemelerden kendi kombinasyonunuzu oluşturun. |

Ön ayarları değiştirdiğinizde tasarımınız, vaka ayrıntılarınız ve yazılı analizleriniz korunur. Bütünlük kontrolleri, kapsam, sınırlamalar ve doğrulama talimatları her tasarımda yer alır. Bir grafik veya transkript gizlendiğinde ZIP dosyasındaki kaynak kayıtlar değişmeden kalır.

İsteğe bağlı **İnceleme notları**, raporun yazarı tarafından yazılan soru, yöntem, bulgular ve sonucu içerir. Bulgularda kaynak dosyasını ve kayıt numaralarını belirtin. İmza, bu yazara ait ifadeleri raporun yanında korur; kaynak gözlemleri ve yazarın yorumları tanımlanabilir kalır. Kısaltılmış devir işlemlerinde bu özel notlar ve tam günlük çizelgeleri hariç tutulur. Çizelge ve muayene seçenekleri günlük raporları için geçerlidir.

Zaman içindeki etkinlikleri, UTC hafta içi gün/saat ısı haritasını, katılımcı sıralamalarını, sohbet sıralamalarını ve kayıt bileşimini seçin. 5–30 sıralı grup ve tarafsız katılımcı takma adları veya hesap kimlikleri seçin. Bilinmeyen gönderenler ve geri kalan katılımcılar ayrı satırlarda yer alır. Takma adlar yalnızca grafikleri etkiler; kaynak kayıtlar hala kimliklerini içerir.

Tasarım önizlemesi, üretim kapağı, inceleme ve grafik bileşenlerini kullanarak kaydedilmemiş taslaktan güncellenir; bu, ilk 50.000 kaynak kayıttaki eşleşmelerle sınırlıdır. Aşağıdaki veri önizlemesi seçimin tamamını hesaplar. Bu önizleme açıkça imzasızdır ve düzenlemeleri kaydetmez. Kapak ve Grafikler düğmeleri, bölüm arasında geçiş yapar. Bu, tam bir PDF önizlemesi değildir. **Rapor ayarlarını kaydet seçeneği,** seçimleri gelecekteki dışa aktarmalara uygular; mevcut imzalı dosyalar değiştirilemez. PDF, seçilen kapak sayfasını, tipografiyi, bölüm düzenini ve HTML ile imzalı JSON’da seçilen aynı toplama değerlerini kullanır.

Güven değerlendirmesi, kapsam sınırlamaları ve doğrulama talimatları mevcut kalmalıdır. Grafikleri veya okunabilir transkripti gizlemek, ZIP dosyasından yetkili kaynak satırlarını kaldırmaz. Devre dışı bırakılmış grafik serileri analitik JSON'dan çıkarılır; kaynak kayıtlarının ifşasını sınırlamak için minimize edilmiş dışa aktarma kullanın.

Veri seçme filtreleri günlük raporlarına uygulanır; hesap ve paylaşım dışa aktarımları kendi toplama ve ifşa kapsamlarını korur.

Paylaşılan tasarım/grafik tercihleri, yeni sohbet/hesap dışa aktarımlarına ve hesap paylaşım önizlemelerine sabitlenir. Hesap/paylaşım dili ve gizlilik ayarları bağımsız kalır; özel vaka ve inceleme notları bu dışa aktarımlara kopyalanmaz. Hesap ve paylaşım raporları, imzalı arşiv manifestosu tarafından korunan HTML formatında kalır. Günlük, küçültülmüş günlük devri ve tek sohbet kitleri de imzalı PDF’ler sağlar.

### Grafiklerde nelerin sayıldığı

Günlük etkinliği ve ısı haritaları, UTC cinsinden toplayıcının gözlem zamanına göre yeni, geçmiş, kurtarılmış, düzenlenmiş, silinmiş ve yeniden kontrol edildiğinde eksik olan **gözlemleri** sayar. Kalp atışları ve ek alım bildirimleri hariç tutulur. Katılımcı sıralamaları yalnızca yeni, geçmiş ve kurtarılmış mesaj gözlemlerini sayar: bir gönderen, düzenleyen veya silici olarak belirtilmez. Tekrarlanan gözlemler aynı Telegram mesajını tanımlayabilir.

Günlük analizleri, türlere göre sayıları, ilk/son kayıt referanslarını ve kaynak `events.jsonl`'nin SHA-256 değerini tutar. Şekiller, HTML ve PDF'de kesin değerleri içerir. Günlük gruplar, kaydedilen 366 günden sonra aylara geçer; grafikler bunları en fazla 36 eşit genişlikli aralığa birleştirir. 100.000'den fazla farklı tanımlayıcı veya 1.200 ay, ilgili grafiğin kullanılamaz hale gelmesine neden olurken, kesin toplam sayılar kullanılabilir durumda kalır.

Anlık görüntü ve hesap paylaşımı grafikleri, yalnızca hizmet dışı mesaj satırlarını, kayıtlı mesaj zamanlarını kullanarak sayar. Paylaşım toplamları, redaksiyon ve filtrelemeden sonra hesaplanır. Bu grafikler en fazla 90 adet eşit genişlikte UTC tarih aralığı kullanır ve en fazla 10.000 gruplama değerini saklar; fazlalık sayıları açıkça belirtilir ve mutabakatı yapılır. Son aralık daha kısa olabilir. Bilinmeyen veya hatalı tarihler zaman grafiklerine dahil edilmez.

Boş bir aralık, ilgili gözlemlerin bulunmadığı anlamına gelir; eksiklikler için kapsam bilgisine bakınız. Bu grafikler, kaydedilen etkinlikleri gösterir. Bilinmeyen gönderenler ayrı bir kategori olarak kalır ve her kontrol ayrı ayrı raporlanır.

`analytics.json` dosyası dahil edildiğinde, arşivin imzalı dosya hash'leri tarafından korunur. `report.json` dosyası, aynı seçilmiş toplamı içerir. İmza doğrulama değiştirilen baytları tespit eder. Rakamları kontrol etmek için, `report_analytics.Analytics` ve `selected` ile günlük toplamlarını yeniden hesaplayın veya `snapshot_analytics.collect` ve `project` ile anlık görüntü toplamlarını yeniden hesaplayın.

Kaynak kodundan, yukarıda listelenen sekiz tasarımı da aynı hayali dergiden oluşturun:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Ortaya çıkan `index.html` dosyasını açarak eksiksiz HTML raporlarını, imzalı PDF'leri ve ZIP dosyalarını karşılaştırın. Her tasarım aynı kaynak günlüğünü kullanır. Her çalıştırma için yeni bir çıktı dizini kullanın, böylece daha önce imzalanmış örnekler korunur.

![Kurgusal HTML dosyası](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

HTML sayfası, vaka kapağı ve ana rakamlarla açılır. Numaralandırılmış delil haritası, her bir bulguya, onu destekleyen gerçeklere, sınırlamalara ve bağımsız incelemeye bağlantı sağlar. Arama yapılabilen kayıtlar ve sabit kayıt referansları, çevrimdışı görüntüleyicide kullanılmaya devam eder. Tasarım, dar ekranlara, her iki temaya ve JavaScript'siz tarayıcılara uyum sağlar.

İmzalı PDF dosyasında özel bir A4 kapak, rapor referansı ve QR kodu, bir yönetici özeti, bir delil haritası, numaralandırılmış bulgular ve belge yer imleri bulunur. Sayfa üstbilgileri ve altbilgileri raporu tanımlar. Bir QR kodu materyali tanımlar; bu, bağımsız bir doğrulama sonucu değildir. Tarayıcıdan alınan çıktılar, bu kriptografik olarak imzalanmış PDF dosyasından ayrıdır.

Gözlem zaman çizelgesi, kaydedilen gözlem dönemlerini ve kesintileri aynı UTC eksenine yerleştirir. Boş alanlar kapsama alanı olarak yorumlanmamalıdır; ayrıntılı tablolar kesin aralıkları korur. ZIP dosyası, okunabilir raporları, imzalı JSON dosyasını, kaynak kayıtlarını ve doğrulama talimatlarını içerir.

Geliştirme ortamı yüklü olarak yeni, kurgusal bir İngilizce/Rusça/Almanca dosya oluşturun:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Her dil dizini, `report.html`, `report.pdf`, `report.json` ve `dossier.zip` dosyalarını içerir. Mevcut örnek dizinler asla üzerine yazılmaz. Oluşturulurken hiçbir Telegram hesabı, harici zaman damgası hizmeti veya ağ bağlantısı kullanılmaz.

![Hayali imzalı PDF dosyasının ilk üç sayfası](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Somut bir vakanın incelenmesi

1.000 numaralı girdide doğrulanmış bir zaman damgası bulunan 1.200 girdilik bir günlük için, rapor, söz konusu zaman damgasının sınırları dışında kalan 200 sonraki girdiyi tespit eder. Bu, bir kontrol noktasının varlığına ilişkin bir üst sınırdır, her bir mesajın gönderilme zamanının kanıtı değildir. Diğer üç zaman damgası dosyası doğrulamayı geçemezse veya doğrulanamazsa, bu dosyalar ayrı olarak sayılır ve kesin bir sonuca ulaşılamaz.

Kullanılabilir bir zaman damgası, şu kontrollerin tümünü karşılamalıdır: damgasının izi kontrol noktasıyla eşleşmeli, imzası damgalandığı anda güvenilir bir TSA köküne zincirlenmeli ve kontrol noktasının imzası, anahtarı, sayısı ve başlığı, günlük önekiyle tam olarak eşleşmelidir. Sadece bir zaman damgasını ayrıştırmak veya bir OTS makbuzu bulundurmak yetersizdir. Okuyucu, güvenilir TSA kökünü bağımsız olarak seçmeli ve doğrulamayı tekrarlamalıdır. OTS’nin kendi Bitcoin onay kontrolüne ihtiyacı vardır.

| Rapor durumu | Anlam |
| --- | --- |
| Dışa aktarım sırasında kontrol edildi | Dışa aktarıcı belirtilen kontrolü gerçekleştirmiştir; yine de bağımsız bir tekrar kontrolü gereklidir. |
| Kaydedildi; inceleme gereklidir | Altta yatan gözlem veya operatör beyanı kaydedilir; bu, bağımsız bir teyit değildir. |
| Bu metne dahil edilmeyenler | Metinde bu iddiayı destekleyen herhangi bir kanıt bulunmamaktadır. Başka bir yerde böyle bir şeyin olmadığı da belirtilmemiştir. |
| Bağımsız olarak kontrol edilmemiştir | Rapor, bağımsız bir doğrulama sonucu sunmamaktadır. |
| Eksik veya mevcut değil | Bir materyal veya gerekli bir kontrol eksik, eksik veya başarısız. |

Her bir kontrolü, kaydedilen toplama kapsamıyla birlikte ayrı ayrı gözden geçirin.

## Güçlü bir yapılandırmanın koruması gerekenler

1. Toplamaya başlamadan önce, toplayıcının anahtar parmak izini ayrı bir güvenilir kanal aracılığıyla saklayın. Bu referansı, dışa aktarılan dosyanın imzalama anahtarıyla karşılaştırın.
2. Bağımsız olarak zaman damgası eklenmiş kontrol noktalarını ve kullanıldığı durumlarda, toplayıcının idari kontrolü dışında tutulan bir tanık günlüğünü koruyun. Bunları, dışa aktarılan günlükle karşılaştırarak önceki sınırlarını kontrol edin.
3. Kayıt toplama kapsamını, eksiklikleri, filtreleri, sınırlamaları ve toplama sürecindeki değişiklikleri belirtin. Gerçek iddia ile ilgili eksik dönemleri açıklayın; gözlemlenmemiş mesaj kimliklerini, silme bildirimlerini ve başarısız yeniden kontrolleri birbirinden ayrı tutun.
4. Orijinal ZIP dosyalarını ve bunların hash değerlerini koruyun. Her bir tutucuyu, aktarımı, tarihi ve amacı kaydedin. Atfedilen operatör ifadelerini ve vaka notlarını bunlarla birlikte koruyun.
5. Gizli VM'ler için, fiyat teklifi, doğrulama sorusu, Intel sertifika zinciri, ölçümler, kesin kaynak ve anahtar işleme koşullarını koruyun ve bağımsız olarak doğrulayın. Doğrulama sonucunu, incelenen kanıtlarla birlikte saklayın.

Güven varsayımları için [doğrulama kapsamına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) ve kaynak iddiaları, kimlik, zaman ve toplama kapsamına ilişkin ayrı değerlendirmeye bakınız.

## Alıcı tarafından incelenmesi

Güvenilir bir TgWitness kurulumu ve bağımsız olarak elde edilmiş bir parmak izi kullanın:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

Witness ZIP dosyası, bağımsız ve güvenilir bir kaynaktan gelmelidir; anahtarını ve kaynağını da koruyun. Komutları, araç sürümünü, çıktıları, incelenen girdi hash'lerini ve çözülmemiş soruları koruyun. Beacon doğrulaması ayrı bir çevrimiçi kontrol işlemidir; rapor oluşturucu, yalnızca bir raporu görüntülemek için hiçbir zaman bir hizmetle iletişim kurmaz.

Belirli bir mesajla ilgili bir ihtilaf durumunda, arşiv referansını, yetkili dosya ve kayıt referansını belirtin, ardından ilgili zaman aralığını, kapsamdaki boşlukları, seçimi ve destekleyici materyali açıklayın. Paylaşım kopyası için, kaydedilen dönüşümü ve kaynak arşive yapılan referansları da gözden geçirin. Özel filtreler ve kimlik eşlemeleri, kamuya açık değerlendirmenin dışında tutulur.

İmzalı PDF'nin doğrulanması, kapsanan baytlarda yapılan değişiklikleri tespit eder. Orijinal dijital dosyayı ve doğrulama sonucunu, ekran görüntüleri veya basılı okuma kopyalarıyla birlikte saklayın.
