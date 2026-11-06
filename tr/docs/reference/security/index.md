# Güvenlik ve veri işleme

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/

Tehdit modeli, erişim modeli, depolanan gizli bilgiler, ağ maruziyeti, oturum içe aktarmaları ve bir güvenlik açığının nasıl bildirileceği.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| Alan | Kısacası |
| --- | --- |
| Erişim | Yönetici anahtarı ve hesaplara/sohbetlere kapsamlı erişim, yedi izin düzeyi ve iptal edilebilir oturumlar; varsayılan olarak localhost |
| Depolanan gizli bilgiler | Oturum, API çifti, imzalama anahtarı ve proxy ayarları Fernet ile şifrelenmiştir. |
| Mesajlar ve medya | Şifrelenmemiş olarak saklanır: disk şifreleme ve sıkı izin ayarları kullanın |
| Bütünlük | Her kayıtta SHA-256 hash zinciri ve Ed25519 imzası bulunur |
| Yerel güven sınırı | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

Güvenlik açıkları bildirimleri için [güvenlik](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)politikasına bakınız.

**On this page**

- [Access model](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/#access-model)
- [Panel content and exports](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/#panel-content-and-exports)
- [Secrets at rest](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/#secrets-at-rest)
- [Proxies and network routes](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/#proxies-and-network-routes)
- [Sign-in and session imports](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/#sign-in-and-session-imports)
- [Logs and transport](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/#logs-and-transport)
- [Integrity limits](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/#integrity-limits)
- [If you suspect a problem](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/#if-you-suspect-a-problem)

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

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### Harici ana anahtar

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/) for setup details.

## Proxy'ler ve ağ yolları

Proxy yapılandırması kasada şifrelenir. Şifreler ve MTProxy gizli bilgileri API tarafından döndürülmez veya kanıt kayıtlarına yazılmaz. Her çalışma alanı kendi Telegram rotasını ve bir [IP modunu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes) seçer.

**Adresi gizle seçeneği,** doğrudan Telegram yedeklemeyi engeller ve harici HTTP istekleri için bir proxy gerektirir. Açıkça seçilen yedekleme modu, gecikmeden sonra doğrudan Telegram erişimine izin verir; tünel/VPN modu ise doğrudan yollara izin verir. Tünel modunun seçilmesi, bir VPN'in kurulmasını veya doğrulanmasını gerektirmez. Bu ayarlar, tüm makine trafiğini, tarayıcıları, paket yöneticilerini veya yerel proxy sunucusunun DNS çözümlemesini kontrol etmez.

MTProxy yalnızca Telegram trafiğini taşır. Harici istekler için ayrı bir SOCKS5/HTTP proxy'si, çalışma alanının SOCKS5/HTTP rotası veya izin verilen bir doğrudan rota kullanılabilir; ayrıca devre dışı bırakılabilirler. Bağımsız tanık, kendi aktarım ayarlarına sahiptir. Sıradan SOCKS5/HTTP CONNECT kimlik doğrulaması, bu proxy protokollerinin kendisi tarafından şifrelenmez. Sahte TLS MTProxy gizli anahtarları hâlâ desteklenmemektedir.

## Giriş ve oturum içe aktarma işlemleri

Dönüştürülmüş .tgwitness-session dosyaları, kasaya yüklenip depolanana kadar düz metin biçiminde bir yetkilendirme şifresi içerir. Çevrimdışı CLI, gözden geçirilmiş Telethon şemalarını kabul eder. Panel içe aktarma özelliği ayrıca Pyrogram SQLite, modern tek hesaplı TData ZIP ve belgelenmiş JSON girdilerini kabul eder. Kimlik doğrulaması yapılır, dört dosya / 8 MiB ile sınırlıdır ve arşiv açma veya orijinal dosyaları kaydetme işlemine gerek kalmadan yüklemeleri bellekte işler. Normalleştirilmiş kimlik bilgileri yalnızca isteği yapan ve kimliği doğrulanmış tarayıcıya döndürülür; Telegram yetkilendirmesi başarıyla tamamlandıktan sonra şifreli kasada saklanır. Orijinalleri ve dönüştürülmüş dosyaları koruyun ve eşzamanlı istemcilerin yetkilendirmeyi kopyalamasını önleyin.

Veri işleme, konteyner sağlama toplamlarını, yerel şifre çözme hash'lerini ve yapı uzunluklarını doğrular. Sağlanan masaüstü yerel şifresi geçici olarak kullanılır ve saklanmaz. Bu sınırlı ayrıştırıcı, her masaüstü sürümünün uyumlu olduğunu garanti etmez. QR görüntüleri yerel olarak oluşturulur, kısa ömürlü Telegram oturum açma belirteçleri içerir ve asla harici bir görüntüleme hizmetine gönderilmez. Kilitleme, çalışma alanı değiştirme, yeni oturum açma ve rota değişiklikleri, bekleyen QR denemelerini iptal eder. Bir sekmeyi yeniden yüklemek/kapatmak, denemeyi süresi dolana kadar beklemede bırakabilir. Başarılı bir QR oturum açma işlemi yine de hesap bağlanmasını zorunlu kılar. Sıradan API gövdeleri 16 KiB ile sınırlı kalır; kimlik doğrulamalı içe aktarma yolu, en fazla 12 MiB kodlanmış JSON kabul eder ve daha küçük kod çözülmüş dosya sınırını ayrı olarak uygular.

Giriş kodları ve Telegram iki aşamalı doğrulama şifreleri kalıcı olarak saklanmaz. Telefon numarası/kod hash durumu, yetkilendirme sırasında bellekte tutulur. Telegram oturumları hesap erişimi sağlar; hiçbir zaman bir veri dizini, oturum, token, kasa anahtarı veya özel imzalama anahtarını GitHub'a yüklemeyin.

## Günlükler ve aktarım

Varsayılan API doğrulama yanıtı, kimlik bilgilerini yansıtmayacak şekilde değiştirilmiştir. Uygulama erişim günlüğü devre dışı bırakılmıştır. Yetkilendirme başlıklarını veya istek gövdelerini günlüğe kaydetmek için ters proxy yapılandırmayın. HTTP, jetonları ve oturum açma şifrelerini düz metin olarak taşır: localhost'tan ayrılırken her zaman HTTPS veya bir SSH tüneli kullanın.

## Bütünlük sınırları

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## Bir sorun olduğundan şüpheleniyorsanız

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
