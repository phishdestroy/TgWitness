# Halka açık vitrin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/showcase/

Seçilen genel kanalların kaydedilmiş mesajlarını ve imzalanmış anlık görüntüleri, süresi dolan ve iptal edilebilir bağlantılar aracılığıyla yayınlayın.

**Erişim → Genel vitrin**, mevcut erişim jetonu sistemini kullanarak ayrı, salt okunur bir sayfa oluşturur. Kurulumun kaydedilmiş gözlemlerini okur. Ziyaretçi için bir toplayıcı başlatmaz, Telegram’da oturum açmaz veya bir kanal edinmez.

## Sayfa yayınla

1. Göstermek istediğiniz her bir genel kanal için bir kaynak profili kaydedin. Bir kanalın en son kaydedilmiş profilinde genel bir kullanıcı adı bulunmalıdır; gruplar ve özel sohbetler bu amaç için uygun değildir.
2. Açık **Erişim → Genel sergi** (veya `/showcase-manage.html`) yönetici olarak.
3. En fazla 16 çalışma alanından kanalları seçin, genel sayfa başlığını girin ve bağlantının geçerlilik süresini 1, 7 veya 30 gün olarak seçin. Çalışma alanı içi etiketler yayınlanmaz. En fazla 64 kanal eklenebilir.
4. Yayınlanacak seçili kanalların metnini gözden geçirin, ardından **Seçili kayıtları önizle'yi** tıklayın. Önizleme, ziyaretçi sayfasıyla aynı sunucu tarafı projeksiyonunu kullanır.
5. **"Vitrin oluştur" bağlantısını** tıklayın. Bağlantı ekranda görünürken kopyalayın. Dağıtmadan önce alıcının sayfasını incelemek için bağlantıyı ayrı bir tarayıcıda açın.

Bağlantının URL parçacığında bir erişim jetonu bulunur. Sayfa, API istekleri yapmadan önce bu parçacığı kaldırır ve onu bir tarayıcı oturumu ile değiştirir. Bağlantıya sahip olan herkes, geçerlilik süresi dolana veya iptal edilene kadar seçilen materyali açabilir. Yeni bağlantılar, her biri en fazla bir saat süren 100 eşzamanlı oturuma izin verir. Mevcut erişim denetimleri, grant API’si aracılığıyla adres kısıtlamaları ve oturum açma sınırlamaları da uygulayabilir. Normal gözden geçiren erişimi farklı bir moddur ve yine de orijinal izin verilen mesajları ve dosyaları içerir.

## Ziyaretçilerin gördükleri

| Görünür | Özel tutulur |
| --- | --- |
| Seçilmiş genel kanal başlıkları, kullanıcı adları ve profil gözlem tarihleri | Hesap kimlikleri, dahili çalışma alanı etiketleri ve seçilmemiş kaynaklar |
| Yakalanan metin ve kaydedilen her düzenleme | Yapılandırılmış gönderen kimlikleri, isimler, kullanıcı adları, telefon numaraları ve profil değerleri |
| Varsa, önceden kaydedilmiş metinle birlikte silme gözlemleri | Ekler, avatarlar, küçük resimler, dosya adları ve orijinal veriler |
| Bir yazar/profil veya ekin kaydedildiğini belirten işaretçiler | Yönlendirme ve yanıt meta verileri, ağ yolları, IP adresleri ve kimlik bilgileri |
| Seçilen kanallardaki olay sayıları, mevcut koleksiyon anahtarları, kalp atışı ve kontrol noktası aralığı | Koleksiyon denetimleri ve standart kanıt dışa aktarma API'leri |
| İmza parmak izi, günlük kontrol noktası ve tutarlılık kanıtı | İmza anahtarları ve Telegram oturumları |

**Halka açık mesaj metinleri otomatik olarak anonimleştirilmez.** Mesaja yazılan bir isim, etiket, telefon numarası veya bağlantı, o metnin bir parçası olarak kalır. `Redacted`Bu, yapılandırılmış yazar/profil alanları için geçerlidir. Yayınlamadan önce, korunan düzenlemeler ve silme işlemleri de dahil olmak üzere, seçilen içeriği gözden geçirin.

