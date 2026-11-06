# Panel kılavuzu

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/

Panelin tüm ekranları: sohbetler, günlük, kaynaklar, dışa aktarmalar, Ekstralar, koruma modları ve kod kontrolü.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[İlk kurulum ve ayarlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/settings/) · [Hesaplar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) · [Dışa aktarma ve doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) · [Vaka raporları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/)

Her ekranın işlevi, imzalı günlüğe ne yazdığı ve ayrıntılı kılavuzun bulunduğu yer. Panel, her seferinde tek bir çalışma alanını gösterir: kendi kaynakları, günlüğü ve imzalama anahtarı olan bir Telegram hesabı. Kenar çubuğunun üst kısmındaki seçici, çalışma alanları arasında geçiş yapar. Adres, çalışma alanını taşır (`?ws=…`); adres, seçici ve yüklü hesap birbiriyle uyuşmadığında işlemler engelli kalır.

Use [Compare collection methods](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md) to choose between live observation, full history, fresh account/chat exports and saved-record handover. The Exports page includes the same comparison above its download controls.

**On this page**

- [Find your way](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#find-your-way)
- [Start here](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#start-here)
- [Chats](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#chats)
- [Journal](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#journal)
- [Sources](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#sources)
- [Exports](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#exports)
- [Settings, accounts and connection](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#settings-accounts-and-connection)
- [Extras](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#extras)
- [Protection modes](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#protection-modes)
- [More tools](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#more-tools)

## Yolunuzu bulun

Günlük bölümler kenar çubuğunun en üstünde yer alır, **Hesaplar** ise **Çalışma Alanı'nın** altındadır, diğer her şey ise **Diğer araçlar ve ayarlar** altında bulunur. Üst çubuktaki **Arayüz seviyesi** anahtarı, kaç bölümün görüneceğini belirler:

| Seviye | Kenar çubuğundaki bölümler |
| --- | --- |
| Basit | Ana Sayfa, Sohbetler, Değişiklikler, Arşivler ve Ayarlar |
| Standart | Ayrıca Case Board, Hesaplar ve Erişim |
| Uzman | Ayrıca Kaynaklar, Ekstralar, Arşive Sor, Parametreler, Hesap, Sistem günlüğü ve Entegrasyonlar |

Basit çağrılar: Buradan Başla, Günlük ve Dışa Aktarım **Ana Sayfası**, **Değişiklikler** ve **Arşivler**. Bir seviye yalnızca bölümleri gizler. Gizlenen bir özellik çalışmaya devam eder ve sunucu her izni kendi başına kontrol eder. Seviye, dil, tema ve saat dilimi, operatör ve çalışma alanı bazında kaydedilir; [ayarlara](https://phishdestroy.github.io/TgWitness/tr/docs/reference/settings/) bakınız.

Üst çubukta ayrıca şunlar bulunur:

- **Bir bölüme git** (Ctrl+K veya Mac'te ⌘K): bir sohbeti, bir parametreyi veya bir günlük kaydını `#number`. Ok tuşlarıyla hareket edin, Enter tuşuyla açın, Esc tuşuyla kapatın.
- **Bildirimler**: günlükten tespit edilen sorunlar ve sohbet değişiklikleri. " **Tümünü okundu olarak işaretle**" seçeneği sayacı sıfırlar ve "**Bildirim kuralları" seçeneği** kuralları açar. Telegram, Discord veya e-postaya gönderim, [Ekstra Özellikler → Bildirimler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#notifications) bölümünden ayarlanır.
- Bu çalışma alanının bağlantı göstergesi. Üst çubuğun altındaki **Collector durumu** bunu Telegram bağlantısı, olay alımı, kaynaklar ve ek kuyruğu olarak ayırır.
- **Kilit**: Bu tarayıcıdaki paneli kapatır. Koleksiyon, sunucuda çalışmaya devam eder.
- Sürüm numarasının yanındaki koruma modu; bkz. [koruma modları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#protection-modes).

Demo çalışma alanı kurgusal mesajlar içerir ve hiçbir zaman Telegram’a bağlanmaz. Gerçek bir çalışma alanını değiştirecek eylemler burada reddedilir.

## Buradan başlayın

Bir görev seçin. **"Hesabımı Dışa Aktar" seçeneği,** hesabın şu anda okuyabileceği içerikleri indirir. "**Bir araştırmayı takip et" seçeneği**, seçtiğiniz sohbetlerden gelen yeni mesajları, gözlemlenen düzenlemeleri ve silme bildirimlerini kaydeder. Kurulum kartında üç adım gösterilir: hesabı bağla, kaynakları seç, gözlemi başlat. Hedef sorusu, siz cevap verene veya atlayana kadar bu sayfada kalır. Bunun yerine yeni bir çalışma alanı [ilk kurulum](https://phishdestroy.github.io/TgWitness/tr/docs/reference/settings/) ekranını açar.

## Sohbetler

Kaydedilen sohbetler, varsayılan olarak salt okunurdur.

- Listeyi ada veya kimliğe göre arayın. **Seçme işlemi,** izlenen sohbetleri ekler veya kaldırır. **"Telegram bağlantısını aç**" seçeneği, bir kullanıcı adı veya davet bağlantısı alır ve önizlemeyi günlüğe kaydeder. **"Katıl / aç ve izle**" seçeneği, sohbete katılır ve onu kaynaklarınıza ekler; botu açmak ise onu gönderir `/start`.
- Sohbet başlığı, **silindi, metin korundu**, **kaydedilmeden önce silindi** ve **yeniden kontrol edildiğinde bulunamadı** mesajlarını sayar. Sohbet listesi ve bildirimler de aynı tanımları kullanır. Silinen bir mesaj kırmızı renktedir ve kaydedilmiş metnini korur; düzenlenmiş bir mesaj ise kaydedilmiş tüm sürümlerini korur. Her silme işlemi bilinen bilgileri gösterir: ne zaman görüntülendiği, Telegram'ın mesajı kimin sildiğini bildirmediği veya sadece bildirim ulaştığı gibi.
- **Yükleme geçmişi,** son 100, 250 veya 500 mesajı bu görünüme ve günlüğe getirir. Etkinleştirilmiş tüm kaynakları yüklemek için [Kaynaklar → Tam geçmiş seçeneğini](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#sources) kullanın.
- **Sohbeti dışa aktar seçeneği,** görünür geçmişin tamamını imzalı bir dosya olarak indirir `chat.json` ve `chat.html`. Birkaç bağlı hesap bu işi paylaşabilir: her biri kendi mesaj numarası aralığını indirir ve kendi kısmını imzalar; dışa aktarmayı başlatan hesap ise arşivi imzalar. Bkz. [tek bir sohbeti dışa aktarma](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md).
- **"Kişiler"** listesi, bu sohbette kaydedilmiş mesajları olan herkesi gösterir. Kişi profilleri, üçüncü şahıslara ait kişisel veriler olduğu için varsayılan olarak kapalıdır. Bir sohbet için açık olduklarında, profilde isim ve kullanıcı adı geçmişi, Telegram işaretleri, avatar hash'leri, etkinlik, kimin kime yanıt verdiği, gözlemlenen diğer sohbetler ve bahsedilen cüzdanlar, telefonlar, kullanıcı adları ve bağlantılar gösterilir. Her bilgi, ilgili kayda yönlendirir. **Profilleri dışa aktarma işlemi**, isteğe bağlı olarak şifreli ZIP bir dosyayı kaydeder; profilleri kapatmak ise profil dosyasını siler. [Kişi profillerine](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#people-profiles) bakın.
- **"Profili Kaydet" seçeneği artık** sohbetin veya bot profilinin bir anlık görüntüsünü kaydeder: açıklama, üyeler, davet bağlantısı, bot komutları.

### Salt okunur, gönderme ve gizli bilgiler

Mesajların üstündeki iki anahtar, hesabı ve okuyucuyu korur:

- Bir sohbet açıldığında "**Salt Okunur"** modu etkindir. Mesaj göndermek veya bot düğmelerine basmak için bu özelliği kapatın. Her eylemde **“@hesap olarak gönder?**” veya **“Bu bot düğmesine @hesap olarak bas?**” sorusu görüntülenir; bu, sohbet üyelerinin bunu göreceğini ve eylemin imzalı günlüğe kaydedileceğini belirtir. **“Bu sohbette 10 dakika boyunca tekrar sorma” seçeneği,** sorunun bir süre atlanmasını sağlar. Panelde ve API’da **“Vaka Kanıtı”**hedefi için gönderme özelliği kapalıdır.
- **Gizli bilgileri maskeleme**, şifre, oturum açma kodu, API anahtarı veya hash, bot jetonu, oturum dizesi, özel anahtar, JWT veya ödeme kartı numarası gibi görünen bilgileri gizler (kart numaraları Luhn toplamı ile kontrol edilir). **Göster seçeneği** bir değeri ortaya çıkarır; bu işlem günlüğe kaydedilir. Bu tarayıcı için maskeleme özelliğinin kapatılması da kaydedilir. Yalnızca görüntüleneni değişir: orijinal kayıtlar ve tüm dışa aktarımlar tam metni korur.

## Günlük

Çalışma alanının imzaladığı tüm kayıtlar, en yenisi önce olmak üzere.

- **Genel Bakış**, gözlemlenen mesajları, kaydedilen düzenlemeleri, silme bildirimlerini ve seçilen kaynakları sayar.
- **Olay zaman çizelgesi**, olay türüne (tümü, düzenlemeler, silme işlemleri, tepkiler, üyelik, kapsama), metne ve kaynağa göre filtreleme yapar. **Önceki etkinlikleri yükle**, bir önceki sayfaya geri dönülmesini sağlar.
- Bir kaydı açarak ayrıntılarını, hash değerini ve yükünü görebilirsiniz. **Bu kayda giden bağlantı**, aynı kaydı açan bir adrestir. Olası gizli bilgiler bu önizlemede maskelenmiştir; dışa aktarımlarda orijinal hali korunur.
- Günlük yalnızca ekleme amaçlıdır: paneldeki hiçbir öğe bir kaydı düzenlemez veya silmez. Bunu **Dışa Aktar → Günlüğü Doğrula** seçeneğiyle kontrol edin veya `python -m tgwitness.verify`; [dışa aktarma ve doğrulama bölümüne](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) bakın.

## Kaynaklar

Bu çalışma alanı hangi sohbetleri kaydeder ve bunlardan neleri saklar? Değişiklikler gelecekteki etkinlikler için geçerlidir; kaydedilmiş kayıtlar kalır.

**Sohbet listesini yenile** seçeneği, hesabın sohbetlerini ve klasörlerini okur. Mesajları indirmez.

### Kapsam

- **Bu hesapta neler kaydedilir?** : **Seçilen sohbetler** (sadece eklediğiniz sohbetler), **Telegram klasörü** (hesabın klasörlerinden biri; daha sonra bu klasöre eklenen sohbetler dahil) veya **Hesabın tamamı** (her sohbet ve ortaya çıktıkça her yeni sohbet, grup, özel sohbet veya bot). **Soruşturma modu** , özel bir hesap içindir: hesabın gördüğü her şeyi, kendi mesajlarını ve düğme basışlarını kaydeder ve her yeni sohbetin profilini ve daha önce görünen mesajları anında kaydeder. [özel hesap kılavuzu](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) ana hesabınızı neden asla kullanmamanız gerektiğini açıklar.
- **Kaynak türleri**, klasör ve tüm hesap modlarını kanallar, gruplar, özel sohbetler ve botlarla sınırlar. **Kendi eylemleri**, hesabın kendi mesajlarını, düzenlemelerini ve yanıt klavyesi tuş vuruşlarını ekler.
- **Yeni bir sohbet veya bot ortaya çıktığında**: profilini ve seçilen sayıya kadar en son görünür mesajlarını kaydedin.

Limits: the published cloud collector does not receive Secret Chats. The separate [Pseudo-secret interface and its demo](https://phishdestroy.github.io/TgWitness/tr/docs/reference/secret-chats/) are documented with their development status and outstanding defects. Nothing is recorded while TgWitness is not running; after a restart it catches up only what Telegram still returns, and the report shows the gap. Chats beyond the chat list limit (1,000 dialogs unless changed in Parameters) are added when they next become active. Inline bot buttons pressed in another app are invisible; the bot's reply is recorded.

### Kapsamdaki sohbetler

Duruma (**Etkin**, **Duraklatılmış**, **Öncelikli**, **Hariç Tutulan**, **Onaylanmamış erişim**, **Yoksayılan**) ve türe göre filtreleyin, ardından seçiminize göre işlem yapın: etkinleştirin, duraklatın, öncelik işareti koyun veya kaldırın, kapsamdan hariç tutun veya kaldırın. Durum rozeti yalnızca durumu gösterir; eylemler her satırın menüsünde yer alır ve ne işe yaradıkları bir satırla belirtilir. Duraklatma ve hariç tutma işlemleri için onay istenir; bu işlemler toplu olarak da yapılabilir. Bir kaynağın kaldırılması için kaynağın adı istenir ve ilgili kişilerin profilleri silinir; kaynağa ait kaydedilmiş kayıtlar günlüğünde kalır.

Hesabın sohbet listesinde görünmeyen bir kaynak **güncelleme** alıyor**; sohbet listesinde** yer almıyor ancak kayıtlar gelmeye devam ediyor; aksi takdirde **erişim onaylanmamıştır**. **"Mevcut sohbetler", "Seçilenleri Ekle"** veya "**Eşleşenlerin Tümünü Ekle"** seçenekleriyle sohbetleri ekler.

### Tam geçmiş

Etkinleştirilmiş her kaynağın mevcut geçmişini Sohbetler ve günlüğe yükler. İlerleme durumu yeniden başlatma sonrasında korunur; ekler, medya ayarlarınıza göre düzenlenir. [Kaynak geçmişine](https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/) bakın.

### Kayıt

- **Hangi değişikliklerin korunacağını seçin**: yeni mesajlar, düzenlemeler, silme bildirimleri, görünür tepkiler, gruba katılma ve gruptan ayrılma. Bir ön ayar, formu değiştirir; **Kayıt ayarlarını kaydet seçeneği ise** bunu uygular. Bir kategoriyi yeniden etkinleştirmek, kaçırılan olayları geri getirmez.
- **Mümkün olduğunda medyayı koruyun**: dosya başına belirli bir boyuta kadar ekleri indirin, tür başına 1 ila 2.000 MiB arasında ayarlayın ve video uzunluğunu saniye cinsinden sınırlayın (0, sınır yok anlamına gelir). Her indirme denemesinin sonucu kaydedilir.
- **Yeniden Kontrol**: öncelikli sohbetler birkaç dakikada bir, diğer sohbetler nadiren kontrol edilir, böylece hesap Telegram’ın FloodWait sınırlarından uzak kalır. 0 değeri bir grubu devre dışı bırakır. Öncelikli sohbetleri listede yıldız işaretiyle işaretleyin; her turda kontrol edilecek sohbet sayısı ve sohbetler arasındaki duraklama süresi Parametreler bölümünde bulunur. [Koleksiyona](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/) bakın.

## Dışa aktarma

**İndirmeler,** dosyaları hazırlar; **Derleme raporu,** raporların görünümünü belirler.

| Ne | Şu amaçlarla kullanın: | Kılavuz |
| --- | --- | --- |
| Hesap dışa aktarma | Hesabın şu anda okuyabildiği içeriklerin güncel bir anlık görüntüsü | [Hesap dışa aktarma](https://phishdestroy.github.io/TgWitness/tr/docs/reference/account-export/) |
| Kopyalama paylaşımı | Tamamlanmış bir hesap dışa aktarımının küçültülmüş bir türevi | [Açıklama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| İmzalı ZIP | Sabit bir günlük sınırı içinde günlük, rapor, ekler ve doğrulama araçları | [Dışa aktar ve doğrula](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) |
| HTML, PDF, JSON raporu | Mühürlenmiş, okunabilir bir rapor | [Vaka raporları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/) |
| JSONL, CSV | İmzalı orijinal kayıtlar; formül güvenliği sağlanmış bir elektronik tablo | [Dışa aktar ve doğrula](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) |
| Devir teslim özeti | Yalnızca alıcının ihtiyaç duyduğu sohbetler, dönemler ve kişiler | [Kanıtlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#investigation-handoff) |
| Sohbet dışa aktarma | İmzalanmış bir sohbet `chat.json` ve `chat.html` | [Bir sohbeti dışa aktar](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Yukarıdaki indirmeleri bir şifre ile şifreleyin** (12 karakter veya daha fazla) bir AES-256 ZIP dosyası kaydeder; bu dosya 7-Zip veya WinRAR ile açılabilir. İçindeki imzalı dosya değiştirilmemiştir. Şifre saklanmaz.
- **Hazırlanan dışa aktarımlar**, 2 GiB sınırında en fazla 20 dosyayı ve en son dosyayı, tekrar indirmeler için saklar; her birinde SHA-256 bulunur. Bir dosyanın hazırlanması, teslim edildiğini kanıtlamaz.
- Tarayıcı kaydetme iletişim kutusunu reddederse, panel normal bir indirmeye geçer.
- **İmzalama kimliğiniz,** anahtar parmak izini gösterir. **Kontrol noktası kaydet** ve **İmzalı çalıştırma makbuzu** indir seçenekleri, toplayıcı dışında saklayabileceğiniz kayıtlar sağlar. **Zaman damgası isteği** hazırla seçeneği, herhangi bir servise başvurmadan bir RFC 3161 isteği oluşturur.

## Ayarlar, hesaplar ve bağlantı

- **Ayarlar**: hedef, bağlantı, neyin kaydedileceği ve arayüz. [İlk kurulum ve ayarlara](https://phishdestroy.github.io/TgWitness/tr/docs/reference/settings/) bakın.
- **Hesaplar**: Her çalışma alanı, durumu, kaynakları, olayları ve ek kuyruğuyla birlikte. **"Dikkat gerektiren**", "**Toplanma aşamasında**", "**Çevrimdışı veya duraklatılmış**" veya **"Bağlantı yok**" seçeneklerine göre filtreleyin, bir seçimi duraklatın veya devam ettirin, hesap dosyalarını toplu olarak içe aktarın ve grupları yönetin. [Hesaplara](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) bakın.
- **Hesap**: oturum açma ve bu hesabın bağlantı yolu. Doğrudan, bir WireGuard profili, kendi proxy'niz, genel MTProto havuzu veya WARP; bir yol hazırlayıp kontrol edin, ardından bunu bu hesaba, bir gruba veya tüm hesaplara uygulayın. Bkz. [bağlantı ve proxy'ler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/)[.](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md)

## Ekstra Özellikler

İsteğe bağlı: Toplamaya başlamak için bir hesap ve kaynaklar yeterlidir. Yalnızca seçtiğiniz seçenek ayarlarını açar; hiçbir şey otomatik olarak bağlanmaz. Üst kısımdaki **Koruma Seviyesi** kartı, [koruma modunu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#protection-modes) gösterir.

| Kart | Neler ekliyor? | Kılavuz |
| --- | --- | --- |
| Depolama ve disk alanı | Yedeklemeler, eski dosyaları bulutunuza taşıma, silinemeyen bir kanıt kopyası | [Depolama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/storage/) |
| Hedef ve koruma seviyesi | Hedefiniz ve iki ölçek için önerilen ayarlar | [aşağıda](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#goal-and-protection-level) |
| Bildirimler | Sorunlar, değiştirilen mesajlar ve günlük özet; size özel kontrol botu | [aşağıda](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#notifications) |
| Kanıtlar ve yedeklemeler | Zaman damgaları, daha fazla tanık ve şifrelenmiş bir dış kopya | [aşağıda](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#evidence-and-backups) |
| Sunucu 7/24 | SSH'siz bir bulut sunucusu; panelden oluşturulur ve silinir | [Yüksek güvenilirlik](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#from-the-panel) |
| Bağımsız tanık | Telegram kanalınıza veya Discord'a gönderilen imzalı kontroller | [Witness](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/) |
| Kod denetimi | Çalışan programı, GitHub’daki herkese açık bir commit ile karşılaştırır | [aşağıda](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#code-check) |

### Amaç ve koruma seviyesi

Dört soru:

1. **Ne için kullanılır?** Kişisel bir kayıt, bir soruşturma veya bir vaka için delil.
2. **Ne kadarını izleyeceksiniz?** Birkaç sohbet (en fazla yaklaşık 50), çok sayıda sohbet (en fazla yaklaşık 500) veya tüm hesaplar. Bu, sohbet listesi sınırını 1.000, 3.000 veya 20.000 olarak belirler.
3. **Fotoğraflar ve dosyalar mı?** Yalnızca metin, fotoğraflar ve kısa medya dosyaları (fotoğraflar 20 MB, videolar 100 MB) veya her şey (her biri 1 GB'a kadar olan videolar ve belgeler). Tüm hesapları içeren "her şey" seçeneği ayrıca 4 GiB disk alanı boş bırakır.
4. **Nerede çalışacak?** Bu bilgisayarda veya sürekli açık olan bir sunucuda.

Öneri listesi, bağımsız zaman damgalarını, drand'ı ve Telegram'ın cihaz listesini içerir; her birinin ne eklediğine dair bir satır bulunur. Zaman damgaları, kişisel bir kayıt, soruşturma veya delil için her 60, 30 veya 10 dakikada bir başlar; drand ve cihaz listesi için zaman damgaları gereklidir. Yalnızca bunları, ek politikasını ve yukarıdaki iki parametreyi **uygulayın**. Her değişiklik bir günlük kaydıdır, ayrıca `setup.applied`. Bildirimler, site dışı bir kopya, bir sunucu, Ağ Geçidi DNS’si, kod kontrolü ve bir tanık, kendi formlarıyla birlikte sonraki adımlar olarak sunulur.

İki ölçek, hedeften değil, yapılan ayarlardan hesaplanır:

| Ölçek | Önemli Noktalar |
| --- | --- |
| Güvenilirlik | İmzalı günlük 1, zaman damgaları 3, drand 1, cihaz listesi 1, eşleşen kod kontrolü 1, tanık oylama 1, onaylanmış sunucu 2, Ağ Geçidi DNS günlüğü 1 |
| Güvenilirlik | Her zaman açık sunucu 3, tesis dışı yedek 3, Object Lock 1, sorun bildirimleri 1 |

%80 veya daha fazlası **maksimum**, %50 **yüksek**, %25 **orta**, bunun altındakiler ise **temel** olarak okunur. Güvenilirlik, şu anda herhangi bir sunucu kontrol edilmeden önce, 4. sorunun yanıtındaki her zaman açık bir sunucuyu dikkate alır.

### Bildirimler

Bildirimler, Apprise aracılığıyla Telegram, Discord, Slack, ntfy, e-posta, Matrix ve 100'den fazla başka hizmete gönderilir. Bir hizmet seçin, bir veya iki alanı doldurun ve bir test gönderin ya da Apprise adreslerini doğrudan yapıştırın.

- **Sorunlar**: disk neredeyse dolu, hesaptan çıkış yapıldı, koleksiyon, kopyalama veya zaman damgası hataları. Kapalı bir sunucuda, açık bir SSH bağlantı noktası veya oturum açma da bir sorundur.
- **Değişiklikler**: gözlemlenen sohbetlerdeki silinmiş, düzenlenmiş ve eksik mesajlar, her kontrol için tek bir bildirimde gruplandırılır (Parametreler'de değiştirilmedikçe her dakika).
- **Tamamlanan görevler**: geçmiş, dışa aktarmalar ve yedek kopyalar.
- Seçilen saatte, sunucu saatine göre **günlük özet**.

Bildirimlerde sohbet adları ve sayıları yer alır. Mesaj alıntıları varsayılan olarak kapalıdır; açık olduğunda mesaj metni bu cihazdan dışarı aktarılır.

**Operatör botunuz**, @BotFather'dan aldığınız ve şu sorulara yanıt veren `/status` ve `/stats`ve isteğe bağlı olarak `/pause`, `/resume` ve `/copy`komutlarına yanıt veren, @BotFather'dan aldığınız kendi botunuzdur. Yalnızca listelenen sohbetler ve Telegram kullanıcı kimlikleri bu botu kullanabilir; sohbet metni çalışma alanında kalır. Komutlarını zaten başka bir uygulama alıyorsa ayrı bir bot kullanın. [Bildirimler](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) ve [operatör botu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/storage/#operator-bot-and-completion-notices) bölümlerine bakın.

### Kanıtlar ve yedeklemeler

- **Bağımsız zaman damgaları**, her 5 ila 1.440 dakikada bir, imzalanmış her kontrol noktasının yalnızca SHA-256'sini RFC 3161 yetkililerine ve OpenTimestamps takvimlerine gönderir. **Anchor şu anda** bir geçiş gerçekleştiriyor. [Zaman damgalarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/) bakın.
- Seçilene kadar devre dışı kalan **diğer tanıklar**: en yeni drand turu, Telegram’ın IP adresleri olmayan oturum açılmış cihaz listesi ve Cloudflare Gateway’in sunucunun DNS sorgularına ait günlüğü. [İsteğe bağlı kayıtlara](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices) bakın.
- **Şifreli yedekleme**, günlüğü, dosyaları, kontrol noktalarını ve sohbet dışa aktarımlarını S3 uyumlu depolama alanlarına (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO) kopyalar. Her şey önce bu makinede şifrelenir. **Şifreleme anahtarını indirin** ve ayrı bir yerde saklayın: anahtar olmadan kopya okunamaz. Yönetişim veya Uyumluluk modundaki Nesne Kilidi, nesnelerin belirli bir süre boyunca silinmesini engeller. [Tesis dışı kopyaya](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md) bakın.

### Kod denetimi

Yüklü programın yayınlanmış bir sürümle eşleşip eşleşmediğini kontrol eder.

1. Bir GitHub deposu (resmi olanı zaten girilmiştir) ve bir etiket, dal veya commit girin.
2. **Check now**, bu çalışma alanının dış istekler için kullandığı yol üzerinden GitHub'ın API'sine, söz konusu commit'in dosya listesini sorar. Ölçülen her program dosyasının git blob kimliğini commit ile karşılaştırır. Satır sonları dönüştürülmüş bir Windows checkout'u da yine eşleşir.
3. Sonuç, değiştirilen, fazladan eklenen ve eksik dosyaları (her birinden en fazla 50 tane) listeler ve bir `source.checked` günlük kaydı olarak kaydedilir.

Sonuç, çalışan program dosyaları değişmediği sürece geçerli sayılır: güncellemeden sonra tekrar kontrol edin. Jeton gerekmez ve yalnızca genel depolar çalışır; sohbetler ve kimlik bilgileri yüklenmez. Bir eşleşme, diskteki kodu tanımlar. Bu, donanım doğrulaması değildir; bunun için [Phala Cloud'](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)a bakın.

## Koruma modları

Sürüm numarasının yanındaki anahtar, seçilen modu ve 18 koruma katmanından kaç tanesinin etkin olduğunu gösterir; örneğin `🟠 Witnessed 9/18`. **Modu değiştirmek** için **Ekstra → Koruma seviyesi** seçeneğine tıklayın. Bir mod, bir hedefi tanımlar ve hala eksik olanları listeler; kayıt, imzalama ve kaydedilmiş ayarlar her modda aynıdır.

| Mod | İçin | Eklenenler |
| --- | --- | --- |
| 🟢 Kolay | Bir sohbeti izleme ve bir kopyasını saklama | Sohbetler, günlük ve sohbet dışa aktarımları; imzalama işlemi arka planda çalışır |
| 🟡 İmzalı | Bir platforma, bir barındırıcıya veya bir kötüye kullanım bildirim birimine rapor verir | İmzalı arşiv, günlük kontrolü, kontrol noktaları, devir teslim özeti |
| 🟠 Tanıklandı | Birinin kaydın değiştirildiğini iddia edebileceği durumlar | İmzalı günlük başlıklarını yayınlayan bağımsız bir tanık |
| 🔴 Mahkemeye hazır | Avukat, polis veya mahkeme için delil | Zaman damgaları, şifrelenmiş ve sunucu dışında tutulan bir kopya, raporlardaki vaka ayrıntıları |
| 🟣 GitHub tarafından doğrulanmıştır | Herkesin yazılımını kontrol edebilmesi gereken kayıtlar | Kod denetimi ve GitHub Actions yakalama |
| ⚫ Mossad | Cömert kaynaklara sahip bir rakibe karşı yüksek riskli davalar | 7/24 çalışan güvenli bir sunucu, gizli bir IP adresi, 18 katmanın tamamı |

Katmanlar: imzalanmış ve zincirlenmiş her kayıt; imzalanmış çalıştırma makbuzu; SHA-256 ile kaydedilen ekler; imzalanmış kontrol noktaları; yeniden kontroller; sorun uyarıları; salt okunur tanık erişimi; programlı olarak kontrol yapan bir tanık; RFC 3161 zaman damgaları; OpenTimestamps kanıtları; doğrulanmış en son zaman damgası; şifrelenmiş, tesis dışı bir kopya; raporlardaki vaka detayları; eşleşen kod kontrolü; Telegram bu makinenin IP adresini asla görmez; proxy aracılığıyla gelen dış istekler; kopyada Nesne Kilidi; sağlayıcı kayıtlarının bulunduğu mühürlü bir sunucu. Kapalı olan bir katmanda, formunu açan **Kurulum seçeneği** bulunur. Daha düşük bir mod seçildiğinde onay istenir ve hiçbir şey silinmez.

## Diğer araçlar

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Arşive danışın**: kaydedilmiş gözlemleri arayın, kaynakları inceleyin, ardından bunları bir AI modeline gönderip göndermemeye karar verin. [Arşiv analizi](https://phishdestroy.github.io/TgWitness/tr/docs/reference/analysis/) ile [yerel OCR ve transkripsiyona](https://phishdestroy.github.io/TgWitness/tr/docs/reference/media-analysis/) bakın.
- **Parametreler**: toplama sınırları ve hızı, yeniden kontroller, indirmeler, profiller, bildirimler ve dışa aktarmalar. Adına göre arama yapın, **“Yalnızca değişen** değerleri göster” seçeneğini kullanın ve “Varsayılanları **geri yükle…”** seçeneğiyle varsayılan ayarları taslak olarak hazırlayın. **“Parametreleri kaydet” seçeneği**, değerleri bir sonraki kullanımdan itibaren uygular ve her değişiklik bir günlük kaydı olarak kaydedilir.
- **Erişim**: gözden geçirenler, analistler ve operatörler için ayrı erişim belirteçleri; seçilen çalışma alanları, sohbetler ve haklarla sınırlıdır. [Erişim bölümüne](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) bakınız.
- **Sistem günlüğü** : Bu işlemin başladığından beri gerçekleştirdiği eylemler (bağlantılar, proxy değişiklikleri, oturum açma işlemleri, reddedilmeler, ayar değişiklikleri) IP adresleri gizlenmiş olarak gösterilir. **"Yeni satırları takip et** " seçeneği, en yeni satırı ekranda tutar. Mesajlar yalnızca günlüğünde kalır.
- **Entegrasyonlar**: AI sağlayıcısı, [salt okunur MCP](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/) bağlantıları ve [imzalı webhook'lar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/webhooks/).
- **Case Board**: kanıtların yanında yer alan özel ekip notları, yer imleri ve kesitler. Bkz. [Case Board](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-board/).
- Dışa Aktarımlar'da **GitHub Actions capture**: fork'unuzdan yakalanan bir sohbet. Bkz. [mühürlü yakalama](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
