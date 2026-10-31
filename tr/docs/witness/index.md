# Witness botunu kurun

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/witness/

Günlüğü ayrı bir işlemle kontrol ettirin ve imzalı kontrol noktalarını kanalınızda yayınlayın.

## İki sunucu, iki imzalama anahtarı

BARINDIRMA / TOPLAYICI**Hesap + günlük**

Telegram oturumu Toplayıcı imzalama anahtarı

Salt okunur kontrol noktası uç noktası

← imzalı yanıt isteği →

HOST B / WITNESS**Doğrula + sakla**

Sabitlenmiş toplayıcı parmak izi Ayrı tanık imzalama anahtarı

Kendi günlüğü + bot jetonu

Witness → Telegram Bot API →**Kanalınız · imzalı TGW1 gönderileri**

Witness, kontrolleri kendi başına gerçekleştirir. Toplayıcının erişimi salt okunurdur. Bot yayını, Witness’ın bağlantısını ve jetonunu kullanır; Witness’a herhangi bir hesap oturumu verilmez.

03 / KONTROL NOKTASI KARARLARIAçıklayıcı cevaplar

SON KABUL EDİLEN**120 kayıt**`head 9c7d…`

SONRAKİ CEVAP**128 kayıt**`head a4f2…`

Kabul edildi: sayı artıyor, imza doğrulanıyor ve anahtar eşleşiyor. Tanık bu yeni sınırı koruyor.

Tüm cevap örnekleri, geçerli bir imza ve sabitlenmiş anahtarın mevcut olduğunu varsayar. Buradaki hash değerleri, örnek niteliğinde kısaltılmış şekildedir. Yalnızca sayıca fazlalık, eski öneklerin tamamının değişmediğini kanıtlayamaz; dışa aktarılan verileri, korunan kontrol noktalarıyla karşılaştırın.

## Bir bot ve bir kanal hazırlayın

BotFather ile bir bot oluşturun ve bu botun sizin kontrolünüz altındaki bir kanalda paylaşım yapmasına izin verin. Tanık için bir bilgisayar veya sunucu seçin. Ayrı bir barındırma sunucusu ve operatör, toplayıcının sunucusundaki ikinci bir işlemden daha fazla bağımsızlık sağlar.

## Ekstra bölümündeki üç adım

1. **Yalnızca okuma erişimi. Ekstralar'ı** açın **→ Kanalınıza bir bot ekleyin**, bir tanık jetonu oluşturun ve erişim dosyasını kaydedin. Bu erişim, kontrol noktalarını ve durum bilgilerini okumaya izin verir; sohbetlere veya toplayıcı kontrollerine erişim sağlamaz.
2. **Kanal ve aralık.** Kanalı ve tanık tarafından erişilebilir bir toplayıcı adresini girin. Ayar dosyasını kaydedin.
3. **Başlatma.** Witness sunucusunda oluşturulan `witness.json`, `witness-token.txt` ve `bot-token.txt` dosyalarını bir araya getirin. Yüklü proje ortamında aşağıdaki komutları çalıştırın.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Dosyaları indirmek, tanık aracını başlatmaz. İlk imzalı gönderinin kanalda göründüğünü kontrol edin, ardından tanık aracının açık anahtar parmak izini ayrı bir yerde saklayın.

## Yayın sıklığını seçin

Her kontrolün yayınlanması, düzenli bir harici kayıt oluşturur. Beş dakikalık aralıklarla bu, çalışma alanı başına günde yaklaşık 288 gönderi anlamına gelir. Gelişmiş ayarlar ayrıca değişiklikler veya sorunlar hakkında yayın yapma, bir proxy ve özel bir Bot API adresi seçenekleri sunar.

**Bot aslında neyi doğruluyor?**

Tanık, toplayıcıdan imzalı bir kontrol noktası ister, bunu beklenen anahtarla karşılaştırarak doğrular ve ayrı bir imzalı günlük tutar. Başarılı kontrollerle birlikte eksik yanıtları ve reddedilen cevapları da kaydeder. Yayınlama, tanığın çalışır durumda olmasına ve Telegram’ın Bot API’sine erişebilmesine bağlıdır.

Toplayıcının bildirdiği günlük durumunu kontrol eder. Her Telegram mesajını bağımsız olarak gözlemlemez. Bunun için kontrollü teslimat testini ekleyin.

## Kanıtları daha sonra kontrol edin

Tanık günlüğünü, kanal gönderilerini ve bağımsız olarak kaydedilmiş parmak izlerini saklayın. [Tam doğrulama prosedürü,](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/#verify) bunları toplayıcının imzalı dışa aktarım dosyasıyla karşılaştırır.
