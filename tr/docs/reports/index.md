# Telegram · Bir rapor tasarlayın

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reports/

Okuru dava sorusundan doğrudan kaydedilmiş kayıtlara götürün.

Report studio seçtiğiniz verileri, değişiklik geçmişlerini, grafikleri ve bulgularınızı bir araya getirir. Sekiz tasarım, HTML ve yerel PDF. Her HTML, PDF ve JSON rapor sizin anahtarınızla mühürlenir.

## Üç adımda bir rapor oluşturun

1. **Dışa aktarımlar → Yapılandır ve önizle → Veri**: tüm çalışma alanı ya da seçtiğiniz sohbetler, yazarlar, tarihler (UTC, TgWitness'ın kaydı gördüğü zaman) ve kayıt türleri.
2. **Tasarım ve içerik**: bir tasarım ve neyin gireceğini seçin: grafikler, katılımcılar, döküm, değişiklikler, Case Board öğeleri, dava ayrıntıları ve notlar.
3. **Önizleme**: sayıları, etkinliği, örnekleri ve eksik kimlik aralıklarını kontrol edin. Kaydedin, sonra gereken biçimi indirin.

### Okuyucu için kaydedilen materyali aynı şekilde düzenleyin

Sentetik örnek · şematik düzen, oluşturulmuş bir rapor değildir

1. **Seç.** Vaka için iki sohbet ve gözlem süresini seçin.
2. **Metni oluşturun.** Bir düzen seçin ve soruyu yanıtlayan bölümleri belirleyin.
3. **Önizleme.** Seçilen sayıları ve kaydedilen "öncesi-sonrası" metinlerini gözden geçirin.
4. **Doğrulayın.** Nihai dosyayı oluşturun ve imzasını güvenilir çalışma alanı parmak iziyle karşılaştırarak kontrol edin.

#### Seçilmiş gözlemler

2 sohbet · 1 gözlem günü

Mesajlar, düzenlemeler ve silme bildirimleri

#### Rapor yapısı

##### Ödeme hedefi değiştirildi

Vaka sorusu → kapsam → bulgular → kayıt referansları

**Mesaj bağlamı**

Gözlem #142: “Yeni ödeme bağlantısını kullanın.”

**Kaydedilen değişiklikler**

Önce: eski.örnek.geçersiz → Sonra: yeni.örnek.geçersiz

#### Seçimi gözden geçirin

18 yorum · 2 kaydedilmiş düzenleme

Gönderilme, düzenlenme ve gözlemlenme zamanları için ayrı etiketler bulunmaktadır.

#### Nihai teslimat

İmzalı PDF + imzalı JSON veya okunabilir raporu içeren imzalı bir ZIP dosyası

Alıcı, dosyayı ve güvenilir parmak izini kontrol eder.

## Bir okuma stili seçin

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**: aynı kayıtlar, farklı görünüm. Değiştirince seçim ve notlar korunur. 25 dilden herhangi biri.

PDF'ler paketlenmiş yazı tipleriyle, tarayıcı olmadan üretilir. Çince, Japonca ve Korece için sunucuda Noto Sans CJK gibi bir yazı tipi gerekir (sistem genelinde ya da `TGWITNESS_FONT_DIR` içinde); yoksa yalnızca HTML ve JSON alırsınız.

## Değişikliği bağlamı içinde okuyun

Düzenlemeler öncesini ve sonrasını, silmeler son kaydedilen sürümü gösterir. Yanıtlar, iletmeler, tepkiler, düğmeler ve ekler başvurularını korur.

Tasarım önizlemesi ilk 50.000 kaydı kullanır, veri önizlemesi her şeyi tam sayar. Son sayfa düzeni için PDF'i oluşturun.

## Alıcının kopyasını özenle seçin

Süzgeçler yalnızca raporu biçimlendirir; kanıt ZIP'i hâlâ tüm günlüğü ve dosyaları içerir. Alıcı daha azını almalıysa [küçültülmüş bir teslim](https://phishdestroy.github.io/TgWitness/tr/docs/handover/) kullanın. Daha fazlası: [rapor içeriği](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/), [dışa aktarımı doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/exports/).
