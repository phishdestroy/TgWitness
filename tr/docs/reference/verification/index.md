# Neler test edildi

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/

Canlı Telegram testi, otomatik kontroller, tarayıcı kontrolleri ve henüz doğrulanmamış olan unsurlar.

## Canlı Telegram testi, tüm hesap · 29 Ekim 2026

Aşağıdaki testin ardından aynı hesap çalışmaya devam etti. 29 Ekim saat 12:10 UTC'de kapsamı tüm hesaba (kanallar, gruplar, özel sohbetler ve botlar) genişletildi; panel onay istedi ve imzalı günlük bunu kaydetti. Saat 17:59 UTC itibarıyla günlükte şunlar yer alıyordu:

| Kayıt tarihi: 27 Ekim 21:36 – 29 Ekim 17:59 UTC | Sayım |
| --- | --- |
| Günlük kayıtları | 9,968 |
| Yeni mesajlar | 5,308 |
| hesabın tamamına geçişten sonra bunların | 3,878 |
| Silme işlemleri | 784 |
| TgWitness mesajı kaydettikten sonra silinenler | 596 |
| Düzenlemeler | 41 |
| Yeniden kontrollerle eklenen mesajlar | 2,273 |
| Yeniden kontrol sonucunda artık bulunamayan mesajlar | 18 |
| Geçmiş anlık görüntüleri ile kaydedilen mesajlar | 242 |
| Kaydedilen ekler | 247 |
| Toplayıcı başlatılıyor | 19 |
| Telegram FloodWait duraklatılır | 26 |

- Panelin **Verify** kontrolü, 9.968 kaydın tamamının imzalarını ve hash zincirini doğruladı.
- Mesajlar 2 grup veya kanaldan ve 3 özel sohbet ile botlardan geldi. **Sohbetler** bölümünden bir mesaj düğmesi basıldı; istek ve Telegram'ın yanıtı günlüğünde yer almaktadır.
- Toplayıcı, yeniden başlatma sırasında hesabı yeniden taradığında yeni sohbetler eklendi. Yeni sohbetlerin önceki mesajlarının kaydedilmesi devre dışıydı (`history = 0`), bu nedenle bu konuda burada yer almamaktadır.

Kapsam dışı olanlar: tepkiler, üyelik değişiklikleri, kişi profilleri, mesaj gönderme, davet yoluyla katılma, vekiller, bildirimler, witness botu ve aynı anda birden fazla hesap. Genel dosyalar yalnızca sayı bilgilerini içerir.

## Şifre korumalı dışa aktarım, libarchive ile açıldı · 29 Ekim 2026

Dışa aktarma şifreleme kodu ile oluşturulmuş bir arşiv (WinZip AES-256, 7-Zip ve WinRAR tarafından okunabilen format), Windows `tar` (bsdtar 3.6.2, libarchive) ile açıldı. Doğru şifre girildiğinde çıkarılan dosyanın SHA-256 değeri orijinaliyle eşleşti; yanlış şifre girildiğinde ise "Yanlış şifre" uyarısı verildi. 7-Zip ve WinRAR programları çalıştırılmadı.

## Canlı Telegram testi · 27–29 Ekim 2026

Yerleşik API çift havuzu aracılığıyla oturum açılmış tek bir gerçek Telegram hesabı, **27 Ekim 21:36 UTC**'den **29 Ekim 05:15 UTC'ye kadar** bir süper grubu kaydetti. Toplayıcı, bu süre zarfında 12 kez başlatıldı.

| Kaydedildi | Sayım |
| --- | --- |
| Kalp atışları ve hizmet kayıtları dahil olmak üzere günlük kayıtları | 2,385 |
| Yeni mesajlar | 1,291 |
| Silme işlemleri | 472 |
| TgWitness metni kaydettikten sonra silinenler | 347 |
| Düzenlemeler | 12 |
| Durdurulmuşken kaçırılan mesajlar, yeniden kontrol sırasında eklenmiştir | 12 |
| Kaydedilen ekler | 17 |
| Ekler indirilmedi (indirme özelliği kapalı veya indirilecek dosya yok) | 14 |
| Telegram FloodWait, yeniden kontroller sırasında her seferinde 3 saniye ara verir | 8 |

- Toplam 2.385 kaydın imzaları ve hash zinciri, günlüğün açık anahtarıyla doğrulanır.
- Yeniden başlatmanın ardından toplayıcı, kaydedilmiş güncelleme durumundan (`pts`) devam eder ve Telethon eksiklikleri giderir; ardından yeniden kontrol işlemi, hâlâ eksik olan mesajları ekler.
- Her FloodWait durumunda, toplayıcı istenen süreyi bekledikten sonra işleme devam etti.
- Hesap oturum açık kaldı ve aynı oturum 29 Ekim'de yeniden bağlandı.

Bu test kapsamında olmayanlar: aynı anda birden fazla hesap, yönetici rolleri, proxy'ler, birkaç saatten uzun süren kesintiler ve tam [canlı kabul prosedürü](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Halka açık dosyalar yalnızca şu bilgileri içerir: hesap veya sohbet kimlikleri, mesajlar ya da kimlik bilgileri bulunmaz.

Aşağıdaki eski kayıtlar kendi çalıştırma sonuçlarını açıklamaktadır; bunların çoğunda sentetik test istemcileri kullanılmıştır. En son otomatik sonuçlar aşağıdadır.

## Yerleşik genel MTProxy listeleri · 29 Ekim 2026

Bu, orijinal manuel seçim sürümünün geçmiş test kaydıdır. Güncel otomatik havuz ve IP modları için [bağlantı ayarlarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes) bakınız. Aşağıdaki sayılar ve desteklenmeyen özellikler, test edilen o sürüme aittir.

SoliSpirit/mtproto ve zakky8/mtproto-proxy-pro kaynaklarından bir paketlenmiş genel anlık görüntü ve açık HTTPS yenileme eklenmiştir. Bu sunucuda, uygulama indiricisi her iki beslemeyi de 29 Ekim 2026 tarihinde saat 12:58 UTC'de başarıyla aldı: filtreleme, tekilleştirme ve kaynak başına 64 giriş sınırlamasından sonra **118 benzersiz uyumlu uç nokta**. Bu, liste alımını doğrular; bağlantı durumunu veya bu uç noktalar üzerinden mesaj iletimini doğrulamaz. Bu çalışma sırasında listelenen bir proxy’ye gerçek bir hesap bağlanmamıştır. [Operatör ve kullanıcı kılavuzu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Başarısız/boş/uyumsuz kaynak yanıtları, önceki girişleri ve tarihleri korur. Güncellemeler seçilen rotayı değiştirmez. Genel adresler doğrulanır ve seçildiğinde IP'ler sabitlenir; operatör/manuel rotalar ayrı kalır. Bağlantı testi artık hesap girişinden önce panelde kullanılabilir. Sahte TLS ee ve otomatik proxy seçimi hala desteklenmemektedir. Operatör kataloğu, abonelikleri tamamen geçersiz kılar.

- Tam test paketi: **366 başarılı, 3 atlandı**, 287,94 saniye. Mevcut bağımlılık uyarıları ve platform atlamaları devam ediyor. Son public-list/yerelleştirme regresyon testi: **36 başarılı**, geçersiz indirme proxy bağlantı noktalarının reddedilmesi dahil; bu, tam test paketiyle örtüşmektedir.
- İngilizce/Rusça dillerinde, açık/koyu modda 390/1440 piksel çözünürlükte tarayıcı uyumluluğu testinden geçmiştir: bir arada sunulan seçenekler, ayarların açılması sırasında harici veri alımı yok, açık yenileme, arızalar sırasında yolların ve önbelleğin korunması, oturum açma öncesi denetimi, geç yanıt durumunda çalışma alanı yalıtımı, kaynak ayrıntıları ve düzen/kontrast. JavaScript hatası veya harici tarayıcı isteği yok.
- 13 dilin tümü için nihai statik çeviri kapsamı onaylandı; yeni metin Rusçaya çevrildi ve diğer yerlerde açıkça belirtilmiş İngilizce yedek metinler kullanıldı. Güncellenen yerleşik kılavuz, her iki temada da mizanpaj/kontrast kontrollerinden geçti.
- Ruff ve yayın kontrolleri başarıyla tamamlandı (259 genel dosya, 1.354 yerel bağlantı); güncellendi. Compose ve CI YAML dosyaları ayrıştırıldı. Docker ve uzaktan CI burada çalıştırılmadı.
- Yeniden geliştirilen araç, tek başına kurulum, paket listesi yükleme ve imzalı dışa aktarım doğrulama testlerini geçti. 69 paket kaynağının tamamı çalışma alanıyla eşleşti; kaynak hash değerleri kontrol edildi.

