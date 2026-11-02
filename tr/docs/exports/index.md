# Dışa aktarma ve doğrulama

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/exports/

Alıcıya, toplama çalışma alanı ve kaydedilmiş geçmişiyle karşılaştırarak kontrol edebileceği dosyalar sağlayın.

Referansı saklayınİmzalı ZIP dosyasını dışa aktarAlıcı doğrular

İmzalar ve kontrol noktaları konusunda yeni misiniz? [Örnek bir kaydı değiştirin](https://phishdestroy.github.io/TgWitness/tr/docs/concepts/#chain) ve hangi kontroller tarafından tespit edildiğini görün.

Bir kopyayı veri toplayıcıdan uzak tutmak mı istiyorsunuz? [S3 kurulumu](https://phishdestroy.github.io/TgWitness/tr/docs/exports/#s3), [Nesne Kilidi](https://phishdestroy.github.io/TgWitness/tr/docs/exports/#s3-retention) veya [doğrulanmış kurtarma](https://phishdestroy.github.io/TgWitness/tr/docs/exports/#s3-restore) bölümlerine gidin.

## Güvenilir bir kaynak olarak kalın

Çalışma alanının açık anahtar parmak izini toplayıcı dışında saklayın. Toplama işlemi sırasında, imzalı kontrol noktalarını başka bir yerde tutun veya [bağımsız bir tanık](https://phishdestroy.github.io/TgWitness/tr/docs/witness/) kullanın. Bu referanslar, alıcının anahtarı ve önceki günlük sınırını kontrol etmesini sağlar.

## İmzalı ZIP dosyasını indirin

**"Exports" bölümünü** açın ve imzalı bir delil ZIP dosyası oluşturun. Bu dosya, çalışma alanının tam günlüğünü ve imzalı bir dosya manifestosunu içerir. Okunabilir bir rapor oluşturmak için [Report Studio'yu](https://phishdestroy.github.io/TgWitness/tr/docs/reports/) kullanın veya yalnızca seçilen, en aza indirgenmiş verileri sunmak için bir [devir özetini](https://phishdestroy.github.io/TgWitness/tr/docs/handover/) kullanın.

HTML, PDF ve JSON raporları kendi imzalı mühürlerini taşır ve ayrı ayrı kontrol edilebilir. CSV, analiz için kullanışlı bir kopyadır; bütünlüğünü kontrol etmek için doğrulanmış ZIP dosyasının içindeki tam CSV dosyasını kullanın. Alıcının kaynak kayıtlara ve ek dosyalara da ihtiyacı varsa, imzalı ZIP dosyasını saklayın.

## TgWitness'in güvenilir bir kopyasıyla doğrulayın

Yüklü proje ortamında, örnek parmak izini ve dosya yollarını değiştirin:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Her iki referans da geçerli olduğunda, sonuçta `key_pinned: true` ve `checkpoint_checked: true` raporlanır. Doğrulama sonucunu orijinal arşivle birlikte saklayın. Saklanan kontrol noktası, dışa aktarım sınırında veya öncesinde olmalıdır.

## Doğrulama sonucunu kullanın

- **Teslim edilen dosyaları kontrol edin:** manifest, dosyaların hash değerlerini birbirine bağlar; kayıt imzaları ise kaydedilen günlüğü birbirine bağlar. Değiştirilmiş bir dosya veya bozuk bir kayıt zinciri tespit edilir.
- **Çalışma alanı kimliğini kontrol edin:** bağımsız olarak saklanan parmak izi, beklediğiniz imza anahtarını doğrular.
- **Daha önceki bir sınırlamayı karşılaştırın:** saklanan bir kontrol noktası, aktarımdan önce kaydedilen bir günlük önekiyle karşılaştırarak dışa aktarımı kontrol eder.
- **Toplama kapsamını gözden geçirin:** eksiklikler, toplama sonuçları ve kontrollü bir "gönder → düzenle → sil" testi, bu kurulumun yakaladığı olayları açıklar.

Bu sonuçları alıcının kopyasıyla birlikte saklayın. [Doğrulamanın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope), kontrollerinin kapsamı ile kaynak iddialarının ve toplama kapsamının ayrı ayrı değerlendirilmesi açısından [neyi belirlediğine](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) bakın.

## S3 dış sunucu kopyasını kurun

Çalışma alanınızda, **Dışa Aktarımlar → Site dışı kopya seçeneğini** açın. Bu isteğe bağlı özellik, AWS S3 ve diğer S3 uyumlu hizmetlerle çalışır. Günlük bölümlerini, saklanan fotoğrafları ve dosyaları, zaman damgası yanıtlarıyla birlikte kontrol noktalarını ve tamamlanmış sohbet dışa aktarımlarını kopyalar. Her nesne, yüklenmeden önce toplayıcıda `AES-256-GCM` ile şifrelenir.

Çevrimiçi demoda, dosya yükleme özelliği devre dışı bırakılmış halde aynı kontrol öğeleri gösterilmektedir. Depolama kimlik bilgilerinizi yalnızca kendi çalışmakta olan çalışma alanınızda girin.

[![Tam kapsamlı site dışı kopyalama paneli: uç nokta, bölge, depo, erişim anahtarları, zamanlama, Nesne Kilidi ve kurtarma anahtarı denetimleri](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Gelişmiş seçeneklerin de yer aldığı tam panel açılmış haldedir. Depolama kimlik bilgileri gösterilmemektedir.

| Alan | Ne yazılmalı |
| --- | --- |
| Uç nokta | Depolama hizmetinin URL'si; kova yolu veya kimlik bilgileri içermez. Kurgusal örnek: `https://s3.example.invalid`. |
| Bölge | İstifacınızın gerektirdiği bölge. Uygulamanın varsayılan ayarı `us-east-1`'dir. |
| Bucket | Erişebileceğiniz mevcut bir depo. Kurgusal örnek: `example-case-backup`. |
| Bucket içindeki klasör | Nesne öneki; varsayılan değer `tgwitness`. Uygulama, bu çalışma alanının imza anahtarı parmak izinden türetilen bir öneki ekler. |
| Erişim anahtarı kimliği / Gizli erişim anahtarı | Her iki depolama kimlik bilgisini de birlikte girin. Bu bilgiler çalışma alanı kasasına kaydedilir. Kaydedilen çifti korumak için sonraki kaydetme işlemlerinde her ikisini de boş bırakın. |
| Yol biçimli adresler | Sağlayıcıya göre, etkinleştirildiğinde `endpoint/bucket`'yi, devre dışı bırakıldığında ise `bucket.endpoint`'yi kullanın. |
| Kopyalama aralığı | 1 ila 1.440 dakika arasında; varsayılan ayar 5 dakikadır. Zamanlanmış kopyalama işlemleri için uygulamanın çalışır durumda olması gerekir. |
| Object Lock saklama süresi | Object Lock özelliğini destekleyen bir depolama kutusu için saklama süresi ve modu. Sıfır gün seçeneği, depolama kutusunun varsayılan saklama süresinin geçerli kalmasını sağlar. |

1. Sağlayıcınızla bir depo oluşturun, ardından hedefini ve kimlik bilgilerini girin. Hazırlık aşamasında **“Tesis dışında bir kopya** **sakla”** seçeneğinin işaretini kaldırın, ardından **“Tesis dışında bir kopya kaydet”** seçeneğini seçin.
2. **"Bağlantıyı Test Et"** seçeneğini seçin. Bu işlem, şifrelenmiş bir test nesnesini yükler ve depolama yanıtını kontrol eder.
3. **"Şifreleme anahtarını indir**" seçeneğini seçin. Bu dosyayı toplayıcıdan ayrı bir yerde saklayın; kurtarma işlemi için gereklidir.
4. "**Dışarıda bir kopya sakla**" onay kutusunu işaretleyin ve tekrar kaydedin. Manuel bir işlem için "**Şimdi kopyala**"yı seçin veya zamanlamayı çalışır durumda bırakın.

## Saklama süresini ve kopyalama sürecini kontrol edin

**"Diğer seçenekler**" altında, saklama süresini seçin ve depolama alanınız Object Lock'u destekliyorsa "`GOVERNANCE`" veya "`COMPLIANCE`" seçeneğini seçin. TgWitness, yüklenen bir nesnenin saklama modunu ve son tarihini geri okur. Ayrı saklama sonucunu inceleyin: onaylandı, saklama eksik veya kontrol başarısız.

Panel, son geçişi, nesne sayısını, aktarılan bayt sayısını, kopyalanan günlük sınırını ve varsa hataları bildirir. Eksik veya değiştirilmiş yerel ortamlar bildirilir ve bir sonraki geçişte yeniden denenir. Bu ortamdan sonraki dosyalar, kontrol noktaları ve kuyrukta bekleyen dışa aktarımlar yine de kopyalanabilir.

Yüklemeler için çalışma alanının Direct, SOCKS5 veya HTTP yolunu kullanın; S3 kopyalama için bu yollardan birini seçin; yalnızca MTProxy yolunun seçilmesi durumunda kopyalama işlemi bir hata mesajıyla beklemede kalır.

## Geri yükleme anahtarını ayrı bir yerde saklayın

İndirilen JSON dosyası, şifre çözme anahtarını, hedef ayarlarını, çalışma alanı nesnesi önekini ve imza anahtarı parmak izini içerir. Kurtarma işlemi için hem bu anahtar dosyasına hem de depolama kovasına okuma erişimi sağlayan ayrı depolama kimlik bilgilerine ihtiyaç vardır. Bunları kurtarma planınızda saklayın.

Uç noktayı, depolama kovasını veya klasör önekini değiştirirseniz, hedef ayarlarının uyumlu olması için anahtar dosyasını yeniden indirin. Uygulama, yerel olarak saklanan günlüğün, dosyaların ve kontrol noktalarının yeni bir kopyasını yeni hedefte başlatır. Tamamlanmış sohbet dışa aktarımları, yerel yükleme kuyruğundan zaten kaldırılmış olsa bile önceki hedeflerinde kalır.

## Başka bir makinede geri yükleme ve doğrulama

Güvenilir bir TgWitness kurulumu, indirilen anahtar JSON dosyası, okuma erişimine sahip depolama kimlik bilgileri ve boş bir çıktı dizini kullanın. Aşağıdaki hayali kimlik bilgisi yer tutucularını değiştirin.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

İndirilen dosyalar ve şifresi çözülmüş nesneler, tüm günlük, saklanan kontrol noktaları ile korunmuş medya hash değerleri ve boyutları kontrol edilirken özel geçici depolama alanında tutulur. Güvenli olmayan yollar, çakışan günlük segmentleri ve kontrol noktasından daha kısa olan günlükler reddedilir. Doğrulama başarısız olursa, geri yüklenen dosyalar yayınlanmaz.

Kurtarma işlemi başarılı olursa, kopyada bulunan içerik için `events.jsonl`, `media/`, `checkpoints/` ve `exports/` değerleri elde edilir. Kurtarılan içerikle birlikte komutun JSON sonucunu da saklayın.

Kurtarılan materyali, bağımsız olarak sakladığınız kontrol noktaları veya tanık kayıtlarıyla karşılaştırın, ardından ihtiyacınız olan dönem için kaydedilen toplama kapsamını inceleyin.
