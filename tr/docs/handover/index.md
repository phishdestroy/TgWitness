# Paylaşım kopyası hazırlayın

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/handover/

Orijinal çalışma alanını olduğu gibi koruyarak ilgili gözlemleri paylaşın.

Bir devir, ayrı bir imzalı özet niteliğindedir. Sohbetleri ve kişileri seçin, kimlik bilgilerini veya metni kısaltın ve hangi dosyaların ve ekip notlarının alıcının kopyasına dahil edileceğine karar verin. Manifestosu, seçimi ve değiştirilmemiş, kısaltılmış ve çıkarılmış kayıtların sayısını kaydeder.

## Alıcının özetini hazırlayın

1. **Dışa Aktar → Devir Özetini** açın. Amacını yazın, sohbetleri ve isteğe bağlı UTC dönemini seçin, ardından isimlendirilmiş kişiler gerekiyorsa **seçilen sohbetlerdeki kişileri yükle seçeneğini** seçin.
2. Diğer kullanıcıların nasıl ele alınacağını seçin: takma ad kullanın, mesajlarını atlayın veya kaydedildiği gibi gösterin. Mesaj metnini ve ekleri ayrı ayrı ayarlayın; isteğe bağlı olarak telefon numaralarını ve e-posta adreslerini gizleyin.
3. Case Board yer imlerini ve dilimlerini mi, yoksa yorum içeren kartları mı dahil edeceğinize karar verin. Bu metinde ekip adlarının yerine soruşturmacı takma adları kullanılabilir.
4. **"İndirme devri özeti"ni** seçin. Oluşturulan raporu ve seçilen kayıtları yerel olarak açın, arşivi doğrulayın ve göndermeden önce kopyayı inceleyin.

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
| Kişiler | Seçilen kişilerin kimlikleri anlaşılır kalmalıdır; diğer katılımcıların kimlikleri tercihe göre takma adlarla belirtilmeli veya metinden çıkarılmalıdır. |
| Metin | Tüm metni dahil edin, yalnızca seçilen kişilerin ve gözlemci hesabının metnini dahil edin ya da mesaj metnini ve metin içeren ayrıntı alanlarını hariç tutun. |
| Dosyalar | Seçilen kişilerin ve gözlemlenen hesabın dosyalarını, gösterilen tüm mesajların dosyalarını veya hiçbir dosyayı seçin. |
| Case Board | Pano materyalleri, yer imleri ve dilimler ya da ekip tartışması içeren kartları seçmeyin. |

Serbest biçimli metinleri ve dosya içeriklerini yanı sıra kimlik bilgilerini de gözden geçirin: bir takma ad, mesajda veya ekte yazan her ismi otomatik olarak silmez. Seçilen bir koruma altındaki dosya mevcut değilse, özeti oluşturmadan önce dosyayı geri yükleyin veya ekleri açıkça hariç tutun.

## Metnin bağımsız olarak doğrulanabilir olmasını sağlayın

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Orijinal imzalı kanıt arşivini ve kontrol noktalarını ayrı olarak muhafaza edin. Devir teslimi kendi projeksiyonunu kaydeder; böylece alıcı, tüm çalışma alanını almadan teslim edilen kopyayı kontrol edebilir. [Report Studio,](https://phishdestroy.github.io/TgWitness/tr/docs/reports/) okuma tasarımını sağlar; [dışa aktarma doğrulaması,](https://phishdestroy.github.io/TgWitness/tr/docs/exports/) güvenilir referansları açıklar.