Makbuzlar: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` ve `test-results/public-proxies-package.log`. Tarayıcı/hesap/aktarım ayarları sentetiktir; yukarıdaki iki besleme indirme işlemi gerçek HTTPS istekleridir.

## İsteğe bağlı ek özelliklerin sunumu · 29 Ekim 2026

Eski Proof botu sayfası artık **"Extras"** olarak adlandırılıyor: kısa bir genel bakışın ardından seçilen seçenek için ayrı bir kurulum sayfası geliyor. Witness formu üç adımdan oluşuyor; bağlantı yönetimi, ağ seçenekleri ve dağıtım ayrıntıları ise katlanmış durumda. GitHub açıkça planlanmış ve kimlik bilgisi formu bulunmuyor. [Rusça genel bakış](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- Yerelleştirme, tanık kurulumu ve yayın denetimleri için 30 odaklanmış testten başarıyla geçilmiştir.
- Chromium kurulum kabul testi, İngilizce/Rusça, açık/koyu modda, 390/1440 piksel çözünürlükte başarıyla geçildi: klavye odağı ve Enter tuşu, ek özellikler seçildiğinde örtük bağlantılar oluşmaması, taslak saklama, sabitlenmiş yapılandırma/token indirmeleri, kilitlendiğinde token silme ve çalışan yerel kılavuz bağlantıları. Mizanpaj ve düz arka plan metin kontrast kontrolleri başarıyla tamamlandı.
- Çalışma alanı geçişi kabul edildi; buna, geçişten sonra gecikmeli olarak gelen token yanıtı da dahildir. Hızlı gezinme özelliği sayesinde bot, kanıt ve GitHub terimleri aracılığıyla ek özelliklere ulaşılabilir; mevcut 320/390/1440 piksel ve Rusça/RTL kontrolleri de başarıyla geçildi.
- Kurulum çalışması sırasında herhangi bir JavaScript hatası veya harici tarayıcı isteği gözlemlenmedi. Bunlar sentetik kullanıcı arayüzü kontrolleri olup, yeni canlı Telegram veya bot yayın kanıtları değildir.
- 13 dil ayarının tümü için son dil yükleme ve sözlük kapsamı testleri başarıyla tamamlandı; Rusça dışında açık İngilizce yedek metinler korunmuştur. Genişletilmiş Proof kılavuzu da her iki temada 320/768/1440 piksel çözünürlüklerde mizanpaj/kontrast kontrollerinden geçmiştir.
- Yeniden oluşturulan sürüm, izole kurulum ve imzalı dışa aktarım doğrulamasını geçti. Paketlenmiş 67 kaynağın tümü çalışma alanıyla uyumluydu; kaynak arşivinde 253 adet genel erişime açık dosya bulunmaktadır. 1.346 yerel dokümantasyon bağlantısı için kaynak/bağlantı kontrolü başarıyla tamamlandı.

Makbuzlar: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` ve `test-results/extras-artifacts.json`. Ekran görüntülerinde sentetik çalışma alanları kullanılmıştır.

## Witness botu ve proxy kurulum denetimi · 29 Ekim 2026

Witness kurulumu (artık **Ekstralar → Kanalınızda bir bot**), bağımsız olarak dağıtılmış bir witness hazırlar: sabitlenmiş toplayıcı anahtarı, kapsamlı token indirme, kendi kanalı, yayın politikası, HTTP/SOCKS5 rotası ve özel Bot API. Bot belirteci tanık sunucusunda kalır. Yeni `--check-config`, bir ağ bağlantısı açmadan veya anahtar oluşturmadan yapılandırmayı ve dosyaları doğrular. JSON dosya yolları, yapılandırmanın yanında çözümlenir. Tüm Compose tanık varyantları artık HTTP proxy ve Bot API ayarlarını iletir.

Hesap ayarları, operatör tarafından yönetilen genel bir MTProxy kataloğunu, özel Telegram proxy bağlantısı önizlemesini ve mevcut manuel alanları destekler. Katalog yanıtlarında gizli bilgiler yer almaz; seçim yapıldığında rota, çalışma alanı kasasına kaydedilir. Eksik veya hatalı biçimlendirilmiş kataloglar durumunda manuel rotalar kullanılabilir kalır. Varsayılan olarak hiçbir proje proxy adresi veya barındırılan tanık hizmeti oluşturulmaz veya etkinleştirilmez. Bir Caddy örneği, paneli gizli kalan bir toplayıcıya harici bir tanığın ulaşması gerektiğinde yalnızca kapsamlı baş uç noktasını gösterir.

Doğrulama:

- Tam test paketi: **348 test başarılı, 3 atlandı**, 195,81 saniye. Atlamalar, Windows'un getirdiği kısıtlamalardan kaynaklanmaktadır; mevcut iki bağımlılık kullanımdan kaldırılma uyarısı hâlâ devam etmektedir.
- Son tanık/yapılandırma/sürüm regresyon çalışması: **11'i geçti, 1'i atlandı**. Bu, tam test paketiyle örtüşmektedir. Testler arasında yol çözümleme, çevrimdışı ön kontrol, gerçek bir loopback HTTP Bot API fikstürü aracılığıyla imzalama/yayınlama, kaydedilmiş teslimat hatası, kanal jetonu doğrulaması ve proxy gizli anahtarının hariç tutulması yer almaktadır.
- Chromium kurulum onayı, 390/1440 piksel çözünürlükte İngilizce/Rusça dillerinde başarıyla tamamlandı: sabitlenmiş yapılandırma ve token indirmeleri, kilitlendiğinde token temizleme, katalog seçimi, özel bağlantı önizlemesi ardından açık bir şekilde kaydetme, düzen/kontrast ve JavaScript hatası ya da harici tarayıcı isteği yok. Rusça hesap başlığındaki darlık ve oturum açma sekmesindeki taşma sorunu düzeltildi.
- Ruff, kaynak/bağlantı kontrolleri ve Compose/iş akışı YAML ayrıştırması başarıyla geçildi.
- Yeniden geliştirilen araç, izole kurulum, panel/statik kaynak ve API kimlik doğrulama kontrollerinin yanı sıra, doğrudan ve akış yoluyla gerçekleştirilen 32 olaylık sentetik dışa aktarımların bağımsız doğrulamasını da başarıyla geçti.

Makbuzlar: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` ve `setup-package.log`. Bu kontroller, sentetik hesaplar/proxy'ler ve yerel bir Bot API fikstürü kullanır. Bunlar, gerçek bir bot yayını, çalışan halka açık MTProxy sunucusu, uzaktan CI çalıştırması veya Docker dağıtımı olduğunu iddia etmez. Yukarıda tutulan gerçek Telegram gözlem geçmişi, ayrı bir delil parçası olarak kalır. [Kurulum talimatları](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Sunum ve dokümantasyon incelemesi · 29 Ekim 2026

Ürün sayfası, erişim ekranı, İngilizce/Rusça README dosyaları ve sunum görselleri artık tek bir görsel stile sahiptir. Halka açık ekran görüntülerinde kurgusal demo verileri kullanılmaktadır. Gözden geçirme sürecinde, yukarıdaki güncelliğini yitirmiş canlı doğrulama ve kurtarma açıklamaları da düzeltilmiştir.

- Odaklanmış yerelleştirme, site ve yayın testleri: **33'ü geçildi, 1'i atlandı**. Atlanan test, bu sunucuda kullanılamayan sembolik bağlantı oluşturulmasını gerektiriyor.
- Tüm dil katalogları, RTL düzeni, açık/koyu temalar, metin kontrastı ve çalışma alanı değiştirme dahil olmak üzere genel Chromium paneli onayı geçti. Profil oluşturma kontrolü artık seçilen çalışma alanını kontrol etmeden önce gerçek HTTP yanıtını bekliyor.
- İngilizce/Rusça erişim ekranları, her iki temada da 320, 390, 768, 850 ve 1440 piksel çözünürlüklerde mizanpaj ve kontrast kontrollerinden geçmiştir; gönder düğmesi ilk görüntü alanında kalmaktadır.
- 320, 390, 768, 1024 ve 1440 piksel çözünürlüklerde, mesaj geçmişi denetimleri, ekran görüntüsü büyütme/Escape/odak geri dönüşü, klavye sekmeleri, panoya kaydetme reddi, proje alt yolları, hareket azaltma ve JavaScript'siz yedekleme dahil olmak üzere 320, 390, 768, 1024 ve 1440 piksel çözünürlüklerde kabul edildi. Başarısız varlık istekleri, harici istekler veya JavaScript hataları gözlemlenmedi.
- Yeniden oluşturulan tekerlek, izole kurulum kontrolünden geçti: panel kaynakları ve yerel ayarlar yüklendi, API erişimi kimlik doğrulaması gerektiriyor ve doğrudan/akışlı dışa aktarımlar, 32 sentetik olayın tümünü bağımsız olarak doğruladı. Ruff ve açık kaynak/bağlantı kontrolleri başarıyla geçti.

Yerel makbuzlar: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` ve `design-package/install-receipt.json`. Bu sunum/belgeleme değişikliği için arka uç paketinin tamamı yeniden çalıştırılmamıştır; önceki sonuç, yayın öncesi denetimde yer almaktadır.

