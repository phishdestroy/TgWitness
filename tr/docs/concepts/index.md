# Telegram · Kanıtların nasıl işlediğini görün

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/concepts/

Mesajlar değişir. Gördüklerinizin kaydı değişmemeli ve bunu herkes doğrulayabilmeli.

Aşağıda iki küçük deney. Kurgusal mesajlar, her şey tarayıcınızda çalışır, Telegram'a hiçbir şey gitmez.

## Sohbet dışa aktarımından doğrulanabilir bir kayda

Bir [Telegram Desktop dışa aktarımı](https://telegram.org/blog/export-and-more) şu an görünen geçmişi HTML ya da JSON olarak kaydeder. TgWitness buna sürekli bir değişiklik günlüğü, her kayıtta imza ve başkalarının karşılaştırabileceği kontrol noktaları ekler.

| Görev | Telegram Desktop dışa aktarma | TgWitness |
| --- | --- | --- |
| Kaydedilmiş sohbetleri okuyun | Seçilen medya ile birlikte HTML veya JSON | Kaydedilmiş sohbetler, aranabilir günlük ve çevrimdışı raporlar |
| Zaman içindeki değişiklikleri takip edin | Dışa aktarıldığında erişilebilen geçmiş | Eski sürümler, sonraki düzenlemeler ve silmeler, hepsi saklanır |
| Devir teslimden sonra dosyaları kontrol edin | Standart HTML/JSON dışa aktarım dosyaları imzalanmamıştır | İmzalı manifest, imzalı kayıtlar ve mühürlü raporlar, güvenilir bir anahtarla doğrulanır |
| Daha önceki bir saklama durumuyla karşılaştırın | Ayrı bir referans kopyası veya hash tutun | İmzalı kontrol noktaları, ayrı bir tanık ve isteğe bağlı harici zaman damgaları |

Karşılaştırma, 2 Kasım 2026 itibarıyla [Telegram Desktop dışa aktarma koduna](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) dayanır.

## Tek mesaj, üç gözlem

Yeni bir mesaj, bir düzenleme ve bir silme üç ayrı kayıt olur. Düzenleme ilkinin üzerine yazmaz, silme de onu ortadan kaldırmaz.

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

Telegram bir mesajı kimin ve tam olarak ne zaman sildiğini söylemez. TgWitness tahmin etmek yerine bu alanları boş bırakır.

## Bir kaydı değiştirin. Hash değerini takip edin.

Her kayıt bir öncekinin karmasını içerir. Başka yerde saklanan bir kontrol noktası günlük uzunluğunu ve son karmayı sabitler.

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

**C**, dokuz olay alanının UTF-8 JSON halidir: sıralı anahtarlar, fazla boşluk yok, ASCII kaçışı yok, NaN/sonsuz yok. `previous_hash` hi−1'dir, h0 64 sıfırdır ve imzalar özetin 32 ham baytını kapsar.

Alanlar: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Tam belirtim: [olay kodlaması](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#event-canonicalization).

KORUNAN KONTROL NOKTASI

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Kontrol noktasının imzasını sabitlenmiş anahtarla doğrulayın, sonra günlükle karşılaştırın. Sonraki bir dışa aktarım daha uzun olabilir ama kontrol noktasında eşleşmelidir.

## Üç soru, üç farklı kontrol

[01 / BÜTÜNLÜK**Bu kayıtta bir değişiklik mi oldu?** Güvendiğiniz bir anahtara karşı karmalar ve imzalar.](https://phishdestroy.github.io/TgWitness/tr/docs/exports/)[02 / SÜREKLİLİK**Daha önce neler korunmuştu?** Dışa aktarımı bir tanığın sakladığı kontrol noktalarıyla karşılaştırın.](https://phishdestroy.github.io/TgWitness/tr/docs/witness/)[03 / TESLİMAT**Bu test olayları geldi mi?** Test mesajları gönderin, düzenleyin, silin ve her hesabın neyi yakaladığını görün.](https://phishdestroy.github.io/TgWitness/tr/docs/cases/)

İmzalar "değiştirildi mi?", kontrol noktaları "önceki haliyle uyuşuyor mu?", test mesajları "her şeyi yakaladık mı?" sorusunu yanıtlar. [Doğrulamanın neyi kanıtladığı ve neyi kanıtlamadığı.](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope)

Sıradaki: baştan dava paketine kadar bir [tüm hesap soruşturması](https://phishdestroy.github.io/TgWitness/tr/docs/cases/).

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
