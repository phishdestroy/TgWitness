# İş akışları ve işlemler

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/operations/

Panelin günlük işleyişi: modlar, izleme kategorileri, parametreler, bildirimler, dışa aktarma işlemleri, yedekleme ve kapasite.

İlk bağlantınız için [hesapları ve oturum biçimlerini](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) kullanın. Kaydedilen sürümler, olay ilkeleri ve boşluklar hakkında açıklama için, [toplama işleminin nasıl çalıştığına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/) bakın. Bu kılavuz, günlük işlemleri ve kurtarma işlemlerini kapsamaktadır.

## Operatör iş akışı

Akış şeması · Depolama ve anahtar korumasını seçin → Token ile paneli açın; Token ile paneli açın → Bir çalışma alanı seçin; Bir çalışma alanı seçin → Doğrudan veya proxy yolunu yapılandırın; Doğrudan veya proxy yolunu yapılandırın → Telefon numarasını girin veya dosyaları / QR kodunu seçin; Telefon numarasını girin veya dosyaları / QR kodunu seçin → Hesap kimliğini kontrol edin ve erişilebilir grupları seçin; Hesap kimliğini kontrol edin ve erişilebilir grupları seçin → Olay ve ek politikalarını kaydedin, ardından gözlemi başlatın; Olay ve ek politikalarını kaydedin, ardından gözlemi başlatın → Hataları, erişimi, kuyrukları ve diski izleyin; Hataları, erişimi, kuyrukları ve diski izleyin → Bağımsız kontrol noktalarını koruyun; Bağımsız kontrol noktalarını koruyun → Verileri dışa aktarın ve doğrulayın · Depolama ve anahtarkorumasını seçin · Token ile paneli açın · Bir çalışma alanıseçin · Doğrudan veya proxyyolunu yapılandırın · Telefon numarasınıgirin veya dosyaları /QR kodunu seçin · Hesap kimliğinikontrol edin veerişilebilir gruplarıseçin · Olay ve ekpolitikalarınıkaydedin, ardındangözlemi başlatın · Hataları, erişimi,kuyrukları ve diskiizleyin · Bağımsız kontrolnoktalarını koruyun · Verileri dışa aktarınve doğrulayın

**Diyagramın metin olarak gösterimi**

1. Depolama ve anahtar korumasını seçin → Token ile paneli açın
2. Token ile paneli açın → Bir çalışma alanı seçin
3. Bir çalışma alanı seçin → Doğrudan veya proxy yolunu yapılandırın
4. Doğrudan veya proxy yolunu yapılandırın → Telefon numarasını girin veya dosyaları / QR kodunu seçin
5. Telefon numarasını girin veya dosyaları / QR kodunu seçin → Hesap kimliğini kontrol edin ve erişilebilir grupları seçin
6. Hesap kimliğini kontrol edin ve erişilebilir grupları seçin → Olay ve ek politikalarını kaydedin, ardından gözlemi başlatın
7. Olay ve ek politikalarını kaydedin, ardından gözlemi başlatın → Hataları, erişimi, kuyrukları ve diski izleyin
8. Hataları, erişimi, kuyrukları ve diski izleyin → Bağımsız kontrol noktalarını koruyun
9. Bağımsız kontrol noktalarını koruyun → Verileri dışa aktarın ve doğrulayın

Yetkilendirme, aktarım bağlantısı, bir gruba erişim ve teslimatın eksiksizliği farklı özelliklerdir. Yeşil bağlantı durumu, tüm olayların kaydedildiği anlamına gelmez.

## Ana anahtarı paylaşmadan çalışmaları paylaşın