## Sürüm 0.6.1

0.6.1 sürümü, panel görünümü, başlatıcılar, paketleme ve belgelerde değişiklikler içerir; toplama, depolama, imzalama ve dışa aktarma kodunda değişiklik yoktur. Windows 11 / Python 3.12.10 sürümünde, sabitlenmiş çalışma zamanı ile:

- Tam paket, **2 atlama** ve mevcut Starlette uyarısı ile birlikte **137 testi** geçti. Yeni testler, başlatıcının Ctrl+C komutunu işleme biçimini (sunucuya düzgün bir şekilde durması için 30 saniye süre verilir) ve eyleme geçirilebilir kurulum adımı hatalarını kapsamaktadır.
- Chromium (headless shell 156), **45 genel senaryonun** tamamını ve **35 hesap içe aktarma/QR/Oturum Açma Anahtarı senaryosunu** başarıyla geçti; bunlar arasında düz metin kontrast kontrolü, 320–1440 px'te yatay taşma olmaması ve 320/390 px'te ilk oturum açma alanlarının görünür olması da yer alıyor. Sayfada herhangi bir JavaScript hatası veya harici istek gözlemlenmedi.
- `python start.py --setup-only`, paketi 0.6.1 sürümü olarak yeniden yükledi ve `python start.py --check` hazır olduğunu bildirdi. Gerçek bir `python -m tgwitness --demo` sunucusu paneli, stil sayfasını, komut dosyasını, logoyu, kılavuzu ve `/api/status` 0.6.1 sürümünü döndürdü; kaldırılan `workspace.css` ise 404 hatası verdi.
- `Start.cmd`, PATH dışında bir Python kurulumu buldu. Kullanılabilir Python bulunmadığından kurulum teklifi gösterildi; basılı kılavuz talimatları reddedildi ve 1'den çıkıldı. python.org indirme adımı, 3.12.10 kurulum programını aldı ve Python Software Foundation Authenticode kontrolünden geçti; kurulum programı bu ana bilgisayarda çalıştırılmadı.
- Python komutu olmadan `start.sh`, kurulum ipucunu yazdırdı ve çıktı. 1. `scripts\Docker.cmd` ve `scripts/docker-start.sh`, sahte `docker` yürütülebilir dosyalarına karşı test edildi: doğru çağrı sırası, panel adresi ve token çıktısı; hata durumunda başarı mesajı yok.
- `python tools/build_portable.py`, sabitlenmiş embeddable-runtime sağlama toplamını doğruladıktan sonra 18,8 MiB boyutunda bir Windows paketi oluşturdu. Boşluk içeren bir yola açıldığında ve PATH'te yalnızca `C:\Windows` dizinleriyle başlatıldığında, gömülü Python'u `TgWitness-Check.cmd`'yi geçti, demoyu (32 olay) ve canlı çalışma alanını sundu; Chromium ise günlüğü ve ayrıntı çekmecesini JavaScript hatası olmadan görüntüledi. Veriler, paketin `data` klasörüne yazıldı.
- `python tools/build_preview.py`, 110 dosyadan oluşan bir kaynak arşivi oluşturdu. `git add`'nin deneme çalıştırmasında, oturum, anahtar, veritabanı, jeton, günlük veya dışa aktarım dosyaları, yerel mutlak yollar ve gizli bilgi içeren dizeler bulunmayan aynı 110 dosya listelendi.

27 Ekim tarihli bu özel paketleme çalışmasında gerçekleştirilmeyenler: otomatik Python kurulumu, Docker derleme/Compose kontrolleri, Linux/macOS çalıştırmaları veya yeni bir canlı hesap denemesi. Gerçek Telegram kanıtları yukarıda ve aşağıdaki önceki hesap kontrollerinde kaydedilmiştir. CI tanımları tek başına platformun çalışır durumda olduğunu kanıtlamaz.

## Sürüm 0.6.0

Windows 11 / Python 3.12.10 üzerindeki en son tam sabitlenmiş çalışma zamanı paketi, **135 testi 1 atlama** ile 26,53 saniyede geçti; mevcut Starlette uyarısı da mevcuttu. Atlanan test, POSIX izinlerini gerektiriyor. QR görüntüleyicisini hazırlık kontrollerine ve işlem ölçümlerine ekledikten sonra, etkilenen 8 hazırlık/çalışma alanı kontrolü de başarıyla geçti.

Yeni kapsama alanları arasında Telethon şemaları 7/8, Pyrogram şemaları 2/3, eksiksiz JSON anahtarları ve yalnızca meta veriler içeren JSON, eşleşen/çakışan hesap dosyaları, TData şifreleri, sağlama toplamı tahrifatı ve güvenli olmayan yollar, çevrimdışı/kimlik doğrulamalı bellek içi dönüştürme, çevrimiçi hesap kimliği kontrolleri, QR başarısı/2FA/süre dolumu, eski iptal ve hesap izolasyonu. TData fikstürleri, şifreleme için ayrı bir AES-IGE uygulaması kullanır.

Chromium, **45 genel senaryoyu** ve **35 hesap içe aktarma/QR/Oturum Açma Anahtarı senaryosunu** geçmiştir; bu süreçte herhangi bir sayfa JavaScript hatası veya harici istek gözlemlenmemiştir. Yeni tarayıcı kontrolleri, dört giriş formatının tümünü bir arada kapsıyor: korumalı TData, API meta verileri, QR görüntüleme, süre dolumu/yeniden deneme, 2FA, yanlış hesap reddi, kilitleme/çalışma alanı iptali, duyarlı düzen ve yeni bir dosya seçimi sonrasında gecikmeli dönüştürme yanıtları.

Hesap girişi değişikliklerinin ardından her iki tarayıcı paketi de tekrar testi geçti. Canlı kurulumda hesap formu açılır; demo modunda ise örnek kayıt defteri açılır. Demo Hesap sayfası, canlı başlatma talimatlarını gösterir ve kimlik bilgisi giriş alanlarını gizler. 320, 390 ve 1440 pikselde yapılan odaklanmış kontroller, sayı alanının ve ana düğmenin kaydırma gerektirmeden sığdığını, API alanlarının başlangıçta daraltılmış olduğunu ve metin kontrastının okunabilir kaldığını doğruladı. Yakalama ve doğrulama kontrolleri, yeni genişletilebilir bölümleri açıldıktan sonra da gizli kalır.

Doğrudan Oturum Açma Anahtarı akışı, gerçek ithalat ve yetkilendirme uç noktaları üzerinden sentetik kimlik bilgileriyle test edildi. Kontroller, eksik anahtarlar, eksik DC, hatalı Kullanıcı Kimlikleri, uyuşmayan hesap kimliği, kaydedilmiş API kimlik bilgileri, görünür istek ilerlemesi, gizli bilgilerin silinmesi ve düzenlemeler veya yöntem değişikliklerinden sonra geciken yanıtları kapsamaktadır. Dört oturum açma yönteminin tümü 320, 390 ve 1440 piksel çözünürlüklerde kontrol edildi. Dosya seçici, biçim kılavuzundan önce gelir ve “Bağlan” düğmesi, API ayarları daraltılmış haldeyken ilk 844 piksel görüntü alanına sığar. Bu kullanıcı arayüzü kabul testinde gerçek bir Oturum Açma Anahtarı yetkilendirme denemesi yapılmadı.

Panel yenilemesi her iki tarayıcı paketiyle tekrar kontrol edildi: sayfada JavaScript hatası veya harici istek gözlemlenmedi. Hesap paketi artık tek bir API kimliği/hash çiftinin yapıştırılmasını, alanları değiştirmeden hatalı biçimlendirilmiş veya birden fazla çiftin reddedilmesini, yalnızca meta veriye dayalı kılavuzluk ve oturum açma yönteminin değiştirilmesi veya kimlik bilgilerinin manuel olarak düzenlenmesinden sonra geçerliliğini yitirmiş içe aktarma yanıtlarının göz ardı edilmesini kapsamaktadır. Kurulum kılavuzu, açık başlatma/duraklatma, boş arama kurtarma ve son bağlantı/yerel kılavuz düzeni ile 320, 390 ve 1440 pikselde sağlam metin kontrastı için altı ek odaklanmış kontrol başarıyla geçildi. Doğrudan oturum açma güncellemesi, tek bir telefon/kod isteği işlemi ekler ve telefon, QR ve oturum açma için mevcut çalışma alanındaki kaydedilmiş API çiftini yeniden kullanır. Yukarıdaki tam Python paketi, yeni kalıcılık, kısmi kimlik bilgisi reddi ve çalışma alanı izolasyonu testlerini içerir. Tarayıcı kontrolleri, doğrudan telefon girişi, kaydedilmiş kimlik bilgilerinin yeniden kullanımı, yalnızca meta veriye dayalı yönlendirme, tek tuşla dosya yetkilendirme ve yinelenen hesap reddi konularını kapsamaktadır. Basitleştirilmiş panel jetonu ve telefon formları da 320, 390 ve 1440 piksel çözünürlüklerde başlangıçta kaydırma yapılmadan kontrol edildi. Bir uyumluluk kontrolü, doğrudan telefon formunun eski bir işlem hala çalışırken önceki yapılandırma/kod uç noktalarını kullanabileceğini doğruladı.

