# İlk kurulum ve ayarlar

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/settings/

Kurulum sihirbazı, hedefler, arayüz seviyeleri, bağlantı yolları ve bir hesap grubu tarafından paylaşılan ayarlar.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Başlangıç](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/)

![Başlangıç](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Hesaplar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) · [Bağlantı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/) · [Erişim](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/)

Yeni bir çalışma alanı açılır `/first-run`: dil ve saat, arayüz seviyesi, hedef, bağlantı, Telegram ve sohbetler. Her cevap, değiştiği anda sunucuya kaydedilir, böylece sayfayı yeniden yüklediğinizde aynı adımdan devam edersiniz. Son ekranda cevaplar listelenir ve bunlardan herhangi birine geri dönmenize olanak tanır.

Dil, IANA saat dilimi, tema ve seviye, operatör ve çalışma alanı bazında saklanır. Varsayılan ayarlar, tarayıcı dili, cihazın saat dilimi, sistem teması ve Basit arayüzdür. Dil değiştirildiğinde panel oturumu korunur. İmzalanmış günlükteki saatler asla değişmez.

`/settings` Sihirbazla aynı kayıtları düzenler. Arama, ana alanları, parametreleri ve genişletilmiş formları kapsar; gizli bir alan, seviye değiştirilmeden açılabilir. Seviyeler yalnızca görüntülenenleri değiştirir: sunucu, izinleri kendi başına kontrol eder. Koleksiyon ayarları ve ilk bağlantı, çalışma alanı yöneticisine aittir.

| Seviye | Alanlar | Kenar Çubuğu |
| --- | --- | --- |
| Basit | Sadece gerekli olanlar | Ana Sayfa, Sohbetler, Değişiklikler, Arşivler, Ayarlar |
| Standart | Açıklamalı genel ayarlar | Case Board, Hesaplar ve Erişim bölümleri eklenmiştir |
| Uzman | Tüm alanlar, sınırlar ve teknik ayrıntılar | Kaynaklar, Ekstralar, Arşive Sor, Parametreler, Hesap, Sistem günlüğü ve Entegrasyonlar eklenmiştir |

[Panel kılavuzu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/), her bir bölümü açıklamaktadır.

## Hedefler

| Hedef | Koleksiyon | Dosyalar | Dış hizmetler | Sunucu adresi |
| --- | --- | --- | --- | --- |
| Arşiv kopyası | Kapalı; **Başlat,** bir dışa aktarma işlemi başlatır | 20 MB'a kadar fotoğraflar | Kapalı | Otomatik |
| Sohbetleri takip et | Sürekli | 60 saniyeye kadar olan fotoğraflar ve videolar / 20 MB | Zaman damgaları ve sorun bildirimleri | Otomatik |
| Kanıt | Sürekli | 1 GB'a kadar tüm dosyalar | Zaman damgaları, drand, bildirimler | Hayır, gizle |

Kanıt amaçlı olarak site dışı kopya, tanık botu ve kod kontrolü önerilir. Depolama ve bildirim adresleri için önce bir hedef belirlenmesi gerekir. Dışarıdaki bir hizmetle iletişim kuran bir özellik, Telegram dışındaki isteklerin izin verilmesini ister; bu özelliği kapatmak, zaman damgalarını, bildirimleri ve site dışı kopyayı da devre dışı bırakır.

Hedefi değiştirdiğinizde önce farklar gösterilir ve manuel değişiklikler korunabilir. Hedeften farklı olan bir alan, "**Sizin tarafınızdan değiştirildi"** olarak işaretlenir ve geri yüklenebilir. Ayar revizyonu, gözden geçirilmiş bir farkın başka bir sekmede yapılan bir değişikliğin üzerine uygulanmasını engeller.

## Bağlantı

**Automatic**, önce genel MTProxy sunucularını, ardından WARP'ı ve son olarak doğrudan bağlantıyı dener; doğrudan bağlantı, yalnızca sunucunun adresinin gösterilebilmesi durumunda kullanılır. Automatic ve WARP, hash kontrollü bileşenleri yükleyebilir ve sunucuyu Cloudflare'e kaydedebilir. WARP, mevcut wgcf/wireproxy yöneticisini ve yerel bir SOCKS5 bağlantı noktasını kullanır; sistem yönlendirme tablosu değiştirilmez. Dış hizmetlere ihtiyaç duyulduğunda, Automatic MTProxy yerine WARP'ı tercih eder.

