# Bağlantı, proxy'ler ve veri koruma

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/

Kimlik doğrulama, otomatik proxy havuzları, IP modları, yedekleme politikası, harici istekler ve gizli depolama.

Bu belge, TgWitness 0.7.1 sürümünün davranışını ve sınırlarını açıklamaktadır. Kimlik doğrulama, kaynağa erişim, ağ bağlantısı ve yakalama eksiksizliği ayrı durumlardır. Oturum açma adımları, dosya biçimleri ve birden fazla hesap hakkında bilgi için [hesaplar ve oturum biçimleri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) bölümünden başlayın. Olay ilkeleri ve yeniden başlatma davranışı hakkında bilgi için [toplama işleminin nasıl çalıştığına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/) bakın.

## Kimlik doğrulama yöntemleri

**API Kimliği ve API hash'i bir uygulamayı tanımlar; hesap girişinin yerini almazlar.** TgWitness'te bunlar isteğe bağlıdır. Öncelik sırası: forma girilen bir çift, ardından içe aktarılan hesap JSON'undan bir çift, sonra çalışma alanında kaydedilen çift ve son olarak da Telegram'ın birini reddetmesi durumunda otomatik rotasyonla rastgele sırayla denen genel çift havuzundan gelenler denir; Telegram bir çifti reddettiğinde otomatik rotasyonla rastgele sırayla denenir. Yalnızca Telegram Desktop çifti (2040), eşleşen Telegram Desktop istemci açıklamasıyla birlikte gönderilir. [my.telegram.org](https://my.telegram.org) adresindeki API Geliştirme Araçları'ndan aldığınız kendi çiftiniz tüm hesaplarınızla kullanılabilir; her hesabın yine de kendi yetkilendirme bilgisi vardır.

| Yöntem | Gereksinimler | TgWitness desteği |
| --- | --- | --- |
| Telefon, kod, isteğe bağlı 2FA | Hesap erişimi; API çifti isteğe bağlı | Panel girişi |
| Oturum Açma Anahtarı HEX + DC Kimliği | Tam 512 karakterlik anahtar ve DC 1–5 | Doğrudan **Otorizasyon anahtarı** sekmesi; yetkilendirme kaydedilmeden önce isteğe bağlı Kullanıcı Kimliği kontrol edilir |
| Telethon StringSession | Geçerli bir oturum dizesi | Panel girişi |
| Telethon SQLite `.session` | Kapalı, tutarlı metin | Şemaların doğrudan panelden içe aktarılması 7/8; isteğe bağlı çevrimdışı CLI |
| Pyrogram SQLite `.session` | Kapalı üretim kullanıcı oturumu | Şemaların doğrudan panelden içe aktarılması 2/3 |
| Telegram Masaüstü TData ZIP | Tek bir modern hesap; koruma varsa yerel şifre | Sağlama toplamı/şifre çözme kontrolleriyle bellek içi dönüştürme |
| Hesap JSON'u | Desteklenen API/oturum/anahtar alanları | Meta veriler tek başına API kimlik bilgilerini doldurur; yine de bir oturum/anahtar veya telefon/QR koduyla oturum açma gereklidir |
| QR ile giriş | Yetkili bir Telegram uygulamasından onay | Yerel QR kodu oluşturma, süre dolumu/yeniden deneme, isteğe bağlı 2FA |
| TDLib / Pyrogram StringSession | Diğer kütüphaneye özgü formatlar | Desteklenmiyor |
| Bot jetonu | Kendi erişim/güncelleme modeline sahip bir bot | Bu veri toplayıcı tarafından kullanılmamaktadır |

Telegram, kod teslimatını tercih eder; SMS'in ulaşması garanti edilmez. Bir API hash'i, iptal edilmiş bir oturumu düzeltemez veya unutulan 2FA şifresinin yerine geçemez. TgWitness, giriş kodlarını veya Telegram 2FA şifresini diske kaydetmez.

Özel bir kaynak için, hesabın halihazırda erişim iznine sahip olması gerekir. Grup kullanıcı adı gerekmez. Proxy veya oturum içe aktarımı, ne üyelik ne de yönetici hakları sağlar. Mevcut üyelik, katılma öncesine ait geçmişe erişimi garanti etmez.

## Bir Telethon oturum dosyasını içe aktarın

Telethon SQLite, Pyrogram SQLite ve Telegram Desktop TData farklı formatlar kullanır. Panel, desteklenen yapıları algılar ve dönüştürür; dosya adını değiştirmek dönüştürme işlemi değildir. **Dosyalar** altından bir oturum ve ona ait JSON dosyasını seçin, ardından **Hesabı bağla düğmesine** basın. En fazla dört eşleşen dosya ve toplam 8 MiB kabul edilir. TData/JSON ayrıntıları için [biçim sınırlarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) bakın. Şifre kurtarma özelliği yoktur. Telefon/2FA veya QR ile giriş, ayrı bir yetkilendirme oluşturur.

İsteğe bağlı, yalnızca Telethon için geçerli olan komut satırı yolu hâlâ kullanılabilir durumdadır:

1. Müşterinin orijinal oturumu kullanmasını durdurun ve tutarlı bir kopya oluşturun. Dönüştürücü, tamamlanmamış WAL/günlüğü olan dosyaları reddeder. Kontrolü atlatmak için bu dosyaları silmek yerine, orijinal müşteriyi düzgün bir şekilde kapatın.
2. TgWitness ortamından şu komutu çalıştırın:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. **Hesap ekle → Dosyalar** bölümünden sonucu yükleyin veya dizesini yapıştırın ve devam edin.
2. Ekranda görüntülenen sayısal hesap kimliğini kontrol edin, kaynakları seçin ve gözlemi başlatın.

Dönüştürücü, SQLite'ı salt okunur olarak açar, şema yükseltmesi veya ağ isteği gerçekleştirmez ve oturumu yazdırmaz. Şema sürümünü, tablo türlerini, tek bir oturum satırını, IP/bağlantı noktası/veri merkezi ve anahtar uzunluğunu kontrol eder. CLI girişi 64 MiB ile sınırlıdır; StringSession metni 4 KiB ile sınırlıdır. Panel dönüştürme, dosyaları kimliği doğrulanmış TgWitness sunucusuna yükler, bunları bellekte işler ve yüklenen orijinalleri kaydetmeden normalleştirilmiş kimlik bilgilerini o tarayıcıya geri gönderir. Uzak sunucu için HTTPS kullanın.

**Dönüştürülen dosya, şifrelenmemiş bir hesap erişim şifresidir.** Bunu güvenli bir depolama alanında saklayın ve asla bir üçüncü taraf dönüştürme hizmetine aktarmayın veya göndermeyin. TgWitness, yetkilendirilmiş oturumu şifreli kasasında saklar. Bir oturumu kopyalamak, ayrı bir yetkilendirme oluşturmaz: klonlanmış yetkilendirme anahtarlarıyla eşzamanlı istemciler çalıştırmayın ve bağımsız güncelleme teslimi olduğunu varsaymayın.

Dönüştürme işlemi, orijinal mesajları, varlık önbelleğini veya kalıcı bir güncelleme imlecini değil, yetkilendirmeyi aktarır. İşlem yeniden başlatmaları arasında güncelleme kurtarmasını düzeltmez.

## MTProto, Telethon ve proxy'ler

MTProto, Telegram'ın protokolüdür. Telethon, TgWitness'in kullandığı Python istemci kütüphanesidir. MTProxy, bir Telegram aktarım proxy'sidir; SOCKS5 ve HTTP CONNECT genel tüneller sağlar. Hiçbiri hesap kimlik doğrulamasının yerini almaz.

Giriş yapmadan önce **Hesap → Ayarlar → Bağlantı ayarları → Bağlantı yolunu değiştir** seçeneğinden her bir çalışma alanı için yolu kaydedin. Yeni çalışma alanları varsayılan olarak **Otomatik MTProxy ·** IP Gizleme özelliğine sahip **genel listeler** olarak ayarlanır. Doğrudan (Direct) seçeneğini açıkça kullanan mevcut çalışma alanları, bunu izin veren modu korur.

## IP modları

Yol, bağlantıyı seçer. IP modu, sunucunun adresinin ne zaman ifşa olabileceğini belirler. Bu denetimler bir VPN kurmaz veya tüm makine trafiğini yönlendirmez.

| Mod | Telegram | Dış talepler |
| --- | --- | --- |
| Hide IP (`hide`) | Bir proxy kullanın; hiçbiri çalışmazsa bekleyin. Doğrudan yedek çözüm yoktur. | SOCKS5/HTTP gerektirir; uygun bir proxy içermeyen istekleri reddeder. |
| Yedek seçeneğe izin ver (`fallback`) | Otomatik MTProxy, yapılandırılan gecikme süresinin ardından Direct'i kullanabilir, ardından çalışan bir proxy'ye geri dönebilir. | Önceden yapılandırılmış bir harici proxy veya hesabın SOCKS5/HTTP yolunu tercih edin; aksi takdirde Direct kullanımına izin verilir. |
| Tünel / VPN (`tunnel`) | Doğrudan yollar ve anında otomatik havuz yedeklemesi izin verilir. | Uygulanabilir bir proxy yapılandırılmamışsa doğrudan erişim izin verilir. |

Tünel/VPN modu, söz konusu ağı ayrı olarak yönettiğinizi varsayar. Çalışır durumda bir tünel olmadan, hedefler sunucunun kendi adresini görebilir. Modu, seçeneğin adına göre değil, gerçek ağınıza göre seçin.

### Bir yol seçin

| Yol | Ayarlar | Sınır |
| --- | --- | --- |
| Otomatik MTProxy | Yerleşik listeler veya bir operatör kataloğu | Çalışır durumda bir Telegram rotası sağlar; doğrudan yedekleme, IP moduna bağlıdır |
| Doğrudan | Tünel/VPN modu | Telethon, sunucunun ağ yolunu kullanır |
| SOCKS5 | Sunucu, bağlantı noktası, isteğe bağlı kullanıcı adı/şifre | python-socks, uzaktaki hedef DNS etkinleştirildi |
| HTTP CONNECT | Sunucu, bağlantı noktası, isteğe bağlı kullanıcı adı/şifre | Düz HTTP CONNECT; proxy sunucusuna yönelik TLS desteği uygulanmamıştır |
| MTProxy | Sunucu, bağlantı noktası, gizli anahtar | Deneysel Telethon aktarım biçimi; 32 onaltılık basamak veya `dd` + 32 onaltılık basamak |

Sahte TLS `ee` gizli anahtarları reddedilir. Telethon 1.45'in normalleştirme işlevi, önek ve etki alanını kaldırabilir, ancak bu, Sahte TLS'yi uygulamaz. `tg://proxy?server=…&port=…&secret=…` veya `https://t.me/proxy?server=…&port=…&secret=…`'yi yapıştırın ve "**Bağlantıdan alanları doldur"** seçeneğini seçin. Bu işlem, bağlantı kurmadan veya kaydetmeden alanları doğrular ve doldurur; yolu ayrı olarak inceleyin ve kaydedin. Manuel alanlar kullanılabilir durumda kalır. [Telegram proxy bağlantılarına](https://core.telegram.org/api/links#proxy-links) bakın.

### Kurulumunuz tarafından sağlanan genel proxy'ler

Yerleşik liste dört kaynağı birleştirir: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) ve [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Paket içindeki anlık görüntü, uç nokta bilgileri, kaynak atıfları ve indirme tarihlerini içerir. Bir sağlayıcının listede yer alması, proxy'nin çalıştığının veya her Telegram güncellemesini ilettiğinin kanıtı değildir.

**Otomatik MTProxy**, Telegram aktarım bağlantısını kontrol eder, çalışan bir proxy'yi korur ve arıza durumunda başka bir proxy'ye geçer. Yeterli sayıda çalışan giriş mevcut olduğunda çalışma alanları farklı proxy'leri tercih eder; benzersiz bir çıkış adresi garanti edilmez. Başarısız olan proxy'ler bir sonraki denemeye kadar beklemeye alınır. Hiçbiri çalışmazsa, IP modu, toplama işleminin beklemesi mi yoksa doğrudan bağlantı kullanması mı gerektiğini belirler. Proxy'lerin değiştirilmesi, hesabı değiştirmez veya günlüğünü silmez. Rota seçimleri ve değişiklikler, imzalı günlüğe kaydedilir.

Otomatik rotalar etkinken, listeler saat başı yenilenir ve aktarım kontrolleri varsayılan olarak her on dakikada bir çalıştırılır. Bu aralıklar yapılandırılabilir. **Genel listeleri güncellemek** bir yenileme gerektirir; listeyi yalnızca görüntülemek, kaydedilmiş bir manuel rotayı değiştirmez.

Her besleme yanıtı 1 MiB ile sınırlıdır; istek zaman aşımı sekiz saniye ve toplam indirme süresi 20 saniyedir; yönlendirmeler reddedilir. Kaynak başına en fazla 64 uyumlu giriş saklanır ve tekilleştirilir. Ayrıştırıcı, desteklenen onaltılık ve base64url gizli anahtarlarını ve JSON beslemesini kabul eder. Sahte TLS `ee`'leri, geçersiz bağlantılar, özel/ayrılmış IP sabitleri ve yerel ana bilgisayar adları atlanır. Ana bilgisayar adları kullanılmadan önce çözümlenir ve kontrol edilir; seçilen IP, o bağlantı için sabitlenir. Otomatik yeniden edinme işlemi, ana bilgisayar adını tekrar çözümler; yeniden çözümlemek için manuel bir girişi tekrar uygulayın.

Başarısız, boş veya uyumsuz besleme yanıtlarında önceki kaynak anlık görüntüsü korunur. Güncellemeler atomiktir, serileştirilmiştir ve çalışma alanı başına dakikada bir denemeyle sınırlıdır. Başarılı bir aktarım denemesi, anonimlik veya yakalama tamlığını değil, bağlantı kurulduğunu gösterir.

**Telegram trafiği ve HTTPS istekleri farklı yollar kullanır.** Liste indirmeleri, ayrı bir HTTPS bağlantısı ve sağlanan harici istek yolunu kullanır. `TGWITNESS_PROXY_FEED_PROXY`, bu yolu bir HTTP/SOCKS5 proxy ile açıkça geçersiz kılar; her iki Compose toplayıcı varyantı da bunu iletir. Arka plan havuzu, ana çalışma alanını takip eder. Feed sağlayıcılara hiçbir Telegram oturumu, API kimlik bilgileri, panel jetonu veya bot jetonu gönderilmez. Sağlayıcı adları, anlık görüntü tarihleri ve indirme yolu, **“Listenin kaynağı”** bölümünde görünür.

Bir MTProxy yalnızca Telegram trafiğini taşır. Zaman damgaları, bildirimler, site dışı kopyalar ve kaynak kontrolleri gibi çalışma alanı HTTP işlemleri, yapılandırıldığında ayrı bir SOCKS5/HTTP proxy'si kullanır, ardından hesabın SOCKS5/HTTP yolunu kullanır. Her ikisi de yoksa, Hide IP isteği reddeder; diğer modlar Doğrudan erişime izin verir. Dış istekler devre dışı bırakılabilir. Açıkça yapılandırılmış bir besleme indirme proxy’si, ayrı bir operatör geçersiz kılma seçeneği olarak kalır. Bağımsız tanık hizmeti kendi rotasını korur.

****Otomatik havuz parametreleri**** **Parametreler → Otomatik MTProxy** altında, hata eşiğini, bekleme süresini, planlı rotasyonu, proxy paylaşımını ve izin verilen yedekleme gecikmesini yapılandırın. | Kontrol | Varsayılan | | --- | --- | | Değiştirilmeden önce bağlantı kesme | 10 dakika içinde 3 kez | | Bağlantı denemesi başına denenecek proxy sayısı | 3 | | Hata sonrası ilk / maksimum bekleme süresi | 10 dakika / 6 saat | | Planlı rotasyon | Devre dışı; arıza durumunda etkinleştir | | Proxy başına hesap sayısı | 0: ayrı girişleri tercih edin, gerektiğinde paylaşın. Özel bir girişi beklemek için 1'i ayarlayın. | | İzin verilen Direct yedeklemesinden önceki gecikme | 10 dakika; Hide IP hala Direct'i reddediyor | | Besleme yenileme / aktarım kontrolleri | 60 / 10 dakika; ana çalışma alanı değerleri paylaşılan havuz için geçerlidir | Farklı proxy'ler, farklı çıkış adreslerini garanti etmez. Bu ayarlar, Telegram sınırlarını geçersiz kılmaz veya anonimliği garanti etmez.

Genel listeyi kendi operatör kataloğunuzla değiştirmek için aşağıdaki geçersiz kılma ayarını yapılandırın. Bu ayar, `proxies` dizisi boş olduğunda da dahil olmak üzere harici abonelikleri tamamen devre dışı bırakır.

[Boş kataloğu](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example)`proxy-config/proxies.json` adresine kopyalayın ve devreye alınmış genel uç noktalarınızı ekleyin:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Örnek değerler değiştirilmelidir. En fazla 32 farklı giriş kabul edilir. Kimlik doğrulaması yapılmış liste, paylaşılan gizli anahtarlar olmadan etiketleri/ana bilgisayarları/bağlantı noktalarını döndürür; bir tanesi seçildiğinde kimlik bilgileri çalışma alanı kasasına kaydedilir. Açık bir aktarım testi yapılana kadar kullanılabilirlik test edilmemiştir. Hatalı biçimlendirilmiş bir katalog, manuel yapılandırmaya olanak tanır.

Yerel başlatma: `TGWITNESS_PROXY_CATALOG` değerini yerel JSON yoluna ayarlayın. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

Overlay, `proxy-config` dizinini salt okunur olarak bağlar; dosyalar, 10001 numaralı konteyner UID'si tarafından okunabilir olmalıdır. Bu dizin, Git, Docker derleme bağlamı ve kaynak arşivlerinden hariç tutulur. Bu katalog, veri toplama hesaplarını yapılandırır; [tanık botu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/), MTProxy yerine kendi HTTP/SOCKS5 yolunu kullanır.

Doğrudan yedekleme, yukarıdaki IP moduna tabidir. Rotayı değiştirmeden önce gözlemi duraklatın. Kaydetme işlemi eski istemcilerin bağlantısını keser ve tamamlanmamış oturum açma işlemlerini iptal eder; yeni istemci kaydedilen rotayı kullanır. Hesabın günlük/oturum bağı korunur. Ayarlar önceki rotanın yerini alır: düzenlerken proxy kimlik bilgilerini yeniden girin.

Kimlik bilgileri `network.enc` ile şifrelenir. API, kullanıcı adını, şifreyi veya gizli anahtarı döndürmez. İmzalı kayıtlar, uç noktayı ve gizli anahtarları hariç tutarak, yol türünü ve kimlik bilgilerinin mevcut olup olmadığını içerir. Operatör, uç noktayı panelden görebilir. Gizli alanlar, çalışma alanları kaydedildikten, kilitlendikten veya değiştirildikten sonra silinir.

**Telegram bağlantısını test etme özelliği**, oturum açmadan önce de kullanılabilir; bu özellik, rota üzerinden geçici ve yetkisiz bir Telegram bağlantısı açar ve kapatır. IP kontrolü yapan bir web sitesiyle iletişim kurmaz. Başarılı sonuç, grup erişimi, tam teslimat veya anonimlik değil, yalnızca aktarım bağlantısının kurulduğunu gösterir.

Proxy, Telegram DC medya indirmeleri de dahil olmak üzere Telegram istemcisinin bağlantılarına uygulanır. Tarayıcı, pip, SSH ve manuel olarak çalıştırılan TSA araçları için ayrı rotalar mevcuttur. Proxy ana bilgisayar adı yerel olarak çözümlenebilir. `rdns`, hedef ana bilgisayar adlarını etkiler; Telegram genellikle sayısal DC IP'leri sağlar.

SOCKS5 ve düz HTTP CONNECT, proxy kimlik bilgilerini veya istemci-proxy tünelini kendileri şifrelemez. MTProto, Telegram trafiğini ayrı olarak korur. Güvenilmeyen bir ağda proxy'ye uygun bir güvenli kanal kullanın. Özel gruplar bulut sohbetleridir; MTProto bunları uçtan uca şifrelenmiş Gizli Sohbetlere dönüştürmez.

## Şifreleme ve imzalar

| Katman | Uygulandı | Operatörün sorumluluğu |
| --- | --- | --- |
| Telegram trafiği | Telethon MTProto | Platform güveni, erişim yolu ve kullanılabilirlik |
| Web paneli | Taşıyıcı jetonu, varsayılan geri döngü, istek sınırları | Uzaktan erişim için HTTPS veya SSH tüneli |
| Sırlar | API kimlik bilgileri, oturum, proxy kimlik bilgileri ve özel anahtar imzalaması için Fernet | Şifre çözme anahtarını ve çalışan sunucuyu koruyun |
| Kasa anahtarı | Yeni bir kurulum için yerel anahtar veya harici ana anahtar | Ayrı korumalı depolama alanı ve anahtar yedekleme |
| Mesajlar ve ekler | Düz metin uygulama depolama | Şifrelenmiş disk/birim |
| ZIP/JSONL/CSV/HTML | Bütünlük kontrolleri, içerik şifreleme yok | Dışa aktarılan kopyaları ve aktarımları koruyun |
| Kaynak ve zaman | İmzalı günlük, işlem makbuzu, RFC 3161 araçları | Güvenilir anahtar, bağımsız kontrol noktaları/TSA ve saklama prosedürü |

Hesap bölümündeki **depolama koruması** bu durumları gösterir. Panel jetonu bir erişim gizli anahtarıdır, şifreleme parolası değildir. Yönetici erişimi sağlar; [düzenlenen jetonların](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) kapsamı hesaplar ve sohbetlerle sınırlandırılabilir. Çalışma alanları ana süreci paylaşır ve izole edilmiş kiracılar değildir.

Açıkça başlatılmış, izole edilmiş sentetik bir demo, doğrudan bir loopback bağlantısı üzerinden otomatik olarak açılabilir. Bu, ayrı bir işlem ömrü özelliğini kullanır; ne yapılandırılmış panel jetonunu açığa çıkarır ne de gerçek çalışma alanlarına erişim izni verir. Uzak, proxy üzerinden veya kaynaklar arası istekler bu otomatik giriş özelliğini elde edemez/kullanamaz. Bu kolaylık, gerçek hesap verileri için kimlik doğrulama sınırını ortadan kaldırmaz.

BitLocker, LUKS, FileVault veya yönetilen şifreli bir birim, kendi tehdit modelleri kapsamında depolama alanını koruyabilir. Kilidi açılmış ve çalışır durumdaki bir makinenin yöneticisi yine de verileri okuyabilir. Depolama planlamasına SQLite WAL/SHM, medya, geçici dışa aktarımlar, takas alanı, yedeklemeler ve tarayıcı indirmelerini dahil edin. Bir Docker birimi, sırf birim olduğu için şifrelenmez. TgWitness, SQLCipher veya nesne şifrelemesini uygulamaz.

## Harici ana anahtar

**Yeni** bir kurulum için, ana anahtarı veri dizininin dışına yerleştirin. Bu işlem, mevcut bir yerel anahtar kasasını otomatik olarak taşırmaz. Yalnızca hizmet kimliğinin erişebileceği bir anahtar dizini hazırlayın, ardından şunu çalıştırın:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, kurulu proje ortamını kullanarak:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

Docker'da, dosyayı `/data` dışında, örneğin `/run/secrets/tgwitness-master.key` konumunda salt okunur olarak bağlayın ve ortam değişkenini bu yola ayarlayın. Hizmet UID'sinin dosyayı okuyabilmesi gerekir. Anahtar baytlarını değil, yolu ortam/yapılandırma dosyaları aracılığıyla aktarın.

Her çalışma alanı, rastgele bir genel tuz değeri ve HKDF-SHA256 aracılığıyla türetilen kendine ait bir Fernet anahtarı alır. `vault.external.json`, ana anahtarı değil, türetme meta verilerini depolar. Anahtarın eksik veya yanlış olması durumunda, sistem sessizce anahtarı değiştirmeden başlatma işlemi başarısız olur. Kurtarma amacıyla hem tuz meta verilerini hem de ana anahtarı saklayın.

Tüm çalışma alanları aynı ana anahtardan türetilir; bu anahtarın güvenliğinin ihlali tüm kurulumu etkiler. Çalışan işlem, gizli bilgileri şifresini çözebilir. Bu bir HSM veya parola KDF değildir. Rastgele bir anahtarın yerine keyfi insan parolaları kabul edilmez.

Kasıtlı bir geçiş gerçekleştirilip doğrulanana kadar mevcut kurulumlar için mevcut anahtarı kullanmaya devam edin. `vault.key`'yi silmek veya ana anahtarı değiştirmek, oturumlara/imza anahtarlarına erişimi engelleyebilir. Şifrelenmiş yedekleri ve anahtarları ayrı tutun ve kurtarma işlemini izole bir ortamda test edin.

## Kaynaklar ve doğrulama kapsamı

26 Ekim 2026 tarihinde gözden geçirilmiştir:

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0: SQLiteSession, StringSession, `Connection._proxy_connect`, `TcpMTProxy.normalize_secret` ve indirme yöntemleri.

Yerel testler, loopback SOCKS5/HTTP CONNECT test senaryolarını, sentetik SQLite oturumlarını, yol izolasyonunu, gizli bilgilerin hariç tutulmasını ve eksik anahtar reddetmesini kapsar. Bu testler, gerçek Telegram/proxy birlikte çalışabilirliğini veya canlı MTProxy davranışını doğrulamaz. [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) ve [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) dosyalarına bakınız.