Kullanıcı tarafından sağlanan bir hesap, genel test düzenekleri dışında ayrı olarak kontrol edildi. Telethon, Pyrogram ve TData girdileri aynı yetkilendirmeye karşılık geldi; eşlik eden JSON dosyası API kimlik bilgilerini sağladı. Dört dosyanın tümü 0.6.0 paneli aracılığıyla yüklendi ve Telegram, beklenen sayısal hesap kimliğini doğruladı. Kaynak dosyalar değişmeden kaldı. Hiçbir kaynak seçilmedi ve gözlem özelliği kapalı kaldı. Bu, canlı veri toplama, kurtarma veya kapasite değil, yalnızca bir içe aktarma/giriş örneğini oluşturur.

Telegram ayrıca gerçek bir QR jetonu da yayınladı; bu jeton taranmadan iptal edildi. QR onayı ve 2FA akışlarının tamamı sentetik istemcilerle test edildi; gerçek bir Telegram uygulamasına karşı mobil onay ise ayrı bir kabul adımı olarak kalmaktadır. Halka açık dosyalarda gerçek hesap tanımlayıcıları, gizli bilgiler veya ekran görüntüleri yer almamaktadır.

Başlatıcı güncellemesi tamamlandı; kaynak, yüklü meta veriler ve hazırlık işaretçisi 0.6.0 raporunda, qrcode 8.2 ve geçerli `pip check` değerleriyle belirtilmiştir. Yüklü tekerlek, panele ve kılavuza hizmet etti, kimliği doğrulanmamış API isteklerini reddetti ve bağımsız olarak doğrudan ve akış halinde 32 olaylık sentetik dışa aktarımları doğruladı. Güncellenen çevrimdışı kılavuz 320, 390 ve 1440 piksel çözünürlüklerde kontrol edildi. Halka açık ekran görüntüleri sentetik olmaya devam ediyor.

Kaynak sürüm, izin listesine alınmış 107 dosya içerir. Yerel dokümantasyon bağlantıları çalışır durumdadır. Docker/Caddy çalıştırma, uzaktan CI/paket yayınlama, ARM64 çalışma zamanı, sürekli veri toplama ve tam canlı Telegram kabul matrisi burada henüz desteklenmemektedir.

## Sürüm 0.5.1

Windows 11 / Python 3.12.10 üzerinde, tam proje ortamı paketi başarılı oldu: **94 test başarılı, 2 atlandı**, 31,21 saniyede tamamlandı; mevcut Starlette uyarısı ile. Atlanan testler, bu ana bilgisayarda mevcut olmayan POSIX izinleri ve sembolik bağlantı oluşturma gerektiriyor. İndirme HTTP fikstürü bir istek iş parçacığı tanılama çıktısı verdi; tüm doğrulamalar başarılı oldu. Bu çalıştırma, ana bilgisayarda aktarım sorunlarının bulunmadığını garanti etmez.

Yeni regresyon kapsamı çalışmaları, StringSession, kod ve 2FA hesap değişikliklerini reddetti, kimlik aramasını iptal etti, bekleyen oturum açma iptallerini ve aktif, reddedilmiş, yerine geçirilmiş ve deneme istemcilerindeki kayıtlı işleyiciler aracılığıyla yapılan güncellemeleri kapsam dışına aldı. Yalnızca aktif toplayıcı olaylara katkıda bulunur; kaydedilmiş kimlik bilgileri ve imzalı geçmiş bozulmadan kalır. Diğer yeni kontroller arasında, veritabanının yeniden açılmasından sonra Unicode araması, Coverage’a izleme politikası sınırlarının dahil edilmesi ve açık kaynak paketleme hariç tutmaları yer almaktadır.

`pythonw.exe` adlı asıl proje, izole edilmiş bir sentetik panel başlattı, HTTP 200 yanıtı verdi ve başlangıç tanılama bilgilerini `logs/server.log`'de sakladı. Günlük dosyasında, oluşturulan panel jetonu veya HTTP erişim kayıtları yer almıyordu. Test, yalnızca kendi sentetik sürecini sonlandırdı. Görev Zamanlayıcı’da herhangi bir görev kaydedilmedi; oturum açma/kapatma, uyku modu ve hizmet kurtarma ayrı yeterlilikler olarak kalmaktadır.

Chromium kabul testi **45 senaryoyu** başarıyla geçti; sayfada JavaScript hatası gözlemlenmedi ve harici istek de tespit edilmedi. Yeni kontroller arasında 601/768/850 piksel zaman çizelgesi tarih ve saatleri, durum güncellemesi sırasında ek taslakları, kaydetme sırasında yapılan yeni düzenlemeler, hesap değiştirme sırasında silinen doğrulama sonuçları, başka bir sayfaya geçip geri döndükten sonra geciken doğrulama yanıtları ve yeni olaylar geldiğinde belirgin doğrulama sınırları yer almaktadır. Arama simgesi/metin aralığı da düzeltildi ve tarayıcı paketi yeniden çalıştırıldı.

Tarayıcı çalıştırmasında, `.venv`'deki sabitlenmiş çalışma zamanı ve mevcut sistem tarafından sağlanan Playwright 1.62.0/Chromium kullanıldı; bunlar, içe aktarma yolundaki proje ortamının sonuna eklendi. Playwright'ın yavaş indirme işlemi sırasında isteğe bağlı bir geliştirme bağımlılığı yüklemesi durduruldu; yeni bir tarayıcı aracı sürümü onaylanmadı. Normal bir `python start.py --setup-only` işlemi, uygulama yükseltmesini tamamladı. Kaynak, yüklü meta veriler ve başlatıcının işaretçisi 0.5.1 sürümünü bildirdi; `pip check` testi başarılı oldu. Hazırlık kontrolleri, beklenen yerel kasa anahtarı uyarısını koruyarak, yeni ve kullanılmamış bir yolda başarılı oldu.

0.5.1 sürümü ayrı olarak kuruldu ve temel testlerden geçirildi: tüm panel/kılavuz öğeleri sunuldu, kimlik doğrulaması yapılmamış API erişimi reddedildi ve hem doğrudan hem de akış yoluyla alınan 32 olaylık kanıt ZIP dosyaları bağımsız doğrulamadan geçti. Yüklenen paketteki uygulama dosyaları kaynak kodla karşılaştırıldı. Halka açık kaynak arşivi, açık bir dosya türü izin listesi kullanır ve bağlantılı kaynak dosyalarını reddeder; kaynak dizinlerinin içine yerleştirilen çalışma zamanı materyalleri regresyon testleri tarafından hariç tutulur.

Kod düzeltme çalışması sırasında, açık kaynak seçimi ve Git aday kümesi 86 dosya içeriyordu; bunlara çalışma zamanı veri dizinleri dahil değildi. Tanınabilir özel anahtar, GitHub jetonu, Telegram bot jetonu ve StringSession kalıpları için yapılan taramada hiçbir eşleşme bulunamadı. Bu, sınırlı bir kalıp kontrolüdür; kapsamlı bir gizli bilgi denetimi değildir. Yoksayma kuralı denetimleri, on iki yaygın hesap/veri/dışa aktarma öğesini kapsamaktadır. İş akışı/sorun/Compose YAML ve Windows görev komut dosyası başarıyla ayrıştırılmıştır. Yerel belgeleme bağlantıları çözümlenmiştir.

27 Ekim tarihli incelemeden elde edilen yedi bulgunun tümü ele alınmıştır. GitHub iş akışı yürütme, Linux/macOS/Docker çalışma ortamı, gerçek Telegram, harici proxy/TSA birlikte çalışabilirliği ve sürekli yük testi, bu yerel çalıştırmanın kapsamı dışında kalmaktadır. Herhangi bir depo yayını, hizmet kaydı veya gerçek hesap toplama işlemi gerçekleştirilmemiştir.

