# Neyin yanlış gittiğini bulun

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/troubleshooting/

Belirtiden başlayın. Her seferinde tek bir katmanı kontrol edin.

## Panel bir jeton talep ediyor

Başlatıcı tarafından gösterilen yerel dosyadaki panel jetonunu kullanın. Docker için `docker compose exec tgwitness cat /data/panel-token.txt` komutunu çalıştırın. Telegram giriş kodu, BotFather jetonu ve salt okunur tanık jetonu farklı amaçlara hizmet eder.

## Telegram bağlanmıyor

Bağlantı ayarlarını açın ve bağlantı kontrolünü çalıştırın. Genel bir proxy kullanıyorsanız, başka bir girişi deneyin ve rotayı açıkça kaydedin. Proxy türünü ve desteklenen gizli formatı kontrol edin. Genel bir listeyi yenilemek, hesabın rotasını değiştirmez.

## Bağlantı kuruldu, ancak yeni mesaj yok

1. Gözlem işleminin doğru çalışma alanında çalıştığını kontrol edin.
2. Kaynağın seçili ve o hesap tarafından görülebilir durumda olduğunu doğrulayın.
3. Kontrol altındaki bir gruba benzersiz yeni bir mesaj gönderin ve tam olarak o metni arayın.
4. Kesintiler, gecikmeler veya Telegram hataları açısından operasyon günlüğünü inceleyin.

Geçmiş anlık görüntüler ile yeni mesaj olayları birbirinden farklıdır. Sessiz bir kaynak, yeni mesajlar üretmeden bağlanabilir. Tamlık önemli olduğunda kontrollü teslimat testi kullanın.

## Yeniden başlatmanın ardından FloodWait veya bir boşluk

"FloodWait" uyarısı, Telegram'ın bir süre beklemesi gerektiği anlamına gelir. Belirtilen süreyi bekleyin ve veri toplama iş yükünü gözden geçirin; tekrar tekrar bağlanmak bu sınırlamayı ortadan kaldırmaz. Kaydedilen güncelleme durumu, yeniden başlatma sonrasında geriye kalan işleri tamamlamaya yardımcı olur, ancak süresi dolmuş güncellemeler ve bazı kesinti aralıkları sınırlamalar olarak kalır. Günlüğü tamamlanmış olarak değerlendirmek yerine, bu boşluğu kayda alın.

## Bot yapılandırılmış ancak hiçbir şey yayınlamıyor

Witness işleminin gerçekten çalıştığından, botun kanalda yayın yapabildiğinden ve Witness'ın toplayıcıya ve Bot API'sine erişebildiğinden emin olun. Günlüğünü inceleyerek başarısız yayın olup olmadığını kontrol edin. Toplayıcıya yapılan başarılı bir sorgu tek başına bir kanal yayınına dair teyit sağlamaz.

## GitHub token entegrasyonu nerede?

**Plan aşamasında.** "Extras" bölümünde, önerilen fork ve derleme doğrulama iş akışı açıklanmaktadır. Şu anda, çalışan bir kurulumun bir depo ile eşleştiğini gösteren bir GitHub jetonu formu veya otomatik doğrulama bulunmamaktadır. [Mevcut özellik durum](https://phishdestroy.github.io/TgWitness/tr/docs/reference/features/)una bakınız.

Bir sorun bildirirken sürümü, işletim sistemini, adımları ve sansürlenmiş hata mesajını ekleyin. Oturumları, jetonları, özel mesajları ve veri dizinini herkese açık sorun bildirimlerinden uzak tutun.
