# Bir proxy seçin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/proxies/

Hesabı bağlı tutun. Rotasının ne zaman sunucunun adresini kullanabileceğine açıkça karar verin.

## Önce IP modunu seçin

01**IP'yi Gizle**

Bir proxy kullanın. Hiçbiri işe yaramazsa, doğrudan Telegram bağlantısı olmadan bekleyin.

02**Yedek seçeneğine izin ver**

Yapılandırılan gecikme süresinin ardından Direct'e izin verin; biri yanıt verdiğinde çalışan bir proxy'ye geri dönün.

03**Tünel / VPN**

Barındırıcı ağından doğrudan bağlantı izin verin. Bu seçenek bir VPN kurmaz veya doğrulamaz.

Yol, bağlantıyı seçer. IP modu, doğrudan bağlantıya izin verilip verilmeyeceğini belirler.

## Havuzun rotayı korumasına izin verin

1. **Hesap** Aç **→ Ayarlar → Bağlantı ayarları**.
2. IP modunu ve **Otomatik MTProxy'yi** seçin veya sabit bir rota girin.
3. **Telegram bağlantısını** kaydedin ve **test** edin. Oturum açmadan önce de çalışır.
4. Toplamaya başladıktan sonra, kontrol edilen mesajın günlüğe ulaştığını kontrol edin.

Yeni çalışma alanları, IP Gizleme özelliğine sahip otomatik MTProxy kullanır. Havuz, dört kamuya açık kaynağı birleştirir, girişleri kontrol eder, çalışan rotaları korur ve arızalı proxy'leri değiştirir. Başarısız indirmelerde önceki anlık görüntüler saklanır.

## Kendi proxy'nizi kullanın

SOCKS5 veya HTTP CONNECT bilgilerini girin, desteklenen bir Telegram proxy bağlantısını yapıştırın veya bir operatör kataloğu sağlayın. Etkin bir rotayı değiştirmeden önce gözlemi duraklatın. `ee` ile başlayan sahte TLS MTProxy gizli anahtarları hâlâ desteklenmemektedir.

**Dönüş, paylaşım ve yeniden deneme ayarları**

**Parametreler → Otomatik MTProxy** altında, hata eşiklerini, bekleme sürelerini, planlı rotasyonu ve proxy başına hesap sayısını ayarlayın. Paylaşım sınırı "bir" olarak ayarlandığında, özel giriş bulunmadığında hesap beklemeye alınır. Liste yenileme ve sondalama aralıkları, ana çalışma alanındaki değerlere göre belirlenir. Ayrı proxy'ler, ayrı çıkış IP'lerini garanti etmez.

## Telegram'ı harici isteklerden ayırın

MTProxy yalnızca Telegram trafiğini taşır. Zaman damgaları, bildirimler, kopyalar ve kaynak kontrolleri için ayrı bir SOCKS5/HTTP proxy'si, hesabın SOCKS5/HTTP rotası veya IP modunun izin verdiği durumlarda Direct kullanılır. Bu harici istekler devre dışı bırakılabilir.

`TGWITNESS_PROXY_FEED_PROXY` parametresinin açıkça belirtilmesi, besleme indiricisinin yönünü belirler. [Bağımsız tanık](https://phishdestroy.github.io/TgWitness/tr/docs/witness/), kendi ayarlarını korur. Bu denetimler, bir sistem VPN'i kurmaz veya tarayıcı trafiğini yönlendirmez.

[Tüm modları, varsayılan ayarları ve kaynak listelerini](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes) görüntüleyin veya [bir hesabın yönlendirmesini kimlerin değiştirebileceğini seçin](https://phishdestroy.github.io/TgWitness/tr/docs/access/).
