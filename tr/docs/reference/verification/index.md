# Neler test edildi

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/verification/

Canlı Telegram testi, otomatik kontroller, tarayıcı kontrolleri ve henüz doğrulanmamış olan unsurlar.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Sayım |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Kontrol et | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Canlı Telegram testi, tüm hesap · 29 Ekim 2026

Aşağıdaki testin ardından aynı hesap çalışmaya devam etti. 29 Ekim saat 12:10 UTC'de kapsamı tüm hesaba (kanallar, gruplar, özel sohbetler ve botlar) genişletildi; panel onay istedi ve imzalı günlük bunu kaydetti. Saat 17:59 UTC itibarıyla günlükte şunlar yer alıyordu:

| Kayıt tarihi: 27 Ekim 21:36 – 29 Ekim 17:59 UTC | Sayım |
| --- | --- |
| Günlük kayıtları | 9,968 |
| Yeni mesajlar | 5,308 |
| hesabın tamamına geçişten sonra bunların | 3,878 |
| Silme işlemleri | 784 |
| TgWitness mesajı kaydettikten sonra silinenler | 596 |
| Düzenlemeler | 41 |
| Yeniden kontrollerle eklenen mesajlar | 2,273 |
| Yeniden kontrol sonucunda artık bulunamayan mesajlar | 18 |
| Geçmiş anlık görüntüleri ile kaydedilen mesajlar | 242 |
| Kaydedilen ekler | 247 |
| Toplayıcı başlatılıyor | 19 |
| Telegram FloodWait duraklatılır | 26 |

- Panelin **Verify** kontrolü, 9.968 kaydın tamamının imzalarını ve hash zincirini doğruladı.
- Mesajlar 2 grup veya kanaldan ve 3 özel sohbet ile botlardan geldi. **Sohbetler** bölümünden bir mesaj düğmesi basıldı; istek ve Telegram'ın yanıtı günlüğünde yer almaktadır.
- Toplayıcı, yeniden başlatma sırasında hesabı yeniden taradığında yeni sohbetler eklendi. Yeni sohbetlerin önceki mesajlarının kaydedilmesi devre dışıydı (`history = 0`), bu nedenle bu konuda burada yer almamaktadır.

Kapsam dışı olanlar: tepkiler, üyelik değişiklikleri, kişi profilleri, mesaj gönderme, davet yoluyla katılma, vekiller, bildirimler, witness botu ve aynı anda birden fazla hesap. Genel dosyalar yalnızca sayı bilgilerini içerir.

## Şifre korumalı dışa aktarım, libarchive ile açıldı · 29 Ekim 2026

Dışa aktarma şifreleme kodu ile oluşturulmuş bir arşiv (WinZip AES-256, 7-Zip ve WinRAR tarafından okunabilen format), Windows `tar` (bsdtar 3.6.2, libarchive) ile açıldı. Doğru şifre girildiğinde çıkarılan dosyanın SHA-256 değeri orijinaliyle eşleşti; yanlış şifre girildiğinde ise "Yanlış şifre" uyarısı verildi. 7-Zip ve WinRAR programları çalıştırılmadı.

## Canlı Telegram testi · 27–29 Ekim 2026

Yerleşik API çift havuzu aracılığıyla oturum açılmış tek bir gerçek Telegram hesabı, **27 Ekim 21:36 UTC**'den **29 Ekim 05:15 UTC'ye kadar** bir süper grubu kaydetti. Toplayıcı, bu süre zarfında 12 kez başlatıldı.

| Kaydedildi | Sayım |
| --- | --- |
| Kalp atışları ve hizmet kayıtları dahil olmak üzere günlük kayıtları | 2,385 |
| Yeni mesajlar | 1,291 |
| Silme işlemleri | 472 |
| TgWitness metni kaydettikten sonra silinenler | 347 |
| Düzenlemeler | 12 |
| Durdurulmuşken kaçırılan mesajlar, yeniden kontrol sırasında eklenmiştir | 12 |
| Kaydedilen ekler | 17 |
| Ekler indirilmedi (indirme özelliği kapalı veya indirilecek dosya yok) | 14 |
| Telegram FloodWait, yeniden kontroller sırasında her seferinde 3 saniye ara verir | 8 |

