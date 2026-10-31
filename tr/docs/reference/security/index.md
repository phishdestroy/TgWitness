# Güvenlik ve veri işleme

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/

Tehdit modeli, erişim modeli, depolanan gizli bilgiler, ağ maruziyeti, oturum içe aktarmaları ve bir güvenlik açığının nasıl bildirileceği.

TgWitness, kendi bilgisayarınızda veya sunucunuzda çalışır. Hesap bağlantıları, genel proxy listesinin bakımı ve isteğe bağlı harici hizmetler için açık yönlendirme ilkeleri vardır. Bildirimler, zaman damgaları, site dışı kopyalar ve tanık ayrı ayrı yapılandırılır. Bu sayfada, nelerin nasıl korunduğu ve nelerin operatöre bırakıldığı listelenmiştir.

| Alan | Kısacası |
| --- | --- |
| Erişim | Yönetici anahtarı ve hesaplara/sohbetlere kapsamlı erişim, yedi izin düzeyi ve iptal edilebilir oturumlar; varsayılan olarak localhost |
| Depolanan gizli bilgiler | Oturum, API çifti, imzalama anahtarı ve proxy ayarları Fernet ile şifrelenmiştir. |
| Mesajlar ve medya | Şifrelenmemiş olarak saklanır: disk şifreleme ve sıkı izin ayarları kullanın |
| Bütünlük | Her kayıtta SHA-256 hash zinciri ve Ed25519 imzası bulunur |
| Kapsam dışı | Bir makine yöneticisi, sızdırılmış bir panel jetonu, yakalama işleminin eksiksizliği |

Güvenlik açıkları bildirimleri için [güvenlik](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)politikasına bakınız.

## Erişim modeli

Ana panel jetonu tam kontrol sağlar. Diğer kullanıcılar kendi [kapsamlı erişim](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) haklarını alabilirler: seçilen çalışma alanları ve sohbetler, izinler, geçerlilik süresi, IP kısıtlamaları, oturum açma sınırları ve iptal edilebilir oturumlar. Sohbetle sınırlı erişim hakları olan kullanıcılar, izinleri işaretli olsa bile tüm çalışma alanı işlemlerini gerçekleştiremezler. Çalışma alanları aynı süreci paylaşır ve verileri ana bilgisayar yöneticisinden izole etmez.

Panel, varsayılan olarak localhost'ta dinleme yapar. Tarayıcı üzerinden oturum açıldığında, bir erişim jetonu oturum kimlik bilgileriyle değiştirilir; tarayıcı bunu taşıyıcı jeton olarak gönderir. Bu jeton, kimlik doğrulama çerezi yerine sessionStorage'da saklanır. Kilitleme/oturum kapatma işlemi, tarayıcı oturumunu temizler. Tarayıcının kapatılması veya oturumun sonlandırılması, veri toplama işlemini durdurmaz.

Verilen tokenlar ve oturum kimlik bilgileri, şifrelenmiş kasada hash olarak saklanır. İptal işlemi, ilgili oturumları sonlandırır; izin değişiklikleri ise sonraki istekleri etkiler. İndirilen dosyalar geri alınamaz. Yönetici, kendi tarayıcı oturumlarını da sınırlayabilir, ancak ana panel tokenını kullanan komut dosyaları doğrudan tam erişim hakkını korur ve bu tarayıcı oturumu sınırlamalarını atlar.

Başarısız kimlik doğrulama işlemleri, istemci adresine göre hız sınırlamasına tabidir. IP kısıtlamaları, uygulama tarafından görülen adresi kullanır; buna güvenmeden önce ters proxy davranışını kontrol edin. Witness kimlik bilgileri, ayrı, salt okunur kontrol noktası/durum kimlik bilgileri olarak kalır.

### Demo erişimi

`/api/demo-access`, açıkça başlatılmış, izole edilmiş sentetik bir demo için kasıtlı olarak kimlik doğrulaması yapılmamış bir önyükleme aracıdır. Ayrı bir işlem ömrü yeteneği sağlar, asla gerçek panel jetonu veya bir TGWITNESS_TOKEN geçersiz kılma işlemi yapmaz. Bu yetkinin verilmesi ve kullanılması için bir loopback eş ve Host gereklidir; başlıkların iletilmesi ve kaynaklar arası istekler kabul edilmez. Ek çalışma alanları veya yetkili bir oturum bu yolu devre dışı bırakır. Canlı çalışma alanları bu yetkiyi asla vermez. Demo, hesapları birbirine bağlayamaz veya toplama ayarlarını değiştiremez.

