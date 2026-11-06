# Telegram · Kanıt formatı

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/

İmzalı ZIP dosyasının içeriği, kayıt türleri, işlem makbuzları, kullanıcı profilleri, site dışı kopyalar ve çevrimdışı doğrulama.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Kanıt ve doğrulama](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

TgWitness, hesapta görülebilen Telegram gözlemlerini imzalı bir günlükte saklar. Alıcılar, kaydedilen kayıtları, ekleri ve raporları güvenilir bir toplayıcı anahtarıyla doğrulayabilir, ardından günlüğü bağımsız olarak saklanan bir kontrol noktasıyla karşılaştırabilir. Bu sayfada, devir için saklanması gereken formatlar, kontroller ve materyaller açıklanmaktadır.

Kullanıcılar, Windows'ta **VERIFY.cmd** ile başlayabilir: program, orijinal ZIP dosyasını ve bağımsız olarak elde edilmiş anahtar parmak izini ister, açıklayıcı bir sonuç gösterir ve ayrı bir doğrulama transkriptini kaydeder. Kurulum ve güven sınırları için [doğrulama başlatıcılarına ve taşınabilir çalışma zamanı](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md)'e bakınız.

**Bu sayfada**

- [Neyin imzalandığı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#what-is-signed)
- [Sohbet dışa aktarımlarının karşılaştırılması](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#comparing-chat-exports)
- [Soruşturma devri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#investigation-handoff)
- [Devir teslim özeti](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#handover-extract)
- [Okunabilir raporlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#readable-reports)
- [Olay kanonikleştirme](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#event-canonicalization)
- [Aktör semantiği](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#actor-semantics)
- [Kapsam: süreklilik, boşluklar ve gözlemlenmemiş kimlikler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)
- [Üretici](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#producer)
- [Kişi profilleri](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#people-profiles)
- [Bağımsız tanık](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#independent-witness)
- [Manifest ve kontrol noktaları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#manifest-and-checkpoints)
- [Doğrulama kapsamı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope)
- [Ekler](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#attachments)
- [Dayanıklı toplama ve işlem makbuzları (0.2)](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#durable-collection-and-process-receipts-02)
- [RFC 3161 hazırlığı ve yanıt doğrulaması (0.2)](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)
- [Kanıt modunda isteğe bağlı kayıtlar: drand ve Telegram cihazları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)

## Neler imzalanır?

| Materyal | Koruma | Neler saklanmalı |
| --- | --- | --- |
| Operasyonel olaylar dahil olmak üzere her günlük kaydı | Her olay için bir SHA-256 zinciri ve bir Ed25519 imzası | Orijinal `events.jsonl`, güvenilir anahtar parmak izi ve saklanan kontrol noktası |
| Kanıt ZIP dosyasının içeriği | `manifest.sig`, içerik dosyalarının hash değerlerini listeleyen kanonik manifestoyu imzalar | Manifestosu ve imzası dahil olmak üzere eksiksiz ZIP dosyası |
| Ekler korunur | İmzalı bir `media.saved` olayındaki SHA-256 ve bayt sayısı; imzalı ZIP manifestosundaki dosya hash değeri | Doğrulanmış ZIP dosyasının içindeki orijinal baytlar |
| Kontrol Noktası | Günlük uzunluğu, başlık hash değeri, açık anahtar ve oluşturulma zamanı üzerinde Ed25519 imzası | Tartışmalı bir değişiklikten önce saklanan bağımsız bir kopya |
| Çalıştırma makbuzu | Toplayıcı sürümü, kaynak dosya hash değerleri ve başlangıç ayarlarının imzalı kaydı; bu bilgiler `process.started` dosyasına da dahil edilmiştir. | Seçilen doğrulama modu için makbuz, ilgili günlük kaydı ve ortam kanıtları |
| Okunabilir raporlar: `report.html` ve bileşenleri, `report.json`, `report.pdf`, `chat.pdf` | Her dosyanın içeriği üzerinde bir Ed25519 mührü bulunur; PDF ayrıca standart bir PDF imzası da taşır (bkz. [Okunabilir raporlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#readable-reports)) | Alınan dosya ve güvenilir anahtar parmak izi; belgede açıklanan ZIP dosyası |
| Bağımsız CSV | Tek başına kriptografik imza yoktur; olay hash'leri tek başına yetersizdir | Bütünlük kontrolü için doğrulanmış ZIP dosyasının içindeki metni aynen kullanın |
| Tarayıcı tarafından oluşturulan ekran görüntüleri, çıktılar veya PDF dosyaları | Türetilmiş sürümde TgWitness imzası bulunmamaktadır. | Orijinal doğrulanmış paketi saklayın ve türev sürümün nasıl oluşturulduğunu belgelendirin |

Toplayıcı, her dışa aktarım formatını oluşturmadan önce günlük imzalarını doğrular. Okunabilir HTML ve PDF raporları kendi mühürlerini taşır; bağımsız CSV dosyası, imzalı bir ZIP dosyasının parçası olarak kontrol edilir. Ek baytlarını ve manifestosunu korumak için ZIP dosyasını koruyun ve günlüğü önceki bir sınırla karşılaştırmak için ayrı bir kontrol noktası oluşturun.

## Sohbet dışa aktarımlarının karşılaştırılması

İmzalanmış iki sohbet dışa aktarım ZIP dosyasını, bağımsız olarak saklanan imzalayıcı parmak izleriyle doğrulayın ve karşılaştırın:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

Her iki arşiv de aynı sayısal hesap ve sohbet kimliklerini kaydettiğinde, kayıtlar mesaj kimliğine göre eşleştirilir. **Değişmemiş**, kaydedilen tam JSON kaydının eşitliği anlamına gelir: tam metin, yazar, tarihler, yanıt hedefi, iç içe geçmiş meta veriler ve bilinmeyen alanların tümü dahildir. JSON nesnesindeki anahtar sırası önemli değildir; eksik alanlar, null değerler, değer türleri ve dizi sırası önemlidir. 300 karakterlik önizleme yalnızca görüntüleme amaçlıdır. Değiştirilen girdiler, önizlemede görünmeyen değişiklikler de dahil olmak üzere, farklılık gösteren üst düzey `changed_fields`'yi belirtir. Eşleştirme sırasında, yinelenen mesaj kimlikleri birbirlerinin üzerine yazılmak yerine reddedilir.

Bir fark, değiştirilmiş bir görüntüleme adı, görüntüleme sayısı, koleksiyon açıklaması veya diğer gözlem meta verileri olabilir. Bu, tek başına bir Telegram düzenlemesini kanıtlamaz, değişikliği kimin yaptığını belirlemez veya çelişen arşivlerden hangisinin doğru olduğunu kanıtlamaz. Ayrıştırılmamış kayıtlar karşılaştırmada kalır; kaydedilmiş temsil biçimlerinin eşit olması, Telegram verilerinin kodunun çözüldüğü anlamına gelmez.

Farklı veya eksik hesap/sohbet kimlikleri için araç, yalnızca gönderen, tam metin, dosya hash değeri, medya türü ve beş saniyelik zaman toleransı kullanarak olası eşleşmeleri bulur. **Değişmemiş** yerine **Eşleşen** raporlar. Bu adaylar, mesaj kimliğini veya tüm meta verilerin eşitliğini kanıtlamaz. Ayrıştırılmamış kayıtlar eşleşmemiş olarak kalır. Eşleştirilmiş kayıtlardaki farklılıklar, içerik modunda da dahil olmak üzere `changed`'te listelenmeye devam eder; bu farklılıklar, aynı mesajın düzenlendiğini kanıtlamaz. `--json` ile birlikte, `matched` çiftleri sayar ve `unchanged`, kaydedilmiş tam kayıtları eşit olan çiftleri sayar. Hiçbir sayım, içerik modunda mesaj kimliğini kanıtlamaz. Mevcut `changed_fields` ve tamsayı `unchanged` çıktıları, önceki karşılaştırma sonuçlarıyla uyumlu kalır. Arşiv biçimi ve imza doğrulaması değişmemiştir.

## Soruşturma devri

1. Vaka referansını, operatörü, sayısal Telegram hesap kimliğini, seçilen kaynakları, toplama politikasını ve toplama süresini vaka notlarınıza kaydedin. TgWitness, gözlemleri korur ve [Case Board](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-board/)'da kaynağa bağlı notları ve koleksiyonları destekler. Aktarım ve muhafaza kayıtlarını vaka materyallerinizle birlikte saklayın. [Canlı kabul](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)prosedürüyle planlanan toplama ayarlarını kontrol edin.
2. Çıkartmalara güvenmeden önce çalışma alanının açık anahtar parmak izini bağımsız olarak saklayın. Toplama işlemi sırasında imzalı kontrol noktalarını toplayıcı dışında kaydedin. Kesintileri ve hesabın görünürlük sınırlarını kaydedin.
3. **İmzalı** bir **ZIP dosyası** dışa aktarın ve imzalı çalıştırma makbuzunu saklayın. Dışa aktarılan günlük sınırında veya öncesinde bir kontrol noktası kullanın. Daha sonraki bir kontrol noktası, daha önceki bir dışa aktarmayı çok kısa olduğu gerekçesiyle doğru bir şekilde reddedebilir. Dışa aktarmalar, panel filtrelerinden bağımsız olarak tam çalışma alanı günlüğünü içerir; paylaşmadan önce materyali gözden geçirin.
4. Alıcının, ZIP dosyasını güvenilir bir doğrulayıcı kopyası ve bağımsız olarak sağlanan parmak izi/kontrol noktası ile doğrulamasını sağlayın. Python ortamı etkin olan güvenilir bir çalışma ortamından:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Her iki girdi de sağlandığında ve kabul edildiğinde, başarılı çıktı raporları `key_pinned: true` ve `checkpoint_checked: true` 'yi verir. Doğrulama sonucunu koruyun.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Arşivin SHA-256 değerini, dışa aktarım sınırını, aktarım tarihini, göndereni ve alıcıyı muhafaza kaydınıza kaydedin. Orijinal paketi olduğu gibi koruyun ve kopyalar üzerinde çalışın. Uygulamanın özel veri dizini yerine kanıt dosyalarını paylaşın; bu dizinde hesap oturumları ve imzalama gizli bilgileri de bulunur. Aktarım için, dışa aktarılan dosya şifre korumalı bir AES-256 ZIP dosyasına yerleştirilebilir. Şifre yalnızca gizliliği korur ve saklanmaz; alıcı, arşivi açar ve içindeki imzalı dışa aktarımı doğrular; bu dosya değiştirilmemiştir.
   2. Bağımsız zaman sabitlemesi gerekiyorsa, [RFC 3161 prosedür](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/)ünü izleyin ve isteği, kontrol noktasını, güvenilir CA bilgilerini ve doğrulanmış yetki yanıtını saklayın. Yalnızca bir istek hazırlamak zaman damgası elde etmez.

Başarılı bir doğrulama, güvenilir toplayıcı anahtarı ve korunan sınır ile ilgili bütünlüğü teyit eder. Gerçekleştirilen kontrollerle ilgili güven varsayımları ve [doğrulama sonuçları](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) için [doğrulama kapsamına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) bakınız.

## Devir teslim özeti

İmzalı bir ZIP dosyası, çalışma alanının tüm günlüğünü içerir. Bir mahkeme, avukat veya ihbar birimi sadece bazı sohbetlere, belirli bir döneme veya belirli kişilere ihtiyaç duyduğunda, **Dışa Aktar → Devir Çıkarımı seçeneği**, seçilen ifşa kurallarına göre küçültülmüş bir kopya (`tgwitness-handover-v1`) hazırlar. Operatör, amacı belirtir ve sohbetleri, isteğe bağlı bir dönemi (UTC), özetin ilgili olduğu kişileri, diğerlerine ne olacağını (gösterilecek, P01, P02… takma adlarıyla değiştirilecek mi yoksa dışarıda bırakılacak mı), hangi mesaj metinlerinin kalacağını, hangi eklerin ve profil fotoğraflarının dahil edileceğini ve metinlerdeki telefon numaraları ile e-posta adreslerinin maskelenip maskelenmeyeceğini belirler. Amaç ve bu kurallar, imzalı manifestoda ve raporda yer alır; günlük, içeriği değil, dosyayı hazırlayan erişim bilgisi ve dosyanın SHA-256 değeriyle birlikte `handover.exported` kaydını tutar.

`verify.py`, bir özeti iki şekilde kontrol eder. Değişmemiş olarak gösterilen bir kayıt tam olarak doğrulanır: içeriği, hash değeri, Ed25519 imzası ve dahil edilen bir önceki kayda olan bağlantısı açısından. Küçültülmüş bir kayıt, orijinal hash değerini ve imzayı korur; bu nedenle imza hâlâ doğrulanır, ancak gizlenen alanlar bu kayıttan yeniden hesaplanamaz; kayıt, neyin gizlendiğini belirtir ve rapor bunu işaretler. Manifest, günlüğün uzunluğunu ve başlığını, o başlığın üzerinde toplayıcının imzasıyla belirtir ve dışarıda bırakılan kayıtların sayısını gösterir; `coverage.json`, seçilen sohbetleri açıklar. Dosya adları içindeki isimler algılanmaz. Paylaşmadan önce son dosyaları gözden geçirin: serbest metin, dosya adları ve seçilen ekler hâlâ kişilerin kimliğini ortaya çıkarabilir. İmzalanmış tam ZIP dosyasını saklayın: açılmış dosya bir ifşadır, ikame değildir.

## Okunabilir raporlar

İmzalı kanıtlar, devir teslim ve sohbet ZIP dosyaları, seçilen rapor dilinde okunabilir HTML ve JSON raporları ile gerekli yazı tipleri mevcut olduğunda PDF dosyalarını içerir. Her bir rapor, çalışma alanının Ed25519 anahtarıyla mühürlenir ve ayrı olarak doğrulanabilir: `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]`.

- `report.html` / `chat.html`: mühürleme ifadesi (`tgwitness-report-seal-v1`) dosyayı kapatır ve önündeki her baytın SHA-256'sini imzalar. Uzun günlükler ve sohbetler, yapılandırılabilir boyutta parçalara bölünür (Rapor ayarları, 500 ila 100.000 kayıt; varsayılan olarak 5.000): `records/records-0001.html` veya `messages/messages-0001.html`; her biri numarası, aralığı ve toplamıyla mühürlenir ve imzalı manifestoda SHA-256 ile birlikte listelenir. Toplayıcı kalp atışları dizileri, Rapor ayarlarında tek tek listelenmedikçe tek bir satır olarak gösterilir.
- `report.json` (`tgwitness-report-json-v1`, anahtarlar `format`, `report`, `seal`): mühür, `report`'nin kanonik JSON'sinin SHA-256'sini imzalar; böylece veriler dava sistemleri ve komut dosyaları tarafından okunabilir ve imzalı dosya bütünlüğünü korurken bunlardan veri koruma amacıyla bir seçim yapılabilir.
- `report.pdf` / `chat.pdf`: yazdırma ve dosyalama amaçlı resmi bir belge, aynı baytlar üzerinde iki kez imzalanmış, imza değeri (`/ByteRange`) hariç dosyanın tamamı. Standart PDF imzası (`adbe.pkcs7.detached`, CMS ile SHA-256 ve ECDSA P-256), çalışma alanı kasasında tutulan, kendi kendine düzenlenmiş bir belge imzalama sertifikasını kullanır; bu sertifikanın konu seri numarası, Ed25519 anahtar parmak izidir. Ed25519 mührü, CMS içinde imzalanmamış öznitelik `2.25.240684792623320047764573196045913242332` olarak yer alır ve sertifikanın SHA-256 adını `"content": "pdf-byte-range"` ile belirtir; böylece Ed25519 anahtarı sertifikanın geçerliliğini garanti eder. PDF okuyucu, dosyanın imzalandıktan sonra değişip değişmediğini gösterir ve sertifika güvenilir hale gelene kadar imzalayanı “bilinmeyen” olarak tanımlar; bunun yerine Ed25519 parmak izini karşılaştırın. Çince, Japonca ve Korece PDF’ler için sunucuda (veya `TGWITNESS_FONT_DIR` içinde) bir yazı tipi gerekir; yazı tipi yoksa ZIP dosyası yalnızca HTML ve JSON raporlarını içerir.

Bir kanalda veya süper grupta Telegram , mesajları 1, 2, 3… şeklinde sıralar. Bir sohbet dışa aktarımında ilk ve son numara, mevcut olanların sayısı ve eksik numaraların her bir dizisi `message-ids.json` , manifest ve `chat.json` başlığında listelenir ve her bir boşluk, transkriptte bulunduğu yerde işaretlenir. `verify.py` , `chat.json` 'den itibaren numaraları yeniden sayar. Eksik bir numara, Telegram 'nin geri döndürmediği bir mesajdır (dışa aktarımdan önce silinmiş veya hesap tarafından görülemiyor olabilir); özel sohbetlerde ve temel gruplarda numaralar hesabın tüm sohbetleri arasında paylaşılır ve boşluklar sayılmaz.

Geçmişi okuduktan sonra, dışa aktarma işlemi Telegram'dan eksik olan her numarayı tekrar, numaraya göre (`channels.getMessages`'dan 10,000'ye kadar olan numaralar) ister. Sonuç `message-ids.json`'de ve raporda yer alır. Boş bir yanıt, yeniden kontrol sırasında bu hesap için sayının mevcut olmadığını kaydeder; nedeni belirtilmez. Yeniden kontrol sırasında döndürülen bir mesaj, dışa aktarıma eklenir ve `found_on_recheck` olarak işaretlenir.

Her rapor **ile başlar. Özetle**: bir paragraf, ardından materyalin neyi gösterdiği ve neyi göstermediği (bir hesabın arkasında kim olduğu, teslimatın eksiksizliği, gözlemden önce yapılan silme işlemleri, zaman damgası olmayan saat bilgisi). Tarayıcı, sayfanın kendisini değil, mührün imzasını doğruladığında sayfanın kendi mühür damgası kehribar rengine döner: bir tarayıcı, bir sayfaya kendi baytlarını vermez. Yalnızca okuyucu dosyayı sayfanın sonundaki kontrol alanına sürüklediğinde ve her bayt eşleştiğinde yeşile döner; ancak bu, gösterilen sayfanın o dosya olması durumunda geçerlidir; aksi takdirde kırmızıya döner.

Her raporda programın adı tam olarak belirtilmelidir: toplayıcı bir checkout'tan çalıştırıldığında veya yükleyici kurulduğunda `TGWITNESS_COMMIT`ve kaynak dosyalarının SHA-256 değerleri (`source_tree_sha256`, yolun kanonik JSON'u → her birin SHA-256'sı `.py`, `.js`, `.css`, `.html` ve `.svg` dosyanın SHA-256 değeri), dosyalar değiştirilmedikçe o commit'in checkout'u ile yeniden üretilebilir. Telegram istemcisi, kütüphanesi, API katmanı ve veri merkezi ile adlandırılır. Gözlem başladığında ve bir sohbet dışa aktarma işlemi başladığında ve bittiğinde, toplayıcı Telegram'dan saatini ister (`updates.getState`, tam saniye) ve Telegram'ın saatinden toplayıcının saatini çıkararak, gidiş-dönüş süresinden kaynaklanan belirsizlikle birlikte kaydeder; raporlar bu ölçümleri "Zincir Sorumluluğu" başlığı altında gösterir. Bir sohbet dışa aktarma işlemi, mesajların tarihlerinin yanı sıra geçmişi ne zaman okuduğunu da kaydeder.

### Çevrimdışı rapor görüntüleyici ve arşiv kılavuzu

`chat.html` veya `report.html` dosyasını açmadan önce ZIP dosyasının tamamını çıkarın. Görüntüleyici, sunucu gerektirmeden arama, filtreler, katılımcılar, göstergeler, kayıt ayrıntıları ve JSON/CSV seçimleri sunar. `viewer/` ve `media/` dosyalarını raporun yanında bulundurun. Seçimler türevlerdir: bunları imzalı arşivle karşılaştırmak için `verify.py SELECTION.json
--evidence ARCHIVE.zip` dosyasını kullanın. Doğrulayıcı, rapor kimliğini, imzalama anahtarını, arşiv sınırını ve seçilen her bir öğeyi kontrol eder; düzenlenmiş, eksik ve yinelenen öğeler kabul edilmez. Seçim notları ve oluşturulma zamanı, imzalanmamış meta veriler olarak kalır.

Mesaj numarası boşlukları yalnızca tam, filtrelenmemiş ve artan sıralı sohbet akışında gösterilir. Bir kategorinin gizlenmesi veya bir veri bloğunun yüklenememesi, atlanan bir satırı eksik bir mesajın kanıtı haline getirmemelidir. Arama vurgulamaları, HTML kaçış kodlamasından önce düz metin üzerinde çalışır ve literal işaretlemeyi korur.

Tarayıcı, manifest imzalarını, rapor kimliğini ve anahtarı ile listelenen tüm dosya hash'lerini kontrol eder. Belirsiz veya hatalı biçimlendirilmiş ZIP yapılarını, yinelenen adları ve güvenli olmayan yolları reddeder; ayrıca dosyaları 256 MiB ile sınırlar ve beyan edilen toplam içerik boyutunu 4 GiB ile sınırlar. Daha büyük arşivler için bağımsız doğrulayıcıyı kullanın. Bu tarayıcı kontrolü, doğrulayıcının günlük zincirleri ve veri anlambilimi üzerindeki kontrollerini tamamlar.

`README.txt`, başlangıç kılavuzu, uyumlu dosya envanteri, doğrulama talimatları ve rapor dilinde veri formatı notlarını içerir; bunu tam bir İngilizce kılavuz izler. `SHA256SUMS`, kendisi, `manifest.json` ve `manifest.sig` hariç olmak üzere içinde listelenen dosyaları kapsar; imzalı manifest ayrıca `SHA256SUMS`'yi de kapsar. Orijinal ZIP dosyasını değiştirmeden koruyun ve çalışma dosyalarını çıkarılan klasörün dışına kaydedin. PDF raporları, bölüm yer imlerini ve sonraki sayfalarda vaka/rapor tanımlamalarını içerir.

### Dışa aktarım anındaki sohbet

Bir sohbet dışa aktarma işlemi, dışa aktarma başladığında Telegram'nin sohbet hakkında söylediklerini kaydeder: Telegram'nin kendi etiketleri (`scam`, `fake`, `restricted` ve gerekçeleri, `verified`), kullanıcı adları, açıklama, üye ve yönetici sayıları, bağlantılı tartışma, içerik koruması, yeni üyelerin önceki mesajları görüp görmediği ve bu hesabın geçmişi hangi mesajdan itibaren görebildiği (`available_min_id`), sohbetin oluşturulduğu tarihteki 1 numaralı mesajın tarihi ve sohbet fotoğrafının SHA-256 numarası (`media/`'de kaydedilmiştir). Sohbetteki dışa aktaran hesabın konumunu kaydeder: rol, katılım tarihi, kimin davet ettiği ve bir yönetici için hakları. Telegram'nin reddettiği bir istek ise bunun yerine adlandırılır.

Dışa aktarım yapan hesap bir yöneticiyse, dışa aktarım işlemi sohbetin yönetici günlüğünü (Telegram yaklaşık 48 saat saklanır) `admin-log.json` dosyasına aktarır: silme ve düzenleme işlemleri, içerik ve işlemi gerçekleştiren hesapla birlikte. Bu, silme işlemini kimin gerçekleştirdiğini belirten tek kayıttır.

### Göstergeler

Rapor listesi ve arşiv, `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) ve `indicators.misp.json` (MISP olayı) olarak, bir suistimal masasının kaydedilmiş mesajlarda harekete geçebileceği unsurları içerir: bağlantılar ve alan adları (metin arkasında, düğmelerde ve bağlantı önizlemelerinde gizlenmiş olanlar dahil), kripto para adresleri, Telegram kullanıcı adları ve davet bağlantıları, telefon numaraları, e-posta adresleri ve kaydedilmiş resimler. Bitcoin, Litecoin, Dogecoin ve TRON adresleri yalnızca base58 sağlama toplamları geçerli olduğunda listelenir; segwit adresleri bech32 veya bech32m sağlama toplamları geçerli olduğunda ve TON adresleri CRC sağlama toplamları geçerli olduğunda listelenir; EVM ve Solana adresleri ise kontrol edilmemiş olarak işaretlenir. Resimler, SHA-256 ve algısal hash (dHash, 64 bit) içerir; bu hash, yeniden sıkıştırılmış veya boyutlandırılmış kopyalarda neredeyse değişmeden kalır. Raporlar, göstergeleri yanlışlıkla açılmayacak şekilde yazar (`hxxps[://]example[.]com` ); dosyalar değerleri olduğu gibi korur. Her gösterge, bilinmeyen ve otomatik algılama için uygun olmayan olarak işaretlenir (STIX , `indicator_types: unknown` , MISP , `to_ids: false` , kendi organizasyona dağıtım): listelenmiş olması, bir mesajın onu içerdiğini gösterir, kötü amaçlı olduğunu değil. Metni, açıldığında görünen adresinden farklı bir adres gösteren bir bağlantı, raporda işaretlenir.

PDF raporları, inceleme görevlisinin elle imzalaması gereken bir beyan, noter veya mahkeme uzmanı için bir kontrol listesi ve rapor kimliği, anahtar parmak izi ile yetkili verilerin SHA-256 numarasını içeren bir QR kodu (aynı zamanda ilk sayfada da bulunur) ile sona erer; böylece yazdırılan kopya arşivine geri bağlanabilir.

## Olay kanonikleştirme

Hash girdisi tam olarak şu alanlardan oluşur:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

UTF-8 ile Python uyumlu JSON kullanarak serileştirin; nesne anahtarları sıralanmış, ASCII kaçış karakteri yok, önemsiz boşluklar yok ve NaN/sonsuzluk yok:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

Bu baytların SHA-256 değeri olay hash'i olur. İmza, 32 ham hash baytı üzerinde Ed25519 ile oluşturulur, ardından base64 ile kodlanır. İlk previous_hash 64 sıfırdan oluşur. Sıra numaraları 1'den başlar ve 1'er artar. Operasyonel olaylar da dahil olmak üzere tüm olaylar tek bir zinciri paylaşır. Yinelenen teslimatların engellenmesi söz konusu değildir: tekrarlanan gözlemler, farklı Telegram eylemlerine dair bir iddia değil, ayrı ayrı alındıklar olarak kabul edilir.

Ham Telegram verileri ISO dizeleridir; ikili alanlar, bytes_base64 içeren nesnelere dönüşür. Mesaj metni, varlıklar, medya tanımlayıcıları, yanıt meta verileri, tepkiler ve hizmet eylemleri, sağlandıkları takdirde ham mesaj meta verilerinde saklanır.

observed_at, toplayıcının UTC duvar saatidir. source_at, mevcut olduğunda sağlanan Telegram tarihidir. Silme bildirimleri kesin bir silme zamanı sağlamadığından, source_at değeri boş kalır. Aktarım alım sırası, kaynak olay sırası ile mutlaka aynı değildir. Geçmiş anlık görüntüleri, daha eski kaynak tarihlerini ancak güncel gözlem zamanlarını kullanır.

## Aktör semantiği

message.new actor_id, mesajın gönderenidir. message.edited'de çıkarılan bir düzenleyici yoktur; payload.sender_id, gözlemlenen mesajın gönderenini kaydeder. Silme işlemlerinde actor_id değeri null olarak kalır. Üyelik hizmeti mesajları, her silme işlemini gönüllü ayrılma olarak yorumlamadan göndereni ve eylem türünü korur. Ham katılımcı güncellemeleri, actor_id değerini sağlandığı şekilde korur. Tepki anlık görüntüleri, bir değişiklik aktörü uydurmaz.

Özel sohbetler ve normal gruplar için silme bildirimleri yalnızca mesaj kimliklerini içerir. Bu sohbetler hesap genelinde tek bir kimlik dizisini paylaşır; dolayısıyla bir kimlik, bu hesaba ait tek bir mesajı tanımlar. Bu kimlik numarasına sahip bir mesaj daha önce bu günlüğe kaydedilmişse, silme işlemi o sohbette message.deleted olarak kaydedilir ve yöntem adı olarak payload.chat_resolution kullanılır. Hiç kaydedilmemiş kimlik numaraları, chat_id olmadan deletion.unscoped olarak tutulur; hiçbir şey tahmin edilmez. Kanallar ve süper gruplar, mesajları sohbet başına numaralandırır ve bu şekilde asla eşleştirilmez. Silinen mesaj gözlemlenen hesap tarafından gönderilmişse, payload.deleted_message_was_outgoing değeri true olur; silen kişinin bilgisi yine de sağlanmaz.

Kapsam dışı bir bildirim, bir mesajın hiçbir zaman kaydedilmediğini kanıtlamaz: eşleşen bir sohbet, mevcut gözlem kapsamı dışında olabilir veya benzersiz bir eşleşme bulunmayabilir. Yokluk kontrolü, rapor sayımlarında, filtrelerde ve etiketlerde bir silme bildiriminden ayrı bir gözlem olarak kalır. Daha sonraki bir kurtarma işlemi, imzalı geçmişteki önceki başarısız kontrolü korurken mevcut eksiklik durumunu ortadan kaldırır; her iki gözlem de bir silme bildirimi oluşturmaz.

Tek bir bildirimden aynı sohbete çözümlenen birden fazla kimlik, sayısına bakılmaksızın `deletion.batch` olarak gruplandırılır. Bildirim, geçmişin tamamının silindiğini, silme işlemini kimin gerçekleştirdiğini veya bunun tüm katılımcılar için geçerli olup olmadığını belirtmez. Kaydedilmiş giden mesajlar bu sınırları değiştirmez. Eski günlükler, on veya daha fazla kimlikten oluşan gruplardan çıkarılan `history.cleared` olaylarını içerebilir; bu olaylarda, silme işleminin diğer katılımcı tarafından yapıldığını belirten açıklayıcı metin bulunur. Bu çıkarımlar güncelleme tarafından desteklenmemektedir. Orijinal imzalı kayıtları koruyun, ancak bunları gruplandırılmış silme bildirimleri olarak değerlendirin; mevcut arayüz bunları uygun şekilde etiketler.

## Kapsam: süreklilik, boşluklar ve gözlemlenmemiş kimlikler

Her imzalı ZIP dosyası `coverage.json`'yi içerir; HTML raporu aynı özetle açılır ve `verify.py`, dosyaya güvenmek yerine `events.jsonl`'den bu özeti yeniden hesaplar:

- **X'ten Y'ye kadar sürekli olarak gözlemlenir.** Bir dönem `observation.started` ile başlar ve bir duraklama, bir durdurma, Telegram bağlantısının kesilmesi, oturumdan çıkış, düzgün bir durdurma olmaksızın başlayan bir işlem veya gözlem sırasında herhangi bir kayıt olmaksızın üç dakikadan fazla süren bir süre ile (her dakika bir kalp atışı kaydı yazılır; bu nedenle sessizlik, işlemin durduğu, donduğu veya bilgisayarın uyku moduna geçtiği anlamına gelir). **Parametreler** bölümünde kalp atışı aralığı değiştirildiğinde, her kalp atışı bu değişikliği kaydeder ve izin verilen sessizlik süresi üç aralığa çıkar; bu süre asla üç dakikadan az olamaz.
- **Boşluklar,** dönemler arasındaki süreyi ve nedenini listeler. Son kayıtta hâlâ açık olan bir boşluk, `not_resumed_by_last_record` olarak işaretlenir.
- **Mesaj kimlikleri gözlemlenmemiştir.** Sohbet başına mesaj sayısını belirleyen kanallar ve süper gruplar için, gözlemlenen kimlikler arasındaki eksik kimlikler aralıklar halinde listelenir. Bunlar, *"gözlemlenmemiş*" — silinmiş, hiç teslim edilmemiş veya kaydedilmiş geçmişin dışında — olarak rapor edilir; asla "silinmiş" olarak rapor edilmez. Özel sohbetler ve normal gruplar hesap genelinde ortak bir sıra numarası kullanır; bu nedenle, bu tür bir sohbet içindeki boşluklar bir anlam ifade etmez ve burada listelenmez.
- Sohbet düzeyindeki boşluk bildirimleri (örneğin, Telegram'ın bir kanalda farkın telafi edilmesini istemesi gibi) not olarak sayılır; bunlar genel kapsamı kesintiye uğratmaz.

### Eksik mesaj numaraları (`gap_summary`)

**Önizleme.** `coverage.json` → `gap_summary` Telegram'ın atadığı ve bu toplayıcının hiç görmediği numaraları ölçer. Telegram, mesajları kanal veya süper grup başına bir kez ve özel sohbetler, botlar ve normal gruplar genelinde hesap başına bir kez numaralandırır. Gözlemlenen iki mesaj arasındaki bir numara ya gözlemlenmiştir ya da eksiktir; ardışık bir aralık, içinde numaralandırılan her mesajın gözlemlendiğine dair kesin bir ifadedir. Bir boşluk, herhangi bir aktörü veya nedeni belirtmez.

| Alan | Anlam |
| --- | --- |
| `status` | `on`, veya `off` **Parametreler → Boşluk analizi** bölümünden kapatıldığında |
| `parameters` | Sonucun elde edilmesini sağlayan parametreler; böylece işlem tekrarlanabilir |
| `chats[]` | Her kanal veya süper grup için birer giriş olacak ve her biri ayrı ayrı numaralandırılacaktır. |
| `account` | Hesap genelinde özel sohbetler, botlar ve normal grupların sıralaması |
| `status` (her sekans için) | `applicable`, veya `not_applicable` ile `reason` |
| `observed_from`, `observed_to`, `span` | İlk ve son gözlemlenen numara ile aralığın boyutu |
| `observed`, `observed_without_content` | Gözlemlenen numaralar; yalnızca silme veya yeniden kontrol kaydından bilinenler |
| `missing`, `density`, `gap_ranges`, `largest_gap` | Hiç gözlemlenmemiş sayılar, aralıktaki payları, kaç kez çalıştırıldığı, en uzun çalıştırma süresi |
| `clusters[]` | Listelenen eksiklikler: `low`, `high`, `missing`ve komşu gözlemlenen sayılar `after` / `before` ve gözlem zamanları |
| `service_estimate` | Yalnızca etkinleştirildiğinde: gözlemlenen paylarına göre kaç tane eksik numaranın hizmet mesajı olacağı. Asla şu değerden çıkarılmamalıdır: `missing` |

Geçerlilik, günlüğünden türetilir; asla varsayılmaz:

- **Kanallar ve süper gruplar**, sohbet başına ölçülür; ayrıca seçilen sohbetlerin dışa aktarımı sırasında da ölçülür. Gönderici tarafından seçilen kayıtlar ölçüme dahil edilir `not_applicable`.
- **Hesap genelindeki sıra**, yalnızca "tüm hesap toplama" özelliği açıkken gelen ilk mesajdan son mesaja kadar ölçülür ve özel sohbetler, botlar, normal gruplar ve hesabın kendi mesajları dahil edilir; bu tür hiçbir sohbet hariç tutulmaz (`scope.changed`). " `deletion.unscoped` sayılan sayılar, içerik olmadan gözlemlenmiş sayılır. Seçilen sohbetlerin dışa aktarılması veya devri bu ölçümü etkilemez. Hesap genelinde veri toplama özelliği kapalı ve açık olarak değiştirildiyse, bu sırada kullanılan sayıların boşluklar olarak göründüğüne dair bir not bulunur.
- Hizmet mesajları, kendi numaralarına sahip günlük kayıtlarıdır; bu nedenle boşlukları kendiliğinden doldururlar; isteğe bağlı tahmin ise yalnızca bağlam bilgisi niteliğindedir.

`verify.py` yeniden hesaplar `gap_summary` 'den `events.jsonl` imzalı `coverage.json` (eski arşivler için varsayılanlar) ve kapsam özetinde hesap genelindeki satırı yazdırır. Arşivin `get_capture_status`(MCP ve komut satırı), bir erişimin okuyabileceği sohbetler için aynı ölçümü döndürür; hesap genelindeki dizi ise yalnızca tüm çalışma alanını kapsayan erişimler için geçerlidir.

Bir hizmet mesajının tekrarlanan gözlemleri bir kez sayılır ve hesap hizmeti tahmini yalnızca ölçülen aralık içindeki sayıları kullanır. Uygulanan kapsam, hesap genelinde ölçüm etkinleştirilmeden önce hesabın kendi mesajlarını açıkça korumalıdır; bu bilgiyi içermeyen eski kayıtlar bu koşulu sağlayamaz. Durdurulan gözlem, ölçüm aralığını genişletmez ve yeniden başlatılması not edilir. Canlı arşiv sorgusunun, veritabanı taraması da dahil olmak üzere bir zaman bütçesi vardır ve tamamlanmamış bir ölçümü kısmi olarak işaretler.

Telegram, [ayrı mesaj kimlik dizilerini](https://core.telegram.org/api/updates#message-id-sequences)belgelemektedir. Bu sayılar gözlemleri tanımlar; bir silme eylemini gerçekleştiren kişiyi tanımlamaz veya bir sayının neden eksik olduğunu belirlemez.

Telegram, hesabı kabul etmeyi durdurduğunda, gözlemi sonlandıran `coverage.gap` kaydı `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` veya `not_authorized`) değerini ve Telegram hatasını taşır; `verify.py` ise dönemin sona erme nedenini belirtir.

Kapsam, kaydedilen gözlem dönemlerini, kesintileri ve mesaj sonuçlarını birleştirir. Bunu, seçilen sohbetler, dönem ve ek politikası ile birlikte değerlendirin; sürekli çalışma tek başına Telegram güncellemelerinin tam olarak iletildiğini garanti etmez.

## Yapımcı

İmzalı kanıt ZIP dosyaları, sohbet dışa aktarımları, tanık günlükleri ve kişi profili dosyalarının beyanı, `producer` bilgilerini içerir: yazılım, sürüm, proje (PhishDestroy), ana sayfa ve kaynak deposu. HTML raporu aynı satırı gösterir ve `verify.py` , bunu doğruladığı bilgilerin bir parçası olarak yazdırır. Bu alan oluşturulmadan önce oluşturulan arşivler, önceki gibi doğrulanır ve üretici adı belirtilmemiş olarak raporlanır.

Her `observation.started` kaydı, gözlem yapan Telegram istemcisinin adını da belirtir: `api_id` (asla hash değeri değil), bunun yerleşik bir açık anahtar çifti mi yoksa operatörün kendi uygulaması mı olduğu, Telegram'nin bağlantı isteğinde gönderilen istemci açıklaması ve IP moduyla birlikte bağlantı yolunun türü (proxy adresi veya gizli bilgi yok). Rapor ve `custody.json`, her bir farklı istemciyi ve rotayı, kaydedildikleri zamanla birlikte listeler; ayrıca listelenen hiçbir proxy'nin yanıt vermediği zamanları ve Telegram'nin sunucunun adresini gördüğü zamanları da gösterir. Bundan önce kaydedilen günlükler de bunu doğrulamaktadır.

## Kişi profilleri

Bir profil dosyası (`tgwitness-dossier-v1`, JSON), talep üzerine, bir sohbet için günlüğünde halihazırda bulunan kayıtlardan oluşturulur; Telegram'dan hiçbir şey alınmaz ve profil içeriği asla günlüğe yazılmaz (profillerin açılıp kapatılması `dossier.changed` olarak kaydedilir). Kaydedilmiş mesajı olan her kişi için, kaydetme anında görüldüğü şekliyle isim ve kullanıcı adı geçmişi, Telegram işaretleri (bot, dolandırıcılık, sahte, premium, doğrulanmış, kısıtlanmış, silinmiş) ile profil fotoğraf kimlikleri, yerel avatar önbelleğindeki benzer avatarların SHA-256 ve algısal hash (pHash, `imagehash.phash` ile uyumlu) değerleri, etkinlik (ilk ve son mesaj, sayılar, düzenlenmiş ve silinmiş paylaşımlar, UTC saatine göre mesajlar), kimin kime yanıt verdiği, kişinin yazdığı ve bahsedilen cüzdanlar (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; Base58Check adresleri sağlama toplamı ile doğrulanır), telefon numaraları, kullanıcı adları ve metin arkasında gizlenmiş bağlantılar dahil olmak üzere bağlantılar.

Her bir gerçek, kaynaklandığı günlük kayıtlarını (`seq`) listeler ve `record_hashes`, bağlantı verilen her kaydın hash değerini içerir. Açıklama, çalışma alanı anahtarıyla imzalanmıştır:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

imzayı kontrol eder, kanıt dışa aktarımının kendisini (imza, hash zinciri ve dosyalar) doğrular ve atıfta bulunulan her kaydın aynı çalışma alanının söz konusu dışa aktarımında değiştirilmemiş olarak mevcut olduğunu teyit eder. Avatar hash'leri yerel önbellekten geldiği şeklinde etiketlenir (günlük kayıtlarından değil). Bahsetmeler desen eşleşmeleridir — doğrulanmış gerçekler değil, kontrol edilmesi gereken ipuçlarıdır. Profiller sohbet bazında etkinleştirilir, şifreli bir AES-256 ZIP dosyası olarak dışa aktarılabilir ve devre dışı bırakıldığında veya sohbet kaynaklardan kaldırıldığında silinir.

## Bağımsız tanık

Bir tanık günlüğü (`tgwitness-witness-v1`) ve kanalındaki gönderiler, `verify.py --witness … --channel …` ile yapılan kanıt dışa aktarımına göre kontrol edilir; bkz. [bağımsız tanık](https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/).

## Manifest ve kontrol noktaları

manifest.json dosyası, formatı, dışa aktarım zamanını, açık anahtarı, parmak izini, günlüğün uzunluğunu, baş hash değerini, kapsamı, üreticiyi, sınırlamaları ve `manifest.json` ile `manifest.sig`'nin kendileri dışındaki her içerik elemanının SHA-256 değerini içerir. manifest.sig dosyası, kanonik manifest JSON dosyası üzerinde oluşturulan base64 Ed25519 imzasını içerir. Doğrulayıcı, beklenmeyen/eksik elemanları, yinelenen adları, bozuk dosyaları, kırık sıra/zinciri, geçersiz imzaları ve sağlanan kontrol noktasıyla uyuşmazlıkları reddeder. Arşiv yollarını asla ayıklamaz. Beyan edilen toplam sıkıştırılmamış boyutu 4 GiB ile sınırlar; `--max-gib N`, artırılmış **Parameters** sınırıyla oluşturulan daha büyük arşivlere izin verir.

Doğrulamayı, kurulu TgWitness sürümünüzden veya incelenmiş bir checkout'tan çalıştırın. Arşivde bulunan kopya taşınabilir kullanım için uygundur; çalıştırmadan önce bu kopyayı güvenilir kurulumunuzla karşılaştırın.

Bir kontrol noktası, açık anahtar, günlük uzunluğu, başlık hash'i ve oluşturulma zamanını içeren bir beyanı imzalar. Doğrulayıcı, daha sonraki bir arşivin aynı önek içerdiğini kontrol edebilir. Kontrol noktasını toplayıcının dışında tutun, böylece daha sonraki doğrulama işlemi arşivi, ondan ayrı olarak tutulan bir referansla karşılaştırır.

## Doğrulama kapsamı

Doğrulama işlemi, arşivi ve arşivin oluşturulmasında kullanılan toplama modunu kontrol eder. Duruma uygun güven sınırına sahip modu seçin, ardından bu modun doğrulama girdilerini koruyun.

| Toplama modu | Doğrulayıcının kontrol ettiği unsurlar | Doğrulama girdileri ve güven sınırı |
| --- | --- | --- |
| Yerel çalışma alanı | İmzaları, hash zincirini, manifestoyu ve ek baytlarını kaydedin | Bağımsız olarak saklanan toplayıcı parmak izi; yerel imzalama anahtarını ana bilgisayar yöneticisi kontrol eder |
| Bağımsız bir tanık içeren yerel çalışma alanı | Arşiv kontrolleri ve tanık tarafından saklanan önceki günlük önekiyle uyumluluk | Ayrı ayrı güvenilir tanık anahtarı ve kayıtlar; kontrol noktası, önceden gözlemlenmiş olan önekle bağlanır |
| [GitHub Actions kaydı](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | Arşiv özetinin GitHub onayı, onaylanmış iş akışı ve toplayıcı taahhütleri, barındırılan çalıştırıcı, yeni oturum/anahtar kaynağı ve dahili arşiv bütünlüğü | Güvenilir doğrulayıcı politikası, arayan deposu ve GitHub tasdik paketi; toplama işlemi sabitlenmiş iş akışı altında yürütülür |
| [Bulut dağıtımı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/) | Sağlayıcı yaşam döngüsü ve erişim kayıtları, güvenlik duvarı ve Cloudflare durumu ile toplayıcının imzalı çalıştırma kaydı | Sağlayıcıya ve Cloudflare’e yönelik salt okunur sorgular; tek tek kontrollerin kullanılabilirliği sağlayıcıya bağlıdır |
| [Intel TDX gizli sanal makinesi](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | İmza ve platform durumunu, toplayıcı beyanına, kompozisyona ve işletim sistemi ölçümlerine bağlayarak alıntılayın. | Intel güven zinciri ve beklenen dağıtım ölçümleri; gerekli tüm TDX kontrollerinin sonuçlarını koruyun |

Mühürlü veri toplama işleminde, onaylanmış toplayıcı, doğrulanmış ortam içindeki kimliği doğrulanmış bir Telegram bağlantısı aracılığıyla verileri alır. Tasdik, arşivi o yürütme işlemine bağlar; böylece doğrulama, veri toplama işleminin yanı sıra daha sonraki dosya bütünlüğünü de kapsar. Bu, onaylanmış koda ve yukarıda listelenen platform güven zincirine dayanır. GitHub yakalama doğrulaması, çalıştırma içinde oluşturulan bir oturum gerektirir ve ithal edilmiş oturum yakalamalarını reddeder.

Çalıştırma makbuzu, toplayıcı sürümünü, dosya hash değerlerini ve başlangıç ayarlarını kaydeder. GitHub kaynak bilgisi ve TDX ölçümleri ortam kontrollerini sağlar; [doğrulama kaydı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/), test edilen yapılandırmaları tanımlar.

TgWitness, topladığı gözlemleri imzalar; Telegram ve mesaj yazarları bu imzaları vermez. Yerel bir çalışma alanında, ilk bağımsız kontrol noktasından önce oluşturulan materyaller hâlâ toplayıcıya ve anahtar sahibine bağlıdır. Kapsam kayıtları, seçilen kapsamı ve toplama sonuçlarını açıklar; doğrulanmış harici zaman damgaları ise kaydedilen arşiv veya günlük sınırını zamansal olarak sabitler.

## Ekler

Dosyalar, media/ dizininde SHA-256 ile tanımlanır. Bir media.saved olayı, bir hash değerini ve bayt uzunluğunu belirli bir mesaj olayına bağlar. Ham dosya adları meta verilerdir, asla yerel yollar değildir. Medya baytları eşzamansız olarak indirilir; bu nedenle anında silme işlemi, yakalamayı engelleyebilir. Devre dışı bırakılmış toplama, aşırı büyük/boyutu bilinmeyen dosyalar, indirme hataları ve kesintiye uğrayan indirmeler sonuçlar olarak görüntülenir. Bir işlem çökmesi, referanssız kısmi dosyalar bırakabilir; bunlar dışa aktarımlara dahil edilmez.

ZIP dışa aktarıcısı, depolanan medya dosyalarını adlarına göre doğrular. JSONL, CSV ve HTML dışa aktarımları olay imzalarını doğrular ancak medya baytlarını içermez. Türetilmiş raporlar kolaylık sağlar; events.jsonl dosyası, olayların resmi temsilidir.

Tam bir sohbet dışa aktarma işlemi, çalışma alanının ek ayarlarında belirtilen ekleri media/ dizinine, SHA-256 adıyla kaydeder. chat.json'deki her mesaj kaydı, dosya adını (`file`, `file_sha256`) veya eksik olma nedenini (`file_status`) belirtir; buna ek olarak okuyucunun metin etrafında gördükleri de dahil edilir: metnin arkasındaki bağlantılar, iletme kaynağı, bot düğmeleri, imza, görüntüleme sayısı ve otomatik silme zamanlayıcısı. `verify.py`, adlandırılmış her dosyanın o hash altındaki imzalı manifestoda bulunduğunu kontrol eder.

## Kalıcı toplama ve işlem makbuzları (0.2)

Bir medya işi ve ilgili mesaj olayı, tek bir işlemde kaydedilir. İş, orijinal TL mesaj tanımlayıcısını depolar; imzalı gözlem, SHA-256 değerini, hesabı ve boyut politikasını bağlar. Kurtarma işlemi, indirme öncesinde bu bağlamayı doğrular. Asla mevcut mesajı almaz ve sessizce daha yeni bir eki ikame eder. Kesintiye uğrayan işler yeniden denenirken, kalıcı hata açık bir sonuç olarak kalır.

Her çalışma alanının kendi günlüğü ve imzalama kimliği vardır. Bir process.started olayı şunları içerir: çalıştırma kimliği, yerel saatler, bağımlılık sürümleri, kaynak dosya hash'leri, başlangıç hesabı/kapsamı ve yakalama ayarları. Heartbeat'ler çalıştırma kimliğini, monotonik zamanı ve kuyruk durumunu içerir. Çalıştırma makbuzu, ayrı olarak imzalanmış bir bildirim olarak da indirilebilir. Yürütme ortamının doğrulanması için, bunu [Doğrulama kapsamı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) bölümünde açıklanan GitHub tasdiki veya TDX kontrolleriyle birlikte kullanın.

Otomatik kontrol noktaları, başlangıçta, gözlem sırasında her beş dakikada bir (**Parametreler → Her**'de imzalı kontrol noktası) ve düzgün bir şekilde durdurulduğunda yerel olarak saklanır. Başlangıç doğrulaması ve dışa aktarma, günlüğü en son saklanan yerel kontrol noktasıyla karşılaştırır. Bu, kontrol noktası korunmuşsa bir veritabanı geri alma işlemini tespit edebilir. Bağımsız saklama, bu referansı çalışma alanı dışında kullanılabilir tutar; doğrulanmış bir harici zaman damgası ise bunu zamana sabitler.

Yeniden başlatmanın ardından, kaydedilmiş Telegram güncelleme konumu devam ettirilir (`catch_up_from`'den `observation.started`'ye) ve kaçırılan güncellemeler istenir. Periyodik bir yeniden kontrol, kaçırılan mesajlar için `message.recovered`'yi ve Telegram'ın artık kaydedilmiş bir mesajı döndürmemesi durumunda `message.missing_on_recheck`'yi kaydeder; ikincisi bir silme bildirimi değildir ve silen kişinin adını veya zamanı belirtmez.

### Site dışı yedekleme ve geri yükleme (S3)

Site dışı kopya (Dışa Aktarımlar, varsayılan olarak kapalı), günlük bölümlerini, korunan dosyaları, kontrol noktalarını zaman damgalarıyla birlikte ve tamamlanmış sohbet dışa aktarımlarını, çalışma alanı kasasında saklanan bir anahtarla AES-256-GCM ile şifrelenir; depolama kovası bunu desteklediğinde Object Lock saklama kuralı geçerlidir. İndirilmiş anahtar olmadan kopya okunamaz. Geri yükleme ve doğrulama işlemleri `python -m tgwitness.replica restore --key-file KEY.json --out DIR` ile gerçekleştirilir.

Geri yükleme işlemi için boş bir normal dizin gereklidir. İndirilen ve şifresi çözülmüş nesneler, tüm günlük ve saklanan her kontrol noktası doğrulanana kadar özel geçici depolama alanında kalır. Güvenli olmayan nesne yolları, tutarsız segment aralıkları ve bir kontrol noktasından daha kısa günlükler reddedilir; başarısız doğrulama durumunda geri yüklenen dosya yayınlanmaz. Saklama kontrolleri, geri döndürülen Nesne Kilidi modunu ve tarihini, yükleme sırasında gönderilen son tarihle karşılaştırır (bir saniyelik yuvarlama toleransı). Süresi dolmuş, geçersiz veya kısaltılmış son tarihler doğrulanmış olarak kabul edilmez. Durum raporu, o yükleme geçişi için saklama süresi okunan örnek nesneyi bildirir.

Eksik veya bozuk yerel medya, geçiş hatası olarak rapor edilir ve medya imleci bunun önünde tutulur, böylece dosya bir sonraki geçişte tekrar denenir; bundan sonraki dosyalar, kontrol noktaları ve dışa aktarımlar yine de kopyalanır. Geri yükleme, şifresi çözülmüş hash değerleri ve kaydedilen boyutlara göre tüm korunmuş medya referanslarını kontrol eder. Kesintiye uğrayan yüklemelerden kaynaklanan aynı çakışan günlük segmentleri tekilleştirilir; çakışan kısımlar reddedilir. Yükleme sırasında oluşturulan kontrol noktaları, kapsadıkları günlük kayıtları kopyalanana kadar ertelenir; böylece tamamlanan bir geçiş, kontrol noktasını günlükten önce yayınlamaz.

### Akış halinde dışa aktarma anlık görüntüleri

Akışlı dışa aktarımlar, kararlı bir SQLite okuma anlık görüntüsü kullanır. İndirme işlemi tamamlandığında, bu anlık görüntünün başlangıcı mevcut canlı günlüğünden daha eski olabilir. Bu anlık görüntünün ardından oluşturulan bir kontrol noktası, arşivin daha kısa olduğunu doğru bir şekilde bildirebilir; bunu, dışa aktarılan önekle aynı veya ondan önceki bir kontrol noktasıyla karşılaştırın, keyfi olarak daha sonraki bir kontrol noktasıyla değil.

## RFC 3161 hazırlığı ve yanıt doğrulaması (0.2)

Kanıt modu (varsayılan olarak kapalı), her bir imzalı kontrol noktasının yalnızca SHA-256 değerini, çalışma alanı rotası üzerinden ve asla MTProxy üzerinden değil, listelenen RFC 3161 yetkililerine ve OpenTimestamps takvimlerine gönderir. Yanıtlar `checkpoints/anchors/`'de saklanır, dışa aktarılır ve `verify.py` tarafından kontrol edilir (`--tsa-ca`, TSA imzasını kontrol eder; OpenTimestamps kanıtlarını `ots upgrade` ve `ots verify` ile doğrular).

Panel, kanonik checkpoint.json baytlarını, timestamp.tsq dosyasında yer alan SHA-256 mesaj parmak izini ve rastgele nonce değerini, sağlama toplamlarını ve talimatları içeren bir istek arşivi hazırlar. Herhangi bir ağ isteği yapılmaz. Hazırlanan dosya, güvenilir bir zaman damgası değildir.

`python -m tgwitness.anchor verify`, OpenSSL ts'yi iki kez çağırır: bir kez kontrol noktası baytlarına karşı, bir kez de orijinal isteğe karşı. Güvenilir bir CA dosyası açıkça gereklidir; dahil edilen sertifikalara otomatik olarak güvenilmez. İstek kontrolü, komut satırında isteğe bağlıdır; bu nedenle, nonce'yi kontrol etmek için --request seçeneğini koruyun ve sağlayın. Sonuç, kontrolün yapılıp yapılmadığını belirtir. Toplayıcı kontrol noktası imzası ve günlüğü, yine de güvenilir toplayıcı parmak izi ile ayrı olarak doğrulanmalıdır.

Doğrulama işlemi, yanıt imzasını, kontrol noktası baytlarını ve (varsa) belirtilen CA güveni kapsamında orijinal isteği kontrol eder. Sertifikanın geçerlilik süresinin dolmasından sonraki iptal kontrolleri ve uzun vadeli arşivleme doğrulaması, mevcut doğrulayıcının kapsamı dışındadır. [Prosedüre](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/) ve [doğrulama sonuçlarına](https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/) bakın.

## Kanıt modunda isteğe bağlı kayıtlar: drand ve Telegram cihazları

Zaman damgalarıyla aynı geçişlerde iki kayıt daha çalıştırılabilir. Her ikisi de varsayılan olarak kapalıdır ve yalnızca kanıt modu açıkken etkin hale gelir: Ekstra Özellikler → Kanıt ve yedeklemeler → **Daha fazla tanık · isteğe bağlı**, veya `"drand": true` ve `"devices": true` içinde `POST /api/evidence`. Birinin başarısız olması, diğerini veya zaman damgalarını durdurmaz; panel, formun altında her birinin en son sonucunu gösterir.

**drand** (`beacon.drand` ). Her geçiş, League of Entropy’nin halka açık rastgelelik kaynağı olan drand quicknet’in en yeni turunu (her 3 saniyede bir tur) günlüğe yazar: `chain` , `round` , `randomness` , `signature` , `round_time` ve yanıt veren `relay` . Doğrulanmış öngörülemez bir tur, sonraki hash bağlantılı materyal için daha düşük bir zaman referansı sağlar. Daha sonraki bir kontrol noktasında doğrulanmış bir zaman damgası, üst zaman referansı sağlar. Bu kontroller bağlantılı içeriği sınırlar; toplama kapsamı ayrı olarak değerlendirilir. Toplayıcı, her geçişte bir istekle önce `drand.cloudflare.com` ’a, ardından çalışma alanı rotası üzerinden Protocol Labs’ın aktarıcılarına başvurur.

`verify.py` , her bir rastgeleliğin imzasının SHA-256 olup olmadığını ve tur süresinin doğru olup olmadığını kontrol eder; turları, tur olmayan en uzun aralığı ve toplayıcının saatinin drand'dan ne kadar geride kaldığını raporlar. BLS imzasını kontrol etmez. `--check-drand` , turları bir Cloudflare aktarıcısıyla ve bir Protocol Labs aktarıcısıyla karşılaştırır; bu karşılaştırma tüm veriler üzerinde veya uzun bir günlükteki rastgele seçilmiş 100 örnek üzerinde yapılır; farklılık gösteren bir tur, doğrulamayı geçemez.

**, Telegram,** (`account.devices`) cihazları. Her geçişte, `account.getAuthorizations` ile hesabın oturumları okunur; Telegram listesi Ayarlar → Cihazlar bölümünde gösterilir ve şu şekilde kaydedilir: önceki geçişten bu yana değişiklik olmuşsa tam olarak, `added` ve `removed` oturum hash'leriyle birlikte; aksi takdirde sadece sayısı ve SHA-256 ile kaydedilir. Cihaz modeli, platform, uygulama ve sürüm, oluşturulma tarihi ve son etkinlik, ülke ve bölge saklanır; IP adresleri saklanmaz, çünkü kanıtların dışa aktarılması sizin kontrolünüz dışındadır. Toplayıcının kendi oturumu her zaman aktiftir, bu nedenle sadece diğer oturumların etkinliği bir değişiklik olarak sayılır. `verify.py`, listenin ne sıklıkla kaydedildiğini ve her yeni ve sona eren oturumu bildirir. Listeyi yalnızca gözlem çalışırken okur.

Göstermedikleri şey: drand, kayıtların kamuya açık zamana göre sıralamasını kanıtlamaktan öteye gitmez, ve cihaz listesi, diğer tüm kayıtlar gibi toplayıcı tarafından imzalanmış, Telegram'nin toplayıcı aracılığıyla yaptığı beyan niteliğindedir.

**Cloudflare Gateway günlüğü** (`cloudflare.gateway_dns`). Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)) üzerinden çözümleme yapan bir sunucu için, her kopyalama işlemi, bir önceki kopyalamadan bu yana Gateway'in kaydettiği verileri kopyalar: en fazla üç saatlik bir zaman aralığı başına bir kayıt; `from`, `until`, `location_id`, ayarlanmışsa sunucunun `address` ve `queries` ile `[at, name, type, rcode, decision, colo]` (hiçbiri yoksa da). **altında ayarlayın. Cloudflare Gateway günlüğü**: hesap, konum, isteğe bağlı adres ve bir salt okunur belirteç (Hesap Analytics Okuma; paylaşılan bir konumun tek bir adresini saklamak için Zero Trust PII Okuma). Panel, kaydetmeden önce bunları tek bir istekle kontrol eder; jeton şifreli kalır ve asla günlüğe girmez. `verify.py`, pencereleri, en çok aranan isimleri ve kopyanın kapsamadığı zamanları listeler; sayısı sorgularıyla eşleşmeyen bir kayıt başarısız olur. Tek bir saniye içinde birden fazla sayfa sorgu barındıran bir pencere, o sayfayı saklar ve geri kalanının eksik olduğunu belirtir. Kopya, toplayıcı aracılığıyla Cloudflare’in verdiği ve toplayıcı tarafından imzalanmış yanıttır; 24 saat içinde salt okunur jetona sahip herkes bunu Cloudflare ile karşılaştırabilir.
