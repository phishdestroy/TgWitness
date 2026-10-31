# Kanıt sistemi nasıl çalışır?

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/how-it-works/

Hash zinciri, imzalar, kontrol noktaları ve tanıklar, doğrulayıcının kullandığı tam formüllerle açıklanmaktadır.

TgWitness, toplama hesabının gözlemlediklerini korur, bu gözlemleri imzalı bir günlüğe bağlar ve başka bir kişinin, güvenilir bir anahtar ve daha önce saklanan bir kontrol noktası ile karşılaştırarak dışa aktarılan verileri doğrulamasına olanak tanır.

[Yerel dokümantasyon web](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) sitesi, `/docs/concepts/` adresinde etkileşimli örnekler ve `/docs/witness/` adresinde bir kontrol noktası karar gezgini sunmaktadır. Tüm örnek mesajlar, sayımlar ve gecikmeler kurgusaldır. Zincir sanal ortamındaki hash değerleri, tarayıcıda SHA-256 ile hesaplanır. Telegram'a hiçbir şey gönderilmez.

## Bir mesaj değişir; gözlemler birikir

Sıra diyagramı · Telegram → Toplayıcı: Yeni mesaj: Saat 10:00'da buluşalım; Toplayıcı → İmzalı kayıt defteri: message.new ekle; Telegram → Toplayıcı: Düzenleme: Saat 11:00'da buluşalım; Toplayıcı → İmzalı kayıt defteri: message.edited ekle; Telegram → Toplayıcı: Silme bildirimi; Toplayıcı → İmzalı kayıt defteri: message.deleted ekle; İmzalı kayıt defteri ile ilgili not: Orijinal mesajlar, düzenlemeler ve silme işlemleri gözlemlenmeye devam eder · Telegram · Toplayıcı · İmzalı kayıt defteri · Yeni mesaj: Saat 10:00'da buluşalım · message.new ekle · Düzenleme: Saat 11:00'da buluşalım · message.edited ekle · Silme bildirimi · message.deleted ekle · Orijinal mesajlar, düzenlemeler ve silme işlemlerigözlemlenmeye devam eder

**Diyagramın metin olarak gösterimi**

1. Telegram → Toplayıcı: Yeni mesaj: Saat 10:00'da buluşalım
2. Toplayıcı → İmzalı kayıt defteri: message.new ekle
3. Telegram → Toplayıcı: Düzenleme: Saat 11:00'da buluşalım
4. Toplayıcı → İmzalı kayıt defteri: message.edited ekle
5. Telegram → Toplayıcı: Silme bildirimi
6. Toplayıcı → İmzalı kayıt defteri: message.deleted ekle
7. İmzalı kayıt defteri ile ilgili not: Orijinal mesajlar, düzenlemeler ve silme işlemleri gözlemlenmeye devam eder

Bu basitleştirilmiş akış, Telegram'ın her güncellemeyi ilettiğini ve seçilen hesabın bunu görebildiğini varsayar. Operasyonel olaylar da günlüğe kaydedilir. Bir silme bildirimi, silme işlemini gerçekleştiren kişiyi veya kesin silme zamanını belirtmez. Tekrarlanan iletimler ayrı gözlemlerdir; günlüğün genelinde yinelenen kayıtların bastırılması söz konusu değildir.

## Bir hash neyi kapsar?

