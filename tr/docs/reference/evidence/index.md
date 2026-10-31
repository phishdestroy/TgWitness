# Kanıt formatı

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/

İmzalı ZIP dosyasının içeriği, kayıt türleri, işlem makbuzları, kullanıcı profilleri, site dışı kopyalar ve çevrimdışı doğrulama.

Bir gözlem, bir sonuç değildir. Gönderen kimliği, gerçek dünyadaki bir kimlik değildir. Hesap tarafından görülebilen hizmet güncellemesi kaynaktır; Telegram, üçüncü taraf araştırmacılar için bu kaydedilmiş kayıtları kriptografik olarak imzalamaz.

## Neler imzalanır?

| Materyal | Koruma | Neler saklanmalı |
| --- | --- | --- |
| Operasyonel olaylar dahil olmak üzere her günlük kaydı | Her olay için bir SHA-256 zinciri ve bir Ed25519 imzası | Orijinal `events.jsonl`, güvenilir anahtar parmak izi ve saklanan kontrol noktası |
| Kanıt ZIP dosyasının içeriği | `manifest.sig`, içerik dosyalarının hash değerlerini listeleyen kanonik manifestoyu imzalar | Manifestosu ve imzası dahil olmak üzere eksiksiz ZIP dosyası |
| Ekler korunur | İmzalı bir `media.saved` olayındaki SHA-256 ve bayt sayısı; imzalı ZIP manifestosundaki dosya hash değeri | Doğrulanmış ZIP dosyasının içindeki orijinal baytlar |
| Kontrol Noktası | Günlük uzunluğu, başlık hash değeri, açık anahtar ve oluşturulma zamanı üzerinde Ed25519 imzası | Tartışmalı bir değişiklikten önce saklanan bağımsız bir kopya |
| Çalıştırma makbuzu | Ayrı ayrı imzalanmış toplayıcı ölçümleri; ayrıca imzalanmış bir `process.started` olayına da dahil edilmiştir | Kayıt ve ilgili günlük; ölçümler kendi beyanlarına dayanmaktadır |
| Bağımsız CSV veya HTML | Tek başına kriptografik imza yoktur; olay hash'leri tek başına yetersizdir | Bütünlük kontrolü için doğrulanmış ZIP dosyasının içindeki metni aynen kullanın |
| Tarayıcı tarafından oluşturulan ekran görüntüleri, çıktılar veya PDF dosyaları | Türetilmiş sürümde TgWitness imzası bulunmamaktadır. | Orijinal doğrulanmış paketi saklayın ve türev sürümün nasıl oluşturulduğunu belgelendirin |

Toplayıcı, her dışa aktarım formatını oluşturmadan önce günlük imzalarını doğrular. Bu kaynak kontrolü, ayrı olarak indirilen CSV veya HTML dosyası üzerinde bir imza oluşturmaz. Geçerli bir JSONL olay imzası da ek baytlarını sağlamaz veya gözlemlenen günlüğün tamamının sağlandığını bağımsız olarak teyit etmez.

## Soruşturma devri

1. Vaka referansını, operatörü, sayısal Telegram hesap kimliğini, seçilen kaynakları, toplama politikasını ve toplama süresini vaka notlarınıza kaydedin. TgWitness gözlemleri korur; vaka ataması ve saklama kayıtları uygulama dışında yönetilir. [Canlı kabul](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)prosedürüyle amaçlanan toplama yapılandırmasını onaylayın.
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

Başarılı bir doğrulama, güvenilir toplayıcı anahtarı ve korunan sınırlarla ilgili bütünlüğü teyit eder. Kaynak doğruluğu, eksiksiz Telegram iletimi, güvenilir zaman bilgisi ve hukuki kabul edilebilirlik için ayrı kanıtlar gereklidir. Bu sürüm, canlı Telegram yeterlilik testini veya bağımsız bir adli/güvenlik değerlendirmesini henüz tamamlamamıştır.

Kopyalanan bir toplayıcı anahtarı, uydurulmuş bir yedek günlüğü imzalayabilir. Bağımsız olarak saklanan bir kontrol noktası veya tanık kaydıyla yapılan doğrulama, değiştirilmiş bir önceki önek tespit eder; sadece imza doğrulaması bunu yapamaz. Bir tanık, toplayıcının sunduğu verileri düzeltir; bu nedenle, ilk harici kontrol noktası öncesinde uydurulmuş kayıtların doğruluğunu bağımsız olarak teyit etmez. Bulut dağıtım raporları, yapılandırmayı ve toplayıcı tarafından bildirilen ölçümleri kontrol eder; ancak önyükleme sırasında özel anahtarın hiçbir zaman kopyalanmadığını teyit etmez.