Kendi proxy'niz `tg://proxy`, `socks5://`, `http://` ve `https://`. Bir HTTPS proksisinin sertifikası, kimlik bilgileri ona gönderilmeden önce kontrol edilir.

Bağlantı kontrolü beş dakika geçerlidir ve rotaya, politikaya ve sihirbazın yanıtlarına bağlıdır; bunlardan herhangi birinde değişiklik yapılması durumunda yeni bir kontrol gerekir. **Kontrol etmeden devam etme** seçeneği mevcuttur ve bu, Telegram oturum açma işleminin yerini almaz. Seçilen rota arka planda yeniden kontrol edilir ve bağlantı kesildiğinde Automatic, zincirini yeniden çalıştırır. Hiçbir genel proxy yanıt vermediğinde, sayı kırmızıya döner ve WARP ile yeniden kontrol işlemleri başlatılır.

## Hesap grupları

Bir gruptaki hesaplar ayarlarını paylaşır. **Hesaplar → Gruplar ve paylaşılan ayarlar → Paylaşılan ayarlar seçeneğini** açın veya bir hesabın Ayarlar sayfasındaki **Grup ayarları seçeneğine gidin**.

Grup, hedefi, kaydedilmiş dosyaları, zaman damgalarını, drand'ı, sorun bildirimlerini, site dışı kopyayı, Telegram dışındaki istekleri, IP modunu, neyin kaydedileceğini, yeniden kontrol programını, bildirim kurallarını, rapor ayarlarını, parametreleri ve bağlantı yolunu paylaşır. Bildirim hedefleri, proxy kimlik bilgileri ve oturum açma bilgileri, toplamanın başlatılması ve duraklatılması gibi işlemler de her hesap için ayrıdır.

- Her üye grubu takip eder. Ayarlar, bir değeri işaretler 🔗 **Gruptan** veya ✏️ **Kendi değeri**; **Grup değerine dön seçeneği,** değeri eski haline getirir.
- Bir değişiklik, etkilediği hesapları listeler (**3 hesaptan 2'sine uygulanır**) ve kendi değerini değiştirmeden önce her hesap için onay ister. İşareti kaldırılmış hesaplar kendi değerlerini korur.
- Grubun paylaşmadığı bir parametre, siz **Bu değeri paylaş** tuşuna basana kadar **Paylaşılmaz: her hesap kendi değerini korur** olarak kalır.
- **Bir hesaptan ayarları kopyalamak,** seçilen hesabın değerlerini grubun ayarları olarak alır.
- Bir gruba taşınan hesaba **“Grubun değerlerini kabul etmek ister misin?”** sorusu sorulur. Aksi takdirde, ✏️ işaretiyle belirtildiği üzere kendi değerlerini korur. Daha sonra eklenen hesaplar ise grubun değerleriyle başlar.
- Gözlemci hesap, duraklatılana kadar IP modunu korur.

Her değişiklik, ana çalışma alanının ve ulaşılan her üyenin imzalı günlüğüne kaydedilir. Bir grubun silinmesi, grubun hesaplarını ve bunların güncel değerlerini korur.

Grup sayfası `/groups/<id>` üyeleri, dikkat edilmesi gerekenleri ve birkaç hesabın görebildiği sohbetleri gösterir. [Hesap gruplarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#bulk-import-and-account-groups) bakın.

## Mevcut çalışma alanları

Bir oturum içeren veya daha önce kurulumu tamamlanmış bir çalışma alanı, sihirbazı göstermez. Sayfa yüklendiğinde bu alanların değerleri bir hedefle değiştirilmez. Bir alanı gizlemek, özelliği devre dışı bırakmaz veya değerini silmez.

Boyut ve süre tahmini, seçilen en fazla üç sohbeti ve her birinden en fazla 20 mesajı okur. Bu bir tahmindir: Telegram sınırlarını, belirli bir sunucunun hızını veya her sohbetteki dosyaları öngörmez.
