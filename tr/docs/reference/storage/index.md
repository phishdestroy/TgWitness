# Depolama ve kurtarma

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/storage/

Yedeklemeler, eski dosyaları bulutunuza taşıma, Object Lock altında kopyalama ve yeni bir makinede kurtarma.

Panel, üç görevi birbirinden ayırır:

| Görev | Ne işe yarar? |
| --- | --- |
| Yedekleme yapın | İmzalanmış günlüğü, kontrol noktalarını, korunan dosyaları ve kuyruğa alınmış dışa aktarmaları yapılandırılmış S3 hedefine kopyalayın. |
| Ücretsiz yerel depolama alanı | Seçilen eski ekleri S3'e veya bir rclone bulut uzaktırına kopyalayın, tam olarak geri okuyun, şifrelenmiş baytları doğrulayın, ardından doğrulanmış yerel kopyayı silin. |
| Kanıt kopyasını saklayın | S3 Object Lock'u yapılandırın ve döndürülen saklama durumunu kontrol edin. Hizmet, istenen modu ve tarihi onaylamalıdır. |

Alan boşaltma işlemi, imzalanmış günlüğü asla silmez veya yeniden yazmaz. Her ek, orijinal SHA-256'sini ve bir kurtarma makbuzunu saklar. İsteğe bağlı gzip sıkıştırması, kimlik doğrulamalı şifrelemeden önce gerçekleştirilir. Bulut dosya adları, Telegram adlarını, sohbet kimliklerini veya orijinal ek adlarını içermez. Bir ek, en fazla 32 GiB boyutunda olabilir.

Yükleme yanıtı tek başına bir dosyayı silme izni değildir. TgWitness, şifrelenmiş nesnenin tamamını indirir, boyutunu doğrular ve SHA-256, makbuzu kaydeder, ardından silme işleminden hemen önce yerel baytları tekrar kontrol eder. Yükleme hatası, farklı geri okuma sonucu veya iptal edilen aktarım durumunda yerel dosya yerinde kalır. Eğer etkinleştirilmiş kanıt yedeklemesi o dosyayı henüz kopyalamamışsa, silme işlemi de yedeklemeyi bekler.

## Bir hedef bağlayın

**Ekstra → Depolama ve disk alanı → Depolamayı yönet** bölümünden görevi ve hedefi seçin, kaydedin, ardından **Yükleme ve indirmeyi test et** seçeneğini seçin. Test, küçük bir rastgele deneme verisini yükler ve geri okur. Telegram içeriği kullanmaz.

S3 için sağlayıcının gerçek uç noktasını, bölgesini ve depolama kovasını kullanın. Wasabi, Backblaze, Cloudflare R2 ve diğer uyumlu hizmetler aynı S3 ayarlarını kullanır. Uyumlu bir API'nin varlığı tek başına Object Lock desteğini garanti etmez. Yönetişim modu, yetkili bir yöneticinin saklama süresini atlamasına izin verebilir; Uyumluluk modunda ise farklı kısıtlamalar geçerlidir. Saklama süresine güvenmeden önce döndürülen Object Lock durumunu okuyun.

Bir rclone hedefi için, rclone’un sağlayıcı kurulumunu kullanarak bir uzak sunucu oluşturun ve bu uzak sunucunun `[name]` bölümünü panele yapıştırın. Yüklü yardımcı program, MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud ve seçicide gösterilen diğer sağlayıcıları destekler. Kimlik bilgileri, bu çalışma alanının şifreli kasasına kaydedilir. OAuth yenilemeleri de kasaya geri kaydedilir. Kimlik bilgileri günlük olaylarına eklenmez veya kurtarma indirmelerine dahil edilmez.

Yardımcı program, sabitlenmiş bir sürüm ve SHA-256 ile çalışma alanı içine kurulur. Sistem PATH'ine eklenmez. Yapılandırma dosyaları ve çalışma dosyaları, söz konusu çalışma alanı içindeki geçici dosyalardır. Komut tabanlı ve yerel dosya uzaktan erişimleri reddedilir. rclone şu anda harici istekler için açıkça seçilmiş bir **Direct** rotası gerektirir; bir çalışma alanı SOCKS5 veya HTTP rotası için yerel S3 depolamasını kullanın; rclone, kullanılamayan bir rotayı sessizce atlamaz.

## Kurtarma dosyasını saklayın