## Panel içeriği ve dışa aktarımlar

Panel, harici yazı tipleri, analiz araçları, CDN kaynakları veya gömülü uzaktan medya kullanmaz. Telegram kaynaklı metinler HTML olarak değil, metin olarak eklenir. İndirilen ekler ikili ekler olarak sunulur. JSONL dışa aktarımları orijinal dizeleri korur; HTML ise bunları kaçırır; formüle dönüşebilecek CSV hücrelerinin başına apostrof eklenir.

Dışa aktarımlar, kimlik doğrulama ve imzalama gizli bilgilerini içermez, ancak kasıtlı olarak toplanan kaynak meta verilerini, tanımlayıcıları ve muhtemelen kişisel veya hassas içeriği içerir. Telegram erişim hash'leri ve dosya referansları, ham kaynak meta verilerinde yer alabilir.

## Depolanan gizli bilgiler

Telegram API kimlik bilgileri, StringSession ve Ed25519 özel anahtarı, Fernet kullanılarak şifrelenir. Varsayılan olarak anahtarı, aynı korumalı veri dizininde saklanır. Bu, düz metnin kazara ifşa edilme riskini azaltır; ancak dizinin tamamını okuyabilen bir saldırgana karşı koruma sağlamaz. Mesaj içeriği ve medya dosyaları TgWitness tarafından **şifrelenmez** . Disk şifreleme ve kısıtlayıcı işletim sistemi izinleri kullanın. Unix özel anahtar dosyaları 0600 modunda oluşturulur; yeni oluşturulan veri dizinleri ise 0700 modunu kullanır. Mevcut dizin izinleri değiştirilmez. Windows, dizin ACL’lerini devralır: bunları hizmet hesabı ve yetkili yöneticilerle sınırlandırın.

### Harici ana anahtar

