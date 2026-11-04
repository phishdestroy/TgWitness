# Witness botunu kurun

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/witness/

Ayrı bir süreç günlüğünüzü kontrol eder ve imzalı kontrol noktalarını bir kanalda yayınlar.

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

BotFather ile bir bot oluşturun ve kanalınızda yazmasına izin verin. Tanığı başka bir yerde çalıştırın: başka bir sunucu, tercihen başka biri tarafından işletilen, toplayıcının yanındaki ikinci bir süreçten çok daha değerlidir.

## Ekstra bölümündeki üç adım

1. **Salt okunur erişim.** **Ekler → Bağımsız tanık**, bir belirteç oluşturun, dosyayı kaydedin. Kontrol noktalarını ve durumu okur, başka bir şey değil.
2. **Kanal ve aralık.** Telegram kanalı ya da Discord webhook'u, artı tanığın ulaşabileceği bir toplayıcı adresi. Ayar dosyasını kaydedin.
3. **Başlatma.** `witness.json`, `witness-token.txt` ve `bot-token.txt`'yi tanık sunucusunda bir araya koyun ve çalıştırın:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Kanalda ilk imzalı gönderiyi bekleyin, sonra tanığın parmak izini güvenli bir yere kaydedin.

Discord mu tercih ediyorsunuz? Webhook URL'sini `discord-webhook.txt` olarak kaydedin. Bir tanık tek bir yere yazar; uzun kontroller Discord'a dosya olarak gelir.

## Yayın sıklığını seçin

Her kontrolü yayınlamak düzenli bir dış kayıt oluşturur: beş dakikada bir, çalışma alanı başına günde yaklaşık 288 gönderi demektir. Gelişmiş ayarlar yalnızca değişiklik ya da sorunlarda yayın yapmaya, bir proxy ya da özel bir Bot API kullanmaya izin verir.

**Bot aslında neyi doğruluyor?**

Toplayıcıdan imzalı bir kontrol noktası ister, beklenen anahtarla doğrular ve kaçırılan ve reddedilen yanıtlar dahil kendi imzalı günlüğünü tutar.

Günlük durumunu kontrol eder, Telegram'ı kendisi izlemez. Bunun için kontrollü bir teslim testi yapın.

## Kanıtları daha sonra kontrol edin

Tanık günlüğünü, gönderileri ve parmak izlerini saklayın. Bunları toplayıcının dışa aktarımına karşı [nasıl kontrol edeceğiniz](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/#verify).
