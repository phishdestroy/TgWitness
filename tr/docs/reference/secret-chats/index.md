# Telegram · Gizli Sohbetler: uygulama ve demo

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/secret-chats/

Ayrı Gizli Sohbet uygulamasını anlayın, kurgusal arayüzü deneyin ve çözülmemiş hataları inceleyin.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**6 Kasım 2026 tarihinde durum kontrol edildi:** ayrı bir Gizli Sohbet uygulaması geliştirme aşamasındadır. Bu uygulama, `3d23e52b647b` adresindeki yayınlanmış `main` dalına henüz birleştirilmemiştir. Sıradan toplayıcı ve Takeout dışa aktarma işlemi Gizli Sohbetleri toplamaz. Etkileşimli web sitesi senaryosu, kurgusal verilerle arayüzü gösterir; Telegram iletişimini etkinleştirmez.

## Uygulamanın bulunduğu yer

`0e60f88e` taahhüdü, yerel geliştirme dalı P3'te **Kaynaklar →**'ye eklendi. `bb8788fb685c`'te kontrol edilen anlık görüntü `fix/panel-routes-sessions`'tür. Uygulaması `tgwitness/secret_chats.py`, uygulama rotaları, `tgwitness/static/views/secret-chats.js` ve özel testleri içerir.

Bu daldaki isteğe bağlı `secret-chats` eklentisi, [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat)'yi kullanır ve `d87bf037b90060383c7b704d8a06ebb98c621c6f`'e sabitlenmiştir. Kütüphane, hesabın mevcut Telethon yetkilendirmesi üzerinden Telegram'ın uçtan uca sohbet protokolünü uygular. Sadece bu kütüphaneyi yüklemek, `main`'e eksik entegrasyonu sağlamaz.

## Geliştirme arayüzünün işlevleri

| Eylem | Kaydedilen davranışlar |
| --- | --- |
| Kullanıcı adı veya kullanıcı kimliği ile sohbet başlatın | Bir istek gönderin; diğer katılımcının bunu kabul etmesi gerekir. |
| Gelen bir isteği kabul edin | TgWitness, o sohbetin alıcı uç noktası olur. Otomatik kabul, varsayılan olarak kapalı olan ayrı bir ayardır. |
| Mesaj gönderin veya alın | Giden veya gelen bir `secret_chat.message` kaydı ekleyin ve bunu ileti dizisinde gösterin. |
| Ek al | Bunların şifresini çözün, baytlarını SHA-256 ve kayıt `secret_chat.file`'e göre saklayın. |
| Zamanlayıcı veya silme bildirimi alın | Uyarıyı kaydedin ve daha önce yakalanan içeriği saklayın. |
| Sohbeti gözden geçirin | Mesajları, dosyaları, bildirimleri ve anahtar görselleştirmesini gösterin. Açık sekme her dört saniyede bir yenilenir. |

Entegrasyonu içeren bir geliştirme sürümünde, operatör seçilen hesap için modülü etkinleştirir ve bağlar. Başlatma, kabul etme ve gönderme işlemleri için etkileşim izni ve hesabın salt okunur korumasının devre dışı olması gerekir. Diğer katılımcının yeni bir giden sohbeti kabul etmesi gerekir. Bu denetimler, yukarıdaki revizyondaki yayınlanmış uygulamada mevcut değildir.

Yalnızca bu TgWitness oturumu tarafından oluşturulan veya kabul edilen sohbetler kapsanmaktadır. Telefonda mevcut Gizli Sohbetler o cihazda kalır. Bir oturumun içe aktarılması, bu sohbetlerin ayrı şifreleme anahtarlarını sağlamaz. Gizli sohbet anahtar malzemesi ve sayaçlar çalışma alanı kasasında saklanır; korunan mesajlar ve şifresi çözülmüş dosyalar normal çalışma alanı depolama korumalarına tabidir.

## Web sitesi tanıtımı

Web sitesindeki **Try Secret Chat** senaryosu kurgusal bir sohbet başlatır. Bu senaryo, okuyucunun bir istek başlatmasına, bu isteğin kabulünü simüle etmesine, örnek bir mesaj göndermesine, önceden yazılmış bir yanıt ve dosya almasına ve zamanlayıcı ile silme bildirimini incelemesine olanak tanır. Gelen bir istek de kabul edilebilir. Kontroller, simüle edilen eş eylemlerini açıkça etiketler.

Bu senaryo tarayıcı belleğinde çalışır. Sıfırlama veya yeniden yükleme işlemi onu temizler. Oturum açmaz, Telegram ile iletişim kurmaz, gerçek şifreleme anahtarları oluşturmaz veya imzalı örnek indirmeleri değiştirmez. Görüntülenen mesajlar imzalı kanıt değildir. Senaryo, amaçlanan etkileşimi gösterir; geliştirme uygulamasının hazır olduğunu onaylamaz.

## Kontroller ve çözülmemiş hatalar

Mevcut beş test, şifrelenmiş anahtar kalıcılığı, yaşam döngüsü ve mesaj kayıtları, gelen kabul politikası, salt okunur gönderim ve ek dışa aktarımını kapsamaktadır. 6 Kasım'daki inceleme sırasında sabitlenmiş kütüphaneye karşı testlerden geçtiler. Üç ek sentetik kontrol, aynı anlık görüntüde kusurları yeniden ortaya çıkardı:

| Bulgular | Sonuç |
| --- | --- |
| `read_only`'yu atlayan kapatma | Etkileşimlerin engellenmesi gerektiğinde, kapatma yolu uzaktan bir eylem gerçekleştirebilir. |
| Yinelenen içerik algılama, yalnızca 500'daki son kayıtları tarar | Eski bir tekrar oynatma, yeniden başlatma sonrasında bir kopya oluşturabilir. |
| Ek indirilemediğinde, bekleyen girişi silinir | Geçici bir hata, yeniden deneme işinin kaybolmasına neden olur. |

Bunlar, [yayınlanan denetim raporunda](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) da kaydedilen açık kusurlardır. Beş başarılı test, bu hataları kapsamamaktadır. İnceleme, sentetik çalışma alanları kullanmış ve Telegram işlemlerini simüle etmiştir; canlı bir el sıkışma işlemini tekrarlamamış veya üretim ortamına dağıtımı doğrulamamıştır.