Uygunluk durumu, canlı bir Telegram aramasını değil, **en son kaydedilen kaynak profil**ini yansıtır. Sonraki bir profilde artık herkese açık kanal kullanıcı adı bulunmuyorsa, yeni istekler bu kanalı hariç tutar. Herkese açık görünürlük değiştiğinde kaynak profillerini yenileyin. Okuyucular, daha önce aldıkları materyalleri zaten kaydetmiş olabilir.

Orijinal imzalı kayıtlar değişmeden kalır. Görüntülenen yansıma ayrı olarak imzalanır ve orijinal kayıtlara referans veren hash değerleri içerir. Bir yansıma imzası, görüntülenen beyanın doğruluğunu teyit eder; bu, sansürlenmiş baytlar üzerinde orijinal olayın imzası değildir.

## İmzaları ve sürekliliği kontrol edin

**"Parmak İzi ve imzalı kontrol noktası**"nı genişletin ve bir anlık görüntüyü indirin. Sayfa yenilendikten sonra, indirilen dosyaya önceki tarayıcı anlık görüntüsü ve günlük sınırları arasındaki bir Merkle tutarlılık kanıtı da dahil edilir. Otomatik yenileme, sayfa görünür durumdayken ve gözlemlerin ilk sayfasını gösterirken dakikada bir gerçekleşir.

TgWitness'nin kurulumundan sonra, indirilen dosyayı çevrimdışı olarak doğrulayın:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

Parmak izi, ayrı olarak güvenilir bir kaynaktan gelmelidir. Kendi elinizde sakladığınız bir anlık görüntüyle karşılaştırmak için `--previous earlier.json`; bu, indirme dosyası içinde bulunan önceki anlık görüntüyü geçersiz kılar. Mevcut kanıt, saklanan sınırdan başlamalıdır. Kimliği doğrulanmış istemciler, `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`kullanarak bu kanıtı talep edebilir. Daha kısa bir günlük, sınırı sessizce sıfırlamak yerine HTTP 409 yanıtı döndürür.

İmzalanmış kontrol noktası, kayıt sayısı ve opak başlık hash'i dahil olmak üzere **tüm toplayıcı**günlüğüne kaydedilir. Görüntülenen mesaj sayıları yalnızca seçilen genel kanallara uygulanır. Sayfa, diğer günlüklerin içeriğini asla listelemez. Bunlar olay sayılarıdır, benzersiz mesaj sayıları değildir. Ayarlar, önceki tüm kayıt aralıklarını değil, mevcut yapılandırmayı açıklar.

İmza ve tutarlılık doğrulaması, saklanan bir sınırla ilişkili değişiklikleri tespit edebilir. İmzalanmış sayaçları bağımsız olarak yeniden saymaz, Telegram kaynağını onaylamaz, kesintisiz yakalama işlemini kanıtlamaz veya bağımsız bir tanığın yerini almaz. Bu inceleme için [kanıt doğrulayıcıyı](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [bağımsız tanığı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/) ve [test edilmiş ölçekli kaydı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) kullanın. Sentetik kurulumlar, görünür şekilde "sentetik" olarak etiketlenir.

## Sayfayı iptal et veya barındır

Vitrin yöneticisindeki **Revoke (İptal Et)** seçeneğini veya mevcut **Access (Erişim)** bölümünü kullanarak bağlantıyı kapatın ve tüm oturumlarını sonlandırın. Bir istek, erişimin sona erdiğini algıladığında ziyaretçi, görüntülenen kayıtları siler. Her istek sırasında son kullanma tarihi ve izinler kontrol edilir. Vitrin izinleri, yerinde sıradan panel erişimine dönüştürülemez; modları değiştirmek için yeni bir izin oluşturun.

Sayfayı, kurulumun mevcut HTTPS adresi üzerinden sunun. Bir bağlantının yayınlanması yeni bir bağlantı noktası açmaz, tünel oluşturmaz veya DNS'yi değiştirmez. HTML ve API kullanıcının kurulumunda kalır. Vitrin ziyaretçisi, bu erişimle normal mesaj, profil, medya, dışa aktarma veya yönetim API'lerini kullanamaz.
