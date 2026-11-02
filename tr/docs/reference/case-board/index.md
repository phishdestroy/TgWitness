# Case Board referansı

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-board/

Case Board tarafından kullanılan yer imleri, tam vurgu işaretleri, eylem dilimleri, tartışmalar, kapsamlı erişim ve imzalı açıklama geçmişi.

Case Board, soruşturma ekibine kaydedilen materyallerin paylaşımlı bir çalışma görünümünü sunar. Bir gözlemi yer imlerine ekleyin, belirli bir bölümü vurgulayın, bir dizi eylemi kaydedin ve bunları meslektaşlarınızla tartışın. Kartlar, kaynak referanslarını ve imzalı revizyon geçmişini korur. Ekip açıklamaları, çalışma alanında kalır ve orijinal Telegram gözlemlerinden ayrı olarak tanımlanabilir.

[Kanıt modeli](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/) · [Erişim](https://phishdestroy.github.io/TgWitness/tr/docs/reference/access/) · [Raporlar](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/) · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/CASE-BOARD.md)

![Sentetik soruşturma akışı](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## Bir vaka üzerinde çalışın

Standart veya Uzman modunda **Soruşturma → Case Board'u** açın. Dil, panele göre değişir. Bir günlük kaydının veya kaydedilmiş sohbet mesajının yanındaki **"To board**" seçeneğini kullanın ya da üzerine gelip **B tuşuna** basın. Yer imi tek bir tıklamayla Gelen Kutusu'na eklenir. Başlığını, etiketlerini ve notunu düzenleyin ya da bir koleksiyona taşıyın. Değiştirilen kart, imzalı bir revizyon ekler; kaldırıldığında geçmiş korunur.

İlk vaka için bir toplama seçin ve bir soruyu yanıtlayan kayıtları ekleyin. Yorumlar bölümünü kullanarak yorumu gözden geçirin, ardından **Sunum** **bölümünü** kullanarak kartları ve kaynak bağlamını inceleyin. Teslim edilecek dosyayı hazırlarken [Report Studio](https://phishdestroy.github.io/TgWitness/tr/docs/reference/case-reports/)'da Case Board materyalini ayrı olarak seçin. Bir dilimi kaydetmek, raporun veri filtrelerini otomatik olarak yapılandırmaz.

Kaydedilmiş bir sohbet mesajı içindeki metni seçerek **Vurgula → pano** seçeneğini açın. Rengini seçin ve bir not ekleyin. Sunucu, emoji, RTL metin ve birleştirme işaretleri dahil olmak üzere tam alıntıyı ve kaydedilmiş sürümü kontrol eder. Arayüz, maskelenmiş veya dönüştürülmüş metin üzerinden bir seçimi eşlemez.

Bir sohbetteki iki kaydı Shift tuşuna basarak tıklayın ve **aralarını kesitleyin**, **zamana göre kesitlemeyi** kullanın veya günlüğün mevcut sohbet, dönem ve olay türü filtrelerini kaydedin. Kaydedilen bir kesitin kendine özgü bir yargısı vardır: bunu Günlük'te açmak, birden fazla sohbeti, mesaj sayısı sınırlarını ve aktör filtrelerini de uygular. "**Yer iminden bu yana eklenen kayıtları göster" seçeneği,** daha sonra eklenenleri ayırır. Journal filtrelerini değiştirmek, dilimi kapatır. "Kişiler" bölümünden "**Bu kişinin eylemlerini dilimle**" seçeneği, kaydedilen aktör kimliğini kullanır; mesajın yazarının bir mesajı düzenlediğini, sildiğini veya tepki verdiğini varsaymaz.

Dilimleme iletişim kutusu, oluşturmaya izin vermeden önce sayıları önizler. "`all`" (tümü), anlık görüntüler, düzenlemeler, silme işlemleri, tepkiler, üyelik/hizmet güncellemeleri, kendi eylemler, düğmeler, medya çıktıları, kurtarılan mesajlar ve gelecekteki olay türleri dahil olmak üzere kaydedilen her tür öğeyi içerir. Seçim, kaydedilen gözlemleri tanımlar. Bilinmeyen sohbet silme bildirimleri ayrı bir bağlamda yer alır; yalnızca tüm çalışma alanına erişim hakkına sahip kullanıcılar tarafından görülebilir ve asla seçilen sohbetlerden birine atfedilmez.

Koleksiyonların tanımlanmış bir sohbet kapsamı vardır. Boş bir kapsam, tüm çalışma alanını ifade eder. Bir koleksiyon, kapsamının dışındaki kartları içerebilir; sohbetle sınırlı bir katılımcı, daha geniş bir koleksiyonu okuyamaz. Gelen Kutusu, atanmamış kartlar için sanal bir koleksiyondur. Arama ve filtreler yalnızca görünür kartları kapsar; ileti dizileri ve etiketlemeler, üst kartın erişim iznini devralır. Silinen yorumların tartışmada bir "mezar taşı" bulunur. Görüntüleme geçmişi kaydedilmez.

**Sunum**, seçilen koleksiyondaki tüm kartları açar; Kart, Kaynak bağlamı ve Ekip yorumları görünümleri ile klavyedeki Önceki/Sonraki kontrolleri bulunur. Düzenleme kontrolleri sunmaz. Normal akış sayfalandırılmıştır; sunum, listesini sayfalar halinde yükler ve her seferinde bir kartın ayrıntılarını getirir.

## İzinler

Tüm işlemler için `view`, çalışma alanı/sohbet kapsamı ve `board.read` yetkileri gereklidir. `board.write`, kart ekleme, yorum yapma, taşıma ve açma/inceleme durumlarını yönetir. `board.manage`, koleksiyon yönetimine, onaylanmış/reddedilmiş durumlara ve başkalarının kartlarının revizyonuna/silinmesine izin verir. Bir durum, kriptografik bir doğrulama sonucu değil, ekip kararıdır.

Form ön ayarlarına erişim: Gözden Geçiren = okuma; Analist = okuma/yazma; Operatör = okuma/yazma/yönetme, mevcut izinlerine ek olarak. Mevcut izinler, yeni hakları otomatik olarak kazandırmaz. Ana yönetici tüm haklara sahiptir ve "**Ana yönetici"** olarak yayın yapar. Atıf için adlandırılmış izinler kullanın. Bahsetmeler listesi, yalnızca üst kartın tamamını okuyabilen mevcut erişimleri gösterir.

A sohbeti için verilen bir yetki, A+B için kart veya dilim elde edemez; bunun için kimliğini tahmin etse veya yanlış bir `target.chat_id` sağlasa bile. Hedef meta verileri, sunucudaki imzalı olay hash'inden çözümlenir. Toplamalar, tartışma sayıları, ilgili kartlar ve canlı bildirimler yanıt vermeden önce filtrelenir. export işlemi için hem `export` hem de `board.read` yetkisi gerekir; panoya erişimi olmayan mevcut bir dışa aktarıcı, ekip notları içermeyen sıradan kanıt arşivini alır. SSE, her toplu işlemden önce mevcut izinleri yeniden kontrol eder.

## Saklanan sözleşmeler

Gözlemler gibi, açıklamalar da çalışma alanındaki yalnızca ekleme yapılabilen bir SQLite tablosuna işlem bazında yazılır. `annotations.jsonl`, `events.jsonl` ile aynı okuma anlık görüntüsünden elde edilen tam kanonik dışa aktarımdır. İkinci bir rakip açıklama deposu ve `board.activity` günlük olayı yoktur.

Her satırda tam olarak şunlar bulunmalıdır:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

Yukarıdaki kısaltılmış örnek, zarfı göstermektedir; gerçek yükler, model varsayılanlarını ve sunucu tarafından çözümlenen hedef alanlarını içerir. API istek şemaları, [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json) altında bulunur ve `python tools/build_board_schemas.py` tarafından çalışma zamanı Pydantic modellerinden oluşturulur. Ekstra istek alanları reddedilir. Kimlikler, eksik bırakıldığında sunucu tarafında oluşturulur. Yazar, zaman, anlık görüntü ve imza, çağıran tarafça sağlanamaz. Adlandırılmış izin kimlikleri, Access’in mevcut 16-hex biçimini izler; kart kimlikleri ise 32 hex’tir.

Kanonik JSON, UTF-8 formatındadır; nesne anahtarları sıralanmıştır, belirteçler arasında boşluk yoktur, Unicode kaçış karakteri kullanılmamıştır ve NaN/sonsuzluk değerleri yoktur. Açıklama hash'i, " `format: "tgwitness-annotations-v1"`" formatını ve `previous_hash`'e kadar olan yedi zarf alanını içeren kanonik nesnenin SHA-256 hash'idir. Bu format etiketi, hash alanını gözlemlerden ayırır. İmza, 32 ham hash baytı üzerinde Ed25519 ile oluşturulur. Sıra 1'den başlar. Revizyonlar kart kimliğini korur ve `supersedes` alanında önceki açıklama hash'ini belirtir; sohbet kapsamını değiştiremezler. Taşımalar, durumlar ve kaldırmalar ayrı kayıtlardır. SQLite tablosu UPDATE ve DELETE komutlarını reddeder.

`case-board.json` dosyası `{statement, signature}` öğelerini içerir. Kanonik ifade, çalışma alanı anahtarı ile imzalanır ve `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning` ve `state` öğelerini içerir. Durum, deterministik tekrar oynatma şeklindedir: `annotations_head`, sıralı bir `items` dizisi (koleksiyonlar, kartlar, tombstone'lar dahil yorumlar) ve `status_history`. Öğeler, revizyonlar boyunca son açıklama hash'ini, sırasını, yazarını ve zamanını, ayrıca orijinal oluşturucuyu ve oluşturulma zamanını korur. Yeniden oynatma, revizyonları, üst öğeleri, koleksiyon referanslarını ve yinelenen eylem kimliklerini kontrol eder. `manifest.json` ve yeni kontrol noktaları da `annotations_head`'i bağlar. Kopyalanmış bir imza anahtarıyla kesilme veya yeniden yazılmayı tespit etmek için bir kontrol noktasını bağımsız olarak saklayın.

### Metin sürümleri

`range.start`, sıfır tabanlı bir Unicode kod noktası ofsetidir; `length`, pozitif bir kod noktası sayısıdır ve `quote`, hedef olaydaki `payload.text` veya `payload.caption`'in tam alt dizesine eşit olmalıdır. NFC/NFKC, büyük/küçük harf dönüştürme veya grafem normalizasyonu uygulanmaz. Python dize dilimleri ve JavaScript’teki `Array.from(text)`, aynı indekslemeyi uygular. İşaretler ile ZWJ emojilerinin birleştirilmesi birkaç kod noktası kaplayabilir. `range.version`, mevcut mesaj sürümü veya Telegram’ın UTF-16 varlık ofseti değil, hedef olay hash’idir. Sonradan yapılan düzenlemeler, bir vurguyu asla otomatik olarak başka bir yere taşımaz.

### Kimlik ve zaman dilimlerini ayırın

`query`, tam olarak bir `chat_id` veya boş olmayan `chat_ids`'leri, isteğe bağlı `from`/`to` aralığını, mesaj-ID sınırlarını (yalnızca bir sohbet), `kinds: "all"` veya tam/önekli joker türlerini, açık `actors`'leri, `search`, `hide_system` ve `include_unscoped`'i kabul eder. Journal tür grupları, tam predikatlarına genişler. Arama, imzalı kaynak metni değiştirmeden günlüğün NFC/büyük/küçük harf duyarlı olmayan yük aramasını kullanır. Tarihler bir saat dilimi gerektirir ve UTC'ye normalleştirilir. Tarihler, **observed_at değerini** filtreler. Telegram'ın `source_at` değeri ayrı olarak görüntülenir. Kaynak zaman damgası olmayan bir silme işlemi için uydurulmuş bir silme zamanı yoktur. Bir zaman aralığı dışında gözlemlenen geç bir kayıt, bu aralığa girmez; bir mesaj kimliği dilimi, söz konusu mesaj kimlikleri için daha geç bir silme işlemini içerebilir.

`snapshot`, oluşturma zamanını, günlük dizisi/hash sınırını, eşleşme sayısını, ilk/son dizisini ve `result_hash` değerini sabitler. Sonuncusu, boş bir dilim için `[]` dahil olmak üzere, sözlük sırasına göre sıralanmış eşleşen olay hash'lerinin UTF-8 kanonik JSON dizisinin SHA-256 değeridir. Ayrıca tam tür sayılarını ve 24-bin gözlem zamanı minyatürünü de içerir. Bir dilim, yinelenen kaynak kayıtlarını değil, bir sorguyu depolar. Dışa aktarım sırasında, `board/slices/<id>.json` dosyası mevcut hash'leri ve eklenen/kaldırılan dizileri listeler. Doğrulayıcı, oluşturma sınırında orijinal sonucu, ardından da mevcut sonucu yeniden oluşturur. Eklenen kayıtlar bir değişiklik olgusu olarak raporlanır. Orijinal bir olayın kaldırılması, değiştirilemez kanıt zincirini bozar; bu, bir dilimden yapılan sıradan bir kaldırma işlemi olarak sessizce kabul edilmez.

Tepki anlık görüntüleri, son katılımcı listelerinde eksiklikler içerir. Gezgin, aynı sohbet/mesajın bitişik anlık görüntülerini karşılaştırır; bu karşılaştırma, dilim dışındaki bir öncülü de içerir ve **gözlemler arasındaki** toplam sayı farklarını raporlar. Eksik son katılımcıların bir tepkiyi sildiği iddia edilmez. İlk anlık görüntüde çıkarılan önceki bir durum yoktur. Aktör gözlemleri, uydurulmuş bir eylem zamanına değil, sağlandıkları anlık görüntüye atfedilmeye devam eder.

## API ve dışa aktarımlar

`GET /api/board`, collection/chat/author/label/state/from/to/q/kind/comments, offset/limit ve newest/oldest sıralamasını kabul eder. `GET /api/board/card/{id}`, bir kart, kaynak önizlemesi, ileti dizisi, durum geçmişi ve ilgili kartları döndürür. Katılımcılar alt yolu, uygun bahsetme seçeneklerini döndürür. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}`, bir kaydı ekler. `POST /api/board/slice-preview`, bir sorguyu hesaplar. Dilim kayıtları, `GET /api/board/slice/{id}/records` adresinde sayfalandırılır; yeniden hesaplama her zaman güncel kararlı okuma anlık görüntüsünü kullanır. Canlı `/api/stream`, günlük imleçlerinden ayrı olarak, yük içermeyen `board` bildirimleri gönderir.

`GET /api/board/export`, imzalı bir belge döndürür. Sohbetle sınırlı erişim, açıkça etiketlenmiş imzalı bir **ifşa** alır; asla başka bir sohbetin açıklamalarını veya tam zinciri almaz. Tam kanıt ZIP dosyaları `annotations.jsonl`, imzalı `case-board.json` ve dilim JSON eklerini içerir. HTML/PDF/JSON rapor ayarları, pano seçmemeyi, tartışmasız yer imlerini/dilimleri veya yorumlu kartları seçer. Bu bölüm, ekip görüşlerini gözlemlerden açıkça ayırır. Rapor veri filtreleri, okunabilir notları da kısıtlar; kanıt ZIP dosyasındaki tam imzalı kaynak dosyaları eksiksiz kalır.

`GET /api/board/slice/{id}/export`, imzalı bir `tgwitness-board-selection-v1` JSON alıntısı üretir; `?format=csv`, bağımsız bir imza içermeyen kullanışlı bir tablo üretir. JSON ve ZIP dosyalarını koruyun:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

Seçim kontrolü, imzalı beyanın, tam kaynak kayıtlarının ve sorgunun belirtilen sınırda eksiksizliğini doğrular. Kanıt ZIP dosyası daha yeni olabilir, ancak bu önek içermelidir. Asılı kalan bir hedef açıkça raporlanır. Farklı bir orijinal dilim anlık görüntüsü, değiştirilmiş açıklama, uyuşmayan yeniden oynatma durumu veya değiştirilmiş kaynak hatalı sayılır. Açıklama içermeyen eski arşivler mevcut doğrulama davranışlarını korur.

Devir, varsayılan olarak **"Dahil etme"** olarak ayarlanmıştır. Açık dahil etme, halihazırda minimize edilmiş kayıtlar üzerinden kartları gösterir, erişilemeyen/ihmal edilen hedefleri hariç tutar, kaynak metni minimize edilmiş olan vurguları gizler, aynı bahsetme/iletişim kurallarıyla ekip metnini temizler ve isteğe bağlı olarak metavergilerde ve notlardaki bilinen örneklerde soruşturmacı etiketlerini R01, R02… ile değiştirir. Orijinal `annotations.jsonl` dosyası ifşa edilmez. İmzalanmış `tgwitness-case-board-handover-v1` sidecar dosyası ve rapor, aynı gizlenmiş materyali içerir. Dilim sayıları yalnızca ifşa edilen kayıtları tanımlar; orijinal anlık görüntü/sorgu aktör ayrıntıları gizlenir. Minimizer tarafından tanınmayan serbest metin adları, sıradan devir işlemlerinde olduğu gibi yine de inceleme gerektirir. Bu türev, redaksiyondan sonra orijinal açıklama imzalarını koruduğunu iddia etmez.

## Çalışma sınırları

Parametreler arasında 10.000 kart ve 50.000 yorumluk esnek sınırlar, en fazla 5.000 kayıt içeren bir dilim sayfası ve medya önizleme kontrolü bulunur. Esnek sınırlar, geçmişi silmeden uyarı verir. Besleme sayfaları en fazla 200 kart içerir. Bağımsız JSON dilim alıntılarının üst sınırı 64 MiB'dir; sorguyu daraltın veya daha büyük materyaller için imzalı ZIP dosyasını kullanın. Bağımsız doğrulayıcı, açıklamaların yeniden oynatılmasını 256 MiB ile sınırlar. Case Board tarafından harici yorum bildirimleri etkinleştirilmemiştir veya uygulanmamaktadır.

Özelliğin otomatik kabul süreci, depolama, erişim, görüntüleme ve dışa aktarım işlemlerini kontrol etmek için kurgusal veriler ve simüle edilmiş bir Telegram aktarımını kullanır. Kanıt kontrollerinin kapsamı için [doğrulama kapsamı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#verification-scope) bölümüne bakınız.