![Gözlemle, kodla, hash değeri al ve imzala: her yeni olay, bir önceki hash değerini içerir.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Formülü içten dışa doğru okuyun: **C**, dokuz alanı tam baytlara dönüştürür; **SHA-256** bunların özetini üretir; **hex,** bu özetin nasıl depolandığını gösterir. Önceki hash zaten olayın içindedir. **unhex,** depolanan hash'i Ed25519'un imzaladığı 32 bayta geri dönüştürür.

[Statik zincir şeması](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

C(ei), dokuz olay alanının kanonik UTF-8 JSON'u olsun. İlk `previous_hash`, 64 sıfır karakterinden oluşur. Sonraki her kayıt, bir önceki kayıtın onaltılık hash değerini içerir:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

İmza, 32 baytlık ham özet verisini kapsar. Hash girdisi tam olarak `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` ve `previous_hash` değerlerini içerir. Nesne anahtarları sıralanır; boşluklar ve ASCII kaçış karakterleri atlanır; NaN ve sonsuz değerleri reddedilir. [Kesin kodlam](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#event-canonicalization)aya bakın.

Akış şeması · 64 boş karakter → Kayıt 1 / hash h1; Kayıt 1 / hash h1 → Kayıt 2, h1 / hash h2 içerir; Kayıt 2, h1 / hash h2 içerir → Kayıt 3, h2 / hash h3 içerir; Kayıt 3, h2 / hash h3 içerir → İmzalı kontrol noktası: sayım 3, başlık h3 (başka bir yerde sakla) · 64 boş karakter · Kayıt 1 / hash h1 · Kayıt 2, h1 / hash h2içerir · Kayıt 3, h2 / hash h3içerir · İmzalı kontrolnoktası: sayım 3,başlık h3 · başka bir yerde sakla

**Diyagramın metin olarak gösterimi**

1. 64 boş karakter → Kayıt 1 / hash h1
2. Kayıt 1 / hash h1 → Kayıt 2, h1 / hash h2 içerir
3. Kayıt 2, h1 / hash h2 içerir → Kayıt 3, h2 / hash h3 içerir
4. Kayıt 3, h2 / hash h3 içerir → İmzalı kontrol noktası: sayım 3, başlık h3 (başka bir yerde sakla)

| Sağlanan günlüğe geçin | Bunu ne tespit eder? |
| --- | --- |
| Kaydedilmiş hash değerini koruyarak 2 numaralı kaydı değiştir | Yeniden hesaplanan olay hash değeri farklıdır; imzası artık değiştirilen olayı kapsamamaktadır |
| Değiştirilmiş kaydı ve sonraki tüm hash değerlerini yeniden oluşturun | Orijinal imzalar geçersiz; etkilenen sınırda tutulan bir kontrol noktası da uyuşmuyor |
| Son eki kaldırın, ancak kalan önek kısmını olduğu gibi bırakın | Verilen önekten daha önceki bir kontrol noktası, dışa aktarılan verinin çok kısa olduğunu ortaya koymaktadır |
| Yedek günlüğü başka bir anahtarla yeniden imzalayın | Ayrı olarak güvenilen bir anahtar parmak izi, değiştirilen kimliği reddeder |

![Kaydedilmiş bir alanın değiştirilmesi, o alanın özetini değiştirir; hash değerlerinin yeniden hesaplanması, orijinal imzaları geri getirmez.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**2 numaralı kayıttaki mantığı deneyin:** kaydedilmiş olayda `Meet at 11:00`'yi `Meet at 12:00` olarak değiştirin. Yeniden hesaplanan hash değeri artık eşleşmiyor. Sonraki zinciri yeniden hesaplamak bağlantılarını onarabilir, ancak orijinal imzaların yeni özetleri kapsamasını sağlayamaz. Buna karşılık, gözlemlenen bir Telegram düzenlemesi yeni bir günlük kaydı haline gelir.

[Statik değişiklik şeması](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Sadece hash bağlantıları, birinin yedek zinciri yeniden hesaplamasını engellemez. Güven, bağımsız olarak güvenilir bir anahtar altında imzaların kontrol edilmesinden ve toplayıcı dışında saklanan referanslarla karşılaştırılmasından kaynaklanır.

## Önceki kontrol noktasının eklediği unsurlar

![3 numaralı satırı ve h3 başlığını koruyun; 4 kaydın daha sonraki dışa aktarımı 3. konumda kontrol edilir.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**Günlük büyürken referans sabit kalır.** Kontrol noktasında “3 kayıt, başlık h3” yazıyorsa, dört kayıtlık bir dışa aktarım, 3. konumdaki h3 ile eşleşerek geçebilir. En yeni başlığı h4’tür ve bunun farklı olması beklenir. Yalnızca iki kayıtlık bir dışa aktarım başarısız olur.

[Statik kontrol noktası şeması](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Kontrol noktası imzasını doğruladıktan sonra şunları talep edin:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Bir dışa aktarım, bir kontrol noktasının ötesine uzanabilir. Saklanan sınırda tutarlı olması gerekir. Gerçek doğrulayıcı ayrıca her olayın sırasını, önceki bağlantısını, hash değerini ve imzasını da kontrol eder. Yalnızca son saklanan başlığı karşılaştırmak, kaydedilen hash değeri güncellenmemiş olan değiştirilmiş bir iç kaydı gözden kaçırabilir.

## Bir tanığın yeri

Akış şeması · Toplayıcı / hesap oturumu / anahtar A → Salt okunur kontrol noktası uç noktası; Witness / sabitlenmiş toplayıcı anahtarı / kendi anahtarı B → Ayrı imzalı tanık günlüğü; Witness / sabitlenmiş toplayıcı anahtarı / kendi anahtarı B → Salt okunur kontrol noktası uç noktası (Kontrol talebinde bulunun); Salt okunur kontrol noktası uç noktası → Witness / sabitlenmiş toplayıcı anahtarı / kendi anahtarı B (İmzalı cevap); Witness / sabitlenmiş toplayıcı anahtarı / kendi anahtarı B → İmzalı TGW1 gönderilerinin yer aldığı kanal (Bot API / kendi token'ı) · Sunucu A · Sunucu B · Toplayıcı / hesap oturumu/ anahtar A · Salt okunur kontrolnoktası uç noktası · Witness / sabitlenmiştoplayıcı anahtarı / kendianahtarı B · Ayrı imzalı tanık günlüğü · İmzalı TGW1 gönderilerininyer aldığı kanal · Kontrol talebinde bulunun · İmzalı cevap · Bot API / kendi token'ı

**Diyagramın metin olarak gösterimi**

1. Toplayıcı / hesap oturumu / anahtar A → Salt okunur kontrol noktası uç noktası
2. Witness / sabitlenmiş toplayıcı anahtarı / kendi anahtarı B → Ayrı imzalı tanık günlüğü
3. Witness / sabitlenmiş toplayıcı anahtarı / kendi anahtarı B → Salt okunur kontrol noktası uç noktası (Kontrol talebinde bulunun)
4. Salt okunur kontrol noktası uç noktası → Witness / sabitlenmiş toplayıcı anahtarı / kendi anahtarı B (İmzalı cevap)
5. Witness / sabitlenmiş toplayıcı anahtarı / kendi anahtarı B → İmzalı TGW1 gönderilerinin yer aldığı kanal (Bot API / kendi token'ı)

Tanık, geri alma işlemlerini, aynı sayımda farklı bir başlık, değiştirilen anahtarlar, geçersiz cevaplar ve eksik yanıtları kaydeder. Yalnızca sayının daha büyük olması, daha önceki tüm kayıtların değişmeden kaldığını kanıtlamaz; dışa aktarılan verileri saklanan kontrol noktalarıyla karşılaştırın. Başka bir sunucudaki tanık, toplayıcının sunucusundaki kesintilerden etkilenmez; ayrı bir operatör ise ek bağımsızlık sağlar.

Witness, toplayıcının bildirdiği günlük durumunu doğrular. Tüm Telegram mesajlarını bağımsız olarak gözlemlemez. [Witness kurulumuna](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/) bakınız.

## Bilinen eylemler karşısında test uygulaması

Kontrollü bir grup, ayrı toplama hesapları ve yeni bir işaretleyici kullanın. Mesajları kasıtlı olarak gönderin, düzenleyin ve silin; aşamalar arasında kayıtların doğru yapıldığını kontrol edin. Sonuçları incelemeden önce beklenen eylemleri ve bir sonlandırma noktasını belirleyin.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Yalnızca beklenen eylemler sayılır; yinelenen makbuzlar payı artırmaz. Payda sıfırdan farklı olmalıdır. Eksik bir makbuzun ölçülen gecikmesi yoktur. Zaman belirsizliğini belgelendirin; Telegram kesin silme zamanını sağlamadığından, kendi kontrollü silme eylem zamanınızı kullanın. 5/6 (83,3%) gibi bir sonuç, test eylemlerini açıklar; tüm Telegram trafiğinin eksiksizliğini değil.

## Bir iş akışı seçin

Bir kanal, grup, bot ve özel sohbet üzerinden yaşanan bir olayı kapsayan [eksiksiz soruşturma kılavuzu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/investigation/):

1. Tüm hesap Soruşturma modunu etkinleştirin ve erişilebilir tüm sohbetleri listeleyin.
2. Günlük anlık görüntülerini, sohbet başına tam geçmişi ve saklanan ekleri elde edin.
3. Canlı değişiklikleri ve panel ile yapılan tüm kasıtlı etkileşimleri, ilgili makbuzlarıyla birlikte saklayın.
4. Alıntılanan kayıtlar ve kişi profilleri aracılığıyla sayısal gönderen kimliklerini, yanıt ilişkilerini, tekrarlanan alıcıları ve dosya hash değerlerini takip edin.
5. Zaman damgaları ve açık boşluklar içeren, farklı sohbetler arası bir zaman çizelgesini yeniden oluşturun.
6. Diğer hesap çalışma alanlarını karşılaştırırken, bunların kaynaklarını ve anahtarlarını ayrı tutun.
7. İmzalı günlükleri, profilleri ve geçmiş verilerini vaka notlarıyla bir araya getirin ve doğrulayın.

Web sitesindeki `/docs/cases/` kılavuzu, etkileşimli bir vaka haritası ile bot anlaşmazlıkları, silinen mesajlar ve isim değiştiren katılımcılar için çeşitli senaryolar içerir. Vaka notları ve çalışma alanları arası analizler harici kaynaklardan sağlanır; uygulama, otomatik olarak genel bir soruşturma grafiği veya birleştirilmiş bir vaka arşivi oluşturmaz.

[Tamamlanan doğrulama ve kalan işler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) · [Dışa aktarma ve doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#investigation-handoff) · [Bir hesapla başlayın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/)
