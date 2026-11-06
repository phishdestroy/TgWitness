# Telegram · Güvenliği sağlayın

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/security/

Makinenizden ne çıkar, her sır neyi açar ve korumalar neyi kapsar, neyi size bırakır.

**127.0.0.1**Varsayılan panel adresi

**256 bit**rastgele panel jetonu

**0**CDN'ler, analitik araçlar veya uzaktan fontlar

**Ed25519**her kayda imza

## Her şeyin bulunduğu yer

Toplayıcı, panel ve tüm kayıtlar makinenizde kalır. Varsayılan olarak yalnızca Telegram'a bağlanılır; geri kalan her şey ayrı bir anahtardır.

06 / MAKİNEDEN NE ÇIKAR?Kurulumunuz

BİLGİSAYARINIZ VEYA SUNUCUNUZ

**Panel**127.0.0.1:8787 · taşıyıcı belirteci

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
- **Tanık**İsteğe bağlı · varsayılan olarak kapalı

  Salt okunur bir jetonla imzalı kontrol noktalarını ve yakalama sayaçlarını alır. Sohbetleri okuyamaz veya ayarları değiştiremez.

Varsayılan ayar: Bu makineden yalnızca Telegram bağlantısı dışarıya çıkar.

İsteğe bağlı hedefler, çalışma alanı başına yapılandırılır. Mesaj metinleri ve medya dosyaları, veri dizininde şifrelenmemiş olarak saklanır: disk şifreleme ve dosya izinleriyle bu verileri koruyun.

## Her bir sırın açığa çıkardığı şeyler

| Gizli | Nerede saklanır? | Neleri mümkün kılar | Eğer sızarsa |
| --- | --- | --- | --- |
| **Panel jetonu** | Veri klasöründe `panel-token.txt`; tarayıcı onu sekme başına tutar | Her çalışma alanındaki her şey | TgWitness'ı durdurun, `panel-token.txt`'yi silin, yeniden başlatın: yenisi oluşur |
| **Telegram oturumu** | Şifreli depo (`credentials.enc`) | Telegram hesabının kendisi | Telegram'da *Ayarlar → Cihazlar* bölümünden oturumu sonlandırın |
| **İmza anahtarı** | Şifreli depo (`signing.enc`) | Kayıtları sizin parmak izinizle imzalamak | Başka yerde saklanan kontrol noktaları, bir tanık ve zaman damgaları önceden neyin var olduğunu yine gösterir |
| **Kasa anahtarı** | Verilerin yanında `vault.key` ya da harici bir ana anahtar | Kasa | Oturumun ve imza anahtarının da sızdığını varsayın |
| **Witness tokeni** | Witness sunucusunda | Salt okunur: kontrol noktaları ve durum | Tanık sayfasında silin, yenisini oluşturun |
| **Site dışı metin anahtarı** | Vault; kurtarma amacıyla bir kez indirin | Harici kopya | Bucket'a da sahip olan herkes onu çözebilir: kopyayı açığa çıkmış sayın |

## Koruma kapsamı

### Kapsanan konular

- Değiştirilmiş, kaldırılmış ya da yeniden sıralanmış bir kayıt: karma zinciri ya da bir imza bozulur.
- Siz başka yere bir kontrol noktası kaydettikten sonra kısaltılmış ya da yeniden kurulmuş bir günlük: kontrol noktası artık eşleşmez.
- Belirteci tahmin etmek: 256 rastgele bit, sabit zamanlı karşılaştırma; dakikada 15 hata ve adres engellenir.
- Düşmanca sohbet içeriği: metin metin kalır, asla HTML olmaz; ekler dosya olarak iner; panel başka sitelerden hiçbir şey yüklemez.
- Harici kasa anahtarıyla çalınmış bir veri klasörü: oturumlar ve anahtarlar şifreli kalır.

### Size kalmış

- Ana belirteç her şeyi yapabilir. Başkalarına kısıtlı erişim verin, ana belirteci kendinize saklayın.
- Makinede yönetici olan her şeyi okuyabilir ve günlüğü yeniden imzalayabilir. Parmak izini ve kontrol noktalarını başka yerde tutun.
- TgWitness mesajları ve medyayı şifrelemez. Diski şifreleyin, izinleri kısıtlayın.
- localhost dışında düz HTTP belirteci sızdırır. HTTPS ya da SSH tüneli kullanın.
- İmzalar neyin kaçırıldığını söylemez. Kapsamı kontrol edin ve teslimatı kendi hesaplarınız ve kaynaklarınızda test edin.

[Bir davaya erişimi paylaşın](https://phishdestroy.github.io/TgWitness/tr/docs/access/); izinler, süre sonu ve oturum sınırlarıyla.

## Kurulumu güçlendirin

8'in 0'ı tamamlandı

1. **Ayrı bir Telegram hesabı kullanın**, asla ana hesabınızı değil.
2. **Paneli 127.0.0.1'de tutun.** Uzaktan erişim yalnızca HTTPS (paketli Caddy) ya da SSH tüneli ile.
3. **Veri klasörünün bulunduğu diski şifreleyin**; mesajlar ve medya geldikleri gibi saklanır.
4. **Veri klasörünü hizmet hesabıyla sınırlayın** (Unix'te 0700, Windows'ta klasör izinleri).
5. **Kasa anahtarını başka yerde tutun**; sunucularda ilk başlatmadan önce `TGWITNESS_VAULT_KEY_FILE` ayarlayın.
6. **Parmak izini ve kontrol noktalarını** başka bir sistemde saklayın, başka bir sunucuda bir tanık çalıştırın.
7. `data/`, oturum anahtarları, `panel-token.txt` veya kasa anahtarlarını **asla** GitHub'a veya bir sohbete **yüklemeyin**.
8. Ters proxy'de `Authorization` başlıklarını veya istek gövdelerini **kaydetmeyin**.

**Verileri kaybetmeden panel jetonunu değiştirebilir miyim?**

Evet, yalnızca paneli açar. TgWitness'ı durdurun, `panel-token.txt`'yi silin, yeniden başlatın. Günlük, oturumlar ve anahtarlar kalır. `TGWITNESS_TOKEN` ayarlıysa o değer dosyanın önüne geçer.

**Mesajlar neden depolandıkları sırada şifrelenmiyor?**

Toplayıcının aramak, karşılaştırmak ve dışa aktarmak için onları okuması gerekir. Aynı makinedeki bir anahtar, o makineyi zaten okuyabilen birini durdurmaz. Disk şifrelemesi çalınan diski, izinler çalışan sistemi korur.

## Bir güvenlik açığını bildir

GitHub'da **Security → Report a vulnerability**. Sürüm, etki ve kurgusal verilerle küçük bir örnek. Asla kimlik bilgileri, hesap klasörleri ya da gerçek kanıt göndermeyin. Gizli bildirim kapalıysa, istismar ayrıntısı vermeden gizli bir kanal isteyen bir issue açın.