Yeni bir veri dizini için, TGWITNESS_VAULT_KEY_FILE harici bir rastgele ana anahtar sağlayabilir. HKDF-SHA256 ve ayrı bir rastgele tuz, her çalışma alanı için farklı bir Fernet anahtarı üretir. Kurtarma amacıyla vault.external.json dosyası saklanmalıdır. Eksik veya yanlış anahtarlar, işlemin başarısızlıkla sonuçlanmasına neden olur. Mevcut yerel kasalar sessizce taşınmaz. Çalışan işlem anahtara erişebilir; bu, HSM izolasyonu değildir. Panel, seçilen modu bildirir ve mesaj/medya depolamasının uygulama tarafından şifrelenmediğini açıkça belirtir. Tam tehdit modeli için [bağlantı, proxy'ler ve veri koruma](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/) bölümlerine bakın.

## Proxy'ler ve ağ yolları

Proxy yapılandırması kasada şifrelenir. Şifreler ve MTProxy gizli bilgileri API tarafından döndürülmez veya kanıt kayıtlarına yazılmaz. Her çalışma alanı kendi Telegram rotasını ve bir [IP modunu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes) seçer.

IP Gizleme modu, Telegram'ın doğrudan yedekleme modunu reddeder ve harici HTTP istekleri için bir proxy gerektirir. Açıkça seçilen yedekleme modu, gecikmeden sonra Telegram'a doğrudan erişime izin verir; tünel/VPN modu ise doğrudan yollara izin verir. Tünel modunun seçilmesi, bir VPN kurmaz veya doğrulamaz. Bu ayarlar, tüm sistem trafiğini, tarayıcıları, paket yöneticilerini veya yerel proxy sunucusunun DNS çözümlemesini kontrol etmez.

MTProxy yalnızca Telegram trafiğini taşır. Harici istekler için ayrı bir SOCKS5/HTTP proxy'si, çalışma alanının SOCKS5/HTTP rotası veya izin verilen bir doğrudan rota kullanılabilir; ayrıca devre dışı bırakılabilirler. Bağımsız tanık, kendi aktarım ayarlarına sahiptir. Sıradan SOCKS5/HTTP CONNECT kimlik doğrulaması, bu proxy protokollerinin kendisi tarafından şifrelenmez. Sahte TLS MTProxy gizli anahtarları hâlâ desteklenmemektedir.

## Giriş ve oturum içe aktarma işlemleri

Dönüştürülmüş .tgwitness-session dosyaları, kasaya yüklenip depolanana kadar düz metin biçiminde bir yetkilendirme şifresi içerir. Çevrimdışı CLI, gözden geçirilmiş Telethon şemalarını kabul eder. Panel içe aktarma özelliği ayrıca Pyrogram SQLite, modern tek hesaplı TData ZIP ve belgelenmiş JSON girdilerini kabul eder. Kimlik doğrulaması yapılır, dört dosya / 8 MiB ile sınırlıdır ve arşiv açma veya orijinal dosyaları kaydetme işlemine gerek kalmadan yüklemeleri bellekte işler. Normalleştirilmiş kimlik bilgileri yalnızca isteği yapan ve kimliği doğrulanmış tarayıcıya döndürülür; Telegram yetkilendirmesi başarıyla tamamlandıktan sonra şifreli kasada saklanır. Orijinalleri ve dönüştürülmüş dosyaları koruyun ve eşzamanlı istemcilerin yetkilendirmeyi kopyalamasını önleyin.

Veri işleme, konteyner sağlama toplamlarını, yerel şifre çözme hash'lerini ve yapı uzunluklarını doğrular. Sağlanan masaüstü yerel şifresi geçici olarak kullanılır ve saklanmaz. Bu sınırlı ayrıştırıcı, her masaüstü sürümünün uyumlu olduğunu garanti etmez. QR görüntüleri yerel olarak oluşturulur, kısa ömürlü Telegram oturum açma belirteçleri içerir ve asla harici bir görüntüleme hizmetine gönderilmez. Kilitleme, çalışma alanı değiştirme, yeni oturum açma ve rota değişiklikleri, bekleyen QR denemelerini iptal eder. Bir sekmeyi yeniden yüklemek/kapatmak, denemeyi süresi dolana kadar beklemede bırakabilir. Başarılı bir QR oturum açma işlemi yine de hesap bağlanmasını zorunlu kılar. Sıradan API gövdeleri 16 KiB ile sınırlı kalır; kimlik doğrulamalı içe aktarma yolu, en fazla 12 MiB kodlanmış JSON kabul eder ve daha küçük kod çözülmüş dosya sınırını ayrı olarak uygular.

Giriş kodları ve Telegram iki aşamalı doğrulama şifreleri kalıcı olarak saklanmaz. Telefon numarası/kod hash durumu, yetkilendirme sırasında bellekte tutulur. Telegram oturumları hesap erişimi sağlar; hiçbir zaman bir veri dizini, oturum, token, kasa anahtarı veya özel imzalama anahtarını GitHub'a yüklemeyin.

## Günlükler ve aktarım

Varsayılan API doğrulama yanıtı, kimlik bilgilerini yansıtmayacak şekilde değiştirilmiştir. Uygulama erişim günlüğü devre dışı bırakılmıştır. Yetkilendirme başlıklarını veya istek gövdelerini günlüğe kaydetmek için ters proxy yapılandırmayın. HTTP, jetonları ve oturum açma şifrelerini düz metin olarak taşır: localhost'tan ayrılırken her zaman HTTPS veya bir SSH tüneli kullanın.

## Bütünlük sınırları

Hash zinciri, veritabanı tetikleyicileri ve imzalar belirli değişiklikleri algılar; ancak bunlar, yerel bir yöneticinin günlüğü yeniden yazmasını ve yeniden imzalamasını engellemez. İmzalı kontrol noktalarını ve açık anahtar parmak izini ayrı bir sistemde saklayın. Kanıt modu ve site dışı kopya (her ikisi de varsayılan olarak kapalıdır), kontrol noktası hash'lerini zaman damgası hizmetlerine ve şifrelenmiş kopyaları S3 uyumlu depolama alanına gönderir; [kanıt](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)formatına bakınız. Şeffaflık günlükleri, HSM destekli imzalama ve resmi zincir-i-mülkiyet sertifikasyonu uygulanmamaktadır.

## Bir sorun olduğundan şüpheleniyorsanız

Orijinal veri dizinini koruyun ve analiz için ayrı bir kopya kullanın. Telegram'a ait özel verileri veya kimlik bilgilerini halka açık bir soruna dahil etmeyin. Bağımsız bir güvenlik sertifikası iddia edilmemektedir.
