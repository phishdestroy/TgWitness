# Muat sejarah sumber

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/

Muat mesej lepas daripada sumber yang diaktifkan, berehat dan sambung semula, serta sahkan laporan kemajuan yang ditandatangani.

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Pause, mula semula dan keputusan separa

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Pengamatan mesej, pemprosesan lampiran dan komitmen penunjuk dalam satu transaksi. Jalankan semula tidak akan mengulangi pengamatan yang telah dikomit. Rakaman langsung atau jalankan berasingan yang dimulakan secara eksplisit boleh memerhati mesej yang sama secara bebas.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Sumber yang tidak dapat diakses dan sumber yang dilumpuhkan semasa pengambilan kekal kelihatan sebagai gagal atau dilangkau. Sumber lain diteruskan; keputusan keseluruhan tidak lengkap.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Penyempurnaan sejarah menerangkan bacaan sejarah sahaja. Lampiran mungkin kekal menunggu, gagal, atau dikecualikan oleh dasar yang dikonfigurasikan. Semak resit media dalam jurnal dan barisan menunggu lampiran; hanya resit yang disempurnakan dengan bait yang terpelihara dianggap sebagai lampiran yang disimpan. Operasi sejarah adalah permintaan snapshot eksplisit dan berasingan daripada suis yang memilih kategori acara langsung akan datang.

## Pindahkan dan sahkan

Simpan **laporan kemajuan yang ditandatangani**, kemudian gunakan **Eksport bukti** untuk memuat turun jurnal dan lampiran yang disimpan. Eksport bukti kemudian mungkin termasuk rekod tambahan; laporan ini mengikat pengiraannya kepada awalan jurnal pada masa ia dibuat. Jalankan pengesah daripada tarikan semak yang dipercayai bagi versi ini:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Penunjuk pemerolehan adalah status ruang kerja tempatan. Memulihkan ZIP bukti sahaja tidak memulihkan kerja pemerolehan yang tertangguh atau sesi Telegram. Simpan sandaran ruang kerja jika sambungan kerja asal diperlukan.
