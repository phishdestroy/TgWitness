# Telegram · Arşivi inceleyin

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/archive/

Mesajı bulun. Kaynağını kontrol edin. Davayı oluşturun.

01**Geçmişi ekleyin**

Etkin kaynaklarınızın eski mesajlarını çalışma alanına çekin.

02**Kaynakları takip edin**

Arayın, sonra her sonucun arkasındaki kaydedilmiş mesajı açın.

03**Devir teslim sürecini net tutun**

Analiziniz bir dosyada, imzalı kanıt hemen yanında.

Kaydedilen veriler, tanınan metinler ve analistlerin sonuçları birbirinden ayrı tutulur.

## Geçmiş mesajları yükle

1. **Kaynaklar → Kapsamdaki sohbetler**: etkin sohbetleri kontrol edin, gözlemi başlatın.
2. **Tüm geçmişi yükle**. Kaynak listesini o anki haliyle alır.
3. **Geçmişi duraklat** / **Geçmişe devam et** istediğiniz zaman. Yeniden başlatmadan sonra elle devam edin.
4. Her kaynağın sonucunu ve indirme kuyruğunu kontrol edin, imzalı ilerleme raporunu dışa aktarımla birlikte saklayın.

Bu, çalışma alanını doldurur. Tek bir sohbeti HTML/JSON olarak dışa aktarmak ayrı bir iştir. [Ayrıntılar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/).

## Önce araştırın, sonra yapay zeka konusunda karar verin

1. **Günlük** yerelde arar; kaynağa ve zamana göre süzer.
2. Bir ifade ya da alan adı arayın, kaydı ve sürümlerini açın.
3. Yapay zekâ için yönetici **Entegrasyonlar** bölümünde bir sağlayıcı ayarlar. Sonra **Arşive sor**: sohbetleri ve dönemi seçin, **Modele gönderilen veriler** bölümüne bakın ve dışarı çıkmaması gerekenlerin işaretini kaldırın.
4. Alıntıları kontrol edin, yanıtı rapor olarak kaydedin, notlarınızı ekleyin.

Arama yapay zekâ gerektirmez. Raporlar kaynaklarını ve düzeltmelerini imzalı günlükten ayrı tutar. [Sağlayıcı kurulumu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/analysis/).

## İhtiyacınız olan bağlantıyı seçin

| Görev | Aç | Kurulum |
| --- | --- | --- |
| Bir yapay zekâ istemcisinin seçili sohbetleri okumasına izin verin | **Entegrasyonlar → MCP** | [MCP'yi kurun, kapsamlı bir belirteç oluşturun, bağlanın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/) |
| Kaydedilmiş medyadaki metni tanıma | Bir `media.saved` kaydı → **Eki tanıma** | [Yerel Docker çalışanını kurun](https://phishdestroy.github.io/TgWitness/tr/docs/reference/media-analysis/) |
| Olayları n8n veya bir SIEM'e gönderin | **Entegrasyonlar → Giden webhook'lar** | [Bir alıcı ekleyin, HMAC'i doğrulayın, yinelenen kimlikleri ayıklayın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/webhooks/) |

**Hangi erişim jetonu nereye girilir?**

Panel erişimi insanlar içindir. MCP'nin kendi salt okunur belirteçleri, webhook'ların kendi HMAC sırrı vardır. Hiçbiri Telegram oturumuna ihtiyaç duymaz.

[Panel erişimini paylaşın](https://phishdestroy.github.io/TgWitness/tr/docs/access/) veya [bir MCP istemcisini yapılandırın](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/).

## Kaynakları ve sonuçları sunun

Raporu imzalı ZIP'in yanına koyun. Rapor sizin kaynak yorumunuzdur; ZIP ise alıcının doğruladığı şeydir.

[Dışa aktarma ve doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/exports/) · [Tam bir soruşturma sürecini adım adım inceleyin](https://phishdestroy.github.io/TgWitness/tr/docs/cases/)
