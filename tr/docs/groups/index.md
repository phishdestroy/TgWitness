# Bir hesap grubunu yönetin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/groups/

Her hesabın kayıtlarını ve imza kimliğini ayrı tutarken, birden fazla toplama hesabını bir arada yönetin.

Bir hesap grubu, bağlantı durumunu, gözlem kontrollerini, paylaşılan ayarları ve dışa aktarmaları tek bir çalışma görünümünde bir araya getirir. Bu özellik, aynı soruşturmayı kapsayan veya tutarlı bir çalışma düzenine ihtiyaç duyan birden fazla hesap olduğunda kullanışlıdır.

## Grup genel bakışını açın

**Hesaplar** bölümünde grubu açın. Her hesap, gözlem durumunu, bağlantı yolunu, son kontrolün başarılı olduğu zamanki en son ölçülen yol gecikmesini ve en son kaydedilen mesajı gösterir. **Dikkat gerektiren** bağlantılar, üzerinde çalışılması gereken hesaplara yönlendirir; **Düzelt seçeneği,** ilgili çalışma alanını ve kontrol panelini açar.

**"Tümünü Başlat**" ve **"Tümünü Duraklat" seçenekleri,** onaylandıktan sonra uygun hesaplar üzerinde işlem yapar. **Grup ayarları,** seçilen ayarları paylaşır; kendi değerlerine sahip hesaplar, siz bunları değiştirmeyi seçene kadar bu değerleri korur.

### Bir grup genelinde yapılan rota değişikliğini gözden geçirin

Örnek metin · açıklayıcı kontroller ve sonuçlar

1. **Seçin.** Grubu seçin ve hangi hesapların değişeceğini gözden geçirin.
2. **Hazırlık.** Ayrı kalması gereken durumlarda hesabın kendi yolunu koruyun.
3. **Kontrol edin.** Önerilen bağlantıyı test edin ve ölçüm sonuçlarını inceleyin.
4. **Başvurun.** Kaydetmeden önce tekrar kontrol edin ve her hesap için sonucu gözden geçirin.

#### Vaka ekibi

Kanal toplayıcı · Grup toplayıcı · Referans hesap

3 ayrı çalışma alanı

#### İncelenen seçim

2 hesap önerilen yolu izler.

Referans hesabı kendi yolunu izler.

#### Hazırlık kontrolleri

Kanal toplayıcı: Telegram aktarım süresi 84 ms

Grup toplayıcı: Telegram aktarım süresi 91 ms

Bu sayılar, örnek amaçlı uydurulmuş ölçümlerdir.

#### Uygulama sonuçları

Kanal toplayıcı: kaydetme işlemi tamamlandı, gözlem devam ediyor.

Grup toplayıcı: yeniden kontrol başarısız, önceki ayarlar geri yüklendi.

Referans hesap: mevcut yol korunmuştur.

## Bir inceleme adımı ekleyerek süreci değiştirin

1. **"Grup rotasını değiştir**" seçeneğini seçin, ardından bağlantı türünü ve ayarları belirleyin.
2. **"Seçimi Gözden Geç" seçeneğini** seçin. Listelenen hesapları ve her birinin rota geçersiz kılma ayarlarını inceleyin.
3. **"Hazırla ve kontrol et"** seçeneğini seçin. Kontrol işlemi yeni bir Telegram aktarımını kullanır; desteklenen HTTP rotaları ayrıca HTTPS çıkış kontrolünü de bildirir.
4. **"İşaretli bağlantıyı uygula"** seçeneğini seçin ve her hesabın sonucunu inceleyin. Daha önce yürütülmekte olan gözlem, uygulamanın başarılı olduğu yerden devam eder; etkin olmayan hesaplar ise etkin olmayan durumda kalır.

Gecikme, ölçülen Telegram bağlantı kurulumunu tanımlar. Çıkış IP kontrolü, kaydedilen kontrol zamanındaki o rotayı tanımlar. Hesap yetkilendirme ve gözlem durumunun kendi göstergeleri vardır; bir grup değişikliği, hesap başına farklı sonuçlarla sonuçlanabilir.

## Çakışan erişim kullanın

**"Birkaç hesap tarafından görülen sohbetler" seçeneği,** paylaşılan kaynakları ve mevcut çalışma alanı gözlem kapsamını gösterir. Uygun kanallar ve süper gruplar, bir sohbetin geçmişini bölmek için **"… hesaplarıyla dışa aktar"** seçeneğini kullanabilir. Özel sohbetler ve normal gruplar, mesaj numaraları bir hesabın geçmişine ait olduğu için başlangıç hesabında kalır.

## Grubu bir paket olarak dışa aktarın

**Dışa aktarma grubu,** her hesabın imzalanmış dışa aktarımını ve bu dosyaların imzalanmış bir listesini içeren tek bir ZIP dosyası oluşturur. Orijinal çalışma alanı kimlikleri ve parmak izleri, doğrulama amacıyla kullanılabilir durumda kalır. Bu referansları kullanarak hesaplar arası bir anlatı oluşturun; tek bir birleştirilmiş zaman çizelgesi yine de ayrı olarak derlenir.

[Rapor tasarımı](https://phishdestroy.github.io/TgWitness/tr/docs/reports/), [çalışma alanı içindeki bir Case Board](https://phishdestroy.github.io/TgWitness/tr/docs/case-board/) veya [dışa aktarma doğrulaması](https://phishdestroy.github.io/TgWitness/tr/docs/exports/) ile devam edin.
