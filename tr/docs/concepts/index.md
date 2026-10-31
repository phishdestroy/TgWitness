# Kanıtların nasıl işlediğini görün

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/concepts/

Bir mesaj değişebilir. Gözlemlediklerinizin kaydı, her zaman doğrulanabilir olmalıdır.

Aşağıdaki iki küçük denemeyi inceleyin. Bu denemeler kurgusal mesajlar kullanır, tarayıcınızda kalır ve hiçbir zaman Telegram'a bağlanmaz.

## Tek mesaj, üç gözlem

Telegram yeni bir mesaj, bir düzenleme veya bir silme bildirimi gönderdiğinde, toplayıcı uygulama üç ayrı gözlem ekler. Düzenleme, ilk kaydı değiştirmez. Silme bildirimi ise onu silmez.

01 / MESAJIN YOLCULUĞUAçıklayıcı akış

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Toplayıcı · Günlük · güncelleme → · ekle →

GÜNCEL SOHBET GÖRÜNÜMÜ Mesaj #42

Mesaj silindi

Mesaj, sohbet ekranından kayboldu.

GÖZLEM GÜNLÜĞÜ 3 kayıt

1. 01

   `message.new`

   Saat 10:00'da buluşalım

   ✓
2. 02

   `message.edited`

   Saat 11:00'da buluşalım

   ✓
3. 03

   `message.deleted`

   #42 için silme bildirimi

   ✓

Alınan üç gözlem de kayıt defterinde kalır.

Önceden seçilmiş bir kaynak için basitleştirilmiş yol. Operasyonel kayıtlar da gerçek günlüğü paylaşır. Yakalama işlemi, hesabın görebildiklerine ve Telegram'ın sağladıklarına bağlıdır.

Bir silme bildirimi, ne güvenilir bir silme zamanını ne de mesajı silen kişiyi belirtir. Bu değerlerin bilinmemesi, bir gözlem ile bir tahmin arasındaki ayrımı korur.

## Bir kaydı değiştirin. Hash değerini takip edin.

Her kayıt, bir önceki kaydın hash değerini içerir. Kayıtın kendi hash değeri, bu bağlantı da dahil olmak üzere olay alanlarını kapsar. Harici olarak tutulan bir kontrol noktası, belirli bir günlük uzunluğunu ve başlangıç hash değerini sabitler.

02 / HASH-CHAIN SANDBOXGerçek SHA-256 · örnek kayıtlar

KAYIT 01**Mesaj alındı**`h₁ = SHA-256(e₁)`64 sıfırlı bağlantılar

KAYIT 02**Saat 11:00'da buluşalım**`h₂ = SHA-256(e₂)`h₁ etiketini içerir

KAYIT 03**Silme işlemi gözlemlendi**`h₃ = SHA-256(e₃)`h₂ içerir

BAŞKA YERDE SAKLANAN**3 kayıt · başlık `h₃`**Bu sabit sınırı, sağlanan kayıt defteriyle karşılaştırın.

Bir olayın değiştirilmesi, o olayın hash değerini değiştirir. Zincirin yeniden oluşturulması, zincirin başını değiştirir. Zincirin sonunun kaldırılması, zinciri saklanan kontrol noktasından daha kısa hale getirir.

**2 numaralı kaydı ve tam hash değerlerini inceleyin**

Bu, örnekte yer alan tam UTF-8 JSON hash değeridir. Değerler hayali olup, dokuz alan ve serileştirme, kayıt defteri formatıyla uyumludur.

```

```

Kaydedilen kayıt 2 hash

``

Yeniden hesaplanan kayıt 2 hash

``

Bu sanal ortam, imzaları değil, hash değerlerini hesaplar. Gerçek doğrulayıcı, her olayın Ed25519 imzasını, sırasını ve bağlantısını da kontrol eder. Yalnızca hash değerlerinin yeniden oluşturulması, güvenilir anahtar altında geçerli imzalar oluşturmaya yetmez.

## Asıl kurallar, birkaç satırda

HASH + İMZA

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C**, dokuz olay alanını UTF-8 JSON olarak serileştirir: sıralı anahtarlar, fazladan boşluk yok, ASCII kaçış karakterleri yok ve NaN/sonsuzluk yok. Olayın `previous_hash` değeri hi−1'dir. Görüntülenen h0, 64 sıfır karakteri anlamına gelir; imzalar 32 ham özet baytını kapsar.

Dokuz alan şunlardır: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` ve `previous_hash`. Bu, TgWitness’in [belgelenmiş JSON](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#event-canonicalization)kodlamasıdır; hash ve imza kendileri hash giriş alanları değildir.

KORUNAN KONTROL NOKTASI

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Sabitlenmiş toplayıcı anahtarının altındaki kontrol noktası imzasını doğrulayın, ardından sınırını doğrulanmış günlükle karşılaştırın. Daha sonraki bir dışa aktarım daha fazla kayıt içerebilir; ancak yine de önceki kontrol noktasıyla uyumlu olmalıdır.

## Üç soru, üç farklı kontrol

[01 / BÜTÜNLÜK**Bu kayıtta bir değişiklik mi oldu?** Hash değerlerini ve imzaları, ayrı bir güvenilir anahtarla karşılaştırarak doğrulayın.](https://phishdestroy.github.io/TgWitness/tr/docs/exports/)[02 / SÜREKLİLİK**Daha önce neler korunmuştu?** İmzalı bir dışa aktarım dosyasını, ayrı bir tanık tarafından tutulan kontrol noktalarıyla karşılaştırın.](https://phishdestroy.github.io/TgWitness/tr/docs/witness/)[03 / TESLİMAT**Bu test olayları geldi mi?** Her hesabın günlüğüyle, kontrollü gönderme, düzenleme ve silme işlemlerini karşılaştırın.](https://phishdestroy.github.io/TgWitness/tr/docs/cases/)

Eşleşen bir hash zinciri, bütünlük sorusuna yanıt verir. Ancak bu, mesajın Telegram üzerinden tam olarak iletildiğini, mesajın doğruluğunu veya bağımsız olarak güvenilir bir gözlem zamanını kanıtlamaz.

Vakalara ilişkin bilgilerin toplanmasından dava dosyasının hazırlanmasına kadar [tüm soruşturma](https://phishdestroy.github.io/TgWitness/tr/docs/cases/) sürecini takip edin.