### İngilizce dokümantasyon güncellemesi

README dosyası, hesap/oturum referansı, veri toplama iş akışı ve pakete dahil kılavuz artık desteklenen girdileri, çalışma alanı davranışını, olay politikalarını ve dışa aktarım formatlarını İngilizce olarak açıklamaktadır. Üç adet halka açık ekran görüntüsü, sentetik veriler kullanılarak güncellendi. Bu noktada, açık kaynak seçkisi, iki yeni kılavuz da dahil olmak üzere 88 dosya içeriyordu. 23 Markdown belgesindeki 131 yerel bağlantının tümü çalışır durumda.

Arayüz ve kılavuz düzenlemelerinin ardından, Chromium kabul testi yine tüm 45 senaryoyu başarıyla geçti; sayfalarda JavaScript hatası veya harici istek gözlemlenmedi. Bu dokümantasyon ve sunum güncellemesi için tam Python test paketi yeniden çalıştırılmadı; yukarıdaki 94 başarılı test sonucu, önceki kod düzeltme çalıştırmasına aittir.

Yeniden oluşturulan tekerlek, yeni ve izole edilmiş bir hedefe kuruldu. Panel ve kılavuz varlıkları başarıyla işlev gördü, kimliği doğrulanmamış API erişimi reddedildi ve hem doğrudan hem de akışlı dışa aktarımlar, 32 sentetik olaydan oluşan bağımsız doğrulama sürecini geçti.

### Kurulum ve devreye alma güncellemesi

Odaklanmış yükleyici, paketleme ve hazırlık kontrolleri **14 testi** geçti; kullanılamayan sembolik bağlantı oluşturma nedeniyle bir test atlandı. Yerel sarmalayıcı kontrolleri, boşluk içeren yollar, argüman iletimi, kurulum/demo modları ve sıfırdan farklı çıkış yayılımını kapsar. Git Bash kontrolleri, simüle edilmiş bir arka plan hizmeti ile Docker kabuk yardımcısını test eder; bu testler arasında eksik Docker, eksik Compose, başarısız durum kontrolü beklemesi ve başarılı alternatif bağlantı noktası başlatma yer alır. Bu simüle edilmiş kontroller, Docker çalışma zamanı uyumluluğunu doğrulamaz.

Tam bir açık kaynak kopyası, yolunda boşluklar bulunan yeni bir Windows dizinine yüklendi. `scripts\Setup.cmd` yeni bir ortam oluşturdu ve sabitlenmiş çalışma zamanını yükledi; `Start.cmd --check --json`, hedef veri dizini oluşturmadan hazır olduğunu bildirdi. `pip check` testi geçti. Yeniden derlenen tekerlek, doğrudan ve akışlı 32 olay dışa aktarımları da dahil olmak üzere yüklü paket kontrolünü de geçti.

Shell sözdizimi ve beş iş akışı/Compose YAML dosyası ayrıştırıldı. Kaynak ve resim Compose yapılandırmaları, depolama ve çalışma zamanı ayarları açısından uyumludur. Bu aşamada, 23 Markdown belgesindeki toplam 139 yerel bağlantı çözümlendi. Açık kaynak seçkisi 99 dosya içermektedir.

CI tanımları artık Windows/Linux/macOS üzerinde yeni yerel kurulum, konteyner yeniden oluşturulması sırasında Compose'un çalışırlığı/erişim kontrolü/kalıcılığı ve Caddy yapılandırmasını uyguluyor. Sürüm iş akışı, yayınlamayı bu kontrollerden geçirme şartına bağlıyor ve öykünülmüş bir ARM64 hızlı testi ekliyor. Docker bu ana bilgisayarda kullanılamıyor: gerçek Compose/Caddy çalıştırması, sertifika düzenleme, ARM64 çalıştırması ve uzaktan iş akışı/paket yayınlama yerel olarak hâlâ desteklenmiyor. Uygulama/kullanıcı arayüzü kodu bu güncellemeyle değişmedi; önceki tam Python ve tarayıcı testleri yeniden çalıştırılmadı.

## Sürüm 0.5.0

Tam sabitlenmiş çalışma zamanı paketi başarılı oldu: **81 başarılı, 1 atlandı**, 22,00 saniyede, mevcut Starlette uyarısı ile. POSIX izin kontrolü, Windows'ta atlanmaktadır. Yeni işleyici testleri, mesajları, düzenlemeleri, kapsamlı/kapsam dışı silme işlemlerini, tepkileri, katılımcı güncellemelerini ve üyelik hizmeti mesajlarını farklı politikalar aracılığıyla gönderir. Devre dışı bırakılan kategoriler, karşılık gelen canlı gözlemler üretmez; kapsam tanılama ve açık anlık görüntüler kullanılabilir durumda kalır. Testler, kalıcı ilkeyi, çalışma alanı ayrımını, denetim kayıtlarından önce/sonra imzalanmış kayıtları, değişmemiş ilke davranışını, sıkı doğrulamayı ve bir sonraki işlem makbuzuna dahil edilmeyi doğrular.

Demo giriş testleri, bu aracın yeteneklerinin yapılandırılmış panel jetonundan farklı olduğunu, canlı bir çalışma alanını yetkilendiremediğini, toplama ayarlarını değiştiremediğini ve uzaktan, yönlendirilmiş, kaynaklar arası veya geçersiz ana bilgisayar istekleri için verilmediğini veya kabul edilmediğini doğrular. Açıkça belirtilen bir demo bayrağı olmadan saklanmış bir demoyu açmak, otomatik girişi etkinleştirmez.

Chromium kabul testi, token girişi olmadan yerel demo girişi, izleme ön ayarları, kaynak seçiminden politikaya geçiş, hesap başına bağımsızlık ve masaüstü/320/390 piksel düzeni ile metin kontrastı kontrolleri dahil olmak üzere **39 senaryoyu** geçmiştir. Sayfada JavaScript hatası görülmedi. Sunucunun AdGuard tarafından eklenen istekleri kayıtlarda yer almaktadır. İndirme HTTP fikstürü, bir istemcinin bağlantısını kapatmasının ardından bir bağlantı sıfırlaması kaydetti; doğrulamalar yine de başarılı oldu. Bu, canlı hizmet sonucu değildir.

Normal başlatıcı, izole ortamı 0.5.0 sürümüne yükseltti; kaynak ve yüklü sürümler birbiriyle uyumlu ve pip kontrolü başarılı oldu. Mevcut gizli kasa şifreleme, hatalı/eksik anahtar reddi ve imza/medya tahrifat kontrolleri, tam test paketinde başarılı oldu. Mesaj içeriği veya ekler için yeni bir uygulama şifreleme özelliği iddia edilmiyor.

Güncellenen kullanıcı arayüzünün kullanılabilir hale gelmesi için yerel demo yeniden başlatılır. Mevcut sentetik kayıtlar korunur; eski arka plan demo sürecinin durdurulması, bir sonraki başlatmada çevrimdışı bir sınır oluşturur. Bu kontroller için gerçek bir Telegram oturumu kullanılmaz.

Çalışır durumdaki localhost:8787 paneli, 0.5.0 sürümünü, otomatik demo erişimini, beş izleme kontrolünü ve saklanan 33 sentetik günlük olayını gösterdi. Ayrı olarak yüklenen 0.5.0 wheel, tüm panel/kılavuz varlıklarını sundu, kimliği doğrulanmamış API erişimini reddetti ve hem doğrudan hem de akışlı indirme yardımcısı aracılığıyla doğrulanmış 32 olaylık bir ZIP dosyası oluşturdu. Çalışma zamanı paket sürümleri, 0.4 sürümünde kaydedildiği gibi sabitlenmiş durumda.

## Sürüm 0.4.0

Tam sabitlenmiş çalışma zamanı paketi başarılı oldu: **78 başarılı, 1 atlandı**, 19,77 saniyede. Atlanan kontrol POSIX izinleri gerektirir; üst akış Starlette TestClient kullanımdan kaldırılma uyarısı devam etmektedir. Yeni testler, akışlı indirme/çalışma alanı yönlendirmesini, yetkilendirme başlıklarını, üzerine yazma reddini, yönlendirmeleri, kesik yanıtları, ilan edilen/gerçek boyut sınırlarını, sınırlı okumaları, temizleme işlemlerini, sabit bağlantıları olmayan dosya sistemlerini, hazırlık hatalarını ve paket yüklememesi gereken başlatıcı modlarını kapsamaktadır. Dışa aktarma testleri, çalışma alanı yerel geçici dosyaları ve seçici yetim dosya temizliğini doğrular.

