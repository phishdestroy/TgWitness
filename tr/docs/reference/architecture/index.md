# Mimari

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/architecture/

Toplayıcı, panel, günlük, işleyiciler ve tanık bileşenleri ile verilerin bunlar arasında nasıl aktarıldığı.

Tek bir Python işlemi, FastAPI panelini ve her biri bir Telethon kullanıcı hesabı istemcisine sahip, istediğiniz sayıda izole çalışma alanını barındırır. SQLite, yalnızca ekleme yapılabilen imzalı bir olay günlüğü ve değiştirilebilir operasyonel ayarları tutar. Şifrelenmiş bir kasa, API kimlik bilgilerini, StringSession'ı ve imzalama anahtarını barındırır. Ön uç, basit bir şekilde paketlenmiş HTML/CSS/JavaScript'ten oluşur: Node derlemesi, CDN'ler veya çalışma zamanı ön uç indirmelerine gerek yoktur.

| Modül | Sorumluluk |
| --- | --- |
| collector.py | Yetkilendirme, diyalog seçimi, güncellemeler, anlık görüntüler, medya kuyruğu, bağlantı izleme |
| interactions.py / telegram_client.py | Açıkça belirtilen panel eylemleri, imzalı makbuzlar, kalıcı istek kimlikleri ve görev bazlı geri arama/katılım yeniden deneme politikası |
| message_content.py | Aktarım erişim meta verileri hariç tutulmuş, gözlemlenebilir mesaj karşılaştırması |
| workers.py | İptal temizliği işleminden önce dosya dışa aktarma işlemlerinin tamamlanmasını bekleyin |
| store.py | WAL işlemleri, sıralı olay zinciri, sorgu filtreleri, operasyonel ayarlar |
| security.py | Özel dosya oluşturma, şifreli depo, Ed25519 imzalaması, tek işlem kilidi |
| evidence.py | Tam günlük dışa aktarma, türevler, kontrol noktaları, ek doğrulama |
| verify.py | Bağımsız, salt okunur doğrulayıcı (stdlib + kriptografi): arşivler, kapsama alanı, tanık günlükleri ve kanal gönderileri, profil dosyaları |
| app.py | Kimliği doğrulanmış API, yaşam döngüsü, istek doğrulama, statik panel |
| profiles.py | Çoklu hesap toplayıcılar, paylaşımlı erişim denetleyicisi, çalışma alanı başına yaşam döngüsü |
| access.py | Kapsamlı izinler, izin kontrolleri, IP kısıtlamaları, oturum sınırları ve yönetici konsolu |
| proxy_catalog.py | Halka açık akış anlık görüntüleri, aktarım kontrolleri, paylaşılan proxy havuzu ve durum tabanlı seçim |
| provenance.py | İmzalı, edinim-çalıştırma kimlik, kod ve bağımlılık ölçümleri |
| network.py | Çalışma alanı başına doğrulanmış rotalar; sansürlenmiş durum ve kanıtlar; Telethon aktarım seçenekleri |
| sessions.py | İncelenmiş Telethon SQLite şemalarının çevrimdışı, salt okunur biçime dönüştürülmesi |
| account_import.py | Desteklenen hesap dosyaları ve JSON'ların bellek içi algılanması ve normalleştirilmesi |
| tdata.py | Sınırlı modern TData ZIP okuyucu, sağlama toplamı/şifre çözme doğrulaması, dosya çıkarma yok |
| doctor.py | Veri toplama, oturum açma veya paket yükleme gerektirmeyen yerel hazırlık kontrolleri |
| download.py | Doğrulanmış akışlı dışa aktarma indirme özelliği; sınırlı okuma sayısı ve üzerine yazma yapılmaması |
| monitoring.py | İş alanı başına doğrulanmış olay politikası ve tür bazında ek kuralları; işleyiciler tarafından paylaşılan durum bilgileri ve imzalı makbuzlar |
| scope.py | Gözlem kapsamı (seçilen sohbetler, Telegram klasörü, tüm hesap), kaynak türleri, hariç tutulanlar, yeniden kontrol aşamaları |
| dossier.py | Kaydedilen kayıtlardan oluşturulan sohbet başına kullanıcı profilleri: kayıt referansları içeren bilgiler, avatar SHA-256/pHash, bahsetme ayıklama |
| witness_api.py | Salt okunur tanık belirteçleri ve bunların alabileceği imzalı günlük başlığı |
| witness.py | Bağımsız tanık süreci: kendi anahtarı ve günlüğü, başlık kontrolleri, imzalı kanal gönderileri, dışa aktarma |
| alerts.py | Apprise bildirimleri ve panelin bildirim listesi |
| logging_config.py | Penceresiz başlatmalar için konsol günlüğü ve dönen sunucu tanılama |
| static/ | Duyarlı arayüz, yerel erişim kapısı, filtreler, ayrıntılar, dışa aktarma, hesap kurulumu |
| demo.py | Gerçek veri toplama işleminden ayrılmış, açıkça "sentetik kayıt defteri" olarak etiketlenmiş |

