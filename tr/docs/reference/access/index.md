# Erişim ve izinler

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/

Hesaplara ve sohbetlere kısıtlı erişim izni verin, izinleri seçin, oturumları ve IP adreslerini sınırlayın ve erişimi iptal edin.

Bir gözden geçiren kişiye bir sohbet erişimi, bir analiste bir vakayı dışa aktarma izni veya bir operatöre seçilen hesaplar üzerinde kontrol hakkı verin. Her kişi kendi jetonuna sahip olur. Ana panel jetonu ise yöneticiye aittir.

[Hesap kurulumu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) · [Bağlantı yolları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/) · [Güvenlik modeli](https://phishdestroy.github.io/TgWitness/tr/docs/reference/security/)

## İki kapsam, iki farklı görev

**Toplama kapsamı**, bir hesabın neleri kaydedeceğini belirler: seçilen sohbetler, bir Telegram klasörü veya hesabın tamamı. **Erişim kapsamı ise,** kaydedilen bu hesap ve sohbetlerden hangilerinin başka bir kişi tarafından görülebileceğini ve kullanılabileceğini belirler. Erişim izni vermek, bir Telegram sohbetine katılmak, toplama işlemini başlatmak veya Telegram hesabı izinleri vermek anlamına gelmez.

Bir erişim izni, seçilen çalışma alanlarını, bunların içindeki seçilen sohbetleri veya tüm çalışma alanlarını açabilir. **Daha sonra eklenenler de dahil olmak üzere tüm çalışma alanları,** gelecekteki hesapları da kapsar. Bir vakanın yalnızca belirli çalışma alanlarıyla sınırlı kalması gerektiğinde, bu çalışma alanlarını açıkça seçin.

## Birine erişim izni verin

1. Ana yönetici olarak oturum açın ve "**Erişim" bölümünü** açın.
2. "**Birine erişim izni ver**" bölümüne, günlüğünde tanıyabileceğiniz bir isim girin.
3. Çalışma alanlarını ve gerektiğinde bireysel sohbetleri seçin.
4. Bu kişinin yapabileceklerini seçin. "**Görüntüle" seçeneği** her zaman dahil edilir.
5. Gerektiği şekilde geçerlilik süresini, oturum açma/oturum sınırlarını ve izin verilen adresleri ayarlayın.
6. **"Erişim Oluştur" düğmesine** basın. Jetonu hemen kopyalayın: bu jeton yalnızca bir kez görüntülenir.
7. Panel adresini ve jetonu özel olarak gönderin. Alıcı, bu jetonu normal oturum açma sayfasına girer; ana panel jetonunuza veya bir Telegram oturumuna ihtiyacı yoktur.

Verilen jetonu içeren paneli ayrı bir tarayıcı oturumunda açın ve teslim etmeden önce görünür sohbetleri ve izin verilen işlemleri kontrol edin.

## İzinleri seçin

| İzin | Neleri sağlar? |
| --- | --- |
| `view` | İzin verilen sohbetleri, yakalanan mesajları, profilleri, dosyaları ve filtrelenmiş günlük kayıtlarını okuyun. Her zaman dahildir. |
| `export` | İzin verilen sohbet geçmişini ve dosyaları dışa aktarın. Tüm çalışma alanına ait kanıtların dışa aktarılması için çalışma alanının tamamına erişim gerekir. |
| `sources` | Kaynakları, anlık görüntüleri ve profil yakalamayı yönetin. Sohbet sınırlı erişim yalnızca izin verilen sohbetlerde işlem yapabilir; hesap genelinde kaynak keşfi ve kapsam ayarları kapalı kalır. |
| `collect` | Bir toplayıcıyı başlatın veya durdurun. Toplama işlemi hesabı etkilediği için tüm çalışma alanına erişim gerektirir. |
| `interact` | Erişim kapsamı dahilinde desteklenen Telegram etkileşimlerini gerçekleştirin. Sohbetle sınırlı erişimde, hesap genelinde bağlantı önizlemeleri kullanılamaz. |
| `settings` | Toplama ayarlarını, zaman damgalarını, bildirimleri, site dışı kopyaları ve parametreleri değiştirin. Tüm çalışma alanına erişim gerektirir. |
| `account` | Telegram'da oturum açın veya kapatın ve bağlantı yollarını yönetin. Tüm çalışma alanına erişim gerektirir. |

İzinler ve kapsam birlikte kontrol edilir. Bir izni işaretlemek, diğer sohbetleri açmaz veya sohbetle sınırlı erişim durumunda çalışma alanı genelinde bir işlemi etkinleştirmez. Paralel bir dışa aktarım için, erişim seçilen her hesapta dışa aktarılan sohbeti kapsamalıdır. Verilen bir erişim, yeni erişimler oluşturamaz, başkalarının oturumlarını yönetemez veya yönetici konsolunu açamaz.

### Üç faydalı kurulum

| Kişi | Kapsam | İzinler |
| --- | --- | --- |
| İnceleme Yapan Kişi | Bir vakanın kaydedilmiş sohbetleri | `view` |
| Devir teslim hazırlığı yapan analist | Araştırılacak ve dışa aktarılacak sohbetler | `view`, `export`; yalnızca Telegram üzerinden hareket etmeleri gerekiyorsa `interact`'yi ekleyin |
| Toplama operatörü | Seçilmiş tüm çalışma alanları | `view`, `sources`, `collect`; `settings` veya `account`'yi yalnızca gerektiğinde ekleyin |

Bunlar, sabit roller değil, izin onay kutularını kullanarak yapılandırabileceğiniz örneklerdir.

## Sınırlar ve oturumlar

| Ayarlar | Nasıl çalışır? |
| --- | --- |
| Paralel oturumlar | Eşzamanlı oturum sayısını 1–100 ile sınırlayın. Sınıra ulaşıldığında, bir sonraki oturum açma girişimini reddedin veya en eski oturumu sonlandırın. |
| Girişlere izin verilir | Oturum başlatmak için jetonun başarılı kullanım sayısını sınırlayın. Son izin verilen oturum açma hakkı kullanılmış olsa bile mevcut oturumlar sona ermez. |
| Geçerlilik süresi | Erişim için kesin bir son kullanma tarihi vardır. Süresi dolmuş erişim, oturum açamaz veya istek göndermeye devam edemez. |
| Etkinlik olmayan dakikalar | Oturum hareketsizlik zaman aşımı süresi, 5 dakikadan 30 güne kadar. Başarılı istekler bu süreyi uzatır; açık bir panel, yoklama yaparak kendini aktif tutabilir. |
| İzin verilen adresler | Belirli IP adreslerini veya CIDR alt ağlarını kabul edin. İlk oturum açma bağlaması etkinleştirilmedikçe, herhangi bir adrese izin vermek için bu alanı boş bırakın. |
| İlk oturum açışa bağla | İlk başarılı oturum açma işlemi, o erişim için izin verilen adresi sabitler. |

IP, uygulama tarafından görülen istemci adresidir. Ters proxy veya tünel arkasında iseniz, IP kurallarına güvenmeden önce **Açık oturumlar** bölümünde gösterilen adresi kontrol edin: aksi takdirde, birkaç kullanıcı proxy adresini paylaşıyormuş gibi görünebilir.

## Erişimi değiştirme veya geri çekme

Kapsamını, izinlerini veya sınırlarını değiştirmek için **Erişimler** altındaki bir girişi düzenleyin. Kapsam ve izin değişiklikleri, halihazırda açık olan oturumlardan gelen istekler de dahil olmak üzere sonraki isteklerde kontrol edilir. Bir erişimin iptal edilmesi, ilgili oturumları sonlandırır ve verilen jetonu kullanılamaz hale getirir. **Açık oturumlar** ayrıca, yöneticinin tüm erişimi iptal etmeden tek bir oturumu sonlandırmasına olanak tanır.

İptal işlemi, birinin daha önce indirdiği dosyaları geri getiremez. Oturumu kapatmak, paneli kilitlemek veya oturumu sonlandırmak, çalışmakta olan toplayıcıyı durdurmaz.

## Yöneticinin görebileceği bilgiler

**Bu başlangıçtan itibaren tutulan günlük,** işlem günlüklerini her çalışma alanından gelen günlük etkinlikleriyle birleştirir: oturum açma işlemleri, reddedilmeler, rota değişiklikleri ve operatör eylemleri. Bu, her mesajın kalıcı bir kopyası değil, mevcut işlem için bellek içi bir konsoldur. Sık tekrarlanan mesaj olayları, konsolu doldurmak yerine günlükte kalır.

Erişim izni verme, değiştirme ve iptal etme ile oturum başlatma veya sonlandırma işlemleri de imzalı `access.*` günlük kayıtları oluşturur. Jetonlar bu kayıtlara dahil edilmez. Verilen jetonlar ve oturum kimlik bilgileri, şifrelenmiş kasada hash değerleri olarak saklanır.

****Ana yönetici ve güven sınırı**** Ana panel jetonu kısıtlamasız kalır. Bu jetonla yapılan tarayıcı oturum açma işlemleri, yöneticinin yapılandırdığı oturum sınırlarına tabi oturumlar oluşturur. Ana jetonu doğrudan gönderen komut dosyaları tam erişim hakkını korur ve tarayıcı oturumları olarak sayılmaz. Bu, tek bir kurulumda uygulama düzeyinde erişim denetimidir. Tüm çalışma alanları sunucu sürecini paylaşır; bu, ana bilgisayar yöneticisinden izolasyon anlamına gelmez. Ana tokeni, Telegram oturumlarını, imzalama anahtarlarını ve veri dizinini gizli tutun. Tanık tokeni, panel erişim tokeni değil, ayrı bir kontrol noktası/durum kimlik bilgisidir.
