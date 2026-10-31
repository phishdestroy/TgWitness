# Bir vaka paylaşın

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/access/

Birinin ihtiyaç duyduğu vakayı paylaşın. Geri kalanını kontrol altında tutun.

01**Kanıtı seçin**

Tüm hesap çalışma alanlarını veya tek tek kaydedilmiş sohbetleri seçin.

02**Eylemleri seçin**

Kişinin ihtiyaç duyduğu görüntüleme, dışa aktarma veya belirli operasyonel izinleri verin.

03**Sınırları belirleyin**

Son kullanma tarihi, oturum sınırları ve isteğe bağlı IP kısıtlamaları içeren kişisel bir jeton oluşturun.

Kayıt kapsamı, nelerin kaydedileceğini belirler. Erişim kapsamı ise bir kişinin neleri görebileceğini ve neler yapabileceğini belirler.

## Birine erişim izni verin

1. Yönetici olarak oturum açın ve "**Erişim" bölümünü** açın.
2. Erişim adını girin ve çalışma alanlarını ve sohbetleri seçin.
3. İnceleme yapan kişi için "**Görüntüle" seçeneğini** koruyun. Kayıtları indirmeleri gerekiyorsa "**Dışa Aktar" seçeneğini** ekleyin.
4. Sınırları belirleyin, ardından "**Erişim Oluştur" düğmesine** basın.
5. Görüntülenen jetonu bir kez kopyalayın. Panel adresiyle birlikte özel olarak gönderin.
6. Teslim etmeden önce ayrı bir tarayıcı oturumunda görüntülenebilirliğini kontrol edin.

## Yapmaları gereken işten başlayın

| Kişi | Erişim | Sonuç |
| --- | --- | --- |
| İnceleme Yapan Kişi | Seçili sohbetler; yalnızca görüntüleme | Toplanan verileri değiştirmeden yakalanan konuşmayı okuyun. |
| Analist | Seçili sohbetler; görüntüleme ve dışa aktarma | Vaka için gerekli kayıtları inceleyin ve indirin. |
| Operatör | Seçilmiş tüm çalışma alanları; kaynaklar ve koleksiyon | Gözlemlenenleri yönetin ve toplayıcıları başlatın veya durdurun. |

Bunlar, sabit roller değil, sizin seçtiğiniz yapılandırmalardır. Hesap genelindeki ayarlar ve tam günlük dışa aktarımları, başka bir izin etkinleştirilmiş olsa bile sohbet sınırlı erişime kapalı kalır. Tüm çalışma alanlarına erişim, gelecekteki hesapları da kapsar.

## İstediğiniz zaman fikrinizi değiştirebilirsiniz

Erişim ayarlarını düzenleyerek sonraki isteklerin neler yapabileceğini değiştirebilirsiniz. Bir oturumu sonlandırın veya tüm oturumları sonlandırmak için erişim iznini tamamen iptal edin. Zaten indirilmiş dosyalar geri alınamaz. Bir panel oturumunu sonlandırmak, veri toplama işlemini durdurmaz.

**Oturum ve IP sınırları**

Eşzamanlı oturumları ve başarılı oturum açma sayısını sınırlayın, kesin bir bitiş tarihi belirleyin, IP adreslerini veya alt ağları izin verin ya da erişimi ilk oturum açma adresine bağlayın. Oturum süresinin dolması, etkin olmama durumuna göre belirlenir; açık bir panelin yoklama işlemi etkinlik olarak sayılır. Uygulama bir proxy veya tünel arkasında çalışırken, uygulama tarafından gösterilen istemci adresini kontrol edin.

**Ana anahtar ve etkinlik günlüğü**

Ana panel jetonunu yönetici saklar. Verilen erişim yetkisi, başkalarının erişimini yönetemez veya yönetici konsolunu açamaz. Konsol, çalışma alanları genelinde mevcut işlem faaliyetlerini gösterir; imzalı erişim kayıtları, jetonlar olmadan yetki verme ve oturum olaylarını saklar. Çalışma alanları ana süreci paylaşır ve verileri sunucu yöneticisinden izole etmez.

Yedi izin, oturum kuralları ve yönetici sınırının tümü için [tam izin referansını](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) kullanın.