Chromium kabul testi, sayfa JavaScript hatası olmaksızın listelenen 36 senaryonun tamamını başarıyla geçti. Simüle edilmiş telefon/kod/2FA oturum açma işlemleri, dönüştürülmüş oturumlar, iki çalışma alanı ve ayrı yollar/durumlar, gözlemler, imzalar, kontrol noktaları ve zaman damgası istekleri ile aşağıdakileri de test eder:

- Masaüstü ve 320/390 piksel düzenleri, yatay taşma olmaması, görünür gezinme menüsü ve ilk 844 piksel görüntü alanında ilk oturum açma alanı.
- WCAG AA metin eşiklerine uygun, düz arka plan üzerinde metin kontrastı. Engelli kontrolleri, opasite ve resim/gradyan arka planlar hariç tutulmuştur; bu, tam bir WCAG denetimi değildir.
- Sahte bir OS dosya seçici/yazılabilir aracılığıyla yazılmış gerçek bir yerel dışa aktarma yanıtı, ardından bağımsız ZIP doğrulaması; iptal edildiğinde dışa aktarma isteği gönderilmez.
- Yazma hatası, hedefi iptal eder; 128 MiB yedekleme, eşleşen bir yük tahsis etmeden aşırı büyük ilan edilmiş yanıtı reddeder.
- Masaüstü ve her iki dar ekran genişliği için İngilizce yerel kılavuz.

İşletim sistemi kaydetme iletişim kutusu ve gerçekte birkaç gigabaytlık tarayıcı kayıtları otomatikleştirilmemiş veya doğrulanmamıştır. Python indirme testlerinde sınırlı parçalar ve döngü geri besleme düzenekleri kullanılmaktadır. Gerçek Telegram ile tam dağıtım kabulü ayrı bir konudur.

Normal yükleyici, `.venv`'yi 0.4.0 sürümüne yükseltti. Kaynak ve yüklü meta veriler birbiriyle uyumludur; `pip check` testi geçti. `python start.py --check --json`, veri dizini oluşturmadan yeni bir sentetik yolda hazır olduğunu bildirdi. Yerel anahtar depolama uyarısı doğru şekilde devam ediyor: günlükler/medya, uygulama tarafından şifrelenmiyor.

0.4.0 sürümü derlendi ve ayrı bir dizine kuruldu. 23 uygulama dosyasının tamamı kaynak dosyayla bayt bayt eşleşmektedir. Yüklenen paket, paneli ve İngilizce kılavuzu/varlıkları sunmuş, kimliği doğrulanmamış API erişimini reddetmiş ve doğrulamadan geçen sentetik 32 olaylık bir ZIP dosyası dışa aktarmıştır. Akış indirme komutu ayrıca, çalışır durumdaki yüklü uygulamadan bağımsız olarak doğrulanmış bir ZIP dosyasını da almıştır.

Genel belgeler ve yerel kılavuz İngilizce; yerel belge bağlantıları çözülür. PowerShell, Windows görev şablonunu, Python ise macOS plist dosyasını ayrıştırdı. Bunlar sözdizimi denetimleridir, hizmet yürütme değildir. Hiçbir görev/hizmet kaydedilmedi. CI yapılandırması artık hazırlık denetimlerini içeriyor ancak uzaktan CI burada çalıştırılmadı.

0.4 tarayıcı çalıştırmasında yine AdGuard enjeksiyonu ve Windows asyncio socket-cleanup OSError 10022 gözlemlendi. Tarayıcı doğrulamaları başarılı; bu ortam gözlemleri, sabit bir uygulama davranışı olarak değerlendirilmek yerine kaydedildi. İlk OpenSSL/tarayıcı/pip sanal alan denemeleri başarısız oldu; başarılı olan denemelerde sanal alan dışında onaylanmış yürütme kullanıldı.

## 0.3.1 sürümü, hazırlık aşamasındaki düzeltmelere odaklanmıştır

Etkilenen başlatıcı, kanıt/depolama ve API kontrolleri: 31'i başarılı, 1'i atlandı, bir adet Starlette uyarısı. Atlanan kontrol, POSIX dizin izinlerini doğrular ve bu Windows sunucusunda söz konusu izinleri sağlayamaz. Eski Python testi, sürüm/ithalat sınırını simüle eder; Python 3.10 yorumlayıcısı yüklenmemiş veya onaylanmamıştır. Daha önce başarılı olan 0.3 test paketi aşağıda kaydedilmiştir; bu odaklanmış değişiklikler için test paketinin tamamı ve tarayıcı senaryoları yeniden çalıştırılmamıştır.

Normal başlatıcı, yerel ortamı 0.3.1 sürümüne yükseltti; kaynak ve yüklü meta veriler birbiriyle uyumlu ve pip kontrolü başarılı oldu. Ayrı olarak yüklenen 0.3.1 wheel sürümü, panel/assets'i sundu, kimliği doğrulanmamış API erişimini reddetti ve doğrulanmış 32 olaylık sentetik bir dışa aktarım oluşturdu. İş akışı YAML dosyası ayrıştırıldı, ancak yeni konteyner çalışma zamanı kontrolü yürütülmedi: kullanılabilir yerel Docker/Podman/Linux çalışma zamanı mevcut değildi.

Kullanılabilirlik, canlı hizmet ve platform eksiklikleri konusunda [hazırlık bulgularına](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) bakınız. Bu yama, ek işletim sistemlerini desteklemez.

## Sürüm 0.3.0

Tam sabitlenmiş çalışma zamanı paketi **61 testi** geçti; bunlardan birinde, Starlette TestClient'ın kullanımdan kaldırılacağına dair bir uyarı vardı. Çalışma zamanı meta verileri, TgWitness 0.3.0 ve python-socks 2.8.2 sürümlerini bildiriyor; pip kontrolü başarılı oldu. Tarayıcı uyumluluk testi, sayfada herhangi bir JavaScript hatası olmadan başarıyla tamamlandı.

0.3.0 sürümü derlendi ve ayrı bir paket dizinine kuruldu. Bu sürüm, panele ve varlıklara hizmet verdi, kimliği doğrulanmamış bir API isteğini reddetti ve bağımsız doğrulamadan geçen 32 olaylık sentetik bir günlüğü dışa aktardı. Yerel belgelerdeki bağlantılar çalışır durumda. MTProxy çıplak anahtar normalleştirme düzeltmesinden sonra, dokuz bağlantı/güvenlik testinin tamamı başarıyla yeniden çalıştırıldı.

Yeni kapsama dahil olanlar:

- Gerçek loopback test sunucuları üzerinden SOCKS5 kullanıcı adı/şifre ve HTTP CONNECT; yapılandırılmış bir proxy çalışmazsa, hedef sunucuya yönlendirilmek yerine hata verir.
- Proxy doğrulama, MTProxy aktarım seçimi, sahte TLS şifrelerinin reddedilmesi, kalıcılık, çalışma alanı yalıtımı, gözlem sırasında yapılan değişikliklerin reddedilmesi ve API durumu ile imzalı olaylardan gizli bilgilerin hariç tutulması.
- Sentetik Telethon SQLite şemaları 7 ve 8'in salt okunur dönüştürülmesi; değişmemiş kaynak hash değeri; diğer biçimlerin, SQL görünümlerinin ve bekleyen bir WAL dosyasının reddedilmesi.
- Harici kasa ana anahtarı: farklı türetilmiş çalışma alanı anahtarları, başarılı yeniden açma, yanlış/eksik anahtar reddi ve mevcut yerel kasaların örtük olarak taşınmaması.
- Tarayıcı proxy ayarları, kimlik bilgilerinin silinmesi, depolama koruması açıklaması, mobil bağlantı sayfası, dönüştürülmüş oturum dosyası yetkilendirme, ayrı rotalar ve sahte bir Telegram istemcisi kullanılarak daha önce ele alınan tüm toplama/dışa aktarma senaryoları.

Geliştirme aşamasında, bir loopback testi eşin kapanmasını süresiz olarak bekledi; başka bir çalışmada ise el sıkışma işleminden sonra Windows bağlantısının sıfırlandığı gözlemlendi. Artık test düzeneği tüm veri alışverişini sınırlandırıyor ve tamamlanmış bir el sıkışma işleminden sonraki EOF/sıfırlamayı bağlantı kapanışı olarak değerlendiriyor. El sıkışma/kimlik doğrulama onayları hâlâ zorunludur. Bu durum, gerçek proxy sağlayıcılarını kapsamaz veya Telegram aktarımında sabit bir kusur olduğu anlamına gelmez.

Aşağıda açıklanan AdGuard istek gözlemi hâlâ geçerlidir. Gerçek bir Telegram hesabı, SOCKS/HTTP proxy dışında veya canlı bir MTProxy sunucusu kullanılmamıştır. MTProxy deneysel bir araçtır ve seçilen seçenekleri/gizli anahtar doğrulaması kontrol edilmiştir, ancak canlı ortamda çalışabilirliği test edilmemiştir. Yeni harici anahtar ve oturum dönüştürme komutları yalnızca sentetik gizli anahtarlarla test edilmiştir. Linux/macOS/Docker platformları bu konuda henüz test edilmemiştir.