Bir gözden geçiren veya analiste kendi jetonunu vermek için Açık **Erişim**. Hangi hesapları ve sohbetleri açabileceklerini seçin, ardından görüntüleme, dışa aktarma veya operasyonel işlemlere izin verin. Toplamayı başlatan/durduran bir operatörün tüm çalışma alanına erişimi gerekir; bir gözden geçirenin erişimi tek bir sohbetle sınırlandırılabilir. Oturum sınırları, süre dolumu ve IP kuralları, Telegram hesap yetkilendirmesinden ayrıdır. [Erişim ve izinlere](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) bakın.

Bir bağlantıyı sonlandırmak için "**Açık oturumlar"** seçeneğini kullanın veya tüm oturumları sonlandırmak üzere erişimi iptal edin. Yönetici konsolu, çalışma alanları genelinde mevcut işlem etkinliklerini bir araya getirir. Oturumun kapatılması, veri toplama işleminin devam etmesini sağlar.

## Çalışma modları

| Mod | Eylem | Davranış |
| --- | --- | --- |
| Demo | scripts\Demo.cmd veya `--demo` | Sentetik veriler; gerçek hesap bağlantıları devre dışı bırakılmıştır |
| Gözlem | Gözlemi başlat | Seçilen kaynaklar için gönderilen güncellemeleri kaydetme |
| Geçmişe bir bakış | Kaynaklar → geçmiş anlık görüntüsü | En fazla 500 güncel mesaj; geçmişteki tüm değişikliklerin yeniden oluşturulması yapılmaz |
| Duraklat | Gözlemi duraklat | Verileri ve kuyrukta bekleyen işleri korurken toplama işlemini durdurun |
| İnceleme/devir teslim | Dışa aktarma | ZIP, JSONL/CSV/HTML, kontrol noktası, işlem onayı ve zaman damgası talebi |
| Birden fazla hesap | Çalışma alanları veya en üstteki **+** düğmesi | Tek bir işlem içinde istediğiniz sayıda ayrı çalışma alanı |

Yerel demo erişimi, manuel jeton girişi yapılmasına gerek kalmadan otomatik olarak açılır. Bu erişim, yalnızca izole edilmiş bir sentetik demoya doğrudan loopback erişimi için geçerli olan işlem ömrü süresince geçerli bir yetki kullanır; ana panel jetonu ifşa edilmez. Gerçek çalışma alanları ile uzaktan veya proxy üzerinden demo erişimi, jeton kimlik doğrulamasını korur. Demo girişi, Telegram yetkilendirmesi sağlamaz.

## İzleme kategorileri

