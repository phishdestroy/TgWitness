# بارگذاری تاریخچه منبع

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/reference/history/

بارگذاری پیام‌های گذشته از منابع فعال، مکث و از سرگیری، و تأیید گزارش پیشرفت امضا شده.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [مستندسازی](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [مجموعه](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## تعطیل، راه‌اندازی مجدد و نتایج جزئی

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- مشاهده پیام، انجام عملیات پیوست و ثبت مکان نما در یک تراکنش واحد. اجرای از سر گرفته شده مشاهدات ثبت‌شده قبلی را تکرار نمی‌کند. ضبط زنده یا اجرای جداگانه و صراحتاً آغازشده می‌تواند به‌طور مستقل همان پیام را مشاهده کند.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- منابع غیرقابل‌دسترس و منابعی که در حین جمع‌آوری غیرفعال شده‌اند، همچنان به‌عنوان «ناموفق» یا «نادیده گرفته شده» قابل مشاهده‌اند. سایر منابع به کار خود ادامه می‌دهند؛ نتیجه کلی ناقص است.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

تکمیل تاریخچه، فقط خواندنی است. ضمیمه‌ها ممکن است در حالت انتظار باقی بمانند، ناموفق باشند، یا توسط سیاست پیکربندی‌شده مستثنی شوند. رسیدهای رسانه را در دفترچه و صف ضمیمه‌ها بررسی کنید؛ تنها یک رسید تکمیل‌شده با بایت‌های حفظ‌شده، یک ضمیمه ذخیره‌شده را تشکیل می‌دهد. عملیات تاریخچه یک درخواست اسنپ‌شات صریح است و از سوئیچ‌هایی که دسته‌های رویدادهای زنده آینده را انتخاب می‌کنند، مستقل است.

## انتقال و تأیید

**گزارش پیشرفت امضا شده** را ذخیره کنید، سپس از **«صادرات شواهد»** برای دانلود دفترچه و پیوست‌های ذخیره شده استفاده کنید. یک صادرات شواهد بعدی ممکن است شامل سوابق اضافی باشد؛ گزارش شمارشگرهای خود را به پیشوند دفترچه در زمان ایجاد آن متصل می‌کند. راستابار را از یک نسخه برداری معتبر از این نسخه اجرا کنید:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

نشانگر اکتشاف وضعیت فضای کاری محلی است. بازیابی یک فایل ZIP مدرک به تنهایی، شغل اکتشافی در حال انتظار یا جلسه تلگرام را بازیابی نمی‌کند. اگر ادامه شغل اصلی لازم است، از پشتیبان فضای کاری نگهداری کنید.
