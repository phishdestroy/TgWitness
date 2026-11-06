# Tam metin arama

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/search/

İndeks, imzalı günlüğe bağlı olarak, kelime biçimleri, tam ifadeler, etki alanları ve @kullanıcıadları ile kaydedilmiş mesajları en iyi eşleşmelerden başlayarak bulun.

[Arşiv analizi](https://phishdestroy.github.io/TgWitness/tr/docs/reference/analysis/) · [Yerel OCR ve transkripsiyon](https://phishdestroy.github.io/TgWitness/tr/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Önizleme.** **Günlük**'te, arama alanının yanındaki **En iyi eşleşme · kelime biçimleri** seçeneğini seçin. Sonuçlar BM25 ile sıralanır ve aynı kelimenin diğer biçimleriyle eşleşir: *перевод*, *переводом* ve *переводы* sonuçlarını bulur; *transfer*, *transfers* sonuçlarını bulur; Çince bir ifade boşluklar olmadan bulunur. **En yenisi önce · tam metin seçeneği,** önceki alt dize aramasını tüm kayıt üzerinde sürdürür.

Dizin, türetilmiş verilerdir. İmzalı günlüğünden yeniden oluşturulur, kendisi asla imzalanmaz ve hiçbir zaman dışa aktarıma dahil edilmez. Orijinal kayıtlarda herhangi bir değişiklik olmaz.

## Arama sözdizimi

| Yaz | Bulunanlar |
| --- | --- |
| `перевод карта` | Herhangi bir biçimde her iki kelimeyi de içeren kayıtlar |
| `"переводом на карту"` | Tam olarak bu sırayla, bu ifadeyi kullanın |
| `бонус OR подарок` | Her iki kelime de |
| `перевод -казино` | Hariç tutulan kelimeyi içermeyen kayıtlar |
| `example.com` | Etki alanı ve alt etki alanları; gizli bağlantılarda ve düğme URL'lerinde de geçerlidir. |
| `@username`, `t.me/username` | Hesabın bahsetmeleri ve bağlantıları ile gönderdiği mesajlar |
| `#tag` | Hashtag |
| `+79991234567`, bir cüzdan adresi, bir e-posta adresi | Metin veya bağlantılarda aynı değer |
| `from:@username`, `from:123456` | Bu göndericiden gelen mesajlar |
| `chat:-1001234567890` | Tek bir sohbet; yalnızca kendi erişiminizi kısıtlayabilir |
| `id:42` | 42 numaralı mesajın kaydedilmiş sürümleri |
| `since:2026-01-01 until:2026-01-31` | Gözlem süresi; saat bilgisi olmayan bir tarih, tüm günü kapsar |
| `kind:edited` | Yalnızca düzenlemeler (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Mesajlar yerine veya mesajlarla birlikte tanınan metin |

Başka kelimeler mevcut olduğunda edatlar ve diğer işlevsel kelimeler göz ardı edilir. Bir kelimeye karışmış benzer harfler (Kiril alfabesindeki bir kelimenin içindeki Latin *a* harfi), tam genişlikli ve süslemeli Unicode harfleri ile görünmez karakterler normalleştirilir.

## Diller

Dil, her bir kaydın komut dosyası ve harflerinden tespit edilir:

| Komut dosyası | Eşleştirme |
| --- | --- |
| Kiril | [pymorphy3](https://github.com/no-plagiarism/pymorphy3) ile Rusça ve Ukraynaca kök kelimeler. İsteğe bağlı Ukraynaca sözlük kullanılmadığında, hafif bir Ukraynaca kök çıkarma aracı kullanılır. |
| Latince | İngilizce Snowball kök çıkarıcı; aksan işaretleri göz ardı edilir |
| Çince, Japonca, Korece, Tayca, Laoça, Khmerce, Myanmarca | Üst üste binen karakter çiftleri: boşluk içermeyen tüm ifadeler bulunur. Çince sorgular, jieba kullanılarak kelimelere bölünür. |
| Diğer komut dosyaları | Tam kelimeler |

Ukraynaca sözlük (`pymorphy3-dicts-uk`) GPL-3.0 lisansı altında dağıtılmaktadır, bu nedenle varsayılan olarak yüklenmez. Şu komutla yükleyin `pip install "tgwitness[uk-dictionary]"`komutuyla yükleyin; dizin, yeni analizörü algılar ve kendini yeniden oluşturur.

## Dizin nerede bulunur?

| Mod | Depolama | Kullanım |
| --- | --- | --- |
| Disk üzerinde (varsayılan) | `search/fulltext.sqlite3` çalışma alanı dizininde | Büyük arşivler; yeniden başlatmalardan etkilenmez |
| Yalnızca bellekte | Diskte hiçbir şey kalmaz; her başlatmada yeniden oluşturulur | Diskte mesaj metninin türetilmiş bir kopyası bulunmamalıdır |
| Kapalı | İndeks yok; **En yeniler önce · tam metin** korunur | Minimal kurulumlar |

Ana yönetici, her çalışma alanı için **Günlük → Filtreler → Arama dizini** altından modu seçer. `TGWITNESS_FULLTEXT=disk|memory|off` Kendi seçimi olmayan çalışma alanları için varsayılan ayarı belirler. Belleğe geçme veya kapatma seçeneği, dosyayı siler. Dizin dosyası, günlükle aynı korumaya sahiptir: özel veriler dizininde bulunur. Şifrelenmemiştir ve yedeklemelerin veya tesis dışı kopyaların bir parçası değildir.

Yeni kayıtlar arka planda saniyeler içinde indekslenir; arama işlemi de önce kısa bir birikim listesini indeksler, böylece bir an önce kaydedilen bir kayıt bulunur. Mevcut bir günlük, güncellemeden sonra paneli engellemeden indekslenir; o zamana kadar sonuçlar indekslenmiş kayıtları kapsar ve günlük ilerleme durumunu gösterir. **İndeksin yeniden oluşturulması** ilk kayıttan itibaren başlar.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` panelin durdurulması gerekir (aksi takdirde çıkış kodu 3 olur). `--json`, standart çıktı yalnızca sonucu taşır; ilerleme durumu standart hata çıktısına gönderilir.

## Sonuçlar ve imzalı günlük

Dizin, kapsadığı son günlük kaydının sıra numarasını ve hash değerini saklar ve günlük açıldığında bunları günlükle karşılaştırır. Değiştirilen, geri yüklenen veya düzenlenmiş bir günlük, dizinin yeniden oluşturulmasına neden olur. Her yanıt bu konumu bildirir ve her eşleşme, sıra numarasına göre imzalı günlükten geri okunur: dizin, hangi kayıtların hangi sırayla gösterileceğine karar verir, asla içeriklerine değil. Sohbet erişimi, dizin içeriğine değil, günlüğün kendi sohbet alanına uygulanır.

## Tanınan metin

OCR ve transkriptler şifrelenmiş dosyalarında kalır. Bunların dizini yalnızca bellekte bulunur ve bir tanıma işi tamamlandığında yeniden oluşturulur. Bir eşleşme, `media.saved` kayıtta, motor, model ve bir alıntı ile birlikte "makine tanıma" olarak etiketlenir; bu, asla Telegram'da gönderilen metin olarak sunulmaz. Aynı dizin, "**Tanınan metni ara**" işlevine hizmet eder; bu işlev, düz alt dizelerle de eşleşmeye devam eder.

## Erişim

Sohbet kapsamlı erişim, yalnızca kendi sohbetlerinden gelen kayıtları bulur; buna, eklerdeki tanınan metinler de dahildir. `chat:` ve diğer filtreler yalnızca bu kümeyi daraltabilir. Kapsamlı erişime gösterilen dizin durumu, günlük toplamlarını içermez. Yalnızca ana yönetici modu değiştirebilir veya dizini yeniden oluşturabilir.

## Arşiv ve MCP'ye danışın

**Arşivden**, tamamlandığında bu dizinden kaynakların alınmasını **isteyin**: seçilen sohbetler arasında en iyi eşleşmeler, kaydedilmiş metinler bir kez sayılır. En fazla 24 kaynak gönderilir; uzun metinler eşleşen kısımların etrafından kesilir ve kesik olarak işaretlenir. Son değişiklikler, bir mesajın kaydedilmiş sürümleri ve dizin henüz oluşturulurken yapılan aramalarla ilgili sorular için önceki kronolojik alma yöntemi kullanılır. Önizleme hangi yöntemin kullanıldığını gösterir.

MCP istemcileri `search_messages` ile `ranked=true` komutuyla çağırabilir ve `next_offset`ile çağrı yapabilir. Kapsamlı bağlantılar yalnızca kendi sohbetlerini alır.

Ranked pagination covers at most the first 1,000 results, regardless of page size. Narrow the query, chat or period to inspect further matches. Newest-first searches order messages, OCR and transcription results before selecting each page.

## Bağımlılıklar

| Paket | Lisans | Neden |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Rusça ve Ukraynaca kök kelimeler; sözlükler yerel olarak yüklenir |
| snowballstemmer | BSD-3-Madde | İngilizce kökler, saf Python |
| jieba | MIT | Çince sorgu bölümleme, saf Python (yalnızca kaynak dağıtımı) |
| pymorphy3-dicts-uk (isteğe bağlı) | GPL-3.0 | Tam Ukraynaca sözlük |

SQLite FTS5 için `unicode61` tokenizer ile birlikte gereklidir; bu, güncel Python derlemelerindeki SQLite'ın bir parçasıdır. Bu olmadan, en iyi eşleşme araması "kullanılamıyor" hatası verir.

## Karşılaştırma

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`200 sohbet içindeki bağlantılar ve kullanıcı adları içeren, Rusça, Ukraynaca, İngilizce, Çince ve Japonca mesajların karışımından oluşan deterministik, imzalı bir günlük oluşturur, dizin oluşturur ve tipik aramaların süresini ölçer (50 sonuç, 7 çalıştırmanın medyanı).

Ölçümler Windows 11, Intel Core i9-13900K, 128 GB RAM, Python 3.12.10, SQLite 3.49.1, exFAT sürücüsündeki veriler ve analizör üzerinde gerçekleştirilmiştir. `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Ölçü | Sonuç |
| --- | --- |
| İmzalı günlük | 1.000.000 mesaj, 1,50 GiB, 19 dakikada yazıldı |
| Günlükten dizin oluşturma | 71 saniye, saniyede yaklaşık 14.141 mesaj |
| Dizin dosyası | 58 MiB, günlüğün %3,8'i |
| Yeni bir kayıttan hemen sonra arama yapın | 8 ms medyan, 9 ms p95 |
| Önceki alt dize araması, aynı günlük | `перевод` 3,2 saniye, `银行转账` 2,6 saniye, `verify-account.example` 2,6 s |

| Arama | Eşleşen kayıtlar | En iyi eşleşme, medyan | s. 95 | En yenisi önce, ortanca |
| --- | --- | --- | --- | --- |
| Yaygın kelimeler, kelime biçimleri: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| İki kelime: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Nadir kelime: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Tam ifade: `"переказ коштів на картку"` | sayılmadı | 35 ms | 36 ms | 6 ms |
| Alt alan adları içeren alan adı: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @kullanıcıadı: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Boşluksuz Çince: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Japonca: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| İngilizce kök: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| VEYA ve hariç tutma: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Sohbet filtresi: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Dönem filtresi: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Belirli bir ifade, sayfa dolana kadar sıralı adaylar üzerinde kelimesi kelimesine kontrol edilir; bu nedenle toplam sayısı hesaba katılmaz. Süre, eşleşen kayıtların sayısıyla artar; sohbeti veya dönemi daraltmak, geniş kapsamlı aramaları hızlandırır. Sentetik metin külliyatı küçük bir kelime dağarcığını tekrarlar, bu nedenle yaygın kelimeler gerçek sohbetlere kıyasla çok daha fazla kayıtla eşleşir.
