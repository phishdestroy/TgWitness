# Bağımsız tanık

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/

Kendi anahtarı ve botu olan bir tanık çalıştırın, imzalı kontrol noktalarını bir kanala yayınlayın ve dışa aktarımları bu kontrol noktalarıyla karşılaştırarak doğrulayın.

[Dışa aktarma ve doğrulama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) · [Yüksek güvenilirlik](https://phishdestroy.github.io/TgWitness/tr/docs/reference/high-assurance/) · [Panel kılavuzu](https://phishdestroy.github.io/TgWitness/tr/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

Akış şeması · Toplayıcı → Witness (imzalı kontrol noktası: kayıt sayısı + başlık hash'i); Witness → Witness günlüğü, özel anahtar; Witness → Telegram kanalı (kendi botu aracılığıyla imzalanmış gönderi); Kanıt ZIP dosyası → verify.py; Witness günlüğü, özel anahtar → verify.py; Telegram kanalı → verify.py (Telegram Desktop dışa aktarma veya t.me/s sayfası) · Toplayıcı · Witness · Witness günlüğü, özelanahtar · Telegram kanalı · Kanıt ZIP dosyası · verify.py · imzalı kontrol noktası: · kayıt sayısı + başlık hash'i · kendi botu aracılığıyla · imzalanmış gönderi · Telegram Desktop dışa · aktarma veya t.me/s sayfası

**Diyagramın metin olarak gösterimi**

1. Toplayıcı → Witness (imzalı kontrol noktası: kayıt sayısı + başlık hash'i)
2. Witness → Witness günlüğü, özel anahtar
3. Witness → Telegram kanalı (kendi botu aracılığıyla imzalanmış gönderi)
4. Kanıt ZIP dosyası → verify.py
5. Witness günlüğü, özel anahtar → verify.py
6. Telegram kanalı → verify.py (Telegram Desktop dışa aktarma veya t.me/s sayfası)

## TgWitness'in sundukları ve sunmadıkları

| Tanık şunlara sahiptir: | Tanık hiçbir zaman |
| --- | --- |
| Bir çalışma alanı için salt okunur **tanık jetonu** | Toplayıcının Telegram oturumu veya API kimlik bilgileri |
| Kendi Ed25519 anahtarı ve günlüğü | Toplayıcının kasası, imzalama anahtarı veya panel jetonu |
| Kendi Telegram bot jetonu | Mesaj içeriği: başlıkta kayıt sayısı ve bir hash yer alır |

Token, **Extras → Independent witness** bölümünde oluşturulur, bir kez gösterilir ve yalnızca SHA-256 olarak saklanır. Tam olarak tek bir uç noktayı açar; `GET /api/witness/head`; bu uç nokta, yeni imzalanmış bir kontrol noktası ile imzalanmış, içerik içermeyen toplama sayaçları ve operasyonel durum bilgisini döndürür. Paneli açamaz, mesaj içeriğini okuyamaz veya ayarları değiştiremez; ayrıca panel jetonu burada kabul edilmez. Aynı sayfadan bir jetonu iptal edebilirsiniz. Toplayıcı, yeni bir tanık anahtarının ne zaman kontrol etmeye başladığını kaydeder (`witness.seen`) ve jeton başına son kontrolü gösterir; 2,5 aralık içinde kontrol yapmamış bir tanık, gecikmiş olarak işaretlenir.

Yeni tanıklar her oylamada rastgele bir doğrulama mesajı gönderir; yakalama ifadesi bunu toplayıcı imzası altında yineler. Sayaçlar tam kontrol noktasına bağlıdır ve imzalı tanık gönderilerine dahil edilir. Eski başlıklar bağımsız tanık tarafından kabul edilmeye devam eder. Günlüğün büyümesi tek başına asla yeni bir mesaj olarak sayılmaz.

## Neleri kontrol eder ve kaydeder?

Her aralıkta (varsayılan olarak 10 dakikada bir) TgWitness:

1. başlığı kendisi alır (toplayıcı bunu zorlayamaz veya atlayamaz);
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
3. kendi günlüğüne imzalı bir kayıt ekler: `witness.anchor`, durumu `ok`, `key_changed`, `rollback` (öncekinden daha az kayıt), `fork` (aynı uzunlukta, farklı başlık) veya `invalid` (yanıt doğrulamayı geçemedi) ya da `witness.no_response` (toplayıcı yanıt vermediğinde);
4. Witness çalışırken ve Bot API'ye erişebiliyorken, sonucu "cevap yok" dahil olmak üzere imzalı olarak kanala gönderir. Gönderi kimliği kaydedilir (`witness.posted`), başarısız bir gönderi de kaydedilir (`witness.post_failed`).

Bir gönderi şu şekilde görünür; son satırda imzalı beyan yer alır:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Witness'ı çalıştırın

Bir Telegram botuna (@BotFather ile oluşturabilirsiniz), bu botun yönetici olduğu bir kanala ve tanık tarafından erişilebilir bir toplayıcı adresine ihtiyacınız vardır — özel ağın dışında HTTPS üzerinden ([kurulum](https://phishdestroy.github.io/TgWitness/tr/docs/reference/deployment/) bölümündeki HTTPS profiline bakın).

Panelde **Ekstralar → Bağımsız tanık → Yapılandır** öğesini açın. Üç adımda salt okunur erişim, kanalınız ve aralık ayarlarını yapıp tanığı başlatabilirsiniz. Yayın politikası, isteğe bağlı HTTP/SOCKS5 proxy ve özel Bot API adresi **Gelişmiş ayarlar** öğesinin altındadır. Form, bu çalışma alanının toplayıcı anahtarı sabitlenmiş olarak `witness.json` bu çalışma alanının toplayıcı anahtarı sabitlenmiş olarak indirilir. Yeni oluşturulan salt okunur jetonu **Erişim dosyasını kaydet** ile `witness-token.txt`; bunu ve `bot-token.txt`tanık sunucusunda oluşturulan bu JSON'un yanına yerleştirin. Toplayıcı, bot jetonunu asla almaz. İndirme işlemi bir hizmeti başlatmaz veya bir mesaj yayınlamaz. Barındırılan hiçbir proje tanığı zımnen kaydedilmez.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

İlk komut, ağ isteği veya anahtar oluşturma gerektirmeden yapılandırma ve gizli dosyaları kontrol eder. JSON'daki yollar o dosyaya göredir; CLI/ortam yolları ise çalışma dizinine göredir. Tanık parmak izini barındırıcı dışındaki bir yerde saklayın. Toplayıcının son sorgulama göstergesi yalnızca bir isteği onaylar; yayınlama işlemi Proof tarafından bildirilir veya tanık günlüğü ve kanalında kontrol edilir.

Panel bir SSH tünelinin arkasında kalıyorsa, [bu Caddy örneğini](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example) kullanarak yalnızca kapsam dahilindeki tanık uç noktasını ayrı bir HTTPS ana bilgisayar adında açığa çıkarın. Varsayılan çalışma alanı `https://witness.example.org`'yi kullanır, diğer çalışma alanları ise `https://witness.example.org/profiles/ID`'yi kullanır. Jetonlar hâlâ gereklidir; panel ve diğer API yolları bu sanal ana bilgisayar tarafından yönlendirilmez.

Düzenli olarak yayınlanan kontrol noktaları için `all`'yi seçin. Beş dakikalık aralık, her çalışma alanı başına günde yaklaşık 288 gönderi anlamına gelir. `changes`/`problems`, bazı kontrolleri kasıtlı olarak yayınlamaz. MTProxy, toplayıcının Telegram istemcisi içindir. Witness HTTP yoklaması ve Telegram’ın HTTPS Bot API’si kendi doğrudan/HTTP/SOCKS5 rotasını ([Bot API](https://core.telegram.org/bots/api)) kullanır.

**Toplayıcının yanında, Docker ile** (aynı ana bilgisayar — bağımsız işlem ve anahtar, ancak aynı operatör): değerleri `.env`'ye girin ve profili başlatın.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

Yayınlanan bir görsel kullanıldığında `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d` kodunu kullanın.

**Başka birinin sunucusunda** (gerçek bir bağımsız tanık): depoyu oraya kopyalayın, `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org`'yi ve yukarıdaki üç değeri `.env`'ye ayarlayın, ardından

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

veya Docker olmadan:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Discord'da yayınla

Bir tanık, Telegram yerine bir Discord kanalına gönderi paylaşabilir. Discord’da **Kanal Düzenle → Entegrasyonlar → Webhook’lar’ı** açın, bir webhook oluşturun ve URL’sini kopyalayın. Panelde, 2. adımda **Discord webhook · kanalınız’ı** seçin. Tanık sunucusunda, URL’yi `discord-webhook.txt` yanına `witness.json`; bu URL asla toplayıcıya ulaşmaz.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Bir tanığın tek bir yayıncısı vardır: ya bir Telegram kanalı ya da bir Discord webhook'u; ikisi birden olamaz. Gönderiler aynı imzalı beyanı içerir ve kimseye ping atamaz. Discord'un 2.000 karakter sınırını aşan bir gönderi, tam kontrolün `witness-check.txt`. Her gönderi kimliği, `witness.posted`. `verify.py --channel`sadece Telegram kanalının dışa aktarımlarını okur; bu nedenle Discord için tanık günlüğünü saklayın: bu günlük her kontrolü içerir.

### Seçenekler

| Seçenek | Ortam | Varsayılan | Anlam |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Kontroller arasındaki süre, 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | Toplayıcı ve Bot API'sinin yanıt vermesi için bekleme süresi: 5–600 saniye |
| `--post` | `_POST` | `all` | `all`: her kontrol; `changes`: yeni bir başlık veya bir sorun; `problems`: sadece sorunlar ve eksik cevaplar |
| `--title` | `_TITLE` | `TgWitness witness` | Her kanal gönderisinin ilk kelimeleri |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | İlk cevaba güvenmek yerine toplayıcı anahtarını sabitleyin |
| `--proxy` | `_PROXY` | doğrudan | `socks5://host:port` veya `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Bot API adresi, örneğin yerel bir Bot API sunucusu |
| `--data-dir` | `_DATA` | `witness-data` | Tanık anahtarı ve günlüğü |
| `--config` | `_CONFIG` | – | Yukarıdaki seçeneklerden herhangi birini içeren JSON dosyası |

Toplayıcı adresi, jetonlar ve kanal `--collector`, `--token` veya `--token-file`, `--bot-token` veya `--bot-token-file`, `--discord-webhook-file` ve `--channel`, veya `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` ve `_CHANNEL`, bu da gizli öğeleri işlem listesinden uzak tutar.

Bir yapılandırma dosyası, alt çizgi içeren seçenek adlarının yanı sıra, kanal gönderilerindeki kelimelerin yerine geçen `texts`'yi kullanır:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts` anahtarları: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Komut satırı ortamdan, ortam ise dosyadan önceliklidir. Bilinmeyen seçenekler veya metin anahtarları, göz ardı edilmeyip bir mesajla tanık işlemini durdurur. İfade biçimi doğrulamayı asla etkilemez: verify.py, her gönderimin sonunda imzalı belirteci kontrol eder. `--post changes` veya `problems` ile, gönderilmemiş kontroller yine de tanık günlüğünde yer alır ve `verify.py` bunları hiç gönderilmemiş olarak listeler; başlangıç kaydı politikayı belirtir. Her kontrol yine de günlüğünde görünür, bu nedenle daha az gönderi, daha az bağımsız Telegram zamanı anlamına gelir, daha az kontrol anlamına gelmez.

Kanal olmasa bile tanık, günlüğünü tutmaya devam eder. Tanık anahtarının parmak izini (`python -m tgwitness.witness fingerprint`) başka bir yerde saklayın.

## Çeşitli çalışma alanları için herkese açık kanıt sayfası

`python -m tgwitness.proof` Aynı anda en fazla 32 çalışma alanını izler ve her birinin en son imzalanmış kontrolünü içeren, salt okunur bir sayfa sunar. Her çalışma alanı, veri klasörü altında kendine ait bir tanık anahtarı ve günlüğü ile sabitlenmiş bir toplayıcı anahtarı alır; bir Telegram kanalına gönderim, çalışma alanı başına isteğe bağlıdır. Şu dosyadan başlayın: [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Alan | Anlam |
| --- | --- |
| `title` | Sayfa başlığı, 1–100 karakter |
| `data_dir` | Dosyaya ilişkin Witness anahtarları ve günlükleri; varsayılan `proof-data` |
| `interval`, `timeout` | Kontroller arasındaki süre (1–1440 dakika, varsayılan 5); bekleme süresi (5–600 saniye, varsayılan 20) |
| `workspaces[].id`, `label` | Kısa küçük harfli takma ad ve gösterilen ad |
| `workspaces[].collector` | Toplayıcı adresi; diğer çalışma alanlarının sonu `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Zorunlu, her çalışma alanı için farklıdır |
| `workspaces[].token_file` | Bu çalışma alanının salt okunur tanık jetonunu içeren dosya |
| `workspaces[].channel`, `bot_token_file` | İsteğe bağlı, birlikte: her kontrolü bir kanala gönderin |
| `workspaces[].proxy`, `bot_api` | İsteğe bağlı rota ve Bot API adresi |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

İlk komut, bağlantı kurmadan dosyayı ve token dosyalarını doğrular. Sayfa yalnızca GET ve HEAD isteklerine yanıt verir:

- `/` Tüm çalışma alanlarını gösterir; 2,5 aralık boyunca kontrol edilmeyen bir çalışma alanı, güncel olmayan olarak işaretlenir.
- `/api/proof` JSON ile aynı sonucu döndürür.
- `/api/proof/<id>` en son imzalanmış beyanı indirir (`tgwitness-public-proof-v1`): tanık kayıt numarası ve hash değeri, durum, sabitlenmiş toplayıcı anahtarı, kontrol noktası, toplama sayıcıları ve kanal gönderisinin başarılı olup olmadığı; söz konusu çalışma alanının tanık anahtarıyla imzalanmış.
- `/healthz` Bir çalışma alanının monitörü durduğunda 503 hatası verir.

Sayfaya, [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example) örneğindeki gibi kendine ait bir ana bilgisayar adı verin. Doğrulama için, bir çalışma alanının tanık günlüğünü `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` dışa aktarın ve aşağıda açıklandığı gibi kullanın.

## Doğrula

Tanık tarafında, günlüğünü dışa aktarın:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Ardından, herhangi bir yerden, toplayıcının imzalı ZIP dosyası ve Telegram Desktop'tan dışa aktarılan kanal (*Sohbet geçmişini dışa aktar* → JSON, `result.json` verir) veya kamuya açık `https://t.me/s/…` sayfası ile:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py`, tanık günlüğünü (zincir ve imzalar) kontrol eder, ardından **tanığın gördüğü her başlığın dışa aktarılan günlüğün bir parçası olup olmadığını** doğrular: o sayımdaki kaydın tam olarak o hash değerine sahip olması gerekir. Eşleşmeyen bir başlık doğrulamayı geçemez — bu durumda günlüğün, tanık tarafından görüldükten sonra değiştirildiği anlaşılır. Ayrıca, dışa aktarımdan sonra görülen başlıkları, tanığın kaydettiği anormallikleri, başarısız olan yanıtları, eşleşen kontrol noktalarının bu dışa aktarımda mevcut olduğu dönemleri (“X’ten Y’ye kadar tanıklandı”) ve boşlukları rapor eder. Daha sonraki kontrol noktaları bu dönemleri uzatmaz. Sonuç, en son eşleşen kayıt numarasını ve eşleşen kontrol noktası olmayan sonraki kayıtların sayısını içerir. Yalnızca dışa aktarmanın kendi anahtarıyla imzalanmış yanıtlar sayılır: tanığın hiç görmediği bir anahtarla imzalanmış bir dışa aktarım, tanıklanmamış olarak rapor edilir ve `--fingerprint` olmadan imzalayanın sabitlenmesi gerçekleşmez. `--channel` ile imzalanmış her gönderi, tanık günlüğüyle kayıt kaydı eşleşmelidir: değiştirilmiş gönderiler doğrulamadan geçemez, eksik gönderiler listelenir. Sağlanan bir Telegram JSON dışa aktarımındaki tarih, imzalanmış tanık belirtecinin dışında, düzenlenebilir bir meta veridir. Belirtecin eşleşmesi, yayın tarihini doğrulamaz; sonuç, yayın zamanı doğrulamasının yapılmadığını açıkça bildirir.

### Tanık eşliğinde dışa aktarma sınırı gerektirir

Tanıkların da yer aldığı bir nihai kayıt içermesi gereken bir devir teslim işlemi için `--require-witness`'yi ekleyin:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Bunun için bağımsız olarak saklanan tanık parmak izi ve bu dışa aktarımın tam sonunda bulunan eşleşen bir kontrol noktası gereklidir. Yalnızca daha önceki bir önekini kapsayan bir kontrol noktası yeterli değildir. Toplamayı duraklatın, tanığın son durumu gözlemlemesine izin verin ve günlüğe başka bir kayıt yapılmadan önce dışa aktarın; günlüğü değişirse, başka bir kontrol noktası saklayın ve o durumu dışa aktarın. Daha sonraki bir kontrol noktası tek başına, daha kısa bir dışa aktarımın son hash değerini doğrulayamaz. `--channel` da sağlandığında, eksik olduğu iddia edilen gönderiler veya boş bir eşleşme kümesi bu sıkı kontrolü geçemez. Bayrak olmadan, sıradan bütünlük kontrolleri, aksi takdirde sağlam olan bir arşivi reddetmeden tanıklanmamış kayıtları yine de rapor eder.

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
