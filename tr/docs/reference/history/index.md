# Kaynak geçmişini yükle

Canonical page: https://phishdestroy.github.io/TgWitness/tr/docs/reference/history/

Etkinleştirilmiş kaynaklardan geçmiş mesajları yükleyin, işlemi duraklatıp devam ettirin ve imzalı bir ilerleme raporunu doğrulayın.

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Duraklatma, yeniden başlatma ve kısmi sonuçlar

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Mesaj gözlemi, ekleme işlemi ve imleç kaydı tek bir işlemde gerçekleştirilir. Devam ettirilen bir çalıştırma, daha önce kaydedilmiş gözlemleri tekrarlamaz. Canlı yakalama veya ayrı, açıkça başlatılan bir çalıştırma, aynı mesajı bağımsız olarak gözlemleyebilir.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Erişilemeyen kaynaklar ve toplama sırasında devre dışı bırakılan kaynaklar, başarısız veya atlanmış olarak görünür kalır. Diğer kaynaklar devam eder; genel sonuç eksik kalır.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Geçmiş tamamlama, yalnızca geçmiş okumalarını tanımlar. Ekler beklemede kalabilir, başarısız olabilir veya yapılandırılmış ilke nedeniyle hariç tutulabilir. Günlükteki medya alım teyitlerini ve ek kuyruğunu kontrol edin; yalnızca baytları korunmuş tamamlanmış bir alım teyidi, kaydedilmiş bir eki oluşturur. Geçmiş işlemi, açık bir anlık görüntü isteğidir ve gelecekteki canlı olay kategorilerini seçen anahtarlardan ayrıdır.

## Aktar ve doğrula

**İmzalı ilerleme**raporunu kaydedin, ardından "**Kanıtları Dışa Aktar"** seçeneğini kullanarak günlüğü ve kaydedilmiş ekleri indirin. Daha sonra gerçekleştirilecek bir kanıt dışa aktarma işlemi ek kayıtlar içerebilir; rapor, sayacılarını oluşturulduğu andaki günlük önekine bağlar. Bu sürümün güvenilir bir kopyasından doğrulayıcıyı çalıştırın:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Alım imleci, yerel çalışma alanının durumunu gösterir. Yalnızca bir kanıt ZIP dosyasını geri yüklemek, bekleyen bir alım işini veya Telegram oturumunu geri yüklemez. Orijinal işin devam ettirilmesi gerekiyorsa çalışma alanı yedeğini saklayın.
