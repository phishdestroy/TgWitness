# Güvenliği sağlayın

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/security/

Telegram için kullanılan yolları, genel proxy listelerini ve isteğe bağlı harici hizmetleri öğrenin. Her bir gizli ayarın neyi açığa çıkardığını, korumaların neleri kapsadığını ve neleri size bıraktığını öğrenin.

**127.0.0.1**Varsayılan panel adresi

**256 bit**rastgele panel jetonu

**0**CDN'ler, analitik araçlar veya uzaktan fontlar

**Ed25519**her kayda imza

## Her şeyin bulunduğu yer

Toplayıcı, paneli ve kaydedilen tüm kayıtlar, aracı çalıştırdığınız bilgisayar veya sunucuda kalır. Varsayılan olarak tek hedef Telegram’dır; diğer her hedef ayrı bir anahtarla seçilir.

06 / MAKİNEDEN NE ÇIKAR?Kurulumunuz

BİLGİSAYARINIZ VEYA SUNUCUNUZ

**Panel**127.0.0.1:8787 · bearer token

**Toplayıcı**Her çalışma alanı için bir Telegram istemcisi

VERİ DİZİNİ

**Günlük**SQLite · hash zincirli · imzalı

**Medya**SHA-256 ile adlandırılmış dosyalar

**Vault**Fernet · oturum, API çifti, imzalama anahtarı, proxy

- **Telegram**Her zaman · sizin rotanız üzerinden

  Hesabın MTProto bağlantısı: doğrudan, SOCKS5, HTTP veya MTProxy. IP gizleme modu, çalışan bir proxy bekler. Doğrudan yedekleme, bunu açıkça izin veren bir mod gerektirir.
- **Site dışı metin**İsteğe bağlı · varsayılan olarak kapalı

  Günlük, dosyalar ve kontrol noktaları, S3 uyumlu depolama alanına yüklenmeden önce AES-GCM ile şifrelenir. Şifre anahtarı sizde kalır; ekler, içerik hash'leri yerine anahtarlı hash'lerle adlandırılır.
- **Bildirimler**İsteğe bağlı · varsayılan olarak kapalı

  Sohbet başlıklarıyla ilgili sorunlar ve değişiklik sayıları. Mesaj alıntıları, yalnızca bu özelliği etkinleştirirseniz gönderilir.
- **Zaman damgası yetkisi**İsteğe bağlı · varsayılan olarak kapalı

  Yalnızca imzalı bir kontrol noktasının SHA-256 değeri ve rastgele bir nonce. Mesaj yok, sohbet adları yok.
- **Witness**İsteğe bağlı · varsayılan olarak kapalı

  Salt okunur bir jetonla imzalı kontrol noktalarını ve yakalama sayaçlarını alır. Sohbetleri okuyamaz veya ayarları değiştiremez.

Varsayılan ayar: Bu makineden yalnızca Telegram bağlantısı dışarıya çıkar.

İsteğe bağlı hedefler, çalışma alanı başına yapılandırılır. Mesaj metinleri ve medya dosyaları, veri dizininde şifrelenmemiş olarak saklanır: disk şifreleme ve dosya izinleriyle bu verileri koruyun.

## Her bir sırın açığa çıkardığı şeyler

| Gizli | Nerede saklanır? | Neleri mümkün kılar | Eğer sızarsa |
| --- | --- | --- | --- |
| **Panel jetonu** | Veri dizininde `panel-token.txt`; tarayıcı bunu yalnızca sekme için saklar | Her çalışma alanında her şey: okuma ve dışa aktarma, kapsamı değiştirme, hesaplara giriş yapma | TgWitness'i durdurun, `panel-token.txt`'yi silin, yeniden başlatın: yeni bir token oluşturulur |
| **Telegram oturumu** | Şifreli depo (`credentials.enc`) | Telegram hesabının kendisi | Telegram'da *Ayarlar → Cihazlar* bölümünden oturumu sonlandırın |
| **İmza anahtarı** | Şifreli depo (`signing.enc`) | Parmak izinizle doğrulanabilen kayıtların imzalanması | Başka bir yerde tutulan kontrol noktaları, bir tanık ve zaman damgaları, daha önce neyin var olduğunu gösterir |
| **Kasa anahtarı** | Verilerin yanında `vault.key` veya yeni bir veri dizini için harici bir ana anahtar | Kasanın şifresini çözme | Oturum ve imzalama anahtarının da sızdırılmış olduğu varsayılmalıdır |
| **Witness tokeni** | Witness sunucusunda | Salt okunur: imzalı kontrol noktaları ve durum bilgisi | Witness sayfasından silin; yeni bir tane oluşturun |
| **Site dışı metin anahtarı** | Vault; kurtarma amacıyla bir kez indirin | Site dışı kopyanın şifresinin çözülmesi | Saklanan nesneleri elinde bulunduran herkes bunları şifresini çözebilir: bu kopyayı ifşa olmuş olarak değerlendirin |