![Sentetik kaynak verileriyle hesap başına izleme ayarları](https://phishdestroy.github.io/TgWitness/assets/sources.png)

**Kaynaklar → Yakalama ayarları → Hangi değişikliklerin saklanacağını seçin** bölümünden yeni mesajları, düzenlemeleri, silme bildirimlerini, tepki güncellemelerini ve üyelik olaylarını ayrı ayrı seçin. Varsayılan ayar tüm kategorileri saklar. **Mesajlar, düzenlemeler ve silmeler** seçeneği, orijinal bağlamı korurken ayrı tepki/üye güncellemelerini devre dışı bırakır. "**Tüm görünür etkinlikler" seçeneği ise** beşini de geri yükler. Ön ayarlar formu değiştirir; uygulamak için "**İzleme ayarlarını kaydet"**e basın.

Kaydedilen politika, o çalışma alanındaki tüm seçili kaynaklar için geçerlidir. Diğer çalışma alanları kendi ayarlarını korur. Her bir gerçek değişiklik, imzalanmış "önce/sonra" değerlerini kaydeder; mevcut politika ayrıca işlem makbuzlarına ve gözlem başlangıç kayıtlarına da dahil edilir. Bir kategorinin devre dışı bırakılması, önceki gözlemleri silmez. Yeniden etkinleştirme işlemi, kaçırılan değişiklikleri geri getirmez. Bu sürümde grup bazında kategori geçersiz kılma özelliği bulunmamaktadır.

Önceki içerik önemliyse yeni mesajları etkin tutun: bir silme bildirimi, hiç yakalanmamış metni geri getiremez. Operasyonel/kapsam kayıtları ve diğer grup hizmet olayları her zaman saklanır. Açık geçmiş anlık görüntüleri, canlı kategori seçiminden ayrıdır ve hizmet mesajlarını içerebilir. Bu ayarlar, aksi belirtilmedikçe yakalanan bir Telegram nesnesine gömülü tepki/üye meta verilerini sansürlemez.

Geçmiş anlık görüntüsü, duraklatıldığında ekleri kuyruğa alabilir. Bunları işlemek için gözlemi başlatın. Kuyruğa alınmış olması, indirilmiş olduğu anlamına gelmez. Ulaşılamayan orijinal dosya, daha yeni bir düzenlenmiş sürümle değiştirilmez; sonuçlar ayrı olarak kaydedilir.

**Kilitleme işlemi,** tarayıcı erişimini ve gizli alanları temizler ancak veri toplama işlemini devam ettirir. Sekmeyi kapatmak da işlemi devam ettirir. Python sürecini veya hizmetini durdurmak, tarayıcının durumuna bakılmaksızın veri toplama işlemini durdurur.

Ek bir çalışma alanının silinmesi, toplayıcısını durdurur ve yerel verilerini kaldırır. Eğer kilitli bir dosya veya dosya sistemi hatası silme işlemini kesintiye uğratırsa, panel hatayı bildirir ve çalışma alanını kullanılamaz (`DeletionPending`) olarak listede tutar. Dosyalarını tutan programları kapatın ve **Silme işlemini** yeniden deneyin. TgWitness'ı yeniden başlatmak, o çalışma alanını durdurulmuş halde bırakır ve kısmen kaldırılmış günlüğünü veya anahtarlarını yeniden oluşturmaz. Başarılı bir silme işlemi, yalnızca dizin kaldırıldıktan sonra kaydedilir; ayrı olarak dışa aktarılan veya yedeklenen kopyalar, kendi saklama politikası kapsamında kalır.

## Bildirimler

**Kaynaklar → Bildirimler → Uyarılar'ı ve günlük özeti** açın. TgWitness, Apprise'ı kullanarak Matrix, Telegram, Discord, Slack, ntfy, e-posta ve diğer desteklenen hizmetlere uyarılar gönderir. Bir çalışma alanına birden fazla hedef ekleyebilirsiniz.

1. Her satıra bir Apprise hedef URL'si girin. Kullandığınız hizmet için [hizmet kataloğuna ve URL biçimlerine](https://appriseit.com/services/) bakın.
2. **"Bildirimleri gönder**" seçeneğini etkinleştirin, ardından sorun uyarılarını, izlenen sohbetlerdeki değişiklikleri ve günlük özeti seçin. Özet saati, sunucunun saatini kullanır.
3. Silinen ve düzenlenmiş mesajlardan kaydedilen metinlerin uyarılarda yer almasını istiyorsanız, "**Kısa alıntılar ekleyin**" seçeneğini etkinleştirin.
4. **"Bildirimleri Kaydet"** düğmesine basın, ardından teslimatı kontrol etmek için "**Test Gönder" seçeneğini seçin**.

Kendi alıcınız için Apprise’ın [JSON webhook’unu](https://appriseit.com/services/json/) kullanın. Örneğin, `jsons://notify.example.org/tgwitness` HTTPS üzerinden o uç noktaya JSON gönderir. Bu kurgusal bir örnektir; bunu kendi hedefinizle değiştirin.

Hedefler ve ayarlar, seçilen çalışma alanına aittir. Değişiklik bildirimleri, yeni eklenen sohbetler de dahil olmak üzere izlenen kaynakları kapsar. Üst çubuktaki zil simgesi ayrıca son sorunları ve sohbet değişikliklerini de listeler.

Demoda, bildirim denetimleri görünür durumdadır ancak gönderme işlevi devre dışıdır. Gerçek bir çalışma alanında teslimat ayarlarını yapılandırın. Bildirimler, o çalışma alanının Direct, SOCKS5 veya HTTP yolunu kullanır; MTProxy bunları taşıyamaz. SMTP gibi HTTP dışı hedefler için doğrudan bir yol gereklidir.

## Panel düzeni

![Sentetik veriler kullanılarak oluşturulan bağlantı çalışma alanı](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Günlük**, gözlemleri, arama sonuçlarını ve filtreleri gösterir. Düzenleme yapıldığında yakalanan sürümler açılır; silme işlemi yapıldığında, varsa önceki içerik görüntülenir. Kaynağı bilinmeyen içerikler açıkça belirtilir. Sayımlar "**Genel Bakış"** bölümünde mevcuttur; toplama ayrıntıları yerel kılavuzda yer alır.

**Kaynaklar** bölümünde gözlem kapsamı (seçilen sohbetler, bir Telegram klasörü veya tüm hesap), her türden erişilebilir sohbetler, öncelik yıldızlarıyla işaretlenmiş seçilmiş kaynaklar, ek ve yeniden kontrol ayarları ile geçmiş anlık görüntüleri yer alır. Özel kaynaklar, herkese açık bir bağlantı olmaksızın diyalog/ID yoluyla seçilir. Erişim durumu, kalıcı izinleri değil, en son kontrolü belirtir.

**Sohbetler → Kişiler,** kaydedilmiş mesajları olan herkesi listeler; sohbet için kişi profilleri etkinleştirildiğinde, bir tıklama ile o kişinin profili açılır ve burada günlük kayıtlarına bağlantılar bulunur.

**Witness**, salt okunur tanık belirteçleri oluşturur, her bir tanığın en son ne zaman kontrol edildiğini gösterir ve bir tanığı ([bağımsız tanık](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/)) çalıştırmak için gerekli komutları ve seçenekleri sunar.

**"Parameters"** bölümü, başka bir sayfada yer almayan çalışma alanının tüm sınırlarını ve hız ayarlarını içerir: okunan diyalog sayısı, sohbet listesinin yeniden okunma sıklığı, kalp atışı ve kontrol noktası aralıkları, başlangıç tamponu, yeniden kontrollerinin isteklerini nasıl dağıttığı (ilk gecikme, her geçiş başına sohbet sayısı, sohbetler arası duraklama, kurtarılan ve yeniden istenen mesajlar), disk ayırma alanı, zaman aşımları ve indirme denemeleri, kullanıcı profillerinde arananlar (kendi düzenli ifadeleriniz dahil), bildirimlerin boyutu ve sıklığı, anlık görüntü, ZIP ve tarayıcı indirme sınırları ile Telegram istemcisinin zaman aşımları ve denemeleri. Her alan, aralığını ve varsayılan değerini gösterir; değiştirilen alanlar işaretlenir ve tek tek veya toplu olarak geri yüklenebilir. Her değişiklik, öncesi ve sonrasındaki değerlerle birlikte `parameters.changed` olarak kaydedilir ve gözlem başlangıç kayıtları, geçerli değerleri belirtir. Değerler bir sonraki kullanımdan itibaren geçerlidir; istemci zaman aşımları ve yeniden denemeler ise bir sonraki bağlantıdan itibaren geçerlidir. Yeniden kontrol aralıkları, ek türleri ve boyutları, kanıt ve site dışı kopya aralıkları kendi sayfalarında kalır ve yalnızca ön ayarlar değil, aralıklarındaki herhangi bir değeri alabilir.

Üst çubuktaki zil simgesi, izlenen sohbetlerdeki son sorunları ve değişiklikleri listeler; okunmamış mesajlar, okundu olarak işaretlenene kadar sayılır. Değişiklikler sohbet ve saat bazında gruplandırılır ("12 silindi, 1 düzenlendi, 0 bulunamadı") ve oturum kapatma veya disk dolması gibi sorunlar, sohbetler ne kadar yoğun olursa olsun listede kalır.

**Hesap oluşturma işlemi** telefon numarası alanından başlar. **Devam düğmesi** doğrudan kod girişine yönlendirir ve yalnızca eksik olduğunda API kimlik bilgilerini ister. QR ve dosya içe aktarma alternatif sekmelerdir. Kaydedilen API kimlik bilgileri yalnızca kendi çalışma alanı içinde yeniden kullanılır. Giriş ekranında kenar çubuğu, istatistikler veya ayar paragrafları bulunmaz. **Ayarlar** simgesi, API, proxy, depolama ve ek hesap kontrollerini açar. Yeni kurulumlar buradan başlar; seçili kaynağı olmayan bağlı hesaplar ise "**Sohbetleri Seç"** bölümünden başlar. Yolun değiştirilmesi, gözlemin duraklatılmasını gerektirir ve tamamlanmamış oturum açma işlemini iptal eder. Mevcut bir günlük, farklı bir Telegram hesabına sessizce yeniden bağlanamaz.

**Dışa aktarma işlemi,** günlüğün bütünlüğünü kontrol eder ve taşınabilir dosyalar oluşturur. Çalışma alanı kimliği indirme komut satırı arayüzüne (CLI) aktarılabilir. Her dışa aktarma işlemi, tam bir günlük önekini sabitler; daha sonraki olaylar bir sonraki dışa aktarma işlemine dahil edilir. Arama filtreleri, paket kapsamını değiştirmez. Ayrıntılı imzalama ve kapsama bilgileri, "**Doğrulama ve sınırlamalar**" bölümünde yer almaktadır.

Panel, toplayıcının durumunu, kuyrukta bekleyen/başarısız medya öğelerini, en eski bekleyen medya öğelerini, boş disk alanını, istek duraklamalarını ve "**Toplayıcı sağlığı**" altında erişimi onaylanmamış kaynakları bildirir. Bu ayrıntılar başlangıçta daraltılmış ve "Hesap" sayfasında gizlenmiştir. Bir kurulum kartı bir sonraki adımı gösterir: bir hesap bağlayın, kaynakları seçin veya gözlemi başlatın. Hesap listesi, yükleme anındaki bir anlık görüntüdür; seçilen çalışma alanı periyodik olarak yenilenir. Bu, çok işlemli bir SLA izleme aracı değildir.

Kullanıcı arayüzü, kaynak içerik için yerel varlıklar ve metin işleme kullanır. Masaüstü ve dar Chromium düzenleri test edilmiştir. Bu, eksiksiz bir erişilebilirlik sertifikası değildir; ekran okuyucu ve insan kullanım kolaylığı değerlendirmeleri ayrı çalışmalar olarak devam etmektedir.

## Dağıtım ortamları

| Ortam | Kurulum | Doğrulama durumu |
| --- | --- | --- |
| Windows PC/sunucu | Python 3.11+, scripts\Setup.cmd/Start.cmd, özel veri dizini | Windows/Python 3.12 üzerinde yerel olarak test edilmiştir. |
| Linux sunucusu/VPS | Python venv, özel hizmet kullanıcısı, HTTPS/SSH | Kod, CI ve systemd örnekleri sunulmuştur; bu sunucuda çalıştırılmamıştır |
| macOS | Python venv, ön plan işlemi veya kullanıcı ajanı | launchd örneği sunulmuştur; ayrı bir kurulum kontrolü gereklidir |
| Docker/Compose | Sabit hacim, tek çalışan | Tanım ve CI çalışma zamanı kontrolü sağlanmıştır; Docker yerel olarak kullanılamaz |
| Telefon tarayıcısı | Çalışır durumdaki bir sunucudaki korumalı panele bağlanın | Chromium tabanlı dar ekran düzeni test edilmiştir; toplayıcı iOS/Android'de çalışmaz. |

Taşınabilirlik, zorunlu bir bulut hizmeti veya ön uç kurulumunun gerekmediği anlamına gelir. Her hedef sistemde yine de uyumlu Python/kripto bağımlılıkları, yerel disk ve ağ erişimi bulunmalıdır. [DEPLOYMENT.md dosyasına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/) ve [hizmet şablonlarına](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) bakınız.

Çalışma alanları CPU, bellek ve bir olay döngüsünü paylaşır. İşlem izolasyonu için farklı örnekler, bağlantı noktaları, veri dizinleri ve hesap yetkilendirmeleri kullanın. Ayrı örnekler arasında birleşik bir kontrol paneli yoktur. Asla birden fazla işleyicisini tek bir veritabanına yönlendirmeyin.

## Başlangıç kontrolleri ve dışa aktarmalar

Hazırlanmış bir ortamı başlatmadan önce `python start.py --check` komutunu çalıştırın. Makine tarafından okunabilir kontroller için `--json` komutunu ekleyin veya amaçlanan `--data-dir`, `--host` ve `--port` komutlarını geçirin. Bu komut, Telegram'da oturum açmaya veya bir günlük oluşturmaya gerek kalmadan ön koşulları kontrol eder. Günlüğü doğrulamaz veya yakalama hazırlığını kanıtlamaz; günlük doğrulaması, uygulamanın başlatılması sırasında gerçekleştirilir. Meşgul bir bağlantı noktası, sadece mevcut bir örnek olabilir.

Dosya Sistemi Erişimi API'sini destekleyen tarayıcılar, dışa aktarımları yazılabilir bir akış üzerinden kaydeder. Diğer tarayıcılar ise en fazla 128 MiB'lik bir tampon kullanır. Daha büyük dışa aktarımlar veya dosya akışını desteklemeyen tarayıcılar için akış CLI'sini kullanın:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Bir alt çalışma alanı için Exports'tan `--profile ID` 'yi ekleyin. Uzaktan erişim için `--url https://server` 'yi kullanın. Düz HTTP yalnızca loopback hedefleri için kabul edilir. Jeton bir dosyadan okunur ve bir başlıkta gönderilir; yazdırılmaz veya bir URL'ye eklenmez. Yönlendirmeler reddedilir. Mevcut hedeflerin üzerine yazılmaz. Başarısız aktarımlar, geçici parça dosyalarını siler. Bildirilen SHA-256, bir aktarım sağlama toplamıdır; imzalı ZIP dosyasını güvenilir bir parmak izi/kontrol noktası ile ayrı olarak doğrulayın.

## Yedekleme, geri yükleme ve kesintiler

1. Gözlemi duraklatın ve işlemi sorunsuz bir şekilde sonlandırın.
2. Tüm veri dizinini kopyalayın: veritabanları, varsa WAL/SHM, medya, `credentials.enc`, `signing.enc`, `network.enc`, kasa anahtarları/meta veriler, token, kontrol noktaları ve tüm `profiles/` dizinleri.
3. Harici anahtar modu için, ana anahtarı ayrı olarak saklayın ve her bir `vault.external.json` değerini muhafaza edin. Yeni bir anahtar oluşturmak, eski gizli bilgileri geri getiremez.
4. Hedef durdurulmuşken geri yükleme yapın; devam etmeden önce orijinal anahtarı yapılandırın, erişimi kısıtlayın ve bütünlüğü doğrulayın.
5. Kesinti sürelerini ve doğrulama sonuçlarını kaydedin. Bir geçmiş anlık görüntüsü, kesinti sırasında hiçbir silme işleminin gerçekleşmediğini kanıtlayamaz.

Kanıt ZIP dosyaları, oturum bilgilerini ve özel anahtarları içermez ve tam hizmet yedeklemeleri değildir. Dört öğe farklı şekilde korunur:

| Ne | Koruma |
| --- | --- |
| Parolasız dışa aktarma dosyaları (varsayılan) | Şifrelenmemiştir. İmzalı olduğundan değişiklikler tespit edilebilir, ancak dosyaya sahip olan herkes dosyayı okuyabilir. |
| Parolalı dışa aktarma dosyaları | Bir şifre belirlediğinizde, tamamlanan dışa aktarım, 7-Zip ve WinRAR ile açılabilen bir WinZip AES-256 ZIP dosyasına değiştirilmeden aktarılır; şifre saklanmaz ([delil işleme](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)). |
| Günlük veritabanı ve diskte kaydedilen ekler | TgWitness tarafından şifrelenmez; şifreli bir disk veya birim kullanın |
| Telegram oturumları ve imzalama anahtarları | Veri dizininde şifrelenmiştir (`credentials.enc`, `signing.enc`, `network.enc`) |

Tam hizmet yedeklemesi, yukarıda açıklanan durdurulmuş veri dizinidir; bir dışa aktarım değildir. Her ikisi için de korumalı depolama alanı ve kasıtlı bir aktarım mekanizması kullanın. Geçici sunucu dışa aktarımları her çalışma alanının `temporary-exports/` dizininde bulunur; tamamlanan yanıtlar temizlenir ve kesintiye uğrayan dışa aktarım dosyaları, o çalışma alanının örnek kilidi tutulurken bir sonraki başlatmada kaldırılır.

Bağlantının yeniden kurulması, ara aşamadaki değişikliklerin geri yükleneceğini garanti etmez. Kalıcı medya işleri ve Telegram güncelleme durumu, yeniden başlatma işleminden sonra da korunur; [kanıt formatına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#durable-collection-and-process-receipts-02) bakınız.

## Kapasite ve saklama süresi

Varsayılan sınırlar, tümü **Parametreler** altında değiştirilebilir: ilk 1.000 diyalog, anlık görüntü başına 500 mesaj, 4 GiB sıkıştırılmamış imzalı ZIP içeriği (daha büyük arşivler için `verify.py --max-gib N` gerekir) ve 128 MiB tarayıcı yedeği. Ekler, **Kaynaklar → Ekler** altında tür başına 1–2.000 MiB yer kaplar. İndirme CLI'sinde varsayılan değer 5 GiB aktarımdır. Kullanılabilir disk alanı daha düşük bir sınır olabilir. Günlükler, medya, WAL, geçici dışa aktarmalar ve yedeklemeler için alan ayırın. Dışa aktarmalar, Compose'un 512 MiB'lik `/tmp` sınırı yerine veri hacmini kullanır.

Sadece grupları saymak yerine, saniye başına olay sayısı, kuyruk yaşı, medya bayt sayısı ve disk gecikmesini ölçün. Sentetik yerel performans testleri, Telegram mesajlarının teslim edilmesini garanti etmez. Otomatik saklama silme özelliği yoktur. Günlüğün son kısmını silmek, saklanan kontrol noktalarıyla olan ilişkisini geçersiz kılar.

Öncelikli yeniden kontroller halihazırda mevcuttur: yıldızlı kaynaklar varsayılan olarak her 15 dakikada bir, diğerleri ise her 6 saatte bir yeniden kontrol edilir ([yeniden kontrol kademelerine](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/#recheck-tiers) bakınız). Yukarıda açıklandığı gibi şifre korumalı dışa aktarımlar mevcuttur. Canlı Telegram/proxy kabulü, kalıcı tekrar oynatma, yönetici günlüğü ve tepki anketi, izole edilmiş işleyiciler, yerel günlüğün ve medyanın TgWitness tarafından şifrelenmesi ve bağımsız inceleme ayrı çalışmalar olarak devam etmektedir. Kapsamlı erişim, [erişim ve izinler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) bölümünde belgelenmiştir. [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) ve [VERIFICATION.md dosyalarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) bakınız.
