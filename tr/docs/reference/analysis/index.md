# Arşiv analizi

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/analysis/

Kaydedilen mesajları arayın, yapay zeka girdilerini inceleyin ve kaynak referanslarıyla birlikte analitik raporlar tutun.

**Güncel ana sürüm:** kaynak kodunu kontrol edin; 0.7.0 taşınabilir önizleme sürümü bu özelliğin öncesine aittir.

[İş akışı kılavuzu](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Yapay zekâ kullanmadan yerel arama yapmak için **Günlük** bölümünü kullanın. **Arşive sor** özelliği için önce **Entegrasyonlar** bölümünde bir sağlayıcıyı etkinleştirip yapılandırın. Çalışma alanı seçici hesabı belirler; form ise sohbetleri ve gözlem dönemini belirler. Getirme işlemi yerel olarak çalışır. Tam bir ifade veya alan adı getirilen sonuçları daraltır; bir mesaj kimliği kaydedilmiş sürümleri talep eder. Alıntıları inceleyin ve ilgili günlük kayıtlarını veya bağlamlarını açın. Vektör veritabanı veya otomatik Telegram eylemi yoktur.

## Hizmet sağlayıcılar ve rıza

AI, her çalışma alanında varsayılan olarak devre dışıdır. Yalnızca ana yönetici, modeli, uç noktayı, şifreli API anahtarını, bağlam/çıktı sınırlarını, zaman aşımını ve günlük istek bütçesini yapılandırabilir. Anahtar hiçbir zaman tarayıcıya geri gönderilmez. Mevcut anahtarı korumak için anahtar alanını boş bırakın veya anahtarı açıkça kaldırın.

Ollama, akışsız JSON çıktısı olan belgelenmiş [`/api/chat` uç](https://docs.ollama.com/api/chat)noktasını kullanır. Varsayılan adresi, TgWitness sunucusundaki `http://127.0.0.1:11434`'dir. Operatör, bunu `TGWITNESS_AI_LOCAL_ENDPOINT` kullanarak değiştirebilir; bu, model tarafından kontrol edilen bir adres değildir. Seçilen modeli kendiniz yükleyin. TgWitness bunu otomatik olarak indirmez.

Uyumlu sağlayıcı, `/v1` ile biten bir temel URL ve [Sohbet Tamamlama protokolü](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) bekler: `messages`, JSON yanıt modu, `max_completion_tokens` ve `choices[0].message.content`. Bu alanlara sahip olmayan hizmetler desteklenmez. Bağlantı testi, sentetik metin gönderir ve istek bütçesinden düşülür.

Her istek, çalışma alanının yapılandırılmış dış rotasını kullanır. Engellenmiş bir rota veya yalnızca Telegram'a özel MTProxy bir hata oluşturur; doğrudan yeniden deneme yapılmaz. Kasıtlı olarak yapılandırılmış yerel bir Ollama adresi, seçilen rotayı kullanmaya devam ederken özel bir hedefe izin verir. Diğer özel hizmetler için mevcut sunucu düzeyindeki özel hedef seçimi geçerlidir. Panel, gerçekte yapılandırılmış uç noktayı gösterir.

Oluşturma işleminden önce, **modele gönderilen veriler** talebi gösterir: soru, kontrol edilen alıntılar, olay türleri, gözlem zamanları ve kapsam işaretçileri. Telegram oturumları, ham alanlar, sağlayıcı anahtarları, ek baytları ve tam günlük bu bağlamın bir parçası değildir. İstenmeyen kaynakların işaretini kaldırın, ardından işlemeyi açıkça onaylayın. Harici sağlayıcılar, gönderilen içeriği kendi politikaları kapsamında saklayabilir. Yerel yürütme, uç noktanın yerel olduğu anlamına gelir; bu, bağımsız olarak yapılandırılmış bir hizmetin davranışına ilişkin bir garanti değildir.

Küresel olarak en fazla iki eşzamanlı sağlayıcı isteği ve her çalışma alanı başına bir istek kabul edilir. Önizleme on dakika sonra geçerliliğini yitirir ve yalnızca bir yanıt üretebilir. Sağlayıcının bildirdiği token sayıları gösterilir; maliyet tahmini yalnızca giriş ve çıkış tarifeleri yapılandırıldığında görünür. Başarısız denemeler de günlük istek bütçesinden düşülür. Otomatik yeniden denemeler ek bütçe harcamaz.

## Kaynaklar ve sınırlamalar

Geri getirme işlevi, kaydedilmiş mesaj metinlerini sınırlı bir sözcüksel arama ile inceler. En fazla 24 kaynak döndürür ve kesilmiş alıntıları veya eksik sonuç kümelerini işaretler. Süre, **gözlem zaman**ını ifade eder; Telegram geçmişinin eksiksiz olduğu iddiasını içermez. Çalışma alanı genelindeki olaylar, sohbet kapsamındaki erişimden hariç tutulur. Eksik veriler, mevcut arşivde bulunamayan veriler olarak tanımlanır.

Modele herhangi bir araç sağlanmaz. Modelin kaynak kimlikleri, seçilen kayıtlara göre doğrulanır, hash değerleri yeniden kontrol edilir ve alıntılanan dizeler bu kayıtlarda yer almalıdır. Bilinmeyen kimlikler, değiştirilmiş alıntılar ve kaynak gösterilmemiş iddialar cevabı geçersiz kılar. Uygulama bağlantılar oluşturur; model tarafından üretilen URL’ler kaynak gösterimi olarak kullanılmaz. Bu kontroller bir çıkarımın doğruluğunu değil, kaynağın varlığını ve alıntının doğruluğunu teyit eder. Çıkarımlara güvenmeden önce bunları kayıtlarla karşılaştırarak gözden geçirin.

## Raporlar

İncelenmiş bir yanıtı ayrı bir analitik rapor olarak kaydedin. Rapor, model özetini, gözlemlenen kronolojiyi, çıkarılan bağlantıları ve kullanıcı adlarını, düzenleme/silme kayıtlarını, kapsam sınırlarını ve kaynak olay hash'lerini içerir. Sağlayıcı, model, uç nokta, zaman ve komut şablonu sürümü de rapora eklenir. Hiçbir kimlik otomatik olarak birleştirilmez.

Analistlerin düzeltmeleri ve notları, model özetinden ayrı olarak saklanır. Raporlar, imzalanmış olay akışının dışında bir dizin içeren şifrelenmiş türetilmiş dosyalarda bulunur; orijinal olaylar ve medya dosyaları değişmez. Yalnızca sahip veya yönetici bir raporu açabilir ve kaynak erişimi yeniden kontrol edilir. İndirme işlemi için de dışa aktarma izni gereklidir. Sürüm 1, raporları imzalamaz veya model sonuçlarının doğrulanmış kanıtlar olduğunu ima etmez. Sınırlar: Çalışma alanı başına 100 rapor ve rapor başına 100 analist revizyonu .

Manuel OCR ve transkriptler için [medya işleme](https://phishdestroy.github.io/TgWitness/tr/docs/reference/media-analysis/) bölümüne bakınız. İstemci erişimi için [MCP bölümüne](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/) bakınız.
