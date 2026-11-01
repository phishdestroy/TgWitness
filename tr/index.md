# Mesajlar değişir. Gördüklerinizi saklayın.

Canonical page: https://phishdestroy.github.io/TgWitness/tr/

[Açık kaynak / v0.7.1](https://phishdestroy.github.io/TgWitness/tr/docs/reference/changelog/)

Telegram mesajlarını yakalayın, değişikliklerini koruyun ve imzalı bir kayıt olarak dışa aktarın.

[Demo'yu açın](https://phishdestroy.github.io/TgWitness/demo/?lang=tr)[Kurulum kılavuzu](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr)

Demo, hayali veriler kullanmaktadır. Telegram ile oturum açmaya gerek yoktur.

 [GitHub Actions ile kayıt (önizleme)](https://phishdestroy.github.io/TgWitness/tr/docs/capture/) [S3 dış sunucu kopyası: kurulum ve kurtarma](https://phishdestroy.github.io/TgWitness/tr/#s3)

ZAMANIN ÖTESİNE UZANAN BİR MESAJ #0042

Northstar · AraştırmaKurgusal kaynak / mesaj 42

1. **Gözlemlenen mesaj:**09:41:02

   Brifing 14:00 adresinde başlıyor.
2. **Düzenleme korunmuştur**09:43:18

   Brifing 15:00 adresinde başlıyor.

   Önceki sürüm korunmuştur
3. **Silme bildirimi**10:06:45

   Kaydedilen içerik günlüğünüzde kalır.

Üç gözlem. Tek tarihçe.ÖRNEK

Mesaj kaybolur. Kaydedilen geçmiş kalır.

## Kaydedilen her değişiklik. Tam da ihtiyacınız olduğu yerde.

Kurgusal demo verileriyle arayüzü inceleyin.

TgWitness / Kaydedilen sohbetlerGÖZLEM ÇALIŞMA ALANINIZ

![Koyu temada kaydedilmiş Telegram sohbetleri; yakalanan düzenlemeler ve silinen mesajlar bağlam içinde korunur](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Kaydedilen sohbetler Mesajların yanında yakalanan düzenlemeler ve silme bildirimlerinin de yer aldığı, tanıdık bir sohbet görünümü.

TgWitness / GünlükYEREL ÇALIŞMA ALANI

![Gözlemlenen mesajlar, düzenlemeler, silme bildirimleri ve kapsama olaylarını içeren günlük](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Günlük: Kesintiler de dahil olmak üzere, hesabınızın gözlemlediklerinin aranabilir bir zaman çizelgesi.

TgWitness / Düzenleme geçmişiYEREL ÇALIŞMA ALANI

![Bir mesajın yakalanan önceki ve düzenlenmiş sürümlerini karşılaştıran ayrıntı penceresi](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Düzenleme geçmişi: Önceki gözlemi üzerine yazmadan yakalanan sürümleri karşılaştırın.

TgWitness / İmzalı dışa aktarımlarYEREL ÇALIŞMA ALANI

![Çalışma alanını, imzalı ZIP, JSONL, CSV ve çevrimdışı HTML raporu olarak dışa aktarma özelliği](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / İmzalı dışa aktarımlar Günlüğü, bir manifest ve bağımsız bir doğrulayıcıyla birlikte yanınızda taşıyın.

01 / KAYIT

### Kapsamı siz belirlersiniz.

Seçilen sohbetler, bir Telegram klasörü veya tüm hesap. Her hesap için ayrı bir çalışma alanı.

[Toplama modlarını karşılaştırın](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#scope)

02 / KORUMA

### Değişiklikler hikayeye değer katar.

Yakalanan sürümler, silme bildirimleri ve gözlem boşlukları günlüğünde kalır.

[olay matrisine bakın](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#events)

03 / DEVİR

### Yol alan bir kayıt.

İmzalı ZIP dosyası, korunmuş dosyalar ve çevrimdışı rapor. İsteğe bağlı şifre koruması.

['yi dışa aktarın ve doğrulayın](https://phishdestroy.github.io/TgWitness/tr/docs/exports/)

## Bir baytı değiştirin. Zincir size haber verir.

Her olay bir önceki hash değerine bağlanır ve bir Ed25519 imzası taşır.

![Kaydedilen olaylar önceki hash değerlerine bağlanır, imzalar içerir ve doğrulanabilir bir dışa aktarım biçiminde aktarılır.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Kaydedilen bir kaydın değiştirilmesi, o kaydın hash değerini değiştirir ve bağlantılı kaydın doğrulanmasını geçersiz kılar.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Ayrı olarak saklanan bir kontrol noktası, alıcının dışa aktarılan günlüğü daha önceki bir gözlemle karşılaştırmasına olanak tanır.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Her bir doğrulama mekanizmasının neyi belirlediğini ve sınırlarının nerede olduğunu inceleyin.

[Sekiz kanıt seviyesini keşfedin](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#levels)

## Başka birinin gözden geçirmesine hazır.

Gözlemleri, dosyaları ve çevrimdışı bir HTML raporunu tek bir imzalı paket halinde teslim edin.

[kanıt modelini okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)

tgwitness-evidence.zipİMZALI PAKET

- 01

  Orijinal gözlemlerJSONL kayıtları + CSV tablosu
- 02

  Okunabilir içerikÇevrimdışı HTML raporu + korunmuş medya dosyaları
- 03

  Bağımsız doğrulamaİmzalı manifest + bağımsız doğrulayıcı

İmzalar, güvenilir bir anahtara göre tahrifatları tespit eder. Telegram kaynaklı olduğunu kanıtlamazlar veya mesajların eksiksiz olarak kaydedildiğini garanti etmezler. Günlük içeriği ve medya dosyaları için sizin tarafınızdan sağlanacak şifreli depolama alanı gereklidir.

## S3 kopyaları. Harici kontroller.

Şifrelenmiş kopyaları saklayın ve bağımsız kontroller ekleyin.

Varsayılan olarak kapalı

### Her şeyi S3 uyumlu depolama alanına kopyalayın

Günlükler, dosyalar, zaman damgalı kontrol noktaları ve sohbet dışa aktarımları — AWS S3 veya uyumlu bir depolama alanına yüklenmeden önce şifrelenir.

**Depolama ayarları ve kurtarma**

İstemci tarafında şifreleme

`AES-256-GCM`, bu makinedeki nesneleri şifreler. Sağlayıcı, şifrelenmiş nesneleri alır.

Zamanlanmış veya manuel kopyalama

Şimdi kopyalayın veya 1 ila 1.440 dakika arasında bir aralık seçin. Panelde ilerleme durumunu kontrol edin.

Object Lock

Depolama süresi günlerini ve depolama alanı destekliyorsa bir modu seçin. Panel, yüklenen bir nesne için saklama işleminin onaylanıp onaylanmadığını bildirir.

Doğrulanmış kurtarma

Şifreleme anahtarını indirin ve ayrı bir yerde saklayın. Başka bir bilgisayarda geri yükleyin; dosyalar ancak doğrulama işleminden sonra yayınlanır.

![Tam kapsamlı site dışı kopyalama paneli: uç nokta, bölge, depo, erişim anahtarları, zamanlama, Nesne Kilidi ve kurtarma anahtarı denetimleri](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Gelişmiş seçeneklerin de yer aldığı tam panel açılmış haldedir. Depolama kimlik bilgileri gösterilmemektedir.

Dergi ve medya`AES-256-GCM`S3 uyumlu depolama alanı

[S3'ü yapılandırın ve kopyasını geri yükleyin](https://phishdestroy.github.io/TgWitness/tr/docs/exports/#s3)[Doğrulama ayrıntılarını okuyun:](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Ne yapmaz** Dışa aktarılan şifre çözme anahtarı olmadan verileri geri yüklemez veya bağımsız bir tanığın yerini almaz.

### Bildirimler · Apprise

Apprise aracılığıyla sorun uyarıları, sohbet değişiklikleri ve günlük özetler: mesajlaşma uygulamaları, e-posta veya kendi JSON webhook'unuz.

**Yapılmayanlar**: Alıntıları etkinleştirmediğiniz sürece mesaj metnini göndermez.

 [Bildirim hedeflerini yapılandırın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/operations/#notifications)

### Harici zaman damgaları

Zaman damgası kontrol noktası hash'lerini RFC 3161 ve OpenTimestamps ile oluşturun.

**Ne yapmaz** Beklemede olan takvim makbuzu, onaylanmış bir Bitcoin zaman damgası olarak değerlendirilmez.

 [Zaman damgası kanıtlarını kontrol edin:](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/)

### Bağımsız tanık

Ayrı bir sunucu, imzalanmış gözlemleri saklar ve `TGW1` kontrol noktalarını yayınlayabilir.

**Ne yapmaz** Aynı toplayıcı sunucudaki iki çalışma alanını bağımsız tanıklar haline getirmez.

 [Bir tanık oluşturun](https://phishdestroy.github.io/TgWitness/tr/docs/witness/)

### Kurtarma ve göze çarpan eksiklikler

Yeniden başlatmanın ardından devam edin. Yeniden kontrol edin ve `coverage.json` kurtarılan mesajları ve eksiklikleri gösterir.

**Ne yapmaz** Kaçırılan her düzenlemeyi veya kaybolan her mesajı yeniden oluşturmaz.

 [Sürekliliği ve boşlukları inceleyin](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#continuity)

## İlk çalışma alanınız burada başlıyor.

Önce demoyu inceleyin. Hazır olduğunuzda özel bir hesap bağlayın. Windows, Linux, macOS veya Docker.

[Kurulum kılavuzunu okuyun](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr)

**İçe aktarılan her oturum için yalnızca bir istemci çalıştırılabilir.**

İçe aktarılan bir TData/oturum anahtarını Telegram Desktop ve TgWitness'te aynı anda çalıştırmayın. Telegram, paylaşılan yetkilendirmeyi (AUTH_KEY_DUPLICATED) geçersiz kılabilir. Paralel kullanım için, telefon veya QR koduyla ayrı bir TgWitness oturumu oluşturun.

[Oturum içe aktarma uyarısını okuyun](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr#session-warning)

**Bağlanmadan önce bir göz atın.**

Telegram hesabı olmadan kurgusal çalışma alanını deneyin.

[Çevrimiçi demoyu aç →](https://phishdestroy.github.io/TgWitness/demo/?lang=tr)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Yerel kurulum komutları**

ADIM 01

### Kaynağı indirin.

[Kaynak ZIP dosyasını indirip](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) açın veya depoyu klonlayın:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Kaynak kodun çalıştırılması için Python 3.11+ gereklidir. Python yüklü değilse, Windows başlatıcısı kurulum seçeneği sunar.

[Sürümleri inceleyin](https://github.com/phishdestroy/TgWitness/releases)

Windows'ta Python yok mu? [Taşınabilir paketi indirin](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.1/TgWitness-0.7.1-windows-amd64-portable.zip), açın ve `TgWitness.cmd` dosyasına çift tıklayın.

ADIM 02

### Çalıştırma şeklini seçin.

`Start.cmd` dosyasına çift tıklayın veya PowerShell'de şu komutu çalıştırın:

```
.\Start.cmd
```

Sadece göz atıyor musunuz? `scripts\Demo.cmd`'ye çift tıklayarak izole bir demoyu deneyin. Telegram ile giriş yapmanıza gerek yoktur.

Python 3.11+ ve `venv` ile kullanılabilir:

```
sh start.sh
```

Bunun yerine kurgusal günlüğü açmak için `sh start.sh --demo` komutunu çalıştırın.

Docker çalışır durumda ve Compose 2.20+ yüklü olduğunda:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

İkinci komut, özel panel jetonunuzu gösterir. Bunu bilgisayarınızda saklayın.

Başlatma işleminden sonra [127.0.0.1:8787 adresini](http://127.0.0.1:8787) açın.

Kaynak koddan kurulumlarda token `data/live/panel-token.txt`'dir. Telegram oturum açma işlemi için yerleşik API ayarları veya [my.telegram.org](https://my.telegram.org) adresinden aldığınız kendi anahtar çiftinizi kullanabilirsiniz. [Tam kurulum kılavuzu ↗](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/)

**TgWitness 0.7.1** [Yenilikler →](https://phishdestroy.github.io/TgWitness/tr/docs/reference/changelog/) · [Özellikler ve bilinen sınırlamalar →](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/)

## Anlaşılır talimatlar. Yararlı bir sonraki adım.

[Kılavuzları inceleyin ↗](https://phishdestroy.github.io/TgWitness/tr/docs/)

[### Modlar, senaryolar ve kanıt düzeyleri Dört toplama modu. Sekiz doğrulama seviyesi. Davanıza uygun iş akışını bulun.](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html)

[01 ### Bir hesap bağlayın Telefon, QR kodu ve desteklenen oturum içe aktarma özellikleri.](https://phishdestroy.github.io/TgWitness/tr/docs/accounts/)[02 ### Bir proxy seçin Genel MTProxy listeleri veya kendi rotanız.](https://phishdestroy.github.io/TgWitness/tr/docs/proxies/)[03 ### Witness botunu kurun Telegram kanalınızda imzalı kontrol noktaları.](https://phishdestroy.github.io/TgWitness/tr/docs/witness/)[04 ### Dışa aktarma ve doğrulama Kaydedilen geçmişi paylaşın ve bütünlüğünü kontrol edin.](https://phishdestroy.github.io/TgWitness/tr/docs/exports/)

## Arşivi inceleyin.

Geçmişi yükleyin, AI kaynaklarını inceleyin, bir MCP istemcisini bağlayın, kaydedilmiş medya dosyalarını tanıyın ve imzalı webhook'lar gönderin.

[İş akışını keşfedin](https://phishdestroy.github.io/TgWitness/tr/docs/archive/)

## Başlamadan önce.

**Bu sayfa Telegram'a bağlanıyor mu?**

Hayır. Bu, kurgusal örnekler ve ekran görüntüleri içeren statik bir proje sayfasıdır. Asıl uygulama bilgisayarınızda veya sunucunuzda çalışır; oturum açma işlemi de orada gerçekleşir.

**Yakalanmadan önce silinen mesajları geri getirebilir mi?**

Hayır. TgWitness, toplama işlemi devam ederken hesabınızda gözlemlenen içeriği saklar. Daha sonraki bir geçmiş anlık görüntüsü, kaçırılan düzenlemeleri veya silinen mesajları yeniden oluşturamaz.

**Günlüğümün tamamı şifrelenmiş mi?**

Hesap kimlik bilgileri ve imzalama gizli anahtarları şifrelenmiş bir kasada saklanır. Yerel mesajlar ve ekler için şifrelenmiş bir disk veya birim gereklidir. Dışa aktarımlarda isteğe bağlı olarak parola korumalı AES-256 ZIP dosyası kullanılabilir.

**Bu site Telegram ile bağlantılı mı?**

Hayır. TgWitness, MIT Lisansı altında dağıtılan Telethon'u kullanan bağımsız bir projedir. Yerleşik API ayarlarını veya kendi API çiftinizi kullanarak kendi hesaplarınızı yetkilendirirsiniz.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Önce keşfedin. Hazır olduğunuzda kurun.

[Demo'yu açın](https://phishdestroy.github.io/TgWitness/demo/?lang=tr)[Kurulum kılavuzu](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr)
