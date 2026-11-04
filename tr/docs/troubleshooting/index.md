# Neyin yanlış gittiğini bulun

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/troubleshooting/

Belirtiden başlayın, her seferinde bir şeyi kontrol edin.

## Panel bir jeton talep ediyor

Başlatıcının gösterdiği dosyadaki panel belirtecini ister. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Telegram kodu, bot belirteci ya da tanık belirteci değil.

## Telegram bağlanmıyor

Bağlantı kontrolünü çalıştırın. Herkese açık bir proxy'deyseniz başka birini seçip kaydedin. Proxy türünü ve sır biçimini kontrol edin. Listeleri yenilemek rotayı kendiliğinden değiştirmez.

## Bağlantı kuruldu, ancak yeni mesaj yok

1. Gözlem çalışıyor mu, doğru çalışma alanında mı?
2. Kaynak seçili ve o hesaba görünür mü?
3. Test grubunuza benzersiz bir mesaj gönderin ve onu arayın.
4. Günlükte kesintileri ya da Telegram hatalarını arayın.

Sessiz bir sohbette yeni bir şey yoktur, o kadar. Eksiksizlik önemliyse kontrollü bir teslim testi yapın.

## Yeniden başlatmanın ardından FloodWait veya bir boşluk

FloodWait, Telegram'ın "yavaşla" demesidir. Geçmesini bekleyin ve yükü azaltın, yeniden bağlanmak işe yaramaz. Yeniden başlatmadan sonra TgWitness, Telegram'da hâlâ olanı yakalar; gerisi bir boşluktur, not edin.

## Bot yapılandırılmış ancak hiçbir şey yayınlamıyor

Tanık çalışıyor mu, bot kanala yazabiliyor mu, toplayıcıya ve Bot API'ye ulaşabiliyor mu? Günlüğünde başarısız gönderileri arayın. Toplayıcı tarafındaki bir sorgu, gönderinin çıktığı anlamına gelmez.

## GitHub token entegrasyonu nerede?

**Plan aşamasında.** "Extras" bölümünde, önerilen fork ve derleme doğrulama iş akışı açıklanmaktadır. Şu anda, çalışan bir kurulumun bir depo ile eşleştiğini gösteren bir GitHub jetonu formu veya otomatik doğrulama bulunmamaktadır. [Mevcut özellik durum](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/)una bakınız.

Hata mı bildiriyorsunuz? Sürüm, işletim sistemi, adımlar ve kişisel veri içermeyen bir hata. Oturumları, belirteçleri, özel mesajları ya da veri klasörünü asla herkese açık bir issue'ya koymayın.
