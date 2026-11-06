# Yüksek güvenilirlikli dağıtım

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/

Hetzner veya Phala Cloud üzerinde 7/24 çalışan, mühürlenmiş bir sunucu, Gateway DNS ve üçüncü tarafların tekrarlayabileceği kontroller.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

High-assurance deployment adds independent checks of the collection environment to archive verification. The reviewer queries deployment and access records held by the cloud provider and Cloudflare, and an Intel TDX deployment adds hardware attestation of the collector's environment.

Sıradan yerel ve Docker kullanımı değişmemiştir. `python -m tgwitness.cloud`komutuyla dağıtmadıkça hiçbir şey çalışmaz ve toplayıcı, yalnızca dağıtım ayarlandığında ana bilgisayarını okur `TGWITNESS_ASSURANCE`.

Akış şeması · Operatör → Sunucu, gelen trafiğe izin vermeyen güvenlik duvarı (sağlayıcı API&#x27;si); Operatör → Tünel ve DNS (Cloudflare API&#x27;si); Sunucu, gelen trafiğe izin vermeyen güvenlik duvarı → Tünel ve DNS (sadece giden); Sunucu, gelen trafiğe izin vermeyen güvenlik duvarı → Sunucuda oluşturulan imzalama anahtarı; Verifier, salt okunur belirteçler → Sağlayıcı günlüğü ve güvenlik duvarı; Verifier, salt okunur belirteçler → Tünel bağlayıcı adresi ve giriş; Verifier, salt okunur belirteçler → İmzalı /api/assurance beyanı; Verifier, salt okunur belirteçler → Kanıt ZIP dosyası · Operatör · Verifier, salt okunurbelirteçler · Sunucu, gelen trafiğe izinvermeyen güvenlik duvarı · Sağlayıcı günlüğü vegüvenlik duvarı · Tünel bağlayıcı adresi vegiriş · İmzalı /api/assurancebeyanı · Kanıt ZIP dosyası · Tünel ve DNS · Sunucuda oluşturulanimzalama anahtarı · sağlayıcı API&#x27;si · Cloudflare API&#x27;si · sadece giden

**Diyagramın metin olarak gösterimi**

1. Operatör → Sunucu, gelen trafiğe izin vermeyen güvenlik duvarı (sağlayıcı API&#x27;si)
2. Operatör → Tünel ve DNS (Cloudflare API&#x27;si)
3. Sunucu, gelen trafiğe izin vermeyen güvenlik duvarı → Tünel ve DNS (sadece giden)
4. Sunucu, gelen trafiğe izin vermeyen güvenlik duvarı → Sunucuda oluşturulan imzalama anahtarı
5. Verifier, salt okunur belirteçler → Sağlayıcı günlüğü ve güvenlik duvarı
6. Verifier, salt okunur belirteçler → Tünel bağlayıcı adresi ve giriş
7. Verifier, salt okunur belirteçler → İmzalı /api/assurance beyanı
8. Verifier, salt okunur belirteçler → Kanıt ZIP dosyası

**On this page**

- [What a verifier can check](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#what-a-verifier-can-check)
- [Providers](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#providers)
- [Confidential VM on Phala Cloud (Intel TDX)](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [Before you start](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#before-you-start)
- [From the panel](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#from-the-panel)
- [Quick tunnel without a domain](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [Deploy](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#deploy)
- [Debug deployment and lock](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#debug-deployment-and-lock)
- [Remove a deployment](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#remove-a-deployment)
- [Any server (self-attested)](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#any-server-self-attested)
- [Verify](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#verify)
- [Report for evidence handover](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare as an outside witness](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [Reading the deployment result](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#reading-the-deployment-result)

## Bir doğrulayıcının kontrol edebileceği şeyler

| İddia | Nasıl kontrol edilir? | Yöneten: |
| --- | --- | --- |
| Sunucu, bilinen bir zamanda sağlayıcı API'si aracılığıyla oluşturuldu | Sunucu nesnesi ve sağlayıcının kendi günlüğünde oluşturulması | Sağlayıcı |
| Hiç kimse sağlayıcının erişim yollarını kullanmadı | Konsol istekleri, kurtarma, şifre sıfırlama, yeniden oluşturma, ISO, görüntüler ve yedeklemelerin günlüğü | Sağlayıcı |
| Hiçbir şey buna bağlanamadı | Sağlayıcının güvenlik duvarında gelen trafiğe ilişkin kural yoktur; SSH, ilk açılışta gizlenir. | Sağlayıcı (güvenlik duvarı), ana bilgisayar (SSH) |
| Panele yalnızca tünel üzerinden erişilebilir | Tünel girişi yalnızca panele yönlendirilir; konektör sunucunun adresinden çalışır | Cloudflare |
| Bu yazılım tam olarak şu şekilde çalışır: | Toplayıcının imzalanmış kaynak ağacı hash değeri, dağıtılmış commit'in bir kopyasına eşittir | Collector, Git ile karşılaştırılarak kontrol edilir |
| İmza anahtarı o sunucuda oluşturuldu | Anahtar, sağlayıcının sunucu kimliğini ve aldığı cloud-init'in hash değerini belirten bir beyanı imzalar | Collector, sağlayıcıyla karşılaştırılarak kontrol edilir |
| Günlük, o anahtara ve sunucuya aittir | ZIP kanıtındaki her işlem başlangıcı, o sunucu için ana bilgisayar ölçümünü içerir | Kanıt ZIP |

The collector records SSH state, sessions, login history and boot information in signed process-start and `host.state` records. On an ordinary VM these are local inventory records, which the reviewer compares with the provider's independent records. The Intel TDX deployment below additionally verifies hardware-backed measurements.

## Sağlayıcılar

| `--provider` | Kimlik Bilgileri | Doğrulayıcının salt okunur erişimi | Doğrulayıcı için sağlayıcı günlüğü | Şu amaçla tutulur: |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Aynı projenin okuma jetonu | Sunucu ve güvenlik duvarı işlemleri | Kaynaklar mevcut olduğu sürece |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Salt okunur kişisel erişim jetonu | Droplet eylemleri | Droplet mevcut olduğu sürece |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` salt okunur kapsamlar | Hesap olayları, güvenlik duvarı kural sürümleri | 90 gün |
| `vultr` | `VULTR_API_KEY` | Okuma erişimi olan ve `activity_logs` izin | Hesap etkinlik günlüğü (yöntem, yol, aktör) | 30 gün; denetim günlüğü aboneliği ile daha uzun süre |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail olay geçmişi | 90 gün |
| `phala` | `PHALA_CLOUD_API_KEY` | Aynı çalışma alanına ait bir API anahtarı | Uygulama revizyonları ve CVM işlemleri: Docker Compose yapılandırması ve ortam değişiklikleri, yeniden başlatmalar, işletim sistemi yükseltmeleri | Uygulama mevcut olduğu sürece |
| `generic` | yok | yok | yok: **kendi kendini doğrulamış** | – |

Her vaka için ayrı bir proje, ekip, hesap veya alt hesap kullanın: doğrulayıcının salt okunur erişimi, yalnızca bu dağıtımı gösterir. Kimlik bilgileri, `--provider-token-file` yukarıdaki değişkenden okunur, asla komut satırından okunmaz. AWS için dosya şunu içerir `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; bölge `--location`.

Her sağlayıcının kayıtlarında görünmeyen bilgiler her raporda belirtilir. Kısaca: Hetzner konsol isteklerini kaydeder; DigitalOcean’ın Kurtarma Konsolu, Linode’un Lish/Glish’i ve Vultr’un web konsolu bu şekilde kaydedilmez, bu nedenle root ilk önyüklemede kilitlenir ve konsola giriş için şifre sıfırlama veya önyükleme değişikliği gerekir; bunlar ise kaydedilir. Vultr, konsol adresini, örneği okuyabilen herhangi bir anahtara döndürür; ne kayıtta ne de raporda bu adres saklanır.

## Phala Cloud üzerindeki Gizli VM (Intel TDX)

Toplayıcı `--provider phala` toplayıcı, dstack tarafından yönetilen [Phala Cloud](https://phala.com/) üzerindeki bir Intel TDX gizli sanal makinesinde çalışır. Barındırıcı ve Phala personeli, makinenin belleğini okuyamaz ve işlemci, makinenin neyle önyükleme yaptığına dair bir tasdik belgesi imzalar. Doğrulayıcı, Phala’nın sözüne güvenmez: `tgwitness.tdx` her bir tasdiki, sabitlenmiş Intel SGX Kök Sertifika Yetkilisi'ne kadar, Intel'in iptal listeleri ve Intel'in imzalı platform verileriyle karşılaştırarak kendisi kontrol eder ve hata ayıklanabilen veya taşınabilen makineleri reddeder.

| Rapor girişi | Neleri gösterir? |
| --- | --- |
| `tdx_binding` | Onay belgesi, toplayıcının imzalı beyanını ve bu isteğin rastgele değerini kapsar. |
| `tdx_quote` | Intel, bu tasdiki garanti eder; ancak Intel, platformu güncel olarak değerlendirdiğinde onay verilir. |
| `tdx_compose_hash` | dstack olay günlüğünden yeniden oynatılan RTMR3, toplayıcının raporladığı uygulama oluşturma işlemlerini ölçer. |
| `tdx_compose` | Bu kod, dağıtılan commit'in derlediği kodun bayt bayt aynısıdır: kaynak dosyalar hash ile, her iki görüntü de özet ile sabitlenmiştir; başka hiçbir kod yoktur. |
| `tdx_identity` | Doğrulama, Phala'nın KMS'sinden alınan anahtarlar ve şifrelenmiş bir disk ile birlikte, devreye alınmış uygulama ve örneğinden sağlanır. |
| `tdx_os` | MRTD ve RTMR0-2, doğrulayıcının Dstack-TEE tarafından yayınlanan dstack işletim sistemi görüntüsünden hesapladığı değerlere eşittir; bu değerler, CVM'nin bildirdiği işletim sistemi görüntüsü hash'i ve QEMU'nun sanal makinenin yapısı için oluşturduğu ACPI tablolarından elde edilir: bellenim, çekirdek, initrd, kök dosya sistemi hash'ini içeren komut satırı, bellek, vCPU'lar ve aygıtlar. Bir geliştirme görüntüsü başarısız olur |

İşletim sistemi görüntüsü (yaklaşık 180 MB, bunun 21 MB'si saklanır) bir kez [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) adresinden kayıtın yanındaki `dstack-images` konumuna indirilir; `--tdx-image FOLDER` başka bir klasör veya açılmış bir görüntü kullanır, `--tdx-image none` karşılaştırmayı atlar. Ölçüm, Dstack-TEE/dstack dizininden alınan `dstack-mr` ve `qemu-acpi` Rust paketini takip eder; `tools/check_dstack_image.py`, bunu QEMU’nun kendi ACPI çıktısıyla ve gerçek bir Phala Cloud donanım doğrulama kaydıyla karşılaştırır; `--live` ise yayınlanmış görüntüyle de karşılaştırır. `--tdx-measurements` ise MRTD ve RTMR0-2 değerlerini JSON formatında karşılaştırmaya devam eder.

Günlüğe kaydedilen her toplayıcı başlatma işlemi böyle bir doğrulama içerir, bu nedenle `verify --evidence` her başlatma işlemini ve önyüklenen işletim sistemi görüntüsünü kontrol eder. Phala'nın uygulama revizyonları ve CVM'nin işlemleri sağlayıcı günlüğü işlevi görür: dağıtımdan sonra değiştirilen bir Docker Compose yapılandırması raporun geçersiz kalmasına neden olur ve yeniden başlatmalar inceleme için listelenir.

Panelde **Ekstra** → **7/24 Sunucu** altından **Gizli sanal makine · Phala Cloud** seçeneğini seçin ve bir Phala Cloud API anahtarını yapıştırın; hızlı tünel, Hetzner'da olduğu gibi çalışır. Komut satırından:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` Intel'in sertifikalarını ve iptal listelerini Intel'den indirmek yerine bir dosyadan okur. Gateway DNS burada kullanılamaz: Phala'da giden trafik için sağlayıcı güvenlik duvarı bulunmamaktadır.

### Doğrulama sertifikası

Bir Phala dağıtımı için `verify --report certificate.md` ayrıca sertifikayı da yazar: bağımsız bir `certificate.html` ve bir A4 `certificate.pdf` dosyası; bu dosyalarda karar, Intel'in kök sertifikasından toplayıcı anahtarına kadar uzanan güven zinciri, standart ve yüksek güvenilirlikli sunucularla karşılaştırma, yayınlanan görüntüden hesaplanan değerlerin yanındaki ölçümler, her bir bölümün garantörleri, Intel sertifika zinciri, her kontrol, sağlayıcı günlüğü ve doğrulamanın nasıl tekrarlanacağı yer alır. JSON raporu resmi kayıt olarak kalır; sayfalar bunu görüntüler.

Rapor, `certificate.seal.json` dosyasında ve yanındaki `.tsq`/`.tsr` dosyalarında imzalar ve zaman damgaları ile dijital olarak mühürlenmiştir:

| Seal | Neler ekliyor? |
| --- | --- |
| Nitelikli elektronik zaman damgası, `http://tsa.belgium.be/connect` | Belçika federal hükümetinin nitelikli güven hizmeti sağlayıcısından (FPS Policy and Support, BOSA) alınan `certificate.json`'in tam baytları üzerinde RFC 3161 zaman damgası. Bu birim, Belçika'nın AB güvenilir listesinde nitelikli zaman damgası hizmeti olarak, "onaylanmış" statüsüyle listelenmiştir; kök (Belçika Kök CA6) ve listenin girişleri, 20 Ekim 2026 tarihinde yayınlanan listeye göre, `tgwitness/tsa_roots.py`'te sabitlenmiştir. (AB) 910/2014 sayılı Tüzüğün 41. maddesi uyarınca, bu tür bir zaman damgası, tarih ve saat açısından ve verilerin bütünlüğü açısından her AB üye devletinde doğru kabul edilir. |
| RFC 3161 zaman damgası, FreeTSA | İkinci, bağımsız bir zaman damgası |
| Doğrulayıcı imzası | Ed25519, raporun SHA-256 değerini ve her zaman damgasını belirten bir ifade üzerinde, doğrulayıcının kendi anahtarıyla (`--sign-with FOLDER`, varsayılan `~/.tgwitness/verifier`) uygulanır; PDF dosyası aynı anahtarla imzalanır |

`--timestamp URL` (tekrarlanabilir) diğer yetkilileri seçer, `--timestamp none` hiçbirini seçmez, `--sign-with
none` mührü imzasız bırakır. `check-report`, raporun hash değerini, doğrulayıcı imzasını, her zaman damgasını güvenilir bir kök sertifikaya ve onun nitelikli durumuna göre kontrol eder ve PDF'nin imzasını doğrular. AB dışında nitelikli bir zaman damgasının ve raporun bir bütün olarak hukuki geçerliliği, raporu alan mahkeme veya yetkili kuruma bağlıdır; mühür, raporun ne zaman mevcut olduğunu ve değiştirilmediğini gösterir.

Bir doğrulama, Intel’in TDX modülünde veya mikro kodunda bir kusuru ya da bellek veriyoluna fiziksel erişimi dışlayamaz. Phala’nın hesabındaki uygulamayı kontrol eden kişi, başka bir “compose” dağıtabilir; bu, yeni bir “compose” hash’iyle yeni bir revizyon olarak görünür. Ana bilgisayar, makinenin zaman kaynağını ve ağını kontrol eder.

Dağıtım, `--evidence` ile doğrulama, yeniden başlatmalar, işletim sistemi görüntüsü karşılaştırması, imzalar ve zaman damgalarıyla dijital olarak mühürlenmiş sertifika ve imha işlemleri Phala Cloud üzerinde gerçekleştirilmiştir; bkz. [, 4 Kasım 2026 tarihli çalıştırma](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026).

## Başlamadan önce

1. Bir Cloudflare bölgesi, hesap kimliği ve **Cloudflare Tunnel Edit**, **Zone Read** ve **DNS Edit** yetkilerine sahip bir API jetonu, `--cloudflare-token-file` veya `CLOUDFLARE_API_TOKEN`ile verilir. Doğrulayıcı için: **Cloudflare Tunnel Read**, **DNS Read** ve denetim günlüğü için **Account Settings Read**. Etki alanı olmadan, [hızlı tünel](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#quick-tunnel-without-a-domain) bunların hiçbirine ihtiyaç duymaz.
2. Özel bir projeye yazma erişimi olan sağlayıcı kimlik bilgileri; `lock` Aynı şeyi kullanır:

   - Hetzner: Okuma ve Yazma iznine sahip API jetonu;
   - DigitalOcean: yazma erişimine sahip kişisel erişim jetonu;
   - Linode: `linodes`, `firewall` ve `events` okuma/yazma kapsamlarına sahip kişisel erişim jetonu;
   - Vultr: Özel bir hesabın veya alt hesabın API anahtarı;
   - AWS: IAM kimlik bilgileri izin verilir `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` ve `ec2:RevokeSecurityGroupIngress`.
3. Çalıştırılacak commit. Bir sürüm etiketi, `git ls-remote`; sunucu her zaman yalnızca 40 karakterlik commit'i alır.

## Panelden

Kendi bilgisayarınızda, **Ekstralar → 7/24 Sunucu**, Hetzner için aynı `deploy` Hetzner için üç adımda çalışır: Avrupa veya Amerika Birleşik Devletleri'ni seçin, bir Hetzner jetonunu (Okuma ve Yazma) yapıştırın, ardından panelin o jetonla bulduğu sunucu türünü, aylık fiyatı, adresi ve sürümü inceleyin. Onay vermeden önce hiçbir şey oluşturulmaz. Panel, her adımı `deploy` bildirdiği şekilde gösterir, ardından adres, panel jetonu ve imza anahtarı parmak izi görüntülenir. Alan adı olmadan sunucuya bir [hızlı tünel](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#quick-tunnel-without-a-domain) atanır; **Sunucularınız → Güncel adresi bul** , yeniden başlatmanın ardından bunu tekrar arar. Kendi alan adınız altında sabit bir adres için **İsteğe bağlı · kendi alan adınız** 'yi açın ve bir Cloudflare jetonu ekleyin (hazırlanan bağlantı, Bölge Okuma, DNS Düzenleme ve Cloudflare Tüneli Düzenleme seçeneklerini seçer).

Jetonlar, her istekle birlikte tarayıcı sekmesinden aynı bilgisayardaki TgWitness adresine aktarılır ve hiçbir yere kaydedilmez; dağıtım kaydı, sansürlenmiş cloud-init, panel jetonu ve hızlı tünel için adres anahtarı, `deployments/NAME` veri dizini içinde saklanır. Panel, bunu yalnızca doğrudan bir loopback bağlantısı üzerinden ana yöneticiye sunar (`127.0.0.1`, proxy veya tünel başlıkları olmadan); ağ üzerinden erişilen bir panel ise bunun yerine komutları gösterir. Sürüm, varsayılan olarak çalışan panelin sürüm etiketidir ve bu, GitHub API'si aracılığıyla belirlenir. Konum, sunucu türü ve fiyat, Hetzner'in API'sinden alınır: `cpx22` sunuluyorsa buradan, aksi takdirde en az 2 GB belleğe sahip en ucuz x86 türü kullanılır.

## Etki alanı gerektirmeyen hızlı tünel

`--quick-tunnel` yerine geçer `--zone`, `--cloudflare-account` ve `--panel-host`; Cloudflare hesabı veya jetonu kullanılmaz:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Sunucuda, cloudflared panele bir [hızlı tünel](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) açar: bu, `https://….trycloudflare.com` adres açar; bu adres, cloudflared veya sunucu yeniden başlatıldığında değişir. Sunucudaki küçük bir hizmet, her adresi rastgele bir ntfy.sh konusuna gönderir; bu adres, yalnızca dağıtım dizininde bulunan bir anahtarla (HMAC-SHA256) imzalanır (`address-key.txt`) ve ntfy.sh gönderileri 12 saat boyunca sakladığı için bunu her üç saatte bir tekrarlar. `deploy` **Güncel adresi bul**, yalnızca imzalı gönderileri kabul eder; bu sayede sahte bir gönderi, sizi ve panel jetonunuzu başka birinin adresine yönlendiremez. Konu, kayıtta ve yayınlanan cloud-init'te bulunur: bunlara sahip olan herkes, hâlâ panel jetonunu isteyen güncel adresi okuyabilir. Sunucu, her iki durumda da gelen bağlantı noktası açmaz.

Bir doğrulayıcının adres anahtarı yoktur ve konuyu okuyan herkes bu konuya gönderi yapabilir. Bu nedenle toplayıcı kendi Ed25519 anahtarıyla imzalanmış adresi de yayınlar ve `verify`, dağıtım kaydında toplayıcı anahtarıyla imzalanmış en yeni gönderiyi alır; gönderiler, iddia ettikleri zamana göre değil, ntfy.sh'nin onları aldığı zamana göre sıralanır. Bu değişiklikten önceki bir toplayıcı hiçbir şeyi imzalamaz ve `verify` daha sonra en yeni gönderiyi alır ve bunu `statement` kontrolünde belirtir; sahte bir gönderi sadece bu kontrolün başarısız olmasına neden olabilir, çünkü adres yine de toplayıcının anahtarıyla yanıt vermelidir.

Maliyeti: Hiçbir Cloudflare hesabı hızlı tünelin kayıtlarını tutmaz, bu nedenle `verify`, tünel, konektör ve DNS kontrolünü kullanılamaz olarak bildirir ve sonuç en iyi ihtimalle `incomplete` olur (Phala Cloud'da ise kontrol başarılı olur: konektör, ölçülen Docker Compose yapılandırması içinde çalışır); sağlayıcı kayıtları, güvenlik duvarı, imzalı beyan, ana bilgisayar ölçümleri ve yükleyici karşılaştırması her zamanki gibi kontrol edilir. Referans yükleyiciyle yapılan bayt karşılaştırması, `--quick-tunnel`'i zaten tanıyan dağıtılmış bir commit gerektirir; 0.7.0 sürümünden yapılan bir checkout, etki alanı yükleyicisini oluşturur ve farkı bildirir. Cloudflare, hızlı tünellere çalışma süresi garantisi vermez, işlem sırasında 200 istek izin verir ve Server-Sent Events'i taşımaz; bu nedenle panelin canlı güncellemeleri (0.7.0'dan sonraki sürümler) bu tünel üzerinden gelmeyebilir ve sayfanın yeniden yüklenmesi gerekebilir; bu kısım henüz denenmemiştir. Kesintisiz çalışması gerekli bir durum için kendi etki alanınızı kullanın.

## Dağıtım

Öncelikle gönderilecek her şeye bir göz atın. `plan` Hiçbir sağlayıcıya veya Cloudflare’e istek göndermez:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Ardından aynı seçenekler ve kimlik bilgileriyle dağıtın:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Başlangıç için sunucu türleri: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` ve `--image` her bir sağlayıcının Avrupa bölgesindeki Ubuntu 24.04 sürümüne varsayılan olarak ayarlanır.

`--repository` başka bir https Git deposundan, URL’de kimlik bilgileri olmadan commit alır (varsayılan `https://github.com/phishdestroy/TgWitness.git`). `deploy` ayrıca `--out` başka bir dağıtım dizini için de kabul eder (varsayılan `deployments/NAME`; halihazırda bir dağıtım içeren bir dizin reddedilir) ve `--wait`, toplayıcının imzalı beyanı için beklenecek dakika sayısı: 1 ila 240, varsayılan 20 veya 60 `generic`.

Komut:

1. bir Cloudflare tüneli oluşturur; bu tünelin girişi, panel ana bilgisayar adını panele ve, varsa, tanık ana bilgisayar adını `/api/witness/head` ve `/api/assurance` sadece;
2. bu ana bilgisayar adları için proxy'li CNAME kayıtları oluşturur ve zaten mevcut olan adları reddeder;
3. gelen kuralları olmayan bir sağlayıcı güvenlik duvarı ve bunun arkasında SSH anahtarı, yedekleme, konsol ajanı bulunmayan ve SSH'yi maskeleyen, root erişimini kilitleyen, `cloudflared`, tam olarak o commit’i alır, kontrol eder ve TgWitness’yi güçlendirilmiş bir systemd hizmeti olarak başlatır;
4. toplayıcının imzalı beyanını bekler ve bu beyanın bu sunucuyu ve bu cloud-init'in hash değerini belirtip belirtmediğini kontrol eder.

`deployments/case-2026-11/` içinde şunlar bulunur:

| Dosya | İçindekiler | Paylaşmak ister misiniz? |
| --- | --- | --- |
| `deployment.json` | Kimlikler, hash değerleri, yapılan API çağrıları (yöntem, yol, durum) ve ilk imzalanmış ifade | Evet, doğrulayıcı ile |
| `cloud-init.redacted.yaml` | İki gizli bilgisi şu şekilde değiştirilmiş olan tam cloud-init komutu: `REDACTED` | Evet |
| `panel-token.txt` | Panel jetonu | Hayır |

Sağlayıcının kök şifresi, tünel jetonu ve panel jetonu hiçbir zaman `deployment.json`. Sonunda yazdırılan toplayıcı parmak izini, tek başınıza kontrol etmediğiniz bir kanal aracılığıyla yayınlayın ; örneğin bir tanık kanalı veya alıcıya gönderilen bir mesaj.

Telegram'da `https://case.example.org` adresinden, [hesap](https://phishdestroy.github.io/TgWitness/tr/docs/reference/accounts/)kılavuzunda belirtildiği gibi panel jetonuyla Telegram'da oturum açın. Panel eylemleri imzalı günlüğe kaydedilir; bunlar SSH oturumları değildir. Bir [tanık](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/), `https://case-witness.example.org`.

SSH yoktur: önyükleme başarısız olursa, toplayıcı asla yanıt vermez. Sunucuyu silip yeniden dağıtın veya nedeni bulmak için hata ayıklama dağıtımı kullanın.

### Kullanıcı verilerindeki gizli bilgiler

Cloud-init iki gizli bilgiyi taşır: panel jetonu ve Cloudflare tünel jetonu. İmza anahtarı bunların arasında yer almaz; sunucuda oluşturulur. Hetzner, DigitalOcean ve Linode, API'leri aracılığıyla kullanıcı verilerini döndürmez. Vultr, örneği okuyabilen herhangi bir anahtara bu verileri döndürür; EC2 ise `DescribeInstanceAttribute`. AWS için doğrulayıcıya yalnızca tablodaki üç eylemi verin, asla `ec2:Describe*`. Vultr için, doğrulayıcının anahtarının her iki jetonu da okuyabildiğini varsayalım. Bir tünel jetonu, birinin ikinci bir konektör çalıştırmasına izin verir: `verify` sunucuda bulunmayan herhangi bir konektörü bildirir ve toplayıcının ifadeleri bu şekilde taklit edilemez çünkü her biri yeni bir meydan okumayı imzalar. `--quick-tunnel` ikinci gizli anahtar ise adres anahtarıdır: bunu okuyan herhangi biri, panelin kabul edeceği sahte bir adres gönderebilir.

Toplayıcının kamuya açık açıklamasında sunucunun adresi ve oturum açma kaynakları belirtilmez; her ikisi de imzalı günlüğünde yer alır.

## Hata ayıklama dağıtımı ve kilitleme

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` SSH, tek bir adresten veya küçük bir ağdan gelen tek bir anahtar için saklanır; IPv4 için en fazla /24 veya IPv6 için en fazla /48. `KEY` zaten sağlayıcıya kayıtlıdır: Hetzner projesindeki bir SSH anahtarının adı veya kimliği, DigitalOcean ekibindeki bir SSH anahtarının kimliği veya parmak izi, SSH anahtarları root'a eklenen bir Linode kullanıcı adı, Vultr hesabındaki bir SSH anahtarının kimliği veya bölgedeki bir EC2 anahtar çiftinin adı. Bu seçenekler `generic`. Bu tür bir dağıtım `debug` şeklinde kaydedilir ve **asla** yüksek güvenilirlikli olarak raporlanmaz. İşiniz bittiğinde, `sudo tgwitness-lock` son SSH oturumunun son komutu olarak çalıştırın, ardından:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Güvenlik duvarı tüm gelen kuralları kaybeder. Raporlar daha sonra SSH’ye ne zaman izin verildiğini ve ne zaman kapatıldığını gösterir; bu pencere görünür kalır.

## Bir dağıtımı kaldır

`destroy` dağıtımın etiketine göre sunucuyu ve güvenlik duvarını siler; böylece yarı yolda başarısız olan bir dağıtım da kaldırılır; ardından tüneline yönlendiren DNS kayıtları ve tünel silinir. Sunucunun günlüğü ve imzalama anahtarı da bununla birlikte silinir: önce kanıtları dışa aktarın. Kayıt, `removed`, kaldırma işleminin API çağrılarıyla birlikte kalır.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Hetzner için API üzerinden silme işlevi uygulanmıştır. Diğer sağlayıcılar için `destroy` herhangi bir şeyi silmeden önce durur ve sağlayıcının konsolunda silinecek etiketin adını belirtir. Elle kurulan bir sunucu (`generic`) yalnızca tünelini ve DNS kayıtlarını kaybeder. Hızlı tünel dağıtımı için Cloudflare jetonuna gerek yoktur: tüneli sunucuda sona erer ve gönderileri ntfy.sh'den 12 saat içinde silinir.

## Herhangi bir sunucu (kendi kendini doğrulayan)

`--provider generic` Bu, satın alınan veya manuel olarak kurulan bir sunucu içindir. `deploy` tüneli ve DNS'yi oluşturur, `install.sh` (özel) ve `install.redacted.sh` (yayınlamak için) yazar ve bekler. Kopyalayın `install.sh` yeni kurulmuş bir Ubuntu 24.04 sunucusuna kopyalayın ve orada çalıştırın:

```
sudo bash install.sh
```

Sunucuyu olduğu gibi kaydeder (girişler, hesaplar, `authorized_keys`, dinleme soketleri, hizmetler, zamanlanmış işler, paketler), taahhüdü yükler, ana bilgisayar güvenlik duvarını etkinleştirir, kendini siler, SSH’yi maskeler ve oturumu sonlandırır. Böyle bir sunucuya ait rapor en iyi ihtimalle **KENDİ KENDİNİ DOĞRULAMALI’dır**: yükleyiciyi çalıştıran kişi, bunu yapmadan önce root erişimine sahipti ve doğrulayıcının elinde hiçbir sağlayıcı kaydı bulunmamaktadır. Yine de açıklanamayan bir sunucudan daha iyidir: envanter, yükleyici hash’i ve sonraki her oturum açma işlemi imzalanmıştır.

## Doğrula

Doğrulayıcının şunlara ihtiyacı vardır `deployment.json`, yayınlanmış yükleyici, salt okunur kimlik bilgileri ve ideal olarak, ilgili commit'in bir kopyası ile bir kanıt ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Her sağlayıcı ve Cloudflare değeri, o anda doğrulayıcı tarafından talep edilir; kayıt sadece sorgulanacak kimlik numaralarını sağlar. Çıkış kodu, **PASS** için 0, **FAIL** için 1 ve **REVIEW**, **INCOMPLETE** veya **SELF-ATTESTED** için 2'dir. `--fingerprint` bağımsız bir kanaldan gelmelidir; bu olmadan anahtar yalnızca operatörün kaydıyla karşılaştırılır. `python verify.py` ZIP, [Evidence](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) bölümünde olduğu gibi kanıtı yine kendisi doğrular.

Sağlayıcı eylemleri sınıflandırılır: oluşturma ve oluşturulduktan sonraki 30 dakika içinde başlatma işlemleri geçer; konsol, kurtarma, şifre sıfırlama, yeniden oluşturma, ISO, görüntüler, anlık görüntüler, yedeklemeler, Sistem Yöneticisi, EC2 Instance Connect ve güvenlik duvarı açılışları başarısız olur; güç eylemleri ve beklenmeyen her şey inceleme için işaretlenir. Bilinmeyen bir eylem asla sessizce geçmez.

## Kanıt teslimi raporu

`--report report.md` Markdown raporunu yazar ve `report.json` yanında:

1. sonuç, toplayıcı anahtar parmak izi, dağıtım, sağlayıcı, commit, sunucu, güvenlik duvarı, tünel;
2. her kontrolün durumu ve kaynağı (sağlayıcı API'si, Cloudflare API'si, toplayıcı beyanı, kanıt günlüğü);
3. her eylemin değerlendirmesini ve sağlayıcının kaydettiği durumlarda, eylemi gerçekleştiren kişiyi içeren sağlayıcı günlüğü;
4. Tünelin bağlantılarını, yapılandırmasını ve denetim günlüğünü barındıran Cloudflare uç noktaları;
5. imzalanmış toplayıcı beyanı;
6. raporun neleri ortaya koyduğu ve neleri ortaya koymadığı;
7. Bunu yeniden oluşturmak için komutlar ve kendisine verilen her dosyanın SHA-256'si.

Raporu, `report.json`, `deployment.json`, yayınlanmış yükleyiciyi ve kanıtları ZIP teslim edin. Raporu erken hazırlayın: sağlayıcı günlükleri sınırlı bir süre saklanır.

## Dış tanık olarak Cloudflare

Buradaki her şey isteğe bağlıdır. Cloudflare hesabı olmasa bile sunucu yine de çalışır ve bunlardan ikisi bugün şu anda çalışır durumda:

| Ne | Neleri gösterir? | TgWitness içinde |
| --- | --- | --- |
| Hızlı tünel veya kendi alan adınızın tüneli | Panele yalnızca tünel üzerinden erişilebilir | sunucu sihirbazı, yukarıya bakın |
| drand relay `drand.cloudflare.com` | drand turundan sonraki kayıtlar ondan daha yenidir: günlük, olaylar gerçekleşirken yazılmıştır | kanıt modu, **Daha fazla tanık**, hesap yok ([biçim](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Tünel durum bildirimleri | tünel kapalıyken, Cloudflare'den e-posta veya webhook yoluyla | Bunları Cloudflare kontrol panelinde ayarlayın |
| Gateway DNS (`--gateway-dns`, ya da sihirbazda **Cloudflare Gateway DNS**) | sunucunun aradığı her isim, Cloudflare tarafından TLS üzerinden yanıtlanır; Hetzner güvenlik duvarı, DNS'nin başka hiçbir yere erişmesine izin vermez; bir Ağ Geçidi politikasının yanıtları yeniden yazıp yazamayacağı | Hetzner, ücretsiz Zero Trust planı, alan adı yok; `verify` güvenlik duvarını, konumu, günlük kaydı, politikaları, sunucunun sorgularını ve denetim günlüğünü kontrol eder; kanıt modu, günlüğü dergiye kopyalar |
| Sunucudaki Cloudflare One istemcisiyle bağlantı sağlayan ağ geçidi; yalnızca Cloudflare'e izin veren bir giden trafik güvenlik duvarı | sunucunun kurduğu her bağlantı, sadece DNS değil | henüz oluşturulmadı |
| Panelin önünden erişim | panele kim ne zaman giriş yaptı | henüz geliştirilmemiştir: kendi alan adınız gereklidir |
| SSH komut günlüğü | hata ayıklama oturumundaki her komut | henüz oluşturulmadı |

Cloudflare'in kendi kopyasını R2'de tutan Logpush, bir Enterprise özelliğidir: ücretsiz planda Cloudflare yanıt verir `logpush is not enabled for this account`. Gateway günlüğü orada 24 saat kalır, bu nedenle kanıt modu onu imzalı günlüğe kopyalar (**Cloudflare Gateway’in bu sunucunun DNS sorgularının günlüğü**; Account Analytics Read ile okunur bir belirteç).

Zero Trust planı olmadan bir hesabın tek bir DNS konumu vardır. Cloudflare başka bir konumu reddettiğinde, sunucu mevcut konumu paylaşır ve sorguları adresine göre ayırt edilir; bu filtre ayrıca Zero Trust PII Read'e de ihtiyaç duyar ve `destroy` ortak bir konum bırakır. Bir günlük sorgusu en fazla üç saat sürer, bu nedenle kopyalama ve `verify` okuma işlemleri üç saatlik aralıklarla gerçekleştirilir.

Gateway DNS, sistem çözümleyicisini kapsar. 443 numaralı bağlantı noktası üzerinden HTTPS üzerinden başka bir çözümleyiciye yapılan DNS işlemleri ve hiçbir yerde aranmayan bir adrese (örneğin Telegram’ın veri merkezleri) yapılan bağlantılar, günlüğünde yer almaz.

Cloudflare, Telegram’ın şifrelemesinin içini, Telegram hesabındaki diğer cihazları (kanıt modundaki cihaz listesi bunları Telegram tarafında kaydeder) veya sağlayıcının hipervizörünü göremez.

## Dağıtım sonucunu okuma

For an ordinary VM, the provider controls the host infrastructure, and local inventory is checked alongside provider records. For Intel TDX, the verifier additionally checks the hardware quote, collector binding, compose and OS measurements. Read the individual results to see which checks passed or were unavailable.

Historical firewall detail depends on the provider; Linode retains rule versions. The [validation record](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) lists tested deployments and remaining live checks, and [verification scope](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) connects these environment checks to archive acquisition and integrity.
