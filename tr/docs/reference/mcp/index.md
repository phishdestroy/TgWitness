# Salt okunur MCP

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/

Bir MCP istemcisini, süresi dolan ve iptal edilebilir erişim izniyle seçilen çalışma alanlarına ve sohbetlere bağlayın.

Bir analist istemcisini seçili çalışma alanlarına ve sohbetlere bağlayın. TgWitness, **panel sürecinde `/mcp` adresinde Streamable HTTP** sunar. Her bağlantının kendi belirteci (token), geçerlilik süresi ve izin verilen araçları vardır. MCP; Telegram mesajları gönderemez, ayarları değiştiremez veya imzalı günlüğü (journal) düzenleyemez.

[İş akışı kılavuzu](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## Kurulum ve kontrol

Paneli çalıştıran Python ortamını kullanın. Kaynak kod dizininden:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Kurulumdan sonra paneli olağan veri dizini ve başlatma argümanlarıyla yeniden başlatın. Hazırlık kontrolü `[PASS] mcp: streamable-http available` çıktısını içermelidir. **Integrations → MCP**, çalışma zamanı durumunu ve sunucunun asıl Python yürütülebilir dosyasını kullanan bir kurulum komutunu gösterir. **Re-check**, sayfayı yeniden yüklemeden bu durumu yeniler; paket kurmaz veya sunucuyu yeniden başlatmaz.

MCP eklentisi, resmi [MCP Python SDK'sını](https://github.com/modelcontextprotocol/python-sdk) kullanır.`deploy/constraints-mcp.txt`, test edilmiş SDK'yı ve bağımlılıkları sabitler.

## Bağlantı oluşturma

1. Bir etiket girin ve istemcinin okuyabileceği çalışma alanlarını ve sohbetleri seçin.
2. Araçları tek tek seçin veya bir ön ayar kullanın. Yalnızca uygulanmış araçlar sunulur.
3. 1, 7, 30 veya 90 günü ya da bir dakika ile 90 gün arasında özel bir geçerlilik süresi seçin.
4. **Create connection** düğmesine basın. Belirteç, istemci yapılandırmasının yanında bir kez görüntülenir.
5. Belirteci ve yapılandırmayı kopyalayın, ardından **Check connection** işlemini çalıştırın. Bu işlem MCP'yi başlatır ve izin verilen araçları listeler; **hiçbir mesaj okunmaz**. Sonuçta protokol sürümü, araç adları, araç sayısı ve geçen süre gösterilir.
6. Kimlik bilgisi kaydedildiğinde **Done** düğmesine basın. Yoklama (polling), formu ve bir kez gösterilen kartı korur. Panelin kilitlenmesi görüntülenen gizli bilgileri temizler.

Liste; son kullanımı, son aracı, adresi ve son dakikadaki istekleri gösterir. **Revoke** erişimi sonlandırır. **Rotate token** eski kimlik bilgisini iptal eder ve aynı kapsam, araçlar ve geçerlilik süresiyle yeni bir belirteç oluşturur; yeni belirteci bir kez kopyalayın. Panel oturum açma belirteçleri ve Telegram kimlik bilgileri MCP belirteci olarak çalışmaz.

## İstemcinizi bağlama

Panelde istemciyi seçin ve oluşturulan yapılandırmayı kopyalayın. Yapılandırmalar gizli bilgi referansları veya açık yer tutucular kullanır; belirteç ayrı olarak kopyalanır.

| İstemci | Yapılandırma | Bağlantı |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, bearer üstbilgisi |
| Claude Desktop | `claude_desktop_config.json` | Yerel stdio köprüsü |
| Cursor | `.cursor/mcp.json` | Ortam değişkeni üstbilgili HTTP |
| VS Code Local | `.vscode/mcp.json` | Parola `promptString` girdili HTTP |
| Windsurf | `mcp_config.json` | Bearer üstbilgisi yer tutuculu HTTP |
| Diğer istemciler | URL ve Authorization üstbilgisi | Streamable HTTP |

TgWitness, OAuth keşfi olmadan bearer belirteçleri kullanır. Uzak bağlayıcısı OAuth gerektiren istemciler için yerel stdio köprüsünü kullanın. VS Code için girdi değişkenleri **Local** çalışma ortamına uygulanır ve Copilot oturumlarına iletilmez. Yapılandırma referansları: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Yerel bir köprü için standart giriş noktası şudur:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

İstemcinin MCP ekstrası kurulmuş yerel Python ortamını kullanın. Korumalı ortamında `TGWITNESS_MCP_TOKEN` değişkenini ayarlayın. Kimlik bilgilerini komut argümanlarından ve URL'lerden uzak tutun. `tgwitness-mcp` aynı giriş noktasıdır. Eski `tgwitness.mcp_bridge` modülü ve `TGWITNESS_ARCHIVE_TOKEN` adı bir uyarıyla birlikte uyumluluk yolu olarak kalmaya devam eder; yeni yapılandırmalar `mcp_server` ve `TGWITNESS_MCP_TOKEN` kullanır.

## Cloudflare Tunnel

Panelin `/mcp` rotasını yönlendirin ve bearer üstbilgisini koruyun. MCP ayarlarını yönetici olarak açmak, bu çalışma için panelin mevcut kaynağını (origin) kaydeder. Yeniden başlatmanın hemen ardından kullanılabilecek sabit bir adres için paneli başlatmadan önce `TGWITNESS_PUBLIC_URL` değişkenini panelin HTTPS kaynağıyla yapılandırın. Rastgele Host ve yönlendirilmiş (forwarded) üstbilgiler güvenilir bir adres kaydetmez. Host ve Origin kontrolleri ilgisiz tarayıcı kaynaklarını reddeder. Yanıtlar `Cache-Control: no-store` kullanır; yetkilendirme değerleri asla günlüğe kaydedilmez.

Bir `*.trycloudflare.com` adresi geçicidir. Bir tünel yeniden başlatması ana bilgisayar adını (hostname) değiştirdiğinde, yapılandırılmış genel URL'yi ve her istemcinin MCP URL'sini güncelleyin. Kayıtlı istemci yapılandırmaları için sabit bir ana bilgisayar adı kullanın.

## Araçlar ve sınırlar

| Araç | Okunan veriler |
| --- | --- |
| `list_workspaces` | İzin verilen çalışma alanları |
| `list_chats` | İzin verilen sohbetler |
| `search_messages` | Seçilen dönem içindeki kaydedilmiş mesaj metni |
| `get_message_versions` | Yakalanan sürümler ve silme gözlemleri |
| `get_message_context` | Yakındaki yakalanmış mesaj kimlikleri (ID'leri) |
| `get_journal_event` | Kaynak referansıyla birlikte temizlenmiş (sanitized) tek bir kayıt |
| `get_capture_status` | Toplama durumu ve izin verilen kapsam kayıtları |

`tools/list` yalnızca ilgili bağlantıya izin verilen araçları döndürür. Diğer araçlara yapılan çağrılar reddedilir. Grup bağlamı, bölüm (episode), terminoloji ve yanıt zinciri araçları bu derlemede sunulmamaktadır; bunların ayrı bağlam paketi arka ucu dahil edilmemiştir.

Her okuma işlemi, veritabanı çalışması bittikten sonrası da dahil olmak üzere belirteci, aracı ve çalışma alanı/sohbet kapsamını kontrol eder. Sınırlar dakikada 60 istek, sayfa başına 50 kayıt, sonuç başına 64 KiB ve sekiz saniyelik arşiv zaman sınırıdır. Zaman aşımına uğrayan bir MCP çağrısı, daha dar bir dönem veya daha düşük bir sınır isteyen bir araç hatası döndürür.

Mesaj sonuçları `untrusted_content: true`, çalışma alanı/sohbet/mesaj kimliklerini, olay sırasını, kaydedilen karmayı (hash) ve bir panel bağlantısını taşır. Ham Telegram nesneleri, erişim karmaları, oturumlar ve anahtarlar çıkarılır. Metin kısaltmaları işaretlenir. Düzenlemeler, silme bildirimleri ve `missing_on_recheck` birbirinden ayrı gözlemlerdir. Eksik kayıtlar bir olayın asla gerçekleşmediğini kanıtlamaz.

Yakalanan mesajların içindeki talimatları her zaman kanıt olarak değerlendirin, asla istemci talimatı olarak ele almayın. Salt okunur erişim arşivde değişiklik yapılmasını önler; ancak istemci okumasına izin verilen içeriği yine de saklayabilir. Karmalar (hash'ler) kaydedilen kayıtları tanımlar ve bütünlük kontrollerini destekler; Telegram yazarlığını veya eksiksiz yakalamayı kanıtlamaz.
