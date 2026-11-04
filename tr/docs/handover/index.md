# Paylaşım kopyası hazırlayın

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/handover/

Yalnızca gerekeni paylaşın, orijinal dokunulmadan kalır.

Teslim, ayrı bir imzalı özettir: sohbetleri ve kişileri seçin, kimlikleri ya da metni gizleyin, dosyaları ve ekip notlarını belirleyin. Manifest neyin tutulduğunu, kısaltıldığını ve dışarıda bırakıldığını kaydeder.

## Alıcının özetini hazırlayın

1. **Dışa aktarımlar → Teslim özeti**: amacı yazın, sohbetleri ve dönemi seçin, adı geçen kişilere ihtiyacınız varsa **Seçili sohbetlerin kişilerini yükle**.
2. Diğer herkes: takma ad, dışarıda ya da kaydedildiği gibi. Metin ve dosyalar ayrı anahtarlardır; telefonlar ve e-postalar maskelenebilir.
3. Case Board: hiçbir şey, yer imleri ve kesitler ya da yorumlu kartlar. Ekip adları takma adlarla değiştirilebilir.
4. **Teslim özetini indir**, açın, doğrulayın, göndermeden önce gözden geçirin.

### Bir adet orijinal, paylaşım amaçlı bir kopya

Sentetik örnek · yalnızca kimlik gösterimi amaçlıdır

1. **Seçin.** Vaka sohbetini ekleyin ve alıntının hangi kişiyle ilgili olduğunu belirtin.
2. **Kısaltın.** Paylaşım kopyasında diğer katılımcının nasıl görüneceğini seçin.
3. **Kontrol edin.** Oluşturulan arşivin raporunu ve kayıtlarını göndermeden önce açın.
4. **Paylaşın.** Düzeltilmiş metni teslim edin ve güvenilir parmak izini ayrı olarak iletin.

#### Orijinal gözlem

Nora · kullanıcı 71002

“Düzeltilmiş bağlantıyı aldım.”

Kaynak günlük dosyası bu kaydedilmiş gözlemi saklar.

#### Alıcının kopyası

Kaydedildiği gibi göster: Nora · kullanıcı 71002 · “Düzeltilmiş bağlantıyı aldım.”

Takma ad: P01 · “Düzeltilmiş bağlantıyı aldım.”

Çıkarılacak kısım: Bu katılımcının mesajı metinden çıkarılmalıdır.

#### Gerçek dosyaları inceleyin

report.html ve records.jsonl dosyalarını okuyun.

Kimlikleri, metni, ekleri ve isteğe bağlı ekip yorumlarını kontrol edin.

#### İmzalı alıntı

Seçim + dosya hash değerleri + imzalı manifest

Kaynak derginin sınırlarına bağlı ayrı bir paket

## Kontrolleri birlikte kullanın

| Kontrol | Metin üzerindeki etkisi |
| --- | --- |
| Kişiler | Seçili kişiler adlarıyla kalır; diğerleri takma ad alır ya da dışarıda bırakılır. |
| Metin | Tüm metin, yalnızca seçili kişilerin ve hesabınızın metni ya da hiçbiri. |
| Dosyalar | Seçili kişilerin ve hesabınızın dosyaları, gösterilen tüm dosyalar ya da hiçbiri. |
| Case Board | Hiçbir şey, yer imleri ve kesitler ya da tartışmalı kartlar. |

Metni ve dosyaları da okuyun: takma ad, bir mesajın ya da ekin içine yazılmış adları kaldırmaz. Seçili bir dosya eksikse geri yükleyin ya da ekleri dışarıda bırakın.

## Metnin bağımsız olarak doğrulanabilir olmasını sağlayın

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Orijinal arşivi ve kontrol noktalarını kendiniz saklayın. Alıcı, tüm çalışma alanını almadan kendi kopyasını doğrulayabilir. Tasarım: [Report studio](https://phishdestroy.github.io/TgWitness/tr/docs/reports/). Güvenilir başvurular: [dışa aktarım doğrulaması](https://phishdestroy.github.io/TgWitness/tr/docs/exports/).