Aşağıdaki 0.2 sürümüne ait verim ölçümü tekrarlanmamıştır ve 0.3 sürümü için yeni bir çoklu hesap/proxy karşılaştırma ölçütü olarak sunulmamalıdır.

## 0.2.0 sürümü temel versiyonu

Windows üzerinde Python 3.12.10 ile test edilmiştir. Gerçek bir Telegram hesabı bağlanmamıştır.

| Kontrol et | Sonuç |
| --- | --- |
| Python paketi | Geliştirme ortamında 52 test başarılı, sabitlenmiş çalışma zamanında 52 test başarılı; her çalıştırmada bir adet Starlette TestClient'ın kullanımdan kaldırılacağına dair uyarı |
| JavaScript sözdizimi | Node.js ile geliştirilmiştir |
| Chromium uyumluluğu | Onaylandı; sayfada JavaScript hatası yok |
| Masaüstü/mobil düzeni | 1440 × 1060 ve 390 × 844 çözünürlüklerde kontrol edilmiştir; yatay yönde belge taşması yoktur |
| HTML biçiminde mesaj içeriği | Metin olarak görüntülenmiştir; eklenen komut dosyası çalıştırılmamıştır |
| Örnek hesap akışı | API kimlik bilgileri → telefon → kod → 2FA → grup seç → başlat → anlık görüntü → duraklat → yeniden yükle |
| Tarayıcıda kanıt | Düzenleme karşılaştırması, silme işleminden önceki içerik, filtreler, ZIP indirme, kontrol noktası, imzalı işlem makbuzu, RFC 3161 isteği indirme ve kontrol noktası bağlama |
| Çoklu hesap | Ayrı günlükler, anahtarlar, kaynaklar ve canlı durumlar; tarayıcı değiştirildiğinde diğer toplayıcı çalışmaya devam eder; yeniden başlatma sonrasında çalışma alanları yeniden açılır; yinelenen hesaplar ve hesap yeniden atamaları reddedilir |
| Kriptografik hatalar | İmzalı alanlar değiştirildi, imzalanmamış alanlar eklendi, yanlış anahtar, bozuk arşiv öğesi, değiştirilmiş/eksik medya, kontrol noktasında tespit edilen kesinti reddedildi |
| Depolama | Eşzamanlı eklemeler doğrulanır; güncelleme/silme işlemleri reddedilir; başlangıç aşamasında, ekleme yapılmadan değiştirilmiş bir günlük reddedilir ve kilidi serbest bırakılır |
| Medya dayanıklılığı | Atomik mesaj/iş yazma işlemleri; yeniden başlatma kurtarma; orijinal sürüm tanımlayıcıları korunur; kuyruk değiştirme ve mevcut dosya bozulması reddedilir; FloodWait kalıcı hale getirildi; kaynak hataları izole edildi |
| Canlı yayın | Yeni kayıtlar eklendikçe sabit bir önek dışa aktarılır; saklanan kontrol noktası, kesik günlüğü algılar; dışa aktarım, olay akışının tamamını yansıtmaz |
| RFC 3161 | OpenSSL 3.5.9, oluşturulan istekleri okur; yerel olarak oluşturulan sentetik CA/TSA yanıtları kabul edilir; değiştirilmiş veriler, nonce ve hatalı CA reddedilir; ortamdaki CA ortamı, açıkça belirtilmiş güveni geçersiz kılmaz |
| Yerel kurulum | start.py --setup-only komutu, izole edilmiş .venv ortamını 0.2.0 sürümüne yükseltti; kaynak ve yüklü meta veriler birbiriyle uyumlu; pip kontrolü başarılı |
| Wheel | 0.2.0 sürümü derlendi ve test-results dizinine ayrı olarak kuruldu; panel/assets dosyaları sunuldu, kimlik doğrulaması yapılmamış API çağrıları reddedildi, 32 olaydan oluşan sentetik bir arşiv dışa aktarıldı ve doğrulandı |

Kaynak testlerinde FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 ve Playwright 1.62.0 kullanılmıştır. Sabitlenmiş çalışma zamanı, FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 ve cryptography 50.0.2 kullanır. deploy/constraints.txt dosyası çalışma zamanı sürüm sabitlemelerini kaydeder; deploy/requirements.lock ve deploy/build.lock dosyaları her paket dosyasının SHA-256 değerini ekler ve Docker ile yüksek güvenlikli sunucular yalnızca bu dosyalardan yükleme yapar (pip --require-hashes). Bunların hiçbiri, yapılandırılmış her CI platformunda uyumluluk kanıtı değildir. Uzak CI çalıştırılmamıştır.

## Sentetik yerel kapasite ölçümü

Komut: `python tools/check_capacity.py --events 10000 --chats 100`

| Metrik | Gözlemlenen |
| --- | --- |
| Giriş | Seçilen 100 sentetik kaynaktan elde edilen 10.000 sentetik mesaj olayı |
| Mesaj metni | 400 karakter; medya veya ağ içermez |
| Verilerin Alınması | 53,273 saniye; saniyede 187,7 olay |
| İşleyici gecikmesi | p50 4,162 ms; p95 7,784 ms; maksimum 129,118 ms |
| ZIP olarak dışa aktarma | tracemalloc etkinleştirildiğinde 19,868 saniye |
| Python export tahsisatlarının en yüksek değerleri | 0,51 MiB; RSS işlenmiyor |
| ZIP boyutu | 4.610.962 bayt |
| Bağımsız doğrulama | 10.000 olayın tamamı doğrulanmıştır |

Bu ölçüm, bu Windows sunucusundaki yerel seri kayıt/dışa aktarma yolunu ölçer. MTProto teslimatı, eşzamanlı hesaplar, Telegram hız sınırlaması, medya, uzun süreli iş yükü veya garantili gerçek sohbet sayısını ölçmez. Bu ölçüm, ölçülen mesaj yolunu değiştirmeyen nihai çevrimdışı zaman damgası araçlarından önce gerçekleştirilmiştir.

## Çevresel gözlemler

Windows sanal ortam kısıtlamaları, varsayılan pytest/pip geçici dizinlerini ve Playwright alt sürecini engelledi. Pytest, proje içindeki yeni bir geçici dizin kullandı; kurulum ve tarayıcı işlemleri, sanal ortam dışında onaylanmış olarak çalıştırılmasını gerektirdi.

Cihazdaki AdGuard, local.adguard.org adresine yönelik istekleri tarayıcıya enjekte etti. Tarayıcı kayıtlarında bu istekler saklanmaktadır. Bu çalışma, değiştirilmemiş bir tarayıcı ortamında dışa giden isteklerin sıfır olduğu anlamına gelmez; uygulamanın kaynak kodu harici varlık/CDN/analitik istekleri içermez. AdGuard ayarlarında herhangi bir değişiklik yapılmamıştır.

Son tarayıcı çalıştırmasında ayrıca bir Windows asyncio soket temizleme OSError 10022 hatası kaydedildi. Tüm tarayıcı doğrulamaları başarılı oldu ve hiçbir sayfada JavaScript hatası meydana gelmedi. Nedeni tespit edilemedi ve bu çalıştırma, ana bilgisayar aktarım sorunlarının bulunmadığını göstermez.

urllib'in connection-close isteklerini kullanan ilk kurulu paket HTTP testi, hem sanal ortam içinde hem de dışında ve her iki bağımlılık kümesinde bağlantı sıfırlamalarıyla karşılaştı. Son test, http.client aracılığıyla standart HTTP/1.1 kalıcı bağlantıları kullandı ve testi geçti. Tarayıcı istekleri de başarılı oldu. Sıfırlamaların kesin kaynağı tespit edilemedi; bunlar, düzeltilmiş bir uygulama hatası olarak nitelendirilmedi.

## Kalan nitelikler

Saklanan canlı günlük, gerçek toplama işlemlerini, düzenlemeleri, silme bildirimlerini, ekleri, yeniden kontrolleri ve hız sınırlaması yönetimini kaydeder. Bu günlük, kapsamlı teslimat bilgilerini veya rol görünürlüğü, tepki veren aktörler, uzatılmış FloodWait, hesap yasaklamaları ve ağ/işlem kesintisi kurtarma işlemlerini içeren kontrollü bir matris kaydetmez. QR jetonu düzenleme işlemi, tamamlanmış mobil QR onayı işleminden ayrıdır.

