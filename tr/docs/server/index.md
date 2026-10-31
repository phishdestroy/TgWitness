# Çalışır durumda tutun

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/server/

Toplayıcıyı her zaman çalışır durumda tutun ve yeniden başlatma işlemlerinde verilerinin bozulmamasını sağlayın.

## Bir başlatma yöntemi seçin

Yerel kurulum için, [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) dizinindeki [başlatıcı](https://phishdestroy.github.io/TgWitness/tr/docs/start/)yı ve hizmet örneklerini kullanın. Docker için, Docker Compose'u kurun ve proje dizininden çalıştırın:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Varsayılan panel, ana bilgisayarın loopback adresinde, 8787 numaralı bağlantı noktasında dinleme yapar. Paneli yerel olarak veya bir SSH tüneli üzerinden açın. Panelin kilidini açmak için ikinci komuttaki jetonu kullanın.

## Tüm veri dizinini koruyun

Yerel kurulumlarda `data/live` kullanılır. Docker ise kalıcı `tgwitness-data` birimini kullanır. Günlükleri, hesap oturumlarını, anahtarları ve çalışma durumunu bir arada tutun. İmzalı bir dışa aktarım, yararlı bir kanıt olmakla birlikte tam bir kurulum yedeği değildir.

1. Tutarlı bir yedekleme almadan önce veri toplama işlemini durdurun.
2. Özel verilerin bulunduğu dizinin tamamını, ana sunucu dışındaki korumalı bir depolama alanına kopyalayın.
3. Yedeklemeye güvenmeden önce, yedeklemeyi izole bir kurulumda geri yüklemeyi test edin.

## Yeniden başlatmanın ardından kontrol edin

Beklenen çalışma alanı ve anahtarı, Telegram bağlantısını, seçilen kaynakları ve yeni mesaj yakalama işlemini doğrulayın. Kaydedilen MTProto durumu ve geriye dönük senkronizasyon, Telegram'ın hâlâ sakladığı güncellemeleri kurtarmaya yardımcı olur. Süresi dolmuş her güncellemeyi veya yakalama işleminden önce silinmiş bir düzenlemeyi yeniden oluşturamazlar.

"Konteyner durumu", web sunucusunun yanıt verdiği anlamına gelir. Toplama ve harici yayınlamayı değerlendirmek için kontrollü bir mesaj ve tanık kontrolü kullanın.

## Sadece yayınlamak istediğiniz içeriği yayınlayın

Kurulum kılavuzunda HTTPS örnekleri, kalıcı birim komutları, güncelleme ve geri yükleme adımları yer almaktadır. Kurulum için Docker komutları sağlanmaktadır; mevcut [doğrulama kaydı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/), fiilen test edilen ortamları belirtmektedir.