- Toplam 2.385 kaydın imzaları ve hash zinciri, günlüğün açık anahtarıyla doğrulanır.
- Yeniden başlatmanın ardından toplayıcı, kaydedilmiş güncelleme durumundan (`pts`) devam eder ve Telethon eksiklikleri giderir; ardından yeniden kontrol işlemi, hâlâ eksik olan mesajları ekler.
- Her FloodWait durumunda, toplayıcı istenen süreyi bekledikten sonra işleme devam etti.
- Hesap oturum açık kaldı ve aynı oturum 29 Ekim'de yeniden bağlandı.

Bu test kapsamında olmayanlar: aynı anda birden fazla hesap, yönetici rolleri, proxy'ler, birkaç saatten uzun süren kesintiler ve tam [canlı kabul prosedürü](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Halka açık dosyalar yalnızca şu bilgileri içerir: hesap veya sohbet kimlikleri, mesajlar ya da kimlik bilgileri bulunmaz.

## Sentetik yerel kapasite ölçümü

Komut: `python tools/check_capacity.py --events 10000 --chats 100`

| Metrik | Gözlemlenen |
| --- | --- |
| Giriş | Seçilen 100 sentetik kaynaktan elde edilen 10.000 sentetik mesaj olayı |
| Mesaj metni | 400 karakter; medya veya ağ içermez |
| Verilerin Alınması | 53,273 saniye; saniyede 187,7 olay |
| İşleyici gecikmesi | p50 4,162 ms; p95 7,784 ms; maksimum 129,118 ms |
| ZIP olarak dışa aktarma | tracemalloc etkinleştirildiğinde 19,868 saniye |
| Python export tahsisatlarının en yüksek değerleri | 0,51 MiB; RSS işlenmiyor |
| ZIP boyutu | 4.610.962 bayt |
| Bağımsız doğrulama | 10.000 olayın tamamı doğrulanmıştır |

Bu ölçüm, bu Windows sunucusundaki yerel seri kayıt/dışa aktarma yolunu ölçer. MTProto teslimatı, eşzamanlı hesaplar, Telegram hız sınırlaması, medya, uzun süreli iş yükü veya garantili gerçek sohbet sayısını ölçmez. Bu ölçüm, ölçülen mesaj yolunu değiştirmeyen nihai çevrimdışı zaman damgası araçlarından önce gerçekleştirilmiştir.

## Kalan nitelikler

Saklanan canlı günlük, gerçek toplama işlemlerini, düzenlemeleri, silme bildirimlerini, ekleri, yeniden kontrolleri ve hız sınırlaması yönetimini kaydeder. Bu günlük, kapsamlı teslimat bilgilerini veya rol görünürlüğü, tepki veren aktörler, uzatılmış FloodWait, hesap yasaklamaları ve ağ/işlem kesintisi kurtarma işlemlerini içeren kontrollü bir matris kaydetmez. QR jetonu düzenleme işlemi, tamamlanmış mobil QR onayı işleminden ayrıdır.

Docker derleme/çalıştırma, Linux/macOS kurulumu, sürekli yüksek yük, bağımsız güvenlik incelemesi, gerçek bir bağımsız TSA yanıtı, sertifika iptal/arşivleme doğrulaması ve adli sertifikasyon, kaydedilen yeterlilik kapsamı dışında kalmaktadır. Kaydedilmiş MTProto durumu ve yakalama işlevleri uygulanmaktadır; atomik kalıcı tekrar oynatma ise henüz kurulmamıştır. Yönetici günlüğü toplama, ek reaktör listeleri ve öncelikli kısa sorgulama ayrı özellikler olarak kalmaktadır. Kontrollü yeterlilik matrisi için [canlı kabul](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) bölümüne bakınız.

Yerel ayrıntılı makbuzlar ve ekran görüntüleri test-results/ dizininde bulunur (Git tarafından göz ardı edilir). docs/assets/ dizinindeki herkese açık ekran görüntüsü yalnızca kurgusal örnek veriler içerir.
