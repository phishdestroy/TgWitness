# Neler test edildi

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/

Canlı Telegram testi, otomatik kontroller, tarayıcı kontrolleri ve henüz doğrulanmamış olan unsurlar.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Kanıt ve doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)

![Kanıt ve doğrulama](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**6 Kasım 2026 tarihinde güncellenmiştir.** Sonuçlar, her çalıştırma için kaydedilen revizyon, ortam ve iş yüküne bağlıdır. [Mevcut yetenekler,](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) kullanılabilir iş akışlarını açıklar; bu sayfa ise gerçekte nelerin kontrol edildiğini kaydeder.

[Performans grafikleri](https://phishdestroy.github.io/TgWitness/docs/validation/) · [İmzalı İngilizce denetim](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [İndirilebilir ölçümler](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| En son kanıtlar | Sonuç | Kapsam |
| --- | --- | --- |
| Sürüm denetimi · 6 Kasım | 1,461 çekirdek testleri geçildi; 37 platformu atlandı | Kaynak `92e539af40d8`; açık bulgular korunmuştur |
| Yeni dışa aktarmalar · 6 Kasım | 127.713 ve 141.781 kayıt/saniye, tam döngü | Sunucu başına iki hesap; metin ve meta veriler WARP üzerinden aktarılır |
| Saklanan arşivler · 6 Kasım | 48arşivleri; 3,598,381doğrulanmış kayıtlar | Mevcut arşivler, sabitlenmiş çalışma alanı anahtarlarıyla karşılaştırılarak kontrol edildi |
| Trusted Live · 5 Kasım | Korunan CPU kaydı ve WARP kontrolleri | Resmi Masaüstü oturum açma ve yerel dışa aktarma işlevleri hâlâ sınırlandırılmamıştır |
| Phala / Intel TDX · 4 Kasım | 16 doğrulayıcısının tüm kontrolleri sonraki çalıştırmalarda başarıyla geçilmiştir | Geçmişteki dağıtım; CVM'de Telegram hesabı bulunmamaktadır |

**Bu sayfada**

- [Sürüm denetimi ve yeni dışa aktarmalar · 6 Kasım 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Güvenilir Canlı CPU Ubuntu ve WARP · 5 Kasım 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Canlı Phala Cloud dağıtımı · 4 Kasım 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Canlı sunucu günlüğü envanteri · 1 Kasım 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Son çevrimdışı ve hata enjeksiyon kontrolleri · 1 Kasım 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Canlı Telegram testi, tüm hesap · 29 Ekim 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Parola korumalı dışa aktarım, libarchive ile açılır · 29 Ekim 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Canlı Telegram testi · 27–29 Ekim 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Sentetik yerel kapasite ölçümü](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Bir milyon mesajda tam metin arama · 5 Kasım 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Kalan nitelik](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#remaining-qualification)

## Sürüm denetimi ve yeni dışa aktarmalar · 6 Kasım 2026

Denetimde kaynak kodda v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, sürüm `92e539af40d8-83e41104669e` kullanılmıştır. Yüklü paketlerin hızlı testleri üç sunucuda başarılı olmuştur. İmzalı rapor, o anda gözlemlenen durumu yansıtmaktadır.

[![İki yeni iş yükü için veri toplama ve tam dışa aktarma oranları](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| İş yükü | Kayıtlar | Edinme | Tam döngü | Tam döngü oranı |
| --- | --- | --- | --- | --- |
| Sunucu A · iki hesap | 27,030 | 189.043'lar | 211.647'lar | 127.713 kayıt/saniye |
| Sunucu B · iki hesap | 29,299 | 182.513'lar | 206.650'lar | 141.781 kayıt/saniye |

Her iki dışa aktarım da devam ettirme özelliği olmadan başlatıldı, ekler ve avatarlar hariç tutuldu ve hiçbir yinelenen veya yeniden kullanılan kayıt olmadan sona erdi. Tam döngü, hazırlık, toplama, seçme, paketleme ve arşiv doğrulamasını içerir. Sunucu A ayrıca bir korumalı sohbet okuma kontrolü de gerçekleştirdi. A’da dört, B’de üç FloodWait olayı dikkate alındı. Bu gözlemler genel bir verim garantisi oluşturmaz.

| Kontrol et | Sonuç | Nitelikler |
| --- | --- | --- |
| Temel pytest | 1,461'dan geçti | 37 platform atlamaları |
| Tarayıcı / tarayıcı kullanıcı deneyimi / kanıt / site | 102 / 66 / 15 / 9 başarılı | Bu programlar diğer testlerle çakışmaktadır; sayılar birbirine eklenemez |
| Capture eklentisi | 124'dan geçti | Gerekli Chromium sanal ortamı tarafından engellenen üç Resmi Web denetimi |
| API yetkilendirme | 269'a yönlendirilenler; 538 istekleri kabul edildi | Eksik kimlik bilgileri ve iptal edilmiş erişim |
| Saklanan arşivler | 48'nin 48'i doğrulandı | 3,598,381 kayıtları; sabitlenmiş çalışma alanı anahtarları |
| Canlı filo okuma kontrolleri | 40 profillerinden 24'u geçti | 16 WARP rotaları yeterlilik testini geçemedi; bu profiller bağlanamadı |

[imzalı rapor](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md), denetlenen ana sürümde yer almayan, yayınlanmamış bir gizli sohbet anlık görüntüsündeki üç kusur da dahil olmak üzere tüm açık bulguları kaydeder. Daha önceki [kamuya açık geçmiş değerlendirmesi](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md), farklı bir revizyon ve iş yükü kullanmıştır; bu değerlendirmenin oranları bu karşılaştırma ile birleştirilmemelidir.

[sabitlenmiş anahtarı ve](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files) doğrulayıcısını kullanarak orijinal raporu doğrulayın. İmzası, operatörün raporunu tahrifata karşı korur. Bu, bağımsız bir tasdik, Telegram'da yazarlık kanıtı veya GDPR sertifikası değildir.

## Güvenilir Canlı CPU Ubuntu ve WARP · 5 Kasım 2026

Korunan entegrasyon çalıştırması, bir RunPod CPU ana bilgisayarı içindeki QEMU altında, yalnızca CPU kullanan bir Ubuntu 24.04.5 konuk sistemi (4 vCPU, 8 GiB) kullandı. Toplayıcı `14e642a5`'ü, doğrulama ise `02072461`'ü kullandı. Nihai düzeltmeler, [PR #114](https://github.com/phishdestroy/TgWitness/pull/114)'de `755f78f6` olarak birleştirildi; bu PR'nin ağacı, test edilen PR başlığıyla eşleşti. Bu bir TEE değildi.

- Gerçek bir WARP Connector'ın durumu sağlıklı olarak bildirildi; proxy üzerinden HTTPS, WARP ve Gateway'in etkin olduğunu bildirdi. Üç sonda aynı çıkış adresini gördü; bu, sabit IP garantisi anlamına gelmez.
- WARP bağlantısının kesilmesi, proxy üzerinden yapılan isteğin başarısız olmasına neden oldu. Doğrudan ağ geçidi hizmeti HTTPS isteği reddedildi. Kaydedici ad alanında, doğrudan IPv4/IPv6, harici DNS ve Docker'ın gömülü UDP çözümleyicisi engellendi.
- Kapsamlı, salt okunur bir sağlayıcı belirteci, durum/bağlantı bilgilerini okuyabilirdi ancak bağlayıcı kayıt belirtecini okuyamazdı. İmzalı sağlayıcı gözlemleri, açıkça kullanılamayan örnekleri içeriyordu. Tanık, operatörün ana bilgisayarında çalışıyordu; bu nedenle bu durum, bağımsız bir üçüncü tarafın saklama hizmetini değil, kayıt ve saklama işlemlerini göstermektedir.
- Official Desktop, kimlik doğrulaması yapılmamış karşılama ekranına ulaştı. Korumalı klavye girişi, yakalama sırasında reddedildi. Üç H.264 ekran segmenti kod çözüldü ve saat katmanları incelendi. 18 olayı ön kontrol arşivi, sabitlenmiş kayıt anahtarı ve saklanan kontrol noktası ile karşılaştırılarak doğrulandı.
- Son yakalama testleri, Windows ve Linux CI ortamlarında gerçek Chromium/FFmpeg kullanılarak 114 vakalarını başarıyla geçti. Beş temel test ve bağımlılık danışma kontrolü başarıyla tamamlandı.

İlk 2 vCPU/4 GiB başlatma işlemi, eşzamanlı görüntü oluşturma yükü altında zaman aşımına uğradı ve koruma mekanizması tarafından durduruldu; bu, başarılı sayılmaz. Manuel test hesabı girişi, yerel sohbet dışa aktarımı, gerçek hibrit karşılaştırma ve Telegram tarafında çıkış işlemleri hala beklemede. Sağlanan hiçbir Telethon oturumu içe aktarılmadı. Ekler, otomatik OCR, yerel drand BLS doğrulaması ve Trusted Live TDX tasdiki geçerli bulunmadı.

## Canlı Phala Cloud dağıtımı · 4 Kasım 2026

**Geçmiş sonuç:** sonraki dağıtımlar, Intel TDX ve hızlı tünel dahil olmak üzere tüm 16 doğrulayıcı kontrollerinden geçti. Kanıtın yeniden başlatılması, imzalı adres keşfi ve rapor zaman damgaları ayrı ayrı kontrol edildi. Her test CVM'si, çalıştırıldıktan sonra kaldırıldı.

| Kurulum | Kaydedilen değer |
| --- | --- |
| Sağlayıcı | Phala Cloud · `tdx.small` · US-WEST-1 |
| Dağıtım | `--provider phala --quick-tunnel`; başlangıçta boş çalışma alanı |
| İlk toplayıcı | `df7d860c` · v0.8.1 |
| Tüm düzeltmelerin bulunduğu toplayıcı | `53a0f7e9` |
| Üretim konuğu | `dstack-0.5.12`; SSH erişimi devre dışı |
| Harici hizmetler | ntfy.sh, GitHub ve Intel PCS |
| Gözlemlenen maliyet | Yedi CVM, toplamda yaklaşık 1.9 ABD senti; geçmiş test fiyatları |

Aşağıdaki sıralama, ilk hataları, düzeltmeleri ve tamamlanan kontrolleri birbirinden ayırmaktadır. Bu CVM'lere hiçbir Telegram hesabı bağlanmamıştır.

**1–2 dağıtımları · sağlayıcı farklılıkları ve regresyon kontrolleri**

İlk iki dağıtımda, simüle edilmiş Phala Cloud'dan beş farklılık tespit edildi. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) artık her birini yeniden üretir ve düzeltme yapılmadığında hata verir:

| Phala Cloud'da | Düzeltme öncesinde | Düzeltme |
| --- | --- | --- |
| `compose_file.name` gereklidir | HTTP 422 hatası, hiçbir şey oluşturulmadı | Docker Compose yapılandırması, CVM adını içerir |
| Boş bir değer belirtilmedikçe, Phala ölçülen app-compose dosyasına kendi başlatma öncesi komut dosyasını ekler (v0.0.20: Docker oturum açma, `docker compose pull`, root şifresi, `user_config`'ten SSH anahtarları) | `tdx_compose` hatası: Yayınlanan Docker Compose yapılandırmasının dışında kod var | app-compose, `pre_launch_script` değerini `""` olarak ayarlar; Phala ise bunu dışarıda bırakır |
| `image` olmadan Phala, SSH erişimi etkin olan geliştirme sürümü olan `dstack-dev-0.5.12`’i seçer | `server_state` başarısız olur. Bu görüntüde yalnızca donanım doğrulama kaydı başarılı olmuştur; bunu yalnızca sağlayıcı kaydı ve `tdx_os` gösterir. | Dağıtım, Phala’nın mevcut sürümünün üretim derlemesini ister: `dstack-0.5.12` |
| dstack ağ geçidi kapalıyken, CVM ayrıntılarında hiçbir zaman `instance_id` | Dağıtım 30 dakika bekledikten sonra başarısız oluyor | Örnek kimliği, CVM durumundan okunur |
| Yeniden başlatma, durdurma ve başlatma işlemleri CVM işlemleridir, uygulama revizyonları değildir | `provider_actions`, yeniden başlatmaları listelemed | İşlemler okuma olarak da gerçekleştirilir |

**3 Dağıtımı · doğrulama, erişim kontrolleri ve yeniden başlatma kanıtları**

- CVM, SSH erişimi kapalıyken `dstack-0.5.12`'i çalıştırdı. Toplayıcı, oluşturulduktan yaklaşık 1,5 dakika sonra imzalı adresini yayınladı. Dağıtım daha sonra `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, donanım doğrulama kaydı v4, FMSPC `20a06f000000`, hata ayıklama modunda değil, taşınamaz, Intel’den alınan kriptografik doğrulama verilerini destekleyen), `tdx_compose_hash`, `tdx_compose` (bayt bayt) ve `tdx_identity` (KMS anahtarları) komutlarını geçti.
- trycloudflare.com adresindeki panel, jeton olmadan veya yanlış bir jetonla 401 yanıtı verdi, jetonla ise 200 yanıtı verdi.
- `verify` ile `--source`, GitHub’ın commit arşivine ayarlandı ve parmak izi ayrı olarak geçti: sunucu, `server_state`, güvenlik duvarı (ağ geçidi yok, genel uç nokta yok), sağlayıcı günlüğü, beyan, parmak izi, kaynak hash, önyükleme ve beş `tdx_*` kontrolü başarıyla geçti. Cloudflare ve `tdx_os` kullanılamadığından sonuç "INCOMPLETE" (Eksik) olarak belirlendi.
- Phala'nın API'si aracılığıyla iki yeniden başlatma: her seferinde CVM, aynı toplayıcı anahtarı, yeni bir imzalı adres ve 530 yanıtı veren eski adresle iki dakikadan kısa sürede geri geldi. `verify`, yeni önyüklemeyi ve her iki yeniden başlatmayı da REVIEW olarak bildirdi. `--evidence` ile günlük imzaları ve üç başlatma işlemi doğrulandı; her birinin aynı CVM'den kendi Intel TDX donanım doğrulama kaydı vardı.
- `destroy` komutu yalnızca o CVM’yi kaldırdı. Ardından çalışma alanı boşaldı ve panel adresi yanıt vermez hale geldi.
- Panel sihirbazındaki fiyat kontrolünde `tdx.small` anahtarı için saat başına 0,058 $ gösterildi. Yanlış bir anahtar girildiğinde, "API anahtarı kabul edilmedi" şeklinde basit bir mesaj görüntülendi.

**Sonraki düzeltmeler · imzalı adres keşfi ve işletim sistemi ölçümleri**

- Adres anahtarı olmadan, `verify`, adres konusundaki en yeni ve geçerli gönderiyi takip etti; bu gönderi, yayınlanan Docker Compose yapılandırmasında yer almaktadır. Sahte bir gönderi, onu var olmayan bir ana bilgisayara yönlendirdi ve `statement` başarısız oldu: bir sahteci, toplayıcı kılığına giremedi, ancak sahtecilik yoluyla üçüncü taraf doğrulamayı, sahte bir gelecek zaman damgası kullanarak 12 saate kadar engelleyebildi. Toplayıcı artık kendi anahtarıyla imzalanmış adresini de yayınlıyor; `verify`, yalnızca toplayıcı tarafından yapılan bu tür gönderileri kabul eder ve gönderiler ntfy.sh'nin alım zamanına göre sıralanır. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py), sahte gönderileri tekrar oynatır. Bir CVM, bunu yalnızca onu içeren bir commit'ten çalıştırır; dolayısıyla bu çalıştırmadaki toplayıcı adresini henüz imzalamamıştı ve `verify` bunu belirtti.
- `tdx_os`, `dstack-mr` olmadan çalışamıyordu; bu aracın mevcut sürümünde belgelerde belirtilen `measure --json` yerine `measure-os` bulunuyor. Doğrulayıcı artık MRTD ve RTMR0-2 değerlerini yayımlanan imajdan ve ACPI tabloları dahil sanal makine yapılandırmasından kendisi hesaplıyor.

**4 dağıtımı · tüm 16 kontrolleri, rapor mühürleri ve yeniden başlatma doğrulaması**

- Dağıtım, yayınlanan `dstack-0.5.12`'i bir kez indirdi, bunu CVM'nin bildirdiği işletim sistemi görüntüsü hash'iyle eşleştirdi ve `tdx_os` başarılı oldu: MRTD, RTMR0, RTMR1 ve RTMR2, QEMU 8.2.2, 1 vCPU ve 2 GiB için hesaplanan değerlere eşitti. Aynı hesaplama, beyan edilen 4 GiB, 2 vCPU, QEMU 9.2.1 veya ikinci bir ağ kartı için farklı bir RTMR0 değeri verdi ve değiştirilmiş çekirdek, bellenim veya komut satırı ve geliştirme görüntüsü için başarısız oldu.
- `verify`, hızlı tünelin konektörü de dahil olmak üzere 16 kontrolün tamamını geçti, dolayısıyla sonuç PASS oldu. HTML ve PDF sertifikasını yazdı; bu belgeler, imzalar ve zaman damgalarıyla dijital olarak mühürlendi; zaman damgaları arasında Belçika hükümetinin zaman damgalama birimi TSU 202301’den alınan eIDAS onaylı bir zaman damgası (Belçika’nın güvenilir listesinde yer alan), bir FreeTSA zaman damgası ve doğrulayıcının imzası bulunuyordu; `check-report` bunların hepsini ve PDF’deki imzayı onayladı.
- Yeniden başlatmanın ardından, `verify --evidence` iki başlatma işlemini doğruladı; her biri CVM içinde oluşturulan bir donanım doğrulama belgesiyle birlikteydi ve her biri yayınlanan `dstack-0.5.12`'ten önyüklendi; yeniden başlatma ve yeni önyükleme işlemleri REVIEW statüsündeydi.
- `destroy`, çalışma alanını boş bıraktı.

**5 Dağıtımı · toplayıcı tarafından imzalanmış keşif ve sahte gönderi reddi**

Toplayıcı, yukarıdaki düzeltmeleri içeren `53a0f7e9` commit'inden itibaren çalıştırıldı.

- Toplayıcı, operatörün HMAC gönderisinin yanına kendi anahtarıyla imzalanmış adresini yayınladı. Ardından konuya iki sahte gönderi eklendi; biri sıfırlanmış HMAC'ye sahip, diğeri ise başka bir Ed25519 anahtarıyla imzalanmış ve her ikisi de 2096 yılına ait bir zamanı iddia ediyordu. `verify`, toplayıcı anahtarıyla imzalanmış adresi aldı ve 16 kontrolün tamamını geçti; mühür yine onaylı Belçika zaman damgasını, FreeTSA’nın zaman damgasını ve doğrulayıcının imzasını taşıyordu ve `check-report` bunları onayladı.
- Yeniden başlatmanın ardından toplayıcı, imzalanmış yeni adresi yayınladı: `verify` bunu hemen buldu; operatörün **Find mevcut adresi**, HMAC gönderisinden 27 saniye sonra buldu ve her ikisi de sahte gönderileri görmezden geldi. `verify --evidence`, `dstack-0.5.12`'ten başlatılan iki başlatmayı doğruladı.
- Dağıtım, Phala’nın CVM için faturalandırdığı tutarı (disk dahil) şu şekilde gösterdi: saat başına 0,06078 $.

### Panel sihirbazı ve kalan kapsam

Panel sihirbazı, Phala Cloud üzerinde iki kez çalıştırıldı; bir kez iş API'si aracılığıyla, bir kez de gerçek Chromium ile tarayıcı üzerinden: fiyat kontrolü, **Advanced** altında commit ile oluşturma, altı doğrulama kontrolünün tümü başarıyla geçti, faturalandırılan fiyatı (aylık 44,37 USD) gösteren sunucu listesi, **Find mevcut adresi bul,**, ölçülen Docker Compose yapılandırmasının indirilmesi ve silinmesi. Tarayıcıda herhangi bir sayfa hatası görülmedi. Her seferinde çalışma alanı sonrasında boştu.

Kapsam dışı olanlar: Phala üzerindeki bir Cloudflare etki alanı, CVM üzerindeki bir Telegram hesabı ve `dstack-0.6.1` görüntüsü. Sihirbazın oluşturma öncesi fiyatı yalnızca Phala’nın hesaplama fiyatıdır, zira API’si disk fiyatını yalnızca mevcut bir CVM için belirtir; sunucu listesi ise oluşturma sonrası faturalandırılan fiyatı gösterir. Bu bölümdeki tüm fiyatlar 4 Kasım 2026 tarihinde gözlemlenmiştir.

## Canlı sunucu günlüğü envanteri · 1 Kasım 2026

Yaklaşık 19:15 UTC'de, sıralı salt okunur SQLite `query_only` sorguları, çalışır durumdaki bir sunucudaki on çalışma alanı veritabanındaki olayları saydı. Sorgular sırasında veri toplama devam etti, dolayısıyla bu, çalışma alanları genelinde atomik bir anlık görüntü değildir.

| On çalışma alanı veritabanında gözlemlenmiştir | Sayım |
| --- | --- |
| En az bir `message.new` olayı içeren çalışma alanları | 8 |
| Operasyonel olayları da içeren günlük kayıtları | 1,610,818 |
| `message.new` olayları | 900,232 |
| `message.edited` olayları | 80,683 |
| `message.deleted` olayları | 400,536 |
| `message.recovered` olayları | 53,403 |
| `message.snapshot` olayları | 2,183 |
| `media.saved` olayları | 50,418 |
| `media.failed` olayları | 5,575 |
| `coverage.gap` olayları | 11 |
| WAL dosyaları ve medya hariç veritabanı baytları | 7,909,003,264 |

Bunlar **olay sayıları**, benzersiz mesajlar, kişiler veya medya dosyaları değil. Aynı mesaj birden fazla çalışma alanında görünebilir ve bir düzenleme veya silme işlemi başka bir günlük olayı oluşturabilir. `media.failed` geçmişteki hata olaylarını sayar, mevcut medya kuyruğunu değil. Sorgular **değil** imzaları ve tüm kayıtların tam hash zincirini yeniden doğrulamadı 1,610,818 kayıtları, teslimatı veya verimi ölçmemiştir ya da her Telegram olayının kaydedildiğini doğrulamamıştır. Burada hiçbir mesaj içeriği, hesap veya sohbet kimliği, çalışma alanı etiketi, kimlik bilgileri veya özel dosya yayınlanmamaktadır.

Bu inceleme sırasında, ayrı olarak yapılandırılmış genel izleme aracı üç kaynağı kapsıyordu: bir yakalama yanıtı OK idi ve ikisi `no_response` bildirdi. Bu izleme aracı, on çalışma alanını kapsayan bir durum özeti değildir. `no_response`, gözlemcinin o kontrolde yanıt alamadığı anlamına gelir; mesaj kaybı olduğu anlamına gelmez. Aşağıdaki daha küçük 29 Ekim testi, kendi açık imzası ve hash zinciri doğrulamasına sahiptir.

## Son çevrimdışı ve hata enjeksiyon kontrolleri · 1 Kasım 2026

Bu kontroller kurgusal veriler ve yerel dosyalar kullanır; bunlar, başka bir canlı Telegram teslim ölçümü için değil, mevcut kaynak için regresyon kanıtı sağlar:

| Kontrol et | Ne üzerinde test edildi |
| --- | --- |
| [Kaynak arşivi](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Kaynak baytları aynı ancak dosya zaman damgaları değiştirilmiş iki derleme, aynı ZIP dosyasını ve sağlama toplamını üretti. Arşivlenmiş baytlar ve dosya hash değerleri tam olarak eşleşti; özel test dosyaları arşivin dışında kaldı. Simüle edilmiş bir yazma hatası, önceki arşivi ve sağlama toplamını bozulmadan bıraktı. |
| [Hesap dışa aktarma kurtarma](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | İkinci ZIP üyesinde simüle edilen bir disk hatası, yayınlanmış veya kısmi bir ZIP dosyası bırakmadı. Devam ettirme işlemi, her imzalı makbuzu bayt düzeyinde aynı tuttu, beklenen imza parmak izini kullanarak bağımsız olarak doğrulanabilir bir arşiv oluşturdu ve sentetik kapsama boşluğunu kısmi bir sonuç olarak korudu. Ölçek iddiaları, geçmişler büyüdükçe görevlerin ve makbuzların tekrar tekrar taranmasını önler. |
| [Gizlilik için en aza indirgenmiş bilgi paylaşımı](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Sentetik Unicode adları ve takma adlar, iç içe geçmiş meta veriler, bilinmeyen gönderenler ve medya alanları, üç kimlik modunun tamamında ve metin eksikliği durumlarında kontrol edildi. Maskeleme sınırı hatası, redaksiyonu sessizce zayıflatmadı; orijinal imzalı hesap dışa aktarımı değişmeden kaldı. |
| [Linux medya kod çözücü ve OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | `5a9e0814` numaralı commit’te gerçekleştirilen bir [Linux Docker CI kontrolü,](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) oluşturulan Ogg/Opus, MP3, M4A, videolu MP4, WAV ve FLAC girdilerini; sahte süre ve ikincil dosya referansı kontrollerini; ve 48 adet değiştirilmiş ayrıştırıcı fikstürünü (34’ü reddedildi, 14’ü sınırlar içinde kod çözüldü) başarıyla geçti. Gerçek Tesseract OCR, orijinal baytlar değiştirilmeden çalıştırıldı. Kod çözücü ve OCR, Whisper modeli olmadan ağdan izole edilmiş kapsayıcılarda çalıştırıldı. |

Kontroller, [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) ve [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) iş akışlarında çalıştırılır. Bu kontroller, olası her türlü depolama hatasını veya bir ifşanın yayınlanmasının otomatik olarak güvenli olup olmadığını değil, bu hata sınırlarını test eder. Medya kontrolü, konuşma tanıma doğruluğunu veya Telegram teslimatını ölçmez. Paylaşmadan önce her bir türev dosyayı inceleyin.

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

## Bir milyon mesajda tam metin arama · 5 Kasım 2026

Komut: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

200 sohbetteki 1.000.000 sentetik mesajdan oluşan deterministik imzalı bir günlük (Rusça kelime biçimleri, Ukraynaca, İngilizce, Çince, Japonca, bağlantılar ve kullanıcı adları) 71 saniyede indekslendi; indeks, 1,50 GiB'lik günlüğün yanı sıra 58 MiB yer kapladı. En iyi eşleşme arama işlemleri 9 ila 190 ms (medyan) sürdü; önceki alt dize aramasında ise bu süre 2,4 ila 3,2 saniyeydi. Tam sonuçlar, donanım ve sınırlar: [Tam metin arama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/search/#benchmark). `tools/test_fulltext.py` ayrıca, tam metin araması öncesinde oluşturulmuş imzalı bir arşivi (`tools/fixtures/evidence-before-fulltext.zip`) ile mevcut doğrulayıcıyı ve o arşivin kendi doğrulayıcısını kullanarak mevcut bir arşivi `verify.py`.

## Kalan nitelikler

Saklanan canlı günlük, gerçek toplama işlemlerini, düzenlemeleri, silme bildirimlerini, ekleri, yeniden kontrolleri ve hız sınırlaması yönetimini kaydeder. Bu günlük, kapsamlı teslimat bilgilerini veya rol görünürlüğü, tepki veren aktörler, uzatılmış FloodWait, hesap yasaklamaları ve ağ/işlem kesintisi kurtarma işlemlerini içeren kontrollü bir matris kaydetmez. QR jetonu düzenleme işlemi, tamamlanmış mobil QR onayı işleminden ayrıdır.

Docker/Compose ve kurulum kontrolleri CI'da kaydedilir; gerçek Phala dağıtımı ve harici zaman damgası doğrulaması yukarıda açıklanmıştır. Bunlar, sürekli yüksek yük, eksiksiz bir canlı platform/rol matrisi, bağımsız güvenlik incelemesi, uzun vadeli arşivleme doğrulaması veya adli sertifikasyon sağlamaz. Kaydedilmiş MTProto durumu ve yakalama işlevi uygulanmaktadır; atomik kayıpsız canlı yeniden oynatma henüz sağlanmamıştır. Daha yeni olan backfill, mesajları ve imleçleri atomik olarak kaydetmekte ve mevcut Son Eylemleri korumaktadır, ancak sentetik kapsamı canlı yeterlilikten farklıdır. Kontrollü yeterlilik matrisi için bkz. [canlı kabul](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).

[kamuya açık denetim dizini](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) yalnızca imzalanmış raporu ve toplu ölçümleri içerir. Ayrıntılı işlem makbuzları, ham yakalamalar ve hesap materyalleri gizli kalır. `docs/assets/`'deki uygulama ekran görüntüleri kurgusal tanıtım verilerini kullanır.
