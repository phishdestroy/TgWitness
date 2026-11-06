# ماخذ کی تاریخ لوڈ کریں

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/reference/history/

ممکنہ ذرائع سے گزشتہ پیغامات لوڈ کریں، وقفہ کریں اور دوبارہ شروع کریں، اور ایک دستخط شدہ پیش رفت رپورٹ کی تصدیق کریں۔

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## وقف، دوبارہ شروع اور جزوی نتائج

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- پیغام کا مشاہدہ، منسلک کی کارروائی اور کرسر کا کمٹ ایک ہی ٹرانزیکشن میں۔ دوبارہ شروع ہونے والا رن اپنے پہلے ہی کمٹ شدہ مشاہدات کو دہراتا نہیں ہے۔ لائیو کیپچر یا ایک الگ، واضح طور پر شروع کیا گیا رن آزادانہ طور پر اسی پیغام کا مشاہدہ کر سکتا ہے۔
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- غیر قابل رسائی ذرائع اور حصول کے دوران غیر فعال کیے گئے ذرائع 'ناکام' یا 'چھوڑا گیا' کے طور پر دکھائی دیتے رہتے ہیں۔ دیگر ذرائع جاری رہتے ہیں؛ مجموعی نتیجہ نامکمل رہتا ہے۔
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

تاریخ کی تکمیل صرف تاریخ کے ریڈز کو بیان کرتی ہے۔ منسلکات زیر التواء رہ سکتے ہیں، ناکام ہو سکتے ہیں، یا ترتیب دی گئی پالیسی کے تحت خارج کیے جا سکتے ہیں۔ جرنل اور منسلکات کی قطار میں میڈیا رسیدیں چیک کریں؛ صرف ایک مکمل رسید جس میں بائٹس محفوظ ہوں، ایک محفوظ شدہ منسلک کے طور پر شمار ہوتی ہے۔ تاریخ کا آپریشن ایک واضح سنپ شاٹ کی درخواست ہے اور یہ ان سوئچز سے الگ ہے جو مستقبل کے لائیو ایونٹس کی زمروں کا انتخاب کرتے ہیں۔

## منتقل کریں اور تصدیق کریں

**دستخط شدہ پیش رفت رپورٹ** محفوظ کریں، پھر **شواہد برآمد** کریں تاکہ جرنل اور محفوظ شدہ منسلکات ڈاؤن لوڈ کیے جا سکیں۔ بعد میں شواہد کی برآمد میں اضافی ریکارڈز شامل ہو سکتے ہیں؛ رپورٹ اپنے کاؤنٹرز کو اس جرنل کے پری فکس سے منسلک کرتی ہے جس وقت یہ بنائی گئی تھی۔ تصدیق کنندہ کو اس ورژن کے ایک معتبر چیک آؤٹ سے چلائیں:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

حصولی نشانہ مقامی ورک اسپیس کی حالت ہے۔ صرف ثبوت کا ZIP بحال کرنا زیر التواء حصولی کام یا ٹیلیگرام سیشن کو بحال نہیں کرتا۔ اگر اصل کام کے تسلسل کی ضرورت ہو تو ورک اسپیس کا بیک اپ رکھیں۔
