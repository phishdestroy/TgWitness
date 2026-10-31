# Salt okunur MCP

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/mcp/

Bir MCP istemcisini, süresi dolan ve iptal edilebilir erişim izniyle seçilen çalışma alanlarına ve sohbetlere bağlayın.

**Güncel ana sürüm:** kaynak kodunu kontrol edin; 0.7.0 taşınabilir önizleme sürümü bu özelliğin öncesine aittir.

[İş akışı kılavuzu](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

TgWitness proje dizininden isteğe bağlı sunucuyu kurun:

```
python -m pip install '.[mcp]'
```

Panelde, **Entegrasyonlar → MCP'yi** açın. Bağlantıya bir ad verin, çalışma alanlarını ve sohbetleri seçin ve bir son kullanma tarihi belirleyin. Arşiv jetonunu bir kez kopyalayın; bu jeton daha sonra geri alınamaz. Kayıp jetonları iptal edin ve yenilerini oluşturun. Panel jetonları ve Telegram kimlik bilgileri, MCP kimlik bilgileri değildir.

## Bir istemciyi bağlayın

Panel, [belgelenmiş yapılandırmasını](https://code.visualstudio.com/docs/agents/reference/mcp-configuration) kullanarak **VS Code Local donanımı** iç`.vscode/mcp.json`'yi oluşturur. İndirilen dosyayı bu konuma kaydedin, MCP: List Servers komutunu çalıştırın ve İndirilen dosyayı bu konuma kaydedin, **MCP: List Servers komutunu** çalıştırın ve TgWitness'i başlatın. VS Code, şifre girişi yoluyla token'ı ister. İndirilen JSON dosyası, token'ı değil, bir istem referansı içerir. MCP extra'nın kurulu olduğu ortamdaki Python yürütülebilir dosyasını kullanın.

Diğer stdio müşterileri için şunu çalıştırın:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

`TGWITNESS_ARCHIVE_TOKEN` değerini müşterinin korumalı ortamında ayarlayın. Bunu komut argümanlarına veya URL'lere eklemeyin. Köprü, panelin yetkili arşiv API'si aracılığıyla okuma yapar; doğrudan veritabanına erişimi yoktur. Stdout yalnızca MCP mesajlarını taşır.

Uzak istemciler için, hizmeti panelin yanında çalıştırın:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

`/mcp`'yi, `127.0.0.1:8766/mcp`'ye bir HTTPS ters proxy üzerinden yönlendirin ve `Authorization: Bearer …` başlığını koruyun. Yetkilendirme başlıklarının ve istek/yanıt gövdelerinin günlüğe kaydedilmesini devre dışı bırakın. Yalnızca gerektiğinde, `--host` ve `--public-url` kullanarak loopback ötesine bağlanın. Uç nokta, resmi [MCP Python](https://github.com/modelcontextprotocol/python-sdk)SDK'sındaki Streamable HTTP'yi kullanır. OAuth keşfi değil, açıkça yapılandırılmış taşıyıcı kimlik bilgilerini destekler; yalnızca OAuth gerektiren istemciler desteklenmez.

**Kontrol protokolü ve erişim,** gerçek bir MCP istemcisini başlatır ve araçları listeler. Bu işlem mesajları almaz. Uzaktan kontrol için, seçilen MCP sunucusu arşiv jetonunu alır. Yalnızca kendi işlettiğiniz veya bu kapsamda güvendiğiniz bir sunucuyu yapılandırın.

## Kapsam ve sonuçlar

Kullanılabilir araçlar: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` ve `get_capture_status`. Telegram eylemleri, yapılandırma değişiklikleri veya toplu dışa aktarma araçları bulunmamaktadır. Her okuma işleminde çalışma alanı/sohbet erişimi yeniden kontrol edilir; süresi dolmuş ve iptal edilmiş kimlik bilgileri artık çalışmaz. Sınırlar, kimlik bilgisi başına dakikada 60 API isteği, sayfa başına 50 kayıt, 64 KiB'lik yanıt ve sekiz saniyelik API süre sınırıdır.

Mesaj sonuçları arasında çalışma alanı, sohbet/mesaj kimlikleri, olay sırası, kaydedilmiş hash ve bir panel bağlantısı yer alır. Bağlantıyı açan görüntüleyicinin kendi yetkili panel oturumu olması gerekir. Ham Telegram nesneleri, erişim hash'leri, dosya referansları, oturum materyalleri ve anahtarlar hariç tutulur. Arama, ham alanları değil, mesaj metnini inceler. Metin sınırlandırılır ve kesintiler işaretlenir. Düzenlemeler, Telegram silme bildirimleri ve `missing_on_recheck` ayrı gözlemler olarak kalır. Sohbet kapsamındaki erişim, çalışma alanı genelindeki operasyonel olayları göremez; yakalama durumu bu sınırı açıkça belirtir.

Arşiv metni güvenilir olmayan bir girdidir. Mesajlardaki talimatlar ek bir kapsam sağlamaz ve müşteri talimatları olarak değerlendirilmemelidir. Harici bir AI modeli, MCP istemcisinin talep ettiği her türlü içeriği alabilir. Salt okunur erişim, arşivde değişiklik yapılmasını engeller; ancak bir istemcinin okuduğu verileri saklamasını engellemez.

Hash değerleri, kaydedilen kayıtları tanımlar ve bütünlük kontrollerini destekler. Ancak bunlar, Telegram mesajlarının yazarlığını veya her mesajın yakalandığını bağımsız olarak kanıtlamaz.