Dosyaları kopyaladıktan sonra **"Kurtarma dosyasını kaydet"** seçeneğini seçin ve dosyayı kurulumdan ayrı bir yerde saklayın. Bu dosya şifre çözme anahtarını ve imzalanmış nesne makbuzlarını içerir, bu nedenle onu özel anahtar yedeği olarak değerlendirin. Orijinal uzaktan yapılandırma ve hedef kimlik bilgilerini de ayrı olarak saklayın. Daha sonraki bir kopyalamadan önce alınan bir kurtarma dosyası, o sonraki dosyanın makbuzunu içermez.

İmza anahtarının parmak izi önceden bağımsız olarak kaydedilmiş olmalıdır. Yalnızca aynı dosya içinde sağlanan anahtarla karşılaştırılarak kontrol edilen bir imza, kurtarma dosyasının kime ait olduğunu belirlemez.

Mevcut bir çalışma alanında eksik depolama makbuzlarını onarmak için **Kaydedilmiş bir kurtarma dosyasından dosyaları kurtarın** öğesini açın ve dosyayı seçin. Panel, imzayı kontrol eder ve aynı çalışma alanı imzalama anahtarını gerektirir. Farklı bir depolama anahtarının değiştirilmesini reddeder. Ardından **Tüm dosyaları geri yükle** öğesini seçin. Geri yükleme işlemi, otomatik depolama kuralını duraklatır; böylece bir sonraki planlanmış işlem, geri yüklenen dosyaları hemen tekrar silemez. Yerel kopyalarla işiniz bittiğinde kuralı yeniden etkinleştirin.

Geri yükleme işlemi, şifreli metni doğrular, şifre çözme işleminin geçerliliğini kontrol eder, gerekirse sıkıştırmayı açar ve dosyayı yerleştirmeden önce orijinal düz metni SHA-256 kontrol eder `media/`. Bozuk bir uzak nesne, asla yerel bir dosyanın yerine geçmez. Farklı baytlara sahip mevcut bir yerel dosya, üzerine yazılmak yerine inceleme amacıyla saklanır.

## Yüklemeyi kaybettikten sonra kurtarma

TgWitness'yi başka bir makineye kurun. Özel kurtarma dosyasını, ayrı olarak kaydedilmiş parmak izini ve orijinal hedef kimlik bilgilerini kullanın:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

S3 için, `--credentials` içinde bulunan özel bir JSON dosyasına işaret eder `access_key` ve `secret_key`içeren özel bir JSON dosyasına işaret eder; imzalanmış kurtarma dosyası hedef ayarlarını sağlar. Komut, doğrudan bir harici bağlantı kullanır ve bir rclone uzak sunucusunun ihtiyaç duyduğu zaman sabitlenmiş yardımcı programı indirir. Mevcut bir çıktı dizinini reddeder.

Geri kazanılan orijinal baytlar, `recovered-attachments/media/`SHA-256 ile adlandırılır. , `recovery-log.jsonl` , kurtarma işlemlerinin imzalanmamış bir kaydıdır. Bu komut, kaybolan imzalı bir günlüğü veya onun imza anahtarını yeniden oluşturmaz. Bunlar için çalışma alanının tam bir yedeğini saklayın. Bir depolama kurtarma dosyası, çalışma alanının tam bir yedeği değildir.

## Operatör botu ve tamamlama bildirimleri

Telegram botu operatöre aittir. BotFather aracılığıyla oluşturun ve panelde token'ını, hedef sohbeti ve açıkça izin verilen Telegram kullanıcı kimliklerini ayarlayın. Hem gönderen hem de sohbet eşleşmelidir. İletilen mesajlar ve diğer botlardan gelen komutlar göz ardı edilir.

`/status` ve `/stats` varsayılan "sadece durum" modunda kullanılabilir. İsteğe bağlı kontrol modu, `/pause`, `/resume` ve `/copy`. `/copy` yapılandırılmış depolama görevini talep eder; bu, uzaktan yüklemenin zaten tamamlandığı anlamına gelmez. Komutlar keyfi URL'ler, dosyalar veya kabuk programları sağlayamaz.

Uyarılar ve görev tamamlama için ayrı bildirim ayarlarını kullanın. Tamamlama bildirimleri, eksiklikler içeren bir hesap dışa aktarımını eksiksiz bir dışa aktarımdan ayırır ve geçmişi ile depolama sayılarını gösterir. Bildirim ayarlarında ayrı olarak etkinleştirilmedikçe mesaj alıntıları dahil edilmez. Hizmet seçici, sabit bir sağlayıcı örnekleri kümesinden ziyade, gerçekte yüklü olan Apprise kataloğundan oluşturulur.
