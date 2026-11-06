# Telegram · Bir hesap grubunu yönetin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/groups/

Birden çok hesabı birlikte yürütün, her biri yine kendi kayıtları ve anahtarıyla.

Bir grup bağlantı durumunu, başlat/duraklat'ı, paylaşılan ayarları ve dışa aktarımları tek ekranda toplar. Birden çok hesap aynı dava üzerinde çalışırken kullanışlıdır.

## Grup genel bakışını açın

Grubu **Hesaplar**'da açın. Her hesap durumunu, rotasını, gecikmesini ve son kaydedilen mesajını gösterir. **İlgi gerekiyor** sorunluları listeler, **Düzelt** sizi doğrudan oraya götürür.

**Tümünü başlat** / **Tümünü duraklat** harekete geçmeden önce sorar. **Grup ayarları** paylaşılır, ama bir hesabın kendi değerleri siz değiştirene kadar kalır.

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

1. **Grup rotasını değiştir**, türü ve ayarları seçin.
2. **Seçimi gözden geçir**: hangi hesaplar değişiyor, hangilerinin kendi rotası var.
3. **Hazırla ve kontrol et** taze bir Telegram bağlantısını ve mümkünse çıkış IP'sini test eder.
4. **Kontrol edilen bağlantıyı uygula** ve her sonuca bakın. Çalışan hesaplar devam eder, boşta olanlar boşta kalır.

Gecikme Telegram bağlantısının kurulma süresidir; çıkış IP'si, rotanın kontrol anında gösterdiğidir. Sonuçlar hesaba göre değişebilir.

## Çakışan erişim kullanın

**Birden çok hesabın gördüğü sohbetler** paylaşılan kaynakları ve kapsamlarını listeler. Kanallar ve süper gruplar **… hesapla dışa aktar** ile birden çok hesapla aynı anda dışa aktarılabilir. Özel sohbetler ve basit gruplar olmaz; oradaki mesaj numaraları hesaba özgüdür.

## Grubu bir paket olarak dışa aktarın

**Grubu dışa aktar**, her hesabın imzalı dışa aktarımını ve bunların imzalı listesini içeren tek bir ZIP verir. Her biri doğrulama için kendi parmak izini korur. Birleşik zaman çizelgesini yine siz kurarsınız.

Sıradaki: [raporlar](https://phishdestroy.github.io/TgWitness/tr/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/tr/docs/case-board/), [dışa aktarımları doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/exports/).
