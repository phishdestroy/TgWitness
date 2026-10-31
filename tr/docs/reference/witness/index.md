# Bağımsız tanık

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/witness/

Kendi anahtarı ve botu olan bir tanık çalıştırın, imzalı kontrol noktalarını bir kanala yayınlayın ve dışa aktarımları bu kontrol noktalarıyla karşılaştırarak doğrulayın.

[Rusça bot ve proxy ayarları](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Bir toplayıcı kendi günlüğünü imzalar; bu nedenle, toplayıcıyı ve anahtarını kontrol eden kişi, prensip olarak günlüğü yeniden yazabilir veya kısaltabilir ve tekrar imzalayabilir. Bir tanık, bunu tespit edilebilir hale getirir. Bu, ayrı bir işlemdir — başka bir konteyner ya da daha doğrusu başka birinin işlettiği bir sunucu — ve birkaç dakikada bir toplayıcının imzalı günlük başlığını alır, gördüklerini kendi anahtarıyla imzalar, kendi günlüğünde saklar ve bir Telegram kanalına gönderir.

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

Token, panelin **Witness** sayfasında oluşturulur, bir kez gösterilir ve yalnızca SHA-256 olarak saklanır. Tam olarak bir uç nokta açar: `GET /api/witness/head`; bu uç nokta, yeni imzalanmış bir kontrol noktası ile imzalanmış, içerik içermeyen toplama sayaçları ve operasyonel durum bilgisini döndürür. Panel açamaz, mesaj içeriğini okuyamaz veya ayarları değiştiremez ve panel jetonu burada kabul edilmez. Aynı sayfadan bir jetonu iptal edebilirsiniz. Toplayıcı, yeni bir tanık anahtarının (`witness.seen`) ne zaman kontrol etmeye başladığını kaydeder ve jeton başına son kontrolü gösterir; 2,5 aralık içinde kontrol yapılmayan bir tanık, gecikmiş olarak işaretlenir.

Yeni tanıklar her oylamada rastgele bir doğrulama mesajı gönderir; yakalama ifadesi bunu toplayıcı imzası altında yineler. Sayaçlar tam kontrol noktasına bağlıdır ve imzalı tanık gönderilerine dahil edilir. Eski başlıklar bağımsız tanık tarafından kabul edilmeye devam eder. Günlüğün büyümesi tek başına asla yeni bir mesaj olarak sayılmaz.

## Neleri kontrol eder ve kaydeder?

Her aralıkta (varsayılan olarak 10 dakikada bir) TgWitness:

1. başlığı kendisi alır (toplayıcı bunu zorlayamaz veya atlayamaz);
2. toplayıcının imzasını, sabitlenmiş toplayıcı anahtarını (`--collector-fingerprint`, veya görülen ilk anahtar), azalmayan bir sayımı ve değişmemiş bir sayımda değişmemiş bir başlığı doğrular;
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

**Ekstra'ları** açın **→ Kanalınızdaki bir bot →** Panelde **bir bot kurun** . Üç adımda salt okunur erişim, kanalınız ve aralık ayarlarını yapın, ardından tanık botunu başlatın. Yayın politikası, isteğe bağlı HTTP/SOCKS5 proxy ve özel Bot API adresi **Gelişmiş ayarlar** altında bulunur. Form, bu çalışma alanının sabitlenmiş toplayıcı anahtarıyla birlikte `witness.json` dosyasını indirir. Yeni oluşturulan salt okunur jetonu "**Erişim dosyasını**`witness-token.txt` olarak **kaydet** " seçeneğiyle indirin; bunu ve tanık sunucusunda oluşturulan `bot-token.txt` dosyasını o JSON dosyasının yanına yerleştirin. Toplayıcı, bot jetonunu asla almaz. İndirme işlemi bir hizmeti başlatmaz veya mesaj yayınlamaz. Barındırılan proje tanığı örtük olarak kaydedilmez.

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

Toplayıcı adresi, tokenlar ve kanal, `--collector`, `--token` veya `--token-file`, `--bot-token` veya `--bot-token-file` ve `--channel`, ya da `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` ve `_CHANNEL`'den gelir; bu sayede gizli bilgiler işlem listesinin dışında tutulur.

Bir yapılandırma dosyası, alt çizgi içeren seçenek adlarının yanı sıra, kanal gönderilerindeki kelimelerin yerine geçen `texts`'yi kullanır:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts` anahtarları: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Komut satırı ortamdan, ortam ise dosyadan önceliklidir. Bilinmeyen seçenekler veya metin anahtarları, göz ardı edilmeyip bir mesajla tanık işlemini durdurur. İfade biçimi doğrulamayı asla etkilemez: verify.py, her gönderimin sonunda imzalı belirteci kontrol eder. `--post changes` veya `problems` ile, gönderilmemiş kontroller yine de tanık günlüğünde yer alır ve `verify.py` bunları hiç gönderilmemiş olarak listeler; başlangıç kaydı politikayı belirtir. Her kontrol yine de günlüğünde görünür, bu nedenle daha az gönderi, daha az bağımsız Telegram zamanı anlamına gelir, daha az kontrol anlamına gelmez.

Kanal olmasa bile tanık, günlüğünü tutmaya devam eder. Tanık anahtarının parmak izini (`python -m tgwitness.witness fingerprint`) başka bir yerde saklayın.

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

Bu işaret, sağlanan ve sabitlenmiş tanık kayıtlarıyla tutarlılığı sağlar. Operatör, yine de tanığın bağımsızlığını teyit etmeli ve kayıtlarını ayrı olarak muhafaza etmelidir. Bu, mesajların doğruluğunu, eksiksiz bir toplama işlemini veya bağımsız olarak ölçülmüş bir çalışma süresini garanti etmez.

Bir tanık, toplayıcının o anlarda neyi rapor ettiğini ve daha sonraki dışa aktarımların bununla uyumlu olduğunu gösterir. Toplayıcının Telegram'ın ilettiği her şeyi kaydettiğini veya mesaj içeriğinin doğru olduğunu göstermez. Aynı operatör tarafından aynı makinede çalıştırılan bir tanık, başka biri tarafından çalıştırılan bir tanığa göre daha zayıftır.

Sadece sayı artışı, çevrimiçi ortamda yalnızca ekleme yapılabilen bir sürekliliği kanıtlayamaz: çevrimdışı karşılaştırmada, saklanan her önek hash değeri, toplayıcının tam dışa aktarımıyla eşleşmelidir. Witness'ın hizmet dışı kalma süreleri ve başarısız yayınlar, aralıklarda harici referans noktalarının bulunmamasına neden olur. Eksik gönderiler, saklanan bir Witness günlüğüne göre bildirilebilir; ne bir kanal ne de aynı operatör tarafından kontrol edilen bir sunucu, değiştirilemez bir üçüncü taraf arşivi değildir.
