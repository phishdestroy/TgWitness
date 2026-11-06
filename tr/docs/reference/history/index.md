# Telegram · Kaynak geçmişini yükle

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/

Etkinleştirilmiş kaynaklardan geçmiş mesajları yükleyin, işlemi duraklatıp devam ettirin ve imzalı bir ilerleme raporunu doğrulayın.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Koleksiyon](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Koleksiyon](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

**Kaynaklar** bölümünde, etkinleştirilmiş sohbetleri gözden geçirin, gözlemi duraklatın, Standart API veya Takeout dışa aktarımını seçin, ardından **Tüm geçmişi yükle** seçeneğini seçin. Bu işlem, kaynak listesini düzeltir ve mevcut geçmiş mesajlarını Sohbetler'e ve imzalı gözlem günlüğüne okur. Medya, mevcut ek ayarlarını ve kalıcı indirme kuyruğunu kullanır. Bu, sohbet başına imzalı JSON/HTML dışa aktarımından ayrıdır.

Hesap genelinde toplama yapmak için **Tüm hesap** seçeneğini seçin, gözlemi başlatarak kaynak listesini yükleyin ve geçmişi başlatmadan önce bu listeyi inceleyin. İletişim kutusu listesi sınırı hâlâ geçerlidir (varsayılan olarak 1,000, Parametreler'den ayarlanabilir). İşlemin başarılı bir şekilde tamamlanması, her hesap iletişim kutusunun listelendiğini kanıtlamaz. Daha sonra keşfedilen veya etkinleştirilen sohbetler için başka bir çalıştırma gerekir. Geçmişi başlatmadan önce gözlemi duraklatın; bir toplama işlemi aynı anda yalnızca bir hesaba ait olabilir.

Bir ila beş ek işleyicisi seçin ve mevcut Son İşlemleri korumak isteyip istemediğinizi belirleyin ve önceden kaydedilmiş sürümleri karşılaştırın. Veri aktarımı, Telegram’da onay ve sunucu tarafından belirlenen bir bekleme süresi gerektirebilir. Bu seçenekler, işlemin devam ettirilmesi durumunda sabit kalır. Aktarım, yeniden deneme ve güven ayrıntıları için [Geriye Dönük Doldurma davranışı ve kanıt sözleşmesine](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) bakın.

## Duraklatma, yeniden başlatma ve kısmi sonuçlar

- **Geçmişi duraklat** okuma işlemini durdurur. **Geçmişe devam et** her kaynaktaki en son kaydedilen mesajdan devam eder; uygulamanın yeniden başlatılması da devam ettirilene kadar çalışmayı duraklatır. Devam ettirmek için aynı atıl Telegram hesabı gereklidir.
- Mesaj gözlemi, ekleme işlemi ve imleç kaydı tek bir işlemde gerçekleştirilir. Devam ettirilen bir çalıştırma, daha önce kaydedilmiş gözlemleri tekrarlamaz. Canlı yakalama veya ayrı, açıkça başlatılan bir çalıştırma, aynı mesajı bağımsız olarak gözlemleyebilir.
- Her kaynak (Takeout'taki her Telegram bölünmüş aralığı), ilk okunduğunda bir üst mesaj kimliği belirler. Daha yeni mesajlar, canlı gözleme aittir; o kaynağın kalan geçmiş sayfalarına ait değildir.
- Erişilemeyen kaynaklar ve toplama sırasında devre dışı bırakılan kaynaklar, başarısız veya atlanmış olarak görünür kalır. Diğer kaynaklar devam eder; genel sonuç eksik kalır.
- FloodWait gecikmeleri, kaydedilen hesap geri çekilme süresine uyar. Geçici arızalarda en fazla beş kez yeniden deneme yapılır; kaynak tükenmesi ve düşük disk alanı durumlarında imleç olduğu gibi kalarak işlem duraklatılır.
- **Bu geçmiş çalıştırmasını sonlandırın;**, kaydedilmiş gözlemleri korur. Bunları silmez veya standart API ekleme işlerini iptal etmez. Takeout'u sonlandırmak, kalan Takeout dosyalarını atlanmış olarak işaretler; duraklatmak ise bunların devam ettirilebilir olmasını sağlar. Yeni bir çalıştırma, etkin kaynakları yeniden okur.

Geçmiş tamamlama, yalnızca geçmiş okumalarını tanımlar. Ekler beklemede kalabilir, başarısız olabilir veya yapılandırılmış ilke nedeniyle hariç tutulabilir. Günlükteki medya alım teyitlerini ve ek kuyruğunu kontrol edin; yalnızca baytları korunmuş tamamlanmış bir alım teyidi, kaydedilmiş bir eki oluşturur. Geçmiş işlemi, açık bir anlık görüntü isteğidir ve gelecekteki canlı olay kategorilerini seçen anahtarlardan ayrıdır.

## Aktar ve doğrula

**İmzalı ilerleme**raporunu kaydedin, ardından "**Kanıtları Dışa Aktar"** seçeneğini kullanarak günlüğü ve kaydedilmiş ekleri indirin. Daha sonra gerçekleştirilecek bir kanıt dışa aktarma işlemi ek kayıtlar içerebilir; rapor, sayacılarını oluşturulduğu andaki günlük önekine bağlar. Bu sürümün güvenilir bir kopyasından doğrulayıcıyı çalıştırın:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Beklenen imza anahtarı parmak izini ayrı tutun. Doğrulayıcı, rapor imzasını, kanıt arşivini, rapor kontrol noktasını, kaynak planını, hesabı ve kaydedilmiş/erişilemeyen mesaj sayılarını kontrol eder. Yeni çalıştırmalar ayrıca kaynak ilerleme durumunu ve seçenekleri imzalı imleç olaylarına bağlar. `--evidence` olmadan, yalnızca imzalı raporu ve iç tutarlılığını kontrol eder. Eski ilerleme alanları ve ek özetleri, imzalı toplayıcı beyanları olarak kalır. Kanıt doğrulayıcı, arşivlenmiş medya baytlarını kontrol eder.

Mevcut geçmişin imzalanması veya tamamlanması, Telegram kökenini, atomik bir anlık görüntüyü veya tarihsel eksiksizliği kanıtlamaz. Mesajlar okunurken değişebilir; silinen mesajlar ve mevcut Son İşlemler ile Gizli Sohbetler dışındaki ara düzenlemeler geri yüklenemez. İmza anahtarını kontrol eden bir operatör, dışarıdan taahhütler oluşmadan önce bir günlük uydurabilir. Belgelenmiş tahrifat algılama özellikleri için ayrı olarak saklanan kontrol noktalarını veya bağımsız bir tanık kullanın.

Alım imleci, yerel çalışma alanının durumunu gösterir. Yalnızca bir kanıt ZIP dosyasını geri yüklemek, bekleyen bir alım işini veya Telegram oturumunu geri yüklemez. Orijinal işin devam ettirilmesi gerekiyorsa çalışma alanı yedeğini saklayın.
