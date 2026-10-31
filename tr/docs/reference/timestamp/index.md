# Zaman damgaları

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/timestamp/

İmzalı kontrol noktaları için RFC 3161 zaman damgaları: yetkili kuruma ne gönderilir ve yanıt nasıl doğrulanır?

TgWitness, RFC 3161 isteklerini hazırlar ve zaman damgası otoritesi (TSA) yanıtlarını doğrular. Bu manuel prosedür ne bir TSA seçer ne de veri gönderir; kanıt modu ise her ikisini de bir zaman çizelgesine göre gerçekleştirir ([kanıt formatı](https://phishdestroy.github.io/TgWitness/tr/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Hazırlanan bir istek, **henüz bir zaman damgası kanıtı değildir**.

## Kanıtın bağlayıcılığı

Akış şeması · Hesap gözlemleri → SHA-256 zinciri ve Ed25519 imzaları; SHA-256 zinciri ve Ed25519 imzaları → İmzalı kontrol noktası; İmzalı kontrol noktası → Tam bayt hash ve rastgele nonce; Tam bayt hash ve rastgele nonce → RFC 3161 isteği; RFC 3161 isteği → Bağımsız TSA; Bağımsız TSA → İmzalı TSA yanıtı; İmzalı kontrol noktası → Verileri, geçici anahtarı ve açık CA güvenini doğrulayın; İmzalı TSA yanıtı → Verileri, geçici anahtarı ve açık CA güvenini doğrulayın · Hesap gözlemleri · SHA-256 zinciri veEd25519 imzaları · İmzalı kontrol noktası · Tam bayt hash verastgele nonce · RFC 3161 isteği · Bağımsız TSA · İmzalı TSA yanıtı · Verileri, geçicianahtarı ve açık CAgüvenini doğrulayın

**Diyagramın metin olarak gösterimi**

1. Hesap gözlemleri → SHA-256 zinciri ve Ed25519 imzaları
2. SHA-256 zinciri ve Ed25519 imzaları → İmzalı kontrol noktası
3. İmzalı kontrol noktası → Tam bayt hash ve rastgele nonce
4. Tam bayt hash ve rastgele nonce → RFC 3161 isteği
5. RFC 3161 isteği → Bağımsız TSA
6. Bağımsız TSA → İmzalı TSA yanıtı
7. İmzalı kontrol noktası → Verileri, geçici anahtarı ve açık CA güvenini doğrulayın
8. İmzalı TSA yanıtı → Verileri, geçici anahtarı ve açık CA güvenini doğrulayın

Toplayıcı imzası, kayıtları kendi anahtarına bağlar. Güvenilir bir TSA yanıtı, TSA'nın belirttiği zamanda belirli bir kontrol noktasının var olduğunu teyit edebilir. Kontrol noktası daha sonra günlük önekini bağlayabilir. Bu, her bir Telegram eyleminin zamanını veya yakalanan içeriğin doğruluğunu teyit etmez.

## Prosedür

1. Toplayıcı anahtarının parmak izini ayrı bir güvenilir kanal aracılığıyla saklayın. Yalnızca incelenen ZIP dosyası tarafından sağlanan bir anahtar, toplayıcıyı tanımlamak için yetersizdir.
2. **Dışa Aktar → Zaman damgası isteği hazırla** bölümünden, seçilen çalışma alanının istek ZIP dosyasını indirin. `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` ve `README.txt` dosyalarını açın. Kontrol noktası baytlarını değiştirmeyin.
3. Soruşturmaya uygun bir TSA seçin. `timestamp.tsq`'yi, belgelenmiş yöntemi kullanılarak, HTTP hizmeti için `application/timestamp-query` ile birlikte gönderin. Orijinal ikili yanıtı `timestamp.tsr` olarak kaydedin; uç noktayı, erişim zamanını ve istek sonucunu da kaydedin. İstek, mesajlar yerine bir hash ve nonce içerir; ağ meta verileri yine de isteği ortaya çıkarır.
4. Yanıtın içeriğinden bağımsız olarak güvenilir kök sertifikayı ve ayrıca gerekli tüm ara sertifikaları edinin. Yanıtta yer alan bir sertifika, sırf orada yer aldığı için güvenilir hale gelmez.
5. Güvenilir bir TgWitness kurulumundan şunları doğrulayın:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Gerekirse `--intermediates tsa-intermediates.pem` veya `--openssl /path/to/openssl` ekleyin. OpenSSL, `ts`'yi desteklemelidir. Windows'ta doğrulayıcı, standart Git kurulumunda da arama yapar. OpenSSL 3.5.9, sentetik bir CA/TSA ile yerel olarak test edilmiştir.

1. Kontrol noktasından sonra, söz konusu önekini içerecek şekilde imzalı bir günlük ZIP dosyasını dışa aktarın. Bağımsız olarak bilinen parmak izini kullanarak doğrulayın:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. ZIP dosyasını, kontrol noktasını, isteği, yanıtı, sertifika zincirini, doğrulama sonuçlarını ve aktarım kaydını toplayıcı dışında saklayın. Alındığında doğrulamayı tekrarlayın.

Kaydedilmiş bir kontrol noktasından bir istek hazırlamak için:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

Hazırlık aşaması, JSON'u kanonikleştirir ve eşleşen kontrol noktasını arşive dahil eder. Giriş dosyasında farklı boşluk karakterleri olsa bile, TSA doğrulaması için **o arşivdeki kontrol noktası baytlarını** kullanın.

## Doğrulama sınırları

| Kontrol et | Mevcut davranış |
| --- | --- |
| Veriler | Kontrol noktası baytlarının tam SHA-256 değeri, yanıtla eşleşmelidir. |
| Talep | `--request` ile orijinal sorgu ve nonce doğrulanır |
| TSA imzası | OpenSSL, imzayı ve açıkça belirtilen CA'ya kadar uzanan zinciri doğrular |
| Toplayıcı imzası | Dergi doğrulayıcısı tarafından sabitlenmiş bir anahtarla ayrı olarak doğrulanmıştır |
| İptal | Otomatik OCSP/CRL alma özelliği yoktur |
| Uzun vadeli geçerlilik | Sertifikanın geçerlilik süresinin dolmasından sonra arşiv doğrulaması yapılmaz |
| Planlanmış gönderim | Kanıt modu, varsayılan olarak kapalıdır |

`--request` teknik olarak isteğe bağlıdır, ancak bunun atlanması orijinal nonce'ın doğrulanmasını engeller. Bu prosedürün tamamı için, sonucun `request_checked`'si doğru olmalıdır. Sertifika doğrulaması, kurulu OpenSSL'in kurallarına ve doğrulama süresine tabidir. Uzun vadeli saklama için ayrı bir sertifika/iptal kanıtı politikası gereklidir.

Geçerli bir kriptografik imza, otomatik olarak nitelikli bir zaman damgası veya yasal kabul edilebilirlik kararı anlamına gelmez. Bir operatör, zaman damgası eklemeden önce gözlemleri uydurmuşsa, TSA bu baytları sabitler; ancak bunların doğruluğunu kanıtlamaz.

## Devir teslimi kaydı

Vaka tanımlayıcısını, göndereni ve alıcıyı, UTC aktarım zamanını ve kaynağını, amacını, dosya adlarını/SHA-256 değerlerini, toplayıcı parmak izini, sıra aralığını, bilinen boşlukları, doğrulayıcı sürümünü ve doğrulama sonucunu kaydedin. Bu kaydı, kuruluşunuzun süreçleri doğrultusunda imzalayın ve bağımsız olarak saklayın. TgWitness’te çok kullanıcılı bir koruma-kayıt sistemi uygulanmamaktadır.

Geliştirme sürecinde bağımsız bir canlı TSA ile iletişim kurulmamıştır. Yerel testlerde, değiştirilen verilerin, nonce'ın veya CA'nın uyumluluğunu ve reddedilmesini kontrol etmek için sentetik bir CA/TSA oluşturulur.
