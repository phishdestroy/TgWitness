# Arşivi inceleyin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/archive/

Mesajı bulun. Kaynağını kontrol edin. Davayı oluşturun.

Bu araçlar mevcut ana dalda mevcuttur. 0.7.0 taşınabilir önizleme sürümü bunlardan daha eskidir; bu iş akışı için kaynak kodunu indirip derleyin.

01**Geçmişi ekleyin**

Etkinleştirilmiş kaynaklarınızdaki geçmiş mesajları çalışma alanına yükleyin.

02**Kaynakları takip edin**

Arşivi arayın ve her sonucun arkasında bulunan kaydedilmiş mesajı açın.

03**Devir teslim sürecini net tutun**

Analizinizi ayrı bir dosyaya kaydedin ve yanında imzalanmış kanıtı dışa aktarın.

Kaydedilen veriler, tanınan metinler ve analistlerin sonuçları birbirinden ayrı tutulur.

## Geçmiş mesajları yükle

1. **Kaynaklar → Kapsamdaki sohbetler** bölümünü açın, etkinleştirilmiş sohbetleri inceleyin ve gözlemi başlatın.
2. **"Tüm geçmişi yükle**" seçeneğini seçin. İşlem, o anda seçili olan kaynak listesini kullanır.
3. Gerektiğinde "**Geçmişi Duraklat"** ve "**Geçmişe Devam Et" seçeneklerini** kullanın. Yeniden başlatmanın ardından, işlemi açıkça devam ettirin.
4. Kaynak bazında sonuçları ve ek kuyruğunu kontrol edin. Kanıt dışa aktarımıyla birlikte imzalı ilerleme raporunu kaydedin.

Bu işlem, çalışma alanını mevcut mesajlarla doldurur. Sohbet başına HTML/JSON dışa aktarma işlemi ayrı bir işlemdir. [Geçmiş ve kurtarma ayrıntıları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/).

## Önce araştırın, sonra yapay zeka konusunda karar verin

1. Yerel arama için **Günlük** bölümünü açın. Bir çalışma alanı seçin ve kaynak ile zaman filtrelerini kullanın.
2. Bir ifadeyi veya etki alanını arayın. Eşleşen kaydı ve kaydedilmiş sürümlerini açın.
3. Yapay zekâ analizi için yönetici, **Entegrasyonlar** bölümünde bir sağlayıcıyı etkinleştirir ve yapılandırır. **Arşive sor** bölümünü açın, sohbetleri ve bir dönem seçin. İsteği onaylamadan önce **Modele gönderilen veriler** bölümünü inceleyin ve istenmeyen alıntıların işaretini kaldırın.
4. Geri dönen alıntıları kontrol edin. Cevabı rapor olarak kaydedin ve kendi düzeltmelerinizi veya notlarınızı ekleyin.

Arama işlemi yapay zeka kullanılmadan yerel olarak gerçekleştirilir. Analitik raporlar kaynak referanslarını ve revizyon geçmişini saklar; bu raporlar imzalı kayıt defterinden ayrıdır. [Sağlayıcı kurulumu ve raporlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/analysis/).

## İhtiyacınız olan bağlantıyı seçin

| Görev | Aç | Kurulum |
| --- | --- | --- |
| Bir AI istemcisinden seçilmiş sohbetleri okuyun | **Entegrasyonlar → MCP** | [MCP eklentisini yükleyin, kapsamlı bir token oluşturun ve istemciyi bağlayın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/) |
| Kaydedilmiş medyadaki metni tanıma | Bir `media.saved` kaydı → **Eki tanıma** | [Yerel Docker işleyicisini ve gerekli dil/model dosyalarını kurun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/media-analysis/) |
| Olayları n8n veya bir SIEM'e gönderin | **Entegrasyonlar → Giden webhook'lar** | [Alıcı ekle, HMAC'yi doğrula ve olay kimliklerini tekilleştir](https://phishdestroy.github.io/TgWitness/tr/docs/reference/webhooks/) |

**Hangi erişim jetonu nereye girilir?**

Panele erişim, davayı inceleyen kişilere açıktır. MCP bağlantıları, ayrı salt okunur arşiv jetonları alır. Bir webhook alıcısı, kendi HMAC gizli anahtarını kullanır. Hiçbiri Telegram oturum dosyasına ihtiyaç duymaz.

[Panel erişimini paylaşın](https://phishdestroy.github.io/TgWitness/tr/docs/access/) veya [bir MCP istemcisini yapılandırın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/).

## Kaynakları ve sonuçları sunun

İncelenmiş analitik raporu, imzalı kanıt ZIP dosyasıyla birlikte saklayın. Rapor, kaynakları nasıl yorumladığınızı açıklar; ZIP dosyası ise alıcının, kaydedilen kaydı bağımsız ve güvenilir bir parmak izi ve kontrol noktasıyla karşılaştırarak doğrulamasını sağlar.

[Dışa aktarma ve doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/exports/) · [Tam bir soruşturma sürecini adım adım inceleyin](https://phishdestroy.github.io/TgWitness/tr/docs/cases/)
