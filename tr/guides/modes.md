# Tek bir günlük. Dört toplama modu. Sekiz doğrulama seviyesi.

Canonical page: https://phishdestroy.github.io/TgWitness/tr/guides/modes.html

Modlar, senaryolar ve kanıt düzeyleri

TgWitness bağlı hesabın gözlemlediklerini kaydeder. Üçüncü bir taraf, kaydı bağımsız olarak güvenilir bir anahtara göre doğrulayabilir.

[Toplama modları](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#scope)[Senaryolar](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#scenarios)[Kanıt düzeyleri](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#levels)

3–5 dakikalık genel bakış · kurgusal örnekler · mevcut uygulama

1. **Telegram**

   Hesap tarafından görülebilen güncellemeler
2. **Toplayıcı**

   Bağlantılı kayıtlar, her biri imzalanmış
3. **Doğrulayıcı**

   Güvenilir anahtar + korunan sınır

`h₁ → h₂ → h₃ · Ed25519`Bütünlük kontrol edilir. Telegram kaynağı ile bir mesajın doğruluğu ayrı konular olarak ele alınır.

## Gözlem kapsamını seçin

Üç kapsam ve bir soruşturma ön ayarı. Hariç tutmalar ve etkinleştirilmiş kaynak türleri hâlâ geçerlidir.

Varsayılan**Seçilen sohbetler**

Kayıtlar

Yalnızca elle seçilmiş kaynaklar.

Yeni sohbetler

Otomatik olarak eklenmez.

Şunları seçin:

Bilinen bir kanal veya grup kümesi. Sabit bir sohbet kapasitesi belirlenmemiştir.

**Ne yapmaz** Diğer sohbetleri keşfetmez veya önceki geçmişi doldurmaz.

Hesap klasörü**Telegram klasörü**

Kayıtlar

Klasör dahil edilenler ve kategoriler; yapılandırıldığında hariç tutulanlar ve arşivlenmiş sohbetler hariç.

Yeni sohbetler

Etkin sohbetlerin eşleştirilmesi; bir saat içindeki klasör değişiklikleri.

Şunları seçin:

Bir analist zaten bir vaka dosyası tutmaktadır. Toplanan verilerin özel bir hesapta saklandığını doğrulayın.

**Ne yapmaz** Klasörün değişen muted/read koşulları geçerli değildir.

Kapsamı doğrulayın**Hesabın tamamı**

Kayıtlar

Seçilen türler dahilinde, özel sohbetler ve botlar da dahil olmak üzere hesap tarafından görülebilen sohbetler.

Yeni sohbetler

İlk güncelleme geldiğinde eklenecektir.

Şunları seçin:

Bir vakaya katılan hesap da dahil olmak üzere, özel bir gözlem hesabı.

**Ne yapmaz** Sohbetlere otomatik olarak katılmıyor veya kaynak erişimini atlamıyor.

Tüm hesap ön ayarı**Araştırma modu**

Kayıtlar

Tüm kaynak türleri, kendi eylemler, kaynak profilleri ve yeni keşfedilen kaynakların en son 200 görünür mesajı.

Yeni sohbetler

Yeni bir sohbet veya bot, bir profil ve geçmiş anlık görüntüsü alır.

Şunları seçin:

Panel aracılığıyla bir takıma katılın veya bir botla etkileşim kurun. Ön ayarı inceleyin ve kaydedin.

**Ne yapmaz** Mevcut her sohbetin anlık görüntüsünü almaz veya başka bir istemcide basılan geri çağırmaları gözlemlemez.

Bu kartlar yerel bir karşılaştırma amaçlıdır, canlı toplayıcı kontrolleri değildir. Hesap üzerinde herhangi bir değişiklik yapmazlar.

**Ne yapmaz** Hiçbir mod gizli sohbetleri okumaz, işlem durdurulmuşken kayıt yapmaz, kaynaklara kendi başına katılmaz veya istenen sürenin ötesindeki geçmişi almaz. snapshot/export.

[Ayrıntıları okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/)

## GitHub Actions ile kayıt (önizleme)

Yeni bir Telegram oturumu, tek sohbet, şifrelenmiş arşiv ve GitHub köken doğrulaması.

[Kayıt yardımcısını aç](https://phishdestroy.github.io/TgWitness/tr/docs/capture/)

## Neler kaydedilir

Yalnızca iletilen veya açıkça talep edilen gözlemler kayda alınır. Bilinmeyen kaynaklar bilinmeyen olarak kalır.

 Anahtarları yakalayın · yerel örnekYeni mesajlarDüzenlemelerSilme işlemleriTepkilerÜyelik

Panel, bu anahtarları çalışma alanı başına uygular. Birini kapatmak mevcut kayıtları korur; tekrar açmak kaçırılan olayları geri getirmez.

**Olay matrisi: kaydedilen materyal ve kalan bilinmeyenler**

| Kategori | Kaydedildi | Hâlâ bilinmiyor |
| --- | --- | --- |
| Mesaj | Metin, kimlikler, gönderen meta verileri, yanıt bağlamı ve orijinal güncelleme zarfı. | Üçüncü taraflarca doğrulanabilir bir Telegram imzası yoktur. |
| Düzenle | Gözlemlenen her sürüm, önceki sürümlerin üzerine yazılmadan. | Ara düzenlemeler gözden kaçabilir; gönderenin mutlaka düzenleyici olduğu söylenemez. |
| Silme | Bildirim ve varsa daha önce kaydedilmiş metin. | Silici ve tam eylem zamanı belirtilmez. |
| Kapsam dışı silme | Hesap düzeyinde bildirim; bilinmeyen eş açıkça belirtilir. | Tahmin edilen sohbetler kullanmayın. Korelasyon, mümkün olduğunda önceden kaydedilmiş hesap kapsamındaki kimlikleri kullanır. |
| Tepki | İletilen sayaçlar ve görünür son kimlikler. | Her reaktör görünür değildir; tam ve kullanılabilir bir liste için ayrı sorgular gerekir. |
| Üyelik | Teslim edilen hizmet mesajları ve katılımcı güncellemeleri. | Rol ve sohbet türü görünürlüğü sınırlar; sessizlik, yokluğu kanıtlamaz. |
| Ek | Orijinal sürüm tanımlayıcısı, kaydedilen baytlar, SHA-256 ve deneme sonuçları. | Silinmiş bir dosya erişilemez olabilir; daha yeni bir sürüm onun yerini almaz. |
| Geçmiş anlık görüntüsü | Şu anda görünür olan mesajlar, geçmiş gözlemleri olarak işaretlenmiştir. | Daha önceki düzenlemeler ve silinmiş içerikler yeniden oluşturulmaz. |
| Kendi eylemleriniz | Giden messages/edits ve eşleşen yanıt klavyesi button_press meta verileri. | Başka bir Telegram istemcisinde tetiklenen geri çağırmalar görünmez. |
| Bot düğmeleri | Geri arama, URL, web uygulaması ve istek meta verileri mesajla birlikte saklanır. | URL'ler ve phone/location istekler metin niteliğindedir; otomatik olarak açılmaz veya yürütülmez. |

### Varsayılan ek sınırları

Fotoğraflar

20 MiB

Video

100 MiB

Dosyalar

50 MiB

Animasyonlar

20 MiB

Video notları

50 MiB

Ses

20 MiB

Ses

50 MiB

Çıkartmalar

5 MiB

**Ne yapmaz** Bir anahtar, gömülü meta verileri sansürlemez veya operasyonel kayıtları devre dışı bırakmaz. Yakalama işlemi, Telegram tarafından sağlanmayan bir aktörü tanımlamaz.

[Ayrıntıları okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/)

## Sahip olduğunuz yetkilendirmeyi kullanın

Her hesabın kendine ait bir çalışma alanı, günlüğü, imzalama anahtarı, yolu ve kuyruğu vardır.

### Telefon + kod

Etkinleştirildiğinde 2FA tuşuna basın.

### QR kod

Yetkili bir cihazdan tarama yapın; 2FA bu yine de gerekli olabilir.

### Telethon .session

Hesabın oturum dosyasını içe aktarın.

### Pyrogram .session

Desteklenen Pyrogram oturum biçimini içe aktarın.

### TData ZIP

Desteklenen tek bir Desktop hesabı; ayarlanmışsa yerel şifre.

### StringSession metin

Bir Telethon StringSession.

### .session + .json

Oturumu ve eşleşen eşlik eden meta verileri seçin.

### Doğrulama anahtarı HEX + DC ID

Hesap yetkilendirmesini veri merkezi tanımlayıcısıyla birlikte içe aktarın.

**API çift**

Kendi API çiftiniz isteğe bağlıdır. Çiftiniz yoksa, TgWitness resmi Telegram Desktop'tan gelen çiftler de dahil olmak üzere halka açık çift havuzunu kullanır.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy deneysel bir özelliktir; yerleşik genel MTProxy kullanılabilir. Başarısız bir proxy yolu, doğrudan bağlantıya geri dönmez.

Aynı makinede bulunan iki çalışma alanı, iki bağımsız tanık değildir.

**Ne yapmaz** İçe aktarma, Telegram yetkilendmesini atlamaz, 2FA veya desteklenmeyen oturum biçimlerini atlamaz. Hesaplar yine de uygulama sürecini paylaşır.

[Hesap biçimleri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/)

## Panelden işlem yapın

Gönderin veya yanıtlayın, mevcut bir bot düğmesine basın, bağlantı önizlemesini kaydedin, ardından bir sohbete açıkça katılın veya başlangıç parametresiyle bir botu başlatın.

`interaction.preview``interaction.requested``interaction.result`

Önizleme, istek ve sonuç makbuzları imzalanır. Bir düğmeye basılmadan önce, sunucu mesajı tekrar alır ve değiştirilmiş bir klavyeyi reddeder. Geri dönen geri arama metni ve URL'ler, kaydedilmiş bağlamda kalır.

**Ne yapmaz** Web uygulamaları, ödemeler, phone/location paylaşım veya satır içi sorgular. Bir URL'nin görüntülenmesi, onu açmaz.

[Ayrıntıları okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/)

## Kurtarma ve süreklilik

Eksiklikler gizlenmez, gösterilir.

### Kaydedilen konuma geri dön

Yeniden başlatmanın ardından, Telegram'dan kaçırılan güncellemeler istenir. Sınırlı saklama süresi ve süresi dolmuş farklılıklar, boşluklara neden olabilir.

### Görünür mesajları yeniden kontrol edin

Varsayılanlar: öncelikli kaynaklar her 15 dakikada bir, diğerleri her 6 saatte bir. Sonuçlar şunları içerir message.recovered ve message.missing_on_recheck.

### Oku coverage.json

Gözlem dönemleri, nedenleriyle birlikte boşluklar ve gözlemlenmemiş kimlikler, imzalanmış dışa aktarımla birlikte verilir. Yeniden kontrol edildiğinde eksik olan bir kayıt, silme bildirimi değildir.

**Ne yapmaz** Daha sonraki bir geçmiş anlık görüntüsü, bir kesintiyi silmez veya kaybolan her sürümü geri getirmez. Kaydedilen imleç, günlüğün kabul edildiğine dair kayıpsız bir onay değildir.

[Ayrıntıları okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)

## Yedi seviye. Farklı sorular.

Her mekanizma sınırlı bir soruyu yanıtlar. Harici hizmetleri ayrı ayrı yapılandırın ve güven dayanaklarını toplayıcının dışında tutun.

1. ### Kaydet

   SHA-256 zincir + Ed25519 olay başına; ilk previous_hash 64 sıfırdır.

   **Üçüncü taraf kontrolleri** Sabitlenmiş toplayıcı anahtarı altında sıralama ve imzalar.

   **Ne yapmaz** Bu, Telegram kökenini veya eksiksizliğini kanıtlamaz.

   **Doğrulama komutu**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Konteyner

   manifest.json dosya hash'lerini listeler; manifest.sig imzalayın. media.saved ek baytlarını bir olaya bağlar.

   **Üçüncü taraf kontrolleri** Sağlanan dosyalar, imzalanmış manifest ve medya makbuzlarıyla uyumludur.

   **Ne yapmaz** Ayrı olarak indirilen CSV, HTML veya ekran görüntüsünü imzalamaz.

   **Doğrulama komutu**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Korunan sınır

   Başlangıçta kontrol noktası, varsayılan olarak her 5 dakikada bir ve düzenli durdurma. Başka bir yerde bir kopyasını saklayın.

   **Üçüncü taraf kontrolleri** Daha sonraki dışa aktarım, daha önce saklanan uzunluk ve başlık ile uyumludur; geri alma tespit edilebilir.

   **Ne yapmaz** Hem günlüğün hem de saklanan tüm kontrol noktalarının değiştirilmesini algılamaz.

   **Doğrulama komutu**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Harici zaman

   Kanıt modu bir kontrol noktası gönderir SHA-256 yetkili makamlara RFC 3161 yetkililere (FreeTSA, DigiCert) ve OpenTimestamps takvimlere bir kontrol noktası gönderir.

   **Üçüncü taraf kontrolleri** Doğrulanmış bir TSA yanıtı bu baytların tarihini belirtir; onaylanmış bir OpenTimestamps kanıt ise bunları Bitcoin’e bağlar.

   **Ne yapmaz** Hazırlanmış bir isteği veya bekleyen takvim makbuzunu onaylanmış bir zaman damgası olarak değerlendirmez.

   **Doğrulama komutu**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Bağımsız tanık

   Ana bilgisayarı, kapsamlı salt okunur uç noktayı, yeni meydan okumayı ve kendine ait key/journal ve TGW1 kanal gönderilerini ayırın.

   **Üçüncü taraf kontrolleri** Daha önce kabul edilen başlıklar; durumlar: ok, key_changed, geri alma, çatallanma, geçersiz ve no_response.

   **Ne yapmaz** Bu, tek bir toplayıcı ana bilgisayardaki iki çalışma alanını bağımsız tanıklara dönüştürmez.

   **Doğrulama komutu**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Site dışı kopya

   S3- uyumlu kopya, AES-256-GCM; Object Lock ile şifrelenmiş kopya.

   **Üçüncü taraf kontrolleri** Restore, yalnızca günlük, kontrol noktası ve korunmuş medya doğrulaması başarıyla tamamlandıktan sonra dosyaları yayınlar.

   **Ne yapmaz** Dışa aktarılan anahtar olmadan geri yükleme yapmaz veya depolama yanıtını kontrol etmeden saklama varsayımı yapmaz.

   **Doğrulama komutu**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Kaynak bilgisini çalıştırın

   İmzalı çalıştırma makbuzu: kaynak hash'leri, bağımlılık sürümleri ve işlem bağlamı. Kendi beyanına göre.

   **Üçüncü taraf kontrolleri** İmza toplayıcısının kendi çalışmasıyla ilgili bildirdiği bilgiler.

   **Ne yapmaz** Bağımsız işlem doğrulaması sağlamaz veya kayda alınmadan önce güvenliği ihlal edilmesini dışlamaz.

   **Doğrulama komutu**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Hiçbir seviyenin kanıtlayamadığı şey

Her Telegram güncellemesinin iletilmesi; metnin doğruluğu; gönderen kimliğinin gerçek bir kişiyi tanımlaması; kayıt öncesinde toplayıcının güvenliğinin ihlal edilmemesi; mahkemede delil olarak kabul edilebilirlik.

[Bağımsız tanık](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/)

Yerel SHA-256 deney

### 2 numaralı kaydı değiştirmeyi deneyin

Bir sonraki kayıt, önceden kaydedilen bağlantıyı korur. Metnin değiştirilmesi, 2 numaralı kaydın hesaplanan hash değerini değiştirir.

Kayıt 2'nin metni

Kayıt 1`h1`64 sıfırla başlar

Kayıt 2`h2`Kaydedilenleri içerir h1

Kayıt 3`h3`Kaydedilenleri içerir h2

Statik örnek: h2 "11:00'da buluşalım" ifadesini içerir. Bu metnin değiştirilmesi h2; kayıt 3 hâlâ kaydedilene atıfta bulunur h2.

**Tam özetleri inceleyin**

Kaydedilen kayıt 2 hash

`SHA-256(e₂)`

Kayıt 2 hash'i yeniden hesaplandı

`SHA-256(e₂)`

Bu örnek, imzaları değil, hash değerlerini hesaplar. Gerçek doğrulayıcı, her imzayı ve bağlantıyı güvenilir anahtarla karşılaştırarak kontrol eder.

 [Ayrıntıları okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/how-it-works/)

## Kanıtlar üzerinden bir yol seçin

Kurgusal durumlar. İlgili olaydan önce verileri toplamaya başlayın; içerikle birlikte sınırları ve boşlukları da koruyun.

### Bir kanal ödeme bilgilerini değiştirir

Mod → olaylar

Seçilen sohbetler → mesajlar, düzenlemeler, silmeler.

Çıktı

Gözlemlenen gönderi sürümleri ve ekler hash değerleriyle belirtilmiştir.

Doğrulama

İmzalanmış ZIP + saklanan kontrol noktası + doğrulanmış TSA yanıtı.

**Ne yapmaz** Hiç yakalanmamış bir orijinali geri getirmez.

### Mesajlar bir olaydan sonra kaybolur

Mod → olaylar

Klasör veya tüm hesap → tüm olay kategorileri.

Çıktı

Kaydedilmiş orijinaller, silme bildirimleri ve eksiklikler içeren kapsam.

Doğrulama

İmzalı ZIP + bağımsız tanık günlüğü.

**Ne yapmaz** Aktör bilgisi içermeyen bir bildirimden siliciyi tanımlamaz.

### Bir mağaza botunu inceleyin

Mod → olaylar

Araştırma ön ayarı → düğmeler, bağlantı önizlemeleri ve açık bot başlatma.

Çıktı

İmzalı etkileşim makbuzları, geri dönen geri aramalar ve kaydedilmiş profiller.

Doğrulama

İmzalanmış ZIP; her dosyayı ZIP.

**Ne yapmaz** Bir bot web uygulamasını açmaz, ödeme yapmaz veya başka bir istemcinin geri aramalarını kaydetmez.

### Bir katılımcı, sohbetler arasında isim değiştirir

Mod → olaylar

Herhangi bir kapsam → gözlemlenen sender/profile meta veriler.

Çıktı

Sayısal kimlik numaralarına göre isim/kullanıcı adı geçmişi, “ayrıca şurada da” bağlantıları ve çıkarılan ipuçları.

Doğrulama

Dosya JSON imzalanmış olanla karşılaştırıldı ZIP.

**Ne yapmaz** Bu, bir cüzdanı, telefon benzeri bir dizeyi veya kullanıcı adını kanıtlanmış bir kimliğe dönüştürmez.

### Tesis dışı bir kopya ile uzun süreli gözlem

Mod → olaylar

Herhangi bir kapsam → Kanıt modu ve S3 desteklenen bir kopya Object Lock.

Çıktı

Şifrelenmiş kopya, saklanan kontrol noktaları ve zaman damgası yanıtları.

Doğrulama

Dışa aktarılan anahtarla geri yükleyin, ardından orijinal sunucu olmadan doğrulayın.

**Ne yapmaz** Bu, bağımsız bir tanığın veya ayrı olarak saklanan bir şifre çözme anahtarının yerini almaz.

[Ayrıntıları okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/investigation/)

## Doğrulanabilir bir paket teslim edin

İmzalanmış orijinali, bağımsız olarak saklanan anahtar parmak izini, ilgili kontrol noktasını ve doğrulama sonucunu sağlayın.

- İmzalı ZIP
- JSONL
- CSV
- HTML
- Kontrol Noktası
- Çalıştırma makbuzu
- Sohbet dışa aktarma: chat.json / chat.html
- Dosya JSON
- Şifre korumalı AES-256 ZIP
- Birden fazla hesap için ayrı dışa aktarımlar
- Akış CLI: 5 GiB varsayılan sınır

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Doğrulayıcıyı, kontrol edilen arşivden değil, güvenilir bir kopyadan alın.

**Ne yapmaz** Bağımsız CSV ve HTML imzalanmış kapsayıcılar değildir. Şifre, aktarımın gizliliğini korur, gerçekliğini değil. Birden fazla dışa aktarma işlemi, hesap günlüklerini birleştirmez.

[Ayrıntıları okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)

## Teslim edilen yapıyı karşılaştırın

İmza, zaman damgası veya tanık sistemleri eklenmemiş temel öğeler. Komut dosyaları ve günlük kaydediciler uygulamaya göre değişiklik gösterir; “kısmi” ifadesi, yakalanan veya görünür materyalle sınırlı olduğu anlamına gelir.

| Yaklaşım | Düzenlemeler / silmeler | İmzayı kaydedin | Harici zaman | Bağımsız tanık | Kapsam / eksiklikler | Yazar olmadan doğrulama |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram Desktop dışa aktarma | Kısmi | Hayır | Hayır | Hayır | Hayır | Hayır |
| Telethon snapshot komut dosyası | Kısmi | Hayır | Hayır | Hayır | Hayır | Hayır |
| Silme günlüğü: metin günlüğü | Kısmi | Hayır | Hayır | Hayır | Hayır | Hayır |
| Ekran görüntüleri / web yakalama | Kısmi | Hayır | Hayır | Hayır | Hayır | Hayır |
| TgWitness yapılandırılmış ek özelliklerle | Kısmi | Evet | Evet | Evet | Kısmi | Evet |

**Ne yapmaz** Tablo, her komut dosyasını veya günlük kaydı ürününü değerlendirmez. İsteğe bağlı zaman ve tanık kontrolleri, kendi hizmetlerini ve güven dayanaklarını gerektirir; hiçbiri kaynak doğruluğunu kanıtlamaz.

[Ayrıntıları okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)

## Kanıtlarla birlikte sınırları da koruyun

Doğrulama, kapsamı açıkça belirtildiğinde yararlıdır.

- Gizli sohbetler kullanılamaz.
- İşlem durdurulmuşken hiçbir şey kaydedilmez; kurtarma sınırlıdır.
- Doğrulanmış bir kayıt, içeriğinin doğru olduğunun kanıtı değildir.
- Anahtara sahip bir operatör, herhangi bir içeriği imzalayabilir. Bağımsız tanıklar ve zaman damgaları, daha sonraki değiştirme işlemlerini kısıtlar; dürüst olmayan ilk yakalama işlemlerini değil.
- Ana hesabınızı değil, bu iş için ayrılmış bir hesap kullanın.
- Telegram, istek hacmi nedeniyle hesaplara kısıtlama uygulayabilir.

**Ne yapmaz** Hiçbir mod veya kanıt seviyesi, yasal kabul edilebilirliği, Telegram'da tam teslimatı veya gerçek dünyadaki kimliği kanıtlamaz.

[Kurulum kılavuzu](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr)[Özel hesap](https://phishdestroy.github.io/TgWitness/tr/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/investigation/)
