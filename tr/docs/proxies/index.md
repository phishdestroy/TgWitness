# Bir proxy seçin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/proxies/

Hesabı çevrimiçi tutun ve sunucunuzun IP'sini hiç gösterip gösteremeyeceğine kendiniz karar verin.

## Önce IP modunu seçin

01**Adresi gizle**

Yalnızca proxy. Hiçbiri çalışmazsa bekler.

02**Son çare olarak Direct**

Bir gecikmeden sonra doğrudan bağlanır, çalışan bir proxy bulunca ona döner.

03**Tünel veya VPN arkasında bulunan sunucu**

Doğrudan bağlantı olur. VPN'i sizin yerinize kurmaz ya da denetlemez.

Yol, bağlantıyı seçer. IP modu, doğrudan bağlantıya izin verilip verilmeyeceğini belirler.

## Havuzun rotayı korumasına izin verin

1. **Hesap → Ayarlar → Bağlantı ayarları**.
2. IP kipini ve **Otomatik MTProxy**'yi ya da sabit bir rotayı seçin.
3. Kaydedin, **Telegram bağlantısını test et** (girişten önce de çalışır).
4. Toplamayı başlatın ve kendinize bir test mesajı gönderin.

Yeni çalışma alanları otomatik MTProxy ve **Adresi gizle** ile başlar. Havuz dört herkese açık listeyi kullanır, sunucuları dener, iyileri tutar, ölüleri değiştirir.

## Kendi proxy'nizi kullanın

SOCKS5, HTTP CONNECT, bir Telegram proxy bağlantısı ya da operatör kataloğu. Değiştirmeden önce gözlemi duraklatın. Fake TLS sırları (`ee`…) çalışmaz.

**Dönüş, paylaşım ve yeniden deneme ayarları**

**Parametreler → Otomatik MTProxy**: hata eşikleri, bekleme süreleri, rotasyon, proxy başına hesap. Sınır 1, hesabın paylaşmak yerine beklemesi demektir. Farklı proxy'ler yine de aynı çıkış IP'sini paylaşabilir.

## Telegram'ı harici isteklerden ayırın

MTProxy yalnızca Telegram trafiğini taşır. Zaman damgaları, bildirimler, kopyalar ve kod kontrolleri ayrı bir SOCKS5/HTTP proxy'si, hesabın SOCKS5/HTTP rotası ya da kip izin veriyorsa doğrudan gider. Ya da kapatın.

`TGWITNESS_PROXY_FEED_PROXY` liste indirmeleri için rotayı belirler. [Tanığın](https://phishdestroy.github.io/TgWitness/tr/docs/witness/) kendi ayarları vardır. Bunların hiçbiri tarayıcınıza ya da sistem ağına dokunmaz.

Daha fazlası: [kipler ve varsayılanlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes), [rotaları kim değiştirebilir](https://phishdestroy.github.io/TgWitness/tr/docs/access/).
