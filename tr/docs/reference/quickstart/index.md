# Hızlı başlangıç

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/

TgWitness'i kurmanın ve çalıştırmanın tüm yolları: Windows paketi, Python, Docker ve ilk kontrolleri içeren sentetik demo.

**İngilizce** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ukraynaca](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Portugizce (Brezilya)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urduca](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [Hintçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Endonezyaca](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Basitleştirilmiş Çince](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness, hesaplarınızın erişebildiği Telegram gruplarını ve kanallarını izlemek için kullanılan bağımsız bir uygulamadır. Kendi veri diziniyle yerel olarak çalışır.

**İlk kez mi ziyaret ediyorsunuz?** Hesabınızı bağlamadan önce [demoyu inceleyin](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/#explore-the-interface). Proxy'ler, tanıklar, veri aktarımları veya sunucu kurulumu için [bir kılavuz seçin](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md).

## Yükleyin ve başlatın

[GitHub Actions ile kayıt (önizleme)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Bir yöntem seçin. Sürüm derlemesi yayınlandıktan sonra taşınabilir indirme dosyaları kullanıma sunulur:

| Barındırma | Yükleme gerektirmez | Kaynak: Python 3.11+ | Docker: Engine/Desktop ile Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | GitHub Sürümleri'nden `TgWitness-<version>-windows-amd64-portable.zip` dosyasını çıkarın, `TgWitness.cmd` dosyasına çift tıklayın | `Start.cmd`'ye çift tıklayın | `scripts\Docker.cmd`'ye çift tıklayın |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Kaynak kodu yöntemleri için [güncel `main` dalını indirip çıkarın](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) veya depoyu klonlayın:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Güncel kaynak kodu; toplu hesap içe aktarma, MTProxy kontrol paneli ve kaldığı yerden devam edebilen geçmiş yükleme özelliklerini içerir. 0.7.0 taşınabilir önizleme sürümü ve sürüm kaynak arşivi bu eklemelerden önceye aittir. Sürüm sınırları için [değişiklik günlüğüne](https://phishdestroy.github.io/TgWitness/tr/docs/reference/changelog/) bakın.

`Start.cmd`, uygun bir Python bulunamazsa Windows kullanıcınız için Python 3.12 kurmayı önerir (winget veya imzalı python.org yükleyicisi ile). `start.sh`, Python eksikse Linux dağıtımınız veya macOS için tam kurulum komutunu yazdırır. Kaynak koddan ilk başlatma, `.venv` ortamını oluşturur ve bağımlılıkları otomatik olarak yükler.

Docker, uygulamayı derler ve arka planda çalıştırır; Python ana bilgisayarı gerekmez. `scripts\Docker.cmd` ve `scripts/docker-start.sh`, konteyner çalışır durumdayken panel adresini ve jetonu yazdırır. Desteklenen her ana bilgisayarda kullanılabilecek eşdeğer Docker komutları şunlardır:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

**http://127.0.0.1:8787** dosyasını açın. Docker yardımcı programı veya ikinci Docker komutu tarafından yazdırılan jetonu kullanın ya da taşınabilir veya kaynak kurulum için **data/live/panel-token.txt dosyasını** okuyun. Aşağıdaki "**Telegram'ı Bağla"** bölümünden devam edin. Yerel ve Docker kurulumları ayrı depolama alanları kullanır; Docker'ı başlatmak, mevcut bir yerel günlüğü içe aktarmaz.

Sunucu için [dağıtım](https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/), otomatik HTTPS, yeniden başlatma, yayınlanan görseller, güncellemeler ve yedeklemeleri kapsar.

## Arayüzü keşfedin

1. Taşınabilir paketteki **TgWitness-Demo.cmd dosyasını** , Windows kaynak klasöründeki **scripts\Demo.cmd** dosyasını veya Linux/macOS'ta `sh start.sh --demo` komutunu çalıştırın. Kaynak klasörden başlatıldığında önce `.venv` dosyası oluşturulur ve bağımlılıklar yüklenir.
2. **http://127.0.0.1:8787 adresini** açın.
3. Yerel demo, örnek günlüğü otomatik olarak açar. Doğrudan yerel erişim için herhangi bir erişim kodu kopyalanmasına gerek yoktur.

Demo mesajları kurgusaldır. Demo modunda gerçek bir Telegram hesabına bağlanılamaz.

## Telegram'a bağlan

> [!UYARI] **Kaybetmeyi göze alamayacağınız hiçbir şeyi kullanmayın.** Kişisel veya değerli hesaplarınızı bağlamamanızı ve değer verdiğiniz bir hesap üzerinde API kimliği / hash oluşturmamanızı şiddetle tavsiye ederiz. Telegram, kullanılan istemciden bağımsız olarak hesapları öngörülemez bir şekilde ve genellikle kalıcı olarak engeller. Sorunsuz bir test çalışması TgWitness’e değil, Telegram’a bağlıdır ve ileride herhangi bir garanti vermez.

1. Yerel demo çalışıyorsa, onu durdurun ve **Start.cmd** veya `sh start.sh` dosyasını çalıştırın. Aksi takdirde, yukarıda başlatılan canlı kurulumu çalışır durumda bırakın.
2. Paneli açmak için kurulum yönteminize uygun panel jetonunu kullanın.
3. Proxy'ye ihtiyacınız varsa, bunu **Hesap → Ayarlar → Bağlantı ayarları → Bağlantı yolunu değiştir** seçeneği altında kaydedin.
4. **Hesap** bölümüne telefon numaranızı girin ve **Devam'a** basın, **QR kodu → QR kodunu göster'i** seçin veya dosyaları seçip **Hesabı bağla**'ya basın. **API Kimliği + Hash** isteğe bağlıdır: çalışma alanı, kaydedilmiş veya içe aktarılmış çifti ya da yerleşik havuzdan çalışan bir çifti kullanır. Kendi uygulamanızı kullanmak için, bir `API ID:API Hash` çiftini API Kimliği alanına yapıştırın. Tam bir yetkilendirme anahtarı için "**Yetkilendirme anahtarı**"**nı** seçin, 512 onaltılık karakterin tamamını yapıştırın ve sağlanan DC Kimliğini seçin. Kullanıcı Kimliği isteğe bağlıdır ve girildiğinde işaretlenir.
5. Seçtiğiniz oturum açma yöntemini tamamlayın: telefon/kod/2FA, QR kodu için oturum açılmış bir Telegram uygulamasından onay veya desteklenen bir yetkili oturum içe aktarımı.
6. Görüntülenen hesap kimliğini kontrol edin. Açık **Kaynaklar**: sohbetleriniz otomatik olarak yüklenir; gruplarınızı ekleyin.
7. "**Hangi değişikliklerin saklanacağını seçin**" bölümünde, olay kategorilerini veya " **Mesajlar, düzenlemeler ve silme işlemleri**" ön ayarını seçin, ardından izleme ayarlarını kaydedin.
8. Ek ayarlarını ayrı ayrı seçin, ardından "**Gözlemi başlat" düğmesine** basın.

API kimlik bilgileri uygulamanızı tanımlar; tek başlarına bir hesaba yetki vermezler. Özel gruplar için herkese açık kullanıcı adı gerekmez, ancak hesabınızın erişim izni olmalıdır.

Mevcut hesaplar için [hesaplar ve oturum biçimleri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/) sayfasına bakın: panel; Telethon StringSession, Telethon/Pyrogram SQLite, tek hesaplı TData ZIP ve desteklenen hesap JSON biçimlerini kabul eder. Bir oturumu ve eşlik eden JSON dosyasını birlikte seçip **Hesap bağla** düğmesine basın. QR ile giriş de aynı isteğe bağlı API ayarlarıyla kullanılabilir. TDLib, bot oturumları ve CSV/JSON hesap envanterleri desteklenmez.

Birden fazla hesap için **Hesaplar → Hesapları içe aktar** yolunu kullanın ve desteklenen oturum dosyalarını seçin. Eşlik eden JSON dosyaları temel dosya adına göre eşleştirilir; içe aktarılan her hesap kendi çalışma alanını alır. [Toplu içe aktarma ve hesap grupları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/#bulk-import-and-account-groups) bölümüne bakın.

Başka bir hesap eklemek için, hesap seçicinin yanındaki **+** tuşuna basın veya **Hesap → Ayarlar → Bağlantı ayarları → Çalışma alanları seçeneğini** açın ya da **Hesaplar bölümünü** kullanın. Çalışma alanlarının ayrı oturumları, günlükleri, anahtarları, kaynakları ve kuyrukları vardır. Görünümler arasında geçiş yapıldığında diğer toplayıcılar çalışmaya devam eder. Bu kurulumda aynı Telegram hesabı iki çalışma alanına atanamaz. Çalışma alanlarının sabit bir sayısı yoktur; hepsi tek bir işlemi paylaşır, bu nedenle kapasite makineye bağlıdır.

Canlı panel jetonu, Telegram yetkilendirmelerinize ve kaydedilmiş materyallerinize erişimi korur; bu, Telegram API kimlik bilgilerinden ayrıdır. Yalnızca açıkça başlatılmış, doğrudan erişilen yerel bir demo otomatik olarak giriş yapabilir. Uzak/proxy üzerinden erişilen bir demo ise yine de `data/demo/panel-token.txt`'yi kullanır.

## İnceleme ve dışa aktarma

- **Günlüğü:** Gözlemleri kaynağa ve olay türüne göre arayın ve filtreleyin.
- Bir olayı seçerek orijinal kaydını, kaynağını ve kaydedilmiş sürümlerini inceleyin.
- Düzenleme ayrıntıları, mevcut "öncesi/sonrası" içeriğini gösterir. Silme ayrıntıları ise varsa en son yakalanan içeriği gösterir; kimliği bilinmeyen bir aktör ise bilinmez olarak kalır.
- **Dışa aktarma formatları:** imzalı ZIP, JSONL, CSV ve çevrimdışı HTML.
- **Sohbetin tamamını dışa aktarma** (Kaynaklar → Sohbetin tamamını dışa aktarma): Bir sohbetin görünür tüm geçmişini, `chat.json` (Telegram dışa aktarma stili) ile imzalanmış bir paket ve okunabilir bir `chat.html` dosyası olarak indirin. Özel sohbetler, hesap üye olduğunda çalışır. Bu, silinmiş veya daha önce düzenlenmiş mesajların yeniden oluşturulması değil, güncel bir anlık görüntüdür. Bir kopyayı `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256` ile doğrulayın.
- **Kontrol noktası:** İmzalı günlüğün sınırını toplayıcının dışında tutun.
- **İmzalı çalıştırma makbuzunu indirin:** toplayıcının program/sürüm kaydını saklayın.
- **Zaman damgası isteği hazırlayın:** bir zaman damgası yetkilisine yönelik çevrimdışı bir istek hazırlayın; yanıtı almak ve doğrulamak için [TIMESTAMP.md dosyasını](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/) izleyin.
- **Günlüğü doğrulayın:** olay imzalarını ve zincir bağlantılarını kontrol edin. ZIP olarak dışa aktarma işlemi sırasında medya dosyaları da kontrol edilir.

Desteklenen tarayıcılar, büyük boyutlu dışa aktarımları doğrudan seçilen bir dosyaya kaydeder. Diğer tarayıcılar en fazla 128 MiB'lik bir önbellek kullanır. Sunucu çalışırken, akış CLI'si tüm yanıtı önbelleğe almadan daha büyük boyutlu indirmeleri destekler:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Başka bir çalışma alanı için, **Dışa Aktar → Çalışma Alanı Kimliği seçeneğini** kullanarak `--profile ID`'yi ekleyin. Uzak bir sunucu için `--url https://your-server`'yi ekleyin. Varsayılan aktarım sınırı 5 GiB'dir; `--max-mib` ile bu sınır değiştirilebilir. İmzalı ZIP içeriği, varsayılan olarak ayrı bir 4 GiB'lik sıkıştırılmamış doğrulama sınırına sahiptir (**Parameters ile** bu sınır artırılabilir; bu tür arşivleri `verify.py --max-gib N` ile doğrulayın). Arşivi, doğrulayıcının güvenilir bir kopyası ve bağımsız olarak saklanan bir anahtar parmak izi/kontrol noktası kullanarak doğrulayın.

## Kurulumu kontrol edin

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check`, yerel bağımlılıkları, imza desteğini, depolama alanını, anahtar yapılandırmasını ve dinleme adresini kontrol eder. Herhangi bir şey yüklemez veya Telegram'a bağlanmaz. Meşgul bir bağlantı noktası, başka bir örneğin çalışıyor olabileceği anlamına gelebilir. Farklı bir `--port` kullanın veya önce bunu durdurun.

Başlatıcı, `.venv`'ye yüklenir. Yardımcı `python -m tgwitness...` komutları, söz konusu ortam zaten etkinleştirilmemişse, Windows'ta `.venv\Scripts\python.exe`'yi veya Linux/macOS'ta `.venv/bin/python`'yi kullanmalıdır.

## Oturumlar, koruma ve çalışma

Kapalı, tutarlı bir Telethon SQLite `.session` dosyası, yerel olarak `python -m tgwitness.sessions account.session --out account.tgwitness-session` ile dönüştürülebilir, ardından Account'a yüklenebilir. Doğrudan dosya içe aktarma ve QR koduyla giriş seçenekleri de mevcuttur. Giriş formatları, SOCKS5, HTTP CONNECT, MTProxy ve harici anahtarlar için [CONNECTION-SECURITY.md dosyasına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/) bakınız.

**Gözlemi duraklatmak,** toplama işlemini durdurur. **Kilitleme** yalnızca tarayıcı erişimini kapatır. Sekmeyi kapatmak, toplayıcı sürecinin çalışmaya devam etmesine neden olur. Süreci durdurmak, toplama işlemini kesintiye uğratır; geçmiş anlık görüntüsü, kaçırılan tüm düzenlemeleri veya silme işlemlerini yeniden oluşturamaz. Olay ilkeleri, ek kuyrukları, hesap izolasyonu ve yeniden başlatma davranışı için [toplama işleminin nasıl çalıştığını](https://phishdestroy.github.io/TgWitness/tr/docs/reference/collection/) inceleyin.

Oturumlar ve gizli bilgiler şifrelenmiştir. Mesaj içeriği, medya dosyaları ve dışa aktarımlar için şifrelenmiş bir disk veya birim gereklidir. İmzalar, güvenilir bir anahtara göre bütünlüğü sağlar; Telegram kaynağını doğrulamaz veya toplayıcıyı ve anahtarını kontrol eden bir operatörün uydurma yapmasını engellemez.

Yedekleme/geri yükleme için [OPERATIONS.md dosyasını](https://phishdestroy.github.io/TgWitness/tr/docs/reference/operations/), barındırma için [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/) dosyasını ve hizmet örnekleri için [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) dosyasını okuyun. Yüklenen panel ayrıca `/guide.html` adresinde bir çevrimdışı kurulum kılavuzu içerir.

Gerçek doğrulama ve mevcut sınırlamalar [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) ve [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) dosyalarında kaydedilmiştir.
