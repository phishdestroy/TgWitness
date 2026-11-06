# Telegram · Dışa aktarma ve doğrulama

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/exports/

Birine, çalışma alanınıza karşı kendisinin doğrulayabileceği dosyalar verin.

Referansı saklayınİmzalı ZIP dosyasını dışa aktarAlıcı doğrular

İmzalar ve kontrol noktaları sizin için yeni mi? [Örnek bir kaydı değiştirin](https://phishdestroy.github.io/TgWitness/tr/docs/concepts/#chain) ve hangi kontrollerin yakaladığını görün.

Bir kopyayı veri toplayıcıdan uzak tutmak mı istiyorsunuz? [S3 kurulumu](https://phishdestroy.github.io/TgWitness/tr/docs/exports/#s3), [Nesne Kilidi](https://phishdestroy.github.io/TgWitness/tr/docs/exports/#s3-retention) veya [doğrulanmış kurtarma](https://phishdestroy.github.io/TgWitness/tr/docs/exports/#s3-restore) bölümlerine gidin.

## Güvenilir bir kaynak olarak kalın

Çalışma alanının anahtar parmak izini toplayıcı dışında bir yere yazın. Toplama sırasında imzalı kontrol noktalarını da başka yerde saklayın ya da [bağımsız bir tanık](https://phishdestroy.github.io/TgWitness/tr/docs/witness/) çalıştırın. Alıcı anahtarı ve önceki bir günlük durumunu bununla karşılaştırır.

## İmzalı ZIP dosyasını indirin

**Dışa aktarımlar** → imzalı kanıt ZIP'i. Tüm günlüğü ve imzalı bir dosya manifestini içerir. Okunabilir raporu [Report studio](https://phishdestroy.github.io/TgWitness/tr/docs/reports/)'da biçimlendirin ya da yalnızca seçili verileri [teslim özeti](https://phishdestroy.github.io/TgWitness/tr/docs/handover/) olarak gönderin.

HTML, PDF ve JSON raporların kendi mühürleri vardır. CSV yalnızca çalışma kopyasıdır; bütünlük için doğrulanmış ZIP'teki CSV'yi kullanın.

## TgWitness'in güvenilir bir kopyasıyla doğrulayın

Proje ortamında, kendi parmak iziniz ve yollarınızla:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Başarılı olursa `key_pinned: true` ve `checkpoint_checked: true` görürsünüz. Bu çıktıyı arşivin yanında saklayın. Kontrol noktası dışa aktarımın sonunda ya da öncesinde olmalı.

## Doğrulama sonucunu kullanın

- **Dosyalar:** manifest karmalarını, imzalar günlüğü bağlar. Her değişiklik ortaya çıkar.
- **Kimlik:** sakladığınız parmak izi bunun beklenen anahtar olduğunu kanıtlar.
- **Önceki durum:** bir kontrol noktası dışa aktarımı teslimden önce kaydedilen bir günlük başıyla karşılaştırır.
- **Kapsam:** boşluklar, edinim sonuçları ve gönder → düzenle → sil testi bu kurulumun gerçekte neyi yakaladığını gösterir.

Ayrıntılar: [doğrulamanın neyi kanıtladığı ve neyi kanıtlamadığı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope).

## S3 dış sunucu kopyasını kurun

Çalışma alanınızda **Dışa aktarımlar → Harici kopya**. AWS S3 ve S3 uyumlu her şeyle çalışır. Günlük segmentlerini, kaydedilen dosyaları, zaman damgalarıyla kontrol noktalarını ve bitmiş sohbet dışa aktarımlarını kopyalar; her biri toplayıcıdan çıkmadan önce `AES-256-GCM` ile şifrelenir.

Çevrimiçi demo bu ayarları yükleme kapalıyken gösterir. Gerçek kimlik bilgilerini yalnızca kendi kurulumunuza girin.

[![Tam kapsamlı site dışı kopyalama paneli: uç nokta, bölge, depo, erişim anahtarları, zamanlama, Nesne Kilidi ve kurtarma anahtarı denetimleri](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Gelişmiş seçeneklerin de yer aldığı tam panel açılmış haldedir. Depolama kimlik bilgileri gösterilmemektedir.

| Alan | Ne yazılmalı |
| --- | --- |
| Uç nokta | Depolama URL'si, bucket yolu ya da kimlik bilgisi olmadan. Örnek: `https://s3.example.invalid`. |
| Bölge | Sağlayıcınızın istediği. Varsayılan `us-east-1`. |
| Kova | Yazabildiğiniz mevcut bir bucket. Örnek: `example-case-backup`. |
| Bucket içindeki klasör | Önek, varsayılan `tgwitness`. Üstüne çalışma alanı başına bir önek eklenir. |
| Erişim anahtarı kimliği / Gizli erişim anahtarı | İkisi birlikte, kasada saklanır. Korumak için sonradan ikisini de boş bırakın. |
| Yol biçimli adresler | Açık: `endpoint/bucket`. Kapalı: `bucket.endpoint`. Sağlayıcıya bağlı. |
| Kopyalama aralığı | 1–1.440 dakika, varsayılan 5. Yalnızca uygulama çalışırken. |
| Object Lock saklama süresi | Bucket Object Lock destekliyorsa gün ve kip. Sıfır, bucket varsayılanını korur. |

1. Bucket'ı oluşturun, **Harici kopya tut** işaretsizken hedefi ve kimlik bilgilerini doldurun, **Harici kopyayı kaydet**'e basın.
2. **Bağlantıyı test et** şifreli bir test nesnesi yükler.
3. **Şifreleme anahtarını indir** ve toplayıcıdan uzakta saklayın. Anahtar yoksa kurtarma da yok.
4. **Harici kopya tut**'u işaretleyin, kaydedin, sonra **Şimdi kopyala** ya da zamanlamayı çalışmaya bırakın.

## Saklama süresini ve kopyalama sürecini kontrol edin

**Diğer seçenekler** altında saklama günlerini ve `GOVERNANCE` ya da `COMPLIANCE` seçin. TgWitness saklamayı yüklenen bir nesneden geri okur ve size söyler: onaylandı, eksik ya da kontrol başarısız.

Panel son geçişi, nesne sayısını, baytları, kopyalanan günlük sınırını ve hataları gösterir. Eksik bir yerel dosya bildirilir ve sonraki geçişte yeniden denenir, gerisi kopyalanmaya devam eder.

Yüklemeler doğrudan, SOCKS5 ya da HTTP üzerinden gider. Yalnızca MTProxy rotasıyla kopya bir hatayla bekler.

## Geri yükleme anahtarını ayrı bir yerde saklayın

Anahtar JSON'u şifre çözme anahtarını, hedefi, öneki ve anahtar parmak izini içerir. Kurtarma için bu ve okuma erişimli depolama kimlik bilgileri gerekir.

Uç nokta, bucket ya da önek mi değişti? Anahtarı yeniden indirin. Yeni hedefte taze bir kopya başlar; eski sohbet dışa aktarımları olduğu yerde kalır.

## Başka bir makinede geri yükleme ve doğrulama

Güvendiğiniz bir TgWitness kurulumu, anahtar JSON'u, salt okunur kimlik bilgileri ve boş bir klasör gerekir:

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

Önce her şey özel bir geçici klasörde denetlenir: tüm günlük, kontrol noktaları, dosya karmaları ve boyutları. Güvensiz yollar, çelişen segmentler ya da kontrol noktasından kısa bir günlük başarısız olur ve o zaman hiçbir şey yazılmaz.

Başarılı olursa `events.jsonl`, `media/`, `checkpoints/` ve `exports/` elde edersiniz. Komutun JSON çıktısını yanlarında saklayın ve kendi sakladığınız kontrol noktaları ya da tanık kayıtlarıyla karşılaştırın.
