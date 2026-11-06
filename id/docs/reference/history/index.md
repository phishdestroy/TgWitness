# Muat riwayat sumber

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/history/

Muat pesan-pesan sebelumnya dari sumber yang diaktifkan, jeda dan lanjutkan, serta verifikasi laporan kemajuan yang telah ditandatangani.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Koleksi](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Jeda, mulai ulang, dan hasil parsial

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Pengamatan pesan, pemrosesan lampiran, dan pencatatan posisi kursor dilakukan dalam satu transaksi. Proses yang dilanjutkan tidak akan mengulangi pengamatan yang telah dicatat sebelumnya. Penangkapan langsung atau proses terpisah yang dimulai secara eksplisit dapat mengamati pesan yang sama secara independen.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Sumber yang tidak dapat diakses dan sumber yang dinonaktifkan selama proses pengumpulan tetap terlihat sebagai gagal atau dilewati. Sumber lainnya tetap berlanjut; hasil keseluruhan tidak lengkap.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Penyelesaian riwayat hanya menggambarkan pembacaan riwayat. Lampiran mungkin tetap dalam status tertunda, gagal, atau dikecualikan oleh kebijakan yang dikonfigurasi. Periksa tanda terima media di jurnal dan antrian lampiran; hanya tanda terima yang telah selesai dengan byte yang terpelihara yang dianggap sebagai lampiran yang tersimpan. Operasi riwayat merupakan permintaan snapshot eksplisit dan terpisah dari opsi yang memilih kategori peristiwa langsung di masa mendatang.

## Transfer dan verifikasi

Simpan **laporan kemajuan** yang **telah ditandatangani**, lalu gunakan **"Ekspor Bukti"** untuk mengunduh jurnal dan lampiran yang disimpan. Ekspor bukti di kemudian hari mungkin mencakup catatan tambahan; laporan tersebut mengikat penghitungnya ke awalan jurnal pada saat dibuat. Jalankan verifikator dari salinan tepercaya versi ini:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Kursor akuisisi menunjukkan status ruang kerja lokal. Memulihkan berkas ZIP bukti saja tidak akan memulihkan tugas akuisisi yang tertunda atau sesi Telegram. Simpan cadangan ruang kerja jika Anda perlu melanjutkan tugas asli.
