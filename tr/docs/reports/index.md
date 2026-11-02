# Bir rapor tasarlayın

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reports/

Okuyucuya, vaka sorusundan kaydedilmiş kayıtlara kadar net bir yol haritası sunun.

Report Studio, veri seçimi, okunabilir değişiklik geçmişleri, grafikler ve yazdığınız bulguları bir araya getirir. Desteklenen HTML ve yerel PDF çıktılarına sekiz entegre tasarım uygulanır. HTML, PDF ve JSON raporları kendi imzalı mühürlerini taşır; ZIP manifestosu da paketteki dosyaları birbirine bağlar. HTML ve PDF, nihai mizanpajları tamamlandıktan sonra mühürlenir.

## Üç adımda bir rapor oluşturun

1. **Dışa Aktar → Yapılandır ve önizle → Veri seçeneğini** açın. Tüm çalışma alanını kullanın veya sohbetleri, yazarları, UTC gözlem tarihlerini ve kayıt türlerini seçin. Tarihler, TgWitness'in kaydı ne zaman gözlemlediğini belirtir.
2. "**Tasarım ve içerik**" bölümünde bir tasarım ve içerik ön ayarı seçin. Etkinlik çizelgelerini, katılımcı etiketlerini, transkripti, kaydedilen değişiklikleri ve isteğe bağlı Case Board materyallerini seçin. Vaka ayrıntılarınızı ve inceleme notlarınızı ekleyin.
3. **Önizleme'yi** açarak sayıları, etkinlikleri, katılımcıları, örneklem kayıtlarını ve eksik kimlik aralıklarını inceleyin. Ayarları kaydedin, ardından ihtiyacınız olan formatı indirin.

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

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading serisi ve Ledger & margin,** aynı temel kayıtları farklı düzenlerde sunar. Tasarım değiştirildiğinde veri seçimi ve yazılı notlar korunur. Rapor dili, desteklenen 25 dilden seçilebilir.

Okuma serisi, vaka, kapsam, bulgular ve değişiklikleri bir bölüm çubuğu etrafında gruplandırır. Ledger & margin, numaralı bölümler ve geniş kenar boşluğu kullanır. Her ikisi de hesap HTML özetlerini ve kopya paylaşımını destekler. Yerel PDF'ler, pakete dahil edilmiş yazı tipleriyle oluşturulur; kullanıcının bilgisayarında PDF oluşturmak için tarayıcı veya Node kurulumu gerekmez. Çince, Japonca ve Korece PDF'ler için ayrıca sunucuda, sistem genelinde kurulmuş veya `TGWITNESS_FONT_DIR` dizinine yerleştirilmiş Noto Sans CJK gibi uygun bir yazı tipinin bulunması gerekir. Bu yazı tipi yoksa, ZIP dosyası HTML ve JSON raporlarını içerir.

## Değişikliği bağlamı içinde okuyun

Kaydedilen düzenlemeler, önceki ve sonraki halleriyle gösterilir. Bir silme bildirimine, en son yakalanan sürüm eşlik edebilir. Yanıtlar, alıntılar, iletmeler, tepkiler, düğmeler ve ek meta verileri, mevcut referanslarını korur. Dosya SHA-256 ve günlük kaydı hash değerleri ayrı ayrı etiketlenir.

Tasarım önizlemesi, ilk 50.000 kaynak kayıttan eşleşen kayıtları kullanarak kapak, inceleme ve grafik bileşenlerini gösterir. Ayrı veri önizlemesi, tam seçim sayılarını belirlemek için kararlı günlük anlık görüntüsünün tamamını tarar ve görüntülenen örnek sınırları etiketlenir. Nihai sayfa numaralandırmasını incelemek için bir PDF oluşturun. Tam hesap dışa aktarımında bir HTML genel bakışı bulunur; tek tek sohbet PDF’leri seçilen tasarımı kullanır.

## Alıcının kopyasını özenle seçin

Rapor filtreleri, okunabilir raporu şekillendirir. Tam kanıt ZIP dosyası, orijinal günlüğü ve ekleri korur. Alıcının yalnızca seçilen verileri alması gerektiğinde, [en az miktarda veri içeren](https://phishdestroy.github.io/TgWitness/tr/docs/handover/) bir [devir işlemi](https://phishdestroy.github.io/TgWitness/tr/docs/handover/) kullanın. [Rapor içeriğini ve doğrulamayı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/) inceleyin veya [tamamlanmış dışa aktarmayı doğrulayın](https://phishdestroy.github.io/TgWitness/tr/docs/exports/).