## Koruma kapsamı

### Kapsanan konular

- Dışa aktarımda değiştirilen, kaldırılan veya sırası değiştirilen bir kayıt: hash zinciri veya imza artık doğrulanamaz.
- Bir kontrol noktası başka bir yerde saklandıktan sonra kısaltılan veya yeniden oluşturulan bir günlük: saklanan kontrol noktası artık eşleşmiyor.
- Panel jetonunu tahmin etme: 256 rastgele bit, sabit sürede karşılaştırılır; dakikada 15 başarısız denemeden sonra adres reddedilir.
- Zararlı sohbet içeriği: metin, asla HTML olarak değil, metin olarak eklenir; ekler dosya olarak indirilir; panel, diğer sitelerden hiçbir şey yüklemez.
- Harici bir kasa anahtarı içeren kopyalanmış bir veri dizini: ana anahtar olmadan oturumlar ve imzalama anahtarları şifreli kalır.

### Size kalmış

- Ana panel jetonu tam kontrol sağlar. Diğer kişilere ihtiyaç duydukları hesaplara, sohbetlere ve eylemlere sınırlı erişim izni verin; ana anahtarı gizli tutun.
- Sistemin bir yöneticisi her şeyi okuyabilir ve günlüğü yeniden yazıp yeniden imzalayabilir. Parmak izini ve kontrol noktalarını başka bir sistemde saklayın.
- Mesaj metinleri ve medya dosyaları TgWitness tarafından şifrelenmez. Disk şifreleme ve sıkı izin ayarları kullanın.
- localhost dışındaki düz HTTP bağlantısı, ağ üzerinde token'ı gösterir. HTTPS veya bir SSH tüneli kullanın.
- İmzalar, kaydedilenlerin değiştirilmediğini kanıtlar; her Telegram olayının kaydedildiğini değil.

İzinler, geçerlilik süresi ve oturum sınırlamalarıyla [bir vakaya erişimi paylaşın](https://phishdestroy.github.io/TgWitness/tr/docs/access/). Tanık jetonu ayrı bir kimlik bilgisi olarak kalır.

## Kurulumu güçlendirin

8'in 0'ı tamamlandı

1. **Ayrı bir Telegram hesabı kullanın** — asla ana hesabınızı kullanmayın. Panel jetonu ve oturum, hesap üzerinde tam kontrol sağlar.
2. **Paneli 127.0.0.1 adresinde tutun.** Panele uzaktan erişim için yalnızca HTTPS (pakete dahil Caddy yapılandırması) veya bir SSH tüneli kullanın.
3. Veri dizinini barındıran **diski şifreleyin**: mesaj metinleri ve medya dosyaları geldikleri haliyle saklanır.
4. **Veri dizinini** hizmet hesabıyla **sınırlandırın**. Unix'te yeni dizinlere 0700 modu atanır; Windows'ta ise klasörün izinlerini ayarlayın.
5. **Kasa anahtarını** sunucularda **başka bir yerde saklayın**: veri dizinini oluşturmadan önce `TGWITNESS_VAULT_KEY_FILE`'yi ayarlayın.
6. **İmza anahtarının parmak izini ve kontrol noktalarını** başka bir sisteme **kaydedin** ve başka bir sunucuya bir tanık ekleyin.
7. `data/`, oturum anahtarları, `panel-token.txt` veya kasa anahtarlarını **asla** GitHub'a veya bir sohbete **yüklemeyin**.
8. Ters proxy'de `Authorization` başlıklarını veya istek gövdelerini **kaydetmeyin**.

**Verileri kaybetmeden panel jetonunu değiştirebilir miyim?**

Evet. Jeton yalnızca paneli açar. TgWitness'i durdurun, veri dizininden `panel-token.txt`'yi silin ve yeniden başlatın; günlük, oturumlar ve anahtarlar değişmeden kalır. `TGWITNESS_TOKEN` ayarlandığında, dosya yerine ortam değeri kullanılır.

**Mesajlar neden depolandıkları sırada şifrelenmiyor?**

Toplayıcı, arama yapmak, sürümleri karşılaştırmak ve dışa aktarmak için bu verileri okumalıdır. Aynı makinedeki bir anahtarla şifrelemek, o makineyi okuyabilen birine karşı pek bir koruma sağlamaz. Disk şifreleme, durdurulmuş veya çalınmış bir diski korur; sıkı izinler ise çalışır durumdaki bir diski korur.

## Bir güvenlik açığını bildir

GitHub deposunda **Güvenlik → Bir güvenlik açığını bildir** seçeneğini kullanın. Sürümü, etkisini ve sorunu en az adımda yeniden oluşturabilen bir örnek ekleyin. Asla kimlik bilgilerini, hesap dizinlerini veya gerçek kanıt arşivlerini göndermeyin. Özel bildirim seçeneği mevcut değilse, istismar ayrıntılarını içermeyen bir özel kanal talebinde bulunmak üzere bir sorun açın.
