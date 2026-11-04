# Çalışır durumda tutun

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/server/

Toplayıcıyı ayakta, verileri de yeniden başlatmalar boyunca güvende tutun.

## Bir başlatma yöntemi seçin

Yerel: [başlatıcı](https://phishdestroy.github.io/TgWitness/tr/docs/start/) ve [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) içindeki hizmet şablonları. Docker, proje klasöründen:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Panel localhost:8787'yi dinler. Yerelde ya da bir SSH tüneliyle, ikinci komuttaki belirteçle açın.

## Tüm veri dizinini koruyun

Yerel: `data/live`. Docker: `tgwitness-data` birimi. Günlükler, oturumlar ve anahtarlar birlikte durur. İmzalı bir dışa aktarım kanıttır, yedek değildir.

1. Önce toplamayı durdurun.
2. Tüm veri klasörünü sunucu dışında güvenli bir yere kopyalayın.
3. Güvenmeden önce ayrı bir kurulumda geri yüklemeyi deneyin.

## Yeniden başlatmanın ardından kontrol edin

Çalışma alanını ve anahtarı, bağlantıyı, kaynakları ve yeni mesajların gelip gelmediğini kontrol edin. TgWitness, Telegram'ın hâlâ tuttuğunu yakalar; kapalıyken olan her şeyi değil.

"Sağlıklı" konteyner, web sunucusunun yanıt verdiği anlamına gelir. Toplamanın çalışıp çalışmadığını bir test mesajı ve tanık söyler.

## Sadece yayınlamak istediğiniz içeriği yayınlayın

HTTPS, birimler, güncellemeler ve geri yükleme dağıtım başvurusundadır. Gerçekte neyin test edildiği: [doğrulama kaydı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/).
