# Uygulama

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/

TgWitness'i Windows, Linux, macOS veya Docker üzerinde, HTTPS üzerinden, yedeklemeler ve güncellemelerle birlikte bir hizmet olarak çalıştırın.

**İngilizce** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Ukraynaca](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Portugizce (Brezilya)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Urduca](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [Hintçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Endonezyaca](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Basitleştirilmiş Çince](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Bir kurulum seçeneği belirleyin

Taşınabilir paket için, GitHub Releases'tan `TgWitness-<version>-windows-amd64-portable.zip` dosyasını çıkarın. Diğer yöntemler için, kaynak ZIP dosyasını indirip açın veya deposunu klonlayın, ardından proje dizininden aşağıdakileri çalıştırın:

| Kurulum | Başlangıç | Arka planda çalışır mı? |
| --- | --- | --- |
| Windows taşınabilir paketi | `TgWitness.cmd` | Hayır; pencereyi açık tutun. |
| Windows için yerel sürüm | `Start.cmd` | Hayır; arka planda çalıştırmak için isteğe bağlı oturum açma görevini kullanın. |
| Linux/macOS için yerel sürüm | `sh start.sh` | Hayır; arka planda çalıştırmak için systemd/launchd kullanın. |
| Desteklenen herhangi bir ana bilgisayarda Docker | `docker compose up -d --build --wait` | Evet, Docker arka plan programı çalışırken. |
| Windows'ta Docker yardımcısı | `scripts\Docker.cmd` | Evet; yardımcı program, web sunucusunun durumunu bekler. |
| Linux/macOS üzerinde Docker yardımcısı | `sh scripts/docker-start.sh` | Evet; yardımcı program, web sunucusunun durumunu bekler. |

Üçüncü tarafların kontrol edebilmesi gereken bir bulut sunucusu için — sağlayıcının API'si aracılığıyla, SSH olmadan oluşturulmuş, yalnızca Cloudflare Tüneli üzerinden erişilebilen — [yüksek güvenilirlikli dağıtım bölümüne](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md) bakınız.

Yerel başlatma işlemi, özel bir `.venv` oluşturur ve sabitlenmiş bağımlılıkları yükler. Docker, ana bilgisayar Python'una ihtiyaç duymadan bunları görüntü içinde derler. İlk kez kurulum için İnternet erişimi gerekir. Python 3.11+ bulunmadığında, `Start.cmd`, mevcut Windows kullanıcısı için Python 3.12'yi yüklemeden önce izin ister (winget; aksi takdirde, Python Software Foundation imzasını kontrol ettikten sonra python.org yükleyicisi kullanılır); hiçbir zaman yönetici ayrıcalıkları talep etmez. Docker ve işletim sistemi hizmetleri ön koşul olarak kalır.

Yerel ve taşınabilir kurulumlar, kendi klasörleri içinde `data/live` adını kullanır. Docker ise `/data` konumunda `tgwitness-data` adlı birim adını kullanır. Tüm veri dizinini kasıtlı olarak taşıyana kadar bunlar ayrı kurulumlardır. Yeni bir Docker konteynerinin yerel hesapları otomatik olarak algılamasını beklemeyin.

## Kurulum gereksinimleri

Yerel kurulum için Python 3.11 veya üstü sürümü (`venv` ve `ensurepip` ile birlikte), ilk bağımlılık kurulumunda İnternet erişimi ve `.venv` için yazılabilir bir proje dizini gereklidir. Pakete dahil olan panel için Node.js veya ön uç derlemesi gerekmez. Başlatıcıyı normal işletim sistemi hesabınızdan çalıştırın; TgWitness için yönetici/root ayrıcalıkları gerekmez.

- **Windows:** `Start.cmd`, önce `py -3`'yi, ardından `python`'yi, sonra da kullanıcı başına varsayılan ve Program Files kurulum klasörlerini kontrol eder ve 3.11 veya daha yeni bir sürümü gerektirir. Hiçbiri işe yaramazsa, yukarıda açıklanan otomatik kullanıcı başına kurulum seçeneğini sunar. `py -3 start.py` de çalışır. Taşınabilir paket için Python'a hiç gerek yoktur.
- **Linux:** `start.sh`, `python3.13`, `python3.12`, `python3.11`, `python3` ve `python`'yi dener ve uygun bir seçenek bulunmadığında apt, dnf, pacman, zypper, apk veya Homebrew için yükleme komutunu görüntüler. Debian/Ubuntu kurulumlarında, seçilen yorumlayıcıyla eşleşen `python3-venv` paketi gerekebilir. Dağıtımın eski varsayılan Python sürümü, Python 3.11+ ile değiştirilmeli veya bu sürümle desteklenmelidir.
- **macOS:** Güncel bir Python 3.11+ dağıtımını yükleyin; işletim sistemi tarafından sağlanan yorumlayıcının gereksinimi karşıladığını varsaymayın. Proje dizininden `python3 start.py` dosyasını kullanın.
- **Docker:** Compose v2.20 veya daha yeni bir sürümle birlikte Docker Engine/Desktop kullanın. Docker Desktop, Windows üzerinde Linux konteynerleri kullanmalıdır. Konteyner, kendi Python bağımlılıklarını yükler; ana bilgisayarda ayrı bir Python kurulumu gerekmez.

Veri dizini için kalıcı yerel depolama alanı kullanın. Mesajlar, medya dosyaları, WAL büyümesi, dışa aktarmalar ve yedeklemelerden yola çıkarak kapasite planlaması yapın; her iş yükü için kanıta dayalı evrensel bir minimum disk/RAM spesifikasyonu bulunmamaktadır. Uyumlu bağımlılık tekerlekleri olmayan CPU mimarileri ve Python sürümleri, ek derleme araçları ve bunların kendi yeterlilik testlerini gerektirebilir. "Taşınabilir" ifadesi, evrensel işletim sistemi veya donanım desteği iddiası değildir.

Windows 11/Python 3.12 yerel olarak doğrulanmıştır. Linux/macOS/konteyner tanımları ve CI sağlanmıştır ancak bu geliştirme sunucusunda çalıştırılmamıştır. Kesin kapsam için [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) dosyasına bakınız.

## Yerel bilgisayar

Windows'ta `Start.cmd`'yi, Linux/macOS'ta `sh start.sh`'yi kullanın. `scripts\Setup.cmd` veya `sh start.sh --setup-only`, ortamı hazırlar. Başlatıcı, ilk kullanımda bağımlılıkları yükler; sonraki başlatmalarda mevcut ortam yeniden kullanılır. Kurulum ve Telegram verilerinin toplanması için internet erişimi gereklidir, ancak mevcut kayıtlara göz atma ve dışa aktarma işlemleri çevrimdışı olarak gerçekleştirilebilir.

Kurulumdan sonra `python start.py --check` komutunu çalıştırarak, bir toplayıcı başlatmadan yerel bağımlılıkları, Ed25519'u, depolama alanını, anahtar yapılandırmasını ve dinleme adresini kontrol edin. Yapılandırılmış çıktı için `--json` komutunu kullanın. İstenen `--data-dir`, `--host` ve `--port` komutlarını çalıştırın. Bu kontrol, paket yüklemez, günlük oluşturmaz veya Telegram'a bağlanmaz; bu, bütünlük veya kapsam yeterliliği değerlendirmesi değildir. Başlangıç işlemi, mevcut günlükleri ayrı olarak doğrular. `python start.py --help` komutu da yüklemeyi gerektirmez.

Seçenekler:

start.py dosyasını kullandıktan sonra, Windows'ta `.venv\Scripts\python.exe`, Linux/macOS'ta `.venv/bin/python` ile yardımcı komutları çalıştırın veya önce bu ortamı etkinleştirin. Aşağıdaki `python -m ...` örnekleri, ortamın etkin olduğunu varsaymaktadır.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Ortam değişkenleri: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE, yeni bir kurulum için harici anahtar modunu seçer; aşağıya bakınız. TGWITNESS_TOKEN, belirtilirse en az 24 karakter içermelidir; kriptografik olarak rastgele bir değer kullanın. Bu değer belirtilmezse, uygulama panel-token.txt dosyasında 256 bitlik rastgele bir token oluşturur. Ortam değişkeni geçersiz kılma işlemi bu dosyayı yeniden yazmaz. Kimlik bilgilerini yenilemek için yeniden başlatın.

Bir veri dizinine tam olarak tek bir işlem sahip olabilir. Platformlar arası bir işletim sistemi dosya kilidi, kazara eşzamanlı yazma işlemlerini önler. Tek bir Uvicorn işçisi kullanın. Panel, profiller/<id>/ altındaki ek çalışma alanı dizinleriyle birlikte istediğiniz sayıda çalışma alanını yönetebilir. Ayrı hizmet örnekleri için ayrı dizinler ve bağlantı noktaları kullanın. SQLite WAL dosyaları, ağ dosya sisteminde değil, yerel kalıcı depolama alanında bulunmalıdır. Replikalar arasında tek bir birimi paylaşmayın.

## Windows taşınabilir paketi

Her GitHub sürümü, `TgWitness-<version>-windows-amd64-portable.zip` ve bunun `.sha256`'sini içerir. Bu sürüm, python.org'dan alınan resmi gömülebilir Python 3.12 çalışma zamanını (`tools/build_portable.py`'de sabitlenmiş sağlama toplamı), TgWitness'i ve sabitlenmiş bağımlılıklarını, ayrıca üç başlatıcıyı içerir:

| Dosya | Amaç |
| --- | --- |
| `TgWitness.cmd` | Paneli başlatın; ek seçenekler aktarılır, örneğin `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | `data\demo` adresinden sentetik demoyu başlatın |
| `TgWitness-Check.cmd` | Başlatmadan hazırlık kontrolünü çalıştırın |

Arşivin tamamını `Documents\TgWitness` gibi yazılabilir bir klasöre çıkarın; ZIP dosyasının içinden veya Program Files klasöründen çalıştırmayın. Çalışma ortamı izole bir modül yolu kullanır, bu nedenle diğer Python kurulumları ve `PYTHONPATH` onu etkilemez. Veriler, paketin `data` klasöründe kalır. Güncellemek için TgWitness’i durdurun, yeni sürümü yeni bir klasöre çıkarın ve `data` klasörünü buraya kopyalayın.

Python 3.12 kullanarak 64 bit Windows üzerinde kendiniz derleyin:

```
python tools/build_portable.py
```

Derleyici, çalışma zamanı sağlama toplamını doğrular, kısıtlanmış bağımlılıkları pakete yükler, gömülü yorumlayıcıyla hazırlık kontrolünü çalıştırır ve ZIP dosyasını ile sağlama toplamını `dist/` dosyasına yazar.

## Konteyner

```
docker compose up -d --build --wait
```

Bu, /data için adlandırılmış bir kalıcı birim oluşturur. Web bağlantı noktası 127.0.0.1:8787 adresine eşlenir. İşlem, yetkileri kaldırılmış UID 10001 olarak, salt okunur bir kök dosya sistemi ve yazılabilir /data ile /tmp ile çalışır. `--wait`, geri dönmeden önce web sunucusunun durumunu kontrol eder; Telegram yetkilendirme veya teslimatını gerçekleştirmez. Sağlanan yardımcı programlar, derlemeden sonra 180 saniyelik bir hazırlık zaman aşımı süresi kullanır. İlk bağımlılık indirmeleri bu süreden daha uzun sürebilir.

Her iki temel Compose dosyası da `tgwitness` proje adını kullanır; bu nedenle, yeni bir sürümü başka bir dizine çıkardığınızda sistem otomatik olarak yeni bir veri birimi seçmez. O proje için yalnızca bir dağıtımı aktif tutun. Bağımsız kurulumlar için benzersiz bir `docker compose -p NAME ...` adı ve farklı bir ana bilgisayar bağlantı noktası kullanın ve güncellemelerde her ikisini de koruyun. Farklı bir proje adı kullanan eski bir dağıtım için, orijinal adını `-p` ile birlikte kullanmaya devam edin; `docker compose ls`, mevcut projeleri listeler.

`deploy/env.example`'yi `.env`'ye kopyalayın ve `TGWITNESS_PORT`'yi farklı bir loopback bağlantı noktası kullanacak şekilde değiştirin. Örneğin, `TGWITNESS_PORT=8788` paneli `http://127.0.0.1:8788` adresinde açar; konteyner ise hâlâ 8787 numaralı bağlantı noktasını dinler. `.env`, Git tarafından göz ardı edilir.

İlk jetonu al:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Yararlı komutlar:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped`, bir çökme veya Docker arka plan programının yeniden başlatılmasından sonra toplayıcıyı yeniden başlatır. Linux sunucusunda, dağıtımınızın hizmet yöneticisini (genellikle `sudo systemctl enable --now docker`) kullanarak önyükleme sırasında Docker'ı etkinleştirin. Windows/macOS'ta, Docker Desktop'ın oturum açıldığında başlatma ayarını etkinleştirin. Masaüstü oturumunun kapatılması, uyku moduna geçilmesi veya durdurulmuş bir Docker arka plan hizmeti, toplama işlemini kesintiye uğratabilir. Açıkça durdurulmuş bir konteyner, siz onu yeniden başlatana kadar durdurulmuş halde kalır.

Örnek yapılandırmada /tmp biriminin üst sınırı 512 MiB olarak belirlenmiştir. Dışa aktarma yapısı bunun yerine kalıcı /data dizininde her çalışma alanının `temporary-exports/`'sini kullanır. Eşzamanlı dışa aktarmalar, günlük/WAL büyümesi, medya ve yedeklemeler için burada yer ayırın. Başlatıcı, deploy/constraints.txt dosyasını kullanarak uygun çalışma zamanı bağımlılık sürümlerini sabitler. Docker ve yüksek güvenilirlikli sunucular, pip --require-hashes komutuyla deploy/requirements.lock ve deploy/build.lock dosyalarından yükleme yapar: her paket dosyası, commit'te kaydedilen bir SHA-256 değeriyle eşleşmelidir; bu nedenle PyPI veya bir aynada değiştirilen dosyalar reddedilir. Python temel görüntüsü ve işletim sistemi paketleri için hâlâ bağımsız sürüm onaylaması gereklidir.

Günlüğü ve anahtarları silmek istemediğiniz sürece docker compose down -v komutunu kullanmayın. Konteyner durum raporu, web sunucusunun erişilebilirliğini bildirir; Telegram mesajlarının başarılı bir şekilde yakalandığını göstermez. Paneldeki toplayıcının durumunu, kalp atışını, hatalarını ve kapsama olaylarını inceleyin.

### Bağımsız tanık profili

İsteğe bağlı `witness` hizmeti, kendi konteynerinde [bağımsız bir tanık](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/) çalıştırır; bu tanığın `witness-data` biriminde kendi anahtarı ve günlüğü bulunur ve toplayıcı için yalnızca okunur bir tanık jetonu vardır. Jetonu panelin **Tanık** sayfasında oluşturun, bunu bir bot jetonu ve kanal ile birlikte `.env`'ye ekleyin, ardından profili başlatın:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Hizmet, Compose ağı içindeki toplayıcıya `http://tgwitness:8787` adresinden ulaşır (`TGWITNESS_WITNESS_COLLECTOR` bu değeri geçersiz kılar; örneğin, `/profiles/<workspace ID>` başka bir çalışma alanı için). Başka biri tarafından işletilen ayrı bir sunucudaki tanık dosyası için, `deploy/compose/compose.witness.yaml` dosyasını kullanın ve `TGWITNESS_WITNESS_COLLECTOR` 'yi toplayıcının HTTPS adresine ayarlayın; bu dosya yalnızca tanık dosyasını içerir.

## Yayınlanmış bir görüntüyü yükleyin

Bu, başarılı bir [sürüm yayın iş akışı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/#automated-github-releases) ve halka açık GHCR paketi yapılandırmasının ardından kullanıma açılır. Deponun sahibi/adı bu kaynak ağacına sabit olarak kodlanmamıştır. Söz konusu sürümün iş akışı özetinde gösterilen görüntüyü kullanın.

`deploy/env.example`'yi `.env`'ye kopyalayın. `TGWITNESS_IMAGE`'yi, **küçük harfli** depo yolunu kullanarak yayınlanan sürüme ayarlayın, örneğin:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

`compose.yaml` yerine bu dosyayı tek başına çalıştırın:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Ana bilgisayarda kaynak derleme, Python veya derleyici gerekmez. Sürüm yayın iş akışı, Docker Desktop'ın Linux sanal makinesi dahil olmak üzere Linux AMD64 ve ARM64 kapsayıcılarını hedefler. İş akışı özetinden bir sürüm etiketi veya `ghcr.io/owner/repository@sha256:...` kullanın. `latest` etiketinin taşınması veya gözetimsiz uygulama yükseltmesi yapılandırılmamıştır. Proje adları eşleştiğinde, görüntü ve kaynak varyantları aynı veri hacmini kullanır.

## Sunucuda otomatik HTTPS

Docker yüklü bir sunucu, sizin kontrolünüz altındaki bir alan adı ve kalıcı yerel depolama alanı kullanın. Etki alanının A/AAAA kayıtlarını sunucuya yönlendirin; AAAA kaydını yalnızca IPv6 adresi sunucuya ulaşırsa yayınlayın. Sertifika düzenlenmesi için gelen TCP 80 ve 443 bağlantılarına ve giden DNS/HTTPS trafiğine izin verin. Bu bağlantı noktaları başka hizmetler tarafından zaten kullanılmamalıdır.

`deploy/env.example`'yi `.env`'ye kopyalayın ve şema veya yol olmadan bir ana bilgisayar adı belirleyin:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

HTTPS katmanıyla kaynak derlemesini başlatın:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Yayınlanmış bir görüntü için, bunun yerine ilk dosya olarak `deploy/compose/compose.image.yaml`'yi kullanın. `-f` argümanlarının her ikisini de daha sonraki durum, günlük, güncelleme ve durdurma komutları için saklayın.

Caddy, bir sertifika alır ve yeniler, HTTP'yi HTTPS'ye yönlendirir ve istekleri özel Compose ağındaki toplayıcıya iletir. Sertifika durumunun kendine ait kalıcı bir birimi vardır. Toplayıcının doğrudan ana bilgisayar bağlantı noktası yalnızca döngü içi (loopback) olarak kalır. Sağlanan Caddy yapılandırması, erişim günlüğü kaydını etkinleştirmez.

`https://watch.your-domain.org` dosyasını açın ve panel jetonunu girin. Hazırlık durumu, sertifika düzenlemesini veya harici erişilebilirliği teyit etmez. HTTPS hazır değilse, DNS'yi, güvenlik duvarı kurallarını ve aşağıdakileri kontrol edin:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

Sağlanan Caddy görüntüsü, `2-alpine` etiketini takip eder. Pull komutu bu görüntüyü yeniler; sabit altyapı sürümlerine ihtiyacınız varsa, dağıtımınıza test edilmiş bir özeti sabitleyin.

## Güncellemeler ve yedeklemeler

Güncellemeler boyunca Compose proje adını ve veri hacmini koruyun. Öncelikle toplayıcıyı durdurun ve tam bir yedekleme yapın. Varsayılan kaynak tabanlı dağıtım için:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Her seferinde, depo dışında yeni bir yedekleme hedefi kullanın ve bunu hesap erişim materyali olarak koruyun. Örnek yol sadece açıklayıcıdır; kendi özel yedekleme konumunuzu kullanın. Gizli dosyalar, tüm çalışma alanları, anahtarlar, günlükler ve medya dahil olmak üzere tüm dizini kopyalayın. Yapılandırılmışsa, harici kasa ana anahtarını ayrı olarak yedekleyin. Kanıt ZIP dosyası, geri yüklenebilir bir uygulama yedeği değildir. HTTPS için, sertifika/hesap durumunu korumak gerekiyorsa Caddy birimlerini de saklayın.

Kaynak dağıtımı için yeni sürüm dosyalarını edinin ve şu komutu çalıştırın:

```
docker compose up -d --build --wait
```

Görüntü dağıtımı için `TGWITNESS_IMAGE`'yi istediğiniz sürüme değiştirin, ardından şunu çalıştırın:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Yukarıdaki durdurma/kopyalama komutları için de kurulumunuzun Compose dosyalarını kullanın. `.env`'yi, özel yapılandırmayı ve aynı proje adını koruyun. `down`, adlandırılmış hacimleri korur; **`down -v`** ise **bunları siler**. `.venv`'yi işletim sistemleri veya Python sürümleri arasında kopyalamayın. Yerel güncellemeler için TgWitness'i durdurun, tüm veri dizinini yedekleyin, kaynak dosyaları değiştirin ve başlatmadan önce `python start.py --setup-only`'yi çalıştırın.

Güncellemeden sonra panel erişimini, hesap kimliğini, gözlem durumunu ve kapsama alanını kontrol edin. Yeniden başlatma, kaçırılan Telegram güncellemelerini geri getirmez. Gelecekteki bir sürümde depolama formatları değişirse, geri alma işlemi için güncelleme öncesi yedeğe ihtiyaç duyulabilir.

## Otomatik GitHub sürümleri

Bu proje, Actions özelliği etkinleştirilmiş bir GitHub deposuna yüklendikten sonra [sürüm yayınlama iş akışı](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) kullanıma hazır hale gelir. Bu iş akışı, ön sürüm dahil olmak üzere bir GitHub Sürümü yayınlandığında çalışır. Taslaklar ve etiket yüklemeleri tek başına paketlerin yayınlanmasına yol açmaz.

1. Paket sürümünü ve değişiklik günlüğünü belirleyin, ardından `v` etiketiyle ve `pyproject.toml`'nin tam sürümünü (örneğin `v0.7.0`) içeren bir sürüm yayınlayın.
2. İş akışı, etiketi doğrular ve paylaşılan Windows/Linux/macOS Python, general/account-import/QR tarayıcı, kaynak paket ve Docker kontrollerini çalıştırır. Ayrıca, Python 3.12 kullanılarak üç işletim sisteminin tümünde yeni yerel kurulum da gerçekleştirilir.
3. Bu kontrollerden geçtikten sonra, QEMU altında bir ARM64 görüntüsünü hızlı test eder, AMD64/ARM64 görüntülerini `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`'ye yayınlar ve kaynak ZIP dosyasını, sağlama toplamını ve Python wheel dosyasını sürüme ekler. Ayrı bir Windows görevi, taşınabilir ZIP dosyasını ve sağlama toplamını derler ve ekler.
4. İlk yayınlamadan sonra, GHCR paket ayarlarını açın ve anonim görüntü alımları planlanıyorsa görünürlüğü "**Herkese Açık**" olarak ayarlayın. Yalnızca herkese açık bir kaynak deposu kendi başına herkese açık bir konteyner paketini garanti etmez. Kurum politikaları paket yayınlamasına izin vermelidir. İş akışı `GITHUB_TOKEN` kullanır; depoda herhangi bir kayıt şifresi veya VPS kimlik bilgileri bulunmamalıdır.

Bu yerel hazırlık ile uzaktan iş akışının başarısı henüz kanıtlanmamıştır. ARM64 emülasyonu, yerel donanım veya canlı Telegram yeterliliği değil, bir ön test niteliğindedir. Bu, sürüm paketlemeyi otomatikleştirir; bir sunucuyu başlatmak için hala Compose komutu ve bunun etki alanı/ana bilgisayar ön koşulları gereklidir. Bir sürüm yayınlandığında mevcut sunucular sessizce yükseltilmez veya yeniden başlatılmaz.

## Uzak sunucu

Hizmeti loopback ile sınırlı tutun ve bir SSH tüneli kullanın ya da HTTPS'yi bir ters proxy'de sonlandırın. Temel Compose dosyası yalnızca yerel kullanım içindir; isteğe bağlı `deploy/compose/compose.https.yaml` overlay'i, yapılandırılmış bir etki alanı için Caddy sağlar. Taşıyıcı belirtecini URL’lerden ve proxy günlüklerinden uzak tutun. Ters proxy, istek boyutunu ve bağlantı hızlarını sınırlamalıdır. Düz HTTP’yi İnternet’e maruz bırakmayın.

[deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) dizininde systemd, bir Windows oturum açma görevi, bir macOS kullanıcı ajanı ve Caddy için örnekler sunulmaktadır. Kurulumdan önce bunların yollarını gözden geçirin ve uyarlayın. Bunlar, yerel olarak yürütülen platform yapılandırmaları değil, şablonlar olarak sağlanmaktadır. Normal başlatıcı tarafından hiçbir arka plan hizmeti veya görevi kaydedilmez.

Windows'ta, penceresiz `pythonw.exe` başlatma işlemi, başlangıç/sunucu tanılama bilgilerini veri dizini altındaki `logs/server.log` dosyasına kaydeder (dosya başına 5 MiB, iki adet dönüşümlü yedek). Konsol başlatmalarında konsol günlüğü tutulur. HTTP erişim günlüğü her iki modda da devre dışıdır. Günlükleri veri diziniyle koruyun ve paylaşmadan önce gözden geçirin.

## Yeniden başlatma ve boşluklar

En son istenen gözlem durumu korunur. Gözlem etkin durumdaysa, başlangıç sırasında seçilen kaynaklara yeniden bağlanılmaya ve izlemeye devam edilmeye çalışılır. Manuel duraklatma, bu niyeti siler. Başarısız bir yeniden başlatma kaydedilir ve panelde gösterilir.

StringSession, yetkilendirmeyi korur ancak Telethon'un kalıcı güncelleme/varlık durumunu korumaz. Diyaloglar başlangıçta yeniden yüklenir. Telegram/Telethon, çalışırken bazı aktarım kesintilerini telafi edebilir, ancak TgWitness, işlem yeniden başlatmaları arasında kalıcı bir tekrar oynatma garantisi vermez. Her başlatma işleminde, önceki günlük başlığı ve çevrimdışı sınır kaydedilir. İzleyici, her 10 saniyede bir bağlantıyı kontrol eder ve her dakika bir kalp atışı ekler (**Parametreler → Canlılık kaydı her**). Kısa süreli kesintiler gözden kaçabilir; bağlı bir aktarım, güncellemelerin tam olarak iletilmesini garanti etmez. Anlık görüntüler, açıkça güncel geçmiş gözlemleridir; asla boşlukları doldurmaz.

Medya kuyruğu, her çalışma alanının SQLite veritabanında saklanır. Bir mesaj ve ilgili iş atomik olarak kaydedilir. Yürütülmesi kesintiye uğrayan işler, başlangıçta yeniden deneme amacıyla kurtarılır. Her indirme işlemi için 120 saniyelik bir temel zaman aşımı süresi ile dosya boyutuna göre 256 KiB/s hızda hesaplanan süre ve ek türü başına 1–2.000 MiB sınırı vardır; zaman aşımı, hız ve yeniden deneme ayarları **Parametreler** bölümünde bulunur. Toplayıcı, boyutu bilinmeyen dosyaları atlar. Duraklatma işlemi, kuyrukta bekleyen işleri korur. Yeniden deneme, orijinal gözlemlenen dosya tanımlayıcısını kullanır; daha sonra düzenlenmiş bir mesajın en son sürümünü asla kullanmaz. Geçici arızalar için sınırlı sayıda yeniden deneme vardır; FloodWait duraklamaları yeniden başlatma sonrasında da korunur. Medya kurtarma, Telegram güncelleme kurtarmasından ayrıdır ve kaybolan dosyaları yeniden oluşturamaz.

## Yedekleme, geri yükleme ve kapasite

Vault.key, signing.enc, credentials.enc, SQLite veritabanı/WAL dosyaları, medya, token, kontrol noktaları ve tüm profiller/alt dizinler dahil olmak üzere **tüm veri dizin**ini kopyalamadan önce işlemi durdurun. Hedef hizmet durdurulmuşken kopyanın tamamını geri yükleyin. Eksik vault anahtarları veya imza anahtarı uyuşmazlığı, başlatma işleminin başarısız olmasına neden olur; erişimi zorlamak için anahtarları yeniden oluşturmayın.

Gizli yedeklemeleri şifreli ve erişim kontrollü tutun. Kanıt ZIP dosyaları taşınabilirdir; uygulama yedeklemeleri veya Telegram oturum yedeklemeleri değil, inceleme artefaktlarıdır. Otomatik saklama süresi dolduktan sonra silme işlemi yoktur. Tüm mesajlar, ham meta veriler, medya dosyaları, geçici dışa aktarımlar ve yedeklemeler için disk alanı planlayın.

Günlüğün tamamını yüklemek yerine, başlangıç doğrulaması ve akış kayıtlarının dışa aktarımı. Dışa aktarım, okunan bir anlık görüntüyü sabitlerken yeni WAL yazma işlemleri devam edebilir; uzun süren dışa aktarımlar WAL sayfalarını tutabilir, bu nedenle disk kapasitesi hâlâ önemlidir. ZIP dosyaları, bağımsız doğrulayıcının varsayılan ayarına uymak üzere sıkıştırılmamış halde 4 GiB ile sınırlandırılmıştır; **Parametreler → En Büyük İmzalı ZIP** seçeneği bu sınırı artırır ve bu tür arşivler `verify.py --max-gib N` ile doğrulanır. Diğer formatlarda olay sayısı sınırı yoktur. Desteklenen tarayıcılar, yanıt parçalarını kullanıcının seçtiği bir dosyaya akış olarak gönderir. Diğer tarayıcılar en fazla 128 MiB'lik tampon kullanır ve daha büyük aktarımları kimliği doğrulanmış CLI'ye yönlendirir:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Başka bir çalışma alanı için **İhracat → Çalışma Alanı Kimliği**'nden `--profile ID`'yi, uzak bir sunucu için `--format zip|jsonl|csv|html`, `--url https://your-server`'yi veya 5 GiB aktarım sınırını değiştirmek için `--max-mib`'yi kullanın. Düz HTTP yalnızca loopback için izin verilir. Jetonlar başlıklarda iletilir, yönlendirmeler reddedilir, mevcut dosyalar üzerine yazılmaz ve tamamlanmamış indirmeler tamamlanmış dosyalar olarak yayınlanmaz. TGWITNESS_TOKEN, oluşturulan jetonu geçersiz kılarsa, bu aktif değeri içeren ayrı olarak korunan bir dosya kullanın: panel-token.txt dosyası, geçersiz kılma işlemiyle yeniden yazılmaz. Komutun SHA-256 değeri yalnızca bir aktarım sağlama toplamıdır; imzalı ZIP dosyasını bağımsız olarak doğrulayın.

Sunucu dışa aktarım dosyaları, her çalışma alanının özel `temporary-exports/` dizininde kalır. Başarılı işlemler, dosyalarını temizler. Kesintiye uğrayan dışa aktarımlar, özel örnek kilidi tutulmuş haldeyken bir sonraki çalışma alanının başlatılması sırasında kaldırılır. Bu dizin, depolama tehdidi/kapasite modelinin bir parçasıdır; şifrelenmiş bir veri birimi kullanın. Üretim ölçeğindeki birkaç gigabaytlık aktarımlar için yine de hedef sisteminizde uygunluk değerlendirmesi gereklidir.

Panel, kuyrukta bekleyen/başarısız medya öğelerini, en eski bekleyen medya öğelerini, boş disk alanını, Telegram istek duraklamalarını ve erişimi onaylanmamış kaynakları gösterir. Bu tanılama bilgileri, tam kapsamlı bir uçtan uca teslimat izleme aracı değildir. Çalışma alanları aynı süreci paylaşır; sorunlu bir hesap diğerlerini yine de etkileyebilir. Ayrı işçi süreçleri, saklama/dönüşüm, dayanıklı güncelleme kurtarma ve tam dağıtım yeterliliği devam etmektedir. Kapsamlı panel erişimi, [erişim ve izinler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) bölümünde belgelenmiştir; bağımsız kontrol noktaları ise [tanık](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/)kılavuzunda ele alınmaktadır.

## Bağlantı ve koruma seçenekleri

Bağlantı yolları çalışma alanı bazındadır ve yetkilendirme öncesinde yapılandırılmalıdır. SOCKS5/HTTP CONNECT, sabitlenmiş python-socks bağımlılığını kullanır. MTProxy, Telethon'un deneysel rastgele ara aktarımını kullanır; Sahte TLS ee gizli anahtarları desteklenmez. Doğrudan yedekleme, seçilen [IP](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/#ip-modes)moduna bağlıdır: Hide IP bunu reddeder; açık yedekleme modu ise bir gecikmeden sonra buna izin verir. Tünel/VPN modu doğrudan yollara izin verir ancak bir VPN oluşturmaz. Bu, sistem genelinde geçerli bir ağ politikası değildir.

Yeni kurulumlarda, TGWITNESS_VAULT_KEY_FILE değişkeni, ayrı olarak korunan rastgele bir ana anahtar dosyasına işaret eder. Bu dosyayı bir konteyner içinde /data dizininin dışında salt okunur olarak bağlayın. Her çalışma alanı ve ana anahtar için vault.external.json salt meta verilerini ayrı ayrı saklayın. Mevcut yerel kasalar için planlı bir geçiş gereklidir; bu değişkenin ayarlanması, kasaları otomatik olarak dönüştürmez. Mesaj/medya depolama ve dışa aktarımlar uygulama tarafından şifrelenmez. Gerektiğinde şifreli birimler ve yeterli miktarda özel geçici depolama alanı kullanın.

Ayrıntılı prosedürler: [bağlantı/güvenlik](https://phishdestroy.github.io/TgWitness/tr/docs/reference/connection/) ve [çalışma modları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/operations/).