Apprise aracılığıyla gönderilen bildirimler, çalışma alanı ve sohbet adlarını ve sayılarını içerir; silinen ve düzenlenmiş mesajların kısa alıntıları yalnızca operatör bu özelliği etkinleştirdiğinde eklenir (varsayılan olarak kapalıdır). Bunlar bir kolaylık işaretidir, kanıt değildir: teslimat garanti edilmez ve yalnızca günlük ile imzalı dışa aktarımları gözlemlenenleri kaydeder. Bir çalışma alanı proxy’si kullanıldığında bildirimler aynı yolu izler; bu yolu kullanamayan hizmetler ve MTProxy yolları reddedilir.

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

## Kapsam: süreklilik, boşluklar ve gözlemlenmemiş kimlikler

Her imzalı ZIP dosyası `coverage.json`'yi içerir; HTML raporu aynı özetle açılır ve `verify.py`, dosyaya güvenmek yerine `events.jsonl`'den bu özeti yeniden hesaplar:

- **X'ten Y'ye kadar sürekli olarak gözlemlenir.** Bir dönem `observation.started` ile başlar ve bir duraklama, bir durdurma, Telegram bağlantısının kesilmesi, oturumdan çıkış, düzgün bir durdurma olmaksızın başlayan bir işlem veya gözlem sırasında herhangi bir kayıt olmaksızın üç dakikadan fazla süren bir süre ile (her dakika bir kalp atışı kaydı yazılır; bu nedenle sessizlik, işlemin durduğu, donduğu veya bilgisayarın uyku moduna geçtiği anlamına gelir). **Parametreler** bölümünde kalp atışı aralığı değiştirildiğinde, her kalp atışı bu değişikliği kaydeder ve izin verilen sessizlik süresi üç aralığa çıkar; bu süre asla üç dakikadan az olamaz.
- **Boşluklar,** dönemler arasındaki süreyi ve nedenini listeler. Son kayıtta hâlâ açık olan bir boşluk, `not_resumed_by_last_record` olarak işaretlenir.
- **Mesaj kimlikleri gözlemlenmemiştir.** Sohbet başına mesaj sayısını belirleyen kanallar ve süper gruplar için gözlemlenen kimlikler arasındaki eksik kimlikler aralıklar halinde listelenmiştir. Bunlar, *"gözlemlenmemiş*" — silinmiş, hiç teslim edilmemiş veya kaydedilmiş geçmişin dışında — olarak rapor edilir; asla "silinmiş" olarak rapor edilmez. Özel sohbetler ve normal gruplar hesap genelinde ortak bir sıra numarası kullanır; bu nedenle buradaki boşluklar anlam ifade etmez ve listelenmez.
- Sohbet düzeyindeki boşluk bildirimleri (örneğin, Telegram'ın bir kanalda farkın telafi edilmesini istemesi gibi) not olarak sayılır; bunlar genel kapsamı kesintiye uğratmaz.

Kapsam, bu toplayıcının neyi kaydettiğini açıklar. Bu, Telegram'ın sürekli bir süre boyunca her güncellemeyi ilettiğinin kanıtı değildir.

## Yapımcı

İmzalı kanıt ZIP dosyaları, sohbet dışa aktarımları, tanık günlükleri ve kişi profili dosyalarının beyanı, `producer` bilgilerini içerir: yazılım, sürüm, proje (PhishDestroy), ana sayfa ve kaynak deposu. HTML raporu aynı satırı gösterir ve `verify.py` , bunu doğruladığı bilgilerin bir parçası olarak yazdırır. Bu alan oluşturulmadan önce oluşturulan arşivler, önceki gibi doğrulanır ve üretici adı belirtilmemiş olarak raporlanır.

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

Doğrulama kodunu, güvenilir bir kaynak veya incelenmiş bağımsız bir kopyadan edinin. Güvenilmeyen bir arşivin içindeki doğrulama kodu, o arşivin yazarı tarafından sağlanan çalıştırılabilir bir materyaldir; varlığı, taşınabilirlik açısından bir kolaylıktır, bağımsız bir güven kaynağı değildir.

Bir kontrol noktası, açık anahtar, günlük uzunluğu, başlık hash'i ve oluşturulma zamanını içeren bir beyanı imzalar. Doğrulayıcı, daha sonraki bir arşivin aynı önek içerdiğini kontrol edebilir. Tartışmalı bir değişiklikten önce, toplayıcının dışında bir kontrol noktası saklayın: hem arşivi hem de kontrol noktasını kontrol eden bir saldırgan, her ikisini de değiştirebilir.

Sabitlenmemiş bir anahtardan alınan geçerli bir imza, yalnızca iç tutarlılığı sağlar. Kayıt öncesinde veri toplayıcı veya anahtarın güvenliği ihlal edilmişse, sabitlenmiş bir anahtar bile kaynak içeriğinin doğruluğunu kanıtlayamaz. Harici zaman damgası ve güvenilir yakalama, ayrı gerekliliklerdir. TgWitness, delil kabul edilebilirliği veya adli sertifikasyon vaat etmez.

## Ekler

Dosyalar, media/ dizininde SHA-256 ile tanımlanır. Bir media.saved olayı, bir hash değerini ve bayt uzunluğunu belirli bir mesaj olayına bağlar. Ham dosya adları meta verilerdir, asla yerel yollar değildir. Medya baytları eşzamansız olarak indirilir; bu nedenle anında silme işlemi, yakalamayı engelleyebilir. Devre dışı bırakılmış toplama, aşırı büyük/boyutu bilinmeyen dosyalar, indirme hataları ve kesintiye uğrayan indirmeler sonuçlar olarak görüntülenir. Bir işlem çökmesi, referanssız kısmi dosyalar bırakabilir; bunlar dışa aktarımlara dahil edilmez.

ZIP dışa aktarıcısı, depolanan medya dosyalarını adlarına göre doğrular. JSONL, CSV ve HTML dışa aktarımları olay imzalarını doğrular ancak medya baytlarını içermez. Türetilmiş raporlar kolaylık sağlar; events.jsonl dosyası, olayların resmi temsilidir.

## Kalıcı toplama ve işlem makbuzları (0.2)

Bir medya işi ve ilgili mesaj olayı, tek bir işlemde kaydedilir. İş, orijinal TL mesaj tanımlayıcısını depolar; imzalı gözlem, SHA-256 değerini, hesabı ve boyut politikasını bağlar. Kurtarma işlemi, indirme öncesinde bu bağlamayı doğrular. Asla mevcut mesajı almaz ve sessizce daha yeni bir eki ikame eder. Kesintiye uğrayan işler yeniden denenirken, kalıcı hata açık bir sonuç olarak kalır.

Her çalışma alanının kendi günlüğü ve imzalama kimliği vardır. Bir process.started olayı şunları içerir: çalıştırma kimliği, yerel saatler, bağımlılık sürümleri, kaynak dosya hash'leri, başlangıç hesabı/kapsamı ve yakalama ayarları. Heartbeat'ler çalıştırma kimliğini, monotonik zamanı ve kuyruk durumunu içerir. İşlem makbuzu, ayrı olarak imzalanmış bir beyan olarak da indirilebilir. Dosya ölçümleri kendi beyanına dayalıdır ve güvenilir donanım doğrulaması değildir.

Otomatik kontrol noktaları, başlangıçta, gözlem sırasında her beş dakikada bir (**Parametreler → Her [süre] imzalı kontrol noktası**) ve düzgün bir şekilde durdurulduğunda yerel olarak saklanır. Başlangıç doğrulaması ve dışa aktarma işlemi sırasında günlük, saklanan en son yerel kontrol noktasıyla karşılaştırılır. Bu, kontrol noktası kaybolmadığında bir veritabanı geri alma işlemini tespit edebilir; her ikisini de kontrol eden bir operatör, yine de her ikisini de değiştirebilir. Bağımsız saklama ve harici güvenilir zaman damgaları ayrı gereksinimler olarak kalır.

Yeniden başlatmanın ardından, kaydedilmiş Telegram güncelleme konumu devam ettirilir (`catch_up_from`'den `observation.started`'ye) ve kaçırılan güncellemeler istenir. Periyodik bir yeniden kontrol, kaçırılan mesajlar için `message.recovered`'yi ve Telegram'ın artık kaydedilmiş bir mesajı döndürmemesi durumunda `message.missing_on_recheck`'yi kaydeder; ikincisi bir silme bildirimi değildir ve silen kişinin adını veya zamanı belirtmez.

### Site dışı yedekleme ve geri yükleme (S3)

Site dışı kopya (Dışa Aktarımlar, varsayılan olarak kapalı), günlük bölümlerini, korunan dosyaları, kontrol noktalarını zaman damgalarıyla birlikte ve tamamlanmış sohbet dışa aktarımlarını, çalışma alanı kasasında saklanan bir anahtarla AES-256-GCM ile şifrelenir; depolama kovası bunu desteklediğinde Object Lock saklama kuralı geçerlidir. İndirilmiş anahtar olmadan kopya okunamaz. Geri yükleme ve doğrulama işlemleri `python -m tgwitness.replica restore --key-file KEY.json --out DIR` ile gerçekleştirilir.

Geri yükleme işlemi için boş bir normal dizin gereklidir. İndirilen ve şifresi çözülmüş nesneler, tüm günlük ve saklanan her kontrol noktası doğrulanana kadar özel geçici depolama alanında kalır. Güvenli olmayan nesne yolları, tutarsız segment aralıkları ve bir kontrol noktasından daha kısa günlükler reddedilir; başarısız doğrulama durumunda geri yüklenen dosya yayınlanmaz. Saklama kontrolleri, geri döndürülen Nesne Kilidi modunu ve tarihini, yükleme sırasında gönderilen son tarihle karşılaştırır (bir saniyelik yuvarlama toleransı). Süresi dolmuş, geçersiz veya kısaltılmış son tarihler doğrulanmış olarak kabul edilmez. Durum raporu, o yükleme geçişi için saklama süresi okunan örnek nesneyi bildirir.

Kopyalama işlemi, hedef konum ve şifreleme anahtarı ile sınırlıdır. Uç nokta, depolama alanı veya önek değiştirildiğinde, yerel olarak saklanan günlük, medya ve kontrol noktalarının söz konusu hedefe tam bir kopyası oluşturulur. Eski, kapsam dışı işlemler korunur ancak yükseltme sonrasında bir kez yeniden oynatılır. Yerel giden kutusundan zaten kaldırılmış olan geçmiş sohbet dışa aktarımları, önceki hedef konumlarında kalır.

Eksik veya bozuk yerel medya, geçiş hatası olarak rapor edilir ve medya imleci bunun önünde tutulur, böylece dosya bir sonraki geçişte tekrar denenir; bundan sonraki dosyalar, kontrol noktaları ve dışa aktarımlar yine de kopyalanır. Geri yükleme, şifresi çözülmüş hash değerleri ve kaydedilen boyutlara göre tüm korunmuş medya referanslarını kontrol eder. Kesintiye uğrayan yüklemelerden kaynaklanan aynı çakışan günlük segmentleri tekilleştirilir; çakışan kısımlar reddedilir. Yükleme sırasında oluşturulan kontrol noktaları, kapsadıkları günlük kayıtları kopyalanana kadar ertelenir; böylece tamamlanan bir geçiş, kontrol noktasını günlükten önce yayınlamaz.

### Akış halinde dışa aktarma anlık görüntüleri

Akışlı dışa aktarımlar, kararlı bir SQLite okuma anlık görüntüsü kullanır. İndirme işlemi tamamlandığında, bu anlık görüntünün başlangıcı mevcut canlı günlüğünden daha eski olabilir. Bu anlık görüntünün ardından oluşturulan bir kontrol noktası, arşivin daha kısa olduğunu doğru bir şekilde bildirebilir; bunu, dışa aktarılan önekle aynı veya ondan önceki bir kontrol noktasıyla karşılaştırın, keyfi olarak daha sonraki bir kontrol noktasıyla değil.

## RFC 3161 hazırlığı ve yanıt doğrulaması (0.2)

Kanıt modu (varsayılan olarak kapalı), her bir imzalı kontrol noktasının yalnızca SHA-256 değerini, çalışma alanı rotası üzerinden ve asla MTProxy üzerinden değil, listelenen RFC 3161 yetkililerine ve OpenTimestamps takvimlerine gönderir. Yanıtlar `checkpoints/anchors/`'de saklanır, dışa aktarılır ve `verify.py` tarafından kontrol edilir (`--tsa-ca`, TSA imzasını kontrol eder; OpenTimestamps kanıtlarını `ots upgrade` ve `ots verify` ile doğrular).

Panel, kanonik checkpoint.json baytlarını, timestamp.tsq dosyasında yer alan SHA-256 mesaj parmak izini ve rastgele nonce değerini, sağlama toplamlarını ve talimatları içeren bir istek arşivi hazırlar. Herhangi bir ağ isteği yapılmaz. Hazırlanan dosya, güvenilir bir zaman damgası değildir.

`python -m tgwitness.anchor verify`, OpenSSL ts'yi iki kez çağırır: bir kez kontrol noktası baytlarına karşı, bir kez de orijinal isteğe karşı. Güvenilir bir CA dosyası açıkça gereklidir; dahil edilen sertifikalara otomatik olarak güvenilmez. İstek kontrolü, komut satırında isteğe bağlıdır; bu nedenle, nonce'yi kontrol etmek için --request seçeneğini koruyun ve sağlayın. Sonuç, kontrolün yapılıp yapılmadığını belirtir. Toplayıcı kontrol noktası imzası ve günlüğü, yine de güvenilir toplayıcı parmak izi ile ayrı olarak doğrulanmalıdır.

Mevcut doğrulayıcı, iptal bilgilerini almamakta ve sertifikanın geçerlilik süresinin dolmasından sonra uzun vadeli arşiv doğrulamasını uygulamamaktadır. Başarılı imza doğrulamasını, nitelikli zaman damgası veya hukuki kabul edilebilirlikle eşdeğer görmeyiniz. Geliştirme sürecinde gerçek bir bağımsız TSA ile iletişime geçilmemiştir. [Prosedüre](https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/) bakınız.
