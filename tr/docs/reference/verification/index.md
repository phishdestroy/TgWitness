# Neler test edildi

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/

Canlı Telegram testi, otomatik kontroller, tarayıcı kontrolleri ve henüz doğrulanmamış olan unsurlar.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | Sonuç | Kapsam |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | Kayıtlar | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| Kontrol et | Sonuç | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Canlı Phala Cloud dağıtımı · 4 Kasım 2026

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| Kurulum | Recorded value |
| --- | --- |
| Sağlayıcı | Phala Cloud · `tdx.small` · US-WEST-1 |
| Dağıtım | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

İlk iki dağıtımda, simüle edilmiş Phala Cloud'dan beş farklılık tespit edildi. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) artık her birini yeniden üretir ve düzeltme yapılmadığında hata verir:

| Phala Cloud'da | Düzeltme öncesinde | Düzeltme |
| --- | --- | --- |
| `compose_file.name` gereklidir | HTTP 422 hatası, hiçbir şey oluşturulmadı | Docker Compose yapılandırması, CVM adını içerir |
| Boş bir değer belirtilmedikçe, Phala ölçülen app-compose dosyasına kendi başlatma öncesi komut dosyasını ekler (v0.0.20: Docker oturum açma, `docker compose pull`, root şifresi, `user_config`'ten SSH anahtarları) | `tdx_compose` hatası: Yayınlanan Docker Compose yapılandırmasının dışında kod var | app-compose, `pre_launch_script` değerini `""` olarak ayarlar; Phala ise bunu dışarıda bırakır |
| `image` olmadan Phala, SSH erişimi etkin olan geliştirme sürümü olan `dstack-dev-0.5.12`’i seçer | `server_state` başarısız olur. Bu görüntüde yalnızca donanım doğrulama kaydı başarılı olmuştur; bunu yalnızca sağlayıcı kaydı ve `tdx_os` gösterir. | Dağıtım, Phala’nın mevcut sürümünün üretim derlemesini ister: `dstack-0.5.12` |
| dstack ağ geçidi kapalıyken, CVM ayrıntılarında hiçbir zaman `instance_id` | Dağıtım 30 dakika bekledikten sonra başarısız oluyor | Örnek kimliği, CVM durumundan okunur |
| Yeniden başlatma, durdurma ve başlatma işlemleri CVM işlemleridir, uygulama revizyonları değildir | `provider_actions`, yeniden başlatmaları listelemed | İşlemler okuma olarak da gerçekleştirilir |

**Deployment 3 · attestation, access checks and restart evidence**

- CVM, SSH erişimi kapalıyken `dstack-0.5.12`'i çalıştırdı. Toplayıcı, oluşturulduktan yaklaşık 1,5 dakika sonra imzalı adresini yayınladı. Dağıtım daha sonra `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, donanım doğrulama kaydı v4, FMSPC `20a06f000000`, hata ayıklama modunda değil, taşınamaz, Intel’den alınan kriptografik doğrulama verilerini destekleyen), `tdx_compose_hash`, `tdx_compose` (bayt bayt) ve `tdx_identity` (KMS anahtarları) komutlarını geçti.
- trycloudflare.com adresindeki panel, jeton olmadan veya yanlış bir jetonla 401 yanıtı verdi, jetonla ise 200 yanıtı verdi.
- `verify` ile `--source`, GitHub’ın commit arşivine ayarlandı ve parmak izi ayrı olarak geçti: sunucu, `server_state`, güvenlik duvarı (ağ geçidi yok, genel uç nokta yok), sağlayıcı günlüğü, beyan, parmak izi, kaynak hash, önyükleme ve beş `tdx_*` kontrolü başarıyla geçti. Cloudflare ve `tdx_os` kullanılamadığından sonuç "INCOMPLETE" (Eksik) olarak belirlendi.
- Phala'nın API'si aracılığıyla iki yeniden başlatma: her seferinde CVM, aynı toplayıcı anahtarı, yeni bir imzalı adres ve 530 yanıtı veren eski adresle iki dakikadan kısa sürede geri geldi. `verify`, yeni önyüklemeyi ve her iki yeniden başlatmayı da REVIEW olarak bildirdi. `--evidence` ile günlük imzaları ve üç başlatma işlemi doğrulandı; her birinin aynı CVM'den kendi Intel TDX donanım doğrulama kaydı vardı.
- `destroy` komutu yalnızca o CVM’yi kaldırdı. Ardından çalışma alanı boşaldı ve panel adresi yanıt vermez hale geldi.
- Panel sihirbazındaki fiyat kontrolünde `tdx.small` anahtarı için saat başına 0,058 $ gösterildi. Yanlış bir anahtar girildiğinde, "API anahtarı kabul edilmedi" şeklinde basit bir mesaj görüntülendi.

**Follow-up fixes · signed address discovery and OS measurements**

- Adres anahtarı olmadan, `verify`, adres konusundaki en yeni ve geçerli gönderiyi takip etti; bu gönderi, yayınlanan Docker Compose yapılandırmasında yer almaktadır. Sahte bir gönderi, onu var olmayan bir ana bilgisayara yönlendirdi ve `statement` başarısız oldu: bir sahteci, toplayıcı kılığına giremedi, ancak sahtecilik yoluyla üçüncü taraf doğrulamayı, sahte bir gelecek zaman damgası kullanarak 12 saate kadar engelleyebildi. Toplayıcı artık kendi anahtarıyla imzalanmış adresini de yayınlıyor; `verify`, yalnızca toplayıcı tarafından yapılan bu tür gönderileri kabul eder ve gönderiler ntfy.sh'nin alım zamanına göre sıralanır. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py), sahte gönderileri tekrar oynatır. Bir CVM, bunu yalnızca onu içeren bir commit'ten çalıştırır; dolayısıyla bu çalıştırmadaki toplayıcı adresini henüz imzalamamıştı ve `verify` bunu belirtti.
- `tdx_os`, `dstack-mr` olmadan çalışamıyordu; bu aracın mevcut sürümünde belgelerde belirtilen `measure --json` yerine `measure-os` bulunuyor. Doğrulayıcı artık MRTD ve RTMR0-2 değerlerini yayımlanan imajdan ve ACPI tabloları dahil sanal makine yapılandırmasından kendisi hesaplıyor.

**Deployment 4 · all 16 checks, report seals and restart verification**

- Dağıtım, yayınlanan `dstack-0.5.12`'i bir kez indirdi, bunu CVM'nin bildirdiği işletim sistemi görüntüsü hash'iyle eşleştirdi ve `tdx_os` başarılı oldu: MRTD, RTMR0, RTMR1 ve RTMR2, QEMU 8.2.2, 1 vCPU ve 2 GiB için hesaplanan değerlere eşitti. Aynı hesaplama, beyan edilen 4 GiB, 2 vCPU, QEMU 9.2.1 veya ikinci bir ağ kartı için farklı bir RTMR0 değeri verdi ve değiştirilmiş çekirdek, bellenim veya komut satırı ve geliştirme görüntüsü için başarısız oldu.
- `verify`, hızlı tünelin konektörü de dahil olmak üzere 16 kontrolün tamamını geçti, dolayısıyla sonuç PASS oldu. HTML ve PDF sertifikasını yazdı; bu belgeler, imzalar ve zaman damgalarıyla dijital olarak mühürlendi; zaman damgaları arasında Belçika hükümetinin zaman damgalama birimi TSU 202301’den alınan eIDAS onaylı bir zaman damgası (Belçika’nın güvenilir listesinde yer alan), bir FreeTSA zaman damgası ve doğrulayıcının imzası bulunuyordu; `check-report` bunların hepsini ve PDF’deki imzayı onayladı.
- Yeniden başlatmanın ardından, `verify --evidence` iki başlatma işlemini doğruladı; her biri CVM içinde oluşturulan bir donanım doğrulama belgesiyle birlikteydi ve her biri yayınlanan `dstack-0.5.12`'ten önyüklendi; yeniden başlatma ve yeni önyükleme işlemleri REVIEW statüsündeydi.
- `destroy`, çalışma alanını boş bıraktı.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- Toplayıcı, operatörün HMAC gönderisinin yanına kendi anahtarıyla imzalanmış adresini yayınladı. Ardından konuya iki sahte gönderi eklendi; biri sıfırlanmış HMAC'ye sahip, diğeri ise başka bir Ed25519 anahtarıyla imzalanmış ve her ikisi de 2096 yılına ait bir zamanı iddia ediyordu. `verify`, toplayıcı anahtarıyla imzalanmış adresi aldı ve 16 kontrolün tamamını geçti; mühür yine onaylı Belçika zaman damgasını, FreeTSA’nın zaman damgasını ve doğrulayıcının imzasını taşıyordu ve `check-report` bunları onayladı.
- Yeniden başlatmanın ardından toplayıcı, imzalanmış yeni adresi yayınladı: `verify` bunu hemen buldu; operatörün **Find mevcut adresi**, HMAC gönderisinden 27 saniye sonra buldu ve her ikisi de sahte gönderileri görmezden geldi. `verify --evidence`, `dstack-0.5.12`'ten başlatılan iki başlatmayı doğruladı.
- Dağıtım, Phala’nın CVM için faturalandırdığı tutarı (disk dahil) şu şekilde gösterdi: saat başına 0,06078 $.

### Panel wizard and remaining scope

Panel sihirbazı, Phala Cloud üzerinde iki kez çalıştırıldı; bir kez iş API'si aracılığıyla, bir kez de gerçek Chromium ile tarayıcı üzerinden: fiyat kontrolü, **Advanced** altında commit ile oluşturma, altı doğrulama kontrolünün tümü başarıyla geçti, faturalandırılan fiyatı (aylık 44,37 USD) gösteren sunucu listesi, **Find mevcut adresi bul,**, ölçülen Docker Compose yapılandırmasının indirilmesi ve silinmesi. Tarayıcıda herhangi bir sayfa hatası görülmedi. Her seferinde çalışma alanı sonrasında boştu.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Sayım |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Kontrol et | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

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

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
