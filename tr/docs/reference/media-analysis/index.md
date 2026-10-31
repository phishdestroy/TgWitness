# Yerel OCR ve transkripsiyon

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/media-analysis/

Yerel bir işleyici ile yakalanan görüntüleri ve sesleri tanıyın; elde edilen metni kaynak dosyasına bağlı tutun.

**Güncel ana sürüm:** kaynak kodunu kontrol edin; 0.7.0 taşınabilir önizleme sürümü bu özelliğin öncesine aittir.

[İş akışı kılavuzu](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Bir `media.saved` günlük kaydını açın, "**Eki tanıma"yı** seçin, ardından "**Arşive sor"** altından OCR veya transkripsiyon seçeneğini seçin. İşleme manuel ve yerel olarak gerçekleştirilir. Bulut ortam modu veya otomatik yükleme yoktur. Orijinal ek baytları ve `media_sha256` dosyası değişmeden kalır; tanınan metin, açıkça "makine tanınması" olarak işaretlenir ve kaynak hash değeri, motor/model sürümü, dil, parametreler ve tamamlanma zamanı ile birlikte ayrı olarak saklanır. Transkriptler, döndürülen zaman damgalarını korur.

Bu sonuçları, **"Tanınan metni ara"** ve OCR/transkript filtresini kullanarak arayın. Bu, ayrı bir türetilmiş veri aramasıdır; makine tanımlamasını sessizce orijinal Telegram metnine dönüştürmez veya imzalı olaylara eklemez.

## İsteğe bağlı işleyicinin kurulumu

Sürüm 1, yerel bir Docker arka plan programı bulunan bir Linux sunucusu gerektirir. Windows kurulumlarında TgWitness, kendi yerel arka plan programı ile bir Linux VM/WSL ortamında çalıştırılabilir. Panel, güvenilir olmayan ekleri asla kendi başına açmaz.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Bu değişkenleri TgWitness hizmet ortamında ayarlayın ve hizmeti yeniden başlatın. Arka plan hizmeti soketinin varsayılan değeri `/var/run/docker.sock`'dir; root erişimi olmayan kurulumlarda `TGWITNESS_DOCKER_SOCKET` ayarlanabilir. İşlemci, uzak bir Docker bağlamı yerine açıkça bu Unix soketini kullanır. Docker API'sını panel kullanıcılarına açmayın veya soketini tanıma konteynerinin içine bağlamayın.

Transkripsiyon için, CTranslate2 ile uyumlu bir Whisper modelini ayrı olarak yükleyin, ardından `TGWITNESS_WHISPER_MODEL_DIR`'yi bu modelin dizinine ayarlayın. İşleyici, `local_files_only=True` ile modeli yükler; seçilen model ve girdi salt okunur olarak bağlanır. Motorun [model yükleme belg](https://github.com/SYSTRAN/faster-whisper)elerine bakın. Sağlanan OCR görüntüsü, İngilizce ve Rusça eğitim verilerini içerir. Gerektiğinde görüntünüze başka bir dil ekleyin; dil kodları [Tesseract'ın CLI'sine](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html) uygundur.

İşleme sırasında herhangi bir model yüklenmez. Kurulum/indirme işlemi ağ bağlantısı gerektirebilir; her bir gerçek tanıma konteynerinde ağ bağlantısı devre dışıdır. Etkinleştirmeden önce görüntüyü yükleyin; çalışma zamanı `--pull=never` kullanır.

## Sınırlar ve kurtarma

Konteyner, salt okunur root erişimi, kısıtlanmış yetkiler, `no-new-privileges` , bir CPU, 2 GiB bellek, bir PID sınırı ve sınırlı geçici dosya sistemi ile ayrıcalıksız bir kullanıcı olarak çalışır. Yalnızca seçilen dosyanın doğrulanmış bir kopyası ve isteğe bağlı bir model dizini bağlanır. Toplayıcının veritabanı, kasası ve oturumu bağlanmaz. [Docker çalışma zamanı bayrakları](https://docs.docker.com/reference/cli/docker/container/run/) bu sınırlamaları uygular; bu, bir donanım bölgesi değil, bir konteyner sınırı olarak kalır.

Dosya boyutu 50 MiB, resim boyutu 20 milyon piksel, ses boyutu ise süresi bilinen 30 dakika ile sınırlıdır ve işleme süresi beş dakikadır. Her seferinde yalnızca bir işçi çalışır; her çalışma alanı başına en fazla 20 kuyrukta bekleyen/çalışan iş ve 100 saklanan iş bulunur. "İptal" komutu konteyneri durdurur; "yeniden dene" komutu önceki denemeyle bağlantılı yeni bir iş oluşturur. Kesintiye uğrayan işler, yeniden başlatıldıktan sonra işaretlenir. Bir model, yapılandırılan sınırlara uymadığında işleme başarısız olabilir; izolasyon olmadan sessizce çalışmaz.