Docker derleme/çalıştırma, Linux/macOS kurulumu, sürekli yüksek yük, bağımsız güvenlik incelemesi, gerçek bir bağımsız TSA yanıtı, sertifika iptal/arşivleme doğrulaması ve adli sertifikasyon, kaydedilen yeterlilik kapsamı dışında kalmaktadır. Kaydedilmiş MTProto durumu ve yakalama işlevleri uygulanmaktadır; atomik kalıcı tekrar oynatma ise henüz kurulmamıştır. Yönetici günlüğü toplama, ek reaktör listeleri ve öncelikli kısa sorgulama ayrı özellikler olarak kalmaktadır. Kontrollü yeterlilik matrisi için [canlı kabul](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) bölümüne bakınız.

Yerel ayrıntılı makbuzlar ve ekran görüntüleri test-results/ dizininde bulunur (Git tarafından göz ardı edilir). docs/assets/ dizinindeki herkese açık ekran görüntüsü yalnızca kurgusal örnek veriler içerir.

## Halka açık web sitesi ve yayın hazırlığı · 27 Ekim 2026

`website/` sunumu ve Pages yapısı, yukarıdaki panel kontrollerinden sonra eklenmiştir. Canlı hesap yapılandırması veya veri toplama mantığında herhangi bir değişiklik yapılmamıştır.

- Mevcut uygulama paketi testleri başarıyla geçti: 138'i geçti, 1'i POSIX'e özgü olduğu için atlandı ve bir Starlette/httpx'in kullanımdan kaldırılacağına dair uyarı çıktı. Eklenen 11 site derleme testi, beklenmeyen çıktı reddi ve bağlantılı girdi reddi dahil olmak üzere bağımsız olarak başarıyla geçti.
- Her iki uygulama tarayıcı komut dosyası da project-venv Playwright ve Chromium headless shell 156 kullanılarak başarıyla çalıştırıldı. Sayfada herhangi bir JavaScript hatası veya harici istek kaydedilmedi. Tüm hesap senaryolarında sahte aktarım ve kurgusal veriler kullanıldı.
- `tools/check_site.py`, 320, 390, 768, 1024 ve 1440 genişliklerinde, proje URL alt yolu, klavye sekmeleri, panoya erişim (başarılı/reddedildi), hareket azaltma ve devre dışı bırakılmış JavaScript ile test edildi. Başarısız varlık istekleri veya harici istekler meydana gelmedi.
- `tools/build_site.py`, toplamda yaklaşık 460 KB büyüklüğünde 10 adet izin listesine alınmış genel erişimli dosya oluşturdu. Tarayıcı ekran görüntüleri ve bir makbuz, göz ardı edilen `test-results/site/` dosyasında bulunmaktadır.
- Proje ortamına yalnızca derleme amaçlı setuptools/wheel araçları yüklendikten sonra wheel başarıyla oluşturuldu. Yalıtılmış bir hedefe kurulduktan ve `tools/check_install.py` komutu çalıştırıldıktan sonra testler başarılı oldu: statik varlıklar, erişim kontrolü, imzalı 32 olaylık sentetik dışa aktarım ve bağımsız olarak doğrulanmış akış indirme.
- `pip check`'den geçti. Git'te seçilen halka açık adayların desen taramasında, tanınabilir özel anahtar blokları, GitHub/bot/AWS belirteçleri, uzun sabit gizli atamalar veya birleştirme çakışması işaretçileri bulunamadı. Bu, olası her türlü gizli biçimin bulunmadığının kanıtı değildir. Çalışma zamanı verileri/oturum/anahtar sondaları Git tarafından göz ardı edildi.
- GitHub CLI kimlik doğrulaması geçersizdi; herhangi bir uzak sunucu yapılandırılmamıştı ve ilk commit mevcut değildi. Push, barındırılan iş akışı, Pages dağıtımı veya sürüm yayını gerçekleştirilmedi. Docker ve canlı Telegram/platform yeterlilik kontrolleri bu kontrolün kapsamı dışındadır.

Bu sunucuda, E: çalışma alanı dosya sisteminde Playwright indirme kilidi başarısız oldu. `%LOCALAPPDATA%/tgwitness-playwright` altında Chromium'u yüklemek ve aynı `PLAYWRIGHT_BROWSERS_PATH`'yi kontroller için kullanmak başarılı oldu. Bu, bir ortam geçici çözümü olup, uygulamanın çalışma zamanı bağımlılıklarında bir değişiklik değildir.

## Etkileşimli dokümantasyon ve web sitesi meta verileri · 29 Ekim 2026

Halka açık site, 12 İngilizce HTML sayfadan oluşur: bir ana sayfa, bir kılavuz dizini ve on kılavuz. Bu çalışma, açıkça listelenmiş 28 sunum dosyası içerir; boyutu yaklaşık 1,85 MB'dir ve hiçbir veri toplama bilgisi içermez. Halka açık web sitesi İngilizcedir; uygulama çevirileri ve çevrilmiş depo kılavuzları ayrıdır.

- Site, kaynak yayın ve sürüm sınırı testleri: **18'i geçti, 2'si atlandı**. Atlanan testler, bu Windows dosya sisteminde sembolik bağlantı oluşturulmasıyla ilgilidir. Testler şunları kontrol eder: benzersiz sayfa meta verileri, yalnızca İngilizce olan genel sayfalar, kanonik URL'ler, tüm site haritası girdileri, yerel varlıklar/bağlantılar, yapılandırılmış gezinme ve özel dosyaların hariç tutulması.
- Hem `tools/check_site.py` hem de `tools/check_docs_site.py`, Chromium'da 320, 390, 768, 1024 ve 1440 piksel çözünürlüklerde proje URL'sinin alt yolu altında testleri geçti. Kontrol edilen kılavuz, 11 belgelerin tamamını, arama ve klavyeyle gezinmeyi, panoya kopyalama/yapıştırma işlemlerinin başarılı/başarısız olmasını ve JavaScript olmadan okunabilir içeriği kapsamaktadır.
- Beş etkileşimli örnek başarıyla geçildi: hareketin azaltılması ve ekran dışı askıya alma ile mesaj oynatma/adımlama/duraklatma/sıfırlama; orijinal/değiştirilmiş/yeniden oluşturulmuş/kesilmiş hash zincirleri; tanık kabulü/geri alma/çatallanma/yanıt yok kararları; ve tam/gecikmeli/eksik teslimat senaryoları; ve gönderen kimliği, hedef ve ek hash'ine göre kurgusal çapraz sohbet gözlemlerini birbirine bağlayan bir soruşturma haritası. Soruşturma kontrolleri, klavye gezinme ve JavaScript'siz yedekleme kontrollerinden geçti. Tarayıcının SHA-256 sonuçları, Python'un `hashlib`'si ve kanonik JSON ile bağımsız olarak karşılaştırıldı. Hash örneği, Web Crypto kullanılamadığında da okunabilir yedek halini korudu.
- Teslim oranları ve grafik işaretçileri, erişilebilir tabloyla eşleştirildi. Mobil eksen etiketleri, görsel incelemenin ardından büyütüldü. Her örnek, açıklayıcı veya sentetik olarak etiketlenmiştir ve hiçbir tarayıcı örneği Telegram ile bağlantı kurmamaktadır.
- Herhangi bir harici istek, başarısız HTTP isteği veya JavaScript hatası kaydedilmedi. Masaüstü/mobil ekran görüntüleri ve makbuzlar, `test-results/site/` ve `test-results/docs-site/` altında göz ardı edilmiştir. Dokümantasyon dizini, mesaj/hash örnekleri, witness düzeni, teslimat grafiği ve soruşturma haritası, masaüstü/mobil boyutlarında incelenmiştir.
- Yayın taraması, 282 açık kaynak dosyası ve 1.426 yerel belgeleme bağlantısı için başarılı sonuç verdi. Ruff, değiştirilmiş Python site araçları ve testleri için başarılı sonuç verdi.
- `docs/HOW-IT-WORKS.md`, Mermaid diyagramları ve formülleri içeren bir GitHub Markdown eklentisi sunar. `docs/INVESTIGATION.md`, hesap genelini, sohbet bazında geçmiş verilerinin toplanmasını, kişi profillerini, sohbetler arası referansları, zaman çizelgelerini ve doğrulanmış vaka devrini kapsar. Adımları ve sınırları, mevcut kapsam, toplama, dosya, dışa aktarma, doğrulayıcı ve panel koduyla karşılaştırılarak kontrol edildi. Barındırılan GitHub görüntüleme işlevi kontrol edilmedi.

Bu, yerel bir web sitesi/belgeleme kontrolüdür. Canlı Telegram doğrulaması eklemez veya barındırılan Pages dağıtımını, uzaktan CI başarısını ya da arama motoru indekslemesini sağlamaz. [Yayınlama prosedürüne](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) ve [web sitesi meta veri notlarına](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md) bakınız.
