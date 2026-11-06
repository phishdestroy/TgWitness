# Yükleme, doğrulama ve güncelleme

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/

Tek bir komutla kurun, imzaları ve hash değerlerini kontrol edin, güncelleyin ve kurulumu kaldırın.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Proje](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Hızlı başlangıç](https://phishdestroy.github.io/TgWitness/tr/docs/reference/quickstart/) · [Dağıtım](https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/)

**On this page**

- [Install with one command](https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/#install-with-one-command)
- [Where everything runs](https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/#where-everything-runs)
- [Full-text search settings](https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/#full-text-search-settings)
- [Command-line access](https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/#command-line-access)
- [Verify before running](https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/#verify-before-running)
- [Update an existing installation](https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/#update-an-existing-installation)
- [Everyday commands on Ubuntu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/#everyday-commands-on-ubuntu)
- [Remove TgWitness](https://phishdestroy.github.io/TgWitness/tr/docs/reference/installation/#remove-tgwitness)

## Tek bir komutla kurun

Kılavuzlu yükleyici, özel bir Python çalışma ortamı içerir. Gelecekteki kurulumlar için aynı adresi kullanın: her yayın, yükleyiciyi, hash değerlerini, imzaları ve derleme bilgilerini bir arada günceller.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Ubuntu sunucusunda, arka plan hizmetini kurmak için root olarak çalıştırın. Masaüstü bilgisayarda ise normal kullanıcı hesabınızla çalıştırın.

**Windows (PowerShell veya Komut İstemi):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Windows'ta yönetici gerekmez. Alt PowerShell işlemi, sonuçla birlikte terminalinizi açık bırakır. Python ve bağımlılıklar kurulum içinde kalır.

Ubuntu'da "**Bu bilgisayar**", "**Geçici HTTPS bağlantısı**" veya **"Kendi etki alanı**" seçeneklerinden birini seçin. Yükleyici, panel adresini ve erişim anahtarını görüntüler. Geçici bir bağlantı için, tarayıcınızda bu HTTPS adresini açın ve anahtarı girin. Uzak bir sunucuya yerel erişim durumunda, bilgisayarınızdan bir SSH yönlendirmesi kullanın (`ssh -L 8787:127.0.0.1:8787 user@server`) ve açın `http://127.0.0.1:8787`. macOS ve Windows'ta yerel panel tarayıcınızda açılır; terminalini çalışır durumda tutun.

Panelde Telegram'a giriş yapın ve neyin toplanacağını seçin. Yalnızca kurulum Telegram'da veri toplama işlemini başlatmaz.

## Her şeyin çalıştığı yer

`get.destroy.tools` **Statik indirmeleri sunan Cloudflare Worker**'dir. TgWitness paneli, Telegram oturumu veya kullanıcı kanıt veritabanı yoktur. Bir proje VPS'sine yönlendirilmez. Uygulama, komutu çalıştırdığınız makinede çalışır.

| Kurulum | Program | Veriler |
| --- | --- | --- |
| Ubuntu'da root olarak | `/opt/tgwitness` | Sistem hizmeti: `/var/lib/tgwitness-<installation ID>`; tam yol için `tgwitness paths` kullanın. |
| Linux / macOS kullanıcısı | `~/.local/share/tgwitness` | `data/live` bu kurulum kapsamında. |
| Windows kullanıcısı | `%LOCALAPPDATA%\TgWitness` | `data\live` bu kurulum kapsamında. |

Başka bir klasör `TGWITNESS_INSTALL_DIR` başka bir klasör seçin. Yüklü sürümler ve veriler ayrıdır. Yükleyici, hesaplarınızı, mesajlarınızı veya anahtarlarınızı indirme sitesine yüklemez. Cloudflare tünelini seçtiğinizde panel trafiği Cloudflare üzerinden gönderilir; kendi alan adınızı kullanırsanız trafik kendi sunucunuza yönlendirilir.

Her kurulumda, yerel yollar, komutlar ve depoya bağlantılar içeren **START-HERE.html** ve **START-HERE.txt** dosyaları bulunur. `tgwitness guide` komutunu çalıştırın. Windows'ta, `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` komutunu kullanın.

## Tam metin arama ayarları

[Tam metin arama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/search/) (önizleme) için herhangi bir kurulum gerekmez. Dizin, güncellemeden sonra arka planda oluşturulur.

| Değişken veya komut | Etki |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Varsayılan: dizin, `search/fulltext.sqlite3` saklanır |
| `TGWITNESS_FULLTEXT=memory` | Dizin dosyası yoktur; dizin her başlatmada yeniden oluşturulur |
| `TGWITNESS_FULLTEXT=off` | Dizin yok; yalnızca tam metin araması |
| `tgwitness index status` | Her çalışma alanının dizin durumu |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | İmzalı günlüğün tüm dizinlerini yeniden oluşturun |

Yöneticinin **Günlük → Filtreler → Arama dizini**'ndeki seçimi, o çalışma alanı için değişkeni geçersiz kılar. Komutlar, kendilerini çalıştıran kurulumun veri dizinini bulur; diğer yerlerde, `--data-dir` buradaki yolu ekleyin `tgwitness paths`. Tam Ukraynaca sözlük (GPL-3.0 verileri) için, `pymorphy3-dicts-uk` kurulumun Python ortamına yükleyin.

## Komut satırı erişimi

[Komut satırı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/cli/) (önizleme), komut dosyaları ve ajanlar için arşivi okur.

| Değişken | Etki |
| --- | --- |
| `TGWITNESS_URL` | Aşağıdaki panel adresi `tgwitness search`, `context`, `messages`, `stats` ve `export`; varsayılan `http://127.0.0.1:8787` bir jeton ayarlandığında |
| `TGWITNESS_MCP_TOKEN` | **Entegrasyonlar → MCP** bölümünden, MCP istemcileriyle paylaşılan bağlantı jetonunu arşivleyin; `--token-file` bunun yerine bir dosyadan okur |
| `TGWITNESS_DATA` | URL veya belirteç belirtilmediğinde `--data-dir`, URL veya belirteç belirtilmediğinde |

## Çalıştırmadan önce doğrulayın

Tek satırlık komut, ilk komut dosyası için HTTPS'ye güvenir. Bu komut dosyası, kurulumdan önce SHA-256'yi ve uygulama ile kısıtlamalar üzerindeki projenin RSA imzasını kontrol eder. Ayrıca, ilk komut dosyasını önceden indirip doğrulayabilirsiniz.

Genel yayın anahtarı [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub)'dır. SHA-256'si şöyledir:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Güvendiğiniz bir depo revizyonundan bu parmak izini saklayın. Aynı indirme sunucusundan alınan bir sağlama toplamı, uyuşmazlığı tespit eder; bağımsız olarak güvenilir olan açık anahtar, sürüm imzasını doğrulayan unsurdur.

Aşağıdaki doğrulama indirmeleri için yeni ve boş bir dizin kullanın.

**Linux / macOS — yeni ve boş bir indirme dizininde çalıştırın** (curl ve OpenSSL gereklidir):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

Eğer `&&` indirme, anahtar parmak izi veya imza kontrolü başarısız olursa zincir yürütülmeden önce durur. Komut dosyasının indirilmesi ile imzalanması arasında bir yayın gerçekleşirse , her ikisini de yeniden indirin. Eski yükleyiciler, değiştirilemez paket URL'lerini korur.

**Windows — çalıştırmadan önce SHA-256 öğesini inceleyin:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Hash değerini `install.ps1` satırla karşılaştırın. Bağımsız bir imza kontrolü için, OpenSSL'i (örneğin, Git Bash'tan) ve yukarıdaki aynı açık anahtar parmak izini kullanın:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Windows kurulum sistemi, paket imzalarını .NET ile doğrular ve OpenSSL gerektirmez. Bunlar, Authenticode değil, ayrık RSA-3072 / SHA-256 imzalarıdır. [Manifest](https://get.destroy.tools/manifest.json) dosyası, yazılım sürümünü, tam Git commit'ini, değiştirilemez sürüm kimliğini ve her bir artefaktın SHA-256'sini kaydeder. Sayfa, ilgili kaynağa bağlantı sağlar. Manifest dosyası ve sağlama toplamı listesi de ayrık imzalara sahiptir (`manifest.json.sig` ve `SHA256SUMS.txt.sig`).

## Mevcut bir kurulumu güncelleme

**Yeni bir yayın, indirme sitesini günceller; yüklü programlar, kurulum programını tekrar çalıştırdığınızda güncellenir.** Katılımsız güncelleyici veya çalışmakta olan bir koleksiyonun otomatik olarak yeniden başlatılması yoktur. Mevcut kurulum kanalı **önizleme** aşamasındadır; yayınlanmış ve kontrol edilmiş derlemeleri takip eder `main`; bu sürümlerin commit'leri, son numaralandırılmış GitHub sürümünden daha yeni olabilir. Sayfanın sürümü `pyproject.toml`; commit ve derleme kimliği, aynı önizleme sürümü içindeki güncellemeleri birbirinden ayırır.

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

Daha önce kullandığınız kurulum klasörünü ve işletim sistemi kullanıcısını kullanın. Toplama işlemi durdurulmuşken tüm veri dizinini yedekleyin; `tgwitness paths` bunu tanımlar. İmzalı bir dışa aktarım tam bir kurulum yedeği değildir.

**Ubuntu'da kök kurulum adresi: `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Kurulum başarıyla tamamlandıktan sonra:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Linux/macOS kullanıcıları için kurulumda, orijinal `TGWITNESS_INSTALL_DIR` veya varsayılan ayarları kullanın ve ilk kurulum komutunu tekrar çalıştırın. Güncellemeden önce ön plandaki paneli kapatın ve güncelleme tamamlandıktan sonra yeniden başlatın. Yapılandırılmış bir Linux kullanıcı hizmeti için, ilgili `tgwitness restart` komutunu çalıştırın.

**Windows:** Çalışan paneli kapatın, Windows kurulum komutunu tekrar çalıştırın, ardından `bin\tgwitness.cmd` aynı kurulumda açın. Yükleyici verileri, oturumları, erişim ayarlarını ve imzalama anahtarlarını korur. Yükleyici, yalnızca yeni ortam kontrolleri geçtikten sonra başlatıcıyı değiştirir; kurulum başarısız olursa önceki başlatıcı yerinde kalır. Depolama formatı değişiklikleri için yükseltme öncesi yedeği saklayın.

## Ubuntu'da günlük komutlar

| Komut | Sonuç |
| --- | --- |
| `tgwitness open` | Güncel panel URL'si ve erişim anahtarı. |
| `tgwitness paths` | Program, veri ve kılavuzların tam yolları. |
| `tgwitness guide --print` | Çevrimdışı kullanım talimatları. |
| `tgwitness status` / `tgwitness logs` | Kullanılabilirlik / hizmet günlükleri. |
| `tgwitness stop` / `tgwitness start` | Hizmeti durdurun / devam ettirin; verileri koruyun. |
| `tgwitness token rotate` | Yönetici anahtarını değiştirin ve tarayıcı oturumlarını sonlandırın. |
| `tgwitness tunnel off` | Genel hızlı tüneli devre dışı bırakın; yerel paneli koruyun. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Hızlı tünel bağlantısı oluşturun / adresini değiştirin. |

İş arkadaşları için [erişim](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) jetonları, oturumlar ve IP kısıtlamaları ile GitHub'dan Cloudflare'e sürüm yayınlama iş akışı hakkında bilgi için [yükleyici yayınlama](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) bölümüne bakın.

## TgWitness öğesini kaldır

Kaldırma programı yoktur: paneli durdurup klasörlerini silmeniz yeterlidir. Veri klasörünü silmek, günlükleri, imzalama anahtarlarını, Telegram oturumlarını ve kaydedilmiş dosyaları kalıcı olarak yok eder. Bunu yapmadan önce:

1. İhtiyacınız olanı dışa aktarın (**Dışa Aktar → İmzalı ZIP'yi indir**) ve imza anahtarının parmak izini ile kontrol noktalarını bu makinenin dışında saklayın. Çalışma alanını korumak için, toplamayı durdurduktan sonra tüm veri klasörünü kopyalayın.
2. **Ekstra → Sunucu 24/7** altında oluşturulan sunucuları "**Sunucularınız"** bölümünden veya `python -m tgwitness.cloud destroy`; sağlayıcı, silinene kadar bunlar için ücretlendirir.
3. Telegram'da **Ayarlar → Cihazlar** bölümünden her hesabın oturumunu sonlandırın. Dosyaları silmek, Telegram tarafında oturumu kapatmaz.

**Ubuntu'da root kurulum.** Veri klasörünü not edin, hizmeti durdurun, ardından hizmeti, klasörleri ve kısayolu kaldırın:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux veya macOS kullanıcıları için kurulum.** Paneli kapatın. Yapılandırılmış bir Linux kullanıcı hizmeti şu komutla durdurulur `systemctl --user disable --now tgwitness-<ID>`; birimi `~/.config/systemd/user/`. Ardından `~/.local/share/tgwitness` (veya kendi `TGWITNESS_INSTALL_DIR`) dosyasını ve `~/.local/bin/tgwitness` kısayolu silin.

**Windows.** Paneli kapatın ve `%LOCALAPPDATA%\TgWitness` (veya `TGWITNESS_INSTALL_DIR`). Yükleyici herhangi bir hizmet, zamanlanmış görev veya kısayol eklemez.
