# Komut satırı

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/cli/

Komut dosyaları ve ajanlardan arama yapın, bağlamı okuyun, etkinlikleri sayın ve kaydedilmiş mesajları dışa aktarın; --json çıktısı, kararlı çıkış kodları ve kapsamlı salt okunur belirteçler ile.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Belgeler](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Arşiv entegrasyonları](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[Salt okunur MCP](https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/) · [Tam metin arama](https://phishdestroy.github.io/TgWitness/tr/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Önizleme.** `tgwitness search`, `context`, `messages`, `stats` ve `export` komut dosyaları ve yapay zeka ajanları için kaydedilmiş gözlemleri okuyun. Bu araçlar, Telegram'a hiçbir şey gönderemez, ayarları değiştiremez veya imzalı günlüğü düzenleyemez.

Bununla `--json`, stdout tam olarak bir JSON belgesi taşır (`export` JSON satırları yazar). İlerleme durumu, ipuçları ve hatalar stderr'e yönlendirilir. Çıkış kodları sabittir:

| Kod | Anlam |
| --- | --- |
| `0` | Başarı, boş sonuç dahil |
| `1` | Hata: panele erişilemiyor, veriler okunamıyor, dışa aktarma kesintiye uğradı |
| `2` | Kullanım hatası veya geçersiz istek: hatalı tarih, bilinmeyen seçenek, arama dizini kapalı |
| `3` | Şu anda kullanılamıyor: çalışma alanı çalışan bir panelde açık veya panel daha sonra tekrar denemenizi istiyor (hız sınırı, zaman aşımı) |
| `4` | Erişim reddedildi: eksik, süresi dolmuş veya iptal edilmiş jeton, kapsam dışı bir sohbet, izin verilmeyen bir araç |

## İki okuma yöntemi

**Panel aracılığıyla (`--url`).** Komut, MCP ile aynı kapsamlı arşiv API'sini kullanır. **Entegrasyonlar → MCP** bölümünden bir bağlantı oluşturun: çalışma alanlarını ve sohbetleri, araçları ve geçerlilik süresini seçin, ardından jetonu bir kez kopyalayın. Bağlantı salt okunurdur, belirtilen sohbetlerle sınırlıdır, dakikada 60 istek ile hız sınırlamasına tabidir ve her an iptal edilebilir veya yenilenebilir. Panel giriş jetonları ve Telegram kimlik bilgileri burada çalışmaz.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Uzak panel için HTTPS gereklidir; düz HTTP yalnızca `127.0.0.1`, `localhost` ve `::1`. Proxy ortam değişkenleri yok sayılır ve yönlendirmeler reddedilir; bu nedenle jeton yalnızca sizin verdiğiniz adrese ulaşır.

**Durdurulmuş bir çalışma alanından doğrudan (`--data-dir`).** Veri dizinini, token olmadan tam yerel erişimle okur. Veri dizininin bir kopyasında veya toplama işlemi durdurulmuşken kullanın. İmzalı kayıtlar asla değiştirilmez; panelde olduğu gibi, bir çalışma alanının açılması, türetilmiş dizinleri güncelleyebilir. Panel çalışma alanını açık tutarken, komut kodu `3`ile sonlanır; bunun yerine panel üzerinden okuma yapın. `--data-dir`, `TGWITNESS_DATA`, `./data/live` komutun çalıştırıldığı kurulumun veri dizini kullanılır.

`--workspace ID` bir çalışma alanını seçer (varsayılan `default`). `tgwitness messages
--workspaces` okuyabileceğiniz çalışma alanlarını listeler.

## Komutlar

| Komut | Sonuç |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | En uygun eşleşmeler ilk sırada gösterilsin; kelime biçimleri, tırnak içindeki tam ifadeler, alan adları ve `@username` ([sözdizimi](https://phishdestroy.github.io/TgWitness/tr/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Tam metin, en yenisi önce, dizin hariç |
| `tgwitness context CHAT_ID MESSAGE_ID` | Her iki tarafta da on mesaj kimliği içindeki kaydedilmiş mesajlar |
| `tgwitness messages` | Okuyabileceğiniz sohbetler |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Sohbetin kaydedilmiş mesajları, en yenisi önce |
| `tgwitness messages CHAT_ID --message ID` | Bir mesajın kaydedilen her sürümü ve silme kaydı |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Aşağıda etkinlik istatistikleri yer almaktadır |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Gözlemler, günlük sırasına göre JSON satırları olarak kaydedilir |

Tarihler `2026-10-01` (UTC gece yarısı) veya saat dilimi belirtilmiş ISO zamanlarıdır `2026-10-01T09:00+03:00`. `search`, `messages` ve `export` için gözlem zamanı seçilir. Sayfalar en fazla 50 kayıt tutar: sıralı arama için `next_offset` (`--offset`) sıralı arama için ve `next_before` (`--before`) başka yerler için.

Sıralı arama, 1,000 sonuçta durur. Son sayfa, `--limit` değerinden daha kısa olabilir; daha fazla eşleşen gözlem varsa sorguyu, sohbeti veya dönemi daraltın.

Her mesaj sonucu `untrusted_content: true`çalışma alanı, sohbet ve mesaj kimliklerini, günlük numarasını, kaydedilen kaydın hash değerini ve bir panel bağlantısını içerir. Düzenlemeler, silme bildirimleri ve `missing_on_recheck` ayrı kayıtlardır. Bir kaydın bulunmaması , bir olayın hiç gerçekleşmediğini kanıtlamaz.

### Etkinlik istatistikleri

`stats` Bir sohbet, bir gönderen veya kapsamdaki tüm sohbetler için kaydedilen gözlemlerin sayısını gösterir:

- UTC saatine ve hafta günlerine göre (önce Pazartesi) mesajlar; en yoğun saatler ve günler;
- düzenlenmiş, silinmiş ve `missing_on_recheck` paylaşımlar;
- mesaj sayıları ile ilk ve son mesaj zamanları bilgilerini içeren gönderenler;
- en sık görülen etki alanları ve `@handles`, kaydedilmiş sürümleri genelinde her mesaj başına bir kez sayılan;
- kapsam: `coverage.gap` kayıtlar ve tüm çalışma alanına erişim için, bağlı bir toplayıcı kalp atışı olmayan dönemler (`collector_liveness`).

Bu aralık, **Telegram tarafından bildirilen mesaj zamanını** seçer. Saat ve hafta içi gün sayıları, göndericinin saat dilimini tahmin etmeye yardımcı olabilir; ancak bunu kesin olarak belirlemez. Rakamlar, günlükten talep üzerine hesaplanır ve saklanmaz. Her sonuç, erişiminiz çalışma alanını kapsadığında kapsadığı günlük başlığını belirtir. Okuma, panel üzerinden beş saniye sonra veya `--timeout` yerel olarak (varsayılan 30 saniye) okuma işlemi sona erer; ardından `complete` false olur ve `partial` okunmamış ilk kaydı belirtir. Bu durumda yalnızca en yeni kayıtlar sayılır.

### Dışa aktar

`export` Kaydedilen her gözlem için (yeni mesajlar, anlık görüntüler, düzenlemeler, kurtarılan mesajlar, silme bildirimleri, `missing_on_recheck` ve kaydedilmiş medya kayıtları) günlük sırasına göre bir JSON nesnesi yazar. Her satır, diğer sonuçlarla aynı alanlara sahiptir ve tam metni içerir. `--output`, dosya bir `.partial` adla yazılır ve yalnızca panelin tamamlanma kaydı sonrasında yeniden adlandırılır; kesintiye uğrayan bir dışa aktarma işlemi dosya bırakmaz ve `1`. `--output` mevcut bir dosyanın üzerine asla yazmaz. `--output` ve `--json`kullanıldığında, stdout bir özet taşır: kayıt sayısı, son günlük sırası ve tüm çalışma alanı erişimi için günlük başlığı.

Panel üzerinden yapılan bir dışa aktarım işlemi, "**Mesajları Dışa Aktar"** seçeneğine izin veren bir bağlantıya ihtiyaç duyar **(yalnızca komut satırı)**; bu seçenek varsayılan olarak seçili değildir. Bu dosya bir çalışma kopyasıdır, kanıt değildir: doğrulanabilir bir devir için, "**Dışa Aktarımlar"** bölümündeki imzalı dışa aktarım seçeneğini kullanın; bu seçenek `python -m tgwitness.verify`kontrol eder.

Panel, tamamlanma kaydı da dahil olmak üzere her kaydı göndermeden önce erişimi yeniden kontrol eder. İptal edilmiş veya süresi dolmuş erişim, eksik bir dışa aktarımla sonuçlanır. Gecikmeli sayfa okumaları, arşiv işleyicisi sınırını diğer sorgularla paylaşır ve sınırlı bir bekleme süresine sahiptir.

## Ajan becerisi

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) dosyası, bir ajana bu komutların nasıl kullanılacağını, kayıtların nasıl alıntılanacağını ve yakalanan metnin nasıl işleneceğini anlatır. Dosyayı `.agents/skills` , bunu bir depo checkout'undan yükler. Claude Code için, `tgwitness-cli` klasörü `.claude/skills/` projenize kopyalayın veya `~/.claude/skills/`.

## MCP ve komut satırı

Her ikisi de aynı bağlantıları, kapsam kontrollerini ve sınırlamaları kullanır. MCP sonuçları 64 KiB'lik bir sayfayla sınırlı olduğundan, MCP toplu dışa aktarma özelliği sunmaz; komut satırı verileri akış halinde gönderir. `get_activity_stats` her ikisi için de kullanılabilir.
