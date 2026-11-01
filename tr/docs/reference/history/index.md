# Kaynak geçmişini yükle

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/

Etkinleştirilmiş kaynaklardan geçmiş mesajları yükleyin, işlemi duraklatıp devam ettirin ve imzalı bir ilerleme raporunu doğrulayın.

**Kaynaklar** bölümünde, etkinleştirilmiş sohbetleri gözden geçirin, gözlemi başlatın, ardından **"Tüm geçmişi yükle**" seçeneğini seçin. İşlem, kaynak listesini sabitler ve mevcut geçmiş mesajlarını Sohbetler bölümüne ve imzalı gözlem günlüğüne aktarır. Medya, mevcut ek ayarlarını ve kalıcı indirme kuyruğunu kullanır. Bu, sohbet başına imzalı JSON/HTML dışa aktarımından ayrıdır.

Hesap genelinde toplama yapmak için "**Tüm hesap**" seçeneğini seçin, gözlemi başlatarak kaynak listesini yükleyin ve geçmişi başlatmadan önce bu listeyi inceleyin. İletişim kutusu listesi sınırı hâlâ geçerlidir (varsayılan olarak 1.000, Parametreler'den ayarlanabilir). İşlemin başarılı bir şekilde tamamlanması, her hesap diyaloğunun listelendiğini kanıtlamaz. Daha sonra keşfedilen veya etkinleştirilen sohbetler için işlemin tekrarlanması gerekir.

## Duraklatma, yeniden başlatma ve kısmi sonuçlar

- **Geçmişi duraklatmak** okumayı durdurur. **Devam ettirmek,** her kaynaktaki en son kaydedilen mesajdan itibaren devam eder; uygulamayı yeniden başlatmak da, devam ettirilene kadar çalışmayı duraklatılmış halde bırakır. Önce gözlemi yeniden başlatın. Devam ettirmek için aynı Telegram hesabı gereklidir.
- Mesaj gözlemi, ekleme işlemi ve imleç kaydı tek bir işlemde gerçekleştirilir. Devam ettirilen bir çalıştırma, daha önce kaydedilmiş gözlemleri tekrarlamaz. Canlı yakalama veya ayrı, açıkça başlatılan bir çalıştırma, aynı mesajı bağımsız olarak gözlemleyebilir.
- Her kaynak, ilk okuma sırasında bir üst mesaj kimliği belirler. Daha yeni mesajlar, canlı gözlem kapsamına girer; o kaynağın kalan geçmiş sayfalarına dahil edilmez.
- Erişilemeyen kaynaklar ve toplama sırasında devre dışı bırakılan kaynaklar, başarısız veya atlanmış olarak görünür kalır. Diğer kaynaklar devam eder; genel sonuç eksik kalır.
- FloodWait, kaydedilen hesap geri çekilme süresine uyar. Aktarım zaman aşımları ve düşük disk alanı, imleç değişmeden çalışmayı duraklatır. Nedeni giderildikten sonra devam eder.
- **"Bu geçmiş çalışmasını sonlandır"** seçeneği, kaydedilmiş gözlemleri korur. Bunları silmez veya sıraya alınmış ek indirmelerini iptal etmez. Yeni bir çalıştırma, etkin kaynakları yeniden okur.

Geçmiş tamamlama, yalnızca geçmiş okumalarını tanımlar. Ekler beklemede kalabilir, başarısız olabilir veya yapılandırılmış ilke nedeniyle hariç tutulabilir. Günlükteki medya alım teyitlerini ve ek kuyruğunu kontrol edin; yalnızca baytları korunmuş tamamlanmış bir alım teyidi, kaydedilmiş bir eki oluşturur. Geçmiş işlemi, açık bir anlık görüntü isteğidir ve gelecekteki canlı olay kategorilerini seçen anahtarlardan ayrıdır.

## Aktar ve doğrula

**İmzalı ilerleme**raporunu kaydedin, ardından "**Kanıtları Dışa Aktar"** seçeneğini kullanarak günlüğü ve kaydedilmiş ekleri indirin. Daha sonra gerçekleştirilecek bir kanıt dışa aktarma işlemi ek kayıtlar içerebilir; rapor, sayacılarını oluşturulduğu andaki günlük önekine bağlar. Bu sürümün güvenilir bir kopyasından doğrulayıcıyı çalıştırın:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Beklenen imza anahtarı parmak izini bağımsız olarak saklayın. Doğrulayıcı, rapor imzasını, kanıt arşivini, rapor kontrol noktasını, kaynak planını, hesabı ve kaydedilmiş/erişilemeyen mesaj sayılarını kontrol eder. `--evidence` olmadan, yalnızca imzalı raporu ve iç tutarlılığını kontrol eder. İlerleme aşamaları, başlıklar, imleçler ve ek özetleri, bu rapor denetleyicisi tarafından bağımsız olarak yeniden oluşturulmamış, imzalı toplayıcı beyanlarıdır. Kanıt doğrulayıcı, arşivlenmiş medya baytlarını yine de kontrol eder.

Mevcut geçmişin imzalanması veya tamamlanması, Telegram kaynağını, atomik bir anlık görüntüyü veya tarihsel eksiksizliği kanıtlamaz. Mesajlar okunurken değişebilir; silinmiş mesajlar, görülmemiş ara düzenlemeler ve Gizli Sohbetler geri yüklenemez. İmza anahtarını kontrol eden bir operatör, dışarıdan taahhütler oluşmadan önce bir günlük uydurabilir. Belgelenmiş tahrifat algılama özellikleri için ayrı olarak saklanan kontrol noktalarını veya bağımsız bir tanığı kullanın.

Alım imleci, yerel çalışma alanının durumunu gösterir. Yalnızca bir kanıt ZIP dosyasını geri yüklemek, bekleyen bir alım işini veya Telegram oturumunu geri yüklemez. Orijinal işin devam ettirilmesi gerekiyorsa çalışma alanı yedeğini saklayın.
