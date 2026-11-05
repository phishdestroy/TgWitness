# Mesajlar değişir． Gördüklerinizi saklayın．

Canonical page: https://phishdestroy.github.io/TgWitness/tr/

[Açık kaynak ／ v0.9.1](https://phishdestroy.github.io/TgWitness/tr/docs/reference/changelog/)

Telegram sohbetlerini her düzenleme ve silmeyle birlikte kaydedin， sonra herkesin doğrulayabileceği bir kayıt teslim edin．

[Demo＇yu açın](https://phishdestroy.github.io/TgWitness/demo/?lang=tr)[Kurulum kılavuzu](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr)

Kurgusal veriler， Telegram girişi yok．

 [GitHub Actions ile kayıt （önizleme）](https://phishdestroy.github.io/TgWitness/tr/docs/capture/) [S3 dış sunucu kopyası： kurulum ve kurtarma](https://phishdestroy.github.io/TgWitness/tr/#s3)

ZAMANIN ÖTESİNE UZANAN BİR MESAJ ＃0042

Northstar · AraştırmaKurgusal kaynak ／ mesaj 42

1. **Gözlemlenen mesaj：**09：41：02

   Brifing 14：00 adresinde başlıyor．
2. **Düzenleme korunmuştur**09：43：18

   Brifing 15：00 adresinde başlıyor．

   Önceki sürüm korunmuştur
3. **Silme bildirimi**10：06：45

   Kaydedilen içerik günlüğünüzde kalır．

Üç gözlem． Tek tarihçe．ÖRNEK

Mesaj kaybolur． Kaydedilen geçmiş kalır．

## Kaydedilen her değişiklik． Tam da ihtiyacınız olduğu yerde．

Gerçek arayüz， uydurma verilerle．

TgWitness ／ Kaydedilen sohbetlerGÖZLEM ÇALIŞMA ALANINIZ

![Koyu temada kaydedilmiş Telegram sohbetleri； yakalanan düzenlemeler ve silinen mesajlar bağlam içinde korunur](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Kaydedilen sohbetler Normal bir sohbet gibi görünür； düzenlemeler ve silmeler mesajların hemen yanında．

TgWitness ／ GünlükYEREL ÇALIŞMA ALANI

![Gözlemlenen mesajlar， düzenlemeler， silme bildirimleri ve kapsama olaylarını içeren günlük](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Günlük Hesabınızın gördüğü her şey， aranabilir， boşluklar dahil．

TgWitness ／ Düzenleme geçmişiYEREL ÇALIŞMA ALANI

![Bir mesajın yakalanan önceki ve düzenlenmiş sürümlerini karşılaştıran ayrıntı penceresi](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Düzenleme geçmişi Eski ve yeni sürüm yan yana， hiçbir şeyin üzerine yazılmaz．

TgWitness ／ İmzalı dışa aktarımlarYEREL ÇALIŞMA ALANI

![Çalışma alanını， imzalı ZIP， JSONL， CSV ve çevrimdışı HTML raporu olarak dışa aktarma özelliği](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ İmzalı dışa aktarımlar Günlüğü yanınızda götürün； imzalı ve kendi doğrulayıcısıyla．

[Case Board](https://phishdestroy.github.io/TgWitness/tr/docs/case-board/)， [rapor tasarımı](https://phishdestroy.github.io/TgWitness/tr/docs/reports/) ve [paylaşım kopyası](https://phishdestroy.github.io/TgWitness/tr/docs/handover/) aracılığıyla kaydedilmiş bir kaydı takip edin． [Hesap gruplarını](https://phishdestroy.github.io/TgWitness/tr/docs/groups/) birlikte [inceleyin](https://phishdestroy.github.io/TgWitness/tr/docs/groups/)．

01 ／ KAYIT

### Kapsamı siz belirlersiniz．

Birkaç sohbet， bir klasör ya da tüm hesap． Her hesabın kendi çalışma alanı vardır．

[Toplama modlarını karşılaştırın](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#scope)

02 ／ KORUMA

### Değişiklikler hikayeye değer katar．

Sürümler， silmeler ve boşluklar günlükte kalır．

[olay matrisine bakın](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#events)

03 ／ DEVİR

### Yol alan bir kayıt．

İmzalı ZIP， dosyalar ve çevrimdışı rapor． Parola isteğe bağlı．

[＇yi dışa aktarın ve doğrulayın](https://phishdestroy.github.io/TgWitness/tr/docs/exports/)

## Bir baytı bile değiştirmeyin．
Doğrulama sistemi size bunu bildirir．

Her olay bir önceki hash değerine bağlanır ve bir Ed25519 imzası taşır．

![Kaydedilen olaylar önceki hash değerlerine bağlanır， imzalar içerir ve doğrulanabilir bir dışa aktarım biçiminde aktarılır．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Kaydedilen bir kaydın değiştirilmesi， o kaydın hash değerini değiştirir ve bağlantılı kaydın doğrulanmasını geçersiz kılar．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Ayrı olarak saklanan bir kontrol noktası， alıcının dışa aktarılan günlüğü daha önceki bir gözlemle karşılaştırmasına olanak tanır．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Dosya hash değerinden ayrı olarak saklanan kontrol noktasına kadar olan kontrolleri takip edin．

[Sekiz kanıt seviyesini keşfedin](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#levels)

## Başka birinin gözden geçirmesine hazır．

Mesajlar， dosyalar ve çevrimdışı rapor tek bir imzalı pakette．

[kanıt modelini okuyun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)

tgwitness-evidence.zipİMZALI PAKET

- 01

  Orijinal gözlemlerJSONL kayıtları ＋ CSV tablosu
- 02

  Okunabilir içerikÇevrimdışı HTML raporu ＋ korunmuş medya dosyaları
- 03

  Bağımsız doğrulamaİmzalı manifest ＋ bağımsız doğrulayıcı

Alıcı her şeyi sizin anahtarınızla doğrular； başka yerde saklanan bir kontrol noktası o zamandan beri hiçbir şeyin yeniden yazılmadığını gösterir． [Kontroller nasıl çalışır．](https://phishdestroy.github.io/TgWitness/tr/docs/concepts/#layers)

## S3 kopyaları． Harici kontroller．

Şifrelenmiş kopyaları saklayın ve bağımsız kontroller ekleyin．

Varsayılan olarak kapalı

### Her şeyi S3 uyumlu depolama alanına kopyalayın

Günlük， dosyalar， kontrol noktaları ve sohbet dışa aktarımları S3＇e gitmeden önce şifrelenir．

**Depolama ayarları ve kurtarma**

İstemci tarafında şifreleme

`AES-256-GCM` sizin makinenizde． Sağlayıcı yalnızca şifreli metin görür．

Zamanlanmış veya manuel kopyalama

Şimdi kopyalayın ya da 1－1.440 dakikada bir； ilerleme panelde．

Object Lock

Saklama günlerini ve kipini seçin； panel gerçekten uygulandığını kontrol eder．

Doğrulanmış kurtarma

Anahtarı ayrı tutun． İstediğiniz yerde geri yükleyin； dosyalar yalnızca doğrulamadan sonra çıkar．

![Tam kapsamlı site dışı kopyalama paneli： uç nokta， bölge， depo， erişim anahtarları， zamanlama， Nesne Kilidi ve kurtarma anahtarı denetimleri](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Gelişmiş seçeneklerin de yer aldığı tam panel açılmış haldedir． Depolama kimlik bilgileri gösterilmemektedir．

Dergi ve medya`AES-256-GCM`S3 uyumlu depolama alanı

[S3＇ü yapılandırın ve kopyasını geri yükleyin](https://phishdestroy.github.io/TgWitness/tr/docs/exports/#s3)[Doğrulama ayrıntılarını okuyun：](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Kurtarma anahtarı** Ayrı saklayın； o olmadan kopya okunamaz．

### Bildirimler · Apprise

Sorunlar， sohbet değişiklikleri ve günlük özet； mesajlaşma uygulamalarına， e－postaya ya da kendi webhook＇unuza．

**Neyin paylaşılacağını seçin** Siz açmadıkça mesaj metni gönderilmez．

 [Bildirim hedeflerini yapılandırın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/operations/#notifications)

### Harici zaman damgaları

Zaman damgası kontrol noktası hash＇lerini RFC 3161 ve OpenTimestamps ile oluşturun．

**Sonucu takip edin** TSA yanıtını kontrol edin ya da OpenTimestamps makbuzunu bir Bitcoin kanıtına yükseltin．

 [Zaman damgası kanıtlarını kontrol edin：](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/)

### Bağımsız tanık

Ayrı bir sunucu， imzalanmış gözlemleri saklar ve `TGW1` kontrol noktalarını yayınlayabilir．

**Referansı ayırın** Başka bir sunucuda， kendi anahtarı ve günlüğüyle çalıştırın．

 [Bir tanık oluşturun](https://phishdestroy.github.io/TgWitness/tr/docs/witness/)

### Kurtarma ve göze çarpan eksiklikler

Yeniden başlatmanın ardından devam edin． Yeniden kontrol edin ve `coverage.json` kurtarılan mesajları ve eksiklikleri gösterir．

**Aralığı inceleyin** Kurtarılan mesajlar ve kaydedilen boşluklar yan yana．

 [Sürekliliği ve boşlukları inceleyin](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html#continuity)

## İlk çalışma alanınız burada başlıyor．

Önce demoyu deneyin， hazır olduğunuzda yedek bir hesap bağlayın．
Windows， Linux， macOS veya Docker．

[Kurulum kılavuzunu okuyun](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr)

**İçe aktarılan her oturum için yalnızca bir istemci çalıştırılabilir．**

İçe aktarılmış bir TData＇yı ya da oturumu Telegram Desktop ve TgWitness＇ta aynı anda kullanmayın： Telegram ikisini de geçersiz kılabilir （AUTH_KEY_DUPLICATED）． İkisi de mi lazım？ TgWitness＇a telefon ya da QR ile ayrıca giriş yapın．

[Oturum içe aktarma uyarısını okuyun](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr#session-warning)

**Bağlanmadan önce bir göz atın．**

Telegram hesabı olmadan kurgusal çalışma alanını deneyin．

[Çevrimiçi demoyu aç →](https://phishdestroy.github.io/TgWitness/demo/?lang=tr)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**Yerel kurulum komutları**

ADIM 01

### Kaynağı indirin．

[Kaynak ZIP dosyasını indirip](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) açın veya depoyu klonlayın：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Python 3.11+ gerekir． Windows＇ta başlatıcı kurmayı önerir．

[Sürümleri inceleyin](https://github.com/phishdestroy/TgWitness/releases)

ADIM 02

### Çalıştırma şeklini seçin．

`Start.cmd` dosyasına çift tıklayın veya PowerShell＇de şu komutu çalıştırın：

```
.\Start.cmd
```

Sadece göz atıyor musunuz？ `scripts\Demo.cmd`＇ye çift tıklayarak izole bir demoyu deneyin． Telegram ile giriş yapmanıza gerek yoktur．

Python 3.11+ ve `venv` ile kullanılabilir：

```
sh start.sh
```

Bunun yerine kurgusal günlüğü açmak için `sh start.sh --demo` komutunu çalıştırın．

Docker çalışır durumda ve Compose 2.20+ yüklü olduğunda：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

İkinci komut， özel panel jetonunuzu gösterir． Bunu bilgisayarınızda saklayın．

Başlatma işleminden sonra [127.0.0.1:8787 adresini](http://127.0.0.1:8787) açın．

Kaynaktan kurulumlarda belirteç `data/live/panel-token.txt` içindedir． [my.telegram.org](https://my.telegram.org) üzerinden kendi API çiftiniz isteğe bağlıdır． [Tam kurulum kılavuzu ↗](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/)

**TgWitness 0.9.1** [Yenilikler →](https://phishdestroy.github.io/TgWitness/tr/docs/reference/changelog/) · [Özellikler ve bilinen sınırlamalar →](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/)

## Anlaşılır talimatlar． Yararlı bir sonraki adım．

[Kılavuzları inceleyin ↗](https://phishdestroy.github.io/TgWitness/tr/docs/)

[### Modlar， senaryolar ve kanıt düzeyleri Dört toplama modu． Sekiz doğrulama seviyesi． Davanıza uygun iş akışını bulun．](https://phishdestroy.github.io/TgWitness/tr/guides/modes.html)

[01 ### Bir hesap bağlayın Telefon， QR kodu ve desteklenen oturum içe aktarma özellikleri．](https://phishdestroy.github.io/TgWitness/tr/docs/accounts/)[02 ### Bir proxy seçin Genel MTProxy listeleri veya kendi rotanız．](https://phishdestroy.github.io/TgWitness/tr/docs/proxies/)[03 ### Witness botunu kurun Telegram kanalınızda imzalı kontrol noktaları．](https://phishdestroy.github.io/TgWitness/tr/docs/witness/)[04 ### Dışa aktarma ve doğrulama Kaydedilen geçmişi paylaşın ve bütünlüğünü kontrol edin．](https://phishdestroy.github.io/TgWitness/tr/docs/exports/)

## Arşivi inceleyin．

Geçmiş， kaynaklı yapay zekâ， MCP， OCR ve imzalı webhook＇lar．

[İş akışını keşfedin](https://phishdestroy.github.io/TgWitness/tr/docs/archive/)

## Başlamadan önce．

**Bu sayfa Telegram＇a bağlanıyor mu？**

Hayır． Bu， kurgusal örneklerle statik bir sayfa． Uygulama sizin makinenizde çalışır ve girişi orada yaparsınız．

**Yakalanmadan önce silinen mesajları geri getirebilir mi？**

Hayır． Çalıştığı sürece hesabınızın gördüklerini tutar． Sonraki bir anlık görüntü kaçırılan düzenlemeleri ya da silinen mesajları yeniden oluşturamaz．

**Günlüğümün tamamı şifrelenmiş mi？**

Oturumlar ve anahtarlar evet． Mesajlar ve dosyalar hayır； disk şifrelemesi kullanın． Dışa aktarımlara AES－256 parolası konabilir．

**Bu site Telegram ile bağlantılı mı？**

Hayır． Telethon tabanlı， MIT lisanslı bağımsız bir proje． Kendi hesaplarınızla giriş yaparsınız．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Önce keşfedin． Hazır olduğunuzda kurun．

[Demo＇yu açın](https://phishdestroy.github.io/TgWitness/demo/?lang=tr)[Kurulum kılavuzu](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=tr)
