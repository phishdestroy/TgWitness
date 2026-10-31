# Giden webhook'lar

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/webhooks/

Kapsam dahilindeki olayları, HMAC imzaları, yeniden deneme ve teslim durumu bilgileriyle birlikte HTTPS alıcılarına gönderin.

**Güncel ana sürüm:** kaynak kodunu kontrol edin; 0.7.0 taşınabilir önizleme sürümü bu özelliğin öncesine aittir.

[İş akışı kılavuzu](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Seçilen çalışma alanında **Entegrasyonlar → Giden webhook'ları** açın. Bir HTTPS alıcısı ekleyin, toplayıcı/medya/dışa aktarma olaylarını seçin ve isteğe bağlı olarak yeni gözlemler ve değişiklikler için sohbetleri seçin. Mesaj metni varsayılan olarak kapalıdır. Alıntıları etkinleştirmek, mesaj değişikliği olaylarına en fazla 1.000 karakter ekler; ham Telegram alanları ve kimlik bilgileri asla gönderilmez.

HMAC gizli anahtarını alıcının korumalı yapılandırmasına bir kez kopyalayın. Bu anahtar, TgWitness'in kasasında şifrelenmiştir ve panelden alınamaz. Hedefi kaldırın ve yeniden oluşturarak rotasyon yapın. **Sentetik test** kuyruklarına, sohbet içeriği içermeyen bir test **gönderin**; sonucunu görmek için teslimat durumunu yenileyin.

Bu hizmet, Apprise ile birlikte mevcut bildirim döngüsünü genişletir. Çalışma alanının dış rotasını ve mevcut özel hedef kısıtlamalarını kullanır. Doğrudan bir yedekleme veya yönlendirme yoktur. URL’ler kimlik bilgileri, sorgu dizeleri veya parçacıklar içermemelidir; özel adresler için sunucu düzeyinde ağ onayı gereklidir; bu, panel kullanıcısının atlayabileceği bir ayar değildir.

## Yük ve imza

Şema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Her yük `event_id`, `timestamp`, `workspace`, `type`, `synthetic` ve sayaçları içerir. Günlük tabanlı olaylar, sıralamalarını ve hash değerlerini içerir. Tam dışa aktarımın tamamlanması ve sentetik testler, uydurulmuş imzalı günlük referansı içermeyen teslimat olaylarıdır. Telegram silme bildirimleri ve `missing_on_recheck` ayrı türler olarak kalır.

`X-TgWitness-Signature` başlığı `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`'dir. `timestamp + "." + raw_request_body` baytları üzerinde, görüntülenen gizli anahtarı UTF-8 baytları olarak kullanarak HMAC hesaplayın. Gövdeyi ayrıştırmadan veya üzerinde işlem yapmadan önce imzaları sabit sürede karşılaştırın. Saatinizden beş dakikadan fazla farklı olan zaman damgalarını reddedin. Zaman damgası her teslimat denemesinde yenilenir.

`event_id`'yi, yan etkilerden önce atomik benzersizlik kısıtlaması olan kalıcı depolamada bir idempotans anahtarı olarak kullanın. Geçerli bir imza tek başına, yakın zamanda yapılan bir isteğin tekrar oynatılmasını engellemez. İşlenmiş kimlikleri en azından tüm yeniden deneme süresi boyunca saklayın; alıcı depolanan olayları yeniden işleyebiliyorsa daha uzun süre saklayın.

## Yeniden denemeler

Teslimatlar, HTTP isteklerinden önce kalıcı olarak kuyruğa alınır. En az bir kez anlamı kullanılır: kaybolan bir onay veya yeniden başlatma, bir olayı aynı kimlikle tekrar teslim edebilir. 15 saniyeden başlayıp bir saatle sınırlı olan, üstel geri çekilme özelliğine sahip sekiz deneme vardır. Başarı için 2xx yanıtı gereklidir. Sonuçsuz kalan işler görünür bir hata bırakır; yeniden denemeler sona erdikten sonra teslimat garanti edilmez.

Kuyruk 1.000 teslimatı barındırır. Dolu olduğunda, günlük olaylarının taranması duraklatılır ve yer açıldığında yeniden başlar. Kuyruğa alınamayan tam dışa aktarma işleminin tamamlanması görünür bir kuyruk hatası oluşturur. Her bildirim geçişinde en fazla beş gönderim denemesi yapılır ve en son 100 deneme kaydı saklanır. Bir hedef silindiğinde bekleyen gönderimleri de silinir.

## n8n örneği

[Örnek iş akışını](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json) içe aktarın. Bu iş akışı etkin değildir ve hiçbir gizli bilgi veya alt eylem içermez. n8n işçi ortamında `TGWITNESS_WEBHOOK_SECRET`'yi ayarlayın, bu ortama erişime izin verin ve Code düğümü için `crypto` yerleşik işlevine izin verin. Örnekte Webhook düğümünün raw-body seçeneği kullanılır, imza/güncellik kontrol edilir ve doğrulanmış olaylar onaylanır. Bu, düğümün [belgelenmiş uygulamas](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts)ına uygundur.

SIEM kayıtlarını veya bildirimlerini eklemeden önce, `event_id` ile anahtarlanmış kalıcı idempotent depolama alanı ekleyin. n8n iş akışı düzenleme ve yürütme günlüğü saklama süresini, göndermeyi seçtiğiniz verilere göre sınırlayın. TgWitness, gelen komut eklemez.
