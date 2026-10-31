# Birkaç dakika içinde başlayın

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/start/

Öncelikle, çalışan bir örneği inceleyin. Ardından kendi hesabınızı bağlayın.

## Hesap oluşturmadan siteyi inceleyin

Projeyi indirin veya klonlayın, **Python 3.11 veya daha yeni bir sürümünü** kurun ve demoyu çalıştırın. Başlatıcı, yerel bir ortam oluşturur ve sabitlenmiş bağımlılıkları yükler.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

Tarayıcı, kurgusal mesajların bulunduğu bir çalışma alanı açar. Bir sohbeti açın, bir düzenlemeyi karşılaştırın ve bir dışa aktarımı inceleyin. Demo modu Telegram'a bağlanmaz.

![Örnek mesajların yer aldığı TgWitness sohbet görünümü](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Örnek bir çalışma alanı. Kendi günlüğünüz ayrı olarak başlar.

## Kendi çalışma alanınızı oluşturun

Demo sürecini kapatın, ardından normal başlatıcıyı kullanın:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Başlatıcıda gösterilen yerel adresi açın. İstenirse, terminalde belirtilen yerel dosyadan **panel erişim jeton**unu girin. Bu işlem TgWitness'in kilidini açar; bu işlem, Telegram oturum açma işleminden ayrıdır.

## İlk mesajınızı kaydedin

1. [Özel bir Telegram hesabı bağlayın.](https://phishdestroy.github.io/TgWitness/tr/docs/accounts/)
2. Hesabın erişebileceği bir grup veya kanal seçin, ardından gözlemi başlatın.
3. Kontrolünüz altındaki bir test grubuna yeni bir mesaj gönderin ve mesajın günlüğünde göründüğünü kontrol edin.

Sunucu kurulumu için "[Keep it running](https://phishdestroy.github.io/TgWitness/tr/docs/server/)" kılavuzunu izleyin.