Gözlem işleyicileri, bağlanmadan önce kaydedilir. Canlı toplama, aktif istemci kimliği, açık çalışma durumu, etkinleştirilmiş kaynaklar veya gözlem kapsamı (klasör veya tüm hesap modları, ilk güncellemede yeni bir sohbeti kaynak olarak ekler) ve olay politikası ile sınırlandırılır. Reddedilen ve geçersiz kılınan istemciler canlı güncellemelere katkıda bulunamaz. Ham tepkiler ve üyelik güncellemeleri görünürlük sınırlarını korur. Gelen mesaj içeriği ve kalıcı medya işi birlikte kaydedilir. İşler, orijinal TL tanımlayıcısını korur ve hash değerini imzalı mesaj gözlemine bağlar. Gönderen/düzenleyen/silici anlamları birbirinden ayrılır.

Her çalışma alanı bir hesap kabul eder ve kendi dizini ile imzalama kimliğine sahiptir. Ana çalışma alanı, uyumluluk amacıyla kök dizinde kalır; ek çalışma alanları ise profiles/<id>/ dizininde bulunur. Tek bir taşıyıcı jeton tüm kurulumu kontrol eder; çalışma alanları ayrı yetkilendirme kiracıları değildir. İşlem kilitleri dizinleri korur; veritabanı kilitleri olay ekleme işlemlerini sıralar. Her ekleme işlemi, FULL senkron modunda SQLite WAL’a senkron olarak kaydedilir. Olay güncelleme/silme tetikleyicileri, sıradan uygulama düzenlemelerini engeller; dosya sistemi yöneticileri güven sınırları içinde kalır.

API yetkilendirmesi, taşıyıcı jeton şeklindedir. Oturum açma işlemleri serileştirilir ve zaman sınırlıdır. Hesap yüklemeleri, 12 MiB'lik özel kodlanmış gövde sınırı ve 8 MiB'lik kod çözülmüş dosya sınırı kullanır; normal API istekleri ise 16 KiB sınırını korur. Dönüştürme işlemi bir işçi iş parçacığında çalışır, yüklemeleri bellekte tutar ve normalleştirilmiş girdiyi kimliği doğrulanmış tarayıcıya döndürür. QR girişinde çalışma alanı başına bir aday, kısa ömürlü bir tanımlayıcı, bekleme görevi ve açık iptal bulunur. Yalnızca kabul edilen yetkilendirme aktif istemci olur. Telegram FloodWait, bir Retry-After değeri ile döndürülür; kimlik bilgileri ve ham RPC hata mesajları API hatalarında gösterilmez. Dışa aktarmalar, asenkron olay döngüsünün dışında çalışır ve çalışma alanı başına serileştirilir. Kararlı bir okuma anlık görüntüsünü aktarırlar ve devam eden WAL yazma işlemleriyle birlikte çalışabilirler. Çalışma alanı toplayıcıları, işlem/olay döngüsünü paylaşır.

Güncel geçmiş anlık görüntüleri ve canlı güncellemeler birbiriyle çakışabilir. Her ikisi de kaynağa göre etiketlenmiş ayrı gözlemlerdir; çift girişler sessizce gizlenmez. Eksik kimlik numaralarından, uydurulmuş silinmiş metinlerden, zorla üye numaralandırmasından veya otomatik grup katılımından herhangi bir çıkarım yapılmaz.

Kullanıcıya yönelik açıklamalar için, [veri toplama sürecinin nasıl işlediğine](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/) ve [hesaplar ile oturum formatlarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) göz atın.

Ağ yapılandırması şifreli kasada bulunur. Bir rota uygulandığında eski istemciler kapatılır ve tamamlanmamış oturum açma işlemleri iptal edilir; sonraki bağlantılar, doğrudan yedekleme olmaksızın bu rotayı kullanır. Yeni bir harici anahtar kurulumunda, her çalışma alanının Fernet anahtarı, bir ana anahtar dosyasından ve depolanmış rastgele bir tuzdan HKDF-SHA256 kullanılarak türetilir. Bu, gizli bilgileri veri dizininden ayrı olarak korur; günlük/medya içeriklerinin düz metin halini korumaz.

Yerel demo girişi, ayrı olarak oluşturulan bir işlem yeteneği kullanır; asla yapılandırılmış panel jetonunu kullanmaz. İhraç ve kabul işlemleri için açık demo modu, ek çalışma alanları veya yetkilendirilmiş oturum içermeyen sentetik bir kök , loopback eş/ana bilgisayar, proxy yönlendirme başlıkları olmaması ve kaynaklar arası tarayıcı isteği olmaması gerekir. Canlı API’ler taşıyıcı kimlik doğrulamasını korur ve demo modunda toplama değişikliklerini reddeder.
